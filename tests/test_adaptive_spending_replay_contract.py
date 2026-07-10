import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_adaptive_spending.py"


def test_adaptive_spending_replay_matches_declared_witness():
    report = runpy.run_path(str(SCRIPT))["build_report"]()
    assert report["schema_version"] == 1
    assert report["spends"] == [
        {"coordinate": 0, "alpha": 0.005, "mode": "camera-a", "label": "screen"},
        {"coordinate": 1, "alpha": 0.01, "mode": "camera-b", "label": "screen"},
        {"coordinate": 0, "alpha": 0.002, "mode": "camera-c", "label": "confirm"},
        {"coordinate": 2, "alpha": 0.003, "mode": "camera-a", "label": "screen"},
    ]
    assert report["ledger_bounds"] == {
        "coordinate_count": 3,
        "spend_count": 4,
        "total_spent_alpha": 0.02,
        "familywise_false_alert_upper_bound": 0.02,
        "expected_false_alerts_upper_bound": 0.02,
        "per_coordinate_spent_alpha": (0.007, 0.01, 0.003),
        "prefix_familywise_false_alert_upper_bounds": (0.005, 0.015, 0.017, 0.02),
        "weighted_false_alert_budget_1_2_5": 0.042,
        "remaining_alpha_budget_at_0_05": 0.03,
        "within_total_budget_0_025": True,
    }
