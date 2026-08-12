"""Report machine-checkable readiness for a Methods in Ecology and Evolution submission.

This checker deliberately distinguishes hard manuscript-structure checks from author
or rights-holder decisions. It never chooses a software license, author list,
conflict-of-interest statement, contribution roles, or AI-responsibility wording.
"""
from __future__ import annotations

import json
import re
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "paper_b_main.tex"
REVIEWER_SECTIONS = ROOT / "manuscript" / "paper_b_reviewer_sections.tex"
RENDER = ROOT / "scripts" / "render_paper_b_figures.py"
PYPROJECT = ROOT / "pyproject.toml"
OUT_REPORT = ROOT / "artifacts" / "mee_submission_check.json"

IDENTITY_TOKENS = (
    "zuizui0223",
    "rachelzhang0223",
    "ZHANG RUIQI",
    "ZHANG Ruiqi",
    "張瑞琪",
)


def _strip_latex(text: str) -> str:
    text = re.sub(r"%.*", " ", text)
    text = re.sub(
        r"\\begin\{(?:equation|align\*?|lstlisting|tikzpicture)\}.*?"
        r"\\end\{(?:equation|align\*?|lstlisting|tikzpicture)\}",
        " ",
        text,
        flags=re.S,
    )
    text = re.sub(
        r"\\(?:cite|ref|label|url|href)\{[^{}]*\}(?:\{[^{}]*\})?", " ", text
    )
    text = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", " ", text)
    text = text.replace("{", " ").replace("}", " ").replace("$", " ")
    text = re.sub(r"[^A-Za-z0-9'\-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _word_count(text: str) -> int:
    stripped = _strip_latex(text)
    return 0 if not stripped else len(stripped.split())


def _abstract_block(text: str) -> str:
    start = text.find(r"\begin{abstract}")
    end = text.find(r"\end{abstract}", start + 1)
    return "" if start < 0 or end < 0 else text[start:end]


def _keyword_values(text: str) -> list[str]:
    marker = r"\section*{Keywords}"
    if marker not in text:
        return []
    tail = text.split(marker, 1)[1].lstrip()
    line = tail.splitlines()[0].strip() if tail else ""
    return [value.strip() for value in line.split(";") if value.strip()]


def _license_status() -> dict[str, object]:
    candidates = (
        "LICENSE",
        "LICENSE.txt",
        "LICENSE.md",
        "COPYING",
        "COPYING.txt",
    )
    files = [name for name in candidates if (ROOT / name).is_file()]
    project_text = PYPROJECT.read_text(encoding="utf-8") if PYPROJECT.exists() else ""
    metadata = bool(re.search(r"(?m)^license\s*=", project_text))
    return {
        "present": bool(files or metadata),
        "files": files,
        "pyproject_license_metadata": metadata,
    }


def build_report() -> dict[str, object]:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    reviewer = REVIEWER_SECTIONS.read_text(encoding="utf-8")
    module = runpy.run_path(str(RENDER))
    bibliography = module["bibliography_tex"]()

    abstract = _abstract_block(manuscript)
    keywords = _keyword_values(manuscript)
    top_sections = re.findall(r"\\section\{([^{}]+)\}", manuscript)
    identity_hits = sorted(
        token for token in IDENTITY_TOKENS if token.lower() in manuscript.lower()
    )
    data_code_present = r"\section*{Data and code for peer review}" in manuscript
    anonymous_author = r"\author{Anonymous for double-anonymous review}" in manuscript
    ai_disclosure = bool(
        re.search(r"ChatGPT|GPT-5\.6|large language model|LLM", manuscript, flags=re.I)
    )
    title_page_candidates = [
        str(path.relative_to(ROOT))
        for path in (ROOT / "manuscript").glob("*title*page*")
        if path.is_file()
    ]
    license_status = _license_status()

    combined_submission_text = manuscript + "\n" + reviewer + "\n" + bibliography
    rough_words = _word_count(combined_submission_text)
    abstract_words = _word_count(abstract)

    hard_checks = {
        "anonymous_main_manuscript": anonymous_author and not identity_hits,
        "abstract_has_four_numbered_items": abstract.count(r"\item") == 4,
        "abstract_at_most_350_rough_words": abstract_words <= 350,
        "data_code_statement_present": data_code_present,
        "keywords_between_5_and_8": 5 <= len(keywords) <= 8,
        "standard_top_level_structure": top_sections
        == ["Introduction", "Materials and Methods", "Results", "Discussion"],
        "four_headline_results_present": all(
            rf"\subsection{{Result {number}:" in manuscript for number in range(1, 5)
        ),
        "reviewer_material_has_no_top_level_section": r"\section{" not in reviewer,
        "rough_total_words_at_most_8000": rough_words <= 8000,
    }

    author_decisions = {
        "open_source_license_present": license_status["present"],
        "separate_title_page_present": bool(title_page_candidates),
        "ai_llm_disclosure_present_in_methods": ai_disclosure,
        "final_author_contributions_confirmed": False,
        "final_conflict_of_interest_statement_confirmed": False,
    }

    return {
        "schema_version": 1,
        "journal": "Methods in Ecology and Evolution",
        "article_type": "Standard Research Article",
        "hard_checks": hard_checks,
        "hard_checks_pass": all(hard_checks.values()),
        "author_decisions": author_decisions,
        "submission_blockers_requiring_human_decision": [
            key for key, value in author_decisions.items() if not value
        ],
        "metrics": {
            "abstract_rough_words": abstract_words,
            "rough_total_words_including_generated_bibliography_and_reviewer_sections": rough_words,
            "keyword_count": len(keywords),
            "keywords": keywords,
            "top_level_sections": top_sections,
            "identity_hits_in_main_manuscript": identity_hits,
            "title_page_candidates": title_page_candidates,
            "license": license_status,
        },
        "notes": [
            "Rough word counts strip LaTeX heuristically and are not the publisher submission-system count.",
            "Human-decision warnings do not make this checker exit non-zero.",
            "Do not add a software license, final authorship metadata, COI wording, contribution roles, or AI-responsibility wording without author confirmation.",
        ],
    }


def main() -> None:
    report = build_report()
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
