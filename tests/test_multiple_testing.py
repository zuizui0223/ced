import pytest

from ced.multiple_testing import MultipleThresholdEvidenceDesign
from ced.threshold_detection import ThresholdEvidenceDesign


def test_familywise_false_alert_bound_tracks_multiplicity():
    per = ThresholdEvidenceDesign(5, 3, 0.7, 0.05)
    design = MultipleThresholdEvidenceDesign(20, per)
    assert design.per_coordinate_false_alert_upper_bound == pytest.approx(0.001158125)
    assert design.expected_false_alerts_upper_bound == pytest.approx(0.0231625)
    assert design.familywise_false_alert_upper_bound == pytest.approx(0.0231625)
    assert design.exact_independent_all_absent_familywise_false_alert == pytest.approx(
        1 - (1 - 0.001158125) ** 20
    )
    assert design.exact_independent_all_absent_familywise_false_alert <= design.familywise_false_alert_upper_bound
    assert design.per_coordinate_evidence_ratio_lower_bound == pytest.approx(722.650836481381)
    assert design.verify()


def test_familywise_threshold_search_is_minimal():
    assert (
        MultipleThresholdEvidenceDesign.minimum_threshold_for_familywise_false_alert(
            coordinate_count=20,
            read_count=5,
            sensitivity_lower_bound=0.7,
            false_positive_upper_bound=0.05,
            familywise_alpha=0.05,
        )
        == 3
    )
    weaker = MultipleThresholdEvidenceDesign(
        20, ThresholdEvidenceDesign(5, 2, 0.7, 0.05)
    )
    assert weaker.familywise_false_alert_upper_bound > 0.05


def test_joint_familywise_and_evidence_ratio_search():
    assert (
        MultipleThresholdEvidenceDesign.minimum_threshold_for_familywise_and_evidence_ratio(
            coordinate_count=20,
            read_count=5,
            sensitivity_lower_bound=0.7,
            false_positive_upper_bound=0.05,
            familywise_alpha=0.05,
            target_evidence_ratio=100,
        )
        == 3
    )
    with pytest.raises(ValueError):
        MultipleThresholdEvidenceDesign.minimum_threshold_for_familywise_and_evidence_ratio(
            coordinate_count=20,
            read_count=5,
            sensitivity_lower_bound=0.7,
            false_positive_upper_bound=0.05,
            familywise_alpha=0.000001,
            target_evidence_ratio=100,
        )


def test_accepted_coordinates_are_thresholded_one_coordinate_at_a_time():
    design = MultipleThresholdEvidenceDesign(4, ThresholdEvidenceDesign(5, 3, 0.7, 0.05))
    assert design.accepted_coordinates((0, 3, 5, 2)) == frozenset({1, 2})
    with pytest.raises(ValueError):
        design.accepted_coordinates((3, 3))


@pytest.mark.parametrize(
    "constructor",
    [
        lambda: MultipleThresholdEvidenceDesign(0, ThresholdEvidenceDesign(5, 3, 0.7, 0.05)),
        lambda: MultipleThresholdEvidenceDesign(3, object()),
        lambda: MultipleThresholdEvidenceDesign.minimum_threshold_for_familywise_false_alert(0, 5, 0.7, 0.05, 0.05),
        lambda: MultipleThresholdEvidenceDesign.minimum_threshold_for_familywise_false_alert(3, 5, 0.7, 0.05, 1.0),
    ],
)
def test_multiple_testing_rejects_invalid_contracts(constructor):
    with pytest.raises(ValueError):
        constructor()
