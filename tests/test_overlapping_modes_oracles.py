"""Finite oracles for overlapping latent failure factors."""

from __future__ import annotations

from itertools import product

import pytest

from ced.overlapping_modes import OverlappingFailureModePanel


def _enumerated_joint_detection(panel: OverlappingFailureModePanel) -> float:
    q = panel.within_mode_coordinate_miss_probability_upper_bound
    total = 0.0
    for failed_bits in product((False, True), repeat=panel.factor_count):
        failed_factors = frozenset(
            index for index, failed in enumerate(failed_bits) if failed
        )
        factor_probability = panel.factor_state_probability(failed_factors)
        active_modes = panel.operating_modes(failed_factors)
        if not active_modes:
            continue
        # Enumerate per-coordinate success/failure after all active modes. Each
        # coordinate is missed by every active mode with probability q^a.
        miss_probability = q ** len(active_modes)
        for coordinate_outcomes in product(
            (False, True), repeat=panel.coordinate_count
        ):
            outcome_probability = 1.0
            for detected in coordinate_outcomes:
                outcome_probability *= (
                    1.0 - miss_probability if detected else miss_probability
                )
            if all(coordinate_outcomes):
                total += factor_probability * outcome_probability
    return total


def _enumerated_all_modes_failed(panel: OverlappingFailureModePanel) -> float:
    return sum(
        panel.factor_state_probability(state)
        for state in panel.factor_states()
        if len(panel.operating_modes(state)) == 0
    )


@pytest.mark.parametrize(
    "panel",
    [
        OverlappingFailureModePanel(
            2,
            2,
            0.6,
            (0.1, 0.2, 0.3),
            (frozenset({0, 1}), frozenset({1, 2})),
        ),
        OverlappingFailureModePanel(
            2,
            3,
            0.7,
            (0.2, 0.2),
            (frozenset({0}), frozenset({1})),
        ),
        OverlappingFailureModePanel(
            2,
            2,
            0.7,
            (0.25,),
            (frozenset({0}), frozenset({0}), frozenset({0})),
        ),
    ],
)
def test_exact_formulas_match_finite_factor_state_and_detection_enumeration(panel):
    assert _enumerated_all_modes_failed(panel) == pytest.approx(
        panel.all_modes_failed_probability
    )
    assert _enumerated_joint_detection(panel) == pytest.approx(
        panel.joint_detection_probability_lower_bound
    )


def test_partial_overlap_lies_between_independent_and_fully_shared_designs():
    # Same two modes, same marginal factor failure probability 0.2. Unique factors
    # maximize failure diversity; one shared factor minimizes it. The partial case
    # adds one shared factor with smaller failure probability.
    independent = OverlappingFailureModePanel(
        2,
        3,
        0.7,
        (0.2, 0.2),
        (frozenset({0}), frozenset({1})),
    )
    partial = OverlappingFailureModePanel(
        2,
        3,
        0.7,
        (0.05, 0.15, 0.15),
        (frozenset({0, 1}), frozenset({0, 2})),
    )
    common = OverlappingFailureModePanel(
        2,
        3,
        0.7,
        (0.2,),
        (frozenset({0}), frozenset({0})),
    )
    assert common.availability_ceiling < partial.availability_ceiling < independent.availability_ceiling
    assert common.joint_detection_probability_lower_bound < partial.joint_detection_probability_lower_bound < independent.joint_detection_probability_lower_bound
