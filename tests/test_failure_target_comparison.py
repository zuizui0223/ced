import pytest

from ced.failure_target_comparison import EqualCostFailureComparison
from ced.target_resolution import (
    CostedTargetResolutionDesign,
    RiskLimitedTargetResolution,
    TargetRecordOutcome,
)


def _resolution(correct, wrong, ambiguity):
    return RiskLimitedTargetResolution(
        "decrease",
        (
            TargetRecordOutcome("correct", correct, frozenset(("decrease",))),
            TargetRecordOutcome("wrong", wrong, frozenset(("increase",))),
            TargetRecordOutcome(
                "ambiguous", ambiguity, frozenset(("decrease", "increase"))
            ),
        ),
    )


def _comparison():
    return EqualCostFailureComparison(
        (
            CostedTargetResolutionDesign("shared_mode", 12, _resolution(0.72, 0.03, 0.25)),
            CostedTargetResolutionDesign("overlapping_modes", 12, _resolution(0.84, 0.025, 0.135)),
            CostedTargetResolutionDesign("independent_modes", 12, _resolution(0.91, 0.02, 0.07)),
        )
    )


def test_equal_cost_ranking_and_feasibility():
    comparison = _comparison()
    assert comparison.shared_cost == 12
    assert comparison.ranked_by_correct_resolution == (
        "independent_modes",
        "overlapping_modes",
        "shared_mode",
    )
    assert comparison.ranked_by_wrong_resolution == (
        "independent_modes",
        "overlapping_modes",
        "shared_mode",
    )
    assert comparison.feasible_designs(0.80, 0.03) == (
        "overlapping_modes",
        "independent_modes",
    )
    assert comparison.feasible_designs(0.90, 0.02) == ("independent_modes",)
    assert comparison.dominant_designs() == ("independent_modes",)


def test_equal_cost_contract_validation():
    with pytest.raises(ValueError):
        EqualCostFailureComparison((_comparison().designs[0],))
    with pytest.raises(ValueError):
        EqualCostFailureComparison(
            (
                _comparison().designs[0],
                CostedTargetResolutionDesign(
                    "different_cost", 13, _resolution(0.9, 0.02, 0.08)
                ),
            )
        )
