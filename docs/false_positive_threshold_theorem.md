# False positives: threshold evidence without presence certificates

## Declared observation contract

For one prespecified binary target coordinate, collect `n` resettable binary reads
and let `X` be the number of positive reads. The theorem assumes:

1. **Bounded false positives.** If the coordinate is absent, each read is positive
   with probability at most `f_max`.
2. **Bounded sensitivity.** If the coordinate is present, each read is positive
   with probability at least `p_min`.
3. **Separation.** `0 ≤ f_max < p_min ≤ 1`.
4. **Conditional independence.** Reads are independent conditional on the latent
   state.
5. **Declared coordinate semantics.** The target coordinate, read protocol, and
   bounds are specified before the record is interpreted.

The model does not infer the false-positive rate, sensitivity, independence, or
coordinate semantics from the observed record.

## Theorem — threshold event as posterior-free evidence ratio

Choose a positive-count threshold `t`, where `1 ≤ t ≤ n`, and define the event

```text
E_t = { X ≥ t }.
```

Under the declared bounds,

```text
P(E_t | present) ≥ B_tail(n, t, p_min),
P(E_t | absent)  ≤ B_tail(n, t, f_max),
```

where

```text
B_tail(n, t, q) = sum_{x=t}^n binom(n, x) q^x (1 - q)^(n - x).
```

Therefore the threshold event has the posterior-free evidence-ratio lower bound

```text
B_tail(n, t, p_min) / B_tail(n, t, f_max),
```

with the ratio treated as infinite when `B_tail(n, t, f_max) = 0` and the
numerator is positive.

This is **not** a deductive certificate of presence unless the false-positive
upper bound makes the denominator exactly zero. With `f_max > 0`, even a record
that crosses the threshold remains compatible with absence; it is only bounded
evidence against the declared absence model.

## Example

Let `n = 5`, `t = 3`, `p_min = 0.7`, and `f_max = 0.05`.

```text
P(X ≥ 3 | present) ≥ 0.83692,
P(X ≥ 3 | absent)  ≤ 0.001158125,
evidence ratio     ≥ 722.65.
```

The threshold has high event-level evidence, but it is not an absolute proof of
presence because false positives are allowed.

## Relation to the one-sided CED detection layer

`OneSidedDetector` corresponds to the special case `f_max = 0`, where any
positive can be a certificate of presence. The threshold theorem generalizes the
logic to `f_max > 0` by replacing proof with a risk-limited event-level evidence
ratio.

## Explicit non-claims

This theorem does not cover unknown or estimated error rates, dependent reads,
correlated false positives, false negatives with heterogeneous sensitivity,
multiple-testing correction across many coordinates, adaptive threshold choice,
non-reset monitoring, or empirical calibration of the bounds. Those are separate
modeling targets.
