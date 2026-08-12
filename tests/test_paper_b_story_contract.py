from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "paper_b_main.tex"
CONSOLIDATION = ROOT / "docs" / "paper_b_theorem_consolidation.md"


def test_main_manuscript_uses_four_result_spine_and_future_focused_conclusion():
    text = MANUSCRIPT.read_text(encoding="utf-8")

    required = (
        r"\title{From ecological states to distinguishable futures:",
        r"\subsection{Result 1: experiment-induced quotient and honest reporting}",
        r"\subsection{Result 2: minimal resolution of future-relevant distinctions}",
        r"\subsection{Result 3: failure architecture determines trustworthy refinement}",
        r"\subsection{Result 4: adaptive risk-limited target resolution}",
        r"\section{Conclusion}",
        "represent what the evidence can report about the future",
    )
    for marker in required:
        assert marker in text

    assert r"\section{Modelling framework}" not in text
    assert text.index(required[1]) < text.index(required[2]) < text.index(required[3]) < text.index(required[4])
    assert text.index(required[4]) < text.index(r"\section{Comparative benchmark}")
    assert text.index(r"\section{Discussion}") < text.index(r"\section{Conclusion}")
    assert "not simply from full-state to target-oriented experimental design" in text


def test_consolidation_demotes_supporting_theorem_families_instead_of_deleting_them():
    text = CONSOLIDATION.read_text(encoding="utf-8")

    assert "Do **not** make this a fifth main result" in text
    assert "Calibration and threshold theorem family" in text
    assert "Posterior-sample bridge" in text
    assert "supporting mathematics" in text.lower()
    assert "No additional theorem family should be added" in text
