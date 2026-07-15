# Reviewer audit — combined CED + MRM paper

## Proposed paper

**Finite Evidence and Honest Ecological Prediction under Observation and Mechanism Uncertainty**

Alternative:

**What Finite Ecological Experiments Can Justify: Detection Error, Mechanism Ambiguity, and Intervention Design**

## Editorial verdict

**Promising but not yet ready as a combined paper.**

CED and MRM share a deep structure, but the current theorem packages use different
latent objects:

- CED distinguishes hidden presence, exposure, and observation coordinates;
- MRM distinguishes hidden mechanism response types.

A manuscript that simply presents CED followed by MRM will look like an imperfect-
detection paper attached to a mechanism-uncertainty paper. A strong combined paper
requires one bridge theorem that makes both special cases of a common finite
evidence problem.

## Required bridge theorem

Let:

- `W` be a finite set of latent ecological worlds;
- `D` be a declared adaptive or nonadaptive experiment design;
- `R_D(w)` be the set or distribution of observation records generated under world
  `w`;
- `T(w)` be the ecological report target, such as coordinate presence, a future
  transition, or a mechanism-safe macro-law.

Define two worlds as observationally equivalent when the declared design cannot
separate them under the relevant observation contract.

### Exact version

For deterministic records,

```text
w ~_D w' iff record_D(w) = record_D(w').
```

An exact deterministic report based only on the record exists iff

```text
w ~_D w'  implies  T(w) = T(w').
```

The coarsest exact report is the quotient of latent worlds by the joint relation
that preserves the observation record and the report target.

### Error-tolerant version

With bounded-support or probabilistic observation error, a record leaves a
compatible set or posterior over observational equivalence classes. A deterministic
report is justified only if the target is constant over the retained support;
otherwise the report must remain set-valued, typed, or posterior-ambiguous.

This theorem would unify:

- CED's exact partial panel quotient;
- CED's residual unprobed classes;
- MRM's candidate-safe quotient;
- MRM's universal/typed/set-valued reporting criterion;
- active discrimination as adaptive quotient refinement;
- detection and false-alert bounds as risk guarantees on quotient refinement.

## Likely reviewer first impression

### Positive

- The paper connects monitoring design to the honesty of ecological prediction.
- It separates latent ecological ambiguity from observation error rather than
  conflating them.
- It gives an operational criterion for when deterministic prediction is justified.
- Shared failure and non-reset dependence make the monitoring theory more realistic
  than simple independent-repeat calculations.
- Minimal quotient and active discrimination provide a constructive response to
  ambiguity.

### Immediate concerns

1. **Is this just occupancy/detection theory plus Bayesian model selection?**
2. **What is new beyond standard sufficient statistics, identifiability, and
   decision trees?**
3. **Why are presence coordinates and mechanism types in the same theorem?**
4. **Does the paper estimate any ecological process from data?**
5. **Are the probability bounds and VOI calculations generic textbook material?**
6. **Is the manuscript too broad to have one ecological audience?**

## Core novelty that is defensible

The novelty is not imperfect detection, Bayesian updating, multiple testing,
value of information, or active learning in general.

The defensible contribution would be:

1. a finite operational quotient theorem linking experiment design to the exact
   ecological reports it can justify;
2. a report criterion: deterministic prediction is valid exactly when the target
   is constant over the record-compatible latent class;
3. a minimal observation-preserving quotient retaining only distinctions that
   declared future actions can expose;
4. a replication-architecture theorem showing how resetability, independent modes,
   overlapping failures, and common-mode ceilings alter the probability of correct
   quotient refinement;
5. a calibrated risk ledger for heterogeneous and adaptive designs.

## Main rejection risks

### Risk 1 — no genuine unification

Without the bridge theorem, reviewers will see two manuscripts compressed into one.

**Required fix:** prove and foreground the experiment-induced quotient theorem.
Every subsequent result must be introduced as one of three questions:

- what latent distinctions remain observationally equivalent?
- does the report target vary inside the retained class?
- with what probability does a noisy design refine the class correctly?

### Risk 2 — generic statistical machinery

Binomial tails, Bonferroni, Chernoff, Bayesian updating, and entropy are standard.

**Required fix:** place formulas such as Chernoff concentration, ordinary posterior
updates, and one-step VOI in methods or supplement. The headline must be the
structural quotient and report criterion, not the probability inequalities.

### Risk 3 — abstract ecology

A finite-world formalism can appear detached from ecology.

