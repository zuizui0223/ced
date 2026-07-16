"""Adaptive decision trees for ecological target resolution.

A policy may stop with a deterministic or set-valued report, or choose another
experiment after observing a record. The tree keeps expected cost and terminal
correct/wrong/ambiguous probabilities explicit.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Hashable, Iterable

Target = Hashable
Record = Hashable


@dataclass(frozen=True)
class TerminalTargetReport:
    compatible_targets: frozenset[Target]

    def __post_init__(self) -> None:
        if not isinstance(self.compatible_targets, frozenset) or not self.compatible_targets:
            raise ValueError("compatible_targets must be a nonempty frozenset")


@dataclass(frozen=True)
class AdaptiveTargetBranch:
    record: Record
    probability: float
    child: "AdaptiveTargetPolicy"

    def __post_init__(self) -> None:
        if not isinstance(self.probability, (int, float)) or isinstance(self.probability, bool):
            raise ValueError("branch probability must be numeric")
        probability = float(self.probability)
        if not isfinite(probability) or not 0.0 <= probability <= 1.0:
            raise ValueError("branch probability must lie between zero and one")
        if not isinstance(self.child, AdaptiveTargetPolicy):
            raise ValueError("child must be an AdaptiveTargetPolicy")
        object.__setattr__(self, "probability", probability)


@dataclass(frozen=True)
class AdaptiveTargetPolicy:
    """One terminal report or one adaptive experiment node."""

    name: str
    terminal_report: TerminalTargetReport | None = None
    experiment_cost: float = 0.0
    branches: tuple[AdaptiveTargetBranch, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("name must be a nonempty string")
        if not isinstance(self.experiment_cost, (int, float)) or isinstance(self.experiment_cost, bool):
            raise ValueError("experiment_cost must be numeric")
        cost = float(self.experiment_cost)
        if not isfinite(cost) or cost < 0.0:
            raise ValueError("experiment_cost must be finite and nonnegative")
        branches = tuple(self.branches)
        terminal = self.terminal_report is not None
        if terminal:
            if not isinstance(self.terminal_report, TerminalTargetReport):
                raise ValueError("terminal_report must be a TerminalTargetReport")
            if branches or cost != 0.0:
                raise ValueError("terminal policies cannot have branches or experiment cost")
        else:
            if not branches:
                raise ValueError("nonterminal policies require branches")
            if len({branch.record for branch in branches}) != len(branches):
                raise ValueError("branch records must be unique")
            if abs(sum(branch.probability for branch in branches) - 1.0) > 1e-12:
                raise ValueError("branch probabilities must sum to one")
        object.__setattr__(self, "experiment_cost", cost)
        object.__setattr__(self, "branches", branches)

    @classmethod
    def stop(cls, name: str, compatible_targets: Iterable[Target]) -> "AdaptiveTargetPolicy":
        return cls(name=name, terminal_report=TerminalTargetReport(frozenset(compatible_targets)))

    @property
    def is_terminal(self) -> bool:
        return self.terminal_report is not None

    @property
    def expected_total_cost(self) -> float:
        if self.is_terminal:
            return 0.0
        return self.experiment_cost + sum(
            branch.probability * branch.child.expected_total_cost for branch in self.branches
        )

    def terminal_distribution(self) -> tuple[tuple[frozenset[Target], float], ...]:
        totals: dict[frozenset[Target], float] = {}

        def visit(policy: AdaptiveTargetPolicy, weight: float) -> None:
            if policy.is_terminal:
                report = policy.terminal_report.compatible_targets
                totals[report] = totals.get(report, 0.0) + weight
                return
            for branch in policy.branches:
                visit(branch.child, weight * branch.probability)

        visit(self, 1.0)
        return tuple(sorted(totals.items(), key=lambda item: tuple(sorted(map(str, item[0])))))

    def correct_probability(self, true_target: Target) -> float:
        return sum(
            probability
            for targets, probability in self.terminal_distribution()
            if targets == frozenset((true_target,))
        )

    def wrong_probability(self, true_target: Target) -> float:
        return sum(
            probability
            for targets, probability in self.terminal_distribution()
            if len(targets) == 1 and true_target not in targets
        )

    def ambiguity_probability(self, true_target: Target) -> float:
        return sum(
            probability
            for targets, probability in self.terminal_distribution()
            if len(targets) > 1
        )

    def meets(self, true_target: Target, minimum_correct: float, maximum_wrong: float, maximum_expected_cost: float) -> bool:
        if not 0.0 <= minimum_correct <= 1.0 or not 0.0 <= maximum_wrong <= 1.0:
            raise ValueError("probability thresholds must lie between zero and one")
        if maximum_expected_cost < 0.0:
            raise ValueError("maximum_expected_cost must be nonnegative")
        return (
            self.correct_probability(true_target) + 1e-12 >= minimum_correct
            and self.wrong_probability(true_target) <= maximum_wrong + 1e-12
            and self.expected_total_cost <= maximum_expected_cost + 1e-12
        )

    def verify(self, true_target: Target) -> bool:
        total = (
            self.correct_probability(true_target)
            + self.wrong_probability(true_target)
            + self.ambiguity_probability(true_target)
        )
        return abs(total - 1.0) <= 1e-12 and self.expected_total_cost >= 0.0


def cheapest_feasible_policy(
    policies: Iterable[AdaptiveTargetPolicy],
    true_target: Target,
    minimum_correct: float,
    maximum_wrong: float,
    maximum_expected_cost: float,
) -> AdaptiveTargetPolicy | None:
    candidates = tuple(policies)
    if not candidates or not all(isinstance(policy, AdaptiveTargetPolicy) for policy in candidates):
        raise ValueError("policies must contain AdaptiveTargetPolicy entries")
    feasible = [
        policy
        for policy in candidates
        if policy.meets(true_target, minimum_correct, maximum_wrong, maximum_expected_cost)
    ]
    return min(feasible, key=lambda policy: (policy.expected_total_cost, policy.name)) if feasible else None
