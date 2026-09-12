"""Reproducible hand-designed synthetic data; no real resident information."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
topology = {f"{tower}{floor:02}{unit:02}": f"{tower}-R{1 if unit == 1 else 2}"
            for tower in "AB" for floor in range(12, 17) for unit in (1, 5)}
texts = ["Vòi sen chảy rất yếu.", "Máy giặt không lấy được nước.", "Bồn rửa gần như mất nước.",
         "Điều hòa chảy nước.", "Nước yếu nhưng không rõ căn hộ.", "Nước ngập gần tủ điện có khói."]
tickets, extracts, truth = [], [], []
for i in range(60):
    batch, kind = divmod(i, 6)
    tower = "A" if batch % 2 == 0 else "B"
    apartment = f"{tower}{12 + kind % 3:02}{1 if kind < 3 else 5:02}"
    text = texts[kind]
    conflict = batch == 3 and kind == 2
    if conflict:
        text += " Ghi chú tổng đài lại ghi nước vẫn bình thường, cần gọi xác minh."
    tickets.append({"id": f"T{i+1:03}", "apartment": None if kind == 4 else apartment,
                    "minute": batch*30 + kind*5, "text": text, "conflict": conflict,
                    "access": [batch*30, 480]})
    extracts.append({"id": f"T{i+1:03}", "symptom": ["low_water", "no_water", "no_water", "ac_leak", "low_water", "other"][kind],
                     "emergency": kind == 5})
    # Same topology/symptom but different root cause in two batches: hard negatives.
    cause = f"common-{batch}" if kind < 3 else f"separate-{i}"
    if batch in (4, 7) and kind == 2:
        cause = f"local-valve-{i}"
    truth.append({"id": f"T{i+1:03}", "synthetic_cause": cause})
data = {"description": "60 synthetic tickets. fixture_extractions are authored labels, NOT LLM outputs.",
        "tickets": tickets, "fixture_extractions": extracts, "topology": topology,
        "technicians": [{"id": f"K{i+1}", "skills": ["water"] if i < 3 else ["hvac"],
                         "shift": [0, 480], "available_from": 0,
                         "zone": "A-R1" if i % 2 == 0 else "B-R1"} for i in range(4)],
        "inventory": {"valve": 1, "pressure_gauge": 2}}
(root / "data/scenario.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
(root / "data/ground-truth.json").write_text(json.dumps(truth, ensure_ascii=False, indent=2) + "\n")
