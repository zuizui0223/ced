# Common-mode imperfect detection: repetition is not failure diversity

## Declared observation contract

Let `i = 1, …, k` index prespecified, truly present binary target coordinates and
let `j = 1, …, m` index declared failure modes. A mode may represent a
camera–power–weather domain, a sampling date, an observer route, or another
shared observation context.

Each mode is operational with probability at least `a`, independently across
modes. If mode `j` fails, every observation assigned to that mode is negative
for every coordinate. Conditional on mode `j` operating, each coordinate is
read `r` times; reads are conditionally independent, have positive probability
at least `p`, and have no false positives.

The theorem assumes that the mode partition, availability lower bound,
sensitivity lower bound, zero-false-positive property, and independence claims
are declared in advance. It does not infer them from data.

## Theorem 1 — exact common-mode joint-detection frontier

Put

```text
q_r = (1 - p)^r.
```

For any chosen subset of `s` target coordinates, one declared mode leaves every
coordinate in that subset undetected with probability at most

```text
1 - a + a q_r^s.
```

Consequently, the probability of detecting all `k` truly present coordinates at
least once is bounded below by

```text
sum_{s=0}^k (-1)^s binom(k, s) [1 - a + a q_r^s]^m.
```

When the mode availability and sensitivity equal their stated lower bounds, this
is the exact probability. The formula follows by inclusion–exclusion over the
set of coordinates still missing after all modes.

## Theorem 2 — availability ceiling and necessary mode floor

No amount of repeat effort within the same `m` modes can remove the event that
all modes fail. Therefore, for every finite `r`, and also in the limit as
`r → infinity`,

```text
P(all k targets detected) <= 1 - (1 - a)^m.
```

For `p > 0`, the right-hand side is the limiting value as within-mode repeat
effort grows. Hence a target joint confidence `c` requires at least

```text
m >= ceil[ log(1 - c) / log(1 - a) ]
```

independent modes when `0 < a < 1`. This **mode floor is necessary but not
sufficient**: finite sensitivity can still require additional repeats within
each selected mode.

If `0 < p < 1`, a confidence equal to the availability ceiling is approached but
not attained by any finite `r`; the target must lie strictly below the ceiling.
When `p = 1`, one read in an operating mode attains the ceiling.

## Example: same total effort, different failure diversity

Let `k = 3`, `a = 0.8`, and `p = 0.6`.

- With one failure mode and 10 repeated reads per coordinate, the joint detection
  probability is approximately `0.799748`. It cannot exceed `0.8`, even with
  arbitrarily many more within-mode reads.
- With two independent failure modes and five reads per coordinate in each mode,
  the joint detection probability is approximately `0.950069`. The availability
  ceiling becomes `0.96`.

The second design uses 30 reads, whereas the first uses 30 reads as well. Their
very different guarantees arise from how effort is distributed across failure
modes, not from raw replicate count.

## Relation to the CED core

`CommonModeProfile` treats declared failures combinatorially for a deterministic
separator panel. This extension treats independent mode availability
probabilistically under imperfect one-sided detection. The two formalisms agree
on the design principle—replication inside one shared domain is not failure
diversity—but they are not interchangeable claims.

## Explicit non-claims

This theorem does not cover false positives, unknown or estimated sensitivity,
correlated mode failures, dependent within-mode reads, heterogeneous coordinates,
non-reset monitoring, adaptive allocation, unobserved failure modes, or
empirical inference of availability from the record. Those require separate
models and evidence conditions.
