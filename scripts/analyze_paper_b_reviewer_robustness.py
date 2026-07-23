"""Reviewer-facing robustness analyses for Paper B.

This script demonstrates that the false-resolution limit is a declared reporting
contract rather than a hard-coded 5% property, and that experiment choice changes
when the prediction target changes while worlds and likelihoods remain fixed.
"""
from __future__ import annotations

import json
import runpy
from dataclasses import replace
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "scripts" / "simulate_paper_b_benchmark.py"
OUT_JSON = ROOT / "artifacts" / "paper_b_reviewer_robustness.json"
OUT_THRESHOLD_TEX = ROOT / "manuscript" / "generated" / "paper_b_threshold_sensitivity.tex"
OUT_TARGET_TEX = ROOT / "manuscript" / "generated" / "paper_b_target_switch.tex"
TOL = 1e-12


def _generic_target_masses(belief, target_fn: Callable) -> dict[str, float]:
    masses: dict[str, float] = {}
    for world, probability in belief.items():
        label = target_fn(world)
        masses[label] = masses.get(label, 0.0) + probability
    return masses


def _generic_report(belief, target_fn: Callable, limit: float) -> frozenset[str]:
    masses = _generic_target_masses(belief, target_fn)
    best_label, best_mass = max(masses.items(), key=lambda item: item[1])
    if 1.0 - best_mass <= limit + TOL:
        return frozenset((best_label,))
    return frozenset(label for label, mass in masses.items() if mass > TOL)


def _generic_resolution_probability(module, belief, kernel, target_fn: Callable, limit: float) -> float:
    total = 0.0
    for outcome, mass in module["predictive_distribution"](belief, kernel).items():
        if mass <= 0.0:
            continue
        updated = module["posterior"](belief, kernel, outcome)
        if len(_generic_report(updated, target_fn, limit)) == 1:
            total += mass
    return total


def threshold_sensitivity(module) -> list[dict[str, float]]:
    base = module["Parameters"](
        state_detection_sensitivity=0.95,
        response_typing_accuracy=0.95,
        common_failure_probability=0.0,
    )
    rows = []
    for limit in (0.01, 0.05, 0.10):
        parameters = replace(base, false_resolution_limit=limit)
        metrics = module["evaluate"](parameters, "independent")["target_safe"]
        rows.append({"false_resolution_limit": limit, **metrics})
    return rows


def target_switch(module) -> list[dict[str, object]]:
    parameters = module["Parameters"](
        response_typing_accuracy=0.95,
        common_failure_probability=0.0,
        false_resolution_limit=0.05,
    )
    belief = module["normalize"]({
        world: mass for world, mass in module["prior"](parameters).items() if world[0] == 1
    })
    experiments = {
        "response": module["response_kernel"](parameters),
        "nuisance": module["nuisance_kernel"](parameters),
    }
    targets = {
        "management response": lambda world: "response-B" if world[1] else "response-A",
        "context classification": lambda world: f"context-{world[2]}",
    }
    rows = []
    for target_name, target_fn in targets.items():
        resolutions = {
            name: _generic_resolution_probability(
                module, belief, kernel, target_fn, parameters.false_resolution_limit
            )
            for name, kernel in experiments.items()
        }
        choice = max(resolutions, key=lambda name: (resolutions[name], name))
        rows.append({"target": target_name, "target_safe_choice": choice, **resolutions})
    return rows


def threshold_table_tex(rows: list[dict[str, float]]) -> str:
    body = []
    for row in rows:
        body.append(
            f"{row['false_resolution_limit']:.2f} & "
            f"{row['correct_probability']:.3f} & {row['wrong_probability']:.3f} & "
            f"{row['ambiguity_probability']:.3f} & {row['expected_cost']:.3f} \\\\" 
        )
    return "\n".join([
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"False-resolution limit & Correct & Wrong & Ambiguous & Cost \\",
        r"\midrule",
        *body,
        r"\bottomrule",
        r"\end{tabular}",
        "",
    ])


def target_switch_table_tex(rows: list[dict[str, object]]) -> str:
    body = []
    for row in rows:
        target = str(row["target"]).replace(" ", r"\ ")
        body.append(
            f"{target} & {row['response']:.3f} & {row['nuisance']:.3f} & "
            f"{row['target_safe_choice']} \\\\" 
        )
    return "\n".join([
        r"\begin{tabular}{lrrl}",
        r"\toprule",
        r"Declared target & Response experiment & Context experiment & Selected \\",
        r"\midrule",
        *body,
        r"\bottomrule",
        r"\end{tabular}",
        "",
    ])


def run() -> dict[str, object]:
    module = runpy.run_path(str(BENCHMARK))
    report = {
        "schema_version": 1,
        "threshold_sensitivity": threshold_sensitivity(module),
        "target_switch": target_switch(module),
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_THRESHOLD_TEX.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    OUT_THRESHOLD_TEX.write_text(
        threshold_table_tex(report["threshold_sensitivity"]), encoding="utf-8"
    )
    OUT_TARGET_TEX.write_text(target_switch_table_tex(report["target_switch"]), encoding="utf-8")
    return report


def main() -> None:
    report = run()
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
