"""Calibration-derived bounds for imperfect detection contracts.

Earlier CED detection layers treat sensitivity and false-positive bounds as
externally declared constants. This module gives a finite calibration layer that
turns known blank-control and known present-control reads into conservative
one-sided binomial bounds. The resulting bounds can be fed into the threshold and
multiple-testing evidence designs without pretending that the error rates are
known exactly.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isfinite

from .threshold_detection import ThresholdEvidenceDesign, binomial_probability
from .multiple_testing import MultipleThresholdEvidenceDesign


def _positive_int(name: str, value: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _count(name: str, value: int, total: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= total:
        raise ValueError(f"{name} must be an integer in [0, total]")
    return value


def _open_unit_interval(name: str, value: float) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{name} must be a finite probability")
    probability = float(value)
    if not isfinite(probability) or not 0.0 < probability < 1.0:
        raise ValueError(f"{name} must lie strictly between zero and one")
    return probability


def binomial_cdf(trials: int, positives: int, probability: float) -> float:
    """P[X <= positives] for X ~ Binomial(trials, probability)."""
    trials = _positive_int("trials", trials)
    positives = _count("positives", positives, trials)
    return fsum(binomial_probability(trials, k, probability) for k in range(positives + 1))


def binomial_survival(trials: int, positives: int, probability: float) -> float:
    """P[X >= positives] for X ~ Binomial(trials, probability)."""
    trials = _positive_int("trials", trials)
    positives = _count("positives", positives, trials)
    return fsum(binomial_probability(trials, k, probability) for k in range(positives, trials + 1))


def false_positive_upper_confidence_bound(
    blank_read_count: int, blank_positive_count: int, delta: float
) -> float:
    """One-sided Clopper-Pearson upper bound for false-positive probability.

    The returned value ``u`` is the solution of
    ``P_u[X <= blank_positive_count] = delta`` when the observed count is not the
    maximum possible count; observing all positives returns the vacuous upper
    bound one.
    """
    blank_read_count = _positive_int("blank_read_count", blank_read_count)
    blank_positive_count = _count(
        "blank_positive_count", blank_positive_count, blank_read_count
    )
    delta = _open_unit_interval("delta", delta)
    if blank_positive_count == blank_read_count:
        return 1.0
    lower, upper = 0.0, 1.0
    for _ in range(100):
        middle = (lower + upper) / 2.0
        if binomial_cdf(blank_read_count, blank_positive_count, middle) >= delta:
            lower = middle
        else:
            upper = middle
    return (lower + upper) / 2.0


def sensitivity_lower_confidence_bound(
    present_read_count: int, present_positive_count: int, delta: float
) -> float:
    """One-sided Clopper-Pearson lower bound for sensitivity.

    The returned value ``l`` is the solution of
    ``P_l[X >= present_positive_count] = delta`` when at least one positive is
    observed; observing zero positives returns the vacuous lower bound zero.
    """
    present_read_count = _positive_int("present_read_count", present_read_count)
    present_positive_count = _count(
        "present_positive_count", present_positive_count, present_read_count
    )
    delta = _open_unit_interval("delta", delta)
    if present_positive_count == 0:
        return 0.0
    lower, upper = 0.0, 1.0
    for _ in range(100):
        middle = (lower + upper) / 2.0
        if binomial_survival(present_read_count, present_positive_count, middle) >= delta:
            upper = middle
        else:
            lower = middle
    return (lower + upper) / 2.0


@dataclass(frozen=True)
class CalibrationBounds:
    """Conservative error bounds from known blank and present controls."""

    blank_read_count: int
    blank_positive_count: int
    present_read_count: int
    present_positive_count: int
    delta: float = 0.05

    def __post_init__(self) -> None:
        _positive_int("blank_read_count", self.blank_read_count)
        _positive_int("present_read_count", self.present_read_count)
        _count("blank_positive_count", self.blank_positive_count, self.blank_read_count)
        _count("present_positive_count", self.present_positive_count, self.present_read_count)
        _open_unit_interval("delta", self.delta)

    @property
    def false_positive_upper_bound(self) -> float:
        return false_positive_upper_confidence_bound(
            self.blank_read_count, self.blank_positive_count, self.delta
        )

    @property
    def sensitivity_lower_bound(self) -> float:
        return sensitivity_lower_confidence_bound(
            self.present_read_count, self.present_positive_count, self.delta
        )

    @property
    def bounds_are_separated(self) -> bool:
        return self.false_positive_upper_bound < self.sensitivity_lower_bound

    @property
    def confidence_level_per_bound(self) -> float:
        return 1.0 - self.delta

    @property
    def joint_confidence_lower_bound(self) -> float:
        """Bonferroni lower bound that both one-sided bounds hold simultaneously."""
        return max(0.0, 1.0 - 2.0 * self.delta)

    def as_threshold_design(self, read_count: int, positive_threshold: int) -> ThresholdEvidenceDesign:
        """Use calibration bounds as a conservative threshold-design contract."""
        return ThresholdEvidenceDesign(
            read_count=read_count,
            positive_threshold=positive_threshold,
            sensitivity_lower_bound=self.sensitivity_lower_bound,
            false_positive_upper_bound=self.false_positive_upper_bound,
        )

    def as_multiple_threshold_design(
        self, coordinate_count: int, read_count: int, positive_threshold: int
    ) -> MultipleThresholdEvidenceDesign:
        """Use calibration bounds in a multiple-coordinate familywise design."""
        return MultipleThresholdEvidenceDesign(
            coordinate_count=coordinate_count,
            per_coordinate=self.as_threshold_design(read_count, positive_threshold),
        )

    def verify(self) -> bool:
        return (
            0.0 <= self.false_positive_upper_bound <= 1.0
            and 0.0 <= self.sensitivity_lower_bound <= 1.0
            and self.joint_confidence_lower_bound <= self.confidence_level_per_bound
            and self.bounds_are_separated
        )
