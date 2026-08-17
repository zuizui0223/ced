# Paper B theorem consolidation

## Purpose

This document resolves the tension between the older standalone-CED manuscript architecture and the current submission-facing Paper B. It is a submission-facing architecture decision, not a new theorem family.

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
- `manuscript/paper_b_supplement.tex`, deterministic and stochastic-support proofs

Do not oversell the equivalence relation itself as novel. The contribution is its coupling to target reporting, observation error, future actions, and risk-limited experiment design.

### Result 2 — Unique coarsest target-safe quotient

The full experiment-induced quotient may preserve biological distinctions that are irrelevant to the declared prediction. Paper B therefore constructs the unique coarsest record-preserving, target-constant, action-stable refinement of the evidence-induced partition.

Main-text interpretation:

> resolve only latent distinctions that can imply different ecological futures.

**Critical evidence boundary.** This quotient is the **minimum refinement that would be sufficient** for deterministic target-safe state tracking; it is not a claim that the current record already identifies which refined block contains the true world. If one current compatible record class contains multiple target-safe blocks and the observation contract has not resolved them, the honest current report remains the set of compatible target values from Result 1. Result 2 therefore supplies a target-relative **resolution requirement** for subsequent experiment design, while Results 3–4 determine when additional evidence can credibly satisfy that requirement.

This is the result that turns the paper from generic identifiability into target-relative ecological prediction without confusing required distinctions with already observed distinctions.

Provenance:

- neutral finite target/action-stable refinement developed in the earlier CED–MRM bridge work, now treated under CREST as **shared classical substrate rather than a combined theorem claim**;
- `ced/target_safe_quotient.py`, generic finite partition-refinement implementation initialized from the CED evidence/record partition;
- `tests/test_target_safe_quotient.py`, target-relativity and exhaustive all-partition minimality oracle;
- `manuscript/paper_b_supplement.tex`, complete existence, uniqueness, minimality, termination, and finite-action-word preservation proofs.

CREST firewall: MRM's minimal candidate-safe quotient is the mechanism-relative specialization in which latent worlds are observable-state × response-type pairs and the scientific output is mechanism-safe prediction. CED's Result 2 begins from an evidence-induced partition and asks what target-relevant refinement the evidence architecture must support. Generic finite partition refinement is not claimed as independent novelty by either repository.

The deterministic report criterion belongs adjacent to Results 1–2 and should not compete as a separate headline theorem.

### Result 3 — Failure architecture determines trustworthy quotient refinement

A nominal experiment may separate two worlds in an ideal record model yet fail to support that split under imperfect observation. The headline statement is structural:

> repetition inside one shared failure domain is not equivalent to independent failure diversity.

Main-text claims:

- finite negative evidence does not become deductive absence under imperfect sensitivity;
- when mode availability is known only through a lower bound `a`, the contract has a worst-case guarantee ceiling `1-(1-a)^m` that arbitrarily many within-mode repeats cannot raise;
- this quantity is not an upper bound on realized detection when true availability exceeds `a`;
- the equal-effort witness shows that allocating effort across independent modes can support a substantially stronger worst-case guarantee than concentrating the same raw replicate count inside one shared mode.

Provenance:

- `docs/imperfect_detection_theorem.md`
- `docs/mode_diverse_detection_theorem.md`
- `ced/mode_detection.py`
- `manuscript/paper_b_supplement.tex`, least-favourable frontier and guarantee-ceiling proof
- overlapping/dependent-repeat theorem notes and deterministic replay

Main text should show the structural worst-case guarantee ceiling and one equal-effort contrast. Detailed heterogeneous thresholds, Markov/Chernoff/Poisson-binomial bounds, and calibration algebra belong in Methods or Supplement.

### Result 4 — Adaptive risk-limited target resolution

A policy maps observed records to a next experiment or stopping decision. Terminal leaves are evaluated by:

