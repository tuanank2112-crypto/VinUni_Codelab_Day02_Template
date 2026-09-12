import copy
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "starter-code"))
import prompt_prototype as p
import incident_engine as e


def valid():
    return {"draft_only": True, "requires_human_review": True, "cause_confirmed": False,
            "action": "propose_review", "tickets": [{"id": "T001", "symptom": "low_water", "emergency": False}]}


def source():
    return {"tickets": [{"id": "T001", "text": "Vòi sen nước yếu"}]}


def test_valid_output():
    assert p.validate_output(json.dumps(valid()), source()) == valid()


@pytest.mark.parametrize("field,value", [("draft_only", False), ("requires_human_review", False),
                                         ("cause_confirmed", True), ("action", "close_ticket"),
                                         ("action", "close_water_valve"),
                                         ("draft_only", "true"), ("resident_phone", "123")])
def test_invalid_boundaries(field, value):
    output = valid()
    output[field] = value
    with pytest.raises(ValueError):
        p.validate_output(json.dumps(output), source())


@pytest.mark.parametrize("ids", [[], ["T999"], ["T001", "T001"]])
def test_wrong_ids(ids):
    output = valid()
    output["tickets"] = [{"id": i, "symptom": "low_water", "emergency": False} for i in ids]
    with pytest.raises(ValueError):
        p.validate_output(json.dumps(output), source())


@pytest.mark.parametrize("raw", ["", "not json", '```json\n{}\n```', "[]"])
def test_malformed_output(raw):
    with pytest.raises(ValueError):
        p.validate_output(raw, source())


def test_input_duplicates():
    data = source()
    data["tickets"] *= 2
    with pytest.raises(ValueError):
        p.validate_input(data)


@pytest.mark.parametrize("args", [[], ["--offline"]])
def test_local_cli_propagates_test_result(monkeypatch, args):
    import subprocess
    calls = []
    monkeypatch.setattr(sys, "argv", ["prompt_prototype.py", *args])
    monkeypatch.setenv("GEMINI_API_KEY", "test-only")
    def fake_call(command, **kwargs):
        calls.append(command)
        return 1
    monkeypatch.setattr(subprocess, "call", fake_call)
    monkeypatch.setattr(p, "run_live", lambda: pytest.fail("Offline must not call Gemini"))
    assert p.main() == 1
    assert calls[0][1:4] == ["-m", "pytest", "-v"]


def test_explicit_live_requires_key(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prompt_prototype.py", "--live"])
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    assert p.main() == 2


def test_sdk_path_with_fake_transport(monkeypatch):
    from google import genai
    from types import SimpleNamespace
    calls = []
    class FakeClient:
        def __init__(self, **kwargs):
            self.models = self
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
        def generate_content(self, **kwargs):
            calls.append(kwargs)
            return SimpleNamespace(text=json.dumps(valid()))
    monkeypatch.setattr(genai, "Client", FakeClient)
    monkeypatch.setenv("GEMINI_API_KEY", "test-only")
    result = p.evaluate_prompt(json.dumps(source()))
    assert p.validate_output(result, source()) == valid()
    assert calls[0]["config"].system_instruction == p.SYSTEM_PROMPT
    assert json.loads(calls[0]["contents"]) == source()
    assert calls[0]["config"].response_json_schema == p.Proposal.model_json_schema()


def fixture():
    return json.loads((e.ROOT / "data/scenario.json").read_text())


def test_grouping_and_urgent_override():
    data = fixture()
    # Even when the fixture/model misses urgency, rule guard promotes smoke.
    data["fixture_extractions"][5]["emergency"] = False
    output = e.propose_groups(data["tickets"], data["topology"], data["fixture_extractions"])
    assert output["groups"][0]["ticket_ids"] == ["T001", "T002", "T003"]
    assert "T004" in output["manual_review"]  # AC water leak
    assert "T005" in output["manual_review"]  # missing location
    assert "T021" in output["manual_review"]  # contradictory evidence
    assert "T006" in output["urgent_review"]
    assert all(not g["cause_confirmed"] for g in output["groups"])


def test_windows_do_not_chain():
    tickets = [{"id": str(i), "minute": m, "apartment": "A1201", "text": "Nước yếu"}
               for i, m in enumerate([0, 14, 28])]
    extraction = [{"id": str(i), "symptom": "low_water", "emergency": False} for i in range(3)]
    output = e.propose_groups(tickets, {"A1201": "A-R1"}, extraction)
    assert [len(g["ticket_ids"]) for g in output["groups"]] == [2, 1]


def test_different_tower_stays_separate():
    data = fixture()
    tickets = [data["tickets"][0], dict(data["tickets"][6], minute=0)]
    output = e.propose_groups(tickets, data["topology"], [data["fixture_extractions"][i] for i in (0, 6)])
    assert len(output["groups"]) == 2


@pytest.mark.parametrize("constraint", ["skills", "shift", "access", "materials", "dependency", "availability", "deadline"])
def test_infeasible_plans_block(constraint):
    data = fixture()
    tech = copy.deepcopy(data["technicians"][:1])
    job = e.task("job", "A-R1", 0)
    stock = {"valve": 1}
    if constraint == "skills": tech[0]["skills"] = ["hvac"]
    if constraint == "shift": tech[0]["shift"] = [0, 10]
    if constraint == "access": job["access"] = [50, 60]
    if constraint == "materials": job["materials"] = {"valve": 2}
    if constraint == "dependency": job["depends_on"] = ["missing"]
    if constraint == "availability": tech[0]["available_from"] = 479
    if constraint == "deadline": job["deadline"] = 10
    result = e.schedule([job], tech, stock)
    assert result["blocked"] and not result["scheduled"]


def test_precedence_stock_and_no_overlap():
    data = fixture()
    jobs = [e.task("repair", "A-R1", 0, materials={"valve": 1}),
            e.task("verify", "A-R1", 0, depends_on=["repair"]),
            e.task("other", "A-R1", 0, materials={"valve": 1})]
    result = e.schedule(jobs, data["technicians"][:1], {"valve": 1})
    a, b = result["scheduled"]
    assert b["start"] >= a["end"]
    assert result["blocked"][0]["task_id"] == "other"


def test_review_evidence_and_partial_closure():
    incident = {"status": "hypothesis", "ticket_ids": ["T1", "T2"]}
    with pytest.raises(ValueError): e.transition(incident, "inspection_planned")
    with pytest.raises(ValueError): e.transition(incident, "closed", approved=True)
    incident["status"] = "inspection_planned"
    with pytest.raises(ValueError): e.transition(incident, "inspected", approved=True)
    incident["status"] = "verification"
    with pytest.raises(ValueError):
        e.transition(incident, "closed", approved=True, evidence={"resolved_ticket_ids": ["T1"]})
    assert e.transition(incident, "closed", approved=True, evidence={"resolved_ticket_ids": ["T1", "T2"]})["status"] == "closed"


def test_repair_requires_confirmed_cause():
    with pytest.raises(ValueError):
        e.transition({"status": "inspected", "cause_confirmed": False}, "repair_planned", approved=True)


def test_demo_reassigns_and_preserves_open_tickets():
    output = e.demo()
    assert output["ticket_count"] == 60 and output["partial_close_blocked"]
    assert output["initial_plan"]["scheduled"][0]["technician"] != output["replanned"]["scheduled"][0]["technician"]
    assert output["final_incident"]["status"] == "closed"
