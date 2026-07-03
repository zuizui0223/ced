"""Write a deterministic replay report for CED's imperfect-detection extension."""

from __future__ import annotations

import json
from pathlib import Path

from ced.detection import OneSidedDetectionPanel, OneSidedDetector

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts" / "ced_imperfect_detection_report.json"


def build_report() -> dict[str, object]:
    detector = OneSidedDetector(0.6)
    repetitions = detector.repetitions_for_joint_detection_confidence(3, 0.95)
    panel = OneSidedDetectionPanel(3, repetitions, detector)
    if not panel.verify() or repetitions != 5:
        raise AssertionError("imperfect-detection witness failed verification")
    return {
        "schema_version": 1,
        "scope": "declared zero-false-positive detectors with bounded sensitivity and conditionally independent resettable reads",
        "non_claim": "finite non-detection does not certify absence, closure, a complete coordinate set, or an inferred ecological boundary",
        "finite_negative_limit": {
            "sensitivity_lower_bound": detector.sensitivity_lower_bound,
            "repetitions": repetitions,
            "all_negative_probability_upper_bound_if_present": round(
                detector.all_negative_probability_if_present(repetitions), 12
            ),
            "absence_certified_by_all_negatives": False,
        },
        "risk_limited_design": {
            "coordinate_count": panel.coordinate_count,
            "target_joint_confidence": 0.95,
            "minimum_repetitions_per_coordinate": repetitions,
            "total_reads": panel.total_reads,
            "joint_detection_lower_bound": round(panel.joint_detection_lower_bound, 12),
        },
        "positive_signature_example": list(
            sorted(panel.positive_signature(((False,) * repetitions, (False, True, False, False, False), (True,) * repetitions)))
        ),
    }


def main() -> None:
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
