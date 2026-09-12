"""Deterministic, local-only incident hypotheses and constrained inspection demo.
Time is minutes from 08:00. Nothing here sends notices or operates equipment.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def propose_groups(tickets, topology, extractions):
    """Anchor each 15-minute window at its FIRST ticket, preventing chained merges."""
    by_id = {e["id"]: e for e in extractions}
    if len(by_id) != len(extractions) or set(by_id) != {t["id"] for t in tickets}:
        raise ValueError("Extraction ids must match source tickets")
    groups, manual, urgent = [], [], []
    for ticket in sorted(tickets, key=lambda t: (t["minute"], t["id"])):
        e = by_id[ticket["id"]]
        # Deterministic high-risk signals augment (never suppress) model flags.
        risk = any(w in ticket["text"].lower() for w in ("khói", "cháy", "điện giật", "tủ điện"))
        if e["emergency"] or risk:
            urgent.append(ticket["id"])
            continue
        zone = topology.get(ticket["apartment"])
        if not zone or ticket.get("conflict") or e["symptom"] not in ("low_water", "no_water"):
            manual.append(ticket["id"])
            continue
        group = next((g for g in groups if g["zone"] == zone and ticket["minute"] - g["first_minute"] <= 15), None)
        if group is None:
            group = {"id": f"I{len(groups)+1:03}", "zone": zone, "first_minute": ticket["minute"],
                     "ticket_ids": [], "reported_apartments": [], "status": "hypothesis",
                     "cause_confirmed": False, "evidence": [],
                     "missing": ["Đo áp lực và kiểm tra nhánh chung", "Xác minh nguyên nhân từng hộ"],
                     "potential_apartments": sorted(a for a, z in topology.items() if z == zone)}
            groups.append(group)
        group["ticket_ids"].append(ticket["id"])
        if ticket["apartment"] not in group["reported_apartments"]:
            group["reported_apartments"].append(ticket["apartment"])
        group["evidence"].append({"ticket_id": ticket["id"], "symptom": e["symptom"],
                                  "zone": zone, "minute": ticket["minute"]})
    return {"groups": groups, "manual_review": manual, "urgent_review": urgent}


def schedule(tasks, technicians, inventory, now=0):
    """Greedy feasible draft; no claim of global optimality, no source mutation.
    Tasks must arrive in dependency order. Missing/unscheduled predecessors block work.
    Travel assumptions: same zone 0, different zone same tower 5, other tower 10 min.
    """
    free = {t["id"]: max(now, t["available_from"], t["shift"][0]) for t in technicians}
    locations = {t["id"]: t["zone"] for t in technicians}
    stock = dict(inventory)
    placed, blocked = {}, []
    if len({t["id"] for t in tasks}) != len(tasks):
        raise ValueError("Duplicate task id")
    for task in tasks:
        reason = None
        if any(p not in placed for p in task["depends_on"]):
            reason = "predecessor_not_scheduled"
        elif any(stock.get(part, 0) < qty for part, qty in task["materials"].items()):
            reason = "missing_material"
        choices = []
        if reason is None:
            ready = max([now, task["release"]] + [placed[p]["end"] for p in task["depends_on"]])
            for tech in technicians:
                if task["skill"] not in tech["skills"]:
                    continue
                zone = locations[tech["id"]]
                travel = 0 if zone == task["zone"] else (5 if zone[0] == task["zone"][0] else 10)
                start = max(free[tech["id"]] + travel, ready, task["access"][0])
                end = start + task["duration"]
                if end <= min(tech["shift"][1], task["access"][1], task["deadline"]):
                    choices.append((end, start, travel, tech["id"]))
        if not choices:
            blocked.append({"task_id": task["id"], "reason": reason or "no_feasible_slot"})
            continue
        end, start, travel, tech_id = min(choices)
        placed[task["id"]] = {"task_id": task["id"], "technician": tech_id, "start": start,
                                "end": end, "travel": travel, "draft_only": True}
        free[tech_id], locations[tech_id] = end, task["zone"]
        for part, qty in task["materials"].items():
            stock[part] -= qty
    return {"draft_only": True, "scheduled": list(placed.values()), "blocked": blocked}


def transition(incident, target, *, approved=False, evidence=None):
    """Demo workflow gate, NOT production authentication. Per-ticket unresolved tracking."""
    allowed = {"hypothesis": "inspection_planned", "inspection_planned": "inspected",
               "inspected": "repair_planned", "repair_planned": "verification", "verification": "closed"}
    if allowed.get(incident["status"]) != target or not approved:
        raise ValueError("Invalid transition or missing human approval")
    if target in ("inspected", "verification", "closed") and not evidence:
        raise ValueError("Field evidence required")
    if target == "repair_planned" and not incident.get("cause_confirmed"):
        raise ValueError("Cannot plan repair without confirmed field cause")
    if target == "closed" and set(evidence.get("resolved_ticket_ids", [])) != set(incident["ticket_ids"]):
        raise ValueError("Unresolved tickets remain open")
    updated = {**incident, "status": target, "history": list(incident.get("history", []))}
    if target == "inspected":
        updated["cause_confirmed"] = evidence.get("common_cause_confirmed") is True
    updated["history"].append({"target": target, "approved": True, "evidence": evidence})
    return updated


def task(identifier, zone, release, *, duration=20, depends_on=None, materials=None):
    return {"id": identifier, "zone": zone, "skill": "water", "duration": duration,
            "release": release, "deadline": 480, "access": [0, 480],
            "depends_on": depends_on or [], "materials": materials or {}}


def demo():
    data = json.loads((ROOT / "data/scenario.json").read_text())
    # Fixture annotations stand in for Gemini ONLY in this offline demo.
    proposal = propose_groups(data["tickets"], data["topology"], data["fixture_extractions"])
    incident = proposal["groups"][0]
    incident = transition(incident, "inspection_planned", approved=True)
    before = schedule([task("inspect", incident["zone"], 15)], data["technicians"], data["inventory"], now=15)
    incident = transition(incident, "inspected", approved=True,
                          evidence={"common_cause_confirmed": True, "note": "GIẢ LẬP: kiểm tra xác nhận van nhánh cần sửa"})
    incident = transition(incident, "repair_planned", approved=True)
    now = before["scheduled"][0]["end"]
    changed = [dict(t) for t in data["technicians"]]
    for tech in changed:
        if tech["id"] == before["scheduled"][0]["technician"]:
            tech["available_from"] = 480  # technician becomes unavailable after inspection
    repair = task("repair", incident["zone"], now, duration=30, materials={"valve": 1})
    verify = task("verify", incident["zone"], now, duration=15, depends_on=["repair"])
    after = schedule([repair, verify], changed, data["inventory"], now=now)
    incident = transition(incident, "verification", approved=True, evidence={"note": "GIẢ LẬP: sửa xong, cần xác minh từng hộ"})
    partial_blocked = False
    try:
        transition(incident, "closed", approved=True, evidence={"resolved_ticket_ids": incident["ticket_ids"][:-1]})
    except ValueError:
        partial_blocked = True
    incident = transition(incident, "closed", approved=True, evidence={"resolved_ticket_ids": incident["ticket_ids"]})
    # Same narrow inspection workload: FIFO vs simple tower batching vs topology batching.
    sample = data["tickets"][:3]
    jobs = {
        "fifo": [task(t["id"], data["topology"][t["apartment"]], t["minute"]) for t in sample],
        "simple_rule": [task("tower-A", "A-R1", 15)],
        "topology_hypothesis": [task("A-R1", "A-R1", 15)],
    }
    comparison = {}
    for mode, work in jobs.items():
        plan = schedule(work, data["technicians"], data["inventory"], now=15)
        comparison[mode] = {"inspection_jobs": len(plan["scheduled"]),
                            "labor_minutes": len(plan["scheduled"])*20,
                            "travel_minutes": sum(j["travel"] for j in plan["scheduled"]),
                            "blocked_jobs": len(plan["blocked"])}
    return {"mode": "offline_fixture_not_llm", "ticket_count": len(data["tickets"]),
            "proposal": proposal, "initial_plan": before, "replanned": after,
            "partial_close_blocked": partial_blocked, "final_incident": incident,
            "inspection_only_comparison": comparison,
            "limitations": "3-ticket illustrative workload only; no disruption/SLA/business improvement claim; simple_rule ties topology here."}


if __name__ == "__main__":
    result = demo()
    (ROOT / "results/offline-demo.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("mode", "ticket_count", "partial_close_blocked", "inspection_only_comparison")}, ensure_ascii=False, indent=2))
