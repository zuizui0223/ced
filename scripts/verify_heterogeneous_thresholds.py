"""Write a deterministic replay for heterogeneous threshold panels."""

from __future__ import annotations

import json
from pathlib import Path

from ced.heterogeneous_thresholds import HeterogeneousThresholdEvidencePanel
from ced.threshold_detection import ThresholdEvidenceDesign

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts" / "ced_heterogeneous_thresholds_report.json"


def build_panel() -> HeterogeneousThresholdEvidencePanel:
    return HeterogeneousThresholdEvidencePanel(
        (
            ThresholdEvidenceDesign(5, 3, 0.7, 0.05),
            ThresholdEvidenceDesign(4, 2, 0.6, 0.02),
            ThresholdEvidenceDesign(6, 4, 0.8, 0.1),
        )
    )


def build_report() -> dict[str, object]:
    panel = build_panel()
    if not panel.verify():
        raise AssertionError("heterogeneous-threshold witness failed verification")
    return {
        "schema_version": 1,
        "scope": "coordinate-specific threshold designs with heterogeneous read counts, thresholds, sensitivity bounds, and false-positive bounds",
        "non_claim": "the replay does not infer coordinate states, error rates, or cross-coordinate independence",
        "coordinate_designs": [
            {
                "read_count": design.read_count,
                "positive_threshold": design.positive_threshold,
                "sensitivity_lower_bound": design.sensitivity_lower_bound,
                "false_positive_upper_bound": design.false_positive_upper_bound,
                "false_alert_probability_upper_bound": round(
                    design.false_alert_probability_upper_bound, 12
                ),
                "detection_probability_lower_bound": round(
                    design.detection_probability_lower_bound, 12
                ),
                "evidence_ratio_lower_bound": round(
                    design.evidence_ratio_lower_bound, 12
                ),
            }
            for design in panel.per_coordinate
        ],
        "panel_bounds": {
            "coordinate_count": panel.coordinate_count,
            "expected_false_alerts_upper_bound": round(
                panel.expected_false_alerts_upper_bound, 12
            ),
            "familywise_false_alert_upper_bound": round(
                panel.familywise_false_alert_upper_bound, 12
            ),
            "exact_independent_all_absent_familywise_false_alert": round(
                panel.exact_independent_all_absent_familywise_false_alert, 12
            ),
            "expected_missed_detections_upper_bound": round(
                panel.expected_missed_detections_upper_bound, 12
            ),
            "all_present_joint_detection_lower_bound_no_independence": round(
                panel.all_present_joint_detection_lower_bound_no_independence, 12
            ),
            "exact_independent_all_present_joint_detection_lower_bound": round(
                panel.exact_independent_all_present_joint_detection_lower_bound, 12
            ),
            "weighted_false_alert_budget_1_2_5": round(
                panel.weighted_false_alert_budget_upper_bound((1, 2, 5)), 12
            ),
        },
        "accepted_coordinates_for_counts_2_2_4": panel.accepted_coordinates((2, 2, 4)),
        "coordinates_with_evidence_ratio_at_least_700": panel.coordinates_meeting_evidence_ratio(
            700
        ),
    }


def main() -> None:
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
