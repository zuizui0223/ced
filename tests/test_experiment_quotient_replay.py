import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_experiment_quotient.py"


def test_experiment_quotient_replay_supports_combined_paper_decision():
    report = runpy.run_path(str(SCRIPT))["build_report"]()
    assert report["schema_version"] == 1
    assert report["designs"]["passive"] == {
        "quotient_state_count": 1,
        "residual_class_sizes": (4,),
        "deterministic_report_exists": False,
        "compatible_targets": ("decrease", "increase", "no-interaction"),
    }
    assert report["designs"]["detection_only"] == {
        "quotient_state_count": 2,
        "residual_class_sizes": (2, 2),
        "deterministic_report_exists": False,
        "absent_targets": ("no-interaction",),
        "present_targets": ("decrease", "increase"),
    }
    assert report["designs"]["detection_plus_intervention"]["quotient_state_count"] == 3
    assert report["designs"]["detection_plus_intervention"]["residual_class_sizes"] == (2, 1, 1)
    assert report["designs"]["detection_plus_intervention"]["deterministic_report_exists"] is True
    assert report["refinement_order"] == {
        "detection_refines_passive": True,
        "combined_refines_detection": True,
    }
    assert report["shared_failure_record"] == {
        "compatible_worlds": ((1, 0), (1, 1)),
        "compatible_targets": ("decrease", "increase"),
        "deterministic_report_exists": False,
    }
    assert report["submission_decision"]["bridge_is_joint"] is True
