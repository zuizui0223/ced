from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_evidence_text_overlap.py"

spec = importlib.util.spec_from_file_location("audit_evidence_text_overlap", SCRIPT)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_integrated_evidence_abstract_passes_source_text_firewall() -> None:
    result = module.audit()
    assert result["status"] == "PASS", result["violations"]
    assert result["violations"] == []
    assert set(result["comparisons"]) == {"boundary", "mrod", "ced_paper_b"}


def test_no_exact_long_sentence_is_reused() -> None:
    result = module.audit()
    for row in result["comparisons"].values():
        assert row["exact_normalized_sentence_matches"] == []
        assert row["shared_12_word_shingle_count"] <= module.MAX_SHARED_SHINGLES
