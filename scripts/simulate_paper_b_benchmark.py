"""Comparative simulation for Paper B.

The benchmark contrasts four reporting/design rules on the same finite
plant--pollinator evidence problem. It intentionally uses only the Python
standard library so that the manuscript result is easy to replay.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "paper_b_simulation_summary.json"
OUT_CSV = ROOT / "artifacts" / "paper_b_simulation_summary.csv"

TARGETS = ("absent", "decrease", "increase")
WORLDS = ((0, 0), (0, 1), (1, 0), (1, 1))


@dataclass(frozen=True)
class Parameters:
    prevalence: float = 0.55
    response_increase_probability: float = 0.5
    detection_sensitivity: float = 0.80
    intervention_sensitivity: float = 0.85
    common_failure_probability: float = 0.15
    screen_cost: float = 1.0
    intervention_cost: float = 4.0
    false_resolution_limit: float = 0.05


def target(world: tuple[int, int]) -> str:
    presence, response = world
    if not presence:
        return "absent"
    return "increase" if response else "decrease"


def draw_world(rng: random.Random, p: Parameters) -> tuple[int, int]:
    presence = int(rng.random() < p.prevalence)
    response = int(rng.random() < p.response_increase_probability)
    return presence, response


def draw_record(rng: random.Random, world: tuple[int, int], p: Parameters) -> dict[str, object]:
    shared_failure = rng.random() < p.common_failure_probability
    presence, response = world
    detected = False if shared_failure else bool(presence and rng.random() < p.detection_sensitivity)
    typed = None
    if detected:
        typed = response if rng.random() < p.intervention_sensitivity else 1 - response
    return {"shared_failure": shared_failure, "detected": detected, "typed": typed}


def classify(report: set[str], truth: str) -> str:
    if len(report) > 1:
        return "ambiguous"
    return "correct" if next(iter(report)) == truth else "wrong"


def occupancy_only(record: dict[str, object], p: Parameters) -> tuple[set[str], float]:
    if not record["detected"]:
        return {"absent"}, p.screen_cost
    majority = "increase" if p.response_increase_probability >= 0.5 else "decrease"
    return {majority}, p.screen_cost


def full_identification(record: dict[str, object], p: Parameters) -> tuple[set[str], float]:
    if not record["detected"]:
        return {"absent"}, p.screen_cost
    typed = "increase" if record["typed"] == 1 else "decrease"
    return {typed}, p.screen_cost + p.intervention_cost


def information_gain(record: dict[str, object], p: Parameters) -> tuple[set[str], float]:
    # In this four-world example entropy reduction always favors response typing
    # after detection, even when the user's target could already be reported as a set.
    return full_identification(record, p)


def target_safe(record: dict[str, object], p: Parameters) -> tuple[set[str], float]:
    if record["shared_failure"]:
        return {"absent", "decrease", "increase"}, p.screen_cost
    if not record["detected"]:
        # A nondetection cannot safely establish absence under imperfect detection.
        return {"absent", "decrease", "increase"}, p.screen_cost
    typing_error = 1.0 - p.intervention_sensitivity
    if typing_error > p.false_resolution_limit:
        return {"decrease", "increase"}, p.screen_cost + p.intervention_cost
    typed = "increase" if record["typed"] == 1 else "decrease"
    return {typed}, p.screen_cost + p.intervention_cost


STRATEGIES = {
    "occupancy_only": occupancy_only,
    "full_identification": full_identification,
    "information_gain": information_gain,
    "target_safe": target_safe,
}


def run(n: int = 20_000, seed: int = 20260718, p: Parameters = Parameters()) -> dict[str, object]:
    rng = random.Random(seed)
    counts = {name: Counter() for name in STRATEGIES}
    costs = Counter()
    for _ in range(n):
        world = draw_world(rng, p)
        truth = target(world)
        record = draw_record(rng, world, p)
        for name, strategy in STRATEGIES.items():
            report, cost = strategy(record, p)
            counts[name][classify(report, truth)] += 1
            costs[name] += cost

    strategies = {}
    for name in STRATEGIES:
        strategies[name] = {
            "correct_probability": counts[name]["correct"] / n,
            "wrong_probability": counts[name]["wrong"] / n,
            "ambiguity_probability": counts[name]["ambiguous"] / n,
            "expected_cost": costs[name] / n,
        }
    return {
        "schema_version": 1,
        "seed": seed,
        "n": n,
        "parameters": p.__dict__,
        "strategies": strategies,
        "interpretation": {
            "occupancy_boundary": "presence-oriented reporting can force a response conclusion not supported by the record",
            "partial_identification_boundary": "target_safe preserves an exact set-valued output rather than selecting a best world",
            "adaptive_monitoring_boundary": "the stopping rule is constrained by target false-resolution rather than generic information gain",
            "failure_boundary": "shared failure returns ambiguity and prevents nominal replication from being treated as independent resolution",
        },
    }


def write_outputs(report: dict[str, object]) -> None:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("strategy", "correct_probability", "wrong_probability", "ambiguity_probability", "expected_cost"),
        )
        writer.writeheader()
        for strategy, metrics in report["strategies"].items():
            writer.writerow({"strategy": strategy, **metrics})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=20_000)
    parser.add_argument("--seed", type=int, default=20260718)
    args = parser.parse_args()
    report = run(n=args.n, seed=args.seed)
    write_outputs(report)
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
