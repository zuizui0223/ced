"""Finite adaptive-policy checks for alpha spending."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from ced.adaptive_spending import AdaptiveAlphaSpend, AdaptiveAlphaSpendingLedger


@dataclass(frozen=True)
class _Node:
    name: str
    alpha: float
    positive: "_Node | None" = None
    negative: "_Node | None" = None


def _enumerate_policy(node: _Node | None, probability: float = 1.0, any_alert: bool = False):
    if node is None:
        yield probability, any_alert, 0.0
        return
    # Stage is selected on reaching this node; the spend is incurred regardless of
    # the outcome. The outcome is generated at the declared conditional alpha.
    for leaf_probability, leaf_alert, downstream_spend in _enumerate_policy(
        node.positive, probability * node.alpha, True
    ):
        yield leaf_probability, leaf_alert, node.alpha + downstream_spend
    for leaf_probability, leaf_alert, downstream_spend in _enumerate_policy(
        node.negative, probability * (1.0 - node.alpha), any_alert
    ):
        yield leaf_probability, leaf_alert, node.alpha + downstream_spend


def test_adaptive_policy_false_alert_is_bounded_by_expected_spend():
    # A is always run. If A alerts, confirm in a different mode with B. If A does
    # not alert, screen another coordinate with C; if C alerts, confirm with D.
    policy = _Node(
        "A",
        0.01,
        positive=_Node("B", 0.02),
        negative=_Node("C", 0.03, positive=_Node("D", 0.04)),
    )
    leaves = list(_enumerate_policy(policy))
    assert sum(probability for probability, _, _ in leaves) == pytest.approx(1.0)
    exact_any_false_alert = sum(probability for probability, any_alert, _ in leaves if any_alert)
    expected_spent_alpha = sum(probability * spend for probability, _, spend in leaves)

    all_possible_stage_ledger = AdaptiveAlphaSpendingLedger(
        3,
        (
            AdaptiveAlphaSpend(0, 0.01, mode="A"),
            AdaptiveAlphaSpend(0, 0.02, mode="B"),
            AdaptiveAlphaSpend(1, 0.03, mode="C"),
            AdaptiveAlphaSpend(1, 0.04, mode="D"),
        ),
    )

    assert exact_any_false_alert == pytest.approx(0.0397)
    assert expected_spent_alpha == pytest.approx(0.041088)
    assert exact_any_false_alert <= expected_spent_alpha
    assert expected_spent_alpha <= all_possible_stage_ledger.total_spent_alpha
    assert exact_any_false_alert <= all_possible_stage_ledger.familywise_false_alert_upper_bound


def test_prefix_bounds_match_every_adaptive_path_ledger():
    alert_path = AdaptiveAlphaSpendingLedger(
        3,
        (
            AdaptiveAlphaSpend(0, 0.01, mode="A"),
            AdaptiveAlphaSpend(0, 0.02, mode="B"),
        ),
    )
    no_alert_then_alert_path = AdaptiveAlphaSpendingLedger(
        3,
        (
            AdaptiveAlphaSpend(0, 0.01, mode="A"),
            AdaptiveAlphaSpend(1, 0.03, mode="C"),
            AdaptiveAlphaSpend(1, 0.04, mode="D"),
        ),
    )
    assert alert_path.prefix_familywise_false_alert_upper_bounds == pytest.approx(
        (0.01, 0.03)
    )
    assert no_alert_then_alert_path.prefix_familywise_false_alert_upper_bounds == pytest.approx(
        (0.01, 0.04, 0.08)
    )
