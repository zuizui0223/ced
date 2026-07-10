from math import inf

import pytest

from ced.threshold_detection import (
    ThresholdEvidenceDesign,
    binomial_probability,
    binomial_tail,
)


def test_threshold_event_has_posterior_free_evidence_ratio():
    design = ThresholdEvidenceDesign(
        read_count=5,
        positive_threshold=3,
        sensitivity_lower_bound=0.7,
        false_positive_upper_bound=0.05,
    )
    assert design.detection_probability_lower_bound == pytest.approx(0.83692)
    assert design.false_alert_probability_upper_bound == pytest.approx(0.001158125)
    assert design.evidence_ratio_lower_bound == pytest.approx(722.650836481381)
    assert not design.threshold_is_presence_certificate
    assert design.accepts(3)
    assert not design.accepts(2)
    assert design.verify()


def test_threshold_search_returns_first_ratio_feasible_threshold():
    assert (
        ThresholdEvidenceDesign.minimum_threshold_for_evidence_ratio(5, 0.7, 0.05, 100)
        == 3
    )
    weaker = ThresholdEvidenceDesign(5, 2, 0.7, 0.05)
    assert weaker.evidence_ratio_lower_bound < 100
    with pytest.raises(ValueError):
        ThresholdEvidenceDesign.minimum_threshold_for_evidence_ratio(5, 0.7, 0.05, 1_000_000)


def test_zero_false_positive_contract_recovers_deductive_certificate():
    design = ThresholdEvidenceDesign(4, 1, 0.6, 0.0)
    assert design.false_alert_probability_upper_bound == 0.0
    assert design.evidence_ratio_lower_bound == inf
    assert design.threshold_is_presence_certificate


def test_binomial_probability_and_tail_edge_cases():
    assert binomial_probability(5, 0, 0.2) == pytest.approx(0.8**5)
    assert binomial_probability(5, 5, 0.2) == pytest.approx(0.2**5)
    assert binomial_tail(5, 0, 0.2) == 1.0
    assert binomial_tail(5, 5, 0.2) == pytest.approx(0.2**5)


@pytest.mark.parametrize(
    "constructor",
    [
        lambda: ThresholdEvidenceDesign(0, 1, 0.7, 0.05),
        lambda: ThresholdEvidenceDesign(5, 0, 0.7, 0.05),
        lambda: ThresholdEvidenceDesign(5, 6, 0.7, 0.05),
        lambda: ThresholdEvidenceDesign(5, 3, 0.05, 0.05),
        lambda: ThresholdEvidenceDesign(5, 3, 0.05, 0.1),
    ],
)
def test_threshold_design_rejects_invalid_contracts(constructor):
    with pytest.raises(ValueError):
        constructor()
