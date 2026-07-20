"""Likelihood-based benchmark for target-safe ecological prediction."""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Callable, Hashable, Iterable

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "paper_b_simulation_summary.json"
OUT_CSV = ROOT / "artifacts" / "paper_b_simulation_grid.csv"
OUT_TEX = ROOT / "artifacts" / "paper_b_simulation_table.tex"
TARGETS = ("condition-absent", "response-A", "response-B")
NUISANCE_STATES = tuple(range(4))
WORLDS = tuple(itertools.product((0, 1), (0, 1), NUISANCE_STATES))
TOL = 1e-12
World = tuple[int, int, int]
Outcome = Hashable
Kernel = Callable[[World], dict[Outcome, float]]


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

    def __post_init__(self) -> None:
        probabilities = (
            self.condition_prevalence,
            self.response_b_probability,
            self.state_detection_sensitivity,
            self.response_typing_accuracy,
            self.common_failure_probability,
            self.false_resolution_limit,
        )
        if any(not 0.0 <= value <= 1.0 for value in probabilities):
            raise ValueError("probability parameters must lie in [0, 1]")
        if self.observation_replicates < 1:
            raise ValueError("observation_replicates must be positive")
        if min(self.state_observation_cost, self.response_experiment_cost, self.nuisance_experiment_cost) < 0.0:
            raise ValueError("experiment costs must be nonnegative")


def target(world: World) -> str:
    condition, response_type, _ = world
    return "condition-absent" if not condition else ("response-B" if response_type else "response-A")


def prior(p: Parameters) -> dict[World, float]:
    result = {}
    for condition, response_type, nuisance in WORLDS:
        condition_mass = p.condition_prevalence if condition else 1.0 - p.condition_prevalence
        response_mass = p.response_b_probability if response_type else 1.0 - p.response_b_probability
        result[(condition, response_type, nuisance)] = condition_mass * response_mass / len(NUISANCE_STATES)
    return result


def normalize(weights: dict[World, float]) -> dict[World, float]:
    total = sum(weights.values())
    if total <= 0.0:
        raise ValueError("posterior has zero mass")
    return {world: value / total for world, value in weights.items() if value > 0.0}


def posterior(belief: dict[World, float], kernel: Kernel, outcome: Outcome) -> dict[World, float]:
    return normalize({world: probability * kernel(world).get(outcome, 0.0) for world, probability in belief.items()})


def entropy(probabilities: Iterable[float]) -> float:
    return -sum(value * math.log2(value) for value in probabilities if value > 0.0)


def predictive_distribution(belief: dict[World, float], kernel: Kernel) -> dict[Outcome, float]:
    result: dict[Outcome, float] = {}
    for world, world_mass in belief.items():
        for outcome, likelihood in kernel(world).items():
            result[outcome] = result.get(outcome, 0.0) + world_mass * likelihood
    return result


def mutual_information(belief: dict[World, float], kernel: Kernel) -> float:
    expected_posterior_entropy = sum(
        outcome_mass * entropy(posterior(belief, kernel, outcome).values())
        for outcome, outcome_mass in predictive_distribution(belief, kernel).items()
        if outcome_mass > 0.0
    )
    return entropy(belief.values()) - expected_posterior_entropy


def response_kernel(p: Parameters) -> Kernel:
    def kernel(world: World) -> dict[Outcome, float]:
        condition, response_type, _ = world
        if not condition:
            return {"not-applicable": 1.0}
        return {response_type: p.response_typing_accuracy, 1 - response_type: 1.0 - p.response_typing_accuracy}
    return kernel


def nuisance_kernel(_: Parameters) -> Kernel:
    return lambda world: {world[2]: 1.0}


def target_masses(belief: dict[World, float]) -> dict[str, float]:
    masses = {label: 0.0 for label in TARGETS}
    for world, probability in belief.items():
        masses[target(world)] += probability
    return masses


