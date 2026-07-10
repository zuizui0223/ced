"""Independent finite-outcome checks for threshold evidence with false positives."""

from __future__ import annotations

from itertools import product
from math import fsum

import pytest

from ced.threshold_detection import ThresholdEvidenceDesign, binomial_tail


def _enumerated_tail(read_count: int, threshold: int, probability: float) -> float:
    masses: list[float] = []
    for record in product((False, True), repeat=read_count):
        positives = sum(record)
        if positives >= threshold:
            masses.append(
                probability**positives * (1.0 - probability) ** (read_count - positives)
            )
    return fsum(masses)


def test_binomial_tail_matches_all_binary_outcomes():
    for read_count in range(1, 8):
        for threshold in range(0, read_count + 1):
            for probability in (0.0, 0.05, 0.25, 0.7, 1.0):
                assert binomial_tail(read_count, threshold, probability) == pytest.approx(
                    _enumerated_tail(read_count, threshold, probability), abs=1e-12
                )


def test_threshold_design_bounds_match_direct_event_enumeration():
    for read_count in range(1, 7):
        for threshold in range(1, read_count + 1):
            design = ThresholdEvidenceDesign(read_count, threshold, 0.7, 0.05)
            assert design.detection_probability_lower_bound == pytest.approx(
                _enumerated_tail(read_count, threshold, 0.7), abs=1e-12
            )
            assert design.false_alert_probability_upper_bound == pytest.approx(
                _enumerated_tail(read_count, threshold, 0.05), abs=1e-12
            )
            if design.false_alert_probability_upper_bound > 0.0:
                assert design.evidence_ratio_lower_bound == pytest.approx(
                    design.detection_probability_lower_bound
                    / design.false_alert_probability_upper_bound,
                    abs=1e-12,
                )


def test_minimum_threshold_search_matches_direct_scan():
    for read_count in range(1, 8):
        for target_ratio in (2, 5, 10, 50):
            feasible = [
                threshold
                for threshold in range(1, read_count + 1)
                if ThresholdEvidenceDesign(
                    read_count, threshold, 0.7, 0.05
                ).evidence_ratio_lower_bound
                >= target_ratio
            ]
            if feasible:
                assert ThresholdEvidenceDesign.minimum_threshold_for_evidence_ratio(
                    read_count, 0.7, 0.05, target_ratio
                ) == min(feasible)
            else:
                with pytest.raises(ValueError):
                    ThresholdEvidenceDesign.minimum_threshold_for_evidence_ratio(
                        read_count, 0.7, 0.05, target_ratio
                    )


def test_threshold_crossing_is_not_a_deductive_certificate_when_false_positives_are_allowed():
    design = ThresholdEvidenceDesign(5, 3, 0.7, 0.05)
    assert design.accepts(5)
    assert design.false_alert_probability_upper_bound > 0.0
    assert not design.threshold_is_presence_certificate
