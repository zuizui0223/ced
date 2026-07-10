"""Independent finite checks for heterogeneous threshold panels."""

from __future__ import annotations

from itertools import product
from math import fsum

import pytest

from ced.heterogeneous_thresholds import HeterogeneousThresholdEvidencePanel
from ced.threshold_detection import ThresholdEvidenceDesign, binomial_probability


def _all_counts_probability(designs, counts, probabilities):
    return product_probability(
        binomial_probability(design.read_count, count, probability)
        for design, count, probability in zip(designs, counts, probabilities)
    )


def product_probability(values):
    out = 1.0
    for value in values:
        out *= value
    return out


def _enumerated_independent_all_absent_familywise(panel):
    designs = panel.per_coordinate
    total = 0.0
    for counts in product(*(range(design.read_count + 1) for design in designs)):
        probability = _all_counts_probability(
            designs,
            counts,
            [design.false_positive_upper_bound for design in designs],
        )
        if panel.accepted_coordinates(counts):
            total += probability
    return total


def _enumerated_independent_all_present_joint_detection(panel):
    designs = panel.per_coordinate
    total = 0.0
    for counts in product(*(range(design.read_count + 1) for design in designs)):
        probability = _all_counts_probability(
            designs,
            counts,
            [design.sensitivity_lower_bound for design in designs],
        )
        if len(panel.accepted_coordinates(counts)) == panel.coordinate_count:
            total += probability
    return total


def _enumerated_expected_false_alerts(panel):
    return fsum(panel.per_coordinate_false_alert_upper_bounds)


def test_heterogeneous_independent_formulas_match_finite_enumeration():
    panel = HeterogeneousThresholdEvidencePanel(
        (
            ThresholdEvidenceDesign(3, 2, 0.7, 0.05),
            ThresholdEvidenceDesign(4, 3, 0.6, 0.02),
            ThresholdEvidenceDesign(2, 1, 0.8, 0.1),
        )
    )
    assert _enumerated_expected_false_alerts(panel) == pytest.approx(
        panel.expected_false_alerts_upper_bound
    )
    assert _enumerated_independent_all_absent_familywise(panel) == pytest.approx(
        panel.exact_independent_all_absent_familywise_false_alert
    )
    assert _enumerated_independent_all_present_joint_detection(panel) == pytest.approx(
        panel.exact_independent_all_present_joint_detection_lower_bound
    )
    assert panel.exact_independent_all_absent_familywise_false_alert <= (
        panel.familywise_false_alert_upper_bound + 1e-12
    )
    assert panel.all_present_joint_detection_lower_bound_no_independence <= (
        panel.exact_independent_all_present_joint_detection_lower_bound + 1e-12
    )


def test_frechet_all_present_bound_is_sharp_for_two_coordinates():
    beta_1 = 0.8
    beta_2 = 0.7
    panel = HeterogeneousThresholdEvidencePanel(
        (
            ThresholdEvidenceDesign(1, 1, beta_1, 0.01),
            ThresholdEvidenceDesign(1, 1, beta_2, 0.01),
        )
    )
    # Extremal dependent construction: two detection events overlap as little as
    # their marginal probabilities allow, so P(A and B) = beta_1 + beta_2 - 1.
    assert panel.all_present_joint_detection_lower_bound_no_independence == pytest.approx(
        beta_1 + beta_2 - 1.0
    )


def test_union_familywise_bound_is_sharp_for_disjoint_false_alerts():
    alpha_1 = 0.02
    alpha_2 = 0.03
    panel = HeterogeneousThresholdEvidencePanel(
        (
            ThresholdEvidenceDesign(1, 1, 0.8, alpha_1),
            ThresholdEvidenceDesign(1, 1, 0.8, alpha_2),
        )
    )
    # Extremal dependent construction: two false-alert events are disjoint, so
    # P(A union B) = alpha_1 + alpha_2.
    assert panel.familywise_false_alert_upper_bound == pytest.approx(alpha_1 + alpha_2)
