# Paper B: Ecological Modelling completion plan

## Fixed modelling claim

Paper B is a target-safe modelling layer that separates ecological state estimation from intervention-response reportability. It consumes candidate worlds and fitted or declared record models, then returns the sharpest management report justified by the compatible class and a target-relevant next experiment.

The manuscript does not claim a new occupancy estimator, a new generic identified-set theory, or a universal adaptive-control algorithm.

## Ecological scope

The framework is deliberately general and is not tied to a focal taxon or interaction system. The main manuscript develops four recurring structures:

- degraded ecosystem state versus restoration response;
- invasion detection versus control response;
- population decline versus demographic intervention;
- regime identification versus reversibility.

The common problem is that present-state evidence can be strong while compatible mechanisms imply different intervention consequences.

## Comparative benchmark

The benchmark uses a generic state--response world model rather than a system-specific case.

- latent worlds: management condition absent/present crossed with response type A/B;
- state-observation sensitivity: 0.60, 0.80, 0.95;
- response-typing accuracy: 0.85, 0.95, 0.99;
- common-failure probability: 0, 0.15, 0.35;
- failure architecture: one shared factor versus independent events;
- strategies: state-only, full identification, information gain, target-safe risk-limited;
- outputs: correct deterministic report, wrong deterministic report, honest ambiguity, expected cost.

This gives 216 exact strategy--scenario evaluations.

## Central empirical questions

1. Can state accuracy be high while intervention-response reportability remains low?
2. Does full identification spend effort on distinctions with identical management consequences?
3. Can generic information gain select an experiment that is inferior for the declared target?
4. Can shared observation structure prevent nominal replication from increasing reportability?

## Remaining submission work

1. Expand the benchmark so target-irrelevant latent dimensions are explicit rather than only discussed.
2. Implement a genuine expected-information-gain policy instead of a simplified proxy.
3. Add manuscript figures for state accuracy versus response reportability, target-irrelevant effort, and failure architecture.
4. Add complete references for occupancy, structural uncertainty, partial identification, adaptive monitoring, regime shifts, restoration, and intervention prediction.
5. Move formal proofs into the supplement and compile against the final Ecological Modelling format.

## Decision gate

Paper B succeeds only if the benchmark shows that the proposed layer changes ecological model construction or experiment choice. Failure architecture is supporting evidence, not the sole contribution. The headline result must remain the structural gap between knowing the present state and knowing the consequence of intervention.
