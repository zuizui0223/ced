import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_imperfect_detection.py"


def test_imperfect_detection_replay_matches_declared_witness():
    report = runpy.run_path(str(SCRIPT))["build_report"]()
    assert report["schema_version"] == 1
    assert report["finite_negative_limit"] == {
        "sensitivity_lower_bound": 0.6,
        "repetitions": 5,
        "all_negative_probability_upper_bound_if_present": 0.01024,
        "absence_certified_by_all_negatives": False,
    }
    assert report["risk_limited_design"] == {
        "coordinate_count": 3,
        "target_joint_confidence": 0.95,
        "minimum_repetitions_per_coordinate": 5,
        "total_reads": 15,
        "joint_detection_lower_bound": 0.969593499058,
    }
    assert report["positive_signature_example"] == [1, 2]
