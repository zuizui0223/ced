"""Closure Evidence Design (CED)."""

from .delayed import DelayedExposureFamily, no_uniform_closure_horizon
from .detection import OneSidedDetectionPanel, OneSidedDetector
from .mode_detection import ModeDiverseDetectionPanel
from .panels import PanelCoverage, panel_budget_frontier
from .robustness import CommonModeProfile

__all__ = [
    "DelayedExposureFamily",
    "no_uniform_closure_horizon",
    "OneSidedDetector",
    "OneSidedDetectionPanel",
    "ModeDiverseDetectionPanel",
    "PanelCoverage",
    "panel_budget_frontier",
    "CommonModeProfile",
]
