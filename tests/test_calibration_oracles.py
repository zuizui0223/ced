"""Independent finite checks for calibration-derived error bounds."""

from __future__ import annotations

from math import fsum

import pytest

from ced.calibration import (
    false_positive_upper_confidence_bound,
    sensitivity_lower_confidence_bound,
)
from ced.threshold_detection import binomial_probability


def _false_positive_coverage_probability(
    trials: int, true_probability: float, delta: float
) -> float:
    """Probability that the upper bound covers the true false-positive rate."""
    masses = []
    for observed in range(trials + 1):
        upper = false_positive_upper_confidence_bound(trials, observed, delta)
        if true_probability <= upper + 1e-12:
            masses.append(binomial_probability(trials, observed, true_probability))
    return fsum(masses)


def _sensitivity_coverage_probability(
    trials: int, true_probability: float, delta: float
) -> float:
    """Probability that the lower bound covers the true sensitivity."""
    masses = []
    for observed in range(trials + 1):
        lower = sensitivity_lower_confidence_bound(trials, observed, delta)
        if true_probability + 1e-12 >= lower:
            masses.append(binomial_probability(trials, observed, true_probability))
    return fsum(masses)


def test_false_positive_upper_bound_has_declared_grid_coverage():
    for trials in range(1, 8):
        for true_probability in (0.01, 0.05, 0.2, 0.6, 0.95):
            coverage = _false_positive_coverage_probability(trials, true_probability, 0.1)
            assert coverage >= 0.9 - 1e-12


def test_sensitivity_lower_bound_has_declared_grid_coverage():
    for trials in range(1, 8):
        for true_probability in (0.05, 0.2, 0.6, 0.9, 0.99):
            coverage = _sensitivity_coverage_probability(trials, true_probability, 0.1)
            assert coverage >= 0.9 - 1e-12


def test_bounds_are_monotone_in_observed_counts():
    false_positive_bounds = [
        false_positive_upper_confidence_bound(10, observed, 0.05)
        for observed in range(11)
    ]
    sensitivity_bounds = [
        sensitivity_lower_confidence_bound(10, observed, 0.05)
        for observed in range(11)
    ]
    assert false_positive_bounds == sorted(false_positive_bounds)
    assert sensitivity_bounds == sorted(sensitivity_bounds)
