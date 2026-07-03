"""Direct finite probability enumerations for the imperfect-detection extension."""

from __future__ import annotations

from itertools import product

import pytest

from ced.detection import OneSidedDetectionPanel, OneSidedDetector


def _record_probability(record: tuple[bool, ...], sensitivity: float) -> float:
    positive_count = sum(record)
    return sensitivity**positive_count * (1.0 - sensitivity) ** (len(record) - positive_count)


def _enumerated_any_positive_probability(sensitivity: float, repetitions: int) -> float:
    return sum(
        _record_probability(record, sensitivity)
        for record in product((False, True), repeat=repetitions)
        if any(record)
    )


def _enumerated_joint_detection_probability(
    sensitivity: float, coordinate_count: int, repetitions: int
) -> float:
    total = 0.0
    for flat_record in product((False, True), repeat=coordinate_count * repetitions):
        rows = tuple(
            flat_record[index * repetitions : (index + 1) * repetitions]
            for index in range(coordinate_count)
        )
        if all(any(row) for row in rows):
            total += _record_probability(flat_record, sensitivity)
    return total


def test_single_coordinate_detection_formula_matches_all_binary_outcomes():
    for sensitivity in (0.25, 0.5, 0.75, 1.0):
        detector = OneSidedDetector(sensitivity)
        for repetitions in range(0, 7):
            enumerated = _enumerated_any_positive_probability(sensitivity, repetitions)
            assert detector.any_positive_probability_if_present(repetitions) == pytest.approx(
                enumerated
            )
            assert detector.all_negative_probability_if_present(repetitions) == pytest.approx(
                1.0 - enumerated
            )


def test_joint_detection_formula_matches_direct_outcome_enumeration():
    for sensitivity in (0.25, 0.5, 0.75):
        detector = OneSidedDetector(sensitivity)
        for coordinate_count in range(1, 4):
            for repetitions in range(0, 4):
                panel = OneSidedDetectionPanel(coordinate_count, repetitions, detector)
                enumerated = _enumerated_joint_detection_probability(
                    sensitivity, coordinate_count, repetitions
                )
                assert panel.joint_detection_lower_bound == pytest.approx(enumerated)


def test_minimal_repeat_helper_matches_direct_search_on_bounded_grid():
    for sensitivity in (0.2, 0.4, 0.6, 1.0):
        detector = OneSidedDetector(sensitivity)
        for coordinate_count in range(1, 5):
            for confidence in (0.1, 0.5, 0.8, 0.95):
                repeats = detector.repetitions_for_joint_detection_confidence(
                    coordinate_count, confidence
                )
                panel = OneSidedDetectionPanel(coordinate_count, repeats, detector)
                assert panel.joint_detection_lower_bound >= confidence
                previous = OneSidedDetectionPanel(
                    coordinate_count, repeats - 1, detector
                )
                assert previous.joint_detection_lower_bound < confidence


def test_negative_signature_is_never_an_absence_certificate_when_sensitivity_is_imperfect():
    for sensitivity in (0.1, 0.4, 0.9):
        detector = OneSidedDetector(sensitivity)
        for repetitions in range(1, 10):
            panel = OneSidedDetectionPanel(3, repetitions, detector)
            assert panel.positive_signature(((False,) * repetitions,) * 3) == frozenset()
            assert panel.all_negative_record_is_ambiguous
            assert detector.all_negative_probability_if_present(repetitions) > 0.0
