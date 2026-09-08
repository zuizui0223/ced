#!/usr/bin/env python3
"""Emit the exact Evidence integration benchmark."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from ced.learning_licensing import benchmark


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("manuscript/evidence_learning_licensing_result.json"),
    )
    args = parser.parse_args()
    payload = benchmark()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("EVIDENCE_LEARNING_LICENSING", "DIVERGES" if payload["divergence"] else "NO_DIVERGENCE")
    print("LEARNING_TOP", payload["learning_rank"][0])
    print("LICENSING_TOP", payload["licensing_rank"][0])


if __name__ == "__main__":
    main()
