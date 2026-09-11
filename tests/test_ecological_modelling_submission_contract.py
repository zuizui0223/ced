from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "manuscript" / "CED_SUBMISSION_STATUS_2026-09-11.json"
CHECKLIST = ROOT / "submission" / "ECOLOGICAL_MODELLING_SUBMISSION_CHECKLIST.md"
HIGHLIGHTS = ROOT / "submission" / "ECOLOGICAL_MODELLING_HIGHLIGHTS.md"
MAIN = ROOT / "manuscript" / "paper_b_main.tex"


def _status() -> dict:
    return json.loads(STATUS.read_text(encoding="utf-8"))


def _highlight_bullets() -> list[str]:
    rows = []
    for line in HIGHLIGHTS.read_text(encoding="utf-8").splitlines():
        if line.startswith("- "):
            rows.append(line[2:])
    return rows


def test_standalone_ced_is_current_ecological_modelling_route() -> None:
    status = _status()
    assert status["paper"] == "CED"
    assert status["target_journal"] == "Ecological Modelling"
    assert status["status"] == "standalone-reframing-active"
    assert "manuscript/paper_b_main.tex" in status["canonical_scientific_base"]
    assert status["science_blocker"] is False


def test_historical_integrated_evidence_does_not_replace_standalone_paper() -> None:
    status = _status()
    assert "manuscript/EVIDENCE_DRAFT_V1.md" in status["historical_integrated_evidence_assets"]
    assert "do not describe" in status["historical_asset_policy"]
    assert MAIN.exists()


def test_ecological_modelling_package_exists() -> None:
    assert CHECKLIST.exists()
    assert HIGHLIGHTS.exists()
    checklist = CHECKLIST.read_text(encoding="utf-8")
    assert "Ecological Modelling" in checklist
    assert "scientific core unchanged" in checklist
    assert "Boundary owns" in checklist
    assert "MROD owns" in checklist


def test_elsevier_highlights_are_short_and_count_limited() -> None:
    bullets = _highlight_bullets()
    assert 3 <= len(bullets) <= 5
    assert all(len(row) <= 85 for row in bullets)
    assert any("target" in row.lower() for row in bullets)
    assert any("failure" in row.lower() for row in bullets)


def test_active_ced_manuscript_retains_standalone_identity() -> None:
    text = MAIN.read_text(encoding="utf-8")
    assert "full-world information" in text
    assert "target-safe" in text
    assert "failure" in text.lower()
    assert "MROD learning utility" not in text
