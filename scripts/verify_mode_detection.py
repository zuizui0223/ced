"""Write a deterministic replay for CED's common-mode detection extension."""

from __future__ import annotations

import json
from pathlib import Path

from ced.detection import OneSidedDetector
from ced.mode_detection import ModeDiverseDetectionPanel

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts" / "ced_mode_detection_report.json"


def build_report() -> dict[str, object]:
    detector = OneSidedDetector(0.6)
    panel = ModeDiverseDetectionPanel(
        coordinate_count=3,
        mode_count=2,
        repetitions_per_mode=5,
        availability_lower_bound=0.8,
        detector=detector,
    )
    one_mode = ModeDiverseDetectionPanel(
        coordinate_count=3,
        mode_count=1,
        repetitions_per_mode=10,
        availability_lower_bound=0.8,
        detector=detector,
    )
    required_modes = ModeDiverseDetectionPanel.minimum_mode_count_for_availability_ceiling(
        0.8, 0.95
    )
    minimum_repeats = ModeDiverseDetectionPanel(
        3, required_modes, 1, 0.8, detector
    ).minimum_repetitions_for_joint_confidence(0.95)
    if not panel.verify() or required_modes != 2 or minimum_repeats != 5:
        raise AssertionError("common-mode detection witness failed verification")
    return {
        "schema_version": 1,
        "scope": "declared independent common-mode availability with zero false positives, bounded sensitivity, and resettable conditionally independent reads inside operating modes",
        "non_claim": "the replay does not infer independent modes, availability, sensitivity, or absence from a negative record",
        "one_mode_same_effort": {
            "mode_count": one_mode.mode_count,
            "repetitions_per_mode": one_mode.repetitions_per_mode,
            "total_reads": one_mode.total_reads,
            "availability_ceiling": one_mode.availability_ceiling,
            "joint_detection_lower_bound": round(one_mode.joint_detection_lower_bound, 12),
        },
        "mode_diverse_design": {
            "mode_count": panel.mode_count,
            "repetitions_per_mode": panel.repetitions_per_mode,
            "total_reads": panel.total_reads,
            "availability_ceiling": panel.availability_ceiling,
            "joint_detection_lower_bound": round(panel.joint_detection_lower_bound, 12),
            "all_negative_probability_upper_bound_if_all_present": round(
                panel.all_negative_probability_if_all_present_upper_bound, 12
            ),
        },
        "design_frontier": {
            "target_joint_confidence": 0.95,
            "necessary_mode_floor": required_modes,
            "minimum_repetitions_per_mode_at_floor": minimum_repeats,
        },
    }


def main() -> None:
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
