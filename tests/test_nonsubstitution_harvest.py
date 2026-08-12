"""Regression tests for the non-substitution harvest.

These pin the qualitative shape of each harvested claim rather than only the
numbers, so that a change in the underlying detection or overlapping-factor
machinery that would invalidate the manuscript argument fails here first.
"""

from __future__ import annotations

import runpy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "harvest_nonsubstitution.py"

_harvest = runpy.run_path(str(SCRIPT))

harvest_allocation = _harvest["harvest_allocation"]
harvest_hitting_set = _harvest["harvest_hitting_set"]
harvest_horizon = _harvest["harvest_horizon"]
harvest_mode_floor = _harvest["harvest_mode_floor"]
harvest_saturation = _harvest["harvest_saturation"]
harvest_sharing = _harvest["harvest_sharing"]
minimum_hitting_set_size = _harvest["minimum_hitting_set_size"]


def test_reads_never_cross_the_availability_ceiling() -> None:
    for row in harvest_saturation():
        assert row["joint_detection_lower_bound"] <= row["availability_ceiling"]
        assert row["gap_to_ceiling"] >= 0.0


def test_reads_saturate_at_the_ceiling_within_fixed_mode_structure() -> None:
    rows = [row for row in harvest_saturation() if row["mode_count"] == 1]
    by_repetitions = {row["repetitions_per_mode"]: row for row in rows}
    # Effort buys progress early and nothing at all once the ceiling is reached.
    assert (
        by_repetitions[1]["joint_detection_lower_bound"]
        < by_repetitions[10]["joint_detection_lower_bound"]
    )
    assert by_repetitions[100]["gap_to_ceiling"] == 0.0
    assert (
        by_repetitions[1000]["joint_detection_lower_bound"]
        == by_repetitions[100]["joint_detection_lower_bound"]
    )


def test_mode_floor_is_necessary_and_sufficient_for_the_ceiling() -> None:
    for row in harvest_mode_floor():
        availability = row["availability_lower_bound"]
        floor = row["necessary_mode_count"]
        # The floor attains the target confidence as a ceiling ...
        assert row["ceiling_at_floor"] >= row["target_confidence"]
        # ... and one fewer mode cannot, for any read budget whatsoever.
        assert 1.0 - (1.0 - availability) ** (floor - 1) < row["target_confidence"]


def test_equal_effort_designs_differ_by_allocation_alone() -> None:
    rows = harvest_allocation()
    assert len({row["total_reads"] for row in rows}) == 1, "effort must be held fixed"
    ordered = sorted(rows, key=lambda row: row["mode_count"])
    bounds = [row["joint_detection_lower_bound"] for row in ordered]
    assert bounds == sorted(bounds), "spreading effort across modes must not hurt"
    assert bounds[-1] > bounds[0], "and here it must strictly help"


def test_sharing_moves_the_ceiling_not_merely_the_approach_to_it() -> None:
    rows = harvest_sharing()
    ceilings = [row["availability_ceiling"] for row in rows]
    assert ceilings == sorted(ceilings, reverse=True), "sharing must not raise the ceiling"
    assert ceilings[0] > ceilings[-1], "and must strictly lower it here"


def test_replication_cannot_recover_what_sharing_costs() -> None:
    rows = harvest_sharing()
    independent, fully_shared = rows[0], rows[-1]
    # This is the discriminating comparison: an unlimited read budget under full
    # sharing loses to a two-read budget under independence.
    assert fully_shared["joint_lb_r1000"] < independent["joint_lb_r2"]


def test_one_surviving_independent_mode_carries_most_of_the_guarantee() -> None:
    rows = {row["sharing_degree"]: row for row in harvest_sharing()}
    total_loss = rows[0]["availability_ceiling"] - rows[4]["availability_ceiling"]
    loss_with_one_mode_spared = rows[0]["availability_ceiling"] - rows[3]["availability_ceiling"]
    # Retaining a single mode off the shared factor avoids most of the collapse.
    assert loss_with_one_mode_spared < 0.25 * total_loss


def test_horizon_and_memory_gap_are_independent_resources() -> None:
    rows = harvest_horizon()
    for module_count in {row["module_count"] for row in rows}:
        group = [row for row in rows if row["module_count"] == module_count]
        assert len({row["memory_gap_bits"] for row in group}) == 1, "delay must not move memory"
        assert len({row["revealing_horizon"] for row in group}) == len(group)
    for row in rows:
        assert row["blind_through_prior_horizon"] is True


def test_minimum_hitting_set_size_is_the_transversal() -> None:
    # One factor shared by every mode is disabled by that factor alone.
    assert minimum_hitting_set_size((frozenset({0, 9}), frozenset({1, 9})), 10) == 1
    # Without a shared factor every mode must be knocked out separately.
    assert minimum_hitting_set_size((frozenset({0}), frozenset({1}), frozenset({2})), 3) == 3


def test_hitting_set_lower_bounds_total_failure() -> None:
    for row in harvest_hitting_set():
        assert row["all_modes_failed_probability"] >= row["hitting_set_lower_bound"]


def test_counting_shared_factors_does_not_predict_the_ceiling() -> None:
    rows = {row["configuration"]: row for row in harvest_hitting_set()}
    three_covering = rows["three shared factors covering all"]
    two_sparing = rows["two shared factors, one mode spared"]
    # The design with MORE shared factors is the safer one, so the count of shared
    # factors cannot be the quantity that orders these designs.
    assert three_covering["shared_factor_count"] > two_sparing["shared_factor_count"]
    assert three_covering["availability_ceiling"] < two_sparing["availability_ceiling"]


def test_sparing_one_mode_raises_the_minimum_hitting_set() -> None:
    rows = {row["configuration"]: row for row in harvest_hitting_set()}
    covering = rows["two shared factors covering all"]
    sparing = rows["two shared factors, one mode spared"]
    assert covering["covers_every_mode"] is True
    assert sparing["covers_every_mode"] is False
    # Leaving one mode off every shared factor forces an extra private failure.
    assert sparing["minimum_hitting_set_size"] == covering["minimum_hitting_set_size"] + 1
    assert sparing["availability_ceiling"] > covering["availability_ceiling"]


def test_sparing_one_mode_recovers_that_modes_own_availability() -> None:
    """The spared-mode identity is general, and independent of the shared factor.

    P(all fail | s) = rho_s * rho_p^(m - s) + (1 - rho_s) * rho_p^m, so the share
    of the total sharing loss still remaining when one mode is spared is
    (rho_p - rho_p^m) / (1 - rho_p^m), which contains no rho_s term at all.
    """
    sharing_panel = _harvest["_sharing_panel"]
    for mode_count in (3, 4, 6):
        for private in (0.1, 0.2, 0.5):
            remaining_by_shared = set()
            for shared in (0.05, 0.2, 0.6):
                ceiling = {
                    degree: sharing_panel(mode_count, degree, 2, private, shared).availability_ceiling
                    for degree in (0, mode_count - 1, mode_count)
                }
                total_loss = ceiling[0] - ceiling[mode_count]
                spared_loss = ceiling[0] - ceiling[mode_count - 1]
                remaining = spared_loss / total_loss
                predicted = (private - private**mode_count) / (1.0 - private**mode_count)
                assert remaining == pytest.approx(predicted, abs=1e-12)
                remaining_by_shared.add(round(remaining, 12))
            # Identical across every shared-factor probability.
            assert len(remaining_by_shared) == 1
