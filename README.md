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
2. **Exact partial evidence quotient.** A resettable intervention panel identifies
   exactly the baseline and coordinates it probes. Unprobed distinctions remain in
   a quantified residual class, and trial count, action budget, and temporal depth
   are distinct design resources.
3. **Robust detection under imperfect and shared failure.** Finite non-detection
   does not certify absence under imperfect sensitivity. Detection guarantees
   depend separately on repeats, independent modes, overlapping latent failure
   factors, and resetability; raw replication inside one shared mode cannot remove
   its availability ceiling.
4. **Calibrated risk-limited evidence design.** False-positive thresholds,
   calibration controls, multiple and heterogeneous coordinates, adaptive alpha
   spending, and independent concentration bounds form one auditable risk-accounting
   framework.

See [the manuscript architecture](docs/manuscript_architecture.md) for theorem
placement, figures, ecological interpretation, and the development freeze. See
[the cross-repository synthesis audit](docs/program_synthesis_audit.md) for the
relationship among CCOC/RACH, MLTR, CED, and MRM.

## Detailed theorem notes

- [Delayed exposure and finite closure limits](docs/delayed_addressability.md)
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
failure-factor states, and independent false-discovery tails.

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
```

## Scope

CED concerns declared finite deterministic grammars, intervention panels, failure
mode families, observation contracts, and calibration-control contracts. It does
not infer delays, resetability, closure, coordinate truth, failure factors,
sensitivity, false-positive rates, independence, or calibration representativeness
from field data. It provides finite conditional guarantees once those contracts are
declared.
