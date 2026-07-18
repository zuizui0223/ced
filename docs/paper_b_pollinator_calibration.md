# Paper B realistic plant--pollinator calibration

## Purpose

This calibration replaces the illustrative benchmark values with a defensible field-monitoring protocol. It deliberately separates quantities supported by published field validation from quantities that remain operational sensitivity assumptions.

## Evidence-backed observation ranges

Automated flower-visitor monitoring in realistic field deployments retained true positives with on-device recall of approximately 0.77--0.83 across alpine meadow, sunflower, and apple systems. Final field classification accuracy varied from 0.76 to 0.89 across those systems, despite substantially higher performance for well represented honey-bee and bumble-bee classes. A separate unseen time-lapse evaluation localized approximately 91% of Hymenoptera and 81% of Diptera, but classification recall was lower, especially for Diptera.

The calibrated protocol therefore uses:

- per-session interaction detection: 0.77, 0.80, 0.83;
- per-block response typing: 0.76, 0.89, 0.95;
- three presence-screen sessions;
- three independently scheduled response-typing blocks;
- a false-resolution contract of 0.05.

The values are not interpreted as universal biological constants. They are field-performance anchors for a realistic mixed pollinator community.

## Derived protocol

Three presence screens at per-session detection 0.80 give cumulative detection

`1 - (1 - 0.80)^3 = 0.992`

when the sessions are operational and conditionally independent.

A single response-typing block with accuracy 0.89 has error 0.11 and therefore fails the 0.05 false-resolution contract. Three independent response-typing blocks with majority voting give

`0.89^3 + 3 * 0.89^2 * (1 - 0.89) = 0.966362`.

The calibrated target-safe policy therefore does not permit a deterministic increase/decrease report from one field classification. It requires at least three independent response blocks and a majority decision, or else retains `{increase, decrease}`.

## Failure architecture

The baseline shared-failure probability is set to 0.15, with 0.05--0.30 used for sensitivity analysis. This is an operational assumption rather than a published estimate. It represents a whole-window failure such as unsuitable weather, access loss, common power failure, or one failed processing batch.

At the baseline values:

- shared architecture joint target resolution: 0.8148;
- diversified architecture joint target resolution: 0.9347;
- gain from diversification: 0.1199.

The two designs use the same nominal three screens and three response blocks. The difference is whether failures are coupled. The practical recommendation is therefore to separate observation windows, power systems, access routes, observers, or processing batches where feasible.

## Costs

Costs remain relative protocol units:

- one screening session: 1 unit;
- one response-typing block: 4 units.

These values encode the fact that a manipulative response experiment is substantially more expensive than passive screening. They are not yet monetary estimates and must be replaced or accompanied by field-hour and equipment-cost accounting before submission.

## Manuscript claim now supported

The realistic calibration supports a narrower and stronger claim than the original toy example:

> Field-level classifier performance that is adequate for descriptive monitoring may still be inadequate for directional management reporting. Under a 5% false-resolution contract, one response classification at 0.89 accuracy is insufficient, whereas three independent response blocks with majority voting are sufficient. Coupling those blocks to one shared failure factor reduces joint target resolution by approximately 0.12 relative to diversified failures at the baseline calibration.

## Sources

- Smith et al. (2026), AutoPollS, Methods in Ecology and Evolution, DOI: 10.1111/2041-210x.70304.
- Stefan et al. (2025), automated pollinator detection on unseen time-lapse images, Scientific Reports / PubMed 40836004.
- Interval-photography validation against direct observation (2025), demonstrating comparable order-level composition but lower species-level identification.

## Remaining empirical replacement

The next field dataset should estimate, rather than assume:

1. the fraction of scheduled camera-hours lost to a common weather/access/power event;
2. per-session detection conditional on manual ground truth;
3. response-direction classification accuracy from independent intervention blocks;
4. labor, travel, equipment, and annotation cost per screen and response block.
