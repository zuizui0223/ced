import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_threshold_detection.py"


def test_threshold_detection_replay_matches_declared_witness():
    report = runpy.run_path(str(SCRIPT))["build_report"]()
    assert report["schema_version"] == 1
    assert report["threshold_design"] == {
        "read_count": 5,
        "positive_threshold": 3,
        "sensitivity_lower_bound": 0.7,
        "false_positive_upper_bound": 0.05,
        "detection_probability_lower_bound": 0.83692,
        "false_alert_probability_upper_bound": 0.001158125,
        "evidence_ratio_lower_bound": 722.650836481237,
        "threshold_is_presence_certificate": False,
    }
    assert report["frontier"] == {
        "target_evidence_ratio": 100,
        "minimum_threshold": 3,
    }
