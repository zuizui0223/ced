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
    reviewer_sections = module["REVIEWER_SECTIONS"].read_text(encoding="utf-8")
    compiled = module["compiled_manuscript_tex"](
        module["MANUSCRIPT"].read_text(encoding="utf-8"), reviewer_sections
    )

    assert report["schema_version"] == 5
    assert "0.713603" in contrast
    assert "2.000000" in contrast
    assert "Target-resolution probability" in contrast
    assert "Target-safe" in outcomes
    assert "Full-world EIG" in outcomes
    assert "0.994432" in outcomes
    assert "0.549931" in outcomes
    assert r"\usepackage{pgfplots}" in compiled
    assert r"\input{generated/paper_b_experiment_contrast.tex}" in compiled
    assert r"\input{generated/paper_b_strategy_outcomes.tex}" in compiled
    assert r"\input{generated/paper_b_target_switch.tex}" in compiled
    assert r"\input{generated/paper_b_threshold_sensitivity.tex}" in compiled
    assert r"\bibitem{CanessaEtAl2015}" in compiled
    assert "We do not claim a universal continuous-state convergence theorem" in compiled
    assert compiled.index(r"\label{fig:strategy-outcomes}") < compiled.index(
        r"\subsection{Additional dimensions}"
    )
    assert compiled.index(r"\subsection{Boundary with value of information") < compiled.index(
        r"\section{Discussion}"
    )
