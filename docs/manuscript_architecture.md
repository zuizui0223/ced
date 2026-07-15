# CED manuscript architecture

## Working title

**Risk-Limited Evidence for Ecological Closure under Imperfect Detection**

Alternative:

**What Finite Monitoring Can Certify: Partial Ecological Evidence under Detection Error and Shared Failure**

## One-sentence thesis

Passive finite non-detection cannot uniformly certify ecological closure, but a
declared intervention and observation design can recover an exact partial quotient
and attach finite, calibrated risk guarantees to the distinctions it actually
probes.

## Paper identity

CED is a theorem-first ecological monitoring paper. It is not an occupancy-model
replacement, an empirical inference pipeline, or a generic multiple-testing paper.
Its contribution is to connect a structural impossibility result to a constructive
finite evidence-design calculus.

## Central narrative

```text
passive finite observation cannot certify closure uniformly
        ↓
intervention panels recover a precise partial quotient
        ↓
observation error weakens certificates into risk-limited evidence
        ↓
replication is useful only relative to resetability and failure diversity
        ↓
calibration and risk spending make multi-coordinate evidence auditable
```

## Main theorem package

### Theorem 1 — No uniform passive finite closure certificate

Every fixed finite declared system may have a finite revealing horizon, but no
single passive horizon works uniformly over families whose first legal exterior
exposure may be delayed arbitrarily far.

Ecological interpretation: finite non-detection over one observation window is not
a structural absence or closure certificate when a legal future exposure can occur
later.

### Theorem 2 — Exact partial quotient of a declared intervention panel

A resettable panel identifies exactly the baseline, the exterior coordinates it
probes, and any response-type coordinate exposed by its declared interventions.
Unprobed distinctions remain in a quantified residual equivalence class.

The trial count, action budget, and temporal depth are separate design resources and
must not be conflated.

Ecological interpretation: finite evidence is exact relative to the questions the
panel actually asks, not relative to all possible hidden ecological distinctions.

### Theorem 3 — Robust detection depends on replication architecture

Under imperfect sensitivity, finite all-negative records do not certify absence.
Detection guarantees depend separately on:

- repeats within a resettable operating mode;
- the number of independent modes;
- partially shared latent failure factors; and
- whether repeats are dependent or non-reset.

Independent repeats produce binomial improvement. Repeats inside one shared mode
cannot overcome its availability ceiling. Overlapping failure factors interpolate
between independent and fully common-mode failure. Without resettable independence,
only sharp expectation-based bounds remain.

Ecological interpretation: ten observations from one shared weather, access,
hardware, or observer domain need not provide the evidence of ten independent
replicates.

### Theorem 4 — Calibrated risk-limited multi-coordinate evidence

With bounded false positives, threshold crossing is evidence rather than a
deductive presence proof. Blank and known-present controls provide conservative
one-sided bounds for false-positive rate and sensitivity. These bounds feed into:

- coordinate-specific threshold evidence;
- familywise and expected false-discovery budgets;
- heterogeneous coordinate designs;
- adaptive conditional alpha spending; and
- exact or Chernoff concentration bounds when cross-coordinate independence is
  explicitly declared.

Ecological interpretation: monitoring conclusions can be reported with an auditable
risk budget tied to calibration data, coordinate-specific effort, and adaptive
follow-up decisions.

## Result placement map

| Repository result | Manuscript role |
|---|---|
| delayed exposure family | Theorem 1 witness and proof |
| no-uniform-horizon statement | Theorem 1 |
| panel quotient | Theorem 2 |
| panel resource frontiers | Theorem 2 corollaries |
| one-sided imperfect detection | Theorem 3 foundation |
| independent mode diversity | Theorem 3 main extension |
| overlapping latent failure factors | Theorem 3 main extension |
| dependent/non-reset threshold bounds | Theorem 3 boundary theorem |
| bounded false-positive threshold evidence | Theorem 4 foundation |
| calibration confidence bounds | Theorem 4 main construction |
| multiple and heterogeneous thresholds | Theorem 4 corollaries |
| expected false-discovery budgets | Theorem 4 corollary |
| adaptive alpha spending | Theorem 4 adaptive extension |
| Poisson-binomial and Chernoff concentration | supplement or final corollary |
| ordinary FDR | exclude unless required by reviewers |

## Results order

1. Passive finite observation does not certify closure uniformly.
2. A finite intervention panel yields an exact partial quotient.
3. Imperfect detection turns panel design into a replication-architecture problem.
4. Shared failures create availability ceilings that raw repetition cannot remove.
5. Calibration converts unknown error rates into conservative evidence contracts.
6. Multi-coordinate and adaptive monitoring can be controlled by explicit risk
   budgets.

