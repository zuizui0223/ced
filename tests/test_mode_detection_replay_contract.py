import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_mode_detection.py"


def test_mode_detection_replay_matches_declared_witness():
    report = runpy.run_path(str(SCRIPT))["build_report"]()
    assert report["schema_version"] == 1
    assert report["one_mode_same_effort"] == {
        "mode_count": 1,
        "repetitions_per_mode": 10,
        "total_reads": 30,
        "availability_ceiling": 0.8,
        "joint_detection_lower_bound": 0.799748368147,
    }
    assert report["mode_diverse_design"] == {
        "mode_count": 2,
        "repetitions_per_mode": 5,
        "total_reads": 30,
        "availability_ceiling": 0.96,
        "joint_detection_lower_bound": 0.950068614217,
        "all_negative_probability_upper_bound_if_all_present": 0.040000343598,
    }
    assert report["design_frontier"] == {
        "target_joint_confidence": 0.95,
        "necessary_mode_floor": 2,
        "minimum_repetitions_per_mode_at_floor": 5,
    }
