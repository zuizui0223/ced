# Paper B publication-completion spine

## Fixed identity

**Working title:** Honest Ecological Prediction from Finite Evidence: Quotients, Failure Architecture, and Risk-limited Experiments

**Repository scope:** CED supplies the experiment, observation-error, and risk-control machinery. MRM supplies target-safe mechanism reporting and minimal candidate-safe quotients. CED is the active combined-manuscript repository; MRM remains theorem provenance and supporting implementation.

**Central question:** What can finite ecological evidence honestly justify under observation uncertainty, mechanism ambiguity, and intervention?

The CED–MRM bridge has passed the mathematical go/no-go gate because the joint presence × response-type witness uses both dimensions essentially and the target-safe minimal quotient connects the two repositories by a genuine minimality result. No new theorem family should be introduced during submission preparation.

## Publication abstract

Ecological monitoring rarely identifies a unique latent world: nondetection can mask presence, several mechanisms can predict the same observations, and interventions can be informative only under particular current states. We represent a finite ecological evidence problem by latent worlds, admissible experiments, observation contracts, and a report target. Every declared experiment induces an ecological quotient whose classes contain worlds producing the same complete record; deterministic reporting is justified exactly when the target is constant on each relevant class, and otherwise the honest conclusion is set-valued. We then characterize the unique coarsest observation-preserving, target-safe quotient stable under future actions, thereby retaining only distinctions needed for declared ecological conclusions. Observation failure architecture determines which quotient refinements can be trusted: shared failures impose resolution ceilings that replication within one mode cannot overcome, whereas independent or partially overlapping modes support different reliable refinements. Finally, adaptive experiment trees minimize expected cost or residual ambiguity subject to explicit correct-report and false-resolution constraints. A plant–pollinator example jointly involving uncertain interaction presence and ambiguous intervention response shows why more data need not justify a sharper prediction unless the experiment separates the target-relevant latent classes and its failure structure supports that separation.

## Introduction spine

### Problem

Finite ecological evidence can leave at least three distinct uncertainties entangled: whether an ecological entity or interaction is present, which candidate mechanism governs its response, and whether the observation process itself failed. Treating a point estimate, MAP mechanism, or positive detection as full resolution can therefore produce conclusions that the experiment does not logically support.

### Gap

Occupancy and imperfect-detection models quantify uncertainty about presence. Model selection and structural-uncertainty methods compare candidate mechanisms. Adaptive monitoring and experimental design choose additional observations. These literatures do not by themselves provide one exact object describing what a declared finite experiment identifies across both presence and mechanism dimensions, nor a unique minimal quotient retaining exactly the distinctions required for a target report under future intervention.

### Contribution hierarchy

1. **Experiment-induced Ecological Quotient.** A design partitions latent worlds by their complete records and determines the maximum exact information supplied by that experiment.
2. **Target-safe Minimal Quotient and Deterministic Report Criterion.** A deterministic report exists exactly when the target is constant on each compatible class; the unique coarsest observation-preserving, action-stable target-safe quotient removes irrelevant distinctions while preserving every declared target conclusion.
3. **Failure Architecture Determines Reliable Refinement.** Shared, overlapping, and independent failure structures produce different resolution ceilings and therefore different trustworthy quotient refinements at equal nominal effort.
4. **Adaptive Risk-limited Experiment Design.** Adaptive experiment trees are evaluated by correct, wrong, and ambiguous report probabilities and expected cost; feasible policies satisfy declared risk constraints rather than merely maximizing identification.

### Ecological conclusion

The framework says not only how uncertain a conclusion is, but whether the available evidence justifies making that conclusion at all, which latent distinctions remain unresolved, and what additional experiment can safely resolve the target at acceptable risk and cost.

## Results spine

### Result 1 — Experiment-induced ecological quotient

For design `D`, define `w ~_D w'` when the complete records generated under latent worlds `w` and `w'` agree. State one theorem package:

- every record-based report is constant on quotient classes;
- exact deterministic reporting of target `T` exists if and only if `T` is constant on every relevant class;
- otherwise the exact honest report is the set of target values represented in the compatible class;
- design refinement can only split, never merge, experiment-induced classes.

**Reviewer-facing interpretation:** The equivalence relation alone is elementary. The contribution is its integration with target reporting, CED partial-evidence classes, MRM mechanism ambiguity, noisy compatibility, and downstream risk-limited design.

