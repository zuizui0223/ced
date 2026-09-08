# EVIDENCE paper integration plan

Status: canonical manuscript integration contract under the two-paper submission architecture.

Submission-facing owner: `zuizui0223/ced`.

Source repositories:

- `zuizui0223/boundary` — current structural identification boundary;
- `zuizui0223/mrod` — mechanism-learning observation value and sequential design;
- `zuizui0223/ced` — target-safe reportability, failure-aware refinement and risk-limited adaptive design.

The source repositories remain independent reproducibility/provenance units. Their current standalone manuscripts are source material, not separate near-term submission targets.

## Paper question

> Given the worlds still compatible with the current record, what can be identified now, which unresolved distinctions matter for the declared scientific target, what should be measured next, and when is a deterministic report licensed?

## Primary claim spine

1. **Current boundary** — the declared observation map determines a structural equivalence/identified set that precision alone cannot eliminate.
2. **Target requirement** — full latent-world identification is unnecessary; only distinctions that can change the declared target or successor report need resolution.
3. **Two observation values** — mechanism-learning value and target-licensing value are different scientific utilities and may rank candidate observations differently.
4. **Trustworthy refinement** — a nominal record split is creditable only under an observation/failure architecture that supports the distinction.
5. **Adaptive acquisition/reporting** — select, observe, update, and stop under explicit information, target, risk, cost and prediction-limit contracts.

## Part I — Boundary: what is identifiable now?

Use Boundary as the opening structural layer.

Key result:

- for positive log-linear channels with observation matrix `M`, unidentified structural dimension is `k - rank(M)`;
- a new scalar observation reduces this dimension iff its row adds a direction outside the current row span;
- duplicate/rescaled/more-precise observations along an existing direction can improve precision without changing structural identification.

Interpretation:

> Before asking what to measure next, declare what the current observation map has failed to distinguish.

Do not present generic rank algebra as the paper's sole novelty. Its role is to anchor the current identification boundary used by the later evidence-design results.

## Part II — CED target-safe requirement: which unresolved distinctions matter?

Use CED Results 1–2 as the target-relative reporting infrastructure.

Key claims:

- a finite experiment induces an exact compatible-world quotient;
- deterministic target reporting is justified only when the target is constant over the current compatible class;
- otherwise the sharp report is the compatible target set;
- the unique coarsest target-safe refinement retains only distinctions needed for the declared target and successors.

Critical firewall:

> Required target-safe refinement is not the same as already-identified state.

The current record may intersect multiple target-safe blocks; in that case ambiguity remains honest.

## Part III — two scientific utilities for next-observation choice

### Learning utility — MROD

For residual mechanism variable `S` and candidate observation `Q`, MROD uses normalized incremental information

`V_learning(Q) = I(S;Q | A) / K`.

This asks:

> How much is this candidate expected to teach us about residual mechanism identity?

Use the frozen G2 benchmark as the main learning-value stress test:

- budget 2 initial confounding edges resolved `1.000` information-guided versus `0.6045` random;
- convergence `0.990` versus `0.435`;
- observations used `1.505` versus `1.821`;
- false exclusion zero in the frozen policy-by-budget cells.

### Licensing utility — CED

CED asks instead:

> Does this candidate resolve the distinctions required for the declared target while satisfying the false-resolution and cost contract?

Use the existing schema-v5 witness in which full-world information gain selects a target-irrelevant measurement while target-safe design selects the target-resolving one.

### Integrated contribution

Evidence must make this non-equivalence explicit:

```text
mechanism-learning value
    !=
target-licensing value
```

The paper should add one unified finite-world benchmark where both values are computed over the same candidate set and demonstrably rank at least one candidate pair differently.

This is the key integration result rather than a conflict between MROD and CED.

## Part IV — trustworthy refinement under failure architecture

Use CED Result 3.

A nominal measurement can separate ideal latent worlds while failing to provide trustworthy evidence under imperfect/shared observation failures.

Main claims to retain:

- finite negative evidence does not become deductive absence under imperfect sensitivity;
- repetition inside one shared failure domain is not equivalent to independent failure diversity;
- independent modes can strengthen the worst-case guarantee even at equal raw effort;
- overlapping/dependent failures require their own contract rather than silent independence assumptions.

This block links Boundary's desired new direction to the question: **is that direction actually reliable enough to count as evidence?**

## Part V — adaptive acquisition and stopping

Combine the MROD sequential design pattern with CED's target/risk/cost reporting contract.

Generic loop:

```text
current compatible region
       |
       v
identify unresolved distinctions
       |
       v
declare utility: learning / licensing
       |
       v
score estimable candidates
       |
       v
select before outcome is revealed
       |
       v
acquire outcome
       |
       v
update compatible region
       |
       +-- target licensed -> report/stop
       +-- budget exhausted -> stop with limitation
       +-- candidates non-estimable -> prediction-limited
       +-- ambiguity remains -> continue if justified
```

Do not force one stopping theorem to cover both utilities. Learning can stop because no declared candidate carries mechanism information; licensing can stop because the target is resolved under the risk contract even while mechanism ambiguity remains.

## Main Evidence results

### E-R1 — Structural identification boundary

Current observation geometry defines what cannot be distinguished in principle under the declared model family.

### E-R2 — Target-safe reporting boundary

Only target-relevant distinctions require resolution; unresolved target variation forces set-valued or ambiguous reporting.

### E-R3 — Learning and licensing can diverge

A new unified benchmark must demonstrate candidate-ranking divergence between mechanism information and target-safe licensing on the same finite world set.

### E-R4 — Failure architecture determines whether a proposed split is trustworthy

Candidate observations are not credited purely because ideal records differ; reliability/failure structure conditions evidential value.

### E-R5 — Adaptive acquisition is objective- and boundary-aware

The next measurement and stopping rule depend on the declared utility, candidate vocabulary, reliability contract, target, cost and risk ceiling.

## Cross-paper firewall

Evidence receives a retained compatible-world set from Observation.

Evidence may not re-claim as novelty:

- retained-reference refinement in general;
- shadow/no-row support loss;
- semantic-coarsening information loss;
- downstream irreversibility after observation-system collapse.

Those belong to Observation.

Evidence may say:

> Given the retained observation and its known limitations, here is what is currently identifiable, what matters for the target, and what evidence action is warranted next.

## Source-manuscript policy

The following standalone drafts are retained as provenance/source material but are not independent near-term submissions under this architecture:

- Boundary Paper A;
- MROD MEE manuscript;
- CED Paper B standalone framing.

CED Paper B remains the primary drafting skeleton because it already contains the strongest target-safe/reportability narrative and MEE production package. Boundary and MROD are integrated as explicit Parts I and III rather than external companion papers.

## Immediate drafting tasks

1. revise current CED Paper B opening so it begins with the current identification boundary before reportability;
2. import Boundary's rank/identified-set result as Part I with clear provenance;
3. retain CED target-safe quotient as Part II;
4. import MROD mechanism-information design as the learning branch of Part III;
5. implement a shared learning-versus-licensing divergence benchmark;
6. retain CED failure architecture as Part IV;
7. rewrite adaptive policy/results as a two-utility design rather than one universal value function;
8. run a claim-overlap audit against archived Boundary and MROD abstracts before submission.
