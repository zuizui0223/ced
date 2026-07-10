# Adaptive allocation by alpha spending

## Declared design contract

A monitoring policy may choose the next coordinate, camera, mode, or confirmation
stage after observing earlier outcomes. For each adaptively selected stage `s`,
assume that under the null state for the relevant coordinate, the conditional
false-alert probability is bounded by a declared spend `alpha_s`:

```text
P(stage s alerts | past history, coordinate absent, stage s selected) <= alpha_s.
```

The policy records every selected stage in an alpha-spending ledger. The ledger
may be path-specific during execution or pre-authorized by a conservative list of
all stages that may be selected.

## Theorem 1 — anytime false-alert spending

For any adaptive policy satisfying the conditional bound above,

```text
P(any false alert) <= E[sum_{selected s} alpha_s].
```

If every possible path is constrained to spend at most `A`, then

```text
P(any false alert) <= A.
```

A conservative all-possible-stage ledger gives the simpler bound

```text
P(any false alert) <= min(1, sum_s alpha_s).
```

This is an anytime union-bound theorem. It does not require independence across
selected stages and does not require the stopping rule to be fixed in advance.

## Theorem 2 — coordinate and weighted budgets

If stages are assigned to coordinates, then under the all-absent state,

```text
E[number of false alerts] <= sum_s alpha_s.
```

For nonnegative coordinate weights `w_i`,

```text
E[sum_i w_i false_alert_i] <= sum_i w_i sum_{s assigned to i} alpha_s.
```

These are alpha-accounting statements, not detection-power statements.

## Example

Consider an adaptive path over three coordinates with four possible spends:

```text
coordinate 0, camera-a screen:  alpha = 0.005
coordinate 1, camera-b screen:  alpha = 0.010
coordinate 0, camera-c confirm: alpha = 0.002
coordinate 2, camera-a screen:  alpha = 0.003
```

The ledger gives

```text
total spent alpha = 0.020,
familywise false-alert upper bound = 0.020,
per-coordinate spent alpha = (0.007, 0.010, 0.003),
prefix familywise bounds = (0.005, 0.015, 0.017, 0.020).
```

For weights `(1, 2, 5)`, the weighted false-alert budget is

```text
0.007 + 2*0.010 + 5*0.003 = 0.042.
```

## Explicit non-claims

This theorem does not infer that an adaptive policy is powerful, optimal, or
unbiased. It does not infer sensitivity, false-positive rates, coordinate states,
mode independence, or posterior probabilities. It only states how to keep
false-alert risk valid when allocation and stopping are chosen adaptively.
