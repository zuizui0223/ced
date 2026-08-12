from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "paper_b_main.tex"
REVIEWER_SECTIONS = ROOT / "manuscript" / "paper_b_reviewer_sections.tex"


def _abstract(text: str) -> str:
    start = text.index(r"\begin{abstract}")
    end = text.index(r"\end{abstract}", start)
    return text[start:end]


def test_mee_abstract_has_four_numbered_items_and_anonymous_review_metadata():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    abstract = _abstract(text)

    assert r"\begin{enumerate}" in abstract
    assert abstract.count(r"\item") == 4
    assert "finite reportability" in abstract
    assert "honest ecological prediction remains a set" in abstract
    assert r"\author{Anonymous for double-anonymous review}" in text
    assert "zuizui0223" not in text


def test_mee_front_matter_contains_review_archive_and_keywords():
    text = MANUSCRIPT.read_text(encoding="utf-8")

    data_code = r"\section*{Data and code for peer review}"
    keywords = r"\section*{Keywords}"
    introduction = r"\section{Introduction}"

    assert data_code in text
    assert keywords in text
    assert "anonymized review archive accompanying the submission" in text
    assert "public version-of-record repository will be archived upon acceptance" in text
    assert text.index(data_code) < text.index(keywords) < text.index(introduction)

    keyword_line = text.split(keywords, 1)[1].split("\n", 2)[1].strip()
    keyword_values = [value.strip() for value in keyword_line.split(";")]
    assert 5 <= len(keyword_values) <= 10
    assert "ecological prediction" in keyword_values
    assert "finite evidence" in keyword_values


def test_mee_top_level_structure_is_standard_and_results_hold_all_four_claims():
    text = MANUSCRIPT.read_text(encoding="utf-8")

    top_level = (
        r"\section{Introduction}",
        r"\section{Materials and Methods}",
        r"\section{Results}",
        r"\section{Discussion}",
    )
    for section in top_level:
        assert section in text
    assert text.index(top_level[0]) < text.index(top_level[1]) < text.index(top_level[2]) < text.index(top_level[3])

    assert r"\section{Conclusion}" not in text
    assert r"\section{Comparative benchmark}" not in text
    assert r"\section{Four linked results}" not in text

    for result in range(1, 5):
        assert rf"\subsection{{Result {result}:" in text


def test_injected_sensitivity_material_remains_inside_results():
    reviewer = REVIEWER_SECTIONS.read_text(encoding="utf-8")
    assert r"\section{" not in reviewer
    assert r"\subsection{Sensitivity analyses and practical scope}" in reviewer
    assert r"\subsubsection{Boundary with goal-oriented design and value of information}" in reviewer
