# Overlapping and partially shared failure modes

## Declared design contract

Independent modes and one global common-mode failure are two endpoints. The
intermediate case is represented by independent latent failure factors.

Let factor `j` fail independently with probability `rho_j`. Mode `m` is assigned a
set of factors `F_m` and operates if none of those factors fail:

```text
mode m operates iff failed_factors ∩ F_m = empty.
```

Modes may share some factors and not others. Conditional on the operating-mode
set, reads are independent across modes, repeats, and coordinates with sensitivity
at least `p_min`.

For `r` reads per coordinate per operating mode, define

```text
q = (1 - p_min)^r.
```

If a failure-factor state leaves `a` modes operating, then one present coordinate
is missed by every operating mode with probability at most `q^a`, and `k` present
coordinates are all detected with probability at least

```text
(1 - q^a)^k.
```

## Exact finite mixture theorem

For every failed-factor subset `S`, let `P(S)` be its product probability and let
`a(S)` be the number of modes whose factor sets are disjoint from `S`. Then

```text
P(all k present coordinates detected)
>= sum_S P(S) [1 - q^a(S)]^k,
```

with the convention that the bracketed term is zero when `a(S)=0`.

The availability ceiling is

```text
1 - sum_{S: a(S)=0} P(S).
```

This is the exact finite lower bound under the declared factor-independence and
conditional read-independence contract.

## Endpoint recovery

### Independent modes

Assign each mode its own unique failure factor. The model reduces to independent
mode availability.

### One common-mode factor

Assign the same single failure factor to every mode. All modes fail together and
the detection guarantee is capped by that one factor's availability.

### Partial sharing

When some factors are shared and others are unique, the guarantee lies between
those endpoints for comparable designs. Shared factors create correlation in mode
availability without forcing perfect common-mode failure.

## Example

Take three failure factors with probabilities

```text
rho = (0.1, 0.2, 0.3),
```

and two modes

```text
mode 0 factors = {0,1},
mode 1 factors = {1,2}.
```

Factor 1 is shared. For `k=3`, `r=2`, and `p_min=0.6`:

```text
q = 0.16,
P(all modes fail) = 0.224,
availability ceiling = 0.776,
joint detection lower bound = 0.6274907366031359.
```

The two modes are neither independent nor perfectly common-mode.

## Explicit non-claims

This theorem does not infer the latent factors, their probabilities, mode-factor
assignments, sensitivity, or ecological causes of failure. The factor graph is a
declared mathematical contract.
