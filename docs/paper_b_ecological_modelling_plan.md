# Paper B: Ecological Modelling completion plan

## Fixed modelling claim

Paper B is a target-safe modelling layer that separates ecological state estimation from prediction-target reportability. It consumes candidate worlds and fitted or declared record models, then returns the sharpest ecological prediction justified by the compatible class and a target-relevant next experiment.

The manuscript does not claim a new occupancy estimator, generic identified-set theory, or universal adaptive-control algorithm.

## Ecological scope

The framework is deliberately general and is not tied to a focal taxon or interaction system. The main manuscript develops four recurring structures:

- degraded ecosystem state versus restoration response;
- invasion detection versus control response;
- population decline versus demographic intervention;
- regime identification versus reversibility.

The common problem is that present-state evidence can be strong while compatible mechanisms imply different future or intervention consequences.

## Completed comparative benchmark

The exact benchmark now uses 16 latent worlds:

- management condition absent/present;
- intervention-response type A/B;
- a four-level latent attribute that does not affect the declared prediction target.

It compares state-only, full-identification, full-world expected-information-gain, and target-safe risk-limited strategies across state detectability, response-experiment accuracy, common failure, and shared versus independent evidence architectures.

The target-irrelevant experiment perfectly resolves the four-level attribute and therefore yields 2 bits of full-world information. At response accuracy 0.95, the response experiment yields approximately 0.714 bits. A genuine full-world EIG rule therefore selects the target-irrelevant experiment, whereas target-safe design selects the response experiment. At response accuracy 0.99, target-safe design resolves the prediction target more often than EIG and costs less than full latent-world identification.

## Remaining submission work

1. Convert the benchmark outputs into final figures: state accuracy versus prediction reportability, full-world information versus target information, and failure-architecture sensitivity.
2. Generalize the prediction target language beyond intervention response where useful, including future state, recovery, persistence, and regime transition.
3. Add complete references for occupancy, structural uncertainty, partial identification, adaptive monitoring, value of information, regime shifts, restoration, and ecological forecasting.
4. Move formal proofs and implementation details into the supplement.
5. Compile against the final Ecological Modelling format and perform a claim-by-claim reviewer audit.

## Decision gate

Paper B succeeds only if it demonstrates that target-relative modelling changes ecological experiment choice. The decisive contrast is now explicit: an experiment can maximize information about the latent ecological world while contributing nothing to the prediction that matters.
