"""Heterogeneous coordinate-specific threshold evidence panels.

Earlier multiple-coordinate layers assume the same threshold design is reused for
every coordinate. This module allows each coordinate to have its own read count,
threshold, sensitivity bound, and false-positive bound. The resulting panel keeps
independence-free union and Frechet bounds separate from exact formulas that are
valid only under declared cross-coordinate independence.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import prod
from typing import Iterable

from .threshold_detection import ThresholdEvidenceDesign


def _as_threshold_tuple(
    per_coordinate: Iterable[ThresholdEvidenceDesign],
) -> tuple[ThresholdEvidenceDesign, ...]:
    designs = tuple(per_coordinate)
    if not designs:
        raise ValueError("per_coordinate must contain at least one design")
    if not all(isinstance(design, ThresholdEvidenceDesign) for design in designs):
        raise ValueError("every per-coordinate design must be a ThresholdEvidenceDesign")
    return designs


def _weights(weight_by_coordinate: Iterable[float], expected_length: int) -> tuple[float, ...]:
    weights = tuple(float(weight) for weight in weight_by_coordinate)
    if len(weights) != expected_length:
        raise ValueError("weight count must equal coordinate count")
    if any(weight < 0.0 for weight in weights):
        raise ValueError("weights must be nonnegative")
    return weights


@dataclass(frozen=True)
class HeterogeneousThresholdEvidencePanel:
    """Panel with coordinate-specific threshold evidence designs."""

    per_coordinate: tuple[ThresholdEvidenceDesign, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "per_coordinate", _as_threshold_tuple(self.per_coordinate))

    @property
    def coordinate_count(self) -> int:
        return len(self.per_coordinate)

    @property
    def per_coordinate_false_alert_upper_bounds(self) -> tuple[float, ...]:
        return tuple(
            design.false_alert_probability_upper_bound for design in self.per_coordinate
        )

    @property
    def per_coordinate_detection_lower_bounds(self) -> tuple[float, ...]:
        return tuple(
            design.detection_probability_lower_bound for design in self.per_coordinate
        )

    @property
    def per_coordinate_evidence_ratio_lower_bounds(self) -> tuple[float, ...]:
        return tuple(design.evidence_ratio_lower_bound for design in self.per_coordinate)

    @property
    def expected_false_alerts_upper_bound(self) -> float:
        """Upper bound on the expected number of false alerts if all are absent."""
        return sum(self.per_coordinate_false_alert_upper_bounds)

    @property
    def familywise_false_alert_upper_bound(self) -> float:
        """Union bound, valid without cross-coordinate independence."""
        return min(1.0, self.expected_false_alerts_upper_bound)

    @property
    def exact_independent_all_absent_familywise_false_alert(self) -> float:
        """Exact all-absent familywise risk under declared independence only."""
        return 1.0 - prod(
            1.0 - alpha for alpha in self.per_coordinate_false_alert_upper_bounds
        )

    @property
    def expected_missed_detections_upper_bound(self) -> float:
        """Upper bound on expected missed detections if all coordinates are present."""
        return sum(1.0 - beta for beta in self.per_coordinate_detection_lower_bounds)

    @property
    def all_present_joint_detection_lower_bound_no_independence(self) -> float:
        """Frechet/union lower bound on detecting every present coordinate."""
        return max(0.0, 1.0 - self.expected_missed_detections_upper_bound)

    @property
    def exact_independent_all_present_joint_detection_lower_bound(self) -> float:
        """Product lower bound under declared cross-coordinate independence only."""
        return prod(self.per_coordinate_detection_lower_bounds)

    def weighted_false_alert_budget_upper_bound(
        self, weight_by_coordinate: Iterable[float]
    ) -> float:
        """Expected weighted false-alert budget if all coordinates are absent."""
        weights = _weights(weight_by_coordinate, self.coordinate_count)
        return sum(
            weight * alpha
            for weight, alpha in zip(weights, self.per_coordinate_false_alert_upper_bounds)
        )

    def accepted_coordinates(self, positive_counts: Iterable[int]) -> tuple[int, ...]:
        """Return zero-based coordinates whose coordinate-specific threshold is met."""
        counts = tuple(positive_counts)
        if len(counts) != self.coordinate_count:
            raise ValueError("positive count length must equal coordinate count")
        accepted: list[int] = []
        for coordinate, (design, count) in enumerate(zip(self.per_coordinate, counts)):
            if not isinstance(count, int) or isinstance(count, bool):
                raise ValueError("positive counts must be integers")
            if not 0 <= count <= design.read_count:
                raise ValueError("positive counts must lie in each coordinate read range")
            if count >= design.positive_threshold:
                accepted.append(coordinate)
        return tuple(accepted)

    def coordinates_meeting_evidence_ratio(self, minimum_evidence_ratio: float) -> tuple[int, ...]:
        if minimum_evidence_ratio < 0.0:
            raise ValueError("minimum_evidence_ratio must be nonnegative")
        return tuple(
            coordinate
            for coordinate, ratio in enumerate(self.per_coordinate_evidence_ratio_lower_bounds)
            if ratio >= minimum_evidence_ratio
        )

    def verify(self) -> bool:
        alphas = self.per_coordinate_false_alert_upper_bounds
        betas = self.per_coordinate_detection_lower_bounds
        return (
            all(0.0 <= alpha <= 1.0 for alpha in alphas)
            and all(0.0 <= beta <= 1.0 for beta in betas)
            and 0.0 <= self.familywise_false_alert_upper_bound <= 1.0
            and 0.0 <= self.exact_independent_all_absent_familywise_false_alert <= 1.0
            and 0.0 <= self.all_present_joint_detection_lower_bound_no_independence <= 1.0
            and 0.0 <= self.exact_independent_all_present_joint_detection_lower_bound <= 1.0
            and self.exact_independent_all_absent_familywise_false_alert
            <= self.familywise_false_alert_upper_bound + 1e-12
            and self.all_present_joint_detection_lower_bound_no_independence
            <= self.exact_independent_all_present_joint_detection_lower_bound + 1e-12
        )
