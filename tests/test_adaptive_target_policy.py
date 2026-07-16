import runpy
from pathlib import Path

import pytest

from ced.adaptive_target_policy import (
    AdaptiveTargetBranch,
    AdaptiveTargetPolicy,
    cheapest_feasible_policy,
)


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_pollinator_adaptive_policy.py"


def test_pollinator_adaptive_policies_match_declared_risk_and_cost():
    module = runpy.run_path(str(SCRIPT))
    policies = module["build_policies"]()
    by_name = {policy.name: policy for policy in policies}

    assert by_name["shared"].expected_total_cost == pytest.approx(2.5)
    assert by_name["shared"].correct_probability("decrease") == pytest.approx(0.6)
    assert by_name["shared"].wrong_probability("decrease") == pytest.approx(0.0725)
    assert by_name["shared"].ambiguity_probability("decrease") == pytest.approx(0.3275)

    assert by_name["overlapping"].expected_total_cost == pytest.approx(2.7)
    assert by_name["overlapping"].correct_probability("decrease") == pytest.approx(0.765)
    assert by_name["overlapping"].wrong_probability("decrease") == pytest.approx(0.05125)
    assert by_name["overlapping"].ambiguity_probability("decrease") == pytest.approx(0.18375)

    assert by_name["independent"].expected_total_cost == pytest.approx(2.86)
    assert by_name["independent"].correct_probability("decrease") == pytest.approx(0.8928)
    assert by_name["independent"].wrong_probability("decrease") == pytest.approx(0.03395)
    assert by_name["independent"].ambiguity_probability("decrease") == pytest.approx(0.07325)
    assert all(policy.verify("decrease") for policy in policies)


def test_independent_policy_is_only_feasible_strict_contract():
    policies = runpy.run_path(str(SCRIPT))["build_policies"]()
    selected = cheapest_feasible_policy(policies, "decrease", 0.85, 0.04, 3.0)
    assert selected is not None
    assert selected.name == "independent"
    assert cheapest_feasible_policy(policies, "decrease", 0.95, 0.02, 3.0) is None


def test_adaptive_policy_validates_tree_contract():
    terminal = AdaptiveTargetPolicy.stop("stop", ("a", "b"))
    assert terminal.is_terminal
    with pytest.raises(ValueError):
        AdaptiveTargetPolicy("bad", experiment_cost=1.0)
    with pytest.raises(ValueError):
        AdaptiveTargetPolicy(
            "bad-probabilities",
            experiment_cost=1.0,
            branches=(AdaptiveTargetBranch("x", 0.5, terminal),),
        )
