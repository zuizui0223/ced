import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "simulate_paper_b_benchmark.py"


def test_paper_b_grid_is_exact_and_target_safe_respects_contract():
    module = runpy.run_path(str(SCRIPT))
    report = module["run_grid"]()

    assert report["schema_version"] == 4
    assert report["grid_size"] == 216
    assert {row["strategy"] for row in report["rows"]} == {
        "state_only",
        "full_identification",
        "information_gain",
        "target_safe",
    }
    assert len(module["WORLDS"]) == 16
    assert report["headline_checks"]["target_safe_max_wrong_probability"] <= 0.05

    for row in report["rows"]:
        total = (
            row["correct_probability"]
            + row["wrong_probability"]
            + row["ambiguity_probability"]
        )
        assert abs(total - 1.0) < 1e-12


def test_full_world_information_gain_can_choose_target_irrelevant_experiment():
    module = runpy.run_path(str(SCRIPT))
    parameters = module["Parameters"](
        response_typing_accuracy=0.95,
        common_failure_probability=0.0,
    )
    gains = module["expected_information_gain"](parameters)
    metrics = module["evaluate"](parameters, "independent")

    assert gains["nuisance_experiment"] == 2.0
    assert gains["nuisance_experiment"] > gains["response_experiment"]
    assert metrics["information_gain"]["correct_probability"] == 0.0
    assert metrics["information_gain"]["ambiguity_probability"] > 0.0


def test_target_safe_resolves_target_without_full_identification():
    module = runpy.run_path(str(SCRIPT))
    parameters = module["Parameters"](
        state_detection_sensitivity=0.95,
        response_typing_accuracy=0.99,
        common_failure_probability=0.0,
        false_resolution_limit=0.05,
    )
    metrics = module["evaluate"](parameters, "independent")

    assert metrics["target_safe"]["correct_probability"] > metrics["information_gain"]["correct_probability"]
    assert metrics["target_safe"]["expected_cost"] < metrics["full_identification"]["expected_cost"]
    assert metrics["target_safe"]["wrong_probability"] <= parameters.false_resolution_limit


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
