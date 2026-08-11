"""Quantitative harvest of the non-substitution results in the failure architecture.

The manuscript currently carries the failure-architecture material as one
qualitative proposition. The machinery in ``ced.mode_detection`` and
``ced.overlapping_modes`` supports considerably sharper statements, which this
script extracts as exact finite numbers.

Five harvests are produced.

``saturation``
    Within a fixed failure-mode structure, joint detection saturates at the
    availability ceiling ``1 - (1 - a) ** m``. Additional reads inside the same
    modes approach it and never cross it.

``mode_floor``
    The ceiling inverts into a necessary condition on design structure: a target
    joint confidence ``c`` cannot be reached by any read budget unless the design
    already contains at least ``ceil(log(1 - c) / log(1 - a))`` independent modes.

``allocation``
    Holding total reads fixed and varying only their allocation across modes
    changes the guarantee. Effort is not a sufficient statistic for evidence.

``sharing``
    The discriminating experiment. Modes are interpolated from fully independent
    to fully sharing one latent factor while every other quantity is held fixed.
    If the ceiling itself moves, replication cannot buy back what sharing costs,
    and the two resources are non-substitutable rather than merely differently
    priced.

``horizon``
    The same question for a second resource pair. Increasing the delay in the
    delayed-exposure family moves the revealing horizon without moving the
    interface memory gap at all, so temporal effort and representational
    capacity are not exchangeable either.

All quantities are exact under the declared factor-independence and
conditional read-independence contracts. Nothing here is inferred from data.
"""

from __future__ import annotations

import json
from pathlib import Path

from ced.delayed import DelayedExposureFamily
from ced.detection import OneSidedDetector
from ced.mode_detection import ModeDiverseDetectionPanel
from ced.overlapping_modes import OverlappingFailureModePanel

COORDINATE_COUNT = 3
SENSITIVITY = 0.6
AVAILABILITY = 0.8


def _panel(mode_count: int, repetitions: int) -> ModeDiverseDetectionPanel:
    return ModeDiverseDetectionPanel(
        coordinate_count=COORDINATE_COUNT,
        mode_count=mode_count,
        repetitions_per_mode=repetitions,
        availability_lower_bound=AVAILABILITY,
        detector=OneSidedDetector(sensitivity_lower_bound=SENSITIVITY),
    )


def harvest_saturation() -> list[dict[str, object]]:
    """Reads inside a fixed mode structure approach the ceiling and stop."""
    rows: list[dict[str, object]] = []
    for mode_count in (1, 2, 3):
        for repetitions in (1, 2, 5, 10, 100, 1000):
            panel = _panel(mode_count, repetitions)
            rows.append(
                {
                    "mode_count": mode_count,
                    "repetitions_per_mode": repetitions,
                    "total_reads": panel.total_reads,
                    "joint_detection_lower_bound": panel.joint_detection_lower_bound,
                    "availability_ceiling": panel.availability_ceiling,
                    "gap_to_ceiling": panel.availability_ceiling
                    - panel.joint_detection_lower_bound,
                }
            )
    return rows


def harvest_mode_floor() -> list[dict[str, object]]:
    """A confidence target is a structural requirement before it is an effort one."""
    rows: list[dict[str, object]] = []
    for availability in (0.5, 0.8, 0.95):
        for confidence in (0.9, 0.95, 0.99, 0.999):
            floor = ModeDiverseDetectionPanel.minimum_mode_count_for_availability_ceiling(
                availability, confidence
            )
            rows.append(
                {
                    "availability_lower_bound": availability,
                    "target_confidence": confidence,
                    "necessary_mode_count": floor,
                    "ceiling_at_floor": 1.0 - (1.0 - availability) ** floor,
                }
            )
    return rows


def harvest_allocation(total_reads: int = 30) -> list[dict[str, object]]:
    """Same total effort, different failure diversity, different guarantee."""
    rows: list[dict[str, object]] = []
    for mode_count in (1, 2, 3, 5, 6):
        repetitions, remainder = divmod(total_reads, mode_count * COORDINATE_COUNT)
        if repetitions < 1 or remainder:
            continue
        panel = _panel(mode_count, repetitions)
        rows.append(
            {
                "mode_count": mode_count,
                "repetitions_per_mode": repetitions,
                "total_reads": panel.total_reads,
                "joint_detection_lower_bound": panel.joint_detection_lower_bound,
                "availability_ceiling": panel.availability_ceiling,
            }
        )
    return rows


