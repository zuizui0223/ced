"""Exact comparative benchmark for target-safe ecological modelling.

The finite scenario represents a generic ecological condition crossed with two
possible intervention-response types. It applies to degradation and recovery,
invasion and controllability, population decline and demographic intervention,
or regime state and reversibility. Manuscript outputs use exact enumeration.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Callable, Iterable

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "paper_b_simulation_summary.json"
OUT_CSV = ROOT / "artifacts" / "paper_b_simulation_grid.csv"
OUT_TEX = ROOT / "artifacts" / "paper_b_simulation_table.tex"

TARGETS = ("condition-absent", "response-A", "response-B")
WORLDS = ((0, 0), (0, 1), (1, 0), (1, 1))


@dataclass(frozen=True)
class Parameters:
    condition_prevalence: float = 0.55
    response_b_probability: float = 0.50
    state_detection_sensitivity: float = 0.80
    response_typing_accuracy: float = 0.85
    common_failure_probability: float = 0.15
    state_observation_cost: float = 1.0
    response_experiment_cost: float = 4.0
    false_resolution_limit: float = 0.05
    observation_replicates: int = 3


def target(world: tuple[int, int]) -> str:
    condition, response_type = world
    if not condition:
        return "condition-absent"
    return "response-B" if response_type else "response-A"


def world_probability(world: tuple[int, int], p: Parameters) -> float:
    condition, response_type = world
    response_prob = p.response_b_probability if response_type else 1.0 - p.response_b_probability
    return (p.condition_prevalence if condition else 1.0 - p.condition_prevalence) * response_prob


def bernoulli_sequences(probability: float, n: int) -> Iterable[tuple[tuple[bool, ...], float]]:
    for values in itertools.product((False, True), repeat=n):
        successes = sum(values)
        yield values, probability**successes * (1.0 - probability) ** (n - successes)


def observation_paths(world: tuple[int, int], p: Parameters, architecture: str):
    condition, response_type = world
    if architecture not in {"shared", "independent"}:
        raise ValueError(f"unknown architecture: {architecture}")

    shared_states = ((False, 1.0),)
    if architecture == "shared":
        shared_states = (
            (False, 1.0 - p.common_failure_probability),
            (True, p.common_failure_probability),
        )

    for shared_failed, p_shared in shared_states:
        if shared_failed:
            detections = (False,) * p.observation_replicates
            yield {"detections": detections, "typed": None}, p_shared
            continue

        sensitivity = p.state_detection_sensitivity
        if architecture == "independent":
            sensitivity *= 1.0 - p.common_failure_probability
        detection_probability = sensitivity if condition else 0.0

        for detections, p_detection in bernoulli_sequences(
            detection_probability, p.observation_replicates
        ):
            if not any(detections):
                yield {"detections": detections, "typed": None}, p_shared * p_detection
                continue
            for correct, p_type in (
                (True, p.response_typing_accuracy),
                (False, 1.0 - p.response_typing_accuracy),
            ):
                typed = response_type if correct else 1 - response_type
                yield {"detections": detections, "typed": typed}, p_shared * p_detection * p_type


def classify(report: set[str], truth: str) -> str:
    if len(report) != 1:
        return "ambiguous"
    return "correct" if next(iter(report)) == truth else "wrong"


def state_only(record: dict[str, object], p: Parameters):
    if bool(record["detections"][0]):
        return {"response-A", "response-B"}, p.state_observation_cost
    return {"condition-absent"}, p.state_observation_cost


def full_identification(record: dict[str, object], p: Parameters):
    if not bool(record["detections"][0]):
        return {"condition-absent"}, p.state_observation_cost
    typed = "response-B" if record["typed"] == 1 else "response-A"
    return {typed}, p.state_observation_cost + p.response_experiment_cost


def information_gain(record: dict[str, object], p: Parameters):
    detections = tuple(bool(value) for value in record["detections"])
    used = next((i + 1 for i, value in enumerate(detections) if value), len(detections))
    if not any(detections):
        prior = {
            "condition-absent": 1.0 - p.condition_prevalence,
            "response-A": p.condition_prevalence * (1.0 - p.response_b_probability),
            "response-B": p.condition_prevalence * p.response_b_probability,
        }
        return {max(prior, key=prior.get)}, used * p.state_observation_cost
    typed = "response-B" if record["typed"] == 1 else "response-A"
    return {typed}, used * p.state_observation_cost + p.response_experiment_cost


def target_safe(record: dict[str, object], p: Parameters):
    detections = tuple(bool(value) for value in record["detections"])
    used = next((i + 1 for i, value in enumerate(detections) if value), len(detections))
    if not any(detections):
        return set(TARGETS), used * p.state_observation_cost
    if 1.0 - p.response_typing_accuracy > p.false_resolution_limit:
        return {"response-A", "response-B"}, used * p.state_observation_cost + p.response_experiment_cost
    typed = "response-B" if record["typed"] == 1 else "response-A"
    return {typed}, used * p.state_observation_cost + p.response_experiment_cost


STRATEGIES: dict[str, Callable] = {
    "state_only": state_only,
    "full_identification": full_identification,
    "information_gain": information_gain,
    "target_safe": target_safe,
}


def evaluate(p: Parameters, architecture: str) -> dict[str, dict[str, float]]:
    totals = {
        name: {"correct": 0.0, "wrong": 0.0, "ambiguous": 0.0, "cost": 0.0}
        for name in STRATEGIES
    }
    for world in WORLDS:
        p_world = world_probability(world, p)
        truth = target(world)
        for record, p_record in observation_paths(world, p, architecture):
            weight = p_world * p_record
            for name, strategy in STRATEGIES.items():
                report, cost = strategy(record, p)
                totals[name][classify(report, truth)] += weight
                totals[name]["cost"] += weight * cost

    return {
        name: {
            "correct_probability": values["correct"],
            "wrong_probability": values["wrong"],
            "ambiguity_probability": values["ambiguous"],
            "expected_cost": values["cost"],
        }
        for name, values in totals.items()
    }


def parameter_grid(base: Parameters = Parameters()):
    for detection, typing, failure in itertools.product(
        (0.60, 0.80, 0.95), (0.85, 0.95, 0.99), (0.00, 0.15, 0.35)
    ):
        yield replace(
            base,
            state_detection_sensitivity=detection,
            response_typing_accuracy=typing,
            common_failure_probability=failure,
        )


def run_grid(base: Parameters = Parameters()) -> dict[str, object]:
    rows = []
    for scenario_id, p in enumerate(parameter_grid(base), start=1):
        for architecture in ("shared", "independent"):
            for strategy, values in evaluate(p, architecture).items():
                rows.append(
                    {
                        "scenario_id": scenario_id,
                        "architecture": architecture,
                        **asdict(p),
                        "strategy": strategy,
                        **values,
                    }
                )

    target_rows = [row for row in rows if row["strategy"] == "target_safe"]
    shared_ceiling = max(
        row["correct_probability"]
        for row in target_rows
        if row["architecture"] == "shared" and row["common_failure_probability"] == 0.35
    )
    independent_best = max(
        row["correct_probability"]
        for row in target_rows
        if row["architecture"] == "independent" and row["common_failure_probability"] == 0.35
    )
    return {
        "schema_version": 3,
        "grid_size": len(rows),
        "rows": rows,
        "headline_checks": {
            "target_safe_max_wrong_probability": max(row["wrong_probability"] for row in target_rows),
            "shared_failure_correct_resolution_ceiling": shared_ceiling,
            "independent_mode_best_correct_resolution": independent_best,
            "independent_modes_break_shared_ceiling": independent_best > shared_ceiling,
        },
    }


def write_outputs(report: dict[str, object]) -> None:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    rows = report["rows"]
    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    baseline = [
        row for row in rows
        if row["architecture"] == "shared"
        and row["state_detection_sensitivity"] == 0.80
        and row["response_typing_accuracy"] == 0.95
        and row["common_failure_probability"] == 0.15
    ]
    lines = [r"\begin{tabular}{lrrrr}", r"\toprule", r"Strategy & Correct & Wrong & Ambiguous & Cost \\", r"\midrule"]
    for row in baseline:
        label = row["strategy"].replace("_", r"\_")
        lines.append(
            f"{label} & {row['correct_probability']:.3f} & {row['wrong_probability']:.3f} & "
            f"{row['ambiguity_probability']:.3f} & {row['expected_cost']:.2f} \\\\"
        )
    lines.extend((r"\bottomrule", r"\end{tabular}"))
    OUT_TEX.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    report = run_grid()
    if not args.no_write:
        write_outputs(report)
    print(json.dumps(report["headline_checks"], sort_keys=True))


if __name__ == "__main__":
    main()
