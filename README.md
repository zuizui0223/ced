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

## Ecological reading

Potential interpretations include phenological gates, seasonal corridors,
post-disturbance colonization, delayed pathogen exposure, seed-bank recruitment,
and camera or sensor panels sharing power, weather, access, or communication
failure domains. These are model contracts, not empirical claims established by
the finite certificates.

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
- `pytest` checks theorem witnesses, canonical panel behavior, and replay-report
  values.
- `scripts/verify_ced_core.py` writes a deterministic JSON artifact.

## Run

```bash
python -m pip install -e '.[dev]'
pytest
python scripts/verify_ced_core.py
```

The replay writes `artifacts/ced_core_report.json`.

## Scope

CED concerns declared finite deterministic grammars, resettable probe panels,
and declared failure-mode families. It does not infer delays, resetability,
closure, action grammars, failure probabilities, or ecological mechanisms from
observations.
