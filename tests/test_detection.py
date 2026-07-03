import pytest

from ced.detection import OneSidedDetectionPanel, OneSidedDetector


def test_finite_all_negative_record_remains_compatible_with_presence():
    detector = OneSidedDetector(0.6)
    assert detector.all_negative_probability_if_present(5) == pytest.approx(0.4**5)
    assert detector.all_negative_is_compatible_with_presence(5)
    assert not OneSidedDetector(1.0).all_negative_is_compatible_with_presence(1)
    assert OneSidedDetector(1.0).all_negative_is_compatible_with_presence(0)


def test_positive_is_a_one_sided_presence_certificate():
    assert OneSidedDetector.positive_observation_certifies_presence(True)
    assert not OneSidedDetector.positive_observation_certifies_presence(False)


def test_joint_repeat_frontier_is_minimal_at_declared_confidence():
    detector = OneSidedDetector(0.6)
    repeats = detector.repetitions_for_joint_detection_confidence(3, 0.95)
    assert repeats == 5
    assert detector.any_positive_probability_if_present(repeats) ** 3 >= 0.95
    assert detector.any_positive_probability_if_present(repeats - 1) ** 3 < 0.95


def test_positive_signature_certifies_only_coordinates_with_a_positive_read():
    panel = OneSidedDetectionPanel(3, 3, OneSidedDetector(0.6))
    assert panel.total_reads == 9
    assert panel.positive_signature(((False, False, False), (False, True, False), (True, True, True))) == frozenset({1, 2})
    assert panel.all_negative_record_is_ambiguous
    assert panel.verify()


@pytest.mark.parametrize(
    "constructor",
    [
        lambda: OneSidedDetector(0.0),
        lambda: OneSidedDetector(1.1),
        lambda: OneSidedDetectionPanel(0, 1, OneSidedDetector(0.5)),
        lambda: OneSidedDetectionPanel(1, -1, OneSidedDetector(0.5)),
    ],
)
def test_detection_contract_rejects_invalid_parameters(constructor):
    with pytest.raises(ValueError):
        constructor()
