"""Exact benchmark for target-safe ecological prediction.

The latent world contains current condition, intervention-response type, and a
four-level attribute irrelevant to the declared prediction target. Expected
information gain is computed on the full world; target-safe design values only
splits that change the declared ecological prediction.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "paper_b_simulation_summary.json"
OUT_CSV = ROOT / "artifacts" / "paper_b_simulation_grid.csv"
OUT_TEX = ROOT / "artifacts" / "paper_b_simulation_table.tex"

TARGETS = ("condition-absent", "response-A", "response-B")
NUISANCE_STATES = tuple(range(4))
WORLDS = tuple(itertools.product((0, 1), (0, 1), NUISANCE_STATES))


@dataclass(frozen=True)
class Parameters:
    condition_prevalence: float = 0.55
    response_b_probability: float = 0.50
    state_detection_sensitivity: float = 0.80
    response_typing_accuracy: float = 0.95
    common_failure_probability: float = 0.15
    state_observation_cost: float = 1.0
    response_experiment_cost: float = 4.0
    nuisance_experiment_cost: float = 1.0
    false_resolution_limit: float = 0.05
    observation_replicates: int = 3


def target(world: tuple[int, int, int]) -> str:
    condition, response_type, _ = world
    if not condition:
        return "condition-absent"
    return "response-B" if response_type else "response-A"


def world_probability(world: tuple[int, int, int], p: Parameters) -> float:
    condition, response_type, _ = world
    response_prob = p.response_b_probability if response_type else 1.0 - p.response_b_probability
    condition_prob = p.condition_prevalence if condition else 1.0 - p.condition_prevalence
    return condition_prob * response_prob / len(NUISANCE_STATES)


def bernoulli_sequences(probability: float, n: int) -> Iterable[tuple[tuple[bool, ...], float]]:
    for values in itertools.product((False, True), repeat=n):
        successes = sum(values)
        yield values, probability**successes * (1.0 - probability) ** (n - successes)


def observation_paths(world: tuple[int, int, int], p: Parameters, architecture: str):
    condition, response_type, nuisance = world
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
            yield {
                "detections": (False,) * p.observation_replicates,
                "response_typed": None,
                "nuisance_observed": None,
            }, p_shared
            continue

        sensitivity = p.state_detection_sensitivity
        if architecture == "independent":
            sensitivity *= 1.0 - p.common_failure_probability
        detection_probability = sensitivity if condition else 0.0

        for detections, p_detection in bernoulli_sequences(
            detection_probability, p.observation_replicates
        ):
            if not any(detections):
                yield {
                    "detections": detections,
                    "response_typed": None,
                    "nuisance_observed": nuisance,
                }, p_shared * p_detection
                continue
            for correct, p_type in (
                (True, p.response_typing_accuracy),
                (False, 1.0 - p.response_typing_accuracy),
            ):
                yield {
                    "detections": detections,
                    "response_typed": response_type if correct else 1 - response_type,
                    "nuisance_observed": nuisance,
                }, p_shared * p_detection * p_type


def classify(report: set[str], truth: str) -> str:
    if len(report) != 1:
        return "ambiguous"
    return "correct" if next(iter(report)) == truth else "wrong"


def used_observations(record: dict[str, object]) -> int:
    detections = tuple(bool(value) for value in record["detections"])
    return next((i + 1 for i, value in enumerate(detections) if value), len(detections))


def state_only(record: dict[str, object], p: Parameters):
    if bool(record["detections"][0]):
        return {"response-A", "response-B"}, p.state_observation_cost
    return {"condition-absent"}, p.state_observation_cost


def full_identification(record: dict[str, object], p: Parameters):
    used = used_observations(record)
    if not any(record["detections"]):
        return {"condition-absent"}, used * p.state_observation_cost
    typed = "response-B" if record["response_typed"] == 1 else "response-A"
    cost = used * p.state_observation_cost + p.response_experiment_cost + p.nuisance_experiment_cost
    return {typed}, cost


def entropy(probabilities: Iterable[float]) -> float:
    return -sum(value * math.log2(value) for value in probabilities if value > 0.0)


def expected_information_gain(p: Parameters) -> dict[str, float]:
    response_prior = (1.0 - p.response_b_probability, p.response_b_probability)
    response_posterior_entropy = entropy(
        (p.response_typing_accuracy, 1.0 - p.response_typing_accuracy)
    )
    return {
        "response_experiment": entropy(response_prior) - response_posterior_entropy,
        "nuisance_experiment": math.log2(len(NUISANCE_STATES)),
    }


def information_gain(record: dict[str, object], p: Parameters):
    used = used_observations(record)
    if not any(record["detections"]):
        return set(TARGETS), used * p.state_observation_cost
    gains = expected_information_gain(p)
    selected = max(gains, key=gains.get)
    if selected != "nuisance_experiment":
        raise AssertionError("benchmark requires full-world EIG to favor the target-irrelevant experiment")
    return {"response-A", "response-B"}, used * p.state_observation_cost + p.nuisance_experiment_cost


def target_safe(record: dict[str, object], p: Parameters):
    used = used_observations(record)
    if not any(record["detections"]):
        return set(TARGETS), used * p.state_observation_cost
    if 1.0 - p.response_typing_accuracy > p.false_resolution_limit:
        return {"response-A", "response-B"}, used * p.state_observation_cost + p.response_experiment_cost
    typed = "response-B" if record["response_typed"] == 1 else "response-A"
    return {typed}, used * p.state_observation_cost + p.response_experiment_cost


STRATEGIES = {
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
                rows.append({
                    "scenario_id": scenario_id,
                    "architecture": architecture,
                    **asdict(p),
                    "strategy": strategy,
                    **values,
                })

    target_rows = [row for row in rows if row["strategy"] == "target_safe"]
    aligned = evaluate(
        replace(base, response_typing_accuracy=0.99, common_failure_probability=0.0),
        "independent",
    )
    gains = expected_information_gain(base)
    return {
        "schema_version": 4,
        "grid_size": len(rows),
        "rows": rows,
        "headline_checks": {
            "target_safe_max_wrong_probability": max(row["wrong_probability"] for row in target_rows),
            "information_gain_selects_target_irrelevant_experiment": (
                gains["nuisance_experiment"] > gains["response_experiment"]
            ),
            "nuisance_information_gain_bits": gains["nuisance_experiment"],
            "response_information_gain_bits": gains["response_experiment"],
            "target_safe_more_resolving_than_information_gain": (
                aligned["target_safe"]["correct_probability"]
                > aligned["information_gain"]["correct_probability"]
            ),
            "target_safe_cheaper_than_full_identification": (
                aligned["target_safe"]["expected_cost"]
                < aligned["full_identification"]["expected_cost"]
            ),
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
        if row["architecture"] == "independent"
        and row["state_detection_sensitivity"] == 0.80
        and row["response_typing_accuracy"] == 0.99
        and row["common_failure_probability"] == 0.15
    ]
    lines = [
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Strategy & Correct & Wrong & Ambiguous & Cost \\",
        r"\midrule",
    ]
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
