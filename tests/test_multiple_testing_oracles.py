"""Independent finite-outcome checks for multiple-coordinate threshold evidence."""

from __future__ import annotations

from itertools import product
from math import fsum

import pytest

from ced.multiple_testing import MultipleThresholdEvidenceDesign
from ced.threshold_detection import ThresholdEvidenceDesign


def _coordinate_tail_by_enumeration(read_count: int, threshold: int, probability: float) -> float:
    masses: list[float] = []
    for record in product((False, True), repeat=read_count):
        positives = sum(record)
        if positives >= threshold:
            masses.append(
                probability**positives * (1.0 - probability) ** (read_count - positives)
            )
    return fsum(masses)


def _familywise_false_alert_by_enumeration(
    coordinate_count: int, read_count: int, threshold: int, false_positive_rate: float
) -> float:
    coordinate_outcomes = tuple(product((False, True), repeat=read_count))
    total = 0.0
    for coordinate_records in product(coordinate_outcomes, repeat=coordinate_count):
        probability = 1.0
        any_alert = False
        for record in coordinate_records:
            positives = sum(record)
            probability *= false_positive_rate**positives * (1.0 - false_positive_rate) ** (
                read_count - positives
            )
            if positives >= threshold:
                any_alert = True
        if any_alert:
            total += probability
    return total


def test_exact_independent_familywise_formula_matches_full_outcome_enumeration():
    for coordinate_count in range(1, 4):
        for read_count in range(1, 4):
            for threshold in range(1, read_count + 1):
                per = ThresholdEvidenceDesign(read_count, threshold, 0.7, 0.05)
                design = MultipleThresholdEvidenceDesign(coordinate_count, per)
                enumerated = _familywise_false_alert_by_enumeration(
                    coordinate_count, read_count, threshold, 0.05
                )
                assert design.exact_independent_all_absent_familywise_false_alert == pytest.approx(
                    enumerated, abs=1e-12
                )


def test_bonferroni_bound_dominates_exact_independent_familywise_risk():
    for coordinate_count in range(1, 10):
        per = ThresholdEvidenceDesign(5, 3, 0.7, 0.05)
        design = MultipleThresholdEvidenceDesign(coordinate_count, per)
        exact = design.exact_independent_all_absent_familywise_false_alert
        assert exact <= design.familywise_false_alert_upper_bound
        assert design.familywise_false_alert_upper_bound <= design.expected_false_alerts_upper_bound


def test_familywise_threshold_search_matches_direct_scan():
    for coordinate_count in (1, 5, 20):
        feasible = [
            threshold
            for threshold in range(1, 6)
            if MultipleThresholdEvidenceDesign(
                coordinate_count, ThresholdEvidenceDesign(5, threshold, 0.7, 0.05)
            ).familywise_false_alert_upper_bound
            <= 0.05
        ]
        if feasible:
            assert MultipleThresholdEvidenceDesign.minimum_threshold_for_familywise_false_alert(
                coordinate_count, 5, 0.7, 0.05, 0.05
            ) == min(feasible)
        else:
            with pytest.raises(ValueError):
                MultipleThresholdEvidenceDesign.minimum_threshold_for_familywise_false_alert(
                    coordinate_count, 5, 0.7, 0.05, 0.05
                )


def test_coordinate_tail_oracle_matches_per_coordinate_false_alert():
    per = ThresholdEvidenceDesign(5, 3, 0.7, 0.05)
    assert per.false_alert_probability_upper_bound == pytest.approx(
        _coordinate_tail_by_enumeration(5, 3, 0.05), abs=1e-12
    )
