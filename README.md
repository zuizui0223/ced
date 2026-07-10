# CED — Closure Evidence Design

CED is a theorem-first mathematical-ecology repository for a finite evidence
question:

> When does finite monitoring fail to certify ecological closure, and what exact
> partial information can a declared intervention panel recover instead?

It is the standalone successor of CCOC legacy `ID-1` and the relevant
`LEGACY-1` panel-design results. CCOC remains frozen provenance; this repository
contains the active development core.

## Theorem core

1. **Delayed exposure / no uniform horizon.** Every fixed finite grammar-aware
   system has a finite exact horizon, but no single passive finite observation
   horizon certifies closure uniformly over families whose legal exterior exposure
   is delayed arbitrarily far.
2. **Exact partial panel quotient.** A reset panel identifies exactly the focal
   baseline, the exterior coordinates it probes, and the response-type coordinate
   if it performs the intervention probe.
3. **Distinct design resources.** Fresh-trial count, total action budget, and
   per-trial temporal depth yield distinct identification frontiers.
4. **Common-mode robustness.** A panel survives a declared number of failures
   when every required separator set cannot be covered by that many common-mode
   failure groups. Raw replicate count is not failure diversity.
5. **One-sided imperfect detection.** With declared zero false positives,
   bounded sensitivity, and resettable independent reads, positive detections are
   certificates of presence but finite non-detections do not certify absence. A
   repeat frontier gives the exact effort required for a declared joint
   positive-detection confidence. See
   [the imperfect-detection theorem](docs/imperfect_detection_theorem.md).
6. **Mode-diverse imperfect detection.** Under independent declared failure modes,
   repeats inside one mode improve sensitivity but cannot overcome the probability
   that every selected mode fails together. The exact joint-detection frontier
   separates repeats per mode from the number of independent modes. See
   [the common-mode detection theorem](docs/mode_diverse_detection_theorem.md).
7. **Bounded false positives.** When false positives are allowed, threshold
   crossings are no longer presence certificates. A positive-count threshold
   instead has a posterior-free evidence-ratio lower bound against the declared
   absence model. See
   [the false-positive threshold theorem](docs/false_positive_threshold_theorem.md).
8. **Multiple-coordinate threshold control.** Screening many declared coordinates
   inflates the probability of at least one false alert. A Bonferroni familywise
   bound stays valid without cross-coordinate independence; an exact all-absent
   formula is available only when independence is declared. See
   [the multiple-testing threshold theorem](docs/multiple_testing_threshold_theorem.md).
9. **Calibration-derived error bounds.** Blank and present controls can supply
   conservative one-sided binomial bounds for `f_max` and `p_min`, avoiding the
   pretense that detection error rates are known exactly. See
   [the calibration-bound theorem](docs/calibration_bounds_theorem.md).

## Ecological reading

Potential interpretations include phenological gates, seasonal corridors,
post-disturbance colonization, delayed pathogen exposure, seed-bank recruitment,
and camera or sensor panels sharing power, weather, access, or communication
failure domains. Imperfect-detection coordinates may represent a target taxon,
an interaction channel, a pathogen signal, or a prespecified environmental
exposure. These are model contracts, not empirical claims established by the
finite certificates.

## Provenance

The initial standalone core is reconstructed from the frozen CCOC legacy source
at `zuizui0223/ccoc`, especially:

- `docs/delayed_addressability.md`;
- `docs/delayed_joint_budgeted_quotients.md`; and
- `docs/common_mode_canonical_panels.md`.

The migration narrows the public surface to the evidence-and-design program. It
does not import CCOC's open-composition manuscript theorem or MLTR's
replacement/rewiring transport theory.

## Verification

- [Standalone verification audit](docs/standalone_verification_audit.md) —
  source-to-successor mapping, replay boundary, and added invariants.
- `pytest` checks theorem witnesses, canonical panel behavior, bounded independent
  oracles, imperfect-detection outcome enumerations, direct common-mode outcome
  enumerations, threshold evidence enumerations, multiple-coordinate familywise
  enumerations, and calibration coverage enumerations.
- `scripts/verify_ced_core.py` writes the deterministic finite-core artifact.
- `scripts/verify_imperfect_detection.py` writes the independent-read replay.
- `scripts/verify_mode_detection.py` writes the common-mode replay.
- `scripts/verify_threshold_detection.py` writes the false-positive replay.
- `scripts/verify_multiple_testing.py` writes the multiple-testing replay.
- `scripts/verify_calibration_bounds.py` writes the calibration-bound replay.

## Run

```bash
python -m pip install -e '.[dev]'
pytest
python scripts/verify_ced_core.py
python scripts/verify_imperfect_detection.py
python scripts/verify_mode_detection.py
python scripts/verify_threshold_detection.py
python scripts/verify_multiple_testing.py
python scripts/verify_calibration_bounds.py
```

The replays write `artifacts/ced_core_report.json`,
`artifacts/ced_imperfect_detection_report.json`,
`artifacts/ced_mode_detection_report.json`,
`artifacts/ced_threshold_detection_report.json`,
`artifacts/ced_multiple_testing_report.json`, and
`artifacts/ced_calibration_bounds_report.json`.

## Scope

CED concerns declared finite deterministic grammars, resettable probe panels,
declared failure-mode families, explicit observation contracts, and declared
calibration-control contracts. It does not infer delays, resetability, closure,
action grammars, failure probabilities, detection sensitivity, false-positive
rates, calibration representativeness, target-set size, mode availability,
independence, coordinate semantics, or ecological mechanisms from observations.
