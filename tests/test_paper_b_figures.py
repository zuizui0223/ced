import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_paper_b_figures.py"


def test_figure_generator_uses_validated_schema_and_expected_values():
    module = runpy.run_path(str(SCRIPT))
    benchmark = runpy.run_path(str(module["BENCHMARK"]))
    report = benchmark["run_grid"]()

    contrast = module["experiment_contrast_tex"](report)
    outcomes = module["strategy_outcomes_tex"](report)

    assert report["schema_version"] == 5
    assert "0.713603" in contrast
    assert "2.000000" in contrast
    assert "Target-resolution probability" in contrast
    assert "Target-safe" in outcomes
    assert "Full-world EIG" in outcomes
    assert "0.994432" in outcomes
    assert "0.549931" in outcomes
