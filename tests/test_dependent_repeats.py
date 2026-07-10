from math import inf

import pytest

from ced.dependent_repeats import DependentThresholdEvidenceDesign


def test_dependent_repeat_bounds_are_expectation_bounds_not_binomial_tails():
    design = DependentThresholdEvidenceDesign(
        read_count=5,
        positive_threshold=3,
        sensitivity_lower_bound=0.7,
        false_positive_upper_bound=0.05,
    )
    assert design.expected_absent_positive_count_upper_bound == pytest.approx(0.25)
    assert design.false_alert_probability_upper_bound == pytest.approx(1 / 12)
    assert design.expected_present_positive_count_lower_bound == pytest.approx(3.5)
    assert design.detection_probability_lower_bound == pytest.approx(0.5)
    assert design.evidence_ratio_lower_bound == pytest.approx(6.0)
    assert not design.threshold_crossing_certifies_presence
    assert design.verify()


def test_nonreset_repeats_do_not_improve_any_positive_detection_guarantee():
    design = DependentThresholdEvidenceDesign(
        read_count=10,
        positive_threshold=1,
        sensitivity_lower_bound=0.6,
        false_positive_upper_bound=0.05,
    )
    assert design.detection_probability_lower_bound == pytest.approx(0.6)
    assert design.false_alert_probability_upper_bound == pytest.approx(0.5)


def test_zero_false_positive_recovers_deductive_threshold_certificate():
    design = DependentThresholdEvidenceDesign(
        read_count=5,
        positive_threshold=3,
        sensitivity_lower_bound=0.7,
        false_positive_upper_bound=0.0,
    )
    assert design.false_alert_probability_upper_bound == 0.0
    assert design.detection_probability_lower_bound == pytest.approx(0.5)
    assert design.evidence_ratio_lower_bound == inf
    assert design.threshold_crossing_certifies_presence


def test_high_threshold_can_have_no_detection_guarantee_without_independence():
    design = DependentThresholdEvidenceDesign(
        read_count=5,
        positive_threshold=5,
        sensitivity_lower_bound=0.7,
        false_positive_upper_bound=0.05,
    )
    assert design.detection_probability_lower_bound == 0.0
    assert design.false_alert_probability_upper_bound == pytest.approx(0.05)
    assert design.evidence_ratio_lower_bound == 0.0


def test_accepts_counts_against_threshold():
    design = DependentThresholdEvidenceDesign(5, 3, 0.7, 0.05)
    assert not design.accepts(2)
    assert design.accepts(3)
    assert design.accepts(5)
    with pytest.raises(ValueError):
        design.accepts(-1)
    with pytest.raises(ValueError):
        design.accepts(6)


@pytest.mark.parametrize(
    "constructor",
    [
        lambda: DependentThresholdEvidenceDesign(0, 1, 0.7, 0.05),
        lambda: DependentThresholdEvidenceDesign(5, 0, 0.7, 0.05),
        lambda: DependentThresholdEvidenceDesign(5, 6, 0.7, 0.05),
        lambda: DependentThresholdEvidenceDesign(5, 3, -0.1, 0.05),
        lambda: DependentThresholdEvidenceDesign(5, 3, 0.7, -0.05),
        lambda: DependentThresholdEvidenceDesign(5, 3, 0.05, 0.05),
        lambda: DependentThresholdEvidenceDesign(5, 3, 0.05, 0.7),
    ],
)
def test_dependent_repeat_design_rejects_invalid_contracts(constructor):
    with pytest.raises(ValueError):
        constructor()