- correct deterministic report probability;
- wrong deterministic report probability;
- honest ambiguity probability;
- expected cost.

Main-text claim:

> within a declared finite policy family, the scientific objective is least-cost defensible target resolution under an explicit false-resolution contract, not full latent-world identification.

The schema-v5 benchmark is the decisive counterexample: full-world information gain selects a target-irrelevant measurement because it supplies more entropy reduction, whereas target-safe design selects the experiment that resolves the declared prediction.

The target-switch and threshold-sensitivity analyses are robustness checks for this result, not separate theorem families. The finite least-cost existence argument is formalized in `manuscript/paper_b_supplement.tex`; the substantive content remains the shared terminal reporting contract and experiment-choice comparison. No claim is made here of a globally optimal policy over an undeclared infinite policy space.

## Supporting mathematics: keep, but do not promote to equal-weight Results

### Delayed-exposure / no-uniform passive closure theorem

`ced/delayed.py` proves a useful impossibility witness: for any proposed passive horizon, a legal delayed family can remain exterior-blind through that horizon and reveal a distinction later.

Role in Paper B:

- one motivating paragraph or Supplement proposition illustrating why finite passive non-detection cannot generally certify that all future-relevant distinctions have been exhausted;
- provenance for the broader finite-evidence philosophy.

Do **not** make this a fifth main result in Paper B. Its primary object is ecological closure, whereas Paper B's central object is target reportability.

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
4. Paper B contributes four linked results: exact experiment quotient, minimal target-safe resolution requirement, failure-aware reliable refinement, and risk-limited adaptive design.

### Results

1. **What did the experiment actually distinguish?** — experiment-induced quotient.
2. **Which additional distinctions would be sufficient for the future being asked about?** — target-safe quotient as required refinement.
3. **Can the observation architecture reliably support that split?** — failure architecture and worst-case guarantee under the declared observation contract.
4. **What should be measured next, and when should monitoring stop?** — risk-limited adaptive design.

### Discussion / conclusion

The final conclusion should not be “we provide a framework.” It should be:

> Ecological monitoring should be designed around distinctions among possible futures, not around resolution of the ecological state as a whole. Full identification is unnecessary when remaining distinctions do not change the target, and more information is insufficient when it does not separate target-relevant futures or is collected under a shared failure architecture.

## Main-text versus Supplement decision table

| Mathematical component | Main text | Methods/Supplement |
|---|---|---|
| experiment-induced quotient | theorem + ecological witness | deterministic factorization proof + stochastic-support extension |
| honest set-valued reporting | theorem criterion | sharpness proof and support-level distinction |
| unique target-safe quotient | theorem + required-resolution interpretation | fixed-point existence/uniqueness proof + finite-action-word corollary |
| imperfect finite non-detection | one boundary statement | exact repeat frontier |
| shared-mode worst-case guarantee ceiling | theorem/corollary + equal-effort example | least-favourable formula, monotonic coupling, limit proof |
| overlapping/dependent failures | concise assumption ladder | complete bounds |
| calibration bounds | short contract provenance | derivation and numerical details |
| multiple/heterogeneous thresholds | no | supplement |
| adaptive risk spending | one sentence if needed for implementation | detailed theorem notes |
| finite policy existence | theorem statement | finite minimization proof |
| full-world EIG benchmark | main result figure | full grid |
| target-switch sensitivity | robustness table | JSON/grid |
| posterior-sample bridge | short practical demonstration | generator details |
| delayed-exposure closure witness | motivation or supplement | proof/code |

## Development gate

No additional theorem family should be added during submission preparation unless it closes one of these four reviewer-visible logical gaps:

1. the experiment quotient is not exact;
2. target-safe minimality is not proved or not matched by the generic implementation;
3. failure architecture is not linked to trustworthy refinement with correctly oriented probability guarantees;
4. the adaptive reporting contract does not control false resolution.

Everything else should be prose consolidation, proof completion, figure generation, literature positioning, or empirical demonstration.
