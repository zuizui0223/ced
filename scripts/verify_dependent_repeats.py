"""Write a deterministic replay for dependent-repeat threshold evidence."""

from __future__ import annotations

import json
from pathlib import Path

from ced.dependent_repeats import DependentThresholdEvidenceDesign

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts" / "ced_dependent_repeats_report.json"


def build_report() -> dict[str, object]:
    dependent = DependentThresholdEvidenceDesign(
        read_count=5,
        positive_threshold=3,
        sensitivity_lower_bound=0.7,
        false_positive_upper_bound=0.05,
    )
    any_positive = DependentThresholdEvidenceDesign(
        read_count=10,
        positive_threshold=1,
        sensitivity_lower_bound=0.6,
        false_positive_upper_bound=0.05,
    )
    zero_false_positive = DependentThresholdEvidenceDesign(
        read_count=5,
        positive_threshold=3,
        sensitivity_lower_bound=0.7,
        false_positive_upper_bound=0.0,
    )
    if not dependent.verify() or not any_positive.verify() or not zero_false_positive.verify():
        raise AssertionError("dependent-repeat witness failed verification")
    return {
        "schema_version": 1,
        "scope": "threshold evidence under marginal read contracts without resettable independence",
        "non_claim": "the replay does not infer dependence, resetability, error rates, or posterior probabilities",
        "threshold_design": {
            "read_count": dependent.read_count,
            "positive_threshold": dependent.positive_threshold,
            "sensitivity_lower_bound": dependent.sensitivity_lower_bound,
            "false_positive_upper_bound": dependent.false_positive_upper_bound,
            "false_alert_probability_upper_bound": round(
                dependent.false_alert_probability_upper_bound, 12
            ),
            "detection_probability_lower_bound": round(
                dependent.detection_probability_lower_bound, 12
            ),
            "evidence_ratio_lower_bound": round(
                dependent.evidence_ratio_lower_bound, 12
            ),
            "threshold_crossing_certifies_presence": dependent.threshold_crossing_certifies_presence,
        },
        "any_positive_nonreset": {
            "read_count": any_positive.read_count,
            "positive_threshold": any_positive.positive_threshold,
            "sensitivity_lower_bound": any_positive.sensitivity_lower_bound,
            "detection_probability_lower_bound": round(
                any_positive.detection_probability_lower_bound, 12
            ),
            "interpretation": "without independence, repeated reads do not improve the any-positive guarantee beyond the marginal sensitivity bound",
        },
        "zero_false_positive_boundary": {
            "false_alert_probability_upper_bound": round(
                zero_false_positive.false_alert_probability_upper_bound, 12
            ),
            "detection_probability_lower_bound": round(
                zero_false_positive.detection_probability_lower_bound, 12
            ),
            "threshold_crossing_certifies_presence": zero_false_positive.threshold_crossing_certifies_presence,
        },
    }


def main() -> None:
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
