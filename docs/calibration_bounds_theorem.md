# Calibration-derived detection bounds

## Declared calibration contract

The earlier threshold layers assume declared constants `p_min` and `f_max`. This
layer explains how those constants may be conservatively derived from finite
calibration controls.

Use two independent calibration panels:

1. **Blank controls.** Run `b` reads on known-absent targets and observe `z` false
   positives.
2. **Present controls.** Run `c` reads on known-present targets and observe `y`
   positives.

The calibration reads are assumed resettable and conditionally independent inside
each control class. The control labels must be known before the detection record
is interpreted.

## Theorem 1 — false-positive upper bound

For confidence level `1 - delta`, define `f_U` by

```text
P_{f_U}[X <= z] = delta,   X ~ Binomial(b, f_U),
```

with the vacuous value `f_U = 1` when `z = b`.

Then the random interval `[0, f_U]` covers the true false-positive probability
with probability at least `1 - delta` under the blank-control model.

## Theorem 2 — sensitivity lower bound

For confidence level `1 - delta`, define `p_L` by

```text
P_{p_L}[X >= y] = delta,   X ~ Binomial(c, p_L),
```

with the vacuous value `p_L = 0` when `y = 0`.

Then the random interval `[p_L, 1]` covers the true sensitivity with probability
at least `1 - delta` under the present-control model.

## Combined conservative design

If the blank-control and present-control calibration panels are treated as
separate one-sided statements, a Bonferroni lower bound on simultaneous coverage
is

```text
1 - 2 delta.
```

The derived values can be passed into the threshold evidence design as

```text
f_max = f_U,
p_min = p_L.
```

If `f_U >= p_L`, the calibration data do not separate the declared false-positive
and sensitivity contracts strongly enough for the threshold evidence layer.

## Example

With `b = 60`, `z = 0`, `c = 60`, `y = 55`, and `delta = 0.05`:

```text
f_U ≈ 0.04870291331,
p_L ≈ 0.83273692357,
per-bound confidence = 0.95,
Bonferroni simultaneous confidence >= 0.90.
```

Using those conservative bounds with `n = 5`, `t = 3` gives

```text
P(threshold | absent) <= 0.001072470525,
P(threshold | present) >= 0.964160039883,
evidence ratio >= 899.008427422.
```

For `M = 20` coordinates, the Bonferroni familywise false-alert bound is

```text
20 * 0.001072470525 = 0.021449410494.
```

## Explicit non-claims

This theorem does not infer whether calibration controls are representative of
field observations, whether reads are independent, whether target coordinates are
correctly labeled, or whether error rates remain stable across seasons, cameras,
observers, or sites. It only converts declared calibration controls into finite
one-sided bounds under the stated binomial contracts.
