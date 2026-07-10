"""Independent sharpness checks for dependent-repeat threshold bounds."""

from __future__ import annotations

from math import floor, fsum

import pytest

from ced.dependent_repeats import DependentThresholdEvidenceDesign


def _event_probability(count_distribution: dict[int, float], threshold: int) -> float:
    return fsum(probability for count, probability in count_distribution.items() if count >= threshold)


def _expected_count(count_distribution: dict[int, float]) -> float:
    return fsum(count * probability for count, probability in count_distribution.items())


def _absent_extremal_count_distribution(
    read_count: int, threshold: int, false_positive_rate: float
) -> dict[int, float]:
    """Distribution with read marginals <= f and threshold probability at Markov."""
    if read_count * false_positive_rate >= threshold:
        return {threshold: 1.0}
    threshold_probability = read_count * false_positive_rate / threshold
    return {threshold: threshold_probability, 0: 1.0 - threshold_probability}


def _present_extremal_count_distribution(
    read_count: int, threshold: int, sensitivity: float
) -> dict[int, float]:
    """Distribution with read marginals >= p and minimal threshold probability."""
    mean = read_count * sensitivity
    if mean <= threshold - 1:
        lower = floor(mean)
        upper = lower + 1
        if lower == upper or upper >= threshold:
            return {lower: 1.0}
        upper_weight = mean - lower
        return {lower: 1.0 - upper_weight, upper: upper_weight}
    threshold_probability = (mean - (threshold - 1)) / (read_count - threshold + 1)
    return {read_count: threshold_probability, threshold - 1: 1.0 - threshold_probability}


@pytest.mark.parametrize(
    "read_count,threshold,false_positive_rate",
    [
        (5, 3, 0.05),
        (10, 1, 0.05),
        (5, 5, 0.05),
        (4, 2, 0.8),
    ],
)
def test_absent_markov_bound_is_sharp_under_dependence(
    read_count, threshold, false_positive_rate
):
    design = DependentThresholdEvidenceDesign(
        read_count, threshold, 0.99, false_positive_rate
    )
    distribution = _absent_extremal_count_distribution(
        read_count, threshold, false_positive_rate
    )
    event_probability = _event_probability(distribution, threshold)
    marginal_probability = _expected_count(distribution) / read_count
    assert marginal_probability <= false_positive_rate + 1e-12
    assert event_probability == pytest.approx(
        design.false_alert_probability_upper_bound, abs=1e-12
    )


@pytest.mark.parametrize(
    "read_count,threshold,sensitivity,false_positive_rate",
    [
        (5, 3, 0.7, 0.05),
        (10, 1, 0.6, 0.05),
        (5, 5, 0.7, 0.05),
        (4, 3, 0.4, 0.05),
    ],
)
def test_present_detection_bound_is_sharp_under_dependence(
    read_count, threshold, sensitivity, false_positive_rate
):
    design = DependentThresholdEvidenceDesign(
        read_count, threshold, sensitivity, false_positive_rate
    )
    distribution = _present_extremal_count_distribution(read_count, threshold, sensitivity)
    event_probability = _event_probability(distribution, threshold)
    marginal_probability = _expected_count(distribution) / read_count
    assert marginal_probability >= sensitivity - 1e-12
    assert event_probability == pytest.approx(
        design.detection_probability_lower_bound, abs=1e-12
    )


def test_dependent_bound_is_weaker_than_binomial_when_independence_would_hold():
    design = DependentThresholdEvidenceDesign(5, 3, 0.7, 0.05)
    assert design.false_alert_probability_upper_bound > 0.001158125
    assert design.detection_probability_lower_bound < 0.83692
