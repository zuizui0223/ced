"""Write a deterministic replay for overlapping latent failure factors."""

from __future__ import annotations

import json
from pathlib import Path

from ced.overlapping_modes import OverlappingFailureModePanel

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts" / "ced_overlapping_modes_report.json"


def build_report() -> dict[str, object]:
    partial = OverlappingFailureModePanel(
        coordinate_count=3,
        repetitions_per_coordinate_per_mode=2,
        sensitivity_lower_bound=0.6,
        factor_failure_probabilities=(0.1, 0.2, 0.3),
        mode_factor_sets=(frozenset({0, 1}), frozenset({1, 2})),
    )
    independent = OverlappingFailureModePanel(
        2,
        3,
        0.7,
        (0.2, 0.2),
        (frozenset({0}), frozenset({1})),
    )
    common = OverlappingFailureModePanel(
        2,
        3,
        0.7,
        (0.2,),
        (frozenset({0}), frozenset({0})),
    )
    if not partial.verify() or not independent.verify() or not common.verify():
        raise AssertionError("overlapping-mode witness failed verification")
    return {
        "schema_version": 1,
        "scope": "detection with independent latent failure factors shared across modes",
        "non_claim": "the replay does not infer factor graphs, factor probabilities, sensitivity, or ecological causes",
        "partial_overlap": {
            "coordinate_count": partial.coordinate_count,
            "mode_count": partial.mode_count,
            "factor_count": partial.factor_count,
            "shared_factor_count": partial.shared_factor_count,
            "pairwise_mode_overlap_counts": partial.pairwise_mode_overlap_counts,
            "within_mode_coordinate_miss_probability_upper_bound": round(
                partial.within_mode_coordinate_miss_probability_upper_bound, 12
            ),
            "all_modes_failed_probability": round(
                partial.all_modes_failed_probability, 12
            ),
            "availability_ceiling": round(partial.availability_ceiling, 12),
            "joint_detection_probability_lower_bound": round(
                partial.joint_detection_probability_lower_bound, 12
            ),
            "total_read_count": partial.total_read_count,
        },
        "endpoint_comparison": {
            "independent_mode_availability_ceiling": round(
                independent.availability_ceiling, 12
            ),
            "independent_mode_joint_detection_lower_bound": round(
                independent.joint_detection_probability_lower_bound, 12
            ),
            "common_mode_availability_ceiling": round(
                common.availability_ceiling, 12
            ),
            "common_mode_joint_detection_lower_bound": round(
                common.joint_detection_probability_lower_bound, 12
            ),
        },
    }


def main() -> None:
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
