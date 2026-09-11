from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "manuscript" / "CED_SUBMISSION_STATUS_2026-09-11.json"
CHECKLIST = ROOT / "submission" / "ECOLOGICAL_MODELLING_SUBMISSION_CHECKLIST.md"
HIGHLIGHTS = ROOT / "submission" / "ECOLOGICAL_MODELLING_HIGHLIGHTS.md"
COVER = ROOT / "submission" / "ECOLOGICAL_MODELLING_COVER_LETTER_DRAFT.md"
DATA_CODE = ROOT / "submission" / "ECOLOGICAL_MODELLING_DATA_CODE_STATEMENT.md"
PACKAGE = ROOT / "submission" / "ECOLOGICAL_MODELLING_PACKAGE_MANIFEST.json"
MAIN = ROOT / "manuscript" / "paper_b_main.tex"
SUPPLEMENT = ROOT / "manuscript" / "paper_b_supplement.tex"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _highlight_bullets() -> list[str]:
    rows = []
    for line in HIGHLIGHTS.read_text(encoding="utf-8").splitlines():
        if line.startswith("- "):
            rows.append(line[2:])
    return rows


def test_standalone_ced_is_current_ecological_modelling_route() -> None:
    status = _load(STATUS)
    assert status["paper"] == "CED"
    assert status["target_journal"] == "Ecological Modelling"
    assert status["status"] == "standalone-reframing-active"
    assert "manuscript/paper_b_main.tex" in status["canonical_scientific_base"]
    assert status["science_blocker"] is False


def test_historical_integrated_evidence_does_not_replace_standalone_paper() -> None:
    status = _load(STATUS)
    assert "manuscript/EVIDENCE_DRAFT_V1.md" in status["historical_integrated_evidence_assets"]
    assert "do not describe" in status["historical_asset_policy"]
    assert MAIN.exists()
    assert SUPPLEMENT.exists()


def test_ecological_modelling_package_exists() -> None:
    for path in (CHECKLIST, HIGHLIGHTS, COVER, DATA_CODE, PACKAGE):
        assert path.exists()
    checklist = CHECKLIST.read_text(encoding="utf-8")
    package = _load(PACKAGE)
    assert "Ecological Modelling" in checklist
    assert "scientific core unchanged" in checklist
    assert "Boundary owns" in checklist
    assert "MROD owns" in checklist
    assert package["paper"] == "CED"
    assert package["target_journal"] == "Ecological Modelling"
    assert package["canonical_main"] == "manuscript/paper_b_main.tex"
    assert "manuscript/EVIDENCE_DRAFT_V1.md" in package["historical_not_submission_units"]


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


def test_cover_letter_and_data_statement_do_not_overclaim_empirical_validation() -> None:
    cover = COVER.read_text(encoding="utf-8")
    data = DATA_CODE.read_text(encoding="utf-8")
    assert "target-safe ecological reportability" in cover
    assert "no external empirical dataset" in cover.lower()
    assert "do not depend on a newly collected empirical dataset" in data
    assert "model examples" in data


def test_package_manifest_preserves_external_novelty_ownership() -> None:
    package = _load(PACKAGE)
    ownership = package["external_ownership"]
    assert "k-rank(M)" in ownership["boundary"]
    assert "G2" in ownership["mrod"]
    assert "four-failure synthesis" in ownership["c2"]
    forbidden = " ".join(package["forbidden_promotions"]).lower()
    assert "do not absorb boundary" in forbidden
    assert "mrod" in forbidden
