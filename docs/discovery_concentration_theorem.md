# False-discovery concentration under independent alerts

## Contract

Let false-alert indicators `X_i` be independent Bernoulli variables with

```text
P(X_i = 1) <= alpha_i.
```

Let

```text
V = sum_i X_i,
mu = sum_i alpha_i.
```

The previous discovery-budget theorem needs no independence and gives only

```text
P(V >= B) <= min(1, mu / B).
```

Under declared cross-coordinate independence, stronger concentration is available.

## Exact Poisson-binomial tail

The worst-case independent tail is attained at the upper probabilities `alpha_i`,
so

```text
P(V >= B) <= P(PoissonBinomial(alpha_1,...,alpha_M) >= B).
```

This tail is computed exactly by finite dynamic programming.

## Chernoff bound

For `B > mu`,

```text
P(V >= B) <= exp(B - mu) (mu / B)^B.
```

For `B <= mu`, the conservative bound is `1`.

Thus the hierarchy is

```text
exact independent tail <= Chernoff bound,
exact independent tail <= Markov bound.
```

Neither Chernoff nor the exact Poisson-binomial tail is valid without the declared
independence contract.

## Example

For

```text
alpha = (0.01, 0.02, 0.03, 0.04, 0.05),
mu = 0.15,
B = 2,
```

we obtain

```text
exact independent tail = 0.008058172,
Chernoff upper bound    = 0.035773984815,
Markov upper bound      = 0.075.
```

The probability of zero false discoveries is at least

```text
product_i (1 - alpha_i) = 0.858277728.
```

## Non-claims

This theorem does not infer independence, does not control ordinary FDR, and does
not infer which coordinates are truly absent. It only strengthens false-discovery
budget tails under an explicit independent-alert contract.
