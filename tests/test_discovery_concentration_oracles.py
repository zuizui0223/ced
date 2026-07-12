from itertools import product

import pytest

from ced.discovery_concentration import IndependentFalseDiscoveryConcentration


def _enumerated_tail(probabilities, budget):
    total = 0.0
    for outcomes in product((0, 1), repeat=len(probabilities)):
        probability = 1.0
        for outcome, alpha in zip(outcomes, probabilities):
            probability *= alpha if outcome else 1.0 - alpha
        if sum(outcomes) >= budget:
            total += probability
    return total


def test_exact_poisson_binomial_tail_matches_binary_record_enumeration():
    probabilities = (0.05, 0.1, 0.2, 0.3)
    design = IndependentFalseDiscoveryConcentration(probabilities)
    for budget in range(1, 6):
        assert design.exact_independent_tail_upper_bound(budget) == pytest.approx(
            _enumerated_tail(probabilities, budget)
        )
        assert design.exact_independent_tail_upper_bound(budget) <= (
            design.markov_tail_upper_bound(budget) + 1e-12
        )
        assert design.exact_independent_tail_upper_bound(budget) <= (
            design.chernoff_tail_upper_bound(budget) + 1e-12
        )