## Headline figures

### Figure 1 — From non-certifiability to partial evidence

A delayed-exposure witness followed by a panel that probes only selected exterior
coordinates. Show the residual equivalence class after the panel.

### Figure 2 — Replication architecture

Compare equal total read budgets allocated as:

- many repeats in one shared mode;
- fewer repeats across independent modes; and
- modes with partially overlapping failure factors.

Plot or tabulate the resulting joint detection guarantees and availability ceilings.

### Figure 3 — Calibration-to-risk pipeline

```text
blank controls + known-present controls
        → conservative f_max and p_min
        → coordinate thresholds
        → familywise / expected / adaptive risk budget
```

### Figure 4 — Assumption ladder

Show the guarantee available under:

1. zero false positives;
2. bounded false positives;
3. independent resettable reads;
4. dependent non-reset reads;
5. independent coordinates; and
6. no cross-coordinate independence.

This figure should make clear that stronger formulas require stronger declared
contracts.

## Ecological worked examples

Use one primary example consistently rather than listing many shallow examples.
Recommended primary example: a multi-site eDNA or camera monitoring panel for a
rare taxon or interaction channel.

The example should include:

- delayed seasonal or episodic exposure;
- site or taxon coordinates;
- repeated reads within sampling modes;
- shared weather, access, batch, camera, or observer failure factors;
- blank and known-positive controls; and
- adaptive confirmation of preliminary alerts.

Secondary interpretations may mention pathogen surveillance, pollinator
interaction detection, seed-bank recruitment, or post-disturbance colonization.

## What is genuinely new

The paper should not claim invention of imperfect-detection models, occupancy
models, multiple testing, calibration intervals, adaptive monitoring, or Chernoff
bounds. Its novelty is the integrated exact decision structure:

1. a closure non-certifiability theorem;
2. an exact partial quotient for what a finite intervention panel identifies;
3. a separation of repetitions from failure-mode diversity; and
4. a contract-indexed risk ladder showing precisely which evidence guarantee is
   valid under each observation architecture.

## Main-text exclusions

The following should not become additional equal-weight sections:

- ordinary FDR procedures;
- generic Bayesian occupancy inference;
- empirical estimation of failure-factor graphs;
- broad survey optimization;
- continuous-time or continuous-state extensions; and
- claims that passing finite checks validate a field ecosystem.

These are future work or external methods that can be connected later.

## Relationship to companion papers

- **CCOC / RACH:** supplies the program-level lesson that widened future operations
  can expose distinctions hidden by a closed-context compression. CED changes the
  question from exact representation to finite evidence.
- **MLTR:** addresses transport and repair after the system itself is replaced.
  CED instead holds the declared target question fixed and analyzes monitoring
  evidence under detection limitations.
- **MRM:** addresses disagreement among candidate future transition mechanisms.
  CED-style observation contracts may support MRM experiments, but mechanism type
  and coordinate presence are different hidden variables.

## Discussion claims

CED supports the following ecological conclusions:

- absence of detection is not generally a certificate of ecological absence or
  closure;
- finite interventions can still recover exact partial information;
- nominal replication can be misleading under shared failure;
- calibration controls are part of the theorem contract, not a cosmetic validation
  step; and
- adaptive monitoring remains auditable when every conditional risk expenditure is
  recorded.

## Non-claims

CED does not infer ecological closure, coordinate truth, failure factors,
resetability, error rates, independence, or calibration representativeness from
field data. It provides finite conditional guarantees once those model and design
contracts are declared.

## Completion checklist

- [x] Freeze the theorem inventory into four main results.
- [ ] Write one notation table covering systems, panels, coordinates, modes,
      factors, thresholds, and risk budgets.
- [ ] Convert theorem notes into formal proof sketches for the main text.
- [ ] Move full finite proofs and secondary bounds to a supplement.
- [ ] Generate Figures 1–4 from deterministic witnesses.
- [ ] Write one complete ecological worked example.
- [ ] Perform a primary-source literature review for occupancy, false-positive
      detection, adaptive monitoring, common-mode failure, and evidence design.
- [ ] Select a target journal and tune terminology for theoretical ecology versus
      ecological methods.
- [ ] Create a stable release tag and archive the replay artifact at the submission
      commit.

## Development freeze

New theorem families should not be added by default. A proposed addition belongs in
the manuscript only if it changes one of the four main conclusions or closes a
reviewer-visible logical gap. Otherwise it should be recorded as future work.