**Ecological payoff:** It prevents a monitoring record from being interpreted more sharply than the latent worlds it can distinguish.

### Result 2 — Target-safe minimal quotient

State the existence and uniqueness of the coarsest equivalence relation that preserves current observable macrostate, preserves target reports under all declared future actions, and is stable under action successors.

The deterministic report criterion should be stated adjacent to this theorem rather than as a separate headline theorem.

**Reviewer-facing interpretation:** The theorem is not generic state minimization dressed in ecological language. Its role is to remove experiment-visible distinctions irrelevant to the declared report while retaining every distinction needed for candidate-safe intervention prediction.

**Ecological payoff:** It identifies the least mechanism typing or latent-state resolution required for a management conclusion; unnecessary biological distinctions are not demanded.

### Result 3 — Failure architecture and reliable refinement

Organize shared, overlapping, and independent failures as one comparative result. Detection formulas, Markov bounds, Chernoff bounds, Poisson-binomial tails, threshold searches, and calibration routines are supporting machinery.

The main claim is structural: failure architecture changes which experiment-induced splits can be trusted and can impose a non-removable availability ceiling even when within-mode replication increases.

**Reviewer-facing interpretation:** Avoid presenting a catalogue of probability inequalities. Use them only to prove or calculate the reliability of quotient refinement under declared contracts.

**Ecological payoff:** It explains why repeating one camera, assay, observer, or laboratory pipeline may not resolve ecological ambiguity when all repetitions share the same failure cause.

### Result 4 — Adaptive risk-limited experiment design

An adaptive policy maps past records to the next experiment and induces terminal leaves with:

- compatible target set;
- correct-report probability;
- wrong-report probability;
- ambiguity probability;
- expected cost.

Present finite policy optimization under declared correct, wrong, and cost constraints. Do not claim a universal optimal sequential-design theorem.

**Reviewer-facing interpretation:** The scientific objective is not shortest full identification. It is least-cost target resolution subject to an explicit false-resolution budget, allowing honest ambiguity when safe resolution is impossible.

**Ecological payoff:** Monitoring can stop once the management target is safely resolved, or retain a set-valued conclusion when further intervention is too costly or unreliable.

## Integrated ecological example

Use one rare plant–pollinator interaction across sites.

### Latent worlds

Each world combines:

- interaction or focal-pollinator presence/absence;
- response type to a declared floral manipulation, exclusion, or competitor-removal intervention.

### Experiment sequence

1. Passive monitoring leaves presence and response type jointly ambiguous.
2. A presence screen separates absent from present worlds but cannot distinguish response types among present worlds.
3. A response intervention resolves mechanism type only when presence has been established.
4. Shared camera, weather, access, or laboratory failure can merge the present response types again in the observed compatible set.
5. An adaptive policy performs response typing only after a positive presence screen.
6. Correct, wrong, ambiguous, and expected-cost outputs are compared across failure architectures.

### Required conclusion

The example must demonstrate a conclusion unavailable from CED or MRM alone: an experiment may resolve presence without justifying a deterministic management response, and the intervention that separates mechanisms may still fail to provide safe resolution under a shared failure architecture.

## Discussion spine

### What is new

The paper provides one finite decision language linking evidence, honest reporting, target-safe abstraction, observation failure, and adaptive intervention. Its novelty is structural and mathematical rather than computational: experiment records induce exact latent-world quotients, target relevance determines the unique minimal safe quotient, and failure/risk contracts determine which refinements can support a deterministic ecological conclusion.

### What is not claimed

- no inference of the latent-world family, priors, likelihoods, costs, or failure factors from data;
- no replacement for occupancy estimation or causal identification;
- no universal asymptotic consistency claim;
- no full partially observed stochastic-control solution;
- no assertion that a MAP mechanism is deterministic resolution;
- no claim that standard concentration inequalities are novel.

### Relation to adjacent literatures

- **Occupancy and imperfect detection:** estimate presence under observation error; this paper additionally tracks target-relevant mechanism ambiguity and exact compatible classes.
- **Structural uncertainty and multimodel inference:** retain several candidate models; this paper characterizes when their distinctions matter for a declared report and intervention.
- **Abstraction and bisimulation:** minimize behaviorally equivalent states; this paper uses an experiment- and target-relative quotient over latent ecological worlds with honest set-valued fallback.
- **Adaptive monitoring and experimental design:** select information-gathering actions; this paper constrains selection by wrong-resolution risk and target-safe stopping rather than full identification alone.
- **Ecological prediction:** the framework separates predictive ambiguity caused by latent mechanisms from ambiguity caused by observation failure.

