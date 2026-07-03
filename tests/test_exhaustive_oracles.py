"""Independent finite-oracle checks for the CED implementation.

These are regression tests, not automated proofs of the all-family theorems.
They enumerate small finite state spaces and declared failure subsets separately
from the package's closed-form helpers.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product

from ced.delayed import DelayedExposureFamily, no_uniform_closure_horizon
from ced.panels import PanelCoverage, panel_budget_frontier
from ced.robustness import CommonModeProfile


def _signature(
    state: tuple[int, tuple[int, ...], int], panel: PanelCoverage
) -> tuple[int, tuple[int, ...], int | None]:
    focal, exterior, response = state
    return (
        focal,
        tuple(exterior[port] for port in sorted(panel.read_ports)),
        response if panel.intervention else None,
    )


def _powerset_indices(size: int):
    for cardinality in range(size + 1):
        yield from combinations(range(size), cardinality)


def test_delayed_grammar_and_counterexamples_match_small_exhaustive_grid():
    for module_count in range(1, 6):
        for delay in range(0, 7):
            family = DelayedExposureFamily(module_count, delay)
            assert family.verify()
            for horizon in range(0, 10):
                expected = [()]
                expected.extend(("wait",) * length for length in range(1, min(horizon, delay) + 1))
                if horizon >= delay + 1:
                    expected.append(("wait",) * delay + ("fire",))
                assert family.legal_words_through(horizon) == tuple(expected)
                assert family.is_exterior_blind_through(horizon) == (horizon <= delay)

    for horizon in range(0, 20):
        witness = no_uniform_closure_horizon(horizon)
        assert witness.delay == horizon
        assert witness.revealing_horizon == horizon + 1
        assert all("fire" not in word for word in witness.legal_words_through(horizon))


def test_panel_quotient_cardinality_matches_enumerated_binary_state_classes():
    for module_count in range(1, 6):
        states = list(product((0, 1), repeat=module_count + 2))
        structured_states = [(state[0], state[1:-1], state[-1]) for state in states]
        for ports in _powerset_indices(module_count):
            for intervention in (False, True):
                panel = PanelCoverage(module_count, frozenset(ports), intervention)
                multiplicities = Counter(_signature(state, panel) for state in structured_states)
                assert len(multiplicities) == panel.quotient_state_count
                assert set(multiplicities.values()) == {panel.residual_class_size}
                assert panel.verify()


def test_panel_parser_is_canonical_on_all_short_trial_streams():
    for module_count in range(1, 5):
        alphabet = ["wait", "intervene"] + [f"read:{port}" for port in range(module_count)]
        for length in range(0, 5):
            for trials in product(alphabet, repeat=length):
                panel = PanelCoverage.from_trials(module_count, trials)
                assert panel.read_ports == frozenset(
                    int(trial.split(":", 1)[1]) for trial in trials if trial.startswith("read:")
                )
                assert panel.intervention == ("intervene" in trials)
                assert PanelCoverage.from_trials(module_count, panel.to_trials()) == panel


def test_budget_frontier_matches_exhaustive_resource_oracle():
    for module_count in range(1, 7):
        terminal_count = module_count + 1
        for trial_budget in range(0, 9):
            assert panel_budget_frontier(module_count, trial_budget) == 1 + min(
                trial_budget, terminal_count
            )
            for delay in range(0, 5):
                for action_budget in range(0, 25):
                    affordable = action_budget // (delay + 1)
                    expected = 1 + min(trial_budget, affordable, terminal_count)
                    assert (
                        panel_budget_frontier(module_count, trial_budget, delay, action_budget)
                        == expected
                    )


def _oracle_cover_number(support: frozenset[str], modes: tuple[frozenset[str], ...]) -> int:
    for cardinality in range(1, len(modes) + 1):
        for indices in combinations(range(len(modes)), cardinality):
            lost = set().union(*(modes[index] for index in indices))
            if support <= lost:
                return cardinality
    raise AssertionError("a valid support must be coverable by the declared modes")


def test_common_mode_cover_and_survival_match_direct_failure_enumeration():
    mode_layouts = (
        ({"a"}, {"b"}, {"c"}),
        ({"a", "b"}, {"b", "c"}, {"a", "c"}),
        ({"a", "b"}, {"b"}, {"c"}),
        ({"a"}, {"a", "b"}, {"b", "c"}),
    )
    for layout in mode_layouts:
        modes = tuple(frozenset(mode) for mode in layout)
        cells = sorted(set().union(*modes))
        for support_size in range(1, len(cells) + 1):
            for support_cells in combinations(cells, support_size):
                support = frozenset(support_cells)
                profile = CommonModeProfile((support,), modes)
                cover_number = _oracle_cover_number(support, modes)
                assert profile.mode_cover_number(0) == cover_number
                assert profile.common_mode_tolerance == cover_number - 1
                for failure_budget in range(0, len(modes) + 2):
                    survives_by_direct_check = all(
                        not support <= set().union(*(modes[index] for index in chosen))
                        for cardinality in range(1, failure_budget + 1)
                        for chosen in combinations(range(len(modes)), cardinality)
                    )
                    assert profile.survives(failure_budget) == survives_by_direct_check
