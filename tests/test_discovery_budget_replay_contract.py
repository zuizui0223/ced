import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_discovery_budget.py"


def test_discovery_budget_replay_matches_declared_witness():
    report = runpy.run_path(str(SCRIPT))["build_report"]()
    assert report["schema_version"] == 1
    assert report["per_coordinate"] == {
        "read_count": 5,
        "positive_threshold": 3,
        "false_alert_probability_upper_bound": 0.001158125,
    }
    assert report["discovery_budget"] == {
        "absent_coordinate_count": 20,
        "expected_false_discoveries_upper_bound": 0.0231625,
        "probability_at_least_one_false_discovery_upper_bound": 0.0231625,
        "probability_at_least_two_false_discoveries_upper_bound": 0.01158125,
        "conditional_expected_false_fraction_if_at_least_five_discoveries": 0.0046325,
    }
