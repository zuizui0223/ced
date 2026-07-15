# CED — Closure Evidence Design

CED is a theorem-first mathematical-ecology repository for one finite evidence
question:

> When does finite monitoring fail to certify ecological closure, and what exact
> partial information can a declared intervention and observation design recover
> instead?

CED is the standalone successor of the delayed-exposure and panel-design results
archived in CCOC/RACH. CCOC remains frozen provenance; CED is now in manuscript
consolidation rather than open-ended theorem expansion.

## Manuscript core

1. **Finite closure non-certifiability.** Every fixed finite declared system may
   have a finite revealing horizon, but no single passive finite horizon certifies
   closure uniformly over families whose first legal exterior exposure can be
   delayed arbitrarily far.
2. **Experiment-induced ecological quotient.** A finite experiment partitions
   latent ecological worlds by the records it can produce. A deterministic report
   is justified exactly when the report target is constant on every remaining
   record class; otherwise the honest report is set-valued or ambiguity-retaining.
3. **Robust detection under imperfect and shared failure.** Finite non-detection
   does not certify absence under imperfect sensitivity. Reliable quotient
   refinement depends separately on repeats, independent modes, overlapping latent
   failure factors, and resetability.
4. **Calibrated risk-limited evidence design.** False-positive thresholds,
   calibration controls, heterogeneous coordinates, adaptive alpha spending, and
   concentration bounds form one auditable risk-accounting framework.

See [the manuscript architecture](docs/manuscript_architecture.md),
[the experiment-induced quotient theorem](docs/experiment_induced_quotient_theorem.md),
and [the submission analysis](docs/submission_analysis.md). The
[cross-repository synthesis audit](docs/program_synthesis_audit.md) records the
relationship among CCOC/RACH, MLTR, CED, and MRM.

## Detailed theorem notes

- [Delayed exposure and finite closure limits](docs/delayed_addressability.md)
- [Experiment-induced ecological quotient](docs/experiment_induced_quotient_theorem.md)
- [Imperfect detection](docs/imperfect_detection_theorem.md)
- [Independent mode diversity](docs/mode_diverse_detection_theorem.md)
- [Overlapping failure factors](docs/overlapping_failure_modes_theorem.md)
- [Dependent and non-reset repeats](docs/dependent_repeats_theorem.md)
- [False-positive threshold evidence](docs/false_positive_threshold_theorem.md)
- [Multiple-coordinate threshold control](docs/multiple_testing_threshold_theorem.md)
- [Calibration-derived bounds](docs/calibration_bounds_theorem.md)
- [Expected false-discovery budgets](docs/discovery_budget_theorem.md)
- [Heterogeneous thresholds](docs/heterogeneous_thresholds_theorem.md)
- [Adaptive alpha spending](docs/adaptive_spending_theorem.md)
- [Independent concentration bounds](docs/discovery_concentration_theorem.md)

## Verification

`pytest` checks theorem witnesses, finite oracles, exact outcome enumerations,
sharpness constructions, calibration coverage, adaptive policy trees, overlapping
failure-factor states, independent false-discovery tails, and the joint
presence-by-mechanism quotient witness.

```bash
python -m pip install -e '.[dev]'
pytest
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
python scripts/verify_experiment_quotient.py
```

## Scope

CED concerns declared finite latent worlds, action grammars, intervention panels,
failure-mode families, observation contracts, report targets, and calibration
contracts. It does not infer those objects from field data. It provides exact or
risk-limited reporting guarantees once they are declared.
