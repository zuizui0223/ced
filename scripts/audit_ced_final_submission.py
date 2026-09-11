#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = ROOT / "manuscript" / "paper_b_main.tex"
COMPILED = ROOT / "manuscript" / "paper_b_compiled.tex"
HISTORICAL = [
    ROOT / "manuscript" / "EVIDENCE_DRAFT_V1.md",
    ROOT / "manuscript" / "evidence_main.tex",
]
OUT_JSON = ROOT / "artifacts" / "ced_final_submission_audit.json"
OUT_MD = ROOT / "artifacts" / "ced_final_submission_audit.md"
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?")
CITE_RE = re.compile(r"\\cite\w*\{([^}]+)\}")
BIB_RE = re.compile(r"\\bibitem\{([^}]+)\}")
COMMENT_RE = re.compile(r"(?m)%.*$")
CODE_RE = re.compile(r"\\begin\{lstlisting\}.*?\\end\{lstlisting\}", re.S)
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


def clean(text: str) -> str:
    text = COMMENT_RE.sub(" ", text)
    text = CODE_RE.sub(" ", text)
    text = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", " ", text)
    text = re.sub(r"[{}$&_^~\\]", " ", text)
    return text


def words(text: str) -> list[str]:
    return [m.group(0).casefold() for m in WORD_RE.finditer(clean(text))]


def ngrams(tokens: list[str], n: int = 12) -> set[tuple[str, ...]]:
    return {tuple(tokens[i:i+n]) for i in range(max(0, len(tokens)-n+1))}


def long_sentences(text: str) -> list[tuple[str, ...]]:
    out = []
    for sent in SENT_SPLIT.split(clean(text)):
        row = tuple(m.group(0).casefold() for m in WORD_RE.finditer(sent))
        if len(row) >= 12:
            out.append(row)
    return out


def overlap(active_text: str, source_text: str, label: str) -> dict:
    a = words(active_text)
    b = words(source_text)
    a12 = ngrams(a)
    b12 = ngrams(b)
    common = a12 & b12
    blocks = sorted((x for x in SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks() if x.size), key=lambda x: x.size, reverse=True)
    longest = blocks[0] if blocks else None
    b_sents = set(long_sentences(source_text))
    exact = []
    seen = set()
    for sent in long_sentences(active_text):
        if sent in b_sents and sent not in seen:
            seen.add(sent)
            exact.append({"word_count": len(sent), "text": " ".join(sent)})
    exact.sort(key=lambda x: x["word_count"], reverse=True)
    return {
        "source": label,
        "active_word_count": len(a),
        "source_word_count": len(b),
        "overlapping_unique_12gram_count": len(common),
        "active_unique_12gram_overlap_fraction": len(common) / len(a12) if a12 else 0.0,
        "longest_exact_contiguous_word_match": longest.size if longest else 0,
        "longest_match_text": " ".join(a[longest.a:longest.a + min(longest.size, 120)]) if longest else "",
        "exact_sentence_matches_12plus": exact,
    }


def main() -> None:
    if not COMPILED.exists():
        raise SystemExit("paper_b_compiled.tex missing; run scripts/render_paper_b_figures.py first")
    compiled = COMPILED.read_text(encoding="utf-8")
    active_text = ACTIVE.read_text(encoding="utf-8")

    citation_keys: set[str] = set()
    for group in CITE_RE.findall(compiled):
        citation_keys.update(k.strip() for k in group.split(",") if k.strip())
    bib_keys = set(BIB_RE.findall(compiled))
    missing = sorted(citation_keys - bib_keys)
    unused = sorted(bib_keys - citation_keys)

    comparisons = []
    for path in HISTORICAL:
        if path.exists():
            comparisons.append(overlap(active_text, path.read_text(encoding="utf-8"), f"ced/{path.relative_to(ROOT).as_posix()}"))

    payload = {
        "schema": "ced-final-submission-audit-v1",
        "active": "ced/manuscript/paper_b_main.tex",
        "compiled": "ced/manuscript/paper_b_compiled.tex",
        "reference_integrity": {
            "citation_key_count": len(citation_keys),
            "bibitem_key_count": len(bib_keys),
            "missing_citation_keys": missing,
            "unused_bibitem_keys": unused,
            "all_citations_resolved": not missing,
        },
        "self_overlap": {
            "method": "case-folded word overlap after stripping LaTeX commands/comments/code; 12-word ngrams; descriptive only",
            "comparisons": comparisons,
        },
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# CED final submission audit",
        "",
        f"Citation keys: **{len(citation_keys)}**; bibitems: **{len(bib_keys)}**; missing: **{len(missing)}**; unused: **{len(unused)}**.",
        "",
        "| Historical source | 12-gram overlap | Longest exact run | Exact sentences >=12 words |",
        "|---|---:|---:|---:|",
    ]
    for row in comparisons:
        lines.append(f"| `{row['source']}` | {row['active_unique_12gram_overlap_fraction']:.4%} ({row['overlapping_unique_12gram_count']}) | {row['longest_exact_contiguous_word_match']} | {len(row['exact_sentence_matches_12plus'])} |")
    if missing:
        lines += ["", "## Missing citation keys", "", *[f"- `{x}`" for x in missing]]
    lines += ["", "## Longest overlap excerpts", ""]
    for row in comparisons:
        lines += [f"### {row['source']}", "", row["longest_match_text"] or "(none)", ""]
    OUT_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    if missing:
        raise SystemExit(f"unresolved citation keys: {missing}")
    print("CED_FINAL_SUBMISSION_AUDIT PASS")
    for row in comparisons:
        print(row["source"], row["active_unique_12gram_overlap_fraction"], row["longest_exact_contiguous_word_match"], len(row["exact_sentence_matches_12plus"]))


if __name__ == "__main__":
    main()
