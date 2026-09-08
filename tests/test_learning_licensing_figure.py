from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "make_learning_licensing_figure.py"
RESULT = ROOT / "manuscript" / "evidence_learning_licensing_result.json"

spec = importlib.util.spec_from_file_location("make_learning_licensing_figure", SCRIPT)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_svg_uses_frozen_result_values() -> None:
    payload = json.loads(RESULT.read_text(encoding="utf-8"))
    svg = module.build_svg(payload)
    assert "2 bits" in svg
    assert "1 bits" in svg
    assert ">Nuisance detail<" in svg
    assert ">Target split<" in svg
    assert "Mechanism-learning top: nuisance detail; target-licensing top: target split" in svg


def test_csv_rows_are_deterministic(tmp_path: Path) -> None:
    payload = json.loads(RESULT.read_text(encoding="utf-8"))
    output = tmp_path / "figure.csv"
    module.write_csv(payload, output)
    rows = output.read_text(encoding="utf-8").splitlines()
    assert rows[0] == "candidate,mechanism_information_bits,exact_target_resolution_probability,equal_cost"
    assert rows[1] == "nuisance_detail,2.0,0.0,1.0"
    assert rows[2] == "target_split,1.0,1.0,1.0"
    assert rows[3] == "constant_probe,0.0,0.0,1.0"
