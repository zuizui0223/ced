"""Adaptive false-alert risk accounting by alpha spending.

Fixed panels predeclare every read and threshold. Adaptive monitoring chooses the
next coordinate, mode, or test after seeing earlier outcomes. This module records
what remains valid in that setting: if each adaptively selected stage has a
conditional false-alert bound and the policy keeps an alpha-spending ledger, then
familywise false-alert risk is controlled by the spent alpha budget.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable


def _nonnegative_int(name: str, value: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
    return value


def _positive_int(name: str, value: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _alpha(value: float) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError("alpha must be a finite probability")
    alpha = float(value)
    if not isfinite(alpha) or not 0.0 <= alpha <= 1.0:
        raise ValueError("alpha must lie between zero and one")
    return alpha


def _weights(weight_by_coordinate: Iterable[float], expected_length: int) -> tuple[float, ...]:
    weights = tuple(float(weight) for weight in weight_by_coordinate)
    if len(weights) != expected_length:
        raise ValueError("weight count must equal coordinate count")
    if any((not isfinite(weight)) or weight < 0.0 for weight in weights):
        raise ValueError("weights must be finite and nonnegative")
    return weights


@dataclass(frozen=True)
class AdaptiveAlphaSpend:
    """One adaptively selectable false-alert spend.

    The stage may represent an additional read block, a coordinate-specific
    threshold, a mode-specific confirmation, or any other declared test whose
    conditional false-alert probability is bounded by ``alpha`` when the target
    coordinate is absent. ``mode`` and ``label`` are identifiers only; they do not
    create independence assumptions.
    """

    coordinate: int
    alpha: float
    mode: str = ""
    label: str = ""

    def __post_init__(self) -> None:
        _nonnegative_int("coordinate", self.coordinate)
        object.__setattr__(self, "alpha", _alpha(self.alpha))
        if not isinstance(self.mode, str):
            raise ValueError("mode must be a string")
        if not isinstance(self.label, str):
            raise ValueError("label must be a string")


@dataclass(frozen=True)
class AdaptiveAlphaSpendingLedger:
    """Ledger for adaptive false-alert risk spending.

    The ledger lists stages that an adaptive policy has spent or pre-authorized
    along a declared path. The familywise false-alert guarantee is purely an
    alpha-spending statement; it does not infer detection power or justify the
    adaptive rule that chose the stages.
    """

    coordinate_count: int
    spends: tuple[AdaptiveAlphaSpend, ...]

    def __post_init__(self) -> None:
        _positive_int("coordinate_count", self.coordinate_count)
        spends = tuple(self.spends)
        if not all(isinstance(spend, AdaptiveAlphaSpend) for spend in spends):
            raise ValueError("spends must contain only AdaptiveAlphaSpend entries")
        if any(spend.coordinate >= self.coordinate_count for spend in spends):
            raise ValueError("spend coordinate exceeds coordinate_count")
        object.__setattr__(self, "spends", spends)

    @classmethod
    def from_coordinate_alphas(
        cls, coordinate_count: int, coordinate_alphas: Iterable[tuple[int, float]]
    ) -> "AdaptiveAlphaSpendingLedger":
        return cls(
            coordinate_count,
            tuple(
                AdaptiveAlphaSpend(coordinate=coordinate, alpha=alpha)
                for coordinate, alpha in coordinate_alphas
            ),
        )

    @property
    def spend_count(self) -> int:
        return len(self.spends)

    @property
    def total_spent_alpha(self) -> float:
        return sum(spend.alpha for spend in self.spends)

    @property
    def familywise_false_alert_upper_bound(self) -> float:
        """Anytime union bound over adaptively spent stages."""
        return min(1.0, self.total_spent_alpha)

    @property
    def expected_false_alerts_upper_bound(self) -> float:
        """Expected number of false alerts if every coordinate is absent."""
        return self.total_spent_alpha

    @property
    def per_coordinate_spent_alpha(self) -> tuple[float, ...]:
        totals = [0.0 for _ in range(self.coordinate_count)]
        for spend in self.spends:
            totals[spend.coordinate] += spend.alpha
        return tuple(totals)

    @property
    def per_coordinate_false_alert_upper_bounds(self) -> tuple[float, ...]:
        return tuple(min(1.0, total) for total in self.per_coordinate_spent_alpha)

    @property
    def prefix_familywise_false_alert_upper_bounds(self) -> tuple[float, ...]:
        bounds: list[float] = []
        running = 0.0
        for spend in self.spends:
            running += spend.alpha
            bounds.append(min(1.0, running))
        return tuple(bounds)

    def stages_for_coordinate(self, coordinate: int) -> tuple[AdaptiveAlphaSpend, ...]:
        _nonnegative_int("coordinate", coordinate)
        if coordinate >= self.coordinate_count:
            raise ValueError("coordinate exceeds coordinate_count")
        return tuple(spend for spend in self.spends if spend.coordinate == coordinate)

    def remaining_alpha_budget(self, total_budget: float) -> float:
        budget = _alpha(total_budget)
        return max(0.0, budget - self.total_spent_alpha)

    def within_total_budget(self, total_budget: float) -> bool:
        budget = _alpha(total_budget)
        return self.total_spent_alpha <= budget + 1e-12

    def weighted_false_alert_budget_upper_bound(
        self, weight_by_coordinate: Iterable[float]
    ) -> float:
        weights = _weights(weight_by_coordinate, self.coordinate_count)
        return sum(
            weight * alpha
            for weight, alpha in zip(weights, self.per_coordinate_spent_alpha)
        )

    def append(
        self, coordinate: int, alpha: float, mode: str = "", label: str = ""
    ) -> "AdaptiveAlphaSpendingLedger":
        return AdaptiveAlphaSpendingLedger(
            self.coordinate_count,
            self.spends + (AdaptiveAlphaSpend(coordinate, alpha, mode, label),),
        )

    def verify(self) -> bool:
        return (
            self.spend_count == len(self.spends)
            and all(0.0 <= spend.alpha <= 1.0 for spend in self.spends)
            and all(0.0 <= alpha <= 1.0 for alpha in self.per_coordinate_false_alert_upper_bounds)
            and 0.0 <= self.familywise_false_alert_upper_bound <= 1.0
            and self.expected_false_alerts_upper_bound >= 0.0
            and self.prefix_familywise_false_alert_upper_bounds
            == tuple(
                min(1.0, sum(spend.alpha for spend in self.spends[: index + 1]))
                for index in range(len(self.spends))
            )
        )
