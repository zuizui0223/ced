# Experiment-induced ecological quotient

## Setup

Let `W` be a finite set of latent ecological worlds, `D` a declared experiment,
`record_D(w)` the complete record generated under world `w`, and `T(w)` the report
target.

Define

```text
w ~_D w'  iff  record_D(w) = record_D(w').
```

## Theorem 1 — exact information supplied by a design

The classes of `~_D` form the exact quotient of latent worlds supplied by the
declared experiment. Every report computed only from the experiment record is
constant on these classes.

An exact deterministic report of `T` exists if and only if

```text
w ~_D w'  implies  T(w) = T(w').
```

When this condition fails, the exact record-based report is set-valued:

```text
{T(w): w belongs to the observed record class}.
```

## Theorem 2 — design refinement

A design `D2` refines `D1` when every pair of worlds separated by `D1` is also
separated by `D2`. Refinement can reduce residual latent ambiguity, but it need not
identify every latent world. It is sufficient for a requested report once the target
is constant on every remaining class.

## Bounded-support observations

For an observed record `x`, let `C_D(x)` be the nonempty set of latent worlds
compatible with the declared observation-error support. A deterministic report is
justified exactly when `T` is constant on `C_D(x)`; otherwise retain the compatible
target set.

## Joint presence and mechanism witness

Use worlds `(presence, response_type)` with both coordinates binary. The report
target is:

```text
absent              -> no interaction
present, type 0     -> response decreases
present, type 1     -> response increases
```

A passive design leaves all four worlds together. A detection design separates
presence but leaves the two present response types together. A combined detection
and intervention design yields three record classes: absent, present/type 0, and
present/type 1. The combined design therefore supports an exact target report even
though it does not distinguish the two response types when the interaction is
absent, where that distinction is target-irrelevant.

This is the essential CED–MRM bridge: presence and response mechanism are not merely
listed as separate uncertainties. They interact in the minimal record partition
required for the ecological report target.

## Scope

The theorem is finite and conditional on declared latent worlds, experiment
records, observation contracts, and report targets. It does not estimate those
objects from field data. Its novelty claim must rest on the ecological target-aware
quotient, the joint witness, and the integration with failure-aware evidence design,
not on the elementary fact that identical records cannot distinguish worlds.
