# Non-substitution of evidence resources

## Why this document exists

The manuscript carries the failure-architecture material as a single qualitative
proposition ("reliability of a target-relevant class split is bounded by the
availability of the observations required to realize that split"). The machinery
in `ced.mode_detection`, `ced.overlapping_modes`, and `ced.delayed` already
supports considerably sharper statements. This document records what those
statements are, as exact finite quantities.

`scripts/harvest_nonsubstitution.py` regenerates every number below and writes
`artifacts/nonsubstitution_harvest.json`. `tests/test_nonsubstitution_harvest.py`
pins the qualitative shape of each claim, so a change to the underlying
machinery that would invalidate the manuscript argument fails there first.

## The claim

> The resources that support an exact ecological conclusion — replication,
> failure-mode diversity, temporal horizon, representational capacity — are not
> mutually substitutable. Increasing one does not in general compensate for a
> deficit in another, and for several pairs no amount of one can compensate for
> any deficit in the other.

This is a different species of statement from the quotient and minimality
results elsewhere in the repository. Those are constructions, and the
construction literature is mature. Non-substitution statements are obstructions,
and they do not collide with it.

## Harvest 1 — replication saturates

Under the declared contract with `k = 3` coordinates, sensitivity lower bound
`p = 0.6`, and mode availability `a = 0.8`, joint detection within a fixed mode
structure approaches the availability ceiling `1 - (1 - a)^m` and stops there.

| modes | reads per mode | joint detection lower bound | ceiling |
|---:|---:|---|---|
| 1 | 1 | 0.17280000 | 0.8000 |
| 1 | 10 | 0.79974837 | 0.8000 |
| 1 | 100 | 0.80000000 | 0.8000 |
| 1 | 1000 | 0.80000000 | 0.8000 |
| 2 | 10 | 0.95989933 | 0.9600 |
| 2 | 1000 | 0.96000000 | 0.9600 |

Effort buys a great deal early and exactly nothing past the ceiling. The ceiling
depends only on the mode structure.

## Harvest 2 — the ceiling inverts into a structural necessary condition

Because the ceiling is read-independent, a target joint confidence is a
requirement on design structure before it is a requirement on budget. At
`a = 0.8`:

| target confidence | necessary modes | ceiling attained |
|---|---:|---|
| 0.90 | 2 | 0.96000 |
| 0.95 | 2 | 0.96000 |
| 0.99 | 3 | 0.99200 |
| 0.999 | 5 | 0.99968 |

`m >= ceil(log(1 - c) / log(1 - a))` is necessary. It is not sufficient: finite
sensitivity still requires reads within each mode. A design that fails the floor
cannot reach the target confidence at any budget, which is the operationally
useful direction.

## Harvest 3 — allocation matters at fixed effort

Thirty reads, distributed differently:

| design | total reads | joint detection lower bound | ceiling |
|---|---:|---|---|
| 1 mode x 10 reads | 30 | 0.799748 | 0.8000 |
| 2 modes x 5 reads | 30 | 0.950069 | 0.9600 |
| 5 modes x 2 reads | 30 | 0.989827 | 0.9997 |

Total effort is not a sufficient statistic for the strength of the evidence.

## Harvest 4 — the discriminating experiment

Harvests 1 to 3 compare independent modes against a single mode. The
substantive question is what happens in between, where real monitoring designs
live: modes that partly share a latent failure factor.

Four modes each carry one private failure factor at `rho = 0.2`. A fifth factor
at `rho = 0.2` is attached to the first `s` of them. Everything else — reads,
sensitivity, coordinate count, private factors — is held fixed across the sweep,
so any movement is attributable to sharing alone.

| `s` | ceiling | all modes fail | `r = 2` | `r = 10` | `r = 1000` |
|---:|---|---|---|---|---|
| 0 | 0.998400 | 0.001600 | 0.970659 | 0.998392 | 0.998400 |
| 1 | 0.997120 | 0.002880 | 0.960105 | 0.997108 | 0.997120 |
| 2 | 0.990720 | 0.009280 | 0.932879 | 0.990693 | 0.990720 |
| 3 | 0.958720 | 0.041280 | 0.871360 | 0.958663 | 0.958720 |
| 4 | 0.798720 | 0.201280 | 0.776527 | 0.798714 | 0.798720 |

Two findings follow, and they are not the same finding.

### Sharing and replication do not trade against each other at all

Sharing moves the ceiling itself, and reads only ever approach whatever ceiling
they are under. The comparison that settles it:

```text
unlimited reads under full sharing  (s = 4, r = 1000) = 0.798720
two reads under independence        (s = 0, r = 2)    = 0.970659
```

An unlimited read budget in a fully shared design loses to a two-read budget in
an independent one. No exchange rate exists between these two resources; the
relationship is a hard obstruction.

### Sharing and achievable confidence do trade, at an exact and strongly convex rate

The ceiling degrades smoothly in `s`, so there is an exact finite rate at which
sharing is paid for in achievable confidence. That rate is far from linear:

```text
s = 0 -> 1   costs 0.00128
s = 3 -> 4   costs 0.16000
```

The last mode to join the shared factor costs 125 times what the first one
costs. Ecologically this is the useful form of the result: **substantial overlap
between observation modes is nearly free, and complete overlap is
catastrophic.** Retaining a single mode that does not depend on the shared factor
avoids roughly four fifths of the total loss. A monitoring programme does not
need fully independent replication; it needs at least one genuinely independent
mode.

## Harvest 5 — horizon and memory are independent

The same question for a second resource pair. In the delayed-exposure family,
increasing the delay moves the revealing horizon without moving the interface
memory gap:

| ports | delay | revealing horizon | memory gap (bits) | blind before horizon |
|---:|---:|---:|---:|---|
| 4 | 0 | 1 | 3 | yes |
| 4 | 1 | 2 | 3 | yes |
| 4 | 5 | 6 | 3 | yes |
| 4 | 50 | 51 | 3 | yes |

The memory gap is a property of how many exterior coordinates can be separately
addressed; the horizon is a property of when the grammar first permits any of
them to be observed. Neither bounds the other, which is why no finite horizon
fixed in advance is adequate for the whole family.

## What this does not establish

The factor graph, failure probabilities, mode-factor assignments, sensitivity,
and availability are declared modelling contracts. Nothing here infers them from
data, and nothing here asserts that any particular monitoring programme has a
given failure architecture.

That boundary is worth stating precisely because it is also where the most
valuable next step lies. The ceiling `1 - (1 - a)^m` is a falsifiable prediction
about real monitoring programmes: one that increases replication without
increasing failure-mode diversity should show detection probability plateauing.
Testing it requires estimating `a` and `m` from study metadata, which crosses the
scope restriction the repository has held everywhere else. That crossing is a
decision to be taken deliberately, not by drift.

## Relation to the manuscript

The current Proposition (failure-controlled refinement) states the qualitative
claim only. Harvests 1, 2, and 4 are theorem-level and belong in the main text;
harvest 3 is the figure; harvest 5 belongs with the delayed-exposure material,
which is presently absent from the manuscript entirely.
