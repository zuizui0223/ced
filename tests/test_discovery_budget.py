import pytest

from ced.discovery_budget import FalseDiscoveryBudget
from ced.threshold_detection import ThresholdEvidenceDesign


def test_expected_false_discovery_budget_without_independence():
    per = ThresholdEvidenceDesign(5, 3, 0.7, 0.05)
    budget = FalseDiscoveryBudget(absent_coordinate_count=20, per_coordinate=per)
    assert budget.per_absent_false_alert_upper_bound == pytest.approx(0.001158125)
    assert budget.expected_false_discoveries_upper_bound == pytest.approx(0.0231625)
    assert budget.probability_exceeding_false_discovery_budget_upper_bound(1) == pytest.approx(
        0.0231625
    )
    assert budget.probability_exceeding_false_discovery_budget_upper_bound(2) == pytest.approx(
        0.01158125
    )
    assert budget.expected_false_discovery_proportion_upper_bound(5) == pytest.approx(
        0.0046325
    )
    assert budget.verify()


def test_worst_case_over_screened_coordinates_uses_all_absent_case():
    per = ThresholdEvidenceDesign(5, 3, 0.7, 0.05)
    budget = FalseDiscoveryBudget.worst_case_over_screened_coordinates(20, per)
    assert budget.absent_coordinate_count == 20
    assert budget.expected_false_discoveries_upper_bound == pytest.approx(0.0231625)


def test_zero_absent_coordinates_have_zero_false_discovery_budget():
    per = ThresholdEvidenceDesign(5, 3, 0.7, 0.05)
    budget = FalseDiscoveryBudget(0, per)
    assert budget.expected_false_discoveries_upper_bound == 0.0
    assert budget.probability_exceeding_false_discovery_budget_upper_bound(1) == 0.0
    assert budget.expected_false_discovery_proportion_upper_bound(1) == 0.0
    assert budget.verify()


@pytest.mark.parametrize(
    "constructor",
    [
        lambda: FalseDiscoveryBudget(-1, ThresholdEvidenceDesign(5, 3, 0.7, 0.05)),
        lambda: FalseDiscoveryBudget(1, object()),
        lambda: FalseDiscoveryBudget.worst_case_over_screened_coordinates(0, ThresholdEvidenceDesign(5, 3, 0.7, 0.05)),
    ],
)
def test_discovery_budget_rejects_invalid_contracts(constructor):
    with pytest.raises(ValueError):
        constructor()


def test_budget_methods_reject_invalid_thresholds():
    budget = FalseDiscoveryBudget(20, ThresholdEvidenceDesign(5, 3, 0.7, 0.05))
    with pytest.raises(ValueError):
        budget.probability_exceeding_false_discovery_budget_upper_bound(0)
    with pytest.raises(ValueError):
        budget.expected_false_discovery_proportion_upper_bound(0)
