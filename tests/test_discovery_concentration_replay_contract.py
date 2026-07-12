import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_discovery_concentration.py"


def test_discovery_concentration_replay_matches_declared_witness():
    report = runpy.run_path(str(SCRIPT))["build_report"]()
    assert report == {
        "schema_version": 1,
        "scope": "false-discovery concentration under declared independent alert indicators",
        "non_claim": "the replay does not infer independence, coordinate states, or ordinary FDR control",
        "false_alert_upper_bounds": (0.01, 0.02, 0.03, 0.04, 0.05),
        "expected_false_discoveries_upper_bound": 0.15,
        "budget_2": {
            "exact_independent_tail_upper_bound": 0.008058172,
            "chernoff_tail_upper_bound": 0.035773984815,
            "markov_tail_upper_bound": 0.075,
        },
        "zero_false_discovery_probability_lower_bound": 0.858277728,
    }
