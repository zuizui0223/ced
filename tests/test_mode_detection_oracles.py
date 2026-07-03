"""Direct finite-outcome checks for common-mode imperfect detection."""

from __future__ import annotations

from itertools import product
from math import fsum

import pytest

from ced.detection import OneSidedDetector
from ced.mode_detection import ModeDiverseDetectionPanel


def _mode_outcomes(
    coordinate_count: int, repetitions: int, availability: float, sensitivity: float
):
    """Each outcome is a failed mode or all binary attempts in an operating mode."""
    yield None, 1.0 - availability
    for reads in product((False, True), repeat=coordinate_count * repetitions):
        positive_count = sum(reads)
        probability = availability * sensitivity**positive_count * (1.0 - sensitivity) ** (
            len(reads) - positive_count
        )
        yield reads, probability


def _joint_detection_by_enumeration(
    coordinate_count: int,
    mode_count: int,
    repetitions: int,
    availability: float,
    sensitivity: float,
) -> float:
    outcomes = tuple(
        _mode_outcomes(coordinate_count, repetitions, availability, sensitivity)
    )
    probabilities: list[float] = []
    for mode_results in product(outcomes, repeat=mode_count):
        probability = 1.0
        detected = [False] * coordinate_count
        for reads, mode_probability in mode_results:
            probability *= mode_probability
            if reads is None:
                continue
            for coordinate in range(coordinate_count):
                start = coordinate * repetitions
                if any(reads[start : start + repetitions]):
                    detected[coordinate] = True
        if all(detected):
            probabilities.append(probability)
    return fsum(probabilities)


def test_joint_detection_formula_matches_direct_mode_outcome_enumeration():
    for availability in (0.5, 0.8):
        for sensitivity in (0.25, 0.6):
            for coordinate_count in range(1, 4):
                for mode_count in range(1, 3):
                    for repetitions in range(0, 3):
                        panel = ModeDiverseDetectionPanel(
                            coordinate_count,
                            mode_count,
                            repetitions,
                            availability,
                            OneSidedDetector(sensitivity),
                        )
                        enumerated = _joint_detection_by_enumeration(
                            coordinate_count,
                            mode_count,
                            repetitions,
                            availability,
                            sensitivity,
                        )
                        assert panel.joint_detection_lower_bound == pytest.approx(
                            enumerated, abs=1e-12
                        )


def test_availability_ceiling_is_an_upper_bound_over_increasing_within_mode_repeats():
    detector = OneSidedDetector(0.6)
    for mode_count in range(1, 5):
        panel = ModeDiverseDetectionPanel(3, mode_count, 1, 0.8, detector)
        values = [
            ModeDiverseDetectionPanel(3, mode_count, repetitions, 0.8, detector).joint_detection_lower_bound
            for repetitions in range(1, 15)
        ]
        assert values == sorted(values)
        assert all(value <= panel.availability_ceiling for value in values)
        assert values[-1] < panel.availability_ceiling


def test_mode_floor_is_necessary_but_not_sufficient_for_finite_sensitivity():
    detector = OneSidedDetector(0.6)
    floor = ModeDiverseDetectionPanel.minimum_mode_count_for_availability_ceiling(0.8, 0.95)
    assert floor == 2
    with_one_repeat = ModeDiverseDetectionPanel(3, floor, 1, 0.8, detector)
    assert with_one_repeat.availability_ceiling >= 0.95
    assert with_one_repeat.joint_detection_lower_bound < 0.95
