"""Closure Evidence Design (CED)."""

from .delayed import DelayedExposureFamily, no_uniform_closure_horizon
from .detection import OneSidedDetectionPanel, OneSidedDetector
from .mode_detection import ModeDiverseDetectionPanel
from .multiple_testing import MultipleThresholdEvidenceDesign
from .panels import PanelCoverage, panel_budget_frontier
from .robustness import CommonModeProfile
from .threshold_detection import ThresholdEvidenceDesign, binomial_tail

__all__ = [
    "DelayedExposureFamily",
    "no_uniform_closure_horizon",
    "OneSidedDetector",
    "OneSidedDetectionPanel",
    "ModeDiverseDetectionPanel",
    "MultipleThresholdEvidenceDesign",
    "ThresholdEvidenceDesign",
    "binomial_tail",
    "PanelCoverage",
    "panel_budget_frontier",
    "CommonModeProfile",
]
