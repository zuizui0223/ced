"""Multiple-coordinate threshold evidence under bounded false positives.

The single-coordinate threshold event controls evidence for one declared target.
When many targets are screened simultaneously, the probability of at least one
false alert grows with the number of absent coordinates. This module keeps that
multiplicity effect explicit through a Bonferroni familywise bound and, when
coordinate-level alert events are declared independent under absence, an exact
all-absent familywise formula.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable

from .threshold_detection import ThresholdEvidenceDesign


def _positive_int(name: str, value: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _open_unit_interval(name: str, value: float) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{name} must be a finite probability")
    probability = float(value)
    if not isfinite(probability) or not 0.0 < probability < 1.0:
        raise ValueError(f"{name} must lie strictly between zero and one")
    return probability


@dataclass(frozen=True)
class MultipleThresholdEvidenceDesign:
    """Identical threshold evidence design applied to multiple coordinates.

    The default familywise guarantee is a union-bound guarantee and therefore
    does not require independence among absent-coordinate alert events. The exact
    all-absent formula is provided separately and is valid only under a declared
    cross-coordinate independence contract.
    """

    coordinate_count: int
    per_coordinate: ThresholdEvidenceDesign

    def __post_init__(self) -> None:
        _positive_int("coordinate_count", self.coordinate_count)
        if not isinstance(self.per_coordinate, ThresholdEvidenceDesign):
            raise ValueError("per_coordinate must be a ThresholdEvidenceDesign")

    @property
    def per_coordinate_false_alert_upper_bound(self) -> float:
        return self.per_coordinate.false_alert_probability_upper_bound

    @property
    def per_coordinate_detection_probability_lower_bound(self) -> float:
        return self.per_coordinate.detection_probability_lower_bound

    @property
    def expected_false_alerts_upper_bound(self) -> float:
        """Upper bound on expected false alerts when all coordinates are absent."""
        return self.coordinate_count * self.per_coordinate_false_alert_upper_bound

    @property
    def familywise_false_alert_upper_bound(self) -> float:
        """Union-bound probability of at least one false alert."""
        return min(1.0, self.expected_false_alerts_upper_bound)

    @property
    def exact_independent_all_absent_familywise_false_alert(self) -> float:
        """Exact all-absent familywise false-alert probability under independence."""
        alpha = self.per_coordinate_false_alert_upper_bound
        return 1.0 - (1.0 - alpha) ** self.coordinate_count

    @property
    def all_present_joint_detection_lower_bound(self) -> float:
        """Joint detection lower bound if all coordinates are present and independent."""
        return self.per_coordinate_detection_probability_lower_bound ** self.coordinate_count

    @property
    def per_coordinate_evidence_ratio_lower_bound(self) -> float:
        return self.per_coordinate.evidence_ratio_lower_bound

    def accepted_coordinates(self, positive_counts: Iterable[int]) -> frozenset[int]:
        """Coordinates whose positive counts cross the shared threshold."""
        counts = tuple(positive_counts)
        if len(counts) != self.coordinate_count:
            raise ValueError("positive_counts must provide one value per coordinate")
        accepted: set[int] = set()
        for index, count in enumerate(counts):
            if self.per_coordinate.accepts(count):
                accepted.add(index)
        return frozenset(accepted)

    @classmethod
    def minimum_threshold_for_familywise_false_alert(
        cls,
        coordinate_count: int,
        read_count: int,
        sensitivity_lower_bound: float,
        false_positive_upper_bound: float,
        familywise_alpha: float,
    ) -> int:
        """Smallest threshold whose Bonferroni familywise bound is below alpha."""
        coordinate_count = _positive_int("coordinate_count", coordinate_count)
        familywise_alpha = _open_unit_interval("familywise_alpha", familywise_alpha)
        for threshold in range(1, _positive_int("read_count", read_count) + 1):
            design = ThresholdEvidenceDesign(
                read_count,
                threshold,
                sensitivity_lower_bound,
                false_positive_upper_bound,
            )
            if coordinate_count * design.false_alert_probability_upper_bound <= familywise_alpha:
                return threshold
        raise ValueError("no threshold satisfies the requested familywise false-alert bound")

    @classmethod
    def minimum_threshold_for_familywise_and_evidence_ratio(
        cls,
        coordinate_count: int,
        read_count: int,
        sensitivity_lower_bound: float,
        false_positive_upper_bound: float,
        familywise_alpha: float,
        target_evidence_ratio: float,
    ) -> int:
        """Smallest threshold satisfying both familywise and per-coordinate evidence."""
        coordinate_count = _positive_int("coordinate_count", coordinate_count)
        familywise_alpha = _open_unit_interval("familywise_alpha", familywise_alpha)
        if not isinstance(target_evidence_ratio, (int, float)) or isinstance(
            target_evidence_ratio, bool
        ):
            raise ValueError("target_evidence_ratio must be finite and positive")
        target = float(target_evidence_ratio)
        if not isfinite(target) or target <= 0.0:
            raise ValueError("target_evidence_ratio must be finite and positive")
        for threshold in range(1, _positive_int("read_count", read_count) + 1):
            design = ThresholdEvidenceDesign(
                read_count,
                threshold,
                sensitivity_lower_bound,
                false_positive_upper_bound,
            )
            if (
                coordinate_count * design.false_alert_probability_upper_bound
                <= familywise_alpha
                and design.evidence_ratio_lower_bound >= target
            ):
                return threshold
        raise ValueError("no threshold satisfies both requested bounds")

    def verify(self) -> bool:
        return (
            0.0 <= self.per_coordinate_false_alert_upper_bound <= 1.0
            and 0.0 <= self.familywise_false_alert_upper_bound <= 1.0
            and 0.0 <= self.exact_independent_all_absent_familywise_false_alert <= 1.0
            and self.exact_independent_all_absent_familywise_false_alert
            <= self.familywise_false_alert_upper_bound
        )
