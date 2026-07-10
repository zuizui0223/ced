# Dependent repeats and non-reset threshold evidence

## Declared design contract

The binomial threshold theorem assumes resettable conditionally independent reads.
This layer removes that assumption. Reads may be dependent and may be non-reset.
Only marginal read contracts remain:

- if the coordinate is absent, each read is positive with probability at most
  `f_max`; and
- if the coordinate is present, each read is positive with probability at least
  `p_min`.

Let `X` be the number of positive reads among `n` reads, and accept the coordinate
when

```text
X >= t.
```

## Theorem 1 — false-alert bound without independence

Under absence,

```text
E[X] <= n f_max.
```

Therefore Markov's inequality gives

```text
P(X >= t | absent) <= min(1, n f_max / t).
```

No cross-read independence is required.

## Theorem 2 — detection lower bound without independence

Under presence,

```text
E[X] >= n p_min.
```

On the complement of the threshold event, `X <= t - 1`; on the event, `X <= n`.
Thus

```text
E[X] <= (t - 1) P(X < t) + n P(X >= t).
```

Solving for the threshold-event probability gives

```text
P(X >= t | present) >= max(0, (n p_min - (t - 1)) / (n - t + 1)).
```

For `t = 1`, this reduces to `P(any positive | present) >= p_min`: repeated
non-reset reads do not improve the guarantee beyond the marginal sensitivity
contract.

## Event-level evidence ratio

The posterior-free event ratio is bounded by

```text
max(0, (n p_min - (t - 1)) / (n - t + 1))
-------------------------------------------------
        min(1, n f_max / t)
```

when the denominator is positive. If `f_max = 0` and the numerator is positive,
the ratio is infinite and the threshold event is deductive under the no-false-
positive contract.

## Sharpness

The bounds are sharp under the marginal-only contract. For the false-alert side,
place mass `n f_max / t` on records with exactly `t` positives and the remaining
mass on all-negative records when `n f_max < t`; symmetrize over read positions.
For the detection side, place mass on counts `t - 1` and `n` to achieve mean
`n p_min` while minimizing the threshold-event probability. These constructions
satisfy the declared marginals and attain the bounds.

## Example

For `n = 5`, `t = 3`, `p_min = 0.7`, and `f_max = 0.05`:

```text
P(X >= 3 | absent) <= 5 * 0.05 / 3 = 0.083333333333,
P(X >= 3 | present) >= (5 * 0.7 - 2) / 3 = 0.5,
evidence ratio >= 6.
```

The corresponding independent binomial threshold layer has much stronger values.
That difference is exactly the mathematical cost of dropping resettable
independence.

## Explicit non-claims

This theorem does not infer dependence structure, resetability, sensitivity,
false-positive rates, or posterior probabilities. It does not claim binomial
behavior. It states what remains valid when only marginal read bounds are
declared.
