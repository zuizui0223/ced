import pytest

from ced.target_resolution import (
    CostedTargetResolutionDesign,
    RiskLimitedTargetResolution,
    TargetRecordOutcome,
    cheapest_feasible_target_resolution,
)


def _designs():
    passive = RiskLimitedTargetResolution(
        "decrease",
        (TargetRecordOutcome("passive", 1.0, frozenset(("no interaction", "decrease", "increase"))),),
    )
    detection = RiskLimitedTargetResolution(
        "decrease",
        (
            TargetRecordOutcome("absent", 0.10, frozenset(("no interaction",))),
            TargetRecordOutcome("present", 0.90, frozenset(("decrease", "increase"))),
        ),
    )
    intervention = RiskLimitedTargetResolution(
        "decrease",
        (
            TargetRecordOutcome("absent", 0.03, frozenset(("no interaction",))),
            TargetRecordOutcome("decrease", 0.88, frozenset(("decrease",))),
            TargetRecordOutcome("shared-failure", 0.09, frozenset(("decrease", "increase"))),
        ),
    )
    return passive, detection, intervention


def test_resolution_decomposes_correct_wrong_and_ambiguous_records():
    passive, detection, intervention = _designs()
    assert passive.correct_resolution_probability == 0.0
    assert passive.wrong_resolution_probability == 0.0
    assert passive.ambiguity_probability == 1.0
    assert detection.correct_resolution_probability == 0.0
    assert detection.wrong_resolution_probability == pytest.approx(0.10)
    assert detection.ambiguity_probability == pytest.approx(0.90)
    assert intervention.correct_resolution_probability == pytest.approx(0.88)
    assert intervention.wrong_resolution_probability == pytest.approx(0.03)
    assert intervention.ambiguity_probability == pytest.approx(0.09)
    assert all(design.verify() for design in (passive, detection, intervention))


def test_cost_aware_selection_requires_target_resolution_not_detection_alone():
    passive, detection, intervention = _designs()
    designs = (
        CostedTargetResolutionDesign("stop", 0.0, passive),
        CostedTargetResolutionDesign("detect", 1.0, detection),
        CostedTargetResolutionDesign("detect-and-intervene", 2.5, intervention),
    )
    chosen = cheapest_feasible_target_resolution(designs, 0.80, 0.05)
    assert chosen is not None
    assert chosen.name == "detect-and-intervene"
    assert cheapest_feasible_target_resolution(designs, 0.95, 0.05) is None


def test_invalid_contracts_are_rejected():
    with pytest.raises(ValueError):
        TargetRecordOutcome("x", 1.2, frozenset(("a",)))
    with pytest.raises(ValueError):
        RiskLimitedTargetResolution(
            "a", (TargetRecordOutcome("x", 0.8, frozenset(("a",))),)
        )
    with pytest.raises(ValueError):
        CostedTargetResolutionDesign("", 1.0, _designs()[0])
