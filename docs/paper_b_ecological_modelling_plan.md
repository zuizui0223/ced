# Paper B: Ecological Modelling completion plan

## Fixed modelling claim

Paper B is a target-safe modelling layer for finite ecological evidence. It consumes candidate worlds and fitted or declared record models, then returns the sharpest management report justified by the compatible class and a failure-aware next experiment.

The manuscript does not claim a new occupancy estimator, a new generic identified-set theory, or a universal adaptive-control algorithm.

## Completed core benchmark

The comparative benchmark now uses exact enumeration rather than Monte Carlo sampling.

- latent worlds: interaction absent/present crossed with decrease/increase intervention response;
- detection sensitivity: 0.60, 0.80, 0.95;
- response-typing accuracy: 0.85, 0.95, 0.99;
- common-failure probability: 0, 0.15, 0.35;
- failure architecture: one shared factor versus independent events;
- strategies: occupancy-only, full identification, information gain, target-safe risk-limited;
- outputs: correct deterministic report, wrong deterministic report, honest ambiguity, expected cost.

This gives 216 exact strategy--scenario evaluations.

## Headline result

At common-failure probability 0.35, the best target-safe correct deterministic reporting probability is 0.354 under three screens sharing one failure factor and 0.514 under three screens with independent failure events. The 0.160 gain comes from failure diversification, not additional sample size.

Across the full grid, target-safe wrong deterministic reporting remains below the declared 0.05 contract. When response-typing accuracy is only 0.85, the policy abstains rather than forcing an intervention direction.

## Ecological interpretation

The actionable result is that monitoring replication should be classified by failure-factor membership. Three cameras in the same storm window, three visits blocked by the same access restriction, or three samples processed in one failed laboratory batch are not equivalent to three independently failing modes. Under a shared factor, nominal replication cannot cross the factor's availability ceiling.

## Remaining submission work

1. Calibrate one realistic plant--pollinator scenario with literature- or pilot-derived ranges for detection, typing accuracy, costs, and shared failures.
2. Add a manuscript figure plotting correct/wrong/ambiguous reporting against failure probability for shared and independent architectures.
3. Add the complete bibliography for occupancy, partial identification, adaptive monitoring, information gain, structural uncertainty, and common-cause failure.
4. Move theorem proofs to a supplement and retain only operational guarantees in the main paper.
5. Compile against the final Ecological Modelling journal format.

## Decision gate

The realistic calibration must preserve the qualitative architecture result. If plausible parameter ranges eliminate the shared-versus-independent resolution contrast, the paper should retreat to a conceptual framework claim. If the contrast persists, it becomes the central ecological modelling result and the main simulation figure.
