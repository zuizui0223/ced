# Paper B theorem consolidation

## Purpose

This document resolves the tension between the older standalone-CED manuscript architecture and the current combined Paper B. It is a submission-facing architecture decision, not a new theorem family.

## Authoritative paper identity

Paper B asks:

> Which distinctions among possible ecological futures can finite evidence honestly resolve, and which experiment can resolve the declared prediction at acceptable error and cost?

The paper is not a general closure paper, an occupancy replacement, or a catalogue of detection bounds. The mathematical spine is a four-result chain:

```text
finite experiment records
        -> exact compatible-world quotient
        -> minimal target-safe quotient
        -> failure-aware trustworthy refinement
        -> risk-limited adaptive experiment and report
```

The biological conclusion is:

> More ecological information is not automatically more predictive. Evidence improves a declared prediction only when it separates worlds that imply different target values, and the observation architecture is reliable enough to support that separation.

## Main-text theorem hierarchy

### Result 1 — Experiment-induced ecological quotient and honest report criterion

For a declared experiment `D`, latent worlds are equivalent when they produce the same complete record. The induced equivalence classes are the exact information supplied by that experiment.

Main-text claim:

- every record-based report is constant on an experiment-induced class;
- deterministic reporting of target `T` is justified exactly when `T` is constant on the compatible class;
- otherwise the sharp report is the set of compatible target values.

Provenance:

- `docs/experiment_induced_quotient_theorem.md`
- `ced/experiment_quotient.py`
- `scripts/verify_experiment_quotient.py`

Do not oversell the equivalence relation itself as novel. The contribution is its coupling to target reporting, observation error, future actions, and risk-limited experiment design.

### Result 2 — Unique coarsest target-safe quotient

The full experiment-induced quotient may preserve biological distinctions that are irrelevant to the declared prediction. Paper B therefore retains the unique coarsest observation-preserving, action-stable quotient that preserves all declared target reports.

Main-text interpretation:

> resolve only latent distinctions that can imply different ecological futures.

This is the result that turns the paper from generic identifiability into target-relative ecological prediction.

Provenance:

- combined CED–MRM theorem package described in `docs/publication_completion_spine.md`
- target-safe implementation and tests in the current Paper B code path

The deterministic report criterion belongs adjacent to Results 1–2 and should not compete as a separate headline theorem.

### Result 3 — Failure architecture determines trustworthy quotient refinement

A nominal experiment may separate two worlds in an ideal record model yet fail to support that split under imperfect observation. The headline statement is structural:

> repetition inside one shared failure domain is not equivalent to independent failure diversity.

Main-text claims:

- finite negative evidence does not become deductive absence under imperfect sensitivity;
- shared failure produces an availability ceiling that arbitrarily many within-mode repeats cannot remove;
- equal nominal effort allocated across independent modes can support a strictly stronger target-relevant refinement.

Provenance:

- `docs/imperfect_detection_theorem.md`
- `docs/mode_diverse_detection_theorem.md`
- overlapping/dependent-repeat theorem notes and deterministic replay

Main text should show the structural ceiling and one equal-effort contrast. Detailed inclusion–exclusion, heterogeneous thresholds, Markov/Chernoff/Poisson-binomial bounds, and calibration algebra belong in Methods or Supplement.

### Result 4 — Adaptive risk-limited target resolution

A policy maps observed records to a next experiment or stopping decision. Terminal leaves are evaluated by:

- correct deterministic report probability;
- wrong deterministic report probability;
- honest ambiguity probability;
- expected cost.

Main-text claim:

> the scientific objective is least-cost defensible target resolution under an explicit false-resolution contract, not full latent-world identification.

The schema-v5 benchmark is the decisive counterexample: full-world information gain selects a target-irrelevant measurement because it supplies more entropy reduction, whereas target-safe design selects the experiment that resolves the declared prediction.

The target-switch and threshold-sensitivity analyses are robustness checks for this result, not separate theorem families.