**Required fix:** one worked example must include both presence uncertainty and
mechanism ambiguity. Recommended example: multi-site monitoring of a rare
plant–pollinator interaction under alternative response mechanisms, with cameras
or eDNA, shared weather/batch failures, controls, and an adaptive manipulation.

### Risk 4 — exactness and declared contracts

Reviewers may object that candidate sets, error bounds, and action grammars are
assumed rather than inferred.

**Required fix:** state clearly that the paper is a design and reporting audit, not
an inference pipeline. Show how empirical models can supply the declared candidate
set and calibration bounds, but do not claim to estimate them here.

### Risk 5 — excessive theorem inventory

CED has many technical layers and MRM has many reporting/design extensions.

**Required fix:** four main results only. Everything else becomes a corollary,
assumption ladder, implementation note, or supplement.

## Recommended four-result hierarchy

### Result 1 — Experiment-induced ecological quotient

A declared experiment partitions latent ecological worlds by the records it can
produce. This quotient is the exact information content of the design.

This is the new bridge theorem and must be proven before combining the papers.

### Result 2 — Honest report criterion and minimal safe quotient

A deterministic report is justified iff the report target is constant on every
record-compatible class. Otherwise retain the relevant response type or report a
set-valued/posterior-ambiguous target. The coarsest exact report is the minimal
observation-preserving candidate-safe quotient.

### Result 3 — Replication architecture controls reliable refinement

Under observation error, the probability of reaching the correct quotient class
depends on sensitivity, false positives, resettable repeats, independent modes,
overlapping latent failure factors, and non-reset dependence. Raw repeat count is
not evidence diversity.

### Result 4 — Adaptive risk-limited discrimination

Calibration controls provide conservative error contracts. Heterogeneous thresholds,
conditional alpha spending, and cost-aware active discrimination allocate effort
while maintaining explicit false-alert or ambiguity-resolution guarantees.

## Recommended story

```text
Ecological data do not identify a world; an experiment only partitions possible worlds.
        ↓
A deterministic ecological prediction is valid only if all worlds left in the same
record class agree on the prediction target.
        ↓
If they disagree, type information or set-valued/posterior ambiguity must remain.
        ↓
Interventions refine the latent class, but imperfect and shared detection limits how
reliably they do so.
        ↓
Calibration, failure-aware replication, and adaptive risk spending determine which
additional experiment is justified.
```

## Main-text content

- finite latent-world and experiment setup;
- experiment-induced quotient theorem;
- deterministic report criterion;
- minimal candidate-safe quotient;
- one mechanism-ambiguity frontier witness;
- replication architecture theorem;
- calibrated adaptive discrimination framework;
- one integrated ecological worked example;
- four figures.

## Supplement content

- delayed closure witness, unless needed in the opening motivation;
- all binomial-tail derivations;
- Bonferroni, Markov, Poisson-binomial, and Chernoff details;
- threshold-search helpers;
- full Bayesian update derivation;
- one-step VOI calculations;
- additional failure-factor examples;
- replay schemas and exhaustive finite oracles.

## Suggested figures

1. **Experiment-induced quotient** — latent worlds collapsed into record classes,
   with one class agreeing and another disagreeing on a future target.
2. **Honest reporting ladder** — universal deterministic, typed/minimal quotient,
   set-valued, posterior-ambiguous.
3. **Replication architecture** — equal read budgets under one shared mode,
   independent modes, overlapping modes, and non-reset repeats.
4. **Adaptive integrated example** — controls, initial monitoring, ambiguous class,
   selected intervention, and final risk-limited report.

## Go/no-go criteria

### Combine CED and MRM only if

- the experiment-induced quotient theorem is stated and proved;
- both CED and MRM central results become corollaries of it;
- one integrated ecological example exercises both detection and mechanism
  ambiguity;
- the main text is limited to four result families;
- generic statistical formulas are demoted from headline novelty.

### Do not combine if

- the bridge theorem is only rhetorical;
- the ecological example naturally uses only CED or only MRM;
- the manuscript requires separate notation and introductions for the two halves;
- reviewers would need two unrelated literature reviews to understand the claim.

## Recommendation

**Conditional go.** Develop the bridge theorem and integrated example first. If
both work cleanly, the combined paper is stronger than separate CED and MRM papers.
If the theorem collapses to a generic identifiability statement without a distinctive
minimality or risk result, keep CED as the main methods paper and retain MRM as a
later mechanism-uncertainty article.