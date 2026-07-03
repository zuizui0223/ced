import pytest

from ced.detection import OneSidedDetector
from ced.mode_detection import ModeDiverseDetectionPanel


def test_common_mode_ceiling_cannot_be_bought_with_within_mode_repeats():
    detector = OneSidedDetector(0.6)
    one_mode = ModeDiverseDetectionPanel(3, 1, 10, 0.8, detector)
    two_modes = ModeDiverseDetectionPanel(3, 2, 5, 0.8, detector)
    assert one_mode.availability_ceiling == pytest.approx(0.8)
    assert one_mode.joint_detection_lower_bound < 0.8
    assert one_mode.joint_detection_lower_bound == pytest.approx(0.7997483681473567)
    assert two_modes.availability_ceiling == pytest.approx(0.96)
    assert two_modes.joint_detection_lower_bound == pytest.approx(0.9500686142165017)


def test_mode_floor_and_repeat_frontier_are_minimal():
    detector = OneSidedDetector(0.6)
    assert ModeDiverseDetectionPanel.minimum_mode_count_for_availability_ceiling(0.8, 0.95) == 2
    one_mode = ModeDiverseDetectionPanel(3, 1, 1, 0.8, detector)
    assert not one_mode.can_reach_joint_confidence(0.95)
    with pytest.raises(ValueError):
        one_mode.minimum_repetitions_for_joint_confidence(0.95)
    two_modes = ModeDiverseDetectionPanel(3, 2, 1, 0.8, detector)
    repeats = two_modes.minimum_repetitions_for_joint_confidence(0.95)
    assert repeats == 5
    assert ModeDiverseDetectionPanel(3, 2, repeats, 0.8, detector).joint_detection_lower_bound >= 0.95
    assert ModeDiverseDetectionPanel(3, 2, repeats - 1, 0.8, detector).joint_detection_lower_bound < 0.95


def test_full_negative_panel_remains_ambiguous_under_common_mode_failure():
    panel = ModeDiverseDetectionPanel(3, 2, 5, 0.8, OneSidedDetector(0.6))
    assert panel.all_negative_record_is_ambiguous
    assert panel.all_negative_probability_if_all_present_upper_bound == pytest.approx(
        (0.2 + 0.8 * 0.4**15) ** 2
    )


def test_positive_signature_is_one_sided_across_modes():
    panel = ModeDiverseDetectionPanel(3, 2, 2, 0.8, OneSidedDetector(0.6))
    observations = (
        ((False, False), (False, True), (False, False)),
        ((True, False), (False, False), (False, False)),
    )
    assert panel.positive_signature(observations) == frozenset({0, 1})
    assert panel.verify()


@pytest.mark.parametrize(
    "constructor",
    [
        lambda: ModeDiverseDetectionPanel(0, 1, 1, 0.8, OneSidedDetector(0.6)),
        lambda: ModeDiverseDetectionPanel(1, 0, 1, 0.8, OneSidedDetector(0.6)),
        lambda: ModeDiverseDetectionPanel(1, 1, -1, 0.8, OneSidedDetector(0.6)),
        lambda: ModeDiverseDetectionPanel(1, 1, 1, 0.0, OneSidedDetector(0.6)),
    ],
)
def test_mode_detection_rejects_invalid_contracts(constructor):
    with pytest.raises(ValueError):
        constructor()
