"""Write a deterministic replay for expected false-discovery budgets."""

from __future__ import annotations

import json
from pathlib import Path

from ced.discovery_budget import FalseDiscoveryBudget
from ced.threshold_detection import ThresholdEvidenceDesign

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts" / "ced_discovery_budget_report.json"


def build_report() -> dict[str, object]:
    per = ThresholdEvidenceDesign(
        read_count=5,
        positive_threshold=3,
        sensitivity_lower_bound=0.7,
        false_positive_upper_bound=0.05,
    )
    budget = FalseDiscoveryBudget(absent_coordinate_count=20, per_coordinate=per)
    if not budget.verify():
        raise AssertionError("discovery-budget witness failed verification")
    return {
        "schema_version": 1,
        "scope": "finite threshold panel with declared absent-coordinate count and per-coordinate false-alert bound",
        "non_claim": "the replay does not control ordinary FDR or infer the number of absent coordinates",
        "per_coordinate": {
            "read_count": per.read_count,
            "positive_threshold": per.positive_threshold,
            "false_alert_probability_upper_bound": round(
                per.false_alert_probability_upper_bound, 12
            ),
        },
        "discovery_budget": {
            "absent_coordinate_count": budget.absent_coordinate_count,
            "expected_false_discoveries_upper_bound": round(
                budget.expected_false_discoveries_upper_bound, 12
            ),
            "probability_at_least_one_false_discovery_upper_bound": round(
                budget.probability_exceeding_false_discovery_budget_upper_bound(1), 12
            ),
            "probability_at_least_two_false_discoveries_upper_bound": round(
                budget.probability_exceeding_false_discovery_budget_upper_bound(2), 12
            ),
            "conditional_expected_false_fraction_if_at_least_five_discoveries": round(
                budget.expected_false_discovery_proportion_upper_bound(5), 12
            ),
        },
    }


def main() -> None:
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
