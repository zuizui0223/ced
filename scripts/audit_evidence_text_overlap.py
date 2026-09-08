#!/usr/bin/env python3
"""Audit Evidence abstract overlap against archived source-paper abstracts.

This is a duplicate-text/salami-risk guard, not a plagiarism detector. It checks
only exact normalized sentences and exact fixed-length word shingles against
pinned source abstracts.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DRAFT = ROOT / "manuscript" / "EVIDENCE_DRAFT_V1.md"
DEFAULT_SOURCES = ROOT / "manuscript" / "EVIDENCE_SOURCE_ABSTRACT_SNAPSHOTS.json"
DEFAULT_OUTPUT = ROOT / "manuscript" / "evidence_overlap_audit.json"
SHINGLE_WORDS = 12
MAX_SHARED_SHINGLES = 2


def normalize_words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower().replace("–", "-").replace("—", "-"))


def normalized_sentences(text: str) -> set[str]:
    output: set[str] = set()
    for raw in re.split(r"(?<=[.!?])\s+", text.strip()):
        words = normalize_words(raw)
        if len(words) >= 12:
            output.add(" ".join(words))
    return output


def shingles(text: str, width: int = SHINGLE_WORDS) -> set[tuple[str, ...]]:
    words = normalize_words(text)
    if len(words) < width:
        return set()
    return {tuple(words[index:index + width]) for index in range(len(words) - width + 1)}


def extract_markdown_abstract(text: str) -> str:
    marker = "## Abstract"
    if marker not in text:
        raise ValueError("Evidence draft lacks ## Abstract")
    after = text.split(marker, 1)[1].lstrip()
    match = re.search(r"\n##\s+", after)
    abstract = after[:match.start()] if match else after
    if not abstract.strip():
        raise ValueError("Evidence abstract is empty")
    return abstract.strip()


def compare(current: str, source: str) -> dict[str, object]:
    current_sentences = normalized_sentences(current)
    source_sentences = normalized_sentences(source)
    exact_sentences = sorted(current_sentences & source_sentences)

    current_shingles = shingles(current)
    source_shingles = shingles(source)
    shared = current_shingles & source_shingles
    union = current_shingles | source_shingles
    jaccard = len(shared) / len(union) if union else 0.0
    return {
        "exact_normalized_sentence_matches": exact_sentences,
        "shared_12_word_shingle_count": len(shared),
        "shingle_jaccard": jaccard,
    }


def audit(draft_path: Path = DEFAULT_DRAFT, source_path: Path = DEFAULT_SOURCES) -> dict[str, object]:
    current = extract_markdown_abstract(draft_path.read_text(encoding="utf-8"))
    source_payload = json.loads(source_path.read_text(encoding="utf-8"))
    comparisons: dict[str, dict[str, object]] = {}
    violations: list[str] = []

    for name, row in source_payload["sources"].items():
        result = compare(current, str(row["abstract"]))
        comparisons[name] = result
        if result["exact_normalized_sentence_matches"]:
            violations.append(f"{name}: exact normalized sentence reuse")
        if int(result["shared_12_word_shingle_count"]) > MAX_SHARED_SHINGLES:
            violations.append(
                f"{name}: shared 12-word shingles {result['shared_12_word_shingle_count']} > {MAX_SHARED_SHINGLES}"
            )

    return {
        "schema": "evidence-source-text-overlap-audit-v1",
        "shingle_words": SHINGLE_WORDS,
        "max_shared_shingles_per_source": MAX_SHARED_SHINGLES,
        "comparisons": comparisons,
        "violations": violations,
        "status": "PASS" if not violations else "FAIL",
        "interpretation": (
            "This guard detects exact long-text reuse against pinned source abstracts. "
            "It does not establish conceptual non-overlap; claim ownership remains governed "
            "by EVIDENCE_CLAIM_MANIFEST.json and EVIDENCE_OVERLAP_FIREWALL.md."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", type=Path, default=DEFAULT_DRAFT)
    parser.add_argument("--sources", type=Path, default=DEFAULT_SOURCES)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = audit(args.draft, args.sources)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("EVIDENCE_OVERLAP_AUDIT", result["status"])
    for name, row in result["comparisons"].items():
        print(name, "shared12", row["shared_12_word_shingle_count"], "jaccard", f"{row['shingle_jaccard']:.6f}")
    if result["violations"]:
        raise SystemExit("; ".join(result["violations"]))


if __name__ == "__main__":
    main()
