import pytest

from ced.experiment_quotient import CompatibleRecordReport, ExperimentInducedQuotient


WORLDS = ((0, 0), (0, 1), (1, 0), (1, 1))


def target(world):
    presence, response_type = world
    if not presence:
        return "no-interaction"
    return "decrease" if response_type == 0 else "increase"


def test_passive_design_retains_all_latent_worlds_and_requires_set_valued_report():
    quotient = ExperimentInducedQuotient.from_functions(
        WORLDS, lambda world: "same-passive-record", target
    )
    assert quotient.quotient_state_count == 1
    assert quotient.residual_class_sizes == (4,)
    assert not quotient.deterministic_report_exists
    assert quotient.set_valued_report_for_record("same-passive-record") == frozenset(
        {"no-interaction", "decrease", "increase"}
    )
    assert quotient.verify()


def test_detection_refines_presence_but_not_present_response_type():
    quotient = ExperimentInducedQuotient.from_functions(
        WORLDS, lambda world: ("detected" if world[0] else "not-detected"), target
    )
    assert quotient.quotient_state_count == 2
    assert quotient.residual_class_sizes == (2, 2)
    assert quotient.targets_for_record("not-detected") == frozenset({"no-interaction"})
    assert quotient.targets_for_record("detected") == frozenset({"decrease", "increase"})
    assert not quotient.deterministic_report_exists


def test_joint_detection_and_intervention_supports_exact_target_report():
    quotient = ExperimentInducedQuotient.from_functions(
        WORLDS,
        lambda world: ("absent", None) if not world[0] else ("present", world[1]),
        target,
    )
    assert quotient.quotient_state_count == 3
    assert quotient.residual_class_sizes == (2, 1, 1)
    assert quotient.deterministic_report_exists
    assert quotient.exact_report_for_record(("absent", None)) == "no-interaction"
    assert quotient.exact_report_for_record(("present", 0)) == "decrease"
    assert quotient.exact_report_for_record(("present", 1)) == "increase"


def test_design_refinement_orders_information_without_claiming_full_identification():
    passive = ExperimentInducedQuotient.from_functions(WORLDS, lambda world: 0, target)
    detection = ExperimentInducedQuotient.from_functions(WORLDS, lambda world: world[0], target)
    combined = ExperimentInducedQuotient.from_functions(
        WORLDS, lambda world: (world[0], world[1] if world[0] else None), target
    )
    assert detection.refines(passive)
    assert combined.refines(detection)
    assert not passive.refines(detection)
    assert not detection.refines(combined)


def test_bounded_support_failure_record_preserves_honest_ambiguity():
    report = CompatibleRecordReport(
        WORLDS,
        tuple(target(world) for world in WORLDS),
        ((1, 0), (1, 1)),
    )
    assert report.compatible_targets == frozenset({"decrease", "increase"})
    assert not report.deterministic_report_exists


def test_rejects_misaligned_or_unknown_contracts():
    with pytest.raises(ValueError):
        ExperimentInducedQuotient(((0,),), (), (0,))
    quotient = ExperimentInducedQuotient(((0,),), ("x",), ("y",))
    with pytest.raises(ValueError):
        quotient.class_of((1,))
    with pytest.raises(ValueError):
        quotient.targets_for_record("missing")
