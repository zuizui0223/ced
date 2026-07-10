"""Threshold evidence without independent resettable repeats.

The binomial threshold layer assumes conditionally independent resettable reads.
When repeated reads may be dependent or non-reset, the binomial tail is no longer
valid. This module keeps only marginal read bounds and derives the finite bounds
that still follow from expectation alone.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import inf, isfinite


def _positive_int(name: str, value: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _probability(name: str, value: float) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{name} must be a finite probability")
    probability = float(value)
    if not isfinite(probability) or not 0.0 <= probability <= 1.0:
        raise ValueError(f"{name} must lie between zero and one")
    return probability


@dataclass(frozen=True)
class DependentThresholdEvidenceDesign:
    """Threshold evidence using only marginal read-error contracts.

    The contract is deliberately weaker than the binomial threshold contract:
    reads need not be independent and need not be resettable. If the coordinate is
    absent, every read has positive probability at most ``false_positive_upper_bound``.
    If the coordinate is present, every read has positive probability at least
    ``sensitivity_lower_bound``.
    """

    read_count: int
    positive_threshold: int
    sensitivity_lower_bound: float
    false_positive_upper_bound: float

    def __post_init__(self) -> None:
        _positive_int("read_count", self.read_count)
        _positive_int("positive_threshold", self.positive_threshold)
        if self.positive_threshold > self.read_count:
            raise ValueError("positive_threshold cannot exceed read_count")
        sensitivity = _probability("sensitivity_lower_bound", self.sensitivity_lower_bound)
        false_positive = _probability(
            "false_positive_upper_bound", self.false_positive_upper_bound
        )
        if false_positive >= sensitivity:
            raise ValueError(
                "false_positive_upper_bound must be below sensitivity_lower_bound"
            )

    @property
    def expected_absent_positive_count_upper_bound(self) -> float:
        """Upper bound on E[X] when the coordinate is absent."""
        return self.read_count * self.false_positive_upper_bound

    @property
    def expected_present_positive_count_lower_bound(self) -> float:
        """Lower bound on E[X] when the coordinate is present."""
        return self.read_count * self.sensitivity_lower_bound

    @property
    def false_alert_probability_upper_bound(self) -> float:
        """Markov bound P[X >= t | absent] <= E[X]/t."""
        return min(
            1.0,
            self.expected_absent_positive_count_upper_bound / self.positive_threshold,
        )

    @property
    def detection_probability_lower_bound(self) -> float:
        """Worst-case P[X >= t | present] from E[X] >= n p.

        On the complement of the threshold event, X can be as large as t - 1.
        On the event, X can be as large as n. Therefore

            E[X] <= (t - 1) P[X < t] + n P[X >= t].

        Solving for P[X >= t] with E[X] >= n p gives the lower bound below.
        """
        numerator = self.expected_present_positive_count_lower_bound - (
            self.positive_threshold - 1
        )
        denominator = self.read_count - self.positive_threshold + 1
        return min(1.0, max(0.0, numerator / denominator))

    @property
    def evidence_ratio_lower_bound(self) -> float:
        """Posterior-free event ratio lower bound under the marginal contract."""
        absent = self.false_alert_probability_upper_bound
        present = self.detection_probability_lower_bound
        if absent == 0.0:
            return inf if present > 0.0 else 0.0
        return present / absent

    @property
    def threshold_crossing_certifies_presence(self) -> bool:
        """Threshold crossing is deductive only under zero false positives."""
        return self.false_positive_upper_bound == 0.0

    def accepts(self, positive_count: int) -> bool:
        if not isinstance(positive_count, int) or isinstance(positive_count, bool):
            raise ValueError("positive_count must be an integer")
        if not 0 <= positive_count <= self.read_count:
            raise ValueError("positive_count must lie in [0, read_count]")
        return positive_count >= self.positive_threshold

    def verify(self) -> bool:
        return (
            0.0 <= self.false_alert_probability_upper_bound <= 1.0
            and 0.0 <= self.detection_probability_lower_bound <= 1.0
            and 0.0 <= self.expected_absent_positive_count_upper_bound <= self.read_count
            and 0.0
            <= self.expected_present_positive_count_lower_bound
            <= self.read_count
        )
