# CED standalone verification audit

## Purpose

CED was reconstructed from frozen CCOC legacy assets. This audit records what the
standalone package verifies, what is preserved analytically from legacy, and what
is deliberately not claimed by a passing test suite.

## Source-to-successor map

| CCOC legacy asset | CED public core | Status |
|---|---|---|
| delayed addressability / no-uniform-horizon family | `ced.delayed.DelayedExposureFamily` | migrated as a finite witness interface |
| reset-panel partial quotient and budget frontiers | `ced.panels.PanelCoverage` | migrated as an exact signature/count construction |
| common-mode canonical panel analysis | `ced.robustness.CommonModeProfile` | migrated as finite mode-cover robustness |
| no CCOC predecessor | `ced.detection.OneSidedDetector` | new one-sided imperfect-detection extension |

The relay-tree compilation and CCOC open-composition manuscript theorem are not
CED dependencies. They remain provenance in the frozen archive.

## What the checks establish

The standalone tests and replay verify that:

1. every proposed finite horizon has a delayed witness whose first revealing word
   is later than that horizon;
2. canonical panel signatures ignore trial order, duplicate probes, and wait-only
   trials;
3. retained and residual signature counts multiply to the declared binary state
   space size;
4. trial, action, and temporal-depth resources are not silently conflated in the
   implemented budget helper;
5. common-mode robustness depends on failure-mode cover number, not raw replicate
   count; and
6. under the declared one-sided detection contract, finite all-negative records
   remain compatible with presence while repeated reads give an exact lower bound
   for joint positive-detection probability.

## Independent finite-oracle checks

`tests/test_exhaustive_oracles.py` separately enumerates bounded finite cases
rather than asserting only the package's own closed-form outputs. It checks:

- delayed grammars and the no-uniform-horizon witness on small grids of module
  counts, delays, and horizons;
- every binary state class of small reset panels, including the number of
  signatures and the size of every residual class;
- canonical parsing of all short trial streams and the resource frontier over
  small trial, action, and delay budgets; and
- direct enumeration of declared common-mode failure subsets, including
  overlapping modes.

`tests/test_detection_oracles.py` separately enumerates every binary observation
record over bounded repeat panels. It checks the single-coordinate and joint
detection formulas, the minimal-repeat helper, and the fact that a fully
negative signature is not an absence certificate when sensitivity is imperfect.

These are implementation cross-checks, not automated proofs of the unbounded
all-family theorems. Their role is to catch formula, normalization, and
boundary-condition regressions that fixed replay witnesses can miss.

## Analytic theorem versus replay

The all-family no-uniform-horizon statement and the exact quotient claims remain
mathematical consequences of their declared finite grammar and panel contracts.
The imperfect-detection extension is a theorem under its own explicit
zero-false-positive, bounded-sensitivity, conditional-independence, and
resettable-read contract. The replays are regression witnesses for selected
values; they are not automated proofs of the all-system theorems.

## Explicit boundaries

The current imperfect-detection extension does not cover false positives,
unknown sensitivity bounds, dependent repeats, non-reset monitoring,
common-mode observation failure combined with imperfect detection, adaptive
policies, probabilistic delays, unknown failure architectures, or inference of
a real ecological closure boundary. Those are next-theorem targets, not hidden
claims of the current package.
