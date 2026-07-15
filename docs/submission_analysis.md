# Submission analysis — finite evidence and honest prediction

## Current decision

The CED–MRM combination has passed the first mathematical go/no-go test. The new
experiment-induced quotient is not merely a shared vocabulary device: the joint
presence × response-type witness produces a target-aware partition that neither
CED presence detection nor MRM response typing alone supplies.

The combined paper remains conditional on one final integration step: existing CED
failure and calibration bounds must be rewritten as reliability guarantees for
correct quotient refinement.

## Central question

> What ecological report can a finite experiment justify when latent presence,
> mechanism response, and observation failure remain unresolved?

## Main result hierarchy

### Result 1 — experiment-induced ecological quotient

A declared experiment partitions finite latent ecological worlds by their complete
records. This quotient is the exact information supplied by the design.

A deterministic report of target `T` exists exactly when `T` is constant on every
record class. Otherwise the honest report is the set of compatible target values.

### Result 2 — target-aware honest prediction

The relevant aim is not always full latent-world identification. A design is
sufficient when every remaining record class is homogeneous for the ecological
report target.

The joint witness shows why this matters. The two response types may remain merged
when the focal interaction is absent because they imply the same report target.
When presence is established, an intervention must separate the response types
because they imply opposite management predictions.

### Result 3 — replication architecture controls reliable refinement

Observation error determines whether the experiment reaches the correct quotient
class. Existing CED results supply the required reliability ladder:

- independent resettable repeats;
- independent failure modes;
- overlapping latent failure factors;
- dependent or non-reset reads;
- bounded false positives; and
- calibration-derived error contracts.

The manuscript should express these as probabilities of correct or incorrect class
refinement, not as a detached catalogue of detection formulas.

### Result 4 — adaptive risk-limited discrimination

Heterogeneous thresholds, alpha spending, and MRM's cost-aware active
discrimination become design rules for reducing the target-compatible class under
explicit cost and false-alert budgets.

Generic Bayesian updates, entropy, Chernoff bounds, and one-step value of information
remain methods or supplement material unless they change the chosen policy in the
worked example.

## Added joint analysis

`scripts/verify_experiment_quotient.py` evaluates four latent worlds:

```text
(presence, response type) in {(0,0), (0,1), (1,0), (1,1)}.
```

The report target is:

```text
absence          -> no interaction
presence/type 0  -> management response decreases
presence/type 1  -> management response increases
```

The verified designs are:

| Design | Record classes | Residual sizes | Deterministic target report? |
|---|---:|---|---|
| passive | 1 | `(4,)` | no |
| detection only | 2 | `(2,2)` | no |
| detection + intervention | 3 | `(2,1,1)` | yes |

The result is genuinely joint:

- detection separates absence from presence;
- it does not resolve the management response among present worlds;
- intervention typing is target-relevant only after presence is established; and
- a shared failure record that leaves both present types compatible restores a
  set-valued `{decrease, increase}` report.

## Story for the manuscript

```text
A finite experiment does not identify an ecosystem; it partitions possible worlds.
        ↓
Prediction is deterministic only when all worlds left in one record class agree.
        ↓
Presence uncertainty and mechanism uncertainty can interact in the same class.
        ↓
Interventions refine the class, but observation architecture determines reliability.
        ↓
Calibration, mode diversity, and adaptive risk spending determine which refinement
can be reported honestly.
```

## Ecological worked example

Use one rare plant–pollinator interaction across sites.

- Presence dimension: focal pollinator/interaction absent or present.
- Response dimension: two mechanisms predict opposite responses to floral-trait
  manipulation or competitor removal.
- Passive observations: cameras, visits, or eDNA do not identify the mechanism.
- Detection stage: establishes interaction presence with imperfect sensitivity.
- Intervention stage: distinguishes response type only in present sites.
- Shared failures: weather, camera power, access, observer, or laboratory batch.
- Controls: blanks and known-positive observations calibrate false-positive and
  sensitivity bounds.
- Report target: universal management response, typed response, or honest set-valued
  prediction.

## Reviewer-facing novelty boundary

Do not claim novelty for identifiability, occupancy modeling, Bayesian updating,
multiple testing, decision trees, or value of information in general.

The defensible combined contribution is:

1. an operational ecological quotient induced by a finite experiment;
2. a target-constancy criterion for honest deterministic reporting;
3. a target-aware joint presence × mechanism witness;
4. replication-architecture results interpreted as reliability of quotient
   refinement; and
5. explicit risk/cost accounting for adaptive class refinement.

The elementary quotient statement alone is not enough. The nontrivial contribution
must remain the target-aware minimality and its coupling to realistic observation
failure.

## Remaining analysis before submission

1. Express one-sided detection probability as probability of reaching a target-safe
   class in the joint witness.
2. Express false alerts as probability of entering a target-incorrect class.
3. Compare equal read budgets under one shared mode, independent modes, and
   overlapping factors for the joint example.
4. Add one cost-aware adaptive decision tree that chooses between additional
   detection and response-typing intervention.
5. Produce one figure showing the latent-world partition after each stage.
6. Produce one figure showing reliable-refinement probability under alternative
   failure architectures.
7. Map MRM's minimal candidate-safe quotient into the neutral latent-world notation
   and state the exact additional assumptions needed for future-action stability.

## Submission gate

Proceed as one combined paper only if the next reliability analysis can be stated
without creating a separate detection-results section. The manuscript should have
one notation, one ecological example, one central quotient figure, and no more than
four named main results.

If that integration fails, retain the quotient theorem and joint witness as a bridge
but submit CED and MRM separately.
