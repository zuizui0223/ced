"""Closure Evidence Design (CED)."""

from .adaptive_spending import AdaptiveAlphaSpend, AdaptiveAlphaSpendingLedger
from .calibration import (
    CalibrationBounds,
    false_positive_upper_confidence_bound,
    sensitivity_lower_confidence_bound,
)
from .delayed import DelayedExposureFamily, no_uniform_closure_horizon
from .dependent_repeats import DependentThresholdEvidenceDesign
from .detection import OneSidedDetectionPanel, OneSidedDetector
from .discovery_budget import FalseDiscoveryBudget
from .discovery_concentration import IndependentFalseDiscoveryConcentration
from .experiment_quotient import CompatibleRecordReport, ExperimentInducedQuotient
from .heterogeneous_thresholds import HeterogeneousThresholdEvidencePanel
from .mode_detection import ModeDiverseDetectionPanel
from .multiple_testing import MultipleThresholdEvidenceDesign
from .overlapping_modes import OverlappingFailureModePanel
from .panels import PanelCoverage, panel_budget_frontier
from .robustness import CommonModeProfile
from .threshold_detection import ThresholdEvidenceDesign, binomial_tail

__all__ = [
    "AdaptiveAlphaSpend",
    "AdaptiveAlphaSpendingLedger",
    "CalibrationBounds",
    "false_positive_upper_confidence_bound",
    "sensitivity_lower_confidence_bound",
    "DelayedExposureFamily",
    "no_uniform_closure_horizon",
    "DependentThresholdEvidenceDesign",
    "OneSidedDetector",
    "OneSidedDetectionPanel",
    "FalseDiscoveryBudget",
    "IndependentFalseDiscoveryConcentration",
    "ExperimentInducedQuotient",
    "CompatibleRecordReport",
    "HeterogeneousThresholdEvidencePanel",
    "ModeDiverseDetectionPanel",
    "MultipleThresholdEvidenceDesign",
    "OverlappingFailureModePanel",
    "ThresholdEvidenceDesign",
    "binomial_tail",
    "PanelCoverage",
    "panel_budget_frontier",
    "CommonModeProfile",
]
