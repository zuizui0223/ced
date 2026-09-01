# CED — Closure Evidence Design

CED is a theorem-first mathematical-ecology repository for one finite evidence question:

> Which distinctions among possible ecological futures can a finite experiment and observation contract honestly resolve and report, and what should be measured next when the declared target remains unresolved?

CED grew from delayed-exposure and panel-design results archived in CCOC/RACH. CCOC now retains its own independent open-future theorem program; CED is the distinct evidence/reportability layer and is in submission consolidation rather than open-ended theorem expansion.

## Current Paper B core

The submission-facing manuscript now uses consequence-first order while preserving the theorem dependency order. Readers encounter the two operational results first:

- **Result 3 — failure architecture and trustworthy refinement.** A nominal record split is not automatically trustworthy under imperfect observation. Repeats inside one shared failure domain, independent modes, overlapping failures, and resetability support different guarantees; the observation architecture constrains which target-relevant refinement may be credited.
- **Result 4 — adaptive risk-limited target resolution.** Experiment choice and stopping are evaluated by correct deterministic reporting, wrong deterministic reporting, honest ambiguity, and cost under an explicit false-resolution contract. The schema-v5 witness shows that full-world information gain can select a target-irrelevant measurement; this does not imply that information or replication is generically unhelpful.

The exact quotient results then supply the reporting infrastructure:

- **Result 1 — experiment-induced ecological quotient and honest report criterion.** A finite experiment partitions latent worlds by the records it can produce. A deterministic target report is justified exactly when the target is constant on the compatible class; otherwise the sharp output remains set-valued or ambiguity-retaining.
- **Result 2 — unique coarsest target-safe quotient.** Starting from the evidence-induced partition, retain the least additional resolution needed to preserve the declared target and deterministic successors under every declared action. Full latent-world identification is unnecessary when remaining distinctions cannot change the requested future report.

Thus the logical dependency remains `Result 1 -> Result 2 -> Result 3 -> Result 4`, while the main-text presentation is `Result 3 -> Result 4 -> Results 1--2 as infrastructure`.

**Evidence boundary for Result 2.** The target-safe quotient is a **required refinement**, not a claim that the current record has already identified its refined blocks. If the current compatible record class intersects more than one target-safe block and the evidence contract has not resolved which block contains the true world, Result 1 still governs the honest output: retain ambiguity or report the compatible target set. Results 3–4 ask when additional observation architecture can justifiably earn that refinement.

Finite passive closure non-certifiability remains an important motivating/supporting result, not a fifth headline Paper B theorem. Calibration, multiple-testing, heterogeneous-threshold, concentration, and related probability machinery remain Methods/Supplement support rather than equal-weight novelty claims.

See [the current Paper B theorem consolidation](docs/paper_b_theorem_consolidation.md), [the experiment-induced quotient theorem](docs/experiment_induced_quotient_theorem.md), and [the MEE submission package](docs/mee_submission_package.md).

## CREST role: evidence licensing after state adequacy

The canonical synthesis lives in the dedicated [CREST repository](https://github.com/zuizui0223/crest), with the current hierarchy in the [trajectory-first program architecture](https://github.com/zuizui0223/crest/blob/main/docs/trajectory_first_program_architecture_2026-08-22.md).

CREST now starts from temporally extended ecological worlds, asks whether a present snapshot is sufficient, and uses CCOC, MLTR, and MRM as three structural reasons that a present merge can fail. **CED is intentionally downstream of that structural question.**

CED asks:

> Once a scientific contract requires a distinction among ecological worlds, does the current experiment and observation architecture actually identify enough of that distinction to license the requested report?

Thus CED separates

\[
\boxed{
\text{required state}
\neq
\text{identified state}
\neq
\text{reportable target}
}
\]

in general.

A CED failure does not mean that nature contains no required distinction. It means the current evidence contract does not justify collapsing the compatible latent worlds to one deterministic state or target value.

Companion ownership remains distinct:

- future-composition / open-grammar interface complexity → **CCOC**;
- inherited source-law transport and least semantic repair → **MLTR**;
- unresolved candidate mechanisms and candidate-safe predictive state → **MRM**;
- finite/noisy evidence, detection/failure architecture, calibration, and risk-limited reportability → **CED**.

CED and MRM share a neutral finite target/action-stable refinement lemma, but not one novelty claim. In CED the initial class is induced by evidence records and the output is an evidentially licensed target report. In MRM the latent worlds specialize to observable-state × response-type worlds and the output is a mechanism-safe state/report. Generic partition refinement is common substrate.

Passing the CED audit does not prove that a proposed state merge is future-sufficient, semantically coherent after structural replacement, or robust to retained mechanism alternatives. It certifies only what the declared evidence architecture licenses about the required distinctions.

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

`pytest` checks theorem witnesses, finite oracles, exact outcome enumerations, sharpness constructions, target-safe minimality, calibration coverage, adaptive policy trees, overlapping failure-factor states, independent false-discovery tails, story/literature contracts, and the submission-facing reportability artifacts.

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

CED concerns declared finite latent worlds, action grammars, intervention panels, failure-mode families, observation contracts, report targets, calibration contracts, and explicit risk/cost rules. It does not infer those objects from field data. It provides exact or risk-limited reporting guarantees once they are declared.
