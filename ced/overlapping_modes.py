"""Detection with partially shared and overlapping failure modes.

Independent modes and one common-mode failure are two endpoints. This module
models the intermediate case with independent latent failure factors. Each mode
is disabled when any factor assigned to that mode fails, so modes may share some
but not all failure causes.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import isfinite


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
class OverlappingFailureModePanel:
    """Exact finite detection model with overlapping latent failure factors.

    ``factor_failure_probabilities[j]`` is the failure probability of latent factor
    ``j``. Factors are independent. ``mode_factor_sets[m]`` lists the factors that
    can disable mode ``m``; a mode operates iff none of its listed factors fail.

    Conditional on the operating-mode set, reads are independent across modes,
    repeats, and coordinates with sensitivity at least ``sensitivity_lower_bound``.
    """

    coordinate_count: int
    repetitions_per_coordinate_per_mode: int
    sensitivity_lower_bound: float
    factor_failure_probabilities: tuple[float, ...]
    mode_factor_sets: tuple[frozenset[int], ...]

    def __post_init__(self) -> None:
        _positive_int("coordinate_count", self.coordinate_count)
        _positive_int(
            "repetitions_per_coordinate_per_mode",
            self.repetitions_per_coordinate_per_mode,
        )
        object.__setattr__(
            self,
            "sensitivity_lower_bound",
            _probability("sensitivity_lower_bound", self.sensitivity_lower_bound),
        )
        factor_probabilities = tuple(
            _probability("factor_failure_probability", probability)
            for probability in self.factor_failure_probabilities
        )
        if not factor_probabilities:
            raise ValueError("at least one failure factor is required")
        object.__setattr__(self, "factor_failure_probabilities", factor_probabilities)

        mode_sets = tuple(frozenset(mode) for mode in self.mode_factor_sets)
        if not mode_sets:
            raise ValueError("at least one mode is required")
        factor_count = len(factor_probabilities)
        if any(not mode for mode in mode_sets):
            raise ValueError("every mode must declare at least one failure factor")
        if any(
            not isinstance(factor, int)
            or isinstance(factor, bool)
            or factor < 0
            or factor >= factor_count
            for mode in mode_sets
            for factor in mode
        ):
            raise ValueError("mode factor index is outside factor range")
        object.__setattr__(self, "mode_factor_sets", mode_sets)

    @property
    def factor_count(self) -> int:
        return len(self.factor_failure_probabilities)

    @property
    def mode_count(self) -> int:
        return len(self.mode_factor_sets)

    @property
    def within_mode_coordinate_miss_probability_upper_bound(self) -> float:
        return (1.0 - self.sensitivity_lower_bound) ** self.repetitions_per_coordinate_per_mode

    def operating_modes(self, failed_factors: frozenset[int]) -> tuple[int, ...]:
        return tuple(
            mode_index
            for mode_index, factors in enumerate(self.mode_factor_sets)
            if factors.isdisjoint(failed_factors)
        )

    def factor_state_probability(self, failed_factors: frozenset[int]) -> float:
        probability = 1.0
        for factor, failure_probability in enumerate(self.factor_failure_probabilities):
            probability *= (
                failure_probability
                if factor in failed_factors
                else 1.0 - failure_probability
            )
        return probability

    def factor_states(self) -> tuple[frozenset[int], ...]:
        return tuple(
            frozenset(index for index, failed in enumerate(bits) if failed)
            for bits in product((False, True), repeat=self.factor_count)
        )

    @property
    def all_modes_failed_probability(self) -> float:
        return sum(
            self.factor_state_probability(state)
            for state in self.factor_states()
            if not self.operating_modes(state)
        )

    @property
    def at_least_one_mode_operates_probability(self) -> float:
        return 1.0 - self.all_modes_failed_probability

    @property
    def availability_ceiling(self) -> float:
        """Upper ceiling for detecting even one present coordinate."""
        return self.at_least_one_mode_operates_probability

    @property
    def joint_detection_probability_lower_bound(self) -> float:
        """Exact finite lower bound after averaging over overlapping factor states."""
        q = self.within_mode_coordinate_miss_probability_upper_bound
        total = 0.0
        for state in self.factor_states():
            active_mode_count = len(self.operating_modes(state))
            conditional_joint_detection = (
                0.0
                if active_mode_count == 0
                else (1.0 - q**active_mode_count) ** self.coordinate_count
            )
            total += self.factor_state_probability(state) * conditional_joint_detection
        return total

    @property
    def total_read_count(self) -> int:
        return (
            self.coordinate_count
            * self.mode_count
            * self.repetitions_per_coordinate_per_mode
        )

    @property
    def shared_factor_count(self) -> int:
        usage = [0 for _ in range(self.factor_count)]
        for mode in self.mode_factor_sets:
            for factor in mode:
                usage[factor] += 1
        return sum(count > 1 for count in usage)

    @property
    def pairwise_mode_overlap_counts(self) -> tuple[tuple[int, ...], ...]:
        return tuple(
            tuple(len(left & right) for right in self.mode_factor_sets)
            for left in self.mode_factor_sets
        )

    def verify(self) -> bool:
        state_mass = sum(
            self.factor_state_probability(state) for state in self.factor_states()
        )
        return (
            abs(state_mass - 1.0) <= 1e-12
            and 0.0 <= self.all_modes_failed_probability <= 1.0
            and 0.0 <= self.availability_ceiling <= 1.0
            and 0.0 <= self.joint_detection_probability_lower_bound <= self.availability_ceiling + 1e-12
            and self.total_read_count
            == self.coordinate_count
            * self.mode_count
            * self.repetitions_per_coordinate_per_mode
        )
