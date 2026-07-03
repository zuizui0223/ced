from ced.panels import PanelCoverage, panel_budget_frontier


def test_panel_signature_is_invariant_to_order_duplicates_and_waits():
    first = PanelCoverage.from_trials(5, ("read:4", "intervene", "read:1", "wait", "read:4"))
    second = PanelCoverage.from_trials(5, ("read:1", "read:4", "intervene"))
    assert first == second
    assert first.to_trials() == ("read:1", "read:4", "intervene")
    assert first.retained_bits == 4
    assert first.residual_bits == 3


def test_each_new_terminal_probe_adds_at_most_one_identified_bit():
    panel = PanelCoverage.from_trials(3, ())
    assert panel.retained_bits == 1
    panel = panel.add_trial("read:0")
    assert panel.retained_bits == 2
    assert panel.add_trial("read:0").retained_bits == 2
    assert panel.add_trial("intervene").retained_bits == 3


def test_depth_gate_is_not_replaced_by_more_shallow_trials():
    # With a delay of four, fewer than five actions buy zero terminal probes.
    assert panel_budget_frontier(3, trial_budget=100, delay=4, action_budget=4) == 1
    assert panel_budget_frontier(3, trial_budget=100, delay=4, action_budget=5) == 2
