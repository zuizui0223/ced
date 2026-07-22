import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_paper_b_figures.py"


def test_figure_generator_uses_validated_schema_and_writes_expected_values(tmp_path):
    module = runpy.run_path(str(SCRIPT))
    module["OUT_DIR"] = tmp_path
    module["OUT_CONTRAST"] = tmp_path / "contrast.tex"
    module["OUT_OUTCOMES"] = tmp_path / "outcomes.tex"

    report = module["write_figures"]()

    assert report["schema_version"] == 5
    contrast = (tmp_path / "contrast.tex").read_text(encoding="utf-8")
    outcomes = (tmp_path / "outcomes.tex").read_text(encoding="utf-8")

    assert "0.713603" in contrast
    assert "2.000000" in contrast
    assert "Target-resolution probability" in contrast
    assert "Target-safe" in outcomes
    assert "Full-world EIG" in outcomes
    assert "0.994432" in outcomes
    assert "0.549931" in outcomes