### Limitations and next step

Bayesian, approximate, continuous, and large-state extensions should remain supporting or future work unless they materially strengthen one of the four central results. The current manuscript should prioritize finite exact transparency and ecological interpretability.

## Figure plan

1. **Evidence-to-report pipeline:** latent worlds → experiment records → quotient classes → deterministic or set-valued target report.
2. **Target-safe quotient:** full record quotient versus the coarser minimal quotient that preserves only target-relevant distinctions.
3. **Failure architecture:** equal-effort shared, overlapping, and independent designs showing different reliable refinement ceilings.
4. **Adaptive experiment tree:** presence screen, conditional mechanism intervention, terminal correct/wrong/ambiguous reports, and expected cost.

Use the same joint plant–pollinator worlds in every figure. Avoid separate CED and MRM example panels that make the manuscript look stitched together.

## Reviewer audit

### Criticism: “The quotient theorem is tautological identifiability.”

**Answer:** Acknowledge that indistinguishable records define equivalence. The nontrivial content is the target-constancy characterization, the unique minimal target-safe action-stable quotient, the joint presence × mechanism witness, and the reliability constraints on quotient refinement.

### Criticism: “This is two papers joined by notation.”

**Answer:** The integrated witness must use both dimensions essentially: detection resolves presence but not response type; intervention resolves response type conditionally on presence; shared failure can undo deterministic target resolution. Every main result is illustrated on this same object.

### Criticism: “The probability bounds dominate the mathematics.”

**Answer:** Move Markov, Chernoff, Poisson-binomial, calibration, and threshold-search details to Methods or Supplement. In the main text, they support the structural statement that failure architecture governs trustworthy refinement.

### Criticism: “Set-valued reporting is not practically useful.”

**Answer:** Set-valued output is the exact conclusion justified by the current experiment. The adaptive-design result then identifies whether an affordable experiment can safely reduce that set for the management target.

### Criticism: “The adaptive result is just brute-force policy search.”

**Answer:** Do not claim algorithmic novelty. The contribution is the risk-limited objective and its coupling to target-compatible quotient leaves; finite enumeration is implementation machinery for declared small systems.

### Criticism: “Ecologists already use occupancy models.”

**Answer:** Occupancy addresses presence uncertainty, whereas this framework jointly handles presence, candidate response mechanisms, intervention-dependent targets, and observation architectures that determine whether sharper prediction is logically warranted.

## Demotion and deletion rules

### Main text

- experiment-induced ecological quotient;
- deterministic target-report criterion and target-safe minimal quotient;
- structural comparison of failure architectures;
- adaptive risk-limited policy result;
- one integrated ecological example.

### Methods or Supplement

- calibration details;
- Markov, Chernoff, and Poisson-binomial derivations;
- heterogeneous threshold panels;
- threshold search and implementation helpers;
- replay utilities and exhaustive finite oracles;
- posterior updates and one-step value-of-information diagnostics;
- secondary product bounds and alternative witnesses.

### Exclude

- theorem families unrelated to the four central results;
- standalone CED and MRM narratives repeated inside the combined paper;
- unsupported empirical claims;
- full sequential Bayesian control claims;
- computational additions that do not improve the manuscript argument.

## Submission gate

Paper B is ready for journal selection only when:

- one title, abstract, introduction, notation table, and ecological example cover both repositories;
- the target-safe quotient theorem visibly proves existence, coarseness, stability, and uniqueness;
- the experiment-induced quotient is not oversold as a new equivalence-relation idea;
- the joint presence × response-type witness appears in all four result sections;
- detection inequalities occupy supporting Methods or Supplement rather than the headline narrative;
- adaptive policies report correct, wrong, ambiguous, and expected-cost quantities under an explicit risk contract;
- related work directly addresses occupancy, imperfect detection, structural uncertainty, abstraction, and adaptive monitoring;
- all numerical values are generated by deterministic replay;
- the manuscript can be read without knowing the CED or MRM repository histories.
