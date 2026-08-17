# CED — Closure Evidence Design

CED is a theorem-first mathematical-ecology repository for one finite evidence
question:

> Which distinctions among possible ecological futures can a finite experiment and observation contract honestly resolve and report, and what should be measured next when the declared target remains unresolved?

CED grew from delayed-exposure and panel-design results archived in CCOC/RACH. CCOC now retains its own independent open-future theorem program; CED is the distinct evidence/reportability layer and is in submission consolidation rather than open-ended theorem expansion.

## Current Paper B core

The submission-facing manuscript is organized around one four-result reportability chain:

1. **Experiment-induced ecological quotient and honest report criterion.** A finite experiment partitions latent worlds by the records it can produce. A deterministic target report is justified exactly when the target is constant on the compatible class; otherwise the sharp output remains set-valued or ambiguity-retaining.
2. **Unique coarsest target-safe quotient.** Starting from the evidence-induced partition, retain the least additional resolution needed to preserve the declared target and deterministic successors under every declared action. Full latent-world identification is unnecessary when remaining distinctions cannot change the requested future report.
3. **Failure architecture and trustworthy refinement.** A nominal record split is not automatically trustworthy under imperfect observation. Repeats inside one shared failure domain, independent modes, overlapping failures, and resetability support different guarantees; the observation architecture constrains which target-relevant refinement may be credited.
4. **Adaptive risk-limited target resolution.** Experiment choice and stopping are evaluated by correct deterministic reporting, wrong deterministic reporting, honest ambiguity, and cost under an explicit false-resolution contract. The objective is defensible target resolution, not maximum latent-world information for its own sake.

Finite passive closure non-certifiability remains an important motivating/supporting result, not a fifth headline Paper B theorem. Calibration, multiple-testing, heterogeneous-threshold, concentration, and related probability machinery remain Methods/Supplement support rather than equal-weight novelty claims.

See [the current Paper B theorem consolidation](docs/paper_b_theorem_consolidation.md),
[the experiment-induced quotient theorem](docs/experiment_induced_quotient_theorem.md), and
[the MEE submission package](docs/mee_submission_package.md).

## CREST role and claim firewall

At program level, CED is the **evidential-licensing audit** of Contract-Relative Ecological State Theory (CREST): it asks which distinctions a declared experiment, observation, failure, calibration, and risk contract can justify reporting for a requested ecological target.

The canonical four-audit synthesis is maintained in MRM at [Contract-Relative Ecological State Theory (CREST)](https://github.com/zuizui0223/mrm/blob/main/docs/contract_relative_ecological_state_theory.md). The local [program synthesis audit](docs/program_synthesis_audit.md) records the CED-facing version of the same firewall.

Companion ownership is distinct:

- future-composition / open-grammar interface complexity → **CCOC**;
- inherited source-law transport and least semantic repair → **MLTR**;
- unresolved candidate mechanisms and candidate-safe predictive state → **MRM**;
- finite/noisy evidence, detection/failure architecture, calibration, and risk-limited reportability → **CED**.

CED and MRM share a neutral finite target/action-stable refinement lemma, but not one novelty claim. In CED the initial class is induced by evidence records and the output is an evidentially licensed target report. In MRM the latent worlds specialize to observable-state × response-type worlds and the output is a mechanism-safe state/report. Generic partition refinement is common substrate.

Passing the CED audit does not prove that the state is future-sufficient under every opened grammar, semantically coherent after structural replacement, or robust to retained mechanism alternatives.

## Detailed theorem notes

- [Delayed exposure and finite closure limits](docs/delayed_addressability.md) — supporting non-certifiability motivation
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
sharpness constructions, target-safe minimality, calibration coverage, adaptive policy
trees, overlapping failure-factor states, independent false-discovery tails, story/literature
contracts, and the submission-facing reportability artifacts.

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
failure-mode families, observation contracts, report targets, calibration contracts,
and explicit risk/cost rules. It does not infer those objects from field data. It
provides exact or risk-limited reporting guarantees once they are declared.