def risk_limited_report(belief: dict[World, float], false_resolution_limit: float) -> frozenset[str]:
    masses = target_masses(belief)
    best_target, best_mass = max(masses.items(), key=lambda item: item[1])
    if 1.0 - best_mass <= false_resolution_limit + TOL:
        return frozenset((best_target,))
    return frozenset(label for label, mass in masses.items() if mass > TOL)


def classify(report: frozenset[str], truth: str) -> str:
    if len(report) != 1:
        return "ambiguous"
    return "correct" if next(iter(report)) == truth else "wrong"


def screen_distribution(world: World, p: Parameters, architecture: str) -> dict[tuple[bool, ...], float]:
    condition, _, _ = world
    if architecture not in {"shared", "independent"}:
        raise ValueError(f"unknown architecture: {architecture}")
    result: dict[tuple[bool, ...], float] = {}
    if architecture == "shared":
        operational_mass = 1.0 - p.common_failure_probability
        sensitivity = p.state_detection_sensitivity if condition else 0.0
        result[(False,) * p.observation_replicates] = p.common_failure_probability
    else:
        operational_mass = 1.0
        sensitivity = p.state_detection_sensitivity * (1.0 - p.common_failure_probability) if condition else 0.0
    for values in itertools.product((False, True), repeat=p.observation_replicates):
        successes = sum(values)
        mass = operational_mass * sensitivity**successes * (1.0 - sensitivity) ** (p.observation_replicates - successes)
        result[values] = result.get(values, 0.0) + mass
    return result


def screen_paths(world: World, p: Parameters, architecture: str):
    return screen_distribution(world, p, architecture).items()


def used_screens(detections: tuple[bool, ...]) -> int:
    return next((index + 1 for index, detected in enumerate(detections) if detected), len(detections))


def belief_after_screen(p: Parameters, architecture: str, detections: tuple[bool, ...]) -> dict[World, float]:
    return normalize({
        world: world_mass * screen_distribution(world, p, architecture).get(detections, 0.0)
        for world, world_mass in prior(p).items()
    })


def target_resolution_probability(belief: dict[World, float], kernel: Kernel, limit: float) -> float:
    return sum(
        mass
        for outcome, mass in predictive_distribution(belief, kernel).items()
        if mass > 0.0 and len(risk_limited_report(posterior(belief, kernel, outcome), limit)) == 1
    )


def select_full_world_eig(belief: dict[World, float], experiments: dict[str, tuple[Kernel, float]]) -> str:
    return max(experiments, key=lambda name: (mutual_information(belief, experiments[name][0]), name))


def select_target_safe(belief: dict[World, float], experiments: dict[str, tuple[Kernel, float]], limit: float) -> str | None:
    candidates = []
    for name, (kernel, cost) in experiments.items():
        resolution = target_resolution_probability(belief, kernel, limit)
        if resolution > TOL:
            candidates.append((cost, -resolution, name))
    return min(candidates)[2] if candidates else None


def followup_distribution(world: World, belief: dict[World, float], plan: tuple[tuple[Kernel, float], ...], limit: float):
    states = [(belief, 1.0, 0.0)]
    for kernel, cost in plan:
        next_states = []
        for current_belief, path_mass, path_cost in states:
            for outcome, likelihood in kernel(world).items():
                if likelihood > 0.0:
                    next_states.append((posterior(current_belief, kernel, outcome), path_mass * likelihood, path_cost + cost))
        states = next_states
    for final_belief, path_mass, path_cost in states:
        yield risk_limited_report(final_belief, limit), path_mass, path_cost


