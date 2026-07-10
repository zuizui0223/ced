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
    by sharp expectation-based bounds from the marginal read contract; and
13. coordinate-specific threshold designs compose through heterogeneous union,
    Frechet, product, and weighted-budget bounds that must not be conflated.

## Independent finite-oracle checks

`tests/test_exhaustive_oracles.py` separately enumerates bounded finite cases
rather than asserting only the package's own closed-form outputs. It checks:

- delayed grammars and the no-uniform-horizon witness on small grids of module
  counts, delays, and horizons;
- every binary state class of small reset panels, including the number of
  signatures and the size of every residual class;
- canonical parsing of all short trial streams and the resource frontier over
  small trial, action, and delay budgets; and
- direct enumeration of declared common-mode failure subsets, including
  overlapping modes.

`tests/test_detection_oracles.py` separately enumerates every binary observation
record over bounded repeat panels. It checks the single-coordinate and joint
detection formulas, the minimal-repeat helper, and the fact that a fully
negative signature is not an absence certificate when sensitivity is imperfect.

`tests/test_mode_detection_oracles.py` enumerates failed versus operating modes
and every binary read outcome inside small operating modes. It checks the
common-mode inclusion–exclusion formula, the availability ceiling, and the fact
that the mode floor is necessary but does not by itself make finite sensing
sufficient.

`tests/test_threshold_detection_oracles.py` enumerates every binary read outcome
for bounded false-positive threshold events. It checks the binomial tail formula,
the event-level evidence ratio, the minimum-threshold helper, and the fact that
threshold crossing is not a proof of presence when false positives are allowed.

`tests/test_multiple_testing_oracles.py` enumerates all small coordinate-by-read
binary records under the all-absent state. It checks the exact independent
familywise formula, the Bonferroni dominance bound, and the threshold-search
frontier for declared familywise false-alert control.

`tests/test_calibration_oracles.py` enumerates calibration outcomes on bounded
finite grids. It checks one-sided coverage for the blank-control false-positive
upper bound and the present-control sensitivity lower bound, plus monotonicity in
observed calibration counts.

`tests/test_discovery_budget_oracles.py` enumerates bounded false-discovery
counts under finite independent alert distributions. It checks the expected
false-discovery formula and verifies that the Markov budget tail dominates the
enumerated tail probability.

`tests/test_dependent_repeats_oracles.py` constructs extremal dependent count
distributions. It checks that the marginal-only false-alert and detection bounds
are sharp, and that they are weaker than the binomial thresholds available under
resettable independence.

`tests/test_heterogeneous_thresholds_oracles.py` enumerates finite heterogeneous
coordinate count patterns. It checks exact independent all-absent familywise risk,
exact independent all-present joint detection, and the independence-free sharpness
of union and Frechet bounds.

These are implementation cross-checks, not automated proofs of the unbounded
all-family theorems. Their role is to catch formula, normalization, and
boundary-condition regressions that fixed replay witnesses can miss.

## Analytic theorem versus replay

The all-family no-uniform-horizon statement and the exact quotient claims remain
mathematical consequences of their declared finite grammar and panel contracts.
The imperfect-detection, mode-diverse, bounded-false-positive,
multiple-coordinate, calibration-bound, discovery-budget, dependent-repeat, and
heterogeneous-threshold extensions are theorems under their own explicit target-
set, control-label, sensitivity, error-rate, resettable-read, marginal-read,
coordinate-specific, and independence contracts. The replays are regression
witnesses for selected values; they are not automated proofs of the all-system
theorems.

## Explicit boundaries

The heterogeneous-threshold extension does not infer coordinate states, error
rates, cross-coordinate independence, shared thresholds, false discovery rates, or
an ecological closure boundary from the record. Those are next-theorem targets,
not hidden claims of the current package.
