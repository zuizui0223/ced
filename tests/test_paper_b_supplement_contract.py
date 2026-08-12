from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUPPLEMENT = ROOT / "manuscript" / "paper_b_supplement.tex"


def test_supplement_contains_formal_proofs_for_four_result_spine():
    text = SUPPLEMENT.read_text(encoding="utf-8")

    required = (
        r"\section{Result 1: experiment-induced information and honest reporting}",
        r"\begin{theorem}[Record factorization and deterministic report criterion]",
        r"\begin{proposition}[Support-level honest report criterion]",
        r"\section{Result 2: unique coarsest target-safe quotient}",
        r"\begin{theorem}[Unique coarsest target-safe quotient]",
        r"\begin{corollary}[Preservation under every finite declared action word]",
        r"\section{Result 3: lower-bound failure contracts and worst-case guarantee ceilings}",
        r"\begin{proposition}[Exact least-favourable joint-detection frontier]",
        r"\begin{corollary}[Worst-case uniform guarantee ceiling]",
        r"\section{Result 4: finite risk-limited policy existence}",
        r"\begin{theorem}[Least-cost feasible finite policy]",
    )
    for marker in required:
        assert marker in text

    assert "not on what every admissible system can realize" in text
    assert "every valid target-safe interface refines" in text
    assert text.count(r"\begin{proof}") >= 8


def test_supplement_distinguishes_exact_logic_from_posterior_risk_reporting():
    text = SUPPLEMENT.read_text(encoding="utf-8")
    assert "support-level statement is distinct from posterior risk-limited reporting" in text
    assert "provided the declared false-resolution contract allows that risk" in text
