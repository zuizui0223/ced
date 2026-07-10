"""Write a deterministic replay for multiple-coordinate threshold evidence."""

from __future__ import annotations

import json
from pathlib import Path

from ced.multiple_testing import MultipleThresholdEvidenceDesign
from ced.threshold_detection import ThresholdEvidenceDesign

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts" / "ced_multiple_testing_report.json"


def build_report() -> dict[str, object]:
    per = ThresholdEvidenceDesign(
        read_count=5,
        positive_threshold=3,
        sensitivity_lower_bound=0.7,
        false_positive_upper_bound=0.05,
    )
    design = MultipleThresholdEvidenceDesign(coordinate_count=20, per_coordinate=per)
    threshold = MultipleThresholdEvidenceDesign.minimum_threshold_for_familywise_and_evidence_ratio(
        coordinate_count=20,
        read_count=5,
        sensitivity_lower_bound=0.7,
        false_positive_upper_bound=0.05,
        familywise_alpha=0.05,
        target_evidence_ratio=100,
    )
    if not design.verify() or threshold != 3:
        raise AssertionError("multiple-testing witness failed verification")
    return {
        "schema_version": 1,
        "scope": "declared finite coordinate set with shared threshold design and bounded false-positive rates",
        "non_claim": "the replay does not infer the coordinate set, false-positive bounds, cross-coordinate independence, or posterior presence probabilities",
        "per_coordinate": {
            "read_count": per.read_count,
            "positive_threshold": per.positive_threshold,
            "false_alert_probability_upper_bound": round(
                per.false_alert_probability_upper_bound, 12
            ),
            "detection_probability_lower_bound": round(
                per.detection_probability_lower_bound, 12
            ),
            "evidence_ratio_lower_bound": round(per.evidence_ratio_lower_bound, 12),
        },
        "familywise": {
            "coordinate_count": design.coordinate_count,
            "expected_false_alerts_upper_bound": round(
                design.expected_false_alerts_upper_bound, 12
            ),
            "bonferroni_familywise_false_alert_upper_bound": round(
                design.familywise_false_alert_upper_bound, 12
            ),
            "exact_independent_all_absent_familywise_false_alert": round(
                design.exact_independent_all_absent_familywise_false_alert, 12
            ),
        },
        "frontier": {
            "target_familywise_alpha": 0.05,
            "target_evidence_ratio": 100,
            "minimum_threshold": threshold,
        },
    }


def main() -> None:
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
