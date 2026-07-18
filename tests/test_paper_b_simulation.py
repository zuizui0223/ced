import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "simulate_paper_b_benchmark.py"


def test_paper_b_grid_is_exact_and_failure_architecture_changes_resolution():
    module = runpy.run_path(str(SCRIPT))
    report = module["run_grid"]()

    assert report["schema_version"] == 3
    assert report["grid_size"] == 216
    assert {row["strategy"] for row in report["rows"]} == {
        "state_only",
        "full_identification",
        "information_gain",
        "target_safe",
    }
    checks = report["headline_checks"]
    assert checks["target_safe_max_wrong_probability"] <= 0.05
    assert checks["independent_modes_break_shared_ceiling"] is True
    assert checks["independent_mode_best_correct_resolution"] > checks["shared_failure_correct_resolution_ceiling"]

    for row in report["rows"]:
        total = (
            row["correct_probability"]
            + row["wrong_probability"]
            + row["ambiguity_probability"]
        )
        assert abs(total - 1.0) < 1e-12


def test_target_safe_abstains_when_response_error_exceeds_contract():
    module = runpy.run_path(str(SCRIPT))
    parameters = module["Parameters"](
        state_detection_sensitivity=0.95,
        response_typing_accuracy=0.85,
        common_failure_probability=0.0,
        false_resolution_limit=0.05,
    )
    metrics = module["evaluate"](parameters, "independent")

    assert metrics["target_safe"]["wrong_probability"] == 0.0
    assert metrics["target_safe"]["ambiguity_probability"] > 0.0
    assert metrics["full_identification"]["wrong_probability"] > 0.0
