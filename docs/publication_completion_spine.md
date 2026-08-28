# Paper B publication-completion spine

## Fixed identity

**Current title:** **When Full-world Information Misses the Ecological Target: Failure-diverse Evidence for Distinguishable Futures**

**Repository role:** CED is the active combined-paper repository. Earlier CED closure/detection results and MRM quotient results remain theorem provenance, but the submission must be readable without knowing either repository history.

**Central question:**

> Which distinctions among possible ecological futures can finite evidence honestly resolve, and which additional experiment can resolve the declared prediction at acceptable error and cost?

**Central conclusion:**

> More ecological information does not necessarily produce more defensible ecological prediction. Monitoring should resolve the latent distinctions that separate possible futures, not identify the ecological state as completely as possible for its own sake.

The theorem inventory is frozen. No new theorem family should be introduced during submission preparation unless it repairs a reviewer-visible logical gap in one of the four headline Results.

**Presentation contract:** logical dependency remains Result 1 $\rightarrow$ Result 2 $\rightarrow$ Result 3 $\rightarrow$ Result 4. The main text uses consequence-first order: Result 3, Result 4 and its benchmark, then Results 1--2 as exact reporting infrastructure. This is an editorial inversion, not theorem renumbering or a change to any proof.

## Four-result mathematical spine

### Result 1 — Experiment-induced ecological quotient and honest reporting

A deterministic experiment partitions finite latent worlds by complete record. Any record-based report factors through that partition. A deterministic target report is justified exactly when the target is constant on the relevant compatible class; otherwise the sharp exact output is the set of compatible target values.

For stochastic likelihood kernels, the analogous logical object is the positive-likelihood compatible class. Posterior risk-limited reporting is deliberately distinguished from this support-level exact criterion.

**Status:** theorem statement in main text; implementation in `ced/experiment_quotient.py`; formal deterministic and stochastic-support proofs in `manuscript/paper_b_supplement.tex`.

### Result 2 — Unique coarsest target-safe quotient

Starting from the current record partition, repeatedly refine by target value and successor block under every declared action. The finite refinement reaches a fixed point that preserves the current record, is target-constant, and has deterministic quotient successors. Every other valid target-safe partition refines this fixed point.

**Status:** generic implementation in `ced/target_safe_quotient.py`; exhaustive all-partition minimality oracle in `tests/test_target_safe_quotient.py`; full proof in the Supplement; deterministic explanatory figure generated from the implementation.

### Result 3 — Failure architecture determines trustworthy refinement

If each of `m` independent modes is operational with probability **at least** `a`, then

```text
1 - (1 - a)^m
```

is the supremum of the joint-detection **guarantee that can be certified uniformly over that lower-bound contract** as within-mode repetition grows. It is not an upper bound on realized detection when true mode availability is higher than `a`.

**Status:** corrected theorem note and API semantics; regression counterexample; formal least-favourable proof in the Supplement; equal-effort explanatory figure generated directly from `ModeDiverseDetectionPanel`.

### Result 4 — Adaptive risk-limited target resolution

A finite adaptive policy maps records to a next experiment or stopping decision. Terminal outcomes are evaluated by correct deterministic-report probability, wrong deterministic-report probability, honest ambiguity probability, and expected cost.

**Status:** schema-v5 exact benchmark and adaptive policy code; finite least-cost existence proof in the Supplement.

## Computational evidence

### Exact 16-world benchmark

At response accuracy 0.95, a perfect nuisance measurement gives 2 bits of full-world information whereas the response measurement gives about 0.714 bits. Full-world EIG therefore selects the nuisance experiment even though it does not resolve the focal target.

**Interpretation boundary:** this is a counterexample to one untargeted objective—full-world entropy reduction. It is not a novelty proof against Bayesian experimental design, targeted/goal-oriented OED, or management VOI.

At the validated baseline used in the manuscript:

- target-safe: correct 0.9944, wrong 0.00557, ambiguity 0, expected cost 4.129;
- full-world EIG: correct 0.4500, wrong 0.000069, ambiguity 0.5499, expected cost 2.479;
- full identification: same target-report probabilities as target-safe, expected cost 4.679.

### Reviewer robustness

Completed:

- target-switch analysis;
- false-resolution sensitivity at 1%, 5%, and 10%;
- explicit VOI/Bayesian-design/goal-oriented-OED boundary;
- exact-support versus posterior-risk distinction.

### Posterior-sample bridge

The deterministic invasion-control bridge uses 500, 2,000, and 10,000 posterior draws as finite supports and produces stable experiment choice for the declared eradication-versus-containment target.

This is **not empirical validation**. It demonstrates how posterior draws, particles, scenarios, or ensemble members can feed the finite logic.

## Nearest-neighbour novelty boundary

The primary-source audit is maintained in `docs/paper_b_literature_boundary_audit.md`.

