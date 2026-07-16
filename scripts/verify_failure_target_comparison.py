"""Replay equal-cost target resolution under shared and diverse failures."""

from __future__ import annotations

import json
from pathlib import Path

from ced.failure_target_comparison import EqualCostFailureComparison
from ced.target_resolution import (
    CostedTargetResolutionDesign,
    RiskLimitedTargetResolution,
    TargetRecordOutcome,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts" / "ced_failure_target_comparison_report.json"


def _resolution(correct: float, wrong: float, ambiguity: float):
    return RiskLimitedTargetResolution(
        "decrease",
        (
            TargetRecordOutcome("correct", correct, frozenset(("decrease",))),
            TargetRecordOutcome("wrong", wrong, frozenset(("increase",))),
            TargetRecordOutcome(
                "ambiguous", ambiguity, frozenset(("decrease", "increase"))
            ),
        ),
    )


def build_report() -> dict[str, object]:
    comparison = EqualCostFailureComparison(
        (
            CostedTargetResolutionDesign("shared_mode", 12, _resolution(0.72, 0.03, 0.25)),
            CostedTargetResolutionDesign("overlapping_modes", 12, _resolution(0.84, 0.025, 0.135)),
            CostedTargetResolutionDesign("independent_modes", 12, _resolution(0.91, 0.02, 0.07)),
        )
    )
    return {
        "schema_version": 1,
        "scope": "equal-cost target resolution under declared failure architectures",
        "shared_cost": comparison.shared_cost,
        "designs": [
            {
                "name": design.name,
                "correct": design.resolution.correct_resolution_probability,
                "wrong": design.resolution.wrong_resolution_probability,
                "ambiguity": design.resolution.ambiguity_probability,
            }
            for design in comparison.designs
        ],
        "ranked_by_correct_resolution": comparison.ranked_by_correct_resolution,
        "dominant_designs": comparison.dominant_designs(),
        "feasible_at_correct_0_80_wrong_0_03": comparison.feasible_designs(0.80, 0.03),
        "feasible_at_correct_0_90_wrong_0_02": comparison.feasible_designs(0.90, 0.02),
        "interpretation": "equal read cost does not imply equal target-resolution reliability; independent failure diversity dominates shared replication in this declared witness",
    }


def main() -> None:
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
