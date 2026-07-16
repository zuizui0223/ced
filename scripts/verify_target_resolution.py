"""Write the submission-facing target-resolution comparison."""

from __future__ import annotations

import json
from pathlib import Path

from ced.target_resolution import (
    CostedTargetResolutionDesign,
    RiskLimitedTargetResolution,
    TargetRecordOutcome,
    cheapest_feasible_target_resolution,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts" / "ced_target_resolution_report.json"


def _resolution(outcomes):
    return RiskLimitedTargetResolution("decrease", tuple(outcomes))


def build_report() -> dict[str, object]:
    designs = (
        CostedTargetResolutionDesign(
            "stop-set-valued",
            0.0,
            _resolution((TargetRecordOutcome("passive", 1.0, frozenset(("no interaction", "decrease", "increase"))),)),
        ),
        CostedTargetResolutionDesign(
            "additional-detection",
            1.0,
            _resolution(
                (
                    TargetRecordOutcome("absent", 0.10, frozenset(("no interaction",))),
                    TargetRecordOutcome("present", 0.90, frozenset(("decrease", "increase"))),
                )
            ),
        ),
        CostedTargetResolutionDesign(
            "response-intervention",
            2.5,
            _resolution(
                (
                    TargetRecordOutcome("absent", 0.03, frozenset(("no interaction",))),
                    TargetRecordOutcome("decrease", 0.88, frozenset(("decrease",))),
                    TargetRecordOutcome("shared-failure", 0.09, frozenset(("decrease", "increase"))),
                )
            ),
        ),
    )
    chosen = cheapest_feasible_target_resolution(designs, 0.80, 0.05)
    return {
        "schema_version": 1,
        "true_target": "decrease",
        "designs": [
            {
                "name": design.name,
                "cost": design.cost,
                "correct_resolution_probability": round(design.resolution.correct_resolution_probability, 12),
                "wrong_resolution_probability": round(design.resolution.wrong_resolution_probability, 12),
                "ambiguity_probability": round(design.resolution.ambiguity_probability, 12),
            }
            for design in designs
        ],
        "constraint": {"minimum_correct": 0.80, "maximum_wrong": 0.05},
        "cheapest_feasible_design": None if chosen is None else chosen.name,
        "interpretation": "presence detection alone does not resolve the management target; the response intervention is selected only after accounting for wrong-report and ambiguity risk",
    }


def main() -> None:
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
