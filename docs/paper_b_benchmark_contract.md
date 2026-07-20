# Paper B benchmark contract

The comparative benchmark uses explicit experiment likelihood kernels and one shared terminal reporting rule.

## Latent worlds

Each finite world contains:

- current condition absent or present;
- response type A or B;
- one of four target-irrelevant latent attributes.

## Experiments

- state screening supplies imperfect condition detections;
- the response experiment supplies a noisy response-type observation;
- the nuisance experiment perfectly identifies only the target-irrelevant attribute.

An unperformed experiment contributes neither an observation nor a posterior update.

## Policies

All policies begin from the same prior, receive the same state-screen record, and use the same risk-limited terminal report. They differ only in follow-up selection:

- state-only stops after screening;
- full identification runs response and nuisance experiments;
- full-world EIG selects the experiment with maximum mutual information about the complete world;
- target-safe selects the least-cost experiment that can yield a deterministic target report within the false-resolution limit.

## Reporting contract

A singleton target is reported only when its posterior error is no greater than the declared false-resolution limit, including the equality boundary. Otherwise the report remains set-valued.

## Reproducibility

`scripts/simulate_paper_b_benchmark.py` writes the exact JSON, CSV, and LaTeX outputs. The reproducibility workflow executes the benchmark and uploads all three artifacts.
