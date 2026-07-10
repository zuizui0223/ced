"""Write a deterministic replay for calibration-derived detection bounds."""

from __future__ import annotations

import json
from pathlib import Path

from ced.calibration import CalibrationBounds

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts" / "ced_calibration_bounds_report.json"


def build_report() -> dict[str, object]:
    calibration = CalibrationBounds(
        blank_read_count=60,
        blank_positive_count=0,
        present_read_count=60,
        present_positive_count=55,
        delta=0.05,
    )
    threshold = calibration.as_threshold_design(read_count=5, positive_threshold=3)
    multiple = calibration.as_multiple_threshold_design(
        coordinate_count=20, read_count=5, positive_threshold=3
    )
    if not calibration.verify() or not threshold.verify() or not multiple.verify():
        raise AssertionError("calibration-bound witness failed verification")
    return {
        "schema_version": 1,
        "scope": "finite blank-control and present-control calibration converted into conservative one-sided binomial bounds",
        "non_claim": "the replay does not infer representativeness, independence, stationarity, or ecological presence from calibration records",
        "calibration": {
            "blank_read_count": calibration.blank_read_count,
            "blank_positive_count": calibration.blank_positive_count,
            "present_read_count": calibration.present_read_count,
            "present_positive_count": calibration.present_positive_count,
            "delta": calibration.delta,
            "false_positive_upper_bound": round(
                calibration.false_positive_upper_bound, 12
            ),
            "sensitivity_lower_bound": round(calibration.sensitivity_lower_bound, 12),
            "confidence_level_per_bound": round(
                calibration.confidence_level_per_bound, 12
            ),
            "joint_confidence_lower_bound": round(
                calibration.joint_confidence_lower_bound, 12
            ),
        },
        "threshold_design": {
            "read_count": threshold.read_count,
            "positive_threshold": threshold.positive_threshold,
            "false_alert_probability_upper_bound": round(
                threshold.false_alert_probability_upper_bound, 12
            ),
            "detection_probability_lower_bound": round(
                threshold.detection_probability_lower_bound, 12
            ),
            "evidence_ratio_lower_bound": round(threshold.evidence_ratio_lower_bound, 12),
        },
        "multiple_testing": {
            "coordinate_count": multiple.coordinate_count,
            "familywise_false_alert_upper_bound": round(
                multiple.familywise_false_alert_upper_bound, 12
            ),
            "exact_independent_all_absent_familywise_false_alert": round(
                multiple.exact_independent_all_absent_familywise_false_alert, 12
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
