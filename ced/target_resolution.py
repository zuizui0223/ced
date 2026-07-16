"""Risk-limited target resolution for finite ecological experiments.

A stochastic experiment may return a record that resolves the requested target
correctly, resolves it incorrectly, or leaves a set-valued target report. This
module keeps those three outcomes separate and supports cost-aware selection among
declared experiments.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Hashable, Iterable

Target = Hashable
Record = Hashable


@dataclass(frozen=True)
class TargetRecordOutcome:
    record: Record
    probability: float
    compatible_targets: frozenset[Target]

    def __post_init__(self) -> None:
        if not isinstance(self.probability, (int, float)) or isinstance(self.probability, bool):
            raise ValueError("probability must be numeric")
        probability = float(self.probability)
        if not isfinite(probability) or not 0.0 <= probability <= 1.0:
            raise ValueError("probability must lie between zero and one")
        if not isinstance(self.compatible_targets, frozenset) or not self.compatible_targets:
            raise ValueError("compatible_targets must be a nonempty frozenset")
        object.__setattr__(self, "probability", probability)


@dataclass(frozen=True)
class RiskLimitedTargetResolution:
    """Declared record distribution for one true report target."""

    true_target: Target
    outcomes: tuple[TargetRecordOutcome, ...]

    def __post_init__(self) -> None:
        outcomes = tuple(self.outcomes)
        if not outcomes or not all(isinstance(outcome, TargetRecordOutcome) for outcome in outcomes):
            raise ValueError("outcomes must contain TargetRecordOutcome entries")
        if len({outcome.record for outcome in outcomes}) != len(outcomes):
            raise ValueError("records must be unique")
        if abs(sum(outcome.probability for outcome in outcomes) - 1.0) > 1e-12:
            raise ValueError("outcome probabilities must sum to one")
        object.__setattr__(self, "outcomes", outcomes)

    @property
    def correct_resolution_probability(self) -> float:
        return sum(
            outcome.probability
            for outcome in self.outcomes
            if outcome.compatible_targets == frozenset((self.true_target,))
        )

    @property
    def wrong_resolution_probability(self) -> float:
        return sum(
            outcome.probability
            for outcome in self.outcomes
            if len(outcome.compatible_targets) == 1
            and self.true_target not in outcome.compatible_targets
        )

    @property
    def ambiguity_probability(self) -> float:
        return sum(
            outcome.probability
            for outcome in self.outcomes
            if len(outcome.compatible_targets) > 1
        )

    @property
    def truth_excluded_probability(self) -> float:
        return sum(
            outcome.probability
            for outcome in self.outcomes
            if self.true_target not in outcome.compatible_targets
        )

    def meets(self, minimum_correct: float, maximum_wrong: float) -> bool:
        if not 0.0 <= minimum_correct <= 1.0 or not 0.0 <= maximum_wrong <= 1.0:
            raise ValueError("risk thresholds must lie between zero and one")
        return (
            self.correct_resolution_probability + 1e-12 >= minimum_correct
            and self.wrong_resolution_probability <= maximum_wrong + 1e-12
        )

    def verify(self) -> bool:
        total = (
            self.correct_resolution_probability
            + self.wrong_resolution_probability
            + self.ambiguity_probability
        )
        # Singleton reports containing the true target, singleton reports excluding
        # it, and multi-target reports partition the declared record outcomes.
        return abs(total - 1.0) <= 1e-12


@dataclass(frozen=True)
class CostedTargetResolutionDesign:
    name: str
    cost: float
    resolution: RiskLimitedTargetResolution

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("name must be a nonempty string")
        if not isinstance(self.cost, (int, float)) or isinstance(self.cost, bool):
            raise ValueError("cost must be numeric")
        cost = float(self.cost)
        if not isfinite(cost) or cost < 0.0:
            raise ValueError("cost must be finite and nonnegative")
        if not isinstance(self.resolution, RiskLimitedTargetResolution):
            raise ValueError("resolution must be RiskLimitedTargetResolution")
        object.__setattr__(self, "cost", cost)


def cheapest_feasible_target_resolution(
    designs: Iterable[CostedTargetResolutionDesign],
    minimum_correct: float,
    maximum_wrong: float,
) -> CostedTargetResolutionDesign | None:
    candidates = tuple(designs)
    if not candidates or not all(isinstance(design, CostedTargetResolutionDesign) for design in candidates):
        raise ValueError("designs must contain CostedTargetResolutionDesign entries")
    feasible = [
        design
        for design in candidates
        if design.resolution.meets(minimum_correct, maximum_wrong)
    ]
    return min(feasible, key=lambda design: (design.cost, design.name)) if feasible else None
