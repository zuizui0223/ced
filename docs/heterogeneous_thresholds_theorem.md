# Heterogeneous coordinate-specific threshold panels

## Declared design contract

A panel screens `M` declared coordinates. Coordinate `i` may have its own
threshold design:

```text
n_i reads,
t_i positive threshold,
p_i sensitivity lower bound,
f_i false-positive upper bound.
```

Let

```text
alpha_i = B_tail(n_i, t_i, f_i),
beta_i  = B_tail(n_i, t_i, p_i).
```

Here `alpha_i` is the per-coordinate false-alert upper bound and `beta_i` is the
per-coordinate detection lower bound under the coordinate-specific threshold
contract.

## Theorem 1 — heterogeneous familywise false-alert bound

If all screened coordinates are absent, then without cross-coordinate
independence,

```text
P(any false alert) <= min(1, sum_i alpha_i).
```

This is the heterogeneous union bound. Under declared cross-coordinate
independence, the exact all-absent familywise probability is

```text
1 - product_i (1 - alpha_i).
```

The exact product expression is not a safe substitute for the union bound unless
that independence contract is declared.

## Theorem 2 — heterogeneous all-present joint detection bound

If all screened coordinates are present, then without cross-coordinate
independence the Frechet/union lower bound gives

```text
P(all detected) >= max(0, 1 - sum_i (1 - beta_i)).
```

Under declared cross-coordinate independence, the product lower bound is

```text
product_i beta_i.
```

Again, the product bound is not valid without the independence contract.

## Theorem 3 — weighted false-alert budgets

For nonnegative coordinate weights `w_i`, the expected weighted false-alert budget
under the all-absent state is bounded by

```text
E[sum_i w_i 1{coordinate i false-alerts}] <= sum_i w_i alpha_i.
```

This is useful when false alerts have unequal design costs.

## Example

For three coordinate-specific designs:

```text
(n,t,p,f) = (5,3,0.7,0.05),
(n,t,p,f) = (4,2,0.6,0.02),
(n,t,p,f) = (6,4,0.8,0.10),
```

the bounds are

```text
alpha = (0.001158125, 0.00233648, 0.00127),
beta  = (0.83692, 0.8208, 0.90112),
sum alpha = 0.004764605,
independent all-absent familywise = 0.004757464352,
Frechet all-present joint detection = 0.55884,
independent all-present joint detection = 0.619018919608.
```

For weights `(1,2,5)`, the weighted false-alert budget is

```text
0.012181085.
```

## Explicit non-claims

This theorem does not infer which coordinates are absent or present, does not
infer error rates, does not infer independence, and does not require all
coordinates to share a common read count, threshold, sensitivity, or false-positive
bound.
