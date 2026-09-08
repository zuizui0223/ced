# EVIDENCE figure architecture

Status: figure-production plan for `manuscript/EVIDENCE_DRAFT_V1.md`.

## Figure 1 — From current boundary to target-safe requirement

Panel A — current observation map

Show latent mechanism coordinates and observation matrix `M` with residual structural dimension

`k - rank(M)`.

Panel B — precision versus new identification direction

- repeated/more precise row in current span -> same structural rank;
- new row outside current span -> structural dimension decreases.

Panel C — experiment-induced compatible class

A realised record induces one compatible-world block.

Panel D — target-safe refinement

Within that compatible class, retain only distinctions that can change the declared target/successor report.

Caption firewall:

- Boundary supplies current structural limit;
- CED target-safe quotient supplies required target-relative refinement;
- required refinement is not evidence that the current record already identifies the refined block.

## Figure 2 — Mechanism-learning value and target-licensing value diverge

Use the new exact eight-world benchmark.

Worlds:

`binary target x four-level target-irrelevant nuisance`.

Panel A — candidate observations

- nuisance_detail: four outcomes, 2 bits full mechanism information;
- target_split: two outcomes, 1 bit full mechanism information;
- constant_probe: one outcome, 0 bits.

Panel B — learning ranking

```text
nuisance_detail (2 bits)
>
target_split (1 bit)
>
constant_probe (0 bits)
```

Panel C — exact target-resolution probability

- nuisance_detail: `0.0`;
- target_split: `1.0`;
- constant_probe: `0.0`.

Panel D — integrated message

```text
mechanism-learning top != target-licensing top
```

This is the key new integrated Evidence figure.

## Figure 3 — Information-guided mechanism resolution in the frozen MROD benchmark

Budget-2 primary comparison:

| metric | information-guided | random order |
|---|---:|---:|
| convergence | 0.990 | 0.435 |
| initial confounding edges resolved | 1.000 | 0.6045 |
| mean observations | 1.505 | 1.821 |
| nuisance selections | 0.001 | 0.974 |
| false exclusion | 0.000 | 0.000 |

Secondary budget-4 inset:

- information-guided convergence `0.999` versus random `0.940`;
- both resolve all initial edges on average;
- mean observations `1.518` versus `2.673`;
- nuisance selections `0.014` versus `1.169`.

Caption boundary: controlled declared-candidate mechanism-learning benchmark, not universal natural-system optimality.

## Figure 4 — Failure architecture controls trustworthy refinement

Panel A — repeated reads in one shared failure mode.

Panel B — same raw effort distributed across independent modes.

Panel C — worst-case guarantee ceiling under lower-bound mode availability `a`:

`1 - (1-a)^m`.

Panel D — interpretation ladder:

```text
ideal new direction
    !=
reliably observable direction
    !=
licensed target report
```

Keep detailed heterogeneous-threshold/calibration/concentration machinery in Supplement.

## Figure 5 — Objective-relative adaptive evidence loop

```text
current compatible worlds
       |
       v
Boundary: unresolved distinctions
       |
       v
CED: target-relevant requirement
       |
       +---------------------+
       |                     |
       v                     v
MROD learning utility    CED licensing utility
       |                     |
       +----------+----------+
                  v
         reliability gate
                  |
                  v
       select candidate before outcome
                  |
                  v
            acquire outcome
                  |
                  v
        update compatible worlds
                  |
       +----------+----------+
       |          |          |
 target licensed  learning   budget/prediction
 -> report/stop   limit      limit
                  |
             remain ambiguous
```

Purpose: integrate the two utilities without pretending they are one scalar.

## Supplementary figures

S1 — Boundary product/coordinate-anchor corollaries and calibration family.
S2 — exact target-safe quotient finite witness and minimality oracle.
S3 — full MROD budget sweep and seed ranges.
S4 — CED equal-effort shared-versus-independent failure witness.
S5 — existing CED schema-v5 full-world-EIG target-irrelevance benchmark.
S6 — target-switch and false-resolution sensitivity.

## Production rule

Quantitative panels must be generated from pinned machine-readable artifacts. The new Figure 2 must be generated from `manuscript/evidence_learning_licensing_result.json`; do not manually draw its numeric bars or rankings without a source-data sidecar.
