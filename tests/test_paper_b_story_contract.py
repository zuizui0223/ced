from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "paper_b_main.tex"
CONSOLIDATION = ROOT / "docs" / "paper_b_theorem_consolidation.md"


def test_main_manuscript_uses_mee_structure_and_four_result_spine():
    text = MANUSCRIPT.read_text(encoding="utf-8")

    required = (
        r"\title{When full-world information misses the ecological target:",
        r"\section*{Data and code for peer review}",
        r"\section*{Keywords}",
        r"\section{Introduction}",
        r"\section{Materials and Methods}",
        r"\section{Results}",
        r"\subsection{Result 3: failure architecture determines trustworthy refinement}",
        r"\subsection{Result 4: adaptive risk-limited target resolution}",
        r"\paragraph{Results 1--2: the reporting infrastructure.}",
        r"\subsection{Result 1: experiment-induced quotient and honest reporting}",
        r"\subsection{Result 2: minimal resolution of future-relevant distinctions}",
        r"\section{Discussion}",
        "Otherwise, the honest ecological prediction remains a set",
    )
    for marker in required:
        assert marker in text

    assert r"\section{Modelling framework}" not in text
    assert r"\section{Conclusion}" not in text
    assert text.index(required[3]) < text.index(required[4]) < text.index(required[5]) < text.index(required[11])
    assert text.index(required[6]) < text.index(required[7]) < text.index(required[8])
    assert text.index(required[8]) < text.index(required[9]) < text.index(required[10])
    assert "present them in consequence-first order" in text
    assert "The central distinction is finite reportability, not target orientation by itself" in text


def test_exact_to_risk_relaxation_layer_is_explicit_and_ordered():
    text = MANUSCRIPT.read_text(encoding="utf-8")

    finite = r"\subsection{Finite evidence problem}"
    relaxation = r"\subsection{Exact reportability and the risk-limited relaxation}"
    failure = r"\subsection{Observation-failure contract}"
    result4 = r"\subsection{Result 4: adaptive risk-limited target resolution}"

    for marker in (finite, relaxation, failure, result4):
        assert marker in text
    assert text.index(finite) < text.index(relaxation) < text.index(failure)

    relaxation_text = text.split(relaxation, 1)[1].split(failure, 1)[0]
    for phrase in (
        "exact support-level baseline",
        "declared false-resolution budget",
        "risk-limited singleton",
        "set-valued report or abstention",
        "does not turn finite nondetection into deductive absence",
    ):
        assert phrase in relaxation_text

    result4_text = text.split(result4, 1)[1].split(r"\subsection{Comparative benchmark}", 1)[0]
    assert "explicit relaxation of the exact support-level rule" in result4_text


def test_consolidation_demotes_supporting_theorem_families_instead_of_deleting_them():
    text = CONSOLIDATION.read_text(encoding="utf-8")

    assert "Do **not** make this a fifth main result" in text
    assert "Calibration and threshold theorem family" in text
    assert "Posterior-sample bridge" in text
    assert "supporting mathematics" in text.lower()
    assert "No additional theorem family should be added" in text
