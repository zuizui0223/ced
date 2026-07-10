import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_calibration_bounds.py"


def test_calibration_bound_replay_matches_declared_witness():
    report = runpy.run_path(str(SCRIPT))["build_report"]()
    assert report["schema_version"] == 1
    assert report["calibration"] == {
        "blank_read_count": 60,
        "blank_positive_count": 0,
        "present_read_count": 60,
        "present_positive_count": 55,
        "delta": 0.05,
        "false_positive_upper_bound": 0.04870291331,
        "sensitivity_lower_bound": 0.832736923575,
        "confidence_level_per_bound": 0.95,
        "joint_confidence_lower_bound": 0.9,
    }
    assert report["threshold_design"] == {
        "read_count": 5,
        "positive_threshold": 3,
        "false_alert_probability_upper_bound": 0.001072470525,
        "detection_probability_lower_bound": 0.964160039883,
        "evidence_ratio_lower_bound": 899.00842742217,
    }
    assert report["multiple_testing"] == {
        "coordinate_count": 20,
        "familywise_false_alert_upper_bound": 0.021449410494,
        "exact_independent_all_absent_familywise_false_alert": 0.021232273676,
    }
