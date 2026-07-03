"""Closure Evidence Design (CED).

Finite theorems for delayed exposure, exact partial identification under reset
panels, robustness to declared common-mode measurement failures, and one-sided
imperfect-detection evidence design.
"""

from .delayed import DelayedExposureFamily, no_uniform_closure_horizon
from .detection import OneSidedDetectionPanel, OneSidedDetector
from .panels import PanelCoverage, panel_budget_frontier
from .robustness import CommonModeProfile

__all__ = [
    "DelayedExposureFamily",
    "no_uniform_closure_horizon",
    "OneSidedDetector",
    "OneSidedDetectionPanel",
    "PanelCoverage",
    "panel_budget_frontier",
    "CommonModeProfile",
]
