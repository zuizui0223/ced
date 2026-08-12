import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RENDER = ROOT / "scripts" / "render_paper_b_figures.py"
MANUSCRIPT = ROOT / "manuscript" / "paper_b_main.tex"
REVIEWER_SECTIONS = ROOT / "manuscript" / "paper_b_reviewer_sections.tex"


def test_target_safe_quotient_figure_matches_generic_implementation():
    module = runpy.run_path(str(RENDER))
    figure = module["target_safe_quotient_tex"]()

    assert "Current record" in figure
    assert "Target-safe quotient" in figure
    assert "Full latent identity" in figure
    assert "refine only when target" in figure
    assert "extra identity split" in figure
    assert figure.count("$A_0$") == 3
    assert figure.count("$B_1$") == 3


def test_failure_architecture_figure_uses_equal_effort_verified_values():
    module = runpy.run_path(str(RENDER))
    figure = module["failure_architecture_tex"]()

    assert "0.799748" in figure
    assert "0.950069" in figure
    assert "0.800000" in figure
    assert "0.960000" in figure
    assert "30 reads in each design" in figure
    assert "Worst-case guarantee ceiling" in figure


def test_compiled_manuscript_injects_figures_adjacent_to_results():
    module = runpy.run_path(str(RENDER))
    compiled = module["compiled_manuscript_tex"](
        MANUSCRIPT.read_text(encoding="utf-8"),
        REVIEWER_SECTIONS.read_text(encoding="utf-8"),
    )

    quotient_label = r"\label{fig:target-safe-quotient}"
    result3 = r"\subsection{Result 3: failure architecture determines trustworthy refinement}"
    failure_label = r"\label{fig:failure-architecture}"
    result4 = r"\subsection{Result 4: adaptive risk-limited target resolution}"

    assert quotient_label in compiled
    assert failure_label in compiled
    assert compiled.index(quotient_label) < compiled.index(result3)
    assert compiled.index(failure_label) < compiled.index(result4)
    assert "not universal upper bounds on realized detection" in compiled
