"""Replay the integrated pollinator management decision tree."""

from __future__ import annotations

import json
from pathlib import Path

from ced.adaptive_target_policy import (
    AdaptiveTargetBranch,
    AdaptiveTargetPolicy,
    cheapest_feasible_policy,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts" / "ced_pollinator_adaptive_policy_report.json"
TARGETS = ("absent", "decrease", "increase")
TRUE_TARGET = "decrease"


def _typing_node(name: str, decrease: float, increase: float, ambiguous: float) -> AdaptiveTargetPolicy:
    return AdaptiveTargetPolicy(
        name=name,
        experiment_cost=2.0,
        branches=(
            AdaptiveTargetBranch("decrease", decrease, AdaptiveTargetPolicy.stop(f"{name}-decrease", ("decrease",))),
            AdaptiveTargetBranch("increase", increase, AdaptiveTargetPolicy.stop(f"{name}-increase", ("increase",))),
            AdaptiveTargetBranch("uncertain", ambiguous, AdaptiveTargetPolicy.stop(f"{name}-ambiguous", ("decrease", "increase"))),
        ),
    )


def _policy(name: str, present: float, absent: float, uncertain: float, typing: tuple[float, float, float]) -> AdaptiveTargetPolicy:
    return AdaptiveTargetPolicy(
        name=name,
        experiment_cost=1.0,
        branches=(
            AdaptiveTargetBranch("present", present, _typing_node(f"{name}-typing", *typing)),
            AdaptiveTargetBranch("absent", absent, AdaptiveTargetPolicy.stop(f"{name}-absent", ("absent",))),
            AdaptiveTargetBranch("uncertain", uncertain, AdaptiveTargetPolicy.stop(f"{name}-uncertain", TARGETS)),
        ),
    )


def build_policies() -> tuple[AdaptiveTargetPolicy, ...]:
    return (
        _policy("shared", 0.75, 0.05, 0.20, (0.80, 0.03, 0.17)),
        _policy("overlapping", 0.85, 0.03, 0.12, (0.90, 0.025, 0.075)),
        _policy("independent", 0.93, 0.02, 0.05, (0.96, 0.015, 0.025)),
    )


def build_report() -> dict[str, object]:
    policies = build_policies()
    selected = cheapest_feasible_policy(
        policies,
        TRUE_TARGET,
        minimum_correct=0.85,
        maximum_wrong=0.04,
        maximum_expected_cost=3.0,
    )
    return {
        "schema_version": 1,
        "ecological_question": "after detecting a pollinator interaction channel, should monitoring stop or perform a response-typing intervention before reporting management direction?",
        "true_target": TRUE_TARGET,
        "policies": [
            {
                "name": policy.name,
                "expected_cost": round(policy.expected_total_cost, 12),
                "correct": round(policy.correct_probability(TRUE_TARGET), 12),
                "wrong": round(policy.wrong_probability(TRUE_TARGET), 12),
                "ambiguous": round(policy.ambiguity_probability(TRUE_TARGET), 12),
                "terminal_distribution": [
                    {"targets": sorted(targets), "probability": round(probability, 12)}
                    for targets, probability in policy.terminal_distribution()
                ],
            }
            for policy in policies
        ],
        "selection_contract": {
            "minimum_correct": 0.85,
            "maximum_wrong": 0.04,
            "maximum_expected_cost": 3.0,
        },
        "selected_policy": selected.name if selected else None,
        "interpretation": "failure diversity can justify an adaptive response intervention under a finite expected-cost budget when shared modes cannot meet the report-risk contract",
    }


def main() -> None:
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
