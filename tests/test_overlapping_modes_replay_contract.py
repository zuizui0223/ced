import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_overlapping_modes.py"


def test_overlapping_mode_replay_matches_declared_witness():
    report = runpy.run_path(str(SCRIPT))["build_report"]()
    assert report["schema_version"] == 1
    assert report["partial_overlap"] == {
        "coordinate_count": 3,
        "mode_count": 2,
        "factor_count": 3,
        "shared_factor_count": 1,
        "pairwise_mode_overlap_counts": ((2, 1), (1, 2)),
        "within_mode_coordinate_miss_probability_upper_bound": 0.16,
        "all_modes_failed_probability": 0.224,
        "availability_ceiling": 0.776,
        "joint_detection_probability_lower_bound": 0.627490736603,
        "total_read_count": 12,
    }
    assert report["endpoint_comparison"] == {
        "independent_mode_availability_ceiling": 0.96,
        "independent_mode_joint_detection_lower_bound": 0.942020500122,
        "common_mode_availability_ceiling": 0.8,
        "common_mode_joint_detection_lower_bound": 0.798834025153,
    }
