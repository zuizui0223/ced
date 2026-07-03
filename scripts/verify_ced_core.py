"""Write a deterministic finite replay report for the CED theorem core."""

from __future__ import annotations

import json
from pathlib import Path

from ced.delayed import DelayedExposureFamily, no_uniform_closure_horizon
from ced.panels import PanelCoverage, panel_budget_frontier
from ced.robustness import CommonModeProfile

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts" / "ced_core_report.json"


def build_report() -> dict[str, object]:
    delayed = DelayedExposureFamily(module_count=4, delay=5)
    no_go = no_uniform_closure_horizon(7)
    panel = PanelCoverage.from_trials(4, ("read:0", "read:3", "intervene"))
    common_mode = CommonModeProfile(
        pair_separators=(frozenset({"site-a", "site-b", "site-c"}),),
        failure_modes=(frozenset({"site-a"}), frozenset({"site-b"}), frozenset({"site-c"})),
    )
    if not delayed.verify() or not no_go.verify() or not panel.verify():
        raise AssertionError("CED finite witness failed verification")
    return {
        "schema_version": 1,
        "scope": "declared finite delayed grammars, resettable probe panels, and declared common-mode failure families",
        "non_claim": "the replay does not infer ecological delays, resetability, failure modes, or closure from observational data",
        "delayed_exposure": {
            "module_count": delayed.module_count,
            "delay": delayed.delay,
            "closed_interface_bits": delayed.closed_interface_bits,
            "open_interface_bits": delayed.open_interface_bits,
            "revealing_horizon": delayed.revealing_horizon,
        },
        "no_uniform_horizon": {
            "proposed_horizon": 7,
            "counterexample_revealing_horizon": no_go.revealing_horizon,
        },
        "partial_panel": {
            "retained_bits": panel.retained_bits,
            "residual_bits": panel.residual_bits,
            "quotient_state_count": panel.quotient_state_count,
            "residual_class_size": panel.residual_class_size,
            "trial_frontier_N2": panel_budget_frontier(4, 2),
            "action_frontier_A8_delay3": panel_budget_frontier(4, 9, delay=3, action_budget=8),
        },
        "common_mode": {
            "mode_cover_number": common_mode.mode_cover_number(0),
            "tolerance": common_mode.common_mode_tolerance,
        },
    }


def main() -> None:
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
