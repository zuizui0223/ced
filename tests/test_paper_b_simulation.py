import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "simulate_paper_b_benchmark.py"


def test_paper_b_benchmark_is_reproducible_and_target_safe_is_honest():
    module = runpy.run_path(str(SCRIPT))
    report = module["run"](n=5000, seed=7)
    strategies = report["strategies"]

    assert report["schema_version"] == 1
    assert set(strategies) == {
        "occupancy_only",
        "full_identification",
        "information_gain",
        "target_safe",
    }
    for metrics in strategies.values():
        total = (
            metrics["correct_probability"]
            + metrics["wrong_probability"]
            + metrics["ambiguity_probability"]
        )
        assert abs(total - 1.0) < 1e-12

    assert strategies["target_safe"]["wrong_probability"] == 0.0
    assert strategies["target_safe"]["ambiguity_probability"] > 0.0
    assert strategies["occupancy_only"]["wrong_probability"] > 0.0
    assert strategies["full_identification"]["expected_cost"] >= strategies["target_safe"]["expected_cost"]
