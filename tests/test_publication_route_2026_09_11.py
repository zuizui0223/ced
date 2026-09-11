from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "manuscript" / "CED_SUBMISSION_STATUS_2026-09-11.json"
HISTORICAL = ROOT / "manuscript" / "EVIDENCE_SUBMISSION_STATUS.json"
ROUTE = ROOT / "manuscript" / "PUBLICATION_ROUTE_2026-09-11.md"


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_ced_standalone_is_current_submission_route() -> None:
    status = _load(STATUS)
    assert status["status"] == "standalone-production-validated"
    assert status["paper"] == "CED"
    assert status["target_journal"] == "Ecological Modelling"
    assert "manuscript/paper_b_main.tex" in status["canonical_scientific_base"]
    assert "manuscript/paper_b_supplement.tex" in status["canonical_scientific_base"]
    assert status["science_blocker"] is False
    assert ROUTE.exists()


def test_integrated_evidence_is_historical_not_submission_canonical() -> None:
    historical = _load(HISTORICAL)
    assert historical["status"] == "superseded-as-submission-unit"
    assert historical["current_publication_route"] == "manuscript/CED_SUBMISSION_STATUS_2026-09-11.json"
    assert historical["current_submission_identity"] == "CED standalone -> Ecological Modelling"
    assert historical["science_blocker"] is False


def test_boundary_and_mrod_ownership_are_not_absorbed() -> None:
    status = _load(STATUS)
    companions = status["external_companions"]
    assert "identification-geometry owner" in companions["boundary"]
    assert "mechanism-learning observation-design owner" in companions["mrod"]
    witness = status["retained_internal_witness"]
    assert witness["source"] == "ced/learning_licensing.py"
    assert "does not transfer MROD ownership" in witness["role"]
