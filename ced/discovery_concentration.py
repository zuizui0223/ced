"""Concentration bounds for independent false discoveries.

The expected-budget layer needs no cross-coordinate independence and therefore
uses Markov's inequality. This module adds the stronger consequences available
when false-alert indicators are explicitly declared independent and may have
heterogeneous upper probabilities.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, prod


def _probability(value: float) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError("false-alert bounds must be finite probabilities")
    probability = float(value)
    if not isfinite(probability) or not 0.0 <= probability <= 1.0:
        raise ValueError("false-alert bounds must lie between zero and one")
    return probability


@dataclass(frozen=True)
class IndependentFalseDiscoveryConcentration:
    """Poisson-binomial false-discovery concentration under independence."""

    false_alert_upper_bounds: tuple[float, ...]

    def __post_init__(self) -> None:
        bounds = tuple(_probability(value) for value in self.false_alert_upper_bounds)
        if not bounds:
            raise ValueError("at least one false-alert bound is required")
        object.__setattr__(self, "false_alert_upper_bounds", bounds)

    @property
    def coordinate_count(self) -> int:
        return len(self.false_alert_upper_bounds)

    @property
    def expected_false_discoveries_upper_bound(self) -> float:
        return sum(self.false_alert_upper_bounds)

    def markov_tail_upper_bound(self, false_discovery_budget: int) -> float:
        if not isinstance(false_discovery_budget, int) or isinstance(false_discovery_budget, bool):
            raise ValueError("false_discovery_budget must be an integer")
        if false_discovery_budget < 1:
            raise ValueError("false_discovery_budget must be positive")
        return min(
            1.0,
            self.expected_false_discoveries_upper_bound / false_discovery_budget,
        )

    def exact_independent_tail_upper_bound(self, false_discovery_budget: int) -> float:
        """Exact Poisson-binomial tail at the declared upper probabilities."""
        if not isinstance(false_discovery_budget, int) or isinstance(false_discovery_budget, bool):
            raise ValueError("false_discovery_budget must be an integer")
        if false_discovery_budget < 0:
            raise ValueError("false_discovery_budget must be nonnegative")
        if false_discovery_budget == 0:
            return 1.0
        if false_discovery_budget > self.coordinate_count:
            return 0.0

        distribution = [1.0] + [0.0] * self.coordinate_count
        for probability in self.false_alert_upper_bounds:
            next_distribution = [0.0] * (self.coordinate_count + 1)
            for count in range(self.coordinate_count):
                mass = distribution[count]
                if mass == 0.0:
                    continue
                next_distribution[count] += mass * (1.0 - probability)
                next_distribution[count + 1] += mass * probability
            distribution = next_distribution
        return sum(distribution[false_discovery_budget:])

    def chernoff_tail_upper_bound(self, false_discovery_budget: int) -> float:
        """Poisson-binomial multiplicative Chernoff bound using mu=sum alpha_i."""
        if not isinstance(false_discovery_budget, int) or isinstance(false_discovery_budget, bool):
            raise ValueError("false_discovery_budget must be an integer")
        if false_discovery_budget < 1:
            raise ValueError("false_discovery_budget must be positive")
        if false_discovery_budget > self.coordinate_count:
            return 0.0

        mu = self.expected_false_discoveries_upper_bound
        if mu == 0.0:
            return 0.0
        budget = float(false_discovery_budget)
        if budget <= mu:
            return 1.0
        return min(1.0, exp(budget - mu) * (mu / budget) ** budget)

    def exact_zero_false_discovery_probability_lower_bound(self) -> float:
        """Exact all-clear probability lower bound under declared independence."""
        return prod(1.0 - probability for probability in self.false_alert_upper_bounds)

    def verify(self) -> bool:
        for budget in range(1, self.coordinate_count + 2):
            exact = self.exact_independent_tail_upper_bound(budget)
            chernoff = self.chernoff_tail_upper_bound(budget)
            markov = self.markov_tail_upper_bound(budget)
            if not (0.0 <= exact <= 1.0):
                return False
            if exact > chernoff + 1e-12:
                return False
            if exact > markov + 1e-12:
                return False
        return True
