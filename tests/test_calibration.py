import pytest

from ced.calibration import (
    CalibrationBounds,
    binomial_cdf,
    binomial_survival,
    false_positive_upper_confidence_bound,
    sensitivity_lower_confidence_bound,
)


def test_calibration_bounds_feed_threshold_and_multiple_designs():
    calibration = CalibrationBounds(
        blank_read_count=60,
        blank_positive_count=0,
        present_read_count=60,
        present_positive_count=55,
        delta=0.05,
    )
    assert calibration.false_positive_upper_bound == pytest.approx(0.04870291331009752)
    assert calibration.sensitivity_lower_bound == pytest.approx(0.8327369235749102)
    assert calibration.bounds_are_separated
    assert calibration.confidence_level_per_bound == pytest.approx(0.95)
    assert calibration.joint_confidence_lower_bound == pytest.approx(0.9)
    threshold = calibration.as_threshold_design(read_count=5, positive_threshold=3)
    assert threshold.false_alert_probability_upper_bound == pytest.approx(0.0010724705247173087)
    assert threshold.detection_probability_lower_bound == pytest.approx(0.9641600398827371)
    assert threshold.evidence_ratio_lower_bound == pytest.approx(899.0084274221699)
    multiple = calibration.as_multiple_threshold_design(
        coordinate_count=20, read_count=5, positive_threshold=3
    )
    assert multiple.familywise_false_alert_upper_bound == pytest.approx(0.021449410494346174)
    assert multiple.verify()
    assert calibration.verify()


def test_clopper_pearson_equations_are_satisfied_at_bounds():
    f_upper = false_positive_upper_confidence_bound(60, 0, 0.05)
    p_lower = sensitivity_lower_confidence_bound(60, 55, 0.05)
    assert binomial_cdf(60, 0, f_upper) == pytest.approx(0.05, abs=1e-12)
    assert binomial_survival(60, 55, p_lower) == pytest.approx(0.05, abs=1e-12)


def test_vacuous_calibration_edges():
    assert false_positive_upper_confidence_bound(5, 5, 0.05) == 1.0
    assert sensitivity_lower_confidence_bound(5, 0, 0.05) == 0.0


@pytest.mark.parametrize(
    "constructor",
    [
        lambda: CalibrationBounds(0, 0, 60, 55, 0.05),
        lambda: CalibrationBounds(60, 61, 60, 55, 0.05),
        lambda: CalibrationBounds(60, 0, 0, 0, 0.05),
        lambda: CalibrationBounds(60, 0, 60, 61, 0.05),
        lambda: CalibrationBounds(60, 0, 60, 55, 0.0),
        lambda: CalibrationBounds(60, 0, 60, 55, 1.0),
    ],
)
def test_calibration_rejects_invalid_contracts(constructor):
    with pytest.raises(ValueError):
        constructor()
