"""Expected false-discovery budgets for threshold evidence panels.

Familywise control bounds the chance of at least one false alert. Sometimes the
mathematically cleaner object is the expected number of false discoveries, plus a
Markov bound on exceeding a declared false-discovery budget. These bounds require
only coordinate-wise false-alert probabilities; they do not require independence
across absent coordinates.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from .threshold_detection import ThresholdEvidenceDesign


def _positive_int(name: str, value: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _nonnegative_int(name: str, value: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
    return value


def _positive_number(name: str, value: float) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{name} must be a finite positive number")
    number = float(value)
    if not isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be a finite positive number")
    return number


@dataclass(frozen=True)
class FalseDiscoveryBudget:
    """Expected false-discovery bound for a threshold panel.

    ``absent_coordinate_count`` is the number of truly absent coordinates among
    the screened coordinate set. The design does not infer this number from the
    record; it is a theorem parameter for worst-case or scenario analysis.
    """

    absent_coordinate_count: int
    per_coordinate: ThresholdEvidenceDesign

    def __post_init__(self) -> None:
        _nonnegative_int("absent_coordinate_count", self.absent_coordinate_count)
        if not isinstance(self.per_coordinate, ThresholdEvidenceDesign):
            raise ValueError("per_coordinate must be a ThresholdEvidenceDesign")

    @property
    def per_absent_false_alert_upper_bound(self) -> float:
        return self.per_coordinate.false_alert_probability_upper_bound

    @property
    def expected_false_discoveries_upper_bound(self) -> float:
        """E[V] upper bound for V false alerts among absent coordinates."""
        return self.absent_coordinate_count * self.per_absent_false_alert_upper_bound

    def probability_exceeding_false_discovery_budget_upper_bound(
        self, false_discovery_budget: float
    ) -> float:
        """Markov bound P[V >= budget] <= E[V] / budget."""
        budget = _positive_number("false_discovery_budget", false_discovery_budget)
        return min(1.0, self.expected_false_discoveries_upper_bound / budget)

    def expected_false_discovery_proportion_upper_bound(
        self, minimum_discoveries: int
    ) -> float:
        """Bound E[V/R | R >= minimum] by E[V] / minimum.

        This is not an FDR theorem. It is a conditional-design bound that applies
        only when the accepted record is known to contain at least
        ``minimum_discoveries`` total discoveries.
        """
        minimum = _positive_int("minimum_discoveries", minimum_discoveries)
        return min(1.0, self.expected_false_discoveries_upper_bound / minimum)

    @classmethod
    def worst_case_over_screened_coordinates(
        cls, screened_coordinate_count: int, per_coordinate: ThresholdEvidenceDesign
    ) -> "FalseDiscoveryBudget":
        """Worst case in which every screened coordinate is absent."""
        return cls(_positive_int("screened_coordinate_count", screened_coordinate_count), per_coordinate)

    def verify(self) -> bool:
        return (
            0.0 <= self.per_absent_false_alert_upper_bound <= 1.0
            and 0.0 <= self.expected_false_discoveries_upper_bound
            <= self.absent_coordinate_count
            and 0.0
            <= self.probability_exceeding_false_discovery_budget_upper_bound(1.0)
            <= 1.0
        )
