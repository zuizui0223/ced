# Expected false-discovery budgets

## Declared design contract

Screen a declared set of coordinates with a fixed threshold evidence design. Let
`V` be the number of false discoveries, meaning accepted coordinates that are
truly absent. Suppose there are `M0` absent coordinates among the screened set and
each absent coordinate has false-alert probability at most

```text
alpha_1 = B_tail(n, t, f_max).
```

No independence across coordinates is required for the expectation bound.

## Theorem 1 — expected false discoveries

By linearity of expectation,

```text
E[V] <= M0 alpha_1.
```

The worst-case all-absent bound over `M` screened coordinates is

```text
E[V] <= M alpha_1.
```

This is not familywise control and not FDR control. It is a discovery-budget
statement: the expected number of false discoveries is bounded by the total
absent-coordinate exposure to false-alert risk.

## Theorem 2 — Markov discovery-budget tail

For any positive budget `B`, Markov's inequality gives

```text
P(V >= B) <= min(1, E[V] / B) <= min(1, M0 alpha_1 / B).
```

This yields a finite bound on the chance that false discoveries exceed a declared
budget, again without cross-coordinate independence.

## Conditional FDP-style design bound

If a retained record is known to contain at least `R_min` total discoveries, then

```text
E[V] / R_min <= M0 alpha_1 / R_min
```

is an upper bound on the expected false-discovery fraction relative to that
minimum denominator. This is only a conditional design bound. It is not a
Benjamini-Hochberg or general FDR theorem.

## Example

For `M0 = 20`, `n = 5`, `t = 3`, and `f_max = 0.05`,

```text
alpha_1 = 0.001158125,
E[V] <= 20 alpha_1 = 0.0231625,
P(V >= 1) <= 0.0231625,
P(V >= 2) <= 0.01158125.
```

If at least five discoveries are retained, the conditional expected false
fraction is bounded by

```text
0.0231625 / 5 = 0.0046325.
```

## Explicit non-claims

This theorem does not control FDR in the usual random-denominator sense, does not
estimate the number of absent coordinates from the record, does not infer error
rates, and does not require or assert independence across coordinates.
