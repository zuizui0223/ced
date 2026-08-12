import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "paper_b_main.tex"
AUDIT = ROOT / "docs" / "paper_b_literature_boundary_audit.md"
RENDER = ROOT / "scripts" / "render_paper_b_figures.py"


def test_adjacent_literatures_are_explicitly_conceded_in_main_text():
    text = MANUSCRIPT.read_text(encoding="utf-8")

    required_phrases = (
        "Occupancy models already separate latent occurrence from observation error",
        "Set-valued reporting is therefore not itself a novelty claim",
        "The framework does not claim that model averaging cannot represent structural uncertainty",
        "Paper B does not claim invention of equivalence classes or partition minimization",
        "Target-safe design is therefore not offered as proof that these approaches cannot target decisions",
        "The benchmark contrasts this contract with full-world entropy reduction, not with optimally specified management VOI",
    )
    for phrase in required_phrases:
        assert phrase in text

    required_citations = (
        "MacKenzieEtAl2002",
        "RoyleLink2006",
        "Manski2003",
        "DormannEtAl2018",
        "Dietze2017",
        "DietzeEtAl2018",
        "NicholsWilliams2006",
        "LindenmayerLikens2009",
        "Williams2011",
        "ChalonerVerdinelli1995",
        "CanessaEtAl2015",
        "GivanDeanGreig2003",
    )
    for key in required_citations:
        assert key in text


def test_generated_bibliography_contains_every_boundary_reference():
    module = runpy.run_path(str(RENDER))
    bibliography = module["bibliography_tex"]()

    required = (
        "MacKenzieEtAl2002",
        "RoyleLink2006",
        "Manski2003",
        "DormannEtAl2018",
        "Dietze2017",
        "DietzeEtAl2018",
        "NicholsWilliams2006",
        "LindenmayerLikens2009",
        "Williams2011",
        "ChalonerVerdinelli1995",
        "CanessaEtAl2015",
        "GivanDeanGreig2003",
    )
    for key in required:
        assert rf"\bibitem{{{key}}}" in bibliography


def test_literature_audit_forbids_straw_man_novelty_claims():
    text = AUDIT.read_text(encoding="utf-8")
    assert "partition refinement" in text.lower()
    assert "VOI rewards information irrespective of management relevance" in text
    assert "question-driven monitoring is new" in text
    assert "set-valued reporting is novel" in text
    assert "equivalence classes, partition refinement" in text
    assert "Paper B links a finite experiment-induced latent-world partition" in text