## Supporting mathematics: keep, but do not promote to equal-weight Results

### Delayed-exposure / no-uniform passive closure theorem

`ced/delayed.py` proves a useful impossibility witness: for any proposed passive horizon, a legal delayed family can remain exterior-blind through that horizon and reveal a distinction later.

Role in Paper B:

- one motivating paragraph or Supplement proposition illustrating why finite passive non-detection cannot generally certify that all future-relevant distinctions have been exhausted;
- provenance for the broader finite-evidence philosophy.

Do **not** make this a fifth main result in the combined Paper B. Its primary object is ecological closure, whereas Paper B's central object is target reportability.

### Calibration and threshold theorem family

Blank and known-present controls can conservatively produce `f_max` and `p_min`, which then feed threshold and multi-coordinate risk bounds.

Role:

- Methods/Supplement machinery establishing where declared observation-error contracts can come from;
- assumption ladder / reproducibility support.

Do not present Clopper–Pearson, Bonferroni, Chernoff, adaptive alpha spending, or threshold-search formulas as independent novelty claims.

### Posterior-sample bridge

The posterior bridge is not a theorem and not empirical evidence. It demonstrates that posterior draws or particles from a continuous model can act as the finite support on which the exact Paper B logic operates.

Role:

- practical bridge after the exact benchmark;
- explicit limitation that guarantees are exact only conditional on the chosen finite support.

## One narrative for the main text

### Introduction

1. Ecologists can know a present state while remaining unable to distinguish futures.
2. More data can resolve target-irrelevant details and still leave the prediction ambiguous.
3. A finite evidence framework therefore needs to say both what the experiment identifies and what it is justified to report.
4. Paper B contributes four linked results: exact experiment quotient, minimal target-safe quotient, failure-aware reliable refinement, and risk-limited adaptive design.

### Results

1. **What did the experiment actually distinguish?** — experiment-induced quotient.
2. **Which of those distinctions matter for the future being asked about?** — target-safe quotient.
3. **Can the observation architecture reliably support that split?** — failure architecture.
4. **What should be measured next, and when should monitoring stop?** — risk-limited adaptive design.

### Discussion / conclusion

The final conclusion should not be “we provide a framework.” It should be:

> Ecological monitoring should be designed around distinctions among possible futures, not around resolution of the ecological state as a whole. Full identification is unnecessary when remaining distinctions do not change the target, and more information is insufficient when it does not separate target-relevant futures or is collected under a shared failure architecture.

## Main-text versus Supplement decision table

| Mathematical component | Main text | Methods/Supplement |
|---|---|---|
| experiment-induced quotient | theorem + ecological witness | exhaustive finite verification |
| honest set-valued reporting | theorem criterion | edge cases |
| unique target-safe quotient | theorem + minimality interpretation | full proof |
| imperfect finite non-detection | one boundary statement | exact repeat frontier |
| shared-mode availability ceiling | theorem/corollary + equal-effort example | inclusion–exclusion derivation |
| overlapping/dependent failures | concise assumption ladder | complete bounds |
| calibration bounds | short contract provenance | derivation and numerical details |
| multiple/heterogeneous thresholds | no | supplement |
| adaptive risk spending | one sentence if needed for implementation | detailed theorem notes |
| full-world EIG benchmark | main result figure | full grid |
| target-switch sensitivity | robustness table | JSON/grid |
| posterior-sample bridge | short practical demonstration | generator details |
| delayed-exposure closure witness | motivation or supplement | proof/code |

## Development gate

No additional theorem family should be added during submission preparation unless it closes one of these four reviewer-visible logical gaps:

1. the experiment quotient is not exact;
2. target-safe minimality is not proved;
3. failure architecture is not linked to trustworthy refinement;
4. the adaptive reporting contract does not control false resolution.

Everything else should be prose consolidation, proof completion, figure generation, literature positioning, or empirical demonstration.