"""Write a deterministic replay for independent false-discovery concentration."""

from __future__ import annotations

import json
from pathlib import Path

from ced.discovery_concentration import IndependentFalseDiscoveryConcentration

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts" / "ced_discovery_concentration_report.json"


def build_report() -> dict[str, object]:
    design = IndependentFalseDiscoveryConcentration((0.01, 0.02, 0.03, 0.04, 0.05))
    if not design.verify():
        raise AssertionError("discovery-concentration witness failed verification")
    return {
        "schema_version": 1,
        "scope": "false-discovery concentration under declared independent alert indicators",
        "non_claim": "the replay does not infer independence, coordinate states, or ordinary FDR control",
        "false_alert_upper_bounds": design.false_alert_upper_bounds,
        "expected_false_discoveries_upper_bound": round(
            design.expected_false_discoveries_upper_bound, 12
        ),
        "budget_2": {
            "exact_independent_tail_upper_bound": round(
                design.exact_independent_tail_upper_bound(2), 12
            ),
            "chernoff_tail_upper_bound": round(design.chernoff_tail_upper_bound(2), 12),
            "markov_tail_upper_bound": round(design.markov_tail_upper_bound(2), 12),
        },
        "zero_false_discovery_probability_lower_bound": round(
            design.exact_zero_false_discovery_probability_lower_bound(), 12
        ),
    }


def main() -> None:
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
