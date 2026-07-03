"""Closure Evidence Design (CED).

Finite theorems for delayed exposure, exact partial identification under reset
panels, and robustness to declared common-mode measurement failures.
"""

from .delayed import DelayedExposureFamily, no_uniform_closure_horizon
from .panels import PanelCoverage, panel_budget_frontier
from .robustness import CommonModeProfile

__all__ = [
    "DelayedExposureFamily",
    "no_uniform_closure_horizon",
    "PanelCoverage",
    "panel_budget_frontier",
    "CommonModeProfile",
]