def evaluate(p: Parameters, architecture: str) -> dict[str, dict[str, float]]:
    names = ("state_only", "full_identification", "full_world_eig", "target_safe")
    totals = {name: {"correct": 0.0, "wrong": 0.0, "ambiguous": 0.0, "cost": 0.0} for name in names}
    experiments = {
        "response": (response_kernel(p), p.response_experiment_cost),
        "nuisance": (nuisance_kernel(p), p.nuisance_experiment_cost),
    }
    for world, world_mass in prior(p).items():
        truth = target(world)
        for detections, screen_mass in screen_paths(world, p, architecture):
            weight = world_mass * screen_mass
            if weight <= 0.0:
                continue
            screen_cost = used_screens(detections) * p.state_observation_cost
            belief = belief_after_screen(p, architecture, detections)
            if not any(detections):
                report = risk_limited_report(belief, p.false_resolution_limit)
                for name in names:
                    totals[name][classify(report, truth)] += weight
                    totals[name]["cost"] += weight * screen_cost
                continue
            state_report = risk_limited_report(belief, p.false_resolution_limit)
            totals["state_only"][classify(state_report, truth)] += weight
            totals["state_only"]["cost"] += weight * screen_cost
            eig_choice = select_full_world_eig(belief, experiments)
            target_choice = select_target_safe(belief, experiments, p.false_resolution_limit)
            plans = {
                "full_identification": (experiments["response"], experiments["nuisance"]),
                "full_world_eig": (experiments[eig_choice],),
                "target_safe": () if target_choice is None else (experiments[target_choice],),
            }
            for name, plan in plans.items():
                for final_report, followup_mass, followup_cost in followup_distribution(world, belief, plan, p.false_resolution_limit):
                    path_weight = weight * followup_mass
                    totals[name][classify(final_report, truth)] += path_weight
                    totals[name]["cost"] += path_weight * (screen_cost + followup_cost)
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
    for detection, typing, failure in itertools.product((0.60, 0.80, 0.95), (0.85, 0.95, 0.99), (0.00, 0.15, 0.35)):
        yield replace(base, state_detection_sensitivity=detection, response_typing_accuracy=typing, common_failure_probability=failure)


def benchmark_contrast(p: Parameters = Parameters()) -> dict[str, object]:
    belief = normalize({world: mass for world, mass in prior(p).items() if world[0] == 1})
    experiments = {
        "response": (response_kernel(p), p.response_experiment_cost),
        "nuisance": (nuisance_kernel(p), p.nuisance_experiment_cost),
    }
    return {
        "full_world_eig_choice": select_full_world_eig(belief, experiments),
        "target_safe_choice": select_target_safe(belief, experiments, p.false_resolution_limit),
        "full_world_information_gain_bits": {name: mutual_information(belief, kernel) for name, (kernel, _) in experiments.items()},
        "target_resolution_probability": {name: target_resolution_probability(belief, kernel, p.false_resolution_limit) for name, (kernel, _) in experiments.items()},
    }


def run_grid(base: Parameters = Parameters()) -> dict[str, object]:
    rows = []
    for scenario_id, parameters in enumerate(parameter_grid(base), start=1):
        for architecture in ("shared", "independent"):
            for strategy, values in evaluate(parameters, architecture).items():
                rows.append({"scenario_id": scenario_id, "architecture": architecture, **asdict(parameters), "strategy": strategy, **values})
    contrast = benchmark_contrast(base)
    target_rows = [row for row in rows if row["strategy"] == "target_safe"]
    return {
        "schema_version": 5,
        "grid_size": len(rows),
        "rows": rows,
        "benchmark_contrast": contrast,
        "headline_checks": {
            "target_safe_max_wrong_probability": max(row["wrong_probability"] for row in target_rows),
            "full_world_eig_selects_nuisance": contrast["full_world_eig_choice"] == "nuisance",
            "target_safe_selects_response": contrast["target_safe_choice"] == "response",
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
    baseline = [row for row in rows if row["architecture"] == "independent" and row["state_detection_sensitivity"] == 0.80 and row["response_typing_accuracy"] == 0.95 and row["common_failure_probability"] == 0.15]
    lines = [r"\begin{tabular}{lrrrr}", r"\toprule", r"Strategy & Correct & Wrong & Ambiguous & Cost \", r"\midrule"]
    for row in baseline:
        label = row["strategy"].replace("_", r"\_")
        lines.append(f"{label} & {row['correct_probability']:.3f} & {row['wrong_probability']:.3f} & {row['ambiguity_probability']:.3f} & {row['expected_cost']:.2f} \\\")
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
