"""Regression tests for the non-substitution harvest.

These pin the qualitative shape of each harvested claim rather than only the
numbers, so that a change in the underlying detection or overlapping-factor
machinery that would invalidate the manuscript argument fails here first.
"""

from __future__ import annotations

from scripts.harvest_nonsubstitution import (
    harvest_allocation,
    harvest_horizon,
    harvest_mode_floor,
    harvest_saturation,
    harvest_sharing,
)


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
