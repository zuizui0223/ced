import pytest

from ced.adaptive_target_policy import (
    AdaptiveTargetBranch,
    AdaptiveTargetPolicy,
    cheapest_feasible_policy,
)


def build_generic_policies():
    ambiguous = AdaptiveTargetPolicy.stop("ambiguous", ("response-A", "response-B"))
    correct = AdaptiveTargetPolicy.stop("correct", ("response-A",))
    wrong = AdaptiveTargetPolicy.stop("wrong", ("response-B",))
    conservative = AdaptiveTargetPolicy(
        "conservative",
        experiment_cost=1.0,
        branches=(
            AdaptiveTargetBranch("resolved", 0.70, correct),
            AdaptiveTargetBranch("wrong", 0.02, wrong),
            AdaptiveTargetBranch("unresolved", 0.28, ambiguous),
        ),
    )
    intensive = AdaptiveTargetPolicy(
        "intensive",
        experiment_cost=2.0,
        branches=(
            AdaptiveTargetBranch("resolved", 0.90, correct),
            AdaptiveTargetBranch("wrong", 0.01, wrong),
            AdaptiveTargetBranch("unresolved", 0.09, ambiguous),
        ),
    )
    return conservative, intensive


def test_adaptive_policy_decomposes_correct_wrong_and_ambiguous_reports():
    conservative, intensive = build_generic_policies()

    assert conservative.correct_probability("response-A") == pytest.approx(0.70)
    assert conservative.wrong_probability("response-A") == pytest.approx(0.02)
    assert conservative.ambiguity_probability("response-A") == pytest.approx(0.28)
    assert intensive.correct_probability("response-A") == pytest.approx(0.90)
    assert intensive.wrong_probability("response-A") == pytest.approx(0.01)
    assert intensive.ambiguity_probability("response-A") == pytest.approx(0.09)
    assert all(policy.verify("response-A") for policy in (conservative, intensive))


def test_cheapest_feasible_policy_uses_declared_risk_and_cost_contract():
    policies = build_generic_policies()
    selected = cheapest_feasible_policy(
        policies,
        "response-A",
        minimum_correct=0.85,
        maximum_wrong=0.02,
        maximum_expected_cost=3.0,
    )
    assert selected is not None
    assert selected.name == "intensive"
    assert cheapest_feasible_policy(
        policies, "response-A", 0.95, 0.005, 3.0
    ) is None


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
