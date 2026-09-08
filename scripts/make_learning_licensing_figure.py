#!/usr/bin/env python3
"""Build a monochrome SVG/CSV for Evidence Figure 2.

No plotting dependency is required. Scientific values are read from the frozen
``evidence_learning_licensing_result.json`` artifact.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
from pathlib import Path
from typing import Mapping


DEFAULT_INPUT = Path("manuscript/evidence_learning_licensing_result.json")
DEFAULT_SVG = Path("manuscript/generated/evidence_learning_vs_licensing.svg")
DEFAULT_CSV = Path("manuscript/generated/evidence_learning_vs_licensing.csv")
ORDER = ("nuisance_detail", "target_split", "constant_probe")
LABELS = {
    "nuisance_detail": "Nuisance detail",
    "target_split": "Target split",
    "constant_probe": "Constant probe",
}


def load_result(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema") != "ced-learning-licensing-divergence-v1":
        raise ValueError("wrong learning/licensing result schema")
    if payload.get("divergence") is not True:
        raise ValueError("frozen result does not contain ranking divergence")
    return payload


def _bar_panel(
    *,
    x0: int,
    y0: int,
    width: int,
    height: int,
    title: str,
    values: Mapping[str, float],
    maximum: float,
    unit: str,
) -> list[str]:
    lines = [
        f'<text x="{x0}" y="{y0 - 20}" font-size="18" font-weight="bold">{html.escape(title)}</text>',
        f'<line x1="{x0}" y1="{y0 + height}" x2="{x0 + width}" y2="{y0 + height}" stroke="black"/>',
        f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0 + height}" stroke="black"/>',
    ]
    bar_width = 70
    gap = (width - bar_width * len(ORDER)) / (len(ORDER) + 1)
    for index, name in enumerate(ORDER):
        value = float(values[name])
        bar_height = 0 if maximum == 0 else height * value / maximum
        x = x0 + gap * (index + 1) + bar_width * index
        y = y0 + height - bar_height
        lines.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width}" height="{bar_height:.1f}" fill="black" fill-opacity="0.70"/>'
        )
        lines.append(
            f'<text x="{x + bar_width / 2:.1f}" y="{y - 8:.1f}" text-anchor="middle" font-size="14">{value:g}{html.escape(unit)}</text>'
        )
        lines.append(
            f'<text x="{x + bar_width / 2:.1f}" y="{y0 + height + 24}" text-anchor="middle" font-size="12">{html.escape(LABELS[name])}</text>'
        )
    return lines


def build_svg(payload: Mapping[str, object]) -> str:
    candidates = payload["candidates"]
    if not isinstance(candidates, dict):
        raise TypeError("candidates must be a mapping")
    mechanism = {
        name: float(candidates[name]["mechanism_information_bits"])
        for name in ORDER
    }
    licensing = {
        name: float(candidates[name]["exact_target_resolution_probability"])
        for name in ORDER
    }

    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="480" viewBox="0 0 1000 480">',
        '<rect x="0" y="0" width="1000" height="480" fill="white"/>',
        '<text x="500" y="32" text-anchor="middle" font-size="22" font-weight="bold">Learning and licensing rank the same candidates differently</text>',
    ]
    lines.extend(
        _bar_panel(
            x0=70,
            y0=90,
            width=380,
            height=280,
            title="A. Mechanism-learning information",
            values=mechanism,
            maximum=2.0,
            unit=" bits",
        )
    )
    lines.extend(
        _bar_panel(
            x0=560,
            y0=90,
            width=380,
            height=280,
            title="B. Exact target-resolution probability",
            values=licensing,
            maximum=1.0,
            unit="",
        )
    )
    lines.append(
        '<text x="500" y="450" text-anchor="middle" font-size="15">Mechanism-learning top: nuisance detail; target-licensing top: target split</text>'
    )
    lines.append('</svg>')
    return "\n".join(lines) + "\n"


def write_csv(payload: Mapping[str, object], path: Path) -> None:
    candidates = payload["candidates"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["candidate", "mechanism_information_bits", "exact_target_resolution_probability", "equal_cost"])
        for name in ORDER:
            row = candidates[name]
            writer.writerow([
                name,
                row["mechanism_information_bits"],
                row["exact_target_resolution_probability"],
                row["equal_cost"],
            ])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--svg", type=Path, default=DEFAULT_SVG)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    args = parser.parse_args()

    payload = load_result(args.input)
    args.svg.parent.mkdir(parents=True, exist_ok=True)
    args.svg.write_text(build_svg(payload), encoding="utf-8")
    write_csv(payload, args.csv)
    print("EVIDENCE_FIGURE2 PASS", args.svg, args.csv)


if __name__ == "__main__":
    main()
