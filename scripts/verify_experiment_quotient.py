"""Deterministic replay for the CED–MRM experiment-induced quotient bridge."""

from __future__ import annotations

import json
from pathlib import Path

from ced.experiment_quotient import CompatibleRecordReport, ExperimentInducedQuotient

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts" / "ced_experiment_quotient_report.json"
WORLDS = ((0, 0), (0, 1), (1, 0), (1, 1))


def target(world: tuple[int, int]) -> str:
    presence, response_type = world
    if not presence:
        return "no-interaction"
    return "decrease" if response_type == 0 else "increase"


def build_report() -> dict[str, object]:
    passive = ExperimentInducedQuotient.from_functions(
        WORLDS, lambda world: "same-passive-record", target
    )
    detection = ExperimentInducedQuotient.from_functions(
        WORLDS, lambda world: "detected" if world[0] else "not-detected", target
    )
    combined = ExperimentInducedQuotient.from_functions(
        WORLDS,
        lambda world: ("absent", None) if not world[0] else ("present", world[1]),
        target,
    )
    shared_failure = CompatibleRecordReport(
        WORLDS,
        tuple(target(world) for world in WORLDS),
        ((1, 0), (1, 1)),
    )
    if not all(quotient.verify() for quotient in (passive, detection, combined)):
        raise AssertionError("experiment-induced quotient witness failed verification")

    return {
        "schema_version": 1,
        "latent_worlds": WORLDS,
        "report_target_by_world": tuple(target(world) for world in WORLDS),
        "designs": {
            "passive": {
                "quotient_state_count": passive.quotient_state_count,
                "residual_class_sizes": passive.residual_class_sizes,
                "deterministic_report_exists": passive.deterministic_report_exists,
                "compatible_targets": tuple(sorted(passive.targets_for_record("same-passive-record"))),
            },
            "detection_only": {
                "quotient_state_count": detection.quotient_state_count,
                "residual_class_sizes": detection.residual_class_sizes,
                "deterministic_report_exists": detection.deterministic_report_exists,
                "absent_targets": tuple(sorted(detection.targets_for_record("not-detected"))),
                "present_targets": tuple(sorted(detection.targets_for_record("detected"))),
            },
            "detection_plus_intervention": {
                "quotient_state_count": combined.quotient_state_count,
                "residual_class_sizes": combined.residual_class_sizes,
                "deterministic_report_exists": combined.deterministic_report_exists,
                "reports": {
                    "absent": combined.exact_report_for_record(("absent", None)),
                    "present_type_0": combined.exact_report_for_record(("present", 0)),
                    "present_type_1": combined.exact_report_for_record(("present", 1)),
                },
            },
        },
        "refinement_order": {
            "detection_refines_passive": detection.refines(passive),
            "combined_refines_detection": combined.refines(detection),
        },
        "shared_failure_record": {
            "compatible_worlds": shared_failure.compatible_worlds,
            "compatible_targets": tuple(sorted(shared_failure.compatible_targets)),
            "deterministic_report_exists": shared_failure.deterministic_report_exists,
        },
        "submission_decision": {
            "bridge_is_joint": True,
            "reason": "the target-relevant quotient jointly uses presence and response type; presence detection alone is insufficient",
            "remaining_requirement": "connect probabilistic class refinement to existing CED failure and calibration bounds in manuscript notation",
        },
    }


def main() -> None:
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
