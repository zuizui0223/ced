import runpy
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "simulate_paper_b_benchmark.py"


def load_module():
    return runpy.run_path(str(SCRIPT))


def test_grid_is_exact_and_all_strategy_probabilities_normalize():
    module = load_module()
    report = module["run_grid"]()

    assert report["schema_version"] == 5
    assert report["grid_size"] == 216
    assert len(module["WORLDS"]) == 16
    assert {row["strategy"] for row in report["rows"]} == {
        "state_only",
        "full_identification",
        "full_world_eig",
        "target_safe",
    }
    for row in report["rows"]:
        total = (
            row["correct_probability"]
            + row["wrong_probability"]
            + row["ambiguity_probability"]
        )
        assert total == pytest.approx(1.0, abs=1e-12)


def test_information_gain_is_computed_from_explicit_likelihood_kernels():
    module = load_module()
    parameters = module["Parameters"](
        response_typing_accuracy=0.95,
        common_failure_probability=0.0,
    )
    belief = module["normalize"](
        {
            world: mass
            for world, mass in module["prior"](parameters).items()
            if world[0] == 1
        }
    )
    response_gain = module["mutual_information"](
        belief, module["response_kernel"](parameters)
    )
    nuisance_gain = module["mutual_information"](
        belief, module["nuisance_kernel"](parameters)
    )

    assert response_gain == pytest.approx(1.0 - module["entropy"]((0.95, 0.05)))
    assert nuisance_gain == pytest.approx(2.0)
    assert module["benchmark_contrast"](parameters)["full_world_eig_choice"] == "nuisance"


def test_response_and_nuisance_experiments_do_not_leak_each_others_outcomes():
    module = load_module()
    parameters = module["Parameters"]()
    world = (1, 0, 3)

    assert set(module["response_kernel"](parameters)(world)) == {0, 1}
    assert module["nuisance_kernel"](parameters)(world) == {3: 1.0}


def test_false_resolution_boundary_accepts_exact_five_percent_error():
    module = load_module()
    parameters = module["Parameters"](
        response_typing_accuracy=0.95,
        false_resolution_limit=0.05,
    )
    belief = module["normalize"](
        {
            world: mass
            for world, mass in module["prior"](parameters).items()
            if world[0] == 1
        }
    )
    updated = module["posterior"](
        belief, module["response_kernel"](parameters), 0
    )

    assert module["risk_limited_report"](updated, 0.05) == frozenset(("response-A",))


def test_target_safe_uses_response_experiment_and_avoids_nuisance_cost():
    module = load_module()
    parameters = module["Parameters"](
        state_detection_sensitivity=0.95,
        response_typing_accuracy=0.99,
        common_failure_probability=0.0,
        false_resolution_limit=0.05,
    )
    contrast = module["benchmark_contrast"](parameters)
    metrics = module["evaluate"](parameters, "independent")

    assert contrast["target_safe_choice"] == "response"
    assert metrics["target_safe"]["correct_probability"] > metrics["full_world_eig"]["correct_probability"]
    assert metrics["target_safe"]["expected_cost"] < metrics["full_identification"]["expected_cost"]
    assert metrics["target_safe"]["wrong_probability"] <= parameters.false_resolution_limit + 1e-12


def test_target_safe_does_not_pay_for_unresolving_experiment():
    module = load_module()
    parameters = module["Parameters"](
        state_detection_sensitivity=0.95,
        response_typing_accuracy=0.85,
        common_failure_probability=0.0,
        false_resolution_limit=0.05,
    )
    contrast = module["benchmark_contrast"](parameters)
    metrics = module["evaluate"](parameters, "independent")

    assert contrast["target_safe_choice"] is None
    assert metrics["target_safe"]["wrong_probability"] == pytest.approx(
        metrics["state_only"]["wrong_probability"]
    )
    assert metrics["target_safe"]["wrong_probability"] <= parameters.false_resolution_limit + 1e-12
    assert metrics["target_safe"]["expected_cost"] == pytest.approx(
        metrics["state_only"]["expected_cost"]
    )
