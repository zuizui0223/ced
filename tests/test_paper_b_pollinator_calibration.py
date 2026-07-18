import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "calibrate_paper_b_pollinator.py"


def test_literature_informed_calibration_changes_protocol_recommendation():
    module = runpy.run_path(str(SCRIPT))
    report = module["calibrated_metrics"]()
    derived = report["derived"]

    assert report["schema_version"] == 1
    assert derived["single_typing_meets_false_resolution_contract"] is False
    assert derived["baseline_typing_meets_false_resolution_contract"] is True
    assert derived["three_replicate_majority_typing_accuracy"]["baseline"] > 0.95
    assert derived["diversified_architecture"]["joint_target_resolution"] > derived["shared_architecture"]["joint_target_resolution"]
    assert derived["architecture_gain"] > 0.10
