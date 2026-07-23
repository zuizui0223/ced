import runpy
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "analyze_paper_b_reviewer_robustness.py"


def test_target_choice_changes_with_declared_target():
    module = runpy.run_path(str(SCRIPT))
    benchmark = runpy.run_path(str(module["BENCHMARK"]))
    rows = {row["target"]: row for row in module["target_switch"](benchmark)}

    assert rows["management response"]["target_safe_choice"] == "response"
    assert rows["management response"]["response"] == pytest.approx(1.0)
    assert rows["management response"]["nuisance"] == pytest.approx(0.0)
    assert rows["context classification"]["target_safe_choice"] == "nuisance"
    assert rows["context classification"]["response"] == pytest.approx(0.0)
    assert rows["context classification"]["nuisance"] == pytest.approx(1.0)


def test_false_resolution_limit_controls_abstention_and_not_a_fixed_five_percent_rule():
    module = runpy.run_path(str(SCRIPT))
    benchmark = runpy.run_path(str(module["BENCHMARK"]))
    rows = {
        row["false_resolution_limit"]: row
        for row in module["threshold_sensitivity"](benchmark)
    }

    assert rows[0.01]["ambiguity_probability"] > rows[0.05]["ambiguity_probability"]
    assert rows[0.01]["expected_cost"] < rows[0.05]["expected_cost"]
    for limit, row in rows.items():
        assert row["wrong_probability"] <= limit + 1e-12
        assert (
            row["correct_probability"]
            + row["wrong_probability"]
            + row["ambiguity_probability"]
        ) == pytest.approx(1.0)
