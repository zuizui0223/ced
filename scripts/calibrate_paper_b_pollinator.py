"""Literature-informed calibration for Paper B's plant--pollinator example.

The script separates evidence-backed observation parameters from operational
assumptions. It converts single-session field performance into cumulative
screening and response-typing reliability under shared and diversified failure
architectures.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "paper_b_pollinator_calibration.json"


@dataclass(frozen=True)
class Calibration:
    # Field-camera recall reported across realistic pollinator deployments.
    detection_low: float = 0.77
    detection_baseline: float = 0.80
    detection_high: float = 0.83
    # Field classification accuracy spans difficult mixed communities.
    typing_low: float = 0.76
    typing_baseline: float = 0.89
    typing_high: float = 0.95
    screen_replicates: int = 3
    typing_replicates: int = 3
    shared_failure_baseline: float = 0.15
    shared_failure_low: float = 0.05
    shared_failure_high: float = 0.30
    false_resolution_limit: float = 0.05
    screen_cost_units: float = 1.0
    typing_cost_units: float = 4.0


def at_least_one_detection(per_session: float, replicates: int) -> float:
    return 1.0 - (1.0 - per_session) ** replicates


def majority_accuracy(per_replicate: float, replicates: int = 3) -> float:
    if replicates != 3:
        raise ValueError("current calibrated protocol uses three typing replicates")
    q = per_replicate
    return q**3 + 3.0 * q**2 * (1.0 - q)


def calibrated_metrics(c: Calibration = Calibration()) -> dict[str, object]:
    screen = {
        label: at_least_one_detection(value, c.screen_replicates)
        for label, value in {
            "low": c.detection_low,
            "baseline": c.detection_baseline,
            "high": c.detection_high,
        }.items()
    }
    typing = {
        label: majority_accuracy(value, c.typing_replicates)
        for label, value in {
            "low": c.typing_low,
            "baseline": c.typing_baseline,
            "high": c.typing_high,
        }.items()
    }
    shared = {
        "screen_success": (1.0 - c.shared_failure_baseline) * screen["baseline"],
        "joint_target_resolution": (
            (1.0 - c.shared_failure_baseline)
            * screen["baseline"]
            * typing["baseline"]
        ),
    }
    diversified = {
        "screen_success": at_least_one_detection(
            (1.0 - c.shared_failure_baseline) * c.detection_baseline,
            c.screen_replicates,
        ),
        "joint_target_resolution": (
            at_least_one_detection(
                (1.0 - c.shared_failure_baseline) * c.detection_baseline,
                c.screen_replicates,
            )
            * typing["baseline"]
        ),
    }
    return {
        "schema_version": 1,
        "calibration": asdict(c),
        "derived": {
            "cumulative_screen_detection": screen,
            "three_replicate_majority_typing_accuracy": typing,
            "shared_architecture": shared,
            "diversified_architecture": diversified,
            "architecture_gain": diversified["joint_target_resolution"]
            - shared["joint_target_resolution"],
            "baseline_typing_meets_false_resolution_contract": (
                1.0 - typing["baseline"] <= c.false_resolution_limit
            ),
            "single_typing_meets_false_resolution_contract": (
                1.0 - c.typing_baseline <= c.false_resolution_limit
            ),
        },
        "provenance": {
            "detection": "field automated pollinator monitoring recall range",
            "typing": "field classification accuracy range; baseline 0.89",
            "failure": "operational sensitivity assumption, not a literature estimate",
            "costs": "relative protocol units, not monetary estimates",
        },
    }


def main() -> None:
    report = calibrated_metrics()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report["derived"], sort_keys=True))


if __name__ == "__main__":
    main()
