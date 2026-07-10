"""Closure Evidence Design (CED)."""

from .calibration import (
    CalibrationBounds,
    false_positive_upper_confidence_bound,
    sensitivity_lower_confidence_bound,
)
from .delayed import DelayedExposureFamily, no_uniform_closure_horizon
from .dependent_repeats import DependentThresholdEvidenceDesign
from .detection import OneSidedDetectionPanel, OneSidedDetector
from .discovery_budget import FalseDiscoveryBudget
from .mode_detection import ModeDiverseDetectionPanel
from .multiple_testing import MultipleThresholdEvidenceDesign
from .panels import PanelCoverage, panel_budget_frontier
from .robustness import CommonModeProfile
from .threshold_detection import ThresholdEvidenceDesign, binomial_tail

__all__ = [
    "CalibrationBounds",
    "false_positive_upper_confidence_bound",
    "sensitivity_lower_confidence_bound",
    "DelayedExposureFamily",
    "no_uniform_closure_horizon",
    "DependentThresholdEvidenceDesign",
    "OneSidedDetector",
    "OneSidedDetectionPanel",
    "FalseDiscoveryBudget",
    "ModeDiverseDetectionPanel",
    "MultipleThresholdEvidenceDesign",
    "ThresholdEvidenceDesign",
    "binomial_tail",
    "PanelCoverage",
    "panel_budget_frontier",
    "CommonModeProfile",
]
