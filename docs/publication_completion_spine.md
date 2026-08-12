# Paper B publication-completion spine

## Fixed identity

**Current title:** **From Ecological States to Distinguishable Futures: Target-safe Prediction from Finite Evidence**

**Repository role:** CED is the active combined-paper repository. Earlier CED closure/detection results and MRM quotient results remain theorem provenance, but the submission must be readable without knowing either repository history.

**Central question:**

> Which distinctions among possible ecological futures can finite evidence honestly resolve, and which additional experiment can resolve the declared prediction at acceptable error and cost?

**Central conclusion:**

> More ecological information does not necessarily produce more defensible ecological prediction. Monitoring should resolve the latent distinctions that separate possible futures, not identify the ecological state as completely as possible for its own sake.

The theorem inventory is frozen. No new theorem family should be introduced during submission preparation unless it repairs a reviewer-visible logical gap in one of the four headline Results.

## Four-result mathematical spine

### Result 1 — Experiment-induced ecological quotient and honest reporting

A deterministic experiment partitions finite latent worlds by complete record. Any record-based report factors through that partition. A deterministic target report is justified exactly when the target is constant on the relevant compatible class; otherwise the sharp exact output is the set of compatible target values.

For stochastic likelihood kernels, the analogous logical object is the positive-likelihood compatible class. Posterior risk-limited reporting is deliberately distinguished from this support-level exact criterion.

**Status:** theorem statement in main text; implementation in `ced/experiment_quotient.py`; formal deterministic and stochastic-support proofs in `manuscript/paper_b_supplement.tex`.

### Result 2 — Unique coarsest target-safe quotient

Starting from the current record partition, repeatedly refine by:

- target value; and
- successor block under every declared action.

The finite refinement reaches a fixed point that preserves the current record, is target-constant, and has deterministic quotient successors. Every other valid target-safe partition refines this fixed point, so it is the unique coarsest target-safe quotient. The quotient preserves target reports after every finite declared action word.

**Ecological meaning:** full mechanism identification is unnecessary when remaining differences cannot change the declared future; a small latent distinction is indispensable when it can reverse that future.

**Status:** generic implementation in `ced/target_safe_quotient.py`; exhaustive all-partition minimality oracle in `tests/test_target_safe_quotient.py`; full proof in the Supplement.

### Result 3 — Failure architecture determines trustworthy refinement

A target-relevant experiment can be nominally separating but unreliable under observation failure. The structural result is that within-mode repetition and independent failure diversity are different design resources.

If each of `m` independent modes is operational with probability **at least** `a`, then

```text
1 - (1 - a)^m
```

is the supremum of the joint-detection **guarantee that can be certified uniformly over that lower-bound contract** as within-mode repetition grows. It is not an upper bound on realized detection when true mode availability is higher than `a`. With exact failure probabilities, an actual realized ceiling can be stated under the corresponding exact contract.

**Ecological meaning:** many reads sharing one weather, access, observer, camera, sensor, or laboratory failure domain need not provide the evidence of equally many independent opportunities.

**Status:** corrected theorem note in `docs/mode_diverse_detection_theorem.md`; API semantics in `ced/mode_detection.py`; regression counterexample in tests; least-favourable formula, monotonic-coupling argument, and limit proof in the Supplement.

### Result 4 — Adaptive risk-limited target resolution

A finite adaptive policy maps records to a next experiment or stopping decision. Terminal outcomes are evaluated by:

- correct deterministic-report probability;
- wrong deterministic-report probability;
- honest ambiguity probability; and
- expected cost.

The scientific objective is least-cost defensible resolution of the declared target under an explicit false-resolution contract, not shortest full identification. Unsupported terminal records remain set-valued.

**Status:** schema-v5 exact benchmark and adaptive policy code; finite least-cost existence proof in the Supplement.

## Decisive computational evidence

### Exact 16-world benchmark

The benchmark crosses a management-relevant state, binary response type, and a four-level target-irrelevant attribute.

At response accuracy 0.95:

- perfect nuisance measurement gives 2 bits of full-world information;
- response measurement gives about 0.714 bits;
- full-world EIG therefore selects the nuisance experiment;
- nuisance target-resolution probability is 0;
- response target-resolution probability is 1 in the detected-state contrast.

At the validated baseline used in the manuscript (state sensitivity 0.95, response accuracy 0.99, three independent screens, no common failure):

- target-safe: correct 0.9944, wrong 0.00557, ambiguity 0, expected cost 4.129;
- full-world EIG: correct 0.4500, wrong 0.000069, ambiguity 0.5499, expected cost 2.479;
- full identification: same target-report probabilities as target-safe, expected cost 4.679.

The benchmark is a possibility/mechanism demonstration, not a universal claim that target-safe design dominates EIG or management VOI.

### Reviewer robustness

The manuscript already includes:

- a target-switch analysis showing the same worlds/priors/likelihoods select different experiments when the declared target changes;
- false-resolution sensitivity at 1%, 5%, and 10%;
- explicit positioning inside the broader Bayesian decision-theoretic/VOI tradition.

### Posterior-sample bridge

A deterministic continuous invasion-control demonstration generates posterior draws over control effect, spread rate, and source pathway. Treating 500, 2,000, and 10,000 posterior draws as finite supports yields stable selection of the response assay for an eradication-versus-containment target.

This is **not empirical validation**. It demonstrates how posterior draws, particles, scenarios, or ensemble members can feed the exact finite logic while keeping the conclusion conditional on the chosen support.

