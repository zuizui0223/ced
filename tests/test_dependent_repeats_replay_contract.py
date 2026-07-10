import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_dependent_repeats.py"


def test_dependent_repeat_replay_matches_declared_witness():
    report = runpy.run_path(str(SCRIPT))["build_report"]()
    assert report["schema_version"] == 1
    assert report["threshold_design"] == {
        "read_count": 5,
        "positive_threshold": 3,
        "sensitivity_lower_bound": 0.7,
        "false_positive_upper_bound": 0.05,
        "false_alert_probability_upper_bound": 0.083333333333,
        "detection_probability_lower_bound": 0.5,
        "evidence_ratio_lower_bound": 6.0,
        "threshold_crossing_certifies_presence": False,
    }
    assert report["any_positive_nonreset"]["detection_probability_lower_bound"] == 0.6
    assert report["zero_false_positive_boundary"] == {
        "false_alert_probability_upper_bound": 0.0,
        "detection_probability_lower_bound": 0.5,
        "threshold_crossing_certifies_presence": True,
    }
