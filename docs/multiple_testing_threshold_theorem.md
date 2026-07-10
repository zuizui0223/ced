# Multiple coordinates: familywise false-alert control

## Declared observation contract

Apply the same bounded-false-positive threshold design to `M` prespecified target
coordinates. For coordinate `i`, collect `n` resettable binary reads and accept
that coordinate when its positive count `X_i` crosses threshold `t`.

The per-coordinate contract is inherited from the false-positive threshold
layer:

- if coordinate `i` is absent, each read is positive with probability at most
  `f_max`;
- if coordinate `i` is present, each read is positive with probability at least
  `p_min`;
- `0 ≤ f_max < p_min ≤ 1`; and
- reads within the coordinate follow the declared resettable independence
  contract.

The familywise guarantee below does **not** require independence across
coordinates. The exact all-absent formula does require a separate declared
cross-coordinate independence contract.

## Theorem 1 — Bonferroni familywise false-alert bound

Let

```text
alpha_1 = B_tail(n, t, f_max),
```

where `B_tail` is the binomial upper tail. If all `M` coordinates are absent,
then the probability of at least one false alert is bounded by

```text
P(any false alert) ≤ min(1, M alpha_1).
```

This is the safe familywise bound. It remains valid even when false alerts across
coordinates are dependent, as long as each coordinate-level false-alert
probability is bounded by `alpha_1`.

## Theorem 2 — exact all-absent formula under independence

If the coordinate-level alert events are declared independent under the all-absent
state, then the all-absent familywise false-alert probability is exactly

```text
1 - (1 - alpha_1)^M.
```

This exact formula is usually smaller than the Bonferroni bound, but it is not a
safe replacement unless cross-coordinate independence is part of the observation
contract.

## Example

For `M = 20`, `n = 5`, `t = 3`, `p_min = 0.7`, and `f_max = 0.05`:

```text
alpha_1 = B_tail(5, 3, 0.05) = 0.001158125,
Bonferroni familywise bound = 20 alpha_1 = 0.0231625,
independent all-absent familywise risk = 1 - (1 - alpha_1)^20 ≈ 0.022920.
```

The per-coordinate evidence ratio remains approximately `722.65`, but screening
20 coordinates means the chance of at least one false alert is no longer the
single-coordinate false-alert probability.

## Design frontier

Given target familywise level `alpha`, the minimal threshold is the smallest
`t ∈ {1, …, n}` such that

```text
M B_tail(n, t, f_max) ≤ alpha.
```

A stricter design may additionally require the per-coordinate evidence ratio

```text
B_tail(n, t, p_min) / B_tail(n, t, f_max)
```

to exceed a declared target ratio.

## Explicit non-claims

This theorem does not estimate `M`, `p_min`, `f_max`, coordinate dependence,
coordinate semantics, or the target set from the record. It does not control
false discovery rate, posterior probability of presence, or adaptive data-driven
threshold choices. Those are separate theorem layers.