## Main-text narrative

### Introduction

1. A present ecological state can be well estimated while several compatible worlds imply different futures.
2. More data can sharpen target-irrelevant details without improving the declared prediction.
3. A useful finite evidence layer must identify what the experiment distinguishes, which distinctions matter for the target, whether the observation architecture can support those distinctions, and whether a deterministic report is safe.
4. The four Results answer those questions in order.

### Results order

1. **What did the experiment actually distinguish?** — experiment-induced quotient.
2. **Which of those distinctions matter for the future?** — target-safe quotient.
3. **Can the observation architecture reliably support that split?** — failure architecture.
4. **What should be measured next, and when should monitoring stop?** — risk-limited adaptive design.

### Discussion / conclusion

Do not end with “we provide a framework.” End with the ecological shift:

> move from resolving the ecological state as a whole to resolving only the distinctions that separate possible futures.

## Relationship to adjacent literatures

The final literature review must position Paper B against primary sources in at least these areas:

- occupancy and imperfect detection, including false-positive detection where relevant;
- structural uncertainty and multimodel inference;
- Bayesian experimental design and active learning;
- ecological value of information and decision analysis;
- adaptive monitoring;
- partial identification / set-valued inference;
- state abstraction, bisimulation, or partition refinement where mathematically relevant;
- ecological forecasting and limits of predictive inference.

The paper must not claim that VOI is unable to target decisions, that partition refinement itself is new, or that standard concentration/calibration inequalities are novel.

## Ecological examples: current role

The main text uses several short ecological interpretations and a concrete invasion-management example. The posterior bridge also uses invasion-control language because it naturally distinguishes current occurrence, management response, and source pathway.

A real public dataset or published posterior output would strengthen the paper, but it is **not currently part of the theorem validity claim** and should not be fabricated or inserted merely to make the paper look empirical. If added, it should demonstrate a management-facing experiment choice that changes because of the declared target or failure architecture.

The old requirement that every figure use a rare plant–pollinator witness is retired. Plant–pollinator systems may be used later only if they provide a genuinely better empirical demonstration.

## Figure status and remaining visual work

Already generated from validated computation:

1. user workflow / evidence-to-report pipeline;
2. full-world information gain versus target-resolution contrast;
3. terminal correct/wrong/ambiguous strategy comparison;
4. target-switch and threshold-sensitivity tables;
5. posterior-sample bridge table.

Still useful before submission:

- one compact schematic of the full record partition versus the coarser target-safe quotient;
- one failure-architecture figure comparing equal nominal effort across shared versus independent modes, with wording explicitly distinguishing worst-case guarantee ceilings from realized-probability ceilings.

These figures should explain Results 2 and 3, not introduce new mathematics.

## Supporting mathematics: do not re-promote

The following remain valid and useful but are not equal-weight headline Results:

- delayed-exposure / no-uniform passive closure theorem;
- one-sided imperfect-detection repeat frontier;
- overlapping/dependent failure bounds;
- calibration confidence bounds;
- multiple and heterogeneous thresholds;
- expected false-discovery budgets;
- adaptive alpha spending;
- Markov, Chernoff, and Poisson-binomial concentration results.

Use them only to support the four-result spine or place them in Methods/Supplement/future work.

## Proof and reproducibility status

Completed:

- main four-result story contract is CI-tested;
- generic target-safe quotient implementation exists in CED;
- target-safe minimality has an exhaustive finite partition oracle;
- Result 3 lower-bound/realized-ceiling semantics have a regression counterexample;
- main manuscript compiles in CI;
- standalone formal Supplement compiles in CI;
- Python 3.10, 3.11, and 3.12 test matrices pass;
- schema-v5 benchmark, reviewer robustness, figures, tables, and posterior bridge regenerate deterministically.

## Remaining submission tasks, in priority order

### 1. Primary-source literature and novelty-boundary audit

Expand the current sparse bibliography and write a claim-by-claim related-work boundary. This is now the largest reviewer-facing weakness.

### 2. Results 2–3 explanatory figures

Generate one target-safe quotient figure and one failure-architecture guarantee figure directly from deterministic witnesses.

### 3. Editorial compression

Remove duplicate explanation between the canonical manuscript and injected reviewer sections. Ensure Abstract, Introduction, four Results, Robustness section, Discussion, and Conclusion use one terminology set.

### 4. Empirical strengthening, only if a defensible dataset is available

Prefer a public dataset or already-published posterior/model output that can be reproduced without extensive new inference. Treat this as external validation/illustration, not as theorem evidence.

### 5. Journal-format submission package

Tune title/keywords/length/references for the selected journal, produce final main/Supplement PDFs, archive the deterministic artifacts, and create a stable release/tag.

## Submission gate

Paper B should not be submitted until:

- the primary-source literature review is complete enough that every novelty claim has an explicit nearest-neighbour boundary;
- the target-safe quotient theorem is described as a target-relative refinement/minimality result rather than invention of equivalence relations;
- Result 3 consistently distinguishes lower-bound guarantee ceilings from realized-probability ceilings;
- VOI/Bayesian design are represented as compatible broader decision-theoretic frameworks, not straw-man alternatives;
- exact support-level reporting is distinguished from posterior risk-limited reporting;
- figures and tables are generated from deterministic artifacts;
- main and Supplement compile from the submission commit;
- all numerical claims match generated outputs;
- no new theorem family has been added merely for breadth;
- the paper can be read without knowledge of CED/MRM repository history.
