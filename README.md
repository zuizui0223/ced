# CED — Closure Evidence Design

CED is a theorem-first mathematical-ecology repository for a finite evidence
question:

> When does finite monitoring fail to certify ecological closure, and what exact
> partial information can a declared intervention panel recover instead?

It is the standalone successor of CCOC legacy `ID-1` and the relevant
`LEGACY-1` panel-design results. CCOC remains frozen provenance; this repository
contains the active development core.

## Theorem core

1. **Delayed exposure / no uniform horizon.** Every fixed finite grammar-aware system has a finite exact horizon, but no single passive finite observation horizon certifies closure uniformly over families whose legal exterior exposure is delayed arbitrarily far.
2. **Exact partial panel quotient.** A reset panel identifies exactly the focal baseline, the exterior coordinates it probes, and the response-type coordinate if it performs the intervention probe.
3. **Distinct design resources.** Fresh-trial count, total action budget, and per-trial temporal depth yield distinct identification frontiers.
4. **Common-mode robustness.** A panel survives a declared number of failures when every required separator set cannot be covered by that many common-mode failure groups. Raw replicate count is not failure diversity.
5. **One-sided imperfect detection.** With declared zero false positives, bounded sensitivity, and resettable independent reads, positive detections are certificates of presence but finite non-detections do not certify absence. See [the imperfect-detection theorem](docs/imperfect_detection_theorem.md).
6. **Mode-diverse imperfect detection.** Under independent declared failure modes, repeats inside one mode improve sensitivity but cannot overcome the probability that every selected mode fails together. See [the common-mode detection theorem](docs/mode_diverse_detection_theorem.md).
7. **Bounded false positives.** Threshold crossings become bounded evidence rather than deductive presence certificates. See [the false-positive threshold theorem](docs/false_positive_threshold_theorem.md).
8. **Multiple-coordinate threshold control.** Bonferroni familywise bounds remain valid without cross-coordinate independence; exact all-absent formulas require independence. See [the multiple-testing threshold theorem](docs/multiple_testing_threshold_theorem.md).
9. **Calibration-derived error bounds.** Blank and present controls supply conservative one-sided binomial bounds for `f_max` and `p_min`. See [the calibration-bound theorem](docs/calibration_bounds_theorem.md).
10. **Expected false-discovery budgets.** Linearity bounds expected false alerts and Markov converts that into a finite budget-exceedance bound. See [the discovery-budget theorem](docs/discovery_budget_theorem.md).
11. **Dependent repeats and non-reset reads.** Without resettable independence, binomial tails are invalid and sharp expectation-based bounds remain. See [the dependent-repeat theorem](docs/dependent_repeats_theorem.md).
12. **Heterogeneous coordinate thresholds.** Coordinates may have different read counts, thresholds, sensitivity bounds, and false-positive bounds. See [the heterogeneous-threshold theorem](docs/heterogeneous_thresholds_theorem.md).
13. **Adaptive alpha spending.** Coordinates, modes, and confirmation stages may be chosen after seeing earlier outcomes while preserving false-alert risk via conditional alpha spending. See [the adaptive-spending theorem](docs/adaptive_spending_theorem.md).
14. **Overlapping failure factors.** Independent modes and one global common mode are endpoint cases of a latent factor graph with partially shared failure causes. See [the overlapping-failure-mode theorem](docs/overlapping_failure_modes_theorem.md).
15. **False-discovery concentration.** Under explicitly independent false-alert indicators, exact Poisson-binomial tails and Chernoff bounds strengthen the independence-free Markov budget bound. See [the discovery-concentration theorem](docs/discovery_concentration_theorem.md).

## Verification

`pytest` checks theorem witnesses, finite oracles, exact outcome enumerations, sharpness constructions, calibration coverage, adaptive policy trees, overlapping failure-factor states, and independent false-discovery tails.

Deterministic replay scripts include:

```bash
python scripts/verify_ced_core.py
python scripts/verify_imperfect_detection.py
python scripts/verify_mode_detection.py
python scripts/verify_threshold_detection.py
python scripts/verify_multiple_testing.py
python scripts/verify_calibration_bounds.py
python scripts/verify_discovery_budget.py
python scripts/verify_dependent_repeats.py
python scripts/verify_heterogeneous_thresholds.py
python scripts/verify_adaptive_spending.py
python scripts/verify_overlapping_modes.py
python scripts/verify_discovery_concentration.py
```

## Scope

CED concerns declared finite deterministic grammars, resettable probe panels,
declared failure-mode families, explicit observation contracts, and declared
calibration-control contracts. It does not infer delays, resetability, closure,
action grammars, failure probabilities, detection sensitivity, false-positive
rates, independence, latent failure factors, coordinate states, ordinary FDR,
adaptive policy optimality, or ecological mechanisms from observations.
