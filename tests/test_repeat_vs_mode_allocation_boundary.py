from __future__ import annotations

import math

from ced.allocation_boundary import two_read_allocation_boundary
from ced.detection import OneSidedDetector
from ced.mode_detection import ModeDiverseDetectionPanel


def panel(k, m, r, a, p):
    return ModeDiverseDetectionPanel(
        coordinate_count=k,
        mode_count=m,
        repetitions_per_mode=r,
        availability_lower_bound=a,
        detector=OneSidedDetector(p),
    ).joint_detection_lower_bound


def test_closed_forms_match_existing_mode_detection_theorem():
    for k in range(1, 7):
        for a in (0.2, 0.5, 0.8, 0.99):
            for p in (0.05, 0.2, 0.6, 0.9):
                audit = two_read_allocation_boundary(
                    coordinate_count=k, availability=a, sensitivity=p
                )
                assert math.isclose(
                    audit.repeat_design_guarantee,
                    panel(k, 1, 2, a, p),
                    rel_tol=0,
                    abs_tol=1e-12,
                )
                assert math.isclose(
                    audit.diverse_design_guarantee,
                    panel(k, 2, 1, a, p),
                    rel_tol=0,
                    abs_tol=1e-12,
                )


def test_preference_sign_matches_exact_threshold_on_dense_grid():
    for k in range(1, 9):
        threshold = 2.0 - 2.0 ** (1.0 / k)
        for a in (0.1, 0.3, 0.8, 0.95):
            for p in (0.05, 0.2, 0.4, 0.6, 0.75, 0.9, 0.99):
                audit = two_read_allocation_boundary(
                    coordinate_count=k, availability=a, sensitivity=p
                )
                expected = (
                    "diverse_modes"
                    if p > threshold + 1e-12
                    else "within_mode_repeats"
                    if p < threshold - 1e-12
                    else "tie"
                )
                assert audit.preferred_design == expected


def test_exact_equality_at_threshold():
    for k in range(1, 9):
        p = 2.0 - 2.0 ** (1.0 / k)
        for a in (0.2, 0.5, 0.8):
            audit = two_read_allocation_boundary(
                coordinate_count=k, availability=a, sensitivity=p
            )
            assert abs(audit.difference_diverse_minus_repeat) < 1e-12
            assert audit.preferred_design == "tie"


def test_single_coordinate_always_favors_diversity_in_the_interior():
    for a in (0.1, 0.5, 0.9):
        for p in (0.01, 0.1, 0.5, 0.99):
            audit = two_read_allocation_boundary(
                coordinate_count=1, availability=a, sensitivity=p
            )
            assert audit.sensitivity_threshold == 0.0
            assert audit.preferred_design == "diverse_modes"


def test_threshold_increases_with_joint_coordinate_count_and_tends_upward():
    thresholds = [
        two_read_allocation_boundary(
            coordinate_count=k, availability=0.8, sensitivity=0.5
        ).sensitivity_threshold
        for k in range(1, 30)
    ]
    assert thresholds[0] == 0.0
    assert all(a < b for a, b in zip(thresholds, thresholds[1:]))
    assert thresholds[-1] > 0.97
    assert all(t < 1.0 for t in thresholds)


def test_both_sides_of_boundary_are_real_not_numerical_artifacts():
    # k=3 threshold is about 0.7401: at p=.6 depth wins.
    low_p = two_read_allocation_boundary(
        coordinate_count=3, availability=0.8, sensitivity=0.6
    )
    assert low_p.preferred_design == "within_mode_repeats"
    assert low_p.repeat_design_guarantee > low_p.diverse_design_guarantee

    # At p=.9, diversification wins under the same k and a.
    high_p = two_read_allocation_boundary(
        coordinate_count=3, availability=0.8, sensitivity=0.9
    )
    assert high_p.preferred_design == "diverse_modes"
    assert high_p.diverse_design_guarantee > high_p.repeat_design_guarantee


def test_availability_boundary_cases_remove_failure_diversity_advantage():
    for a in (0.0, 1.0):
        for k in (1, 2, 5):
            audit = two_read_allocation_boundary(
                coordinate_count=k, availability=a, sensitivity=0.7
            )
            assert abs(audit.difference_diverse_minus_repeat) < 1e-12
            assert audit.preferred_design == "tie"
