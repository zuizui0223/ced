import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_heterogeneous_thresholds.py"


def test_heterogeneous_threshold_replay_matches_declared_witness():
    report = runpy.run_path(str(SCRIPT))["build_report"]()
    assert report["schema_version"] == 1
    assert report["coordinate_designs"] == [
        {
            "read_count": 5,
            "positive_threshold": 3,
            "sensitivity_lower_bound": 0.7,
            "false_positive_upper_bound": 0.05,
            "false_alert_probability_upper_bound": 0.001158125,
            "detection_probability_lower_bound": 0.83692,
            "evidence_ratio_lower_bound": 722.650836481381,
        },
        {
            "read_count": 4,
            "positive_threshold": 2,
            "sensitivity_lower_bound": 0.6,
            "false_positive_upper_bound": 0.02,
            "false_alert_probability_upper_bound": 0.00233648,
            "detection_probability_lower_bound": 0.8208,
            "evidence_ratio_lower_bound": 351.2976785592,
        },
        {
            "read_count": 6,
            "positive_threshold": 4,
            "sensitivity_lower_bound": 0.8,
            "false_positive_upper_bound": 0.1,
            "false_alert_probability_upper_bound": 0.00127,
            "detection_probability_lower_bound": 0.90112,
            "evidence_ratio_lower_bound": 709.543307086614,
        },
    ]
    assert report["panel_bounds"] == {
        "coordinate_count": 3,
        "expected_false_alerts_upper_bound": 0.004764605,
        "familywise_false_alert_upper_bound": 0.004764605,
        "exact_independent_all_absent_familywise_false_alert": 0.004757464352,
        "expected_missed_detections_upper_bound": 0.44116,
        "all_present_joint_detection_lower_bound_no_independence": 0.55884,
        "exact_independent_all_present_joint_detection_lower_bound": 0.619018919608,
        "weighted_false_alert_budget_1_2_5": 0.012181085,
    }
    assert report["accepted_coordinates_for_counts_2_2_4"] == (1, 2)
    assert report["coordinates_with_evidence_ratio_at_least_700"] == (0, 2)
