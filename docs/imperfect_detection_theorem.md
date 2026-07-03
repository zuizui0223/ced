# One-sided imperfect detection: finite negative evidence and repeat design

## Declared observation contract

For each latent binary coordinate `z_i ∈ {0, 1}`, a resettable read returns
`Y_ij ∈ {0, 1}`.  The theorem assumes:

1. **No false positives.** If `z_i = 0`, then every `Y_ij = 0`.
2. **Bounded sensitivity.** If `z_i = 1`, then each read is positive with
   probability at least `p_min`, where `0 < p_min ≤ 1`.
3. **Conditional independence.** For a fixed present coordinate, resettable
   reads are independent conditional on its latent state.
4. **Declared coordinate semantics.** A coordinate is a prespecified ecological
   exposure, taxon, interaction channel, or other binary target; the theorem
   does not infer that coordinate set from the records.

The model deliberately excludes false positives, unknown sensitivity bounds,
dependence among repeats, non-reset monitoring, and common-mode observation
failure.  Those require separate extensions.

## Theorem 1 — finite non-detection does not certify absence

Let `0 < p_min < 1`, and collect any finite number `r ≥ 1` of reads for one
coordinate.  The all-negative record has probability

```text
P(Y_i1 = ... = Y_ir = 0 | z_i = 1) ≤ (1 - p_min)^r,
```

and is strictly possible whenever the true sensitivity is below one.  Under
absence that same record occurs with probability one.  Therefore an all-negative
finite record cannot distinguish absence from presence in this model.

A positive record does distinguish: because false positives are excluded, any
coordinate with at least one positive is certified present.  Thus the natural
object under this contract is a **one-sided random partial certificate**, not an
exact deterministic quotient: the positive signature is the subset of
coordinates with at least one observed positive; all remaining coordinates stay
undecided.

## Theorem 2 — exact risk-limited repeat frontier for positive detection

Suppose `k` prespecified coordinates are truly present, each receives `r`
resettable reads, and the declared contract holds.  The probability that every
coordinate has at least one positive is bounded below by

```text
[1 - (1 - p_min)^r]^k.
```

For target joint confidence `1 - α`, the least uniform repeat count is the
smallest positive integer `r` satisfying

```text
[1 - (1 - p_min)^r]^k ≥ 1 - α.
```

Equivalently, the required total read budget is `k r`.  This is an exact
frontier for the stated independent one-sided model; it is not a guarantee of
absence, closure, or ecological completeness after non-detection.

## Example

With `p_min = 0.6`, `k = 3`, and target joint confidence `0.95`, five reads per
coordinate are required:

```text
[1 - (1 - 0.6)^5]^3 = 0.969591... ≥ 0.95,
[1 - (1 - 0.6)^4]^3 = 0.925... < 0.95.
```

The 15-read design makes simultaneous positive detection likely when all three
coordinates are present; it does **not** turn 15 negative reads into a proof
that any coordinate is absent.

## Relation to the CED core

The deterministic reset-panel theorem records exactly which latent coordinates
are read.  Imperfect detection breaks that exact negative identification: a
planned read can end in a non-detection even when its coordinate is present.
The extension preserves a useful design claim—how repeat effort buys a declared
positive-detection risk bound—while keeping the no-certificate boundary
explicit.
