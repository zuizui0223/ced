import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check_mee_submission.py"


def test_mee_checker_passes_machine_structure_and_surfaces_human_decisions():
    report = runpy.run_path(str(CHECKER))["build_report"]()

    assert report["schema_version"] == 1
    assert report["journal"] == "Methods in Ecology and Evolution"
    assert report["article_type"] == "Standard Research Article"
    assert report["hard_checks_pass"]
    assert all(report["hard_checks"].values())

    metrics = report["metrics"]
    assert metrics["abstract_rough_words"] <= 350
    assert metrics["keyword_count"] == 8
    assert metrics["top_level_sections"] == [
        "Introduction",
        "Materials and Methods",
        "Results",
        "Discussion",
    ]
    assert metrics["identity_hits_in_main_manuscript"] == []
    assert metrics["rough_total_words_including_generated_bibliography_and_reviewer_sections"] <= 8000

    # These are deliberate author / rights-holder decisions, not values for CI to invent.
    assert not report["author_decisions"]["open_source_license_present"]
    assert not report["author_decisions"]["separate_title_page_present"]
    assert not report["author_decisions"]["ai_llm_disclosure_present_in_methods"]
    assert "open_source_license_present" in report["submission_blockers_requiring_human_decision"]
    assert "ai_llm_disclosure_present_in_methods" in report["submission_blockers_requiring_human_decision"]