Established ingredients that Paper B must not claim in isolation include:

- occupancy/imperfect detection and false-positive observation models;
- partial identification and sharp set-valued inference;
- set-valued prediction with user-specified finite-sample risk control;
- structural uncertainty, model averaging, and ecological forecasting;
- Bayesian experimental design;
- targeted and goal-oriented OED for predictions / QoIs;
- ecological value of information;
- adaptive monitoring and adaptive management;
- state abstraction, bisimulation, and partition refinement.

The safe residual contribution is:

> Paper B links the finite compatible-world structure induced by a realized ecological record to a sharp ecological target set, computes the coarsest action-stable target-preserving refinement, checks whether observation failure permits that refinement to be trusted, and evaluates adaptive stopping / experiment choices under an explicit false-resolution contract.

Particularly important non-claims:

- target-oriented experiment selection is not new;
- parameter/state EIG versus prediction/QoI EIG is not new;
- set-valued prediction plus risk control is not new;
- partition refinement is not new;
- the benchmark is not novelty evidence against predictive OED or VOI.

## Figure status

Completed and generated from tested code:

1. user workflow / evidence-to-report pipeline;
2. **current record → target-safe quotient → full latent identity** figure for Result 2;
3. **equal effort / different failure diversity** figure for Result 3, with worst-case guarantee semantics;
4. full-world information gain versus target-resolution contrast;
5. terminal correct/wrong/ambiguous strategy comparison;
6. target-switch and threshold-sensitivity tables;
7. posterior-sample bridge table.

No additional theorem figure is required before submission unless a reviewer-facing logical gap appears.

## Editorial status

Completed:

- four-result main-text reorganization;
- future-focused title and conclusion;
- formal standalone Supplement;
- Related Work rewritten to concede the strongest nearby methods;
- injected robustness section compressed so it no longer repeats the full literature review;
- terminology aligned around compatible worlds, target set, target-safe quotient, failure architecture, false resolution, and honest ambiguity.

Remaining editorial work should be copyediting, not conceptual expansion.

## Empirical-strengthening decision

A real public dataset or published posterior/model output would strengthen external validity, but only if it exercises something beyond standard target-oriented OED.

**Add an empirical example only if it demonstrates at least one of:**

1. the realized record leaves a nontrivial sharp target set even though a state estimate appears confident;
2. the coarsest target-safe quotient discards model distinctions that an empirical pipeline would otherwise retain;
3. shared versus independent observation failure changes what target conclusion can be certified;
4. a false-resolution contract changes the stopping/report decision in a management-facing way.

**Do not add an empirical example merely to show that a target-specific experiment is useful.** Targeted/goal-oriented OED already establishes that principle, and a weak case study would increase scope without strengthening the residual novelty.

Current default decision: **do not delay submission for a synthetic or weak empirical case.** Add a public empirical demonstration only if an immediately reproducible dataset/model output satisfies one of the four criteria above.

## Remaining submission tasks, in priority order

### 1. Final risk-set literature boundary

The audit now records Bates et al. (2021) as a nearest neighbour for finite-sample risk-controlled prediction sets. Add it to the manuscript bibliography only if the final prose retains novelty-adjacent wording about risk-controlled set-valued prediction.

### 2. Final editorial/citation pass

- remove residual duplicate wording;
- verify exact bibliographic metadata and journal style;
- ensure every citation is attached to the claim it bounds;
- keep GO-OED, VOI, prediction-set, and bisimulation methods in their strongest form.

### 3. Decide empirical example by the gate above

Do not initiate a new empirical analysis unless it adds reportability/failure-architecture evidence unavailable from the current theorem/benchmark package.

### 4. Journal-format package and archive

- tune title, abstract length, keywords, and reference style for the selected journal;
- build final main and Supplement PDFs from one commit;
- archive deterministic JSON/CSV/TikZ outputs;
- create stable release/tag and DOI-ready archive if desired.

## Submission gate

Paper B should not be submitted until:

- every novelty claim has an explicit primary-source nearest-neighbour boundary;
- targeted/goal-oriented OED is acknowledged as established prediction/QoI-focused design;
- risk-controlled set-valued prediction is not claimed as novel in isolation;
- the full-world-EIG benchmark is not presented as novelty evidence against predictive OED;
- the target-safe quotient theorem is described as a target-relative refinement/minimality result rather than invention of equivalence relations;
- Result 3 consistently distinguishes lower-bound guarantee ceilings from realized-probability ceilings;
- VOI/Bayesian design are represented as compatible broader decision-theoretic frameworks;
- exact support-level reporting is distinguished from posterior risk-limited reporting;
- all figures and tables are generated from deterministic artifacts;
- main and Supplement compile from the submission commit;
- all numerical claims match generated outputs;
- no new theorem family is added merely for breadth;
- the paper can be read without knowledge of CED/MRM repository history.
