import pytest

from ced.overlapping_modes import OverlappingFailureModePanel


def test_partially_shared_failure_factors():
    panel = OverlappingFailureModePanel(
        coordinate_count=3,
        repetitions_per_coordinate_per_mode=2,
        sensitivity_lower_bound=0.6,
        factor_failure_probabilities=(0.1, 0.2, 0.3),
        mode_factor_sets=(frozenset({0, 1}), frozenset({1, 2})),
    )
    assert panel.factor_count == 3
    assert panel.mode_count == 2
    assert panel.shared_factor_count == 1
    assert panel.pairwise_mode_overlap_counts == ((2, 1), (1, 2))
    assert panel.within_mode_coordinate_miss_probability_upper_bound == pytest.approx(0.16)
    assert panel.all_modes_failed_probability == pytest.approx(0.224)
    assert panel.availability_ceiling == pytest.approx(0.776)
    assert panel.joint_detection_probability_lower_bound == pytest.approx(0.6274907366031359)
    assert panel.total_read_count == 12
    assert panel.verify()


def test_operating_modes_follow_factor_overlap():
    panel = OverlappingFailureModePanel(
        1,
        1,
        0.8,
        (0.1, 0.2, 0.3),
        (frozenset({0, 1}), frozenset({1, 2})),
    )
    assert panel.operating_modes(frozenset()) == (0, 1)
    assert panel.operating_modes(frozenset({0})) == (1,)
    assert panel.operating_modes(frozenset({2})) == (0,)
    assert panel.operating_modes(frozenset({1})) == ()


def test_independent_modes_are_recovered_with_unique_factors():
    panel = OverlappingFailureModePanel(
        2,
        3,
        0.7,
        (0.2, 0.2),
        (frozenset({0}), frozenset({1})),
    )
    q = (1.0 - 0.7) ** 3
    expected = (
        0.8**2 * (1.0 - q**2) ** 2
        + 2 * 0.8 * 0.2 * (1.0 - q) ** 2
    )
    assert panel.joint_detection_probability_lower_bound == pytest.approx(expected)
    assert panel.all_modes_failed_probability == pytest.approx(0.2**2)
    assert panel.shared_factor_count == 0


def test_one_common_factor_recovers_common_mode_ceiling():
    panel = OverlappingFailureModePanel(
        2,
        4,
        0.7,
        (0.25,),
        (frozenset({0}), frozenset({0}), frozenset({0})),
    )
    q = (1.0 - 0.7) ** 4
    assert panel.availability_ceiling == pytest.approx(0.75)
    assert panel.joint_detection_probability_lower_bound == pytest.approx(
        0.75 * (1.0 - q**3) ** 2
    )
    assert panel.shared_factor_count == 1


@pytest.mark.parametrize(
    "constructor",
    [
        lambda: OverlappingFailureModePanel(0, 1, 0.8, (0.1,), (frozenset({0}),)),
        lambda: OverlappingFailureModePanel(1, 0, 0.8, (0.1,), (frozenset({0}),)),
        lambda: OverlappingFailureModePanel(1, 1, -0.1, (0.1,), (frozenset({0}),)),
        lambda: OverlappingFailureModePanel(1, 1, 0.8, (), (frozenset({0}),)),
        lambda: OverlappingFailureModePanel(1, 1, 0.8, (0.1,), ()),
        lambda: OverlappingFailureModePanel(1, 1, 0.8, (0.1,), (frozenset(),)),
        lambda: OverlappingFailureModePanel(1, 1, 0.8, (0.1,), (frozenset({1}),)),
    ],
)
def test_rejects_invalid_overlapping_mode_contracts(constructor):
    with pytest.raises(ValueError):
        constructor()
