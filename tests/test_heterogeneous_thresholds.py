import pytest

from ced.heterogeneous_thresholds import HeterogeneousThresholdEvidencePanel
from ced.threshold_detection import ThresholdEvidenceDesign


def _panel() -> HeterogeneousThresholdEvidencePanel:
    return HeterogeneousThresholdEvidencePanel(
        (
            ThresholdEvidenceDesign(5, 3, 0.7, 0.05),
            ThresholdEvidenceDesign(4, 2, 0.6, 0.02),
            ThresholdEvidenceDesign(6, 4, 0.8, 0.1),
        )
    )


def test_heterogeneous_panel_risk_and_detection_bounds():
    panel = _panel()
    assert panel.coordinate_count == 3
    assert panel.per_coordinate_false_alert_upper_bounds == pytest.approx(
        (0.001158125, 0.00233648, 0.00127)
    )
    assert panel.per_coordinate_detection_lower_bounds == pytest.approx(
        (0.83692, 0.8208, 0.90112)
    )
    assert panel.expected_false_alerts_upper_bound == pytest.approx(0.004764605)
    assert panel.familywise_false_alert_upper_bound == pytest.approx(0.004764605)
    assert panel.exact_independent_all_absent_familywise_false_alert == pytest.approx(
        0.004757464352288521
    )
    assert panel.expected_missed_detections_upper_bound == pytest.approx(0.44116)
    assert panel.all_present_joint_detection_lower_bound_no_independence == pytest.approx(
        0.55884
    )
    assert panel.exact_independent_all_present_joint_detection_lower_bound == pytest.approx(
        0.61901891960832
    )
    assert panel.verify()


def test_heterogeneous_weighted_budget_and_acceptance():
    panel = _panel()
    assert panel.weighted_false_alert_budget_upper_bound((1, 2, 5)) == pytest.approx(
        0.012181085
    )
    assert panel.accepted_coordinates((2, 2, 4)) == (1, 2)
    assert panel.accepted_coordinates((3, 1, 3)) == (0,)
    with pytest.raises(ValueError):
        panel.weighted_false_alert_budget_upper_bound((1, 2))
    with pytest.raises(ValueError):
        panel.weighted_false_alert_budget_upper_bound((1, -1, 1))
    with pytest.raises(ValueError):
        panel.accepted_coordinates((1, 2))
    with pytest.raises(ValueError):
        panel.accepted_coordinates((1, 2, 7))


def test_evidence_ratio_filter_is_coordinate_specific():
    panel = _panel()
    assert panel.per_coordinate_evidence_ratio_lower_bounds == pytest.approx(
        (722.650836481381, 351.2976785592001, 709.543307086614)
    )
    assert panel.coordinates_meeting_evidence_ratio(700) == (0, 2)
    assert panel.coordinates_meeting_evidence_ratio(800) == ()
    with pytest.raises(ValueError):
        panel.coordinates_meeting_evidence_ratio(-1)


def test_rejects_empty_or_non_threshold_inputs():
    with pytest.raises(ValueError):
        HeterogeneousThresholdEvidencePanel(())
    with pytest.raises(ValueError):
        HeterogeneousThresholdEvidencePanel((object(),))  # type: ignore[arg-type]