def _sharing_panel(
    mode_count: int,
    sharing_degree: int,
    repetitions: int,
    private_failure: float,
    shared_failure: float,
) -> OverlappingFailureModePanel:
    """Modes with one private factor each; the first ``sharing_degree`` also share one.

    ``sharing_degree == 0`` is the fully independent design and
    ``sharing_degree == mode_count`` makes every mode depend on the same extra
    latent factor. Read effort, sensitivity, and the private factors are
    identical across the whole sweep, so any movement is attributable to sharing.
    """
    shared_index = mode_count
    probabilities = tuple([private_failure] * mode_count + [shared_failure])
    mode_factor_sets = tuple(
        frozenset({mode} | ({shared_index} if mode < sharing_degree else set()))
        for mode in range(mode_count)
    )
    return OverlappingFailureModePanel(
        coordinate_count=COORDINATE_COUNT,
        repetitions_per_coordinate_per_mode=repetitions,
        sensitivity_lower_bound=SENSITIVITY,
        factor_failure_probabilities=probabilities,
        mode_factor_sets=mode_factor_sets,
    )


def harvest_sharing(
    mode_count: int = 4,
    private_failure: float = 0.2,
    shared_failure: float = 0.2,
) -> list[dict[str, object]]:
    """Does replication compensate for shared failure, or is the ceiling moved?"""
    rows: list[dict[str, object]] = []
    for sharing_degree in range(mode_count + 1):
        entry: dict[str, object] = {
            "sharing_degree": sharing_degree,
            "modes_on_shared_factor": sharing_degree,
        }
        for repetitions in (2, 10, 1000):
            panel = _sharing_panel(
                mode_count,
                sharing_degree,
                repetitions,
                private_failure,
                shared_failure,
            )
            entry[f"joint_lb_r{repetitions}"] = panel.joint_detection_probability_lower_bound
            entry["availability_ceiling"] = panel.availability_ceiling
            entry["all_modes_failed"] = panel.all_modes_failed_probability
        rows.append(entry)
    return rows


def harvest_horizon() -> list[dict[str, object]]:
    """Interface memory and revealing horizon move independently.

    The delayed-exposure family separates how much exact memory an open
    interface needs from how long a legal trace must be before any of it can be
    observed. Holding the port count fixed and increasing the delay leaves the
    memory gap untouched while pushing the revealing horizon arbitrarily far, so
    no finite horizon chosen in advance is adequate for the whole family.
    """
    rows: list[dict[str, object]] = []
    for module_count in (1, 2, 4):
        for delay in (0, 1, 5, 50):
            family = DelayedExposureFamily(module_count=module_count, delay=delay)
            rows.append(
                {
                    "module_count": module_count,
                    "delay": delay,
                    "revealing_horizon": family.revealing_horizon,
                    "closed_interface_bits": family.closed_interface_bits,
                    "open_interface_bits": family.open_interface_bits,
                    "memory_gap_bits": family.open_interface_bits
                    - family.closed_interface_bits,
                    "blind_through_prior_horizon": family.is_exterior_blind_through(
                        family.revealing_horizon - 1
                    ),
                }
            )
    return rows


def main() -> dict[str, object]:
    saturation = harvest_saturation()
    mode_floor = harvest_mode_floor()
    allocation = harvest_allocation()
    sharing = harvest_sharing()
    horizon = harvest_horizon()

    independent = sharing[0]
    fully_shared = sharing[-1]
    ceiling_loss = float(independent["availability_ceiling"]) - float(
        fully_shared["availability_ceiling"]
    )
    # Best case for replication: unlimited reads under full sharing.
    unlimited_reads_shared = float(fully_shared["joint_lb_r1000"])
    modest_reads_independent = float(independent["joint_lb_r2"])

    report = {
        "schema_version": 1,
        "contract": {
            "coordinate_count": COORDINATE_COUNT,
            "sensitivity_lower_bound": SENSITIVITY,
            "availability_lower_bound": AVAILABILITY,
        },
        "saturation": saturation,
        "mode_floor": mode_floor,
        "allocation": allocation,
        "sharing": sharing,
        "horizon": horizon,
        "findings": {
            "ceiling_loss_from_full_sharing": ceiling_loss,
            "unlimited_reads_under_full_sharing": unlimited_reads_shared,
            "two_reads_under_independence": modest_reads_independent,
            "replication_cannot_recover_sharing": unlimited_reads_shared
            < modest_reads_independent,
        },
    }

    destination = Path("artifacts") / "nonsubstitution_harvest.json"
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    main()
