# Evidence theory closure

Status: **structural theory closed for the integrated Evidence paper under declared finite/model-supported assumptions**.

Evidence starts from a current compatible-world block `C` delivered by the Observation layer and separates three questions:

1. what mechanism distinctions remain unresolved;
2. whether the declared scientific target is already resolved;
3. whether the declared candidate vocabulary contains an informative next observation.

These are different predicates. The integrated paper does not collapse them into one universal utility or one universal stopping theorem.

## Objects

Let `C` be the current compatible-world set. Let

- `S: C -> Sspace` be the declared mechanism state;
- `T: C -> Y` be the scientific target;
- `Q_j: C -> X_j` be declared candidate observations.

For any mapping `f`, write `f(C)={f(w):w in C}`.

Define:

- **mechanism resolved** iff `|S(C)|=1`;
- **target resolved** iff `|T(C)|=1`;
- **declared deterministic candidate exhausted** iff every `Q_j` is constant on `C`.

For a realized additional observation `Q=q`, update

`C+ = {w in C: Q(w)=q}`.

Then `C+ subseteq C`.

## E-T1 — current identification boundary

Within the declared positive log-linear family with `k` latent coordinates and observation matrix `M`, structural unidentified dimension is

`k-rank(M)`.

A new scalar row reduces this dimension iff it lies outside the current row span.

Source owner: Boundary.

## E-T2 — exact target report criterion

A deterministic target report is exact iff `|T(C)|=1`. Otherwise the sharp support-level output is the set `T(C)`.

Source owner: CED.

## E-T3 — target-safe resolution requirement

Among refinements of the current evidence partition, the target/action-stable quotient retains only distinctions needed to preserve the declared target and successors. It is a required refinement, not evidence that the current record has already identified the correct refined block.

Source owner: CED.

## E-T4 — learning and licensing need not share a maximizer

There exist finite compatible-world problems with equal-cost candidates for which the candidate maximizing full mechanism mutual information differs from the candidate maximizing exact target-resolution probability.

**Witness.** Eight equiprobable worlds cross binary target `T` with four-level target-irrelevant coordinate `N`. `Q_N=N` gives 2 bits about full mechanism identity `(T,N)` and target-resolution probability 0. `Q_T=T` gives 1 bit and target-resolution probability 1. Therefore their rankings disagree.

This is an existence theorem/counterexample, not a universal preference between utilities.

## E-T5 — mechanism resolution implies target resolution when target is mechanism-measurable

Assume `T=h(S)` for a deterministic map `h`. If `|S(C)|=1`, then `|T(C)|=1`.

**Proof.** If `S(w)=s*` for every `w in C`, then `T(w)=h(s*)` for every `w in C`. Therefore `T(C)` is singleton. □

The converse fails whenever `h` is non-injective. The eight-world witness supplies an example: observing `T` resolves the target while four nuisance/mechanism-detail states remain compatible.

## E-T6 — target resolution does not imply mechanism resolution

There exist finite problems with `|T(C)|=1` but `|S(C)|>1`.

**Witness.** Condition the eight-world benchmark on one realized `target_split` outcome. The target is fixed while four nuisance states remain compatible.

Thus target licensing may rationally stop before mechanism learning is complete.

## E-T7 — candidate exhaustion does not imply target resolution

There exist finite problems in which every declared candidate is constant on `C` while `|T(C)|>1`.

**Witness.** Let `C` contain two worlds with different targets and let the declared candidate family contain only a constant probe. All candidate information values are zero, but the target remains unresolved.

Thus an exhausted candidate vocabulary is a limitation of the declared measurement family, not evidence that the target has been resolved.

## E-T8 — target resolution does not imply candidate exhaustion

There exist finite problems with `|T(C)|=1` while some declared candidate remains non-constant on `C`.

**Witness.** After conditioning the eight-world benchmark on `target_split`, `nuisance_detail` still separates four compatible mechanism-detail states.

Thus licensing can stop while learning opportunities remain.

## E-T9 — realized acquisition is nested refinement

For every current block `C` and candidate `Q`, after observing realized outcome `q`,

`C+={w in C:Q(w)=q} subseteq C`.

Therefore mechanism and target value sets can only weakly contract after non-destructive acquisition.

This is the Evidence-side specialization of the general compatible-world refinement theorem.

## E-T10 — objective-relative stopping relations

Under `T=h(S)`:

- mechanism resolved => target resolved;
- target resolved does not imply mechanism resolved;
- candidate exhausted does not imply target resolved;
- target resolved does not imply candidate exhausted.

Therefore mechanism-learning stop, target-licensing stop and candidate-vocabulary exhaustion are mathematically distinct states. No single one can be substituted for the others without additional assumptions.

## Closure boundary

The integrated Evidence mathematics is therefore closed at the level required by the paper:

`current boundary -> target requirement -> learning/licensing non-equivalence -> failure-aware crediting -> objective-relative stopping`.

Still empirical/model-dependent are:

- whether a physical candidate realizes the predicted observation partition;
- whether failure-mode contracts hold in a natural system;
- whether the declared world/mechanism vocabulary is adequate;
- whether predictive likelihoods are calibrated;
- transport to new systems.

These are not missing structural theorems.