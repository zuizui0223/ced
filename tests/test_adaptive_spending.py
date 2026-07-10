import pytest

from ced.adaptive_spending import AdaptiveAlphaSpend, AdaptiveAlphaSpendingLedger


def _ledger() -> AdaptiveAlphaSpendingLedger:
    return AdaptiveAlphaSpendingLedger(
        3,
        (
            AdaptiveAlphaSpend(0, 0.005, mode="camera-a", label="screen"),
            AdaptiveAlphaSpend(1, 0.01, mode="camera-b", label="screen"),
            AdaptiveAlphaSpend(0, 0.002, mode="camera-c", label="confirm"),
            AdaptiveAlphaSpend(2, 0.003, mode="camera-a", label="screen"),
        ),
    )


def test_adaptive_alpha_spending_bounds():
    ledger = _ledger()
    assert ledger.coordinate_count == 3
    assert ledger.spend_count == 4
    assert ledger.total_spent_alpha == pytest.approx(0.02)
    assert ledger.familywise_false_alert_upper_bound == pytest.approx(0.02)
    assert ledger.expected_false_alerts_upper_bound == pytest.approx(0.02)
    assert ledger.per_coordinate_spent_alpha == pytest.approx((0.007, 0.01, 0.003))
    assert ledger.per_coordinate_false_alert_upper_bounds == pytest.approx(
        (0.007, 0.01, 0.003)
    )
    assert ledger.prefix_familywise_false_alert_upper_bounds == pytest.approx(
        (0.005, 0.015, 0.017, 0.02)
    )
    assert ledger.weighted_false_alert_budget_upper_bound((1, 2, 5)) == pytest.approx(
        0.042
    )
    assert ledger.within_total_budget(0.025)
    assert not ledger.within_total_budget(0.019)
    assert ledger.remaining_alpha_budget(0.05) == pytest.approx(0.03)
    assert ledger.verify()


def test_stages_for_coordinate_and_append():
    ledger = _ledger()
    assert [stage.label for stage in ledger.stages_for_coordinate(0)] == [
        "screen",
        "confirm",
    ]
    assert ledger.stages_for_coordinate(1)[0].mode == "camera-b"
    extended = ledger.append(2, 0.004, mode="camera-d", label="confirm")
    assert extended.total_spent_alpha == pytest.approx(0.024)
    assert extended.per_coordinate_spent_alpha == pytest.approx((0.007, 0.01, 0.007))
    assert extended.spends[-1].label == "confirm"


def test_from_coordinate_alphas_constructor():
    ledger = AdaptiveAlphaSpendingLedger.from_coordinate_alphas(
        2, ((0, 0.01), (1, 0.02), (1, 0.03))
    )
    assert ledger.per_coordinate_spent_alpha == pytest.approx((0.01, 0.05))
    assert ledger.familywise_false_alert_upper_bound == pytest.approx(0.06)


def test_familywise_bound_saturates_at_one():
    ledger = AdaptiveAlphaSpendingLedger.from_coordinate_alphas(
        2, ((0, 0.9), (1, 0.8))
    )
    assert ledger.total_spent_alpha == pytest.approx(1.7)
    assert ledger.familywise_false_alert_upper_bound == 1.0
    assert ledger.per_coordinate_false_alert_upper_bounds == pytest.approx((0.9, 0.8))


@pytest.mark.parametrize(
    "constructor",
    [
        lambda: AdaptiveAlphaSpend(-1, 0.1),
        lambda: AdaptiveAlphaSpend(0, -0.1),
        lambda: AdaptiveAlphaSpend(0, 1.1),
        lambda: AdaptiveAlphaSpend(0, 0.1, mode=object()),
        lambda: AdaptiveAlphaSpendingLedger(0, ()),
        lambda: AdaptiveAlphaSpendingLedger(1, (object(),)),
        lambda: AdaptiveAlphaSpendingLedger(1, (AdaptiveAlphaSpend(1, 0.1),)),
    ],
)
def test_rejects_invalid_adaptive_spending_contracts(constructor):
    with pytest.raises(ValueError):
        constructor()


def test_rejects_invalid_budget_and_weights():
    ledger = _ledger()
    with pytest.raises(ValueError):
        ledger.remaining_alpha_budget(1.1)
    with pytest.raises(ValueError):
        ledger.within_total_budget(-0.1)
    with pytest.raises(ValueError):
        ledger.weighted_false_alert_budget_upper_bound((1, 2))
    with pytest.raises(ValueError):
        ledger.weighted_false_alert_budget_upper_bound((1, -1, 1))
    with pytest.raises(ValueError):
        ledger.stages_for_coordinate(3)
