# CED standalone verification audit

## Purpose

CED was reconstructed from frozen CCOC legacy assets. This audit records what the
standalone package verifies, what is preserved analytically from legacy, and what
is deliberately not claimed by a passing test suite.

## Source-to-successor map

| CCOC legacy asset | CED public core | Status |
|---|---|---|
| delayed addressability / no-uniform-horizon family | `ced.delayed.DelayedExposureFamily` | migrated as a finite witness interface |
| reset-panel partial quotient and budget frontiers | `ced.panels.PanelCoverage` | migrated as an exact signature/count construction |
| common-mode canonical panel analysis | `ced.robustness.CommonModeProfile` | migrated as finite mode-cover robustness |
| no CCOC predecessor | `ced.detection.OneSidedDetector` | one-sided imperfect-detection extension |
| no CCOC predecessor | `ced.mode_detection.ModeDiverseDetectionPanel` | common-mode imperfect-detection extension |
| no CCOC predecessor | `ced.threshold_detection.ThresholdEvidenceDesign` | bounded false-positive evidence extension |
| no CCOC predecessor | `ced.multiple_testing.MultipleThresholdEvidenceDesign` | multiple-coordinate familywise extension |
| no CCOC predecessor | `ced.calibration.CalibrationBounds` | calibration-derived error-bound extension |
| no CCOC predecessor | `ced.discovery_budget.FalseDiscoveryBudget` | expected false-discovery budget extension |
| no CCOC predecessor | `ced.dependent_repeats.DependentThresholdEvidenceDesign` | dependent-repeat threshold extension |
| no CCOC predecessor | `ced.heterogeneous_thresholds.HeterogeneousThresholdEvidencePanel` | heterogeneous threshold-panel extension |
| no CCOC predecessor | `ced.adaptive_spending.AdaptiveAlphaSpendingLedger` | adaptive alpha-spending extension |
| no CCOC predecessor | `ced.overlapping_modes.OverlappingFailureModePanel` | overlapping latent failure-factor extension |

The relay-tree compilation and CCOC open-composition manuscript theorem are not
CED dependencies. They remain provenance in the frozen archive.

## What the checks establish

The standalone tests and replay verify that:

1. every proposed finite horizon has a delayed witness whose first revealing word
   is later than that horizon;
2. canonical panel signatures ignore trial order, duplicate probes, and wait-only
   trials;
3. retained and residual signature counts multiply to the declared binary state
   space size;
4. trial, action, and temporal-depth resources are not silently conflated in the
   implemented budget helper;
5. common-mode robustness depends on failure-mode cover number, not raw replicate
   count;
6. under the declared one-sided detection contract, finite all-negative records
   remain compatible with presence while repeated reads give a lower bound for
   joint positive-detection probability;
7. under declared independent common-mode availability, moving effort across
   failure modes changes the detection frontier in a way that repeated reads
   inside one mode cannot reproduce;
8. with bounded false positives, threshold crossings are not deductive presence
   certificates but do have a posterior-free event-level evidence-ratio lower
   bound under the declared read contract;
9. screening many declared coordinates inflates false-alert risk, requiring an
   explicit familywise bound even when the per-coordinate evidence ratio is high;
10. finite blank and present controls can be converted into conservative one-sided
    binomial error bounds before threshold evidence is computed;
11. expected false discoveries are bounded by linearity, with Markov bounds for
    exceeding declared false-discovery budgets;
12. if reads are dependent or non-reset, binomial threshold tails must be replaced
    by sharp expectation-based bounds from the marginal read contract;
13. coordinate-specific threshold designs compose through heterogeneous union,
    Frechet, product, and weighted-budget bounds that must not be conflated;
14. adaptively selected coordinates, modes, and confirmation stages preserve
    false-alert risk accounting when every selected stage spends declared
    conditional alpha; and
15. partially shared failure causes are represented by an explicit latent factor
    graph whose exact finite mixture recovers both independent-mode and global
    common-mode endpoints.

## Independent finite-oracle checks

`tests/test_exhaustive_oracles.py` separately enumerates bounded finite cases
rather than asserting only the package's own closed-form outputs. It checks delayed
grammars, reset-panel signatures, budget frontiers, and finite common-mode failure
subsets.

`tests/test_detection_oracles.py` enumerates binary observation records for the
one-sided imperfect-detection layer.

`tests/test_mode_detection_oracles.py` enumerates failed versus operating modes and
binary read outcomes under independent mode availability.

`tests/test_threshold_detection_oracles.py` enumerates bounded false-positive
threshold events.

`tests/test_multiple_testing_oracles.py` enumerates small coordinate-by-read binary
records for familywise control.

`tests/test_calibration_oracles.py` enumerates calibration outcomes on bounded
finite grids.

`tests/test_discovery_budget_oracles.py` enumerates bounded false-discovery counts.

`tests/test_dependent_repeats_oracles.py` constructs extremal dependent count
distributions and checks sharp marginal-only bounds.

`tests/test_heterogeneous_thresholds_oracles.py` enumerates finite heterogeneous
coordinate count patterns.

`tests/test_adaptive_spending_oracles.py` enumerates a small adaptive policy tree.

`tests/test_overlapping_modes_oracles.py` enumerates latent factor states and
coordinate detection outcomes. It checks the exact overlapping-factor mixture,
all-modes-failed probability, endpoint recovery, and a partial-overlap design
between independent and fully shared mode structures.

These are implementation cross-checks, not automated proofs of the unbounded
all-family theorems. Their role is to catch formula, normalization, and
boundary-condition regressions that fixed replay witnesses can miss.

## Analytic theorem versus replay

The all-family no-uniform-horizon statement and the exact quotient claims remain
mathematical consequences of their declared finite grammar and panel contracts.
The imperfect-detection, mode-diverse, bounded-false-positive,
multiple-coordinate, calibration-bound, discovery-budget, dependent-repeat,
heterogeneous-threshold, adaptive-spending, and overlapping-failure-factor
extensions are theorems under their own explicit target-set, control-label,
sensitivity, error-rate, resettable-read, marginal-read, coordinate-specific,
conditional-alpha, latent-factor, and independence contracts. The replays are
regression witnesses for selected values; they are not automated proofs of the
all-system theorems.

## Explicit boundaries

The overlapping-factor extension does not infer latent factors, factor failure
probabilities, mode-factor assignments, sensitivity, ecological failure causes,
false discovery rates, or an ecological closure boundary from the record. Those
are not hidden claims of the current package.
