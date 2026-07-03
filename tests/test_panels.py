from ced.panels import PanelCoverage, panel_budget_frontier


def test_panel_coverage_is_an_exact_partial_quotient():
    panel = PanelCoverage.from_trials(4, ("read:0", "read:3", "intervene", "read:3", "wait"))
    assert panel.read_ports == frozenset({0, 3})
    assert panel.intervention
    assert panel.retained_bits == 4
    assert panel.residual_bits == 1
    assert panel.quotient_state_count == 16
    assert panel.residual_class_size == 2
    assert panel.verify()


def test_panel_frontiers_distinguish_trials_from_action_budget():
    assert panel_budget_frontier(4, trial_budget=0) == 1
    assert panel_budget_frontier(4, trial_budget=2) == 3
    assert panel_budget_frontier(4, trial_budget=9) == 6
    assert panel_budget_frontier(4, trial_budget=9, delay=3, action_budget=8) == 3


def test_full_coverage_is_exact():
    panel = PanelCoverage.from_trials(3, ("read:0", "read:1", "read:2", "intervene"))
    assert panel.is_exact
    assert panel.residual_bits == 0
    assert panel.residual_class_size == 1
