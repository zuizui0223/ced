"""Build a curated anonymous code archive for MEE peer review.

The builder is intentionally strict about software licensing. It will not create the
final review ZIP until an open-source license file exists. Author metadata is never
inferred. The archive is built from a curated allow-list rather than from ``git
archive`` so Git metadata and unrelated submission notes are excluded.
"""
from __future__ import annotations

import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "artifacts"
OUT_ZIP = OUT_DIR / "paper_b_mee_review_archive.zip"
OUT_REPORT = OUT_DIR / "paper_b_mee_review_archive_check.json"

IDENTITY_TOKENS = (
    "zuizui0223",
    "rachelzhang0223",
    "ZHANG RUIQI",
    "ZHANG Ruiqi",
    "張瑞琪",
)

LICENSE_NAMES = ("LICENSE", "LICENSE.txt", "LICENSE.md", "COPYING", "COPYING.txt")
TEXT_SUFFIXES = {".py", ".toml", ".md", ".txt", ".tex", ".yml", ".yaml", ".json", ".csv"}

ANONYMOUS_README = """# Paper B — anonymous code archive for peer review

This archive accompanies the manuscript "From ecological states to distinguishable
futures: Target-safe prediction from finite evidence" for double-anonymous review.

## Install and test

```bash
python -m pip install -e '.[dev]'
pytest
```

## Reproduce submission-facing outputs

```bash
python scripts/simulate_paper_b_benchmark.py
python scripts/analyze_paper_b_reviewer_robustness.py
python scripts/analyze_paper_b_posterior_bridge.py
python scripts/render_paper_b_figures.py
python scripts/check_mee_submission.py
```

The repository is theorem-first: tests and deterministic replays are part of the
scientific record. The posterior-sample bridge is a methodological demonstration,
not an empirical dataset.
"""


def _license_files() -> list[Path]:
    return [ROOT / name for name in LICENSE_NAMES if (ROOT / name).is_file()]


def _allowed_files() -> list[Path]:
    files: list[Path] = []
    for directory in (ROOT / "ced", ROOT / "scripts", ROOT / "tests"):
        files.extend(path for path in directory.rglob("*") if path.is_file())
    files.append(ROOT / "pyproject.toml")
    files.extend(_license_files())
    return sorted(set(files))


def _identity_hits(path: Path) -> list[str]:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []
    lower = text.lower()
    return [token for token in IDENTITY_TOKENS if token.lower() in lower]


def preflight() -> dict[str, object]:
    files = _allowed_files()
    hits: list[dict[str, object]] = []
    for path in files:
        found = _identity_hits(path)
        if found:
            hits.append(
                {
                    "path": str(path.relative_to(ROOT)),
                    "tokens": found,
                }
            )
    licenses = [str(path.relative_to(ROOT)) for path in _license_files()]
    return {
        "schema_version": 1,
        "license_present": bool(licenses),
        "license_files": licenses,
        "identity_hits": hits,
        "identity_scan_pass": not hits,
        "curated_file_count": len(files),
        "archive_ready": bool(licenses) and not hits,
        "archive_path": str(OUT_ZIP.relative_to(ROOT)),
    }


def build_archive() -> dict[str, object]:
    report = preflight()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if not report["license_present"]:
        raise RuntimeError(
            "MEE review archive is blocked: add an author-approved open-source LICENSE first"
        )
    if not report["identity_scan_pass"]:
        raise RuntimeError(
            "MEE review archive is blocked: identifying tokens remain in curated source files"
        )

    with zipfile.ZipFile(OUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("README.md", ANONYMOUS_README)
        for path in _allowed_files():
            archive.write(path, path.relative_to(ROOT).as_posix())

    final = dict(report)
    final["archive_size_bytes"] = OUT_ZIP.stat().st_size
    OUT_REPORT.write_text(json.dumps(final, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return final


def main() -> None:
    report = preflight()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    if not report["archive_ready"]:
        print(
            "Archive not built. Resolve the reported license/identity blockers, then run "
            "build_archive() or this script after the blockers are cleared."
        )
        return
    print(json.dumps(build_archive(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
