"""Write a deterministic replay for bounded false-positive threshold evidence."""

from __future__ import annotations

import json
from pathlib import Path

from ced.threshold_detection import ThresholdEvidenceDesign

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts" / "ced_threshold_detection_report.json"


def build_report() -> dict[str, object]:
    design = ThresholdEvidenceDesign(
        read_count=5,
        positive_threshold=3,
        sensitivity_lower_bound=0.7,
        false_positive_upper_bound=0.05,
    )
    threshold_for_100 = ThresholdEvidenceDesign.minimum_threshold_for_evidence_ratio(
        5, 0.7, 0.05, 100
    )
    if not design.verify() or threshold_for_100 != 3:
        raise AssertionError("false-positive threshold witness failed verification")
    return {
        "schema_version": 1,
        "scope": "declared conditionally independent binary reads with bounded sensitivity and bounded false positives",
        "non_claim": "threshold crossing is not a deductive presence certificate when false positives are allowed",
        "threshold_design": {
            "read_count": design.read_count,
            "positive_threshold": design.positive_threshold,
            "sensitivity_lower_bound": design.sensitivity_lower_bound,
            "false_positive_upper_bound": design.false_positive_upper_bound,
            "detection_probability_lower_bound": round(
                design.detection_probability_lower_bound, 12
            ),
            "false_alert_probability_upper_bound": round(
                design.false_alert_probability_upper_bound, 12
            ),
            "evidence_ratio_lower_bound": round(design.evidence_ratio_lower_bound, 12),
            "threshold_is_presence_certificate": design.threshold_is_presence_certificate,
        },
        "frontier": {
            "target_evidence_ratio": 100,
            "minimum_threshold": threshold_for_100,
        },
    }


def main() -> None:
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
