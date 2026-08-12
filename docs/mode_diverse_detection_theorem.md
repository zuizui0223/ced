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

## Theorem 1 — exact worst-case joint-detection frontier

Put

```text
q_r = (1 - p)^r.
```

Among all systems satisfying the declared lower-bound contract, the smallest
joint-detection probability is attained when each mode availability equals `a`
and each operating read sensitivity equals `p`. In that least-favourable case,
for any chosen subset of `s` target coordinates, one declared mode leaves every
coordinate in that subset undetected with probability

```text
1 - a + a q_r^s.
```

Consequently, the contract guarantees detection of all `k` truly present
coordinates with probability at least

```text
sum_{s=0}^k (-1)^s binom(k, s) [1 - a + a q_r^s]^m.
```

The expression is exact when the availability and sensitivity lower bounds are
attained. For larger actual availability or sensitivity, realized joint detection
can be higher.

## Theorem 2 — worst-case guarantee ceiling and necessary mode floor

The lower-bound contract permits the least-favourable case in which every mode
operates with probability exactly `a`. In that admissible case, no amount of
within-mode repeat effort can remove the event that all `m` modes fail. Therefore
no uniform guarantee valid over the entire declared contract can exceed

```text
1 - (1 - a)^m.
```

For `p > 0`, the guaranteed lower bound in Theorem 1 converges to this value as
`r → infinity`. Thus a target joint confidence `c` can be certified uniformly
only if

```text
m >= ceil[ log(1 - c) / log(1 - a) ]
```

when `0 < a < 1`. This **mode floor is necessary but not sufficient**: finite
sensitivity can still require additional repeats within each selected mode.

This quantity is a **worst-case guarantee ceiling implied by the availability
lower bound**. It is an actual probability ceiling only when the true mode
availabilities equal the stated bound (or when exact availabilities are otherwise
specified). If true availabilities are higher than `a`, realized detection may
exceed `1 - (1 - a)^m`.

If `0 < p < 1`, a confidence equal to the worst-case guarantee ceiling is
approached but not attained by any finite `r`; a finite-repeat certified target
must lie strictly below it. When `p = 1`, one read in an operating mode attains
the least-favourable ceiling.

## Example: same total effort, different failure diversity

Let `k = 3`, `a = 0.8`, and `p = 0.6`.

- With one failure mode and 10 repeated reads per coordinate, the guaranteed
  joint detection probability is approximately `0.799748`. The worst-case
  guarantee cannot exceed `0.8`, even with arbitrarily many more within-mode
  reads.
- With two independent failure modes and five reads per coordinate in each mode,
  the guaranteed joint detection probability is approximately `0.950069`. The
  worst-case guarantee ceiling becomes `0.96`.

The second design uses 30 reads, whereas the first uses 30 reads as well. Their
very different guarantees arise from how effort is distributed across failure
modes, not from raw replicate count. If actual mode availability exceeds the
lower bound, either realized probability may be higher than these guaranteed
values.

## Relation to the CED core

`CommonModeProfile` treats declared failures combinatorially for a deterministic
separator panel. This extension treats independent mode availability
probabilistically under imperfect one-sided detection. The two formalisms agree
on the design principle—replication inside one shared domain is not failure
diversity—but they are not interchangeable claims.

## Explicit non-claims

This theorem does not cover false positives, unknown or estimated sensitivity,
correlated mode failures, dependent within-mode reads, heterogeneous coordinates,
non-reset monitoring, adaptive allocation, unobserved failure modes, or empirical
inference of availability from the record. A lower bound `a` does not imply an
upper bound on realized detection probability; it supports a worst-case guarantee
calculation. Exact probability ceilings require exact (or upper-bounded) failure
probabilities.
