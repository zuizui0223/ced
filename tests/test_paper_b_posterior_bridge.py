import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "analyze_paper_b_posterior_bridge.py"


def test_posterior_sample_bridge_is_stable_and_target_relevant():
    module = runpy.run_path(str(SCRIPT))
    draws = module["generate_draws"]()
    rows = [module["summarize"](draws[:n]) for n in module["SAMPLE_SIZES"]]

    assert [row["posterior_draws"] for row in rows] == [500, 2000, 10000]
    assert all(row["target_safe_choice"] == "response_assay" for row in rows)
    assert all(row["response_assay_resolution_probability"] == 1.0 for row in rows)
    assert all(row["source_trace_resolution_probability"] == 0.0 for row in rows)
    assert abs(rows[-1]["eradication_probability"] - 0.4835) < 1e-12
    assert max(row["eradication_probability"] for row in rows) - min(
        row["eradication_probability"] for row in rows
    ) < 0.02


def test_generated_table_disclaims_empirical_status():
    module = runpy.run_path(str(SCRIPT))
    report = module["run"]()
    table = module["OUT_TEX"].read_text(encoding="utf-8")

    assert report["interpretation"] == "deterministic posterior-sample demonstration, not empirical data"
    assert "Posterior-sample bridge" in table
    assert "10000 & 0.4835 & 1.0000 & 0.0000" in table
