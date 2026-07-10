"""Write a deterministic replay for adaptive alpha spending."""

from __future__ import annotations

import json
from pathlib import Path

from ced.adaptive_spending import AdaptiveAlphaSpend, AdaptiveAlphaSpendingLedger

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts" / "ced_adaptive_spending_report.json"


def build_ledger() -> AdaptiveAlphaSpendingLedger:
    return AdaptiveAlphaSpendingLedger(
        3,
        (
            AdaptiveAlphaSpend(0, 0.005, mode="camera-a", label="screen"),
            AdaptiveAlphaSpend(1, 0.010, mode="camera-b", label="screen"),
            AdaptiveAlphaSpend(0, 0.002, mode="camera-c", label="confirm"),
            AdaptiveAlphaSpend(2, 0.003, mode="camera-a", label="screen"),
        ),
    )


def build_report() -> dict[str, object]:
    ledger = build_ledger()
    if not ledger.verify():
        raise AssertionError("adaptive-spending witness failed verification")
    return {
        "schema_version": 1,
        "scope": "adaptive allocation false-alert risk accounting by alpha spending",
        "non_claim": "the replay does not infer policy optimality, detection power, error rates, or posterior probabilities",
        "spends": [
            {
                "coordinate": spend.coordinate,
                "alpha": spend.alpha,
                "mode": spend.mode,
                "label": spend.label,
            }
            for spend in ledger.spends
        ],
        "ledger_bounds": {
            "coordinate_count": ledger.coordinate_count,
            "spend_count": ledger.spend_count,
            "total_spent_alpha": round(ledger.total_spent_alpha, 12),
            "familywise_false_alert_upper_bound": round(
                ledger.familywise_false_alert_upper_bound, 12
            ),
            "expected_false_alerts_upper_bound": round(
                ledger.expected_false_alerts_upper_bound, 12
            ),
            "per_coordinate_spent_alpha": tuple(
                round(value, 12) for value in ledger.per_coordinate_spent_alpha
            ),
            "prefix_familywise_false_alert_upper_bounds": tuple(
                round(value, 12)
                for value in ledger.prefix_familywise_false_alert_upper_bounds
            ),
            "weighted_false_alert_budget_1_2_5": round(
                ledger.weighted_false_alert_budget_upper_bound((1, 2, 5)), 12
            ),
            "remaining_alpha_budget_at_0_05": round(
                ledger.remaining_alpha_budget(0.05), 12
            ),
            "within_total_budget_0_025": ledger.within_total_budget(0.025),
        },
    }


def main() -> None:
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
