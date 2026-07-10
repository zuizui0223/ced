"""Independent finite-outcome checks for false-discovery budget bounds."""

from __future__ import annotations

from itertools import product
from math import fsum

import pytest

from ced.discovery_budget import FalseDiscoveryBudget
from ced.threshold_detection import ThresholdEvidenceDesign


def _alert_probability_by_record_enumeration(read_count: int, threshold: int, rate: float) -> float:
    total = 0.0
    for record in product((False, True), repeat=read_count):
        positives = sum(record)
        if positives >= threshold:
            total += rate**positives * (1.0 - rate) ** (read_count - positives)
    return total


def _false_discovery_distribution(
    absent_coordinate_count: int, read_count: int, threshold: int, false_positive_rate: float
) -> dict[int, float]:
    coordinate_alert = _alert_probability_by_record_enumeration(
        read_count, threshold, false_positive_rate
    )
    distribution = {count: 0.0 for count in range(absent_coordinate_count + 1)}
    for alerts in product((False, True), repeat=absent_coordinate_count):
        false_discoveries = sum(alerts)
        probability = 1.0
        for alert in alerts:
            probability *= coordinate_alert if alert else 1.0 - coordinate_alert
        distribution[false_discoveries] += probability
    return distribution


def test_expected_false_discoveries_match_enumerated_distribution_under_independence():
    for absent_coordinate_count in range(0, 6):
        per = ThresholdEvidenceDesign(3, 2, 0.7, 0.05)
        budget = FalseDiscoveryBudget(absent_coordinate_count, per)
        distribution = _false_discovery_distribution(absent_coordinate_count, 3, 2, 0.05)
        expected = fsum(count * mass for count, mass in distribution.items())
        assert budget.expected_false_discoveries_upper_bound == pytest.approx(expected, abs=1e-12)


def test_markov_bound_dominates_enumerated_tail_probability():
    per = ThresholdEvidenceDesign(3, 2, 0.7, 0.05)
    budget = FalseDiscoveryBudget(5, per)
    distribution = _false_discovery_distribution(5, 3, 2, 0.05)
    for threshold in (1, 2, 3):
        tail = fsum(mass for count, mass in distribution.items() if count >= threshold)
        assert tail <= budget.probability_exceeding_false_discovery_budget_upper_bound(threshold) + 1e-12


def test_expected_fdp_bound_for_records_with_minimum_discoveries():
    per = ThresholdEvidenceDesign(5, 3, 0.7, 0.05)
    budget = FalseDiscoveryBudget(20, per)
    assert budget.expected_false_discovery_proportion_upper_bound(10) == pytest.approx(
        budget.expected_false_discoveries_upper_bound / 10
    )
