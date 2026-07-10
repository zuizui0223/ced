import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_multiple_testing.py"


def test_multiple_testing_replay_matches_declared_witness():
    report = runpy.run_path(str(SCRIPT))["build_report"]()
    assert report["schema_version"] == 1
    assert report["per_coordinate"] == {
        "read_count": 5,
        "positive_threshold": 3,
        "false_alert_probability_upper_bound": 0.001158125,
        "detection_probability_lower_bound": 0.83692,
        "evidence_ratio_lower_bound": 722.650836481381,
    }
    assert report["familywise"] == {
        "coordinate_count": 20,
        "expected_false_alerts_upper_bound": 0.0231625,
        "bonferroni_familywise_false_alert_upper_bound": 0.0231625,
        "exact_independent_all_absent_familywise_false_alert": 0.022909423955,
    }
    assert report["frontier"] == {
        "target_familywise_alpha": 0.05,
        "target_evidence_ratio": 100,
        "minimum_threshold": 3,
    }
