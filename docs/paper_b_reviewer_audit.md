# Paper B reviewer audit

This document records the strongest likely reviewer objections and the repository evidence that answers them. It is not manuscript prose and should be updated whenever a claim, benchmark contract, or generated artifact changes.

## 1. "This is only value of information with another utility"

**Concede:** target-safe design can be represented inside Bayesian decision theory by a constrained loss or utility.

**Distinct modelling contribution:** the framework makes the prediction target, admissible false-resolution rate, abstention rule, set-valued report, and target-preserving quotient explicit without requiring a cardinal management utility over all outcomes.

**Repository evidence:**

- `manuscript/paper_b_reviewer_sections.tex`, method-boundary subsection and comparison table;
- `scripts/analyze_paper_b_reviewer_robustness.py`, target-switch analysis;
- `tests/test_paper_b_reviewer_robustness.py`, experiment-choice reversal under a changed target.

**Language to avoid:** "VOI cannot target decisions" or "target-safe design is outside decision theory."

## 2. "The result is manufactured by choosing one convenient target"

**Answer:** target relativity is the declared scientific contract, not a hidden tuning choice. Holding worlds, priors, costs, and likelihoods fixed, the selected experiment reverses when the target changes from management response to context classification.

**Required evidence:** generated `paper_b_target_switch.tex` and the exact 1/0 versus 0/1 resolution probabilities.

## 3. "The method is hard-coded to a 5% error rate"

**Answer:** the error limit is an input constraint. At response accuracy 0.95, a 1% limit retains ambiguity and avoids follow-up cost, whereas 5% and 10% limits admit the response experiment. Wrong deterministic reporting remains within each declared contract.

**Required evidence:** `paper_b_reviewer_robustness.json` and `paper_b_threshold_sensitivity.tex`.

## 4. "Finite worlds make the framework irrelevant to real ecological models"

**Concede:** exact guarantees are conditional on a finite representation.

**Answer:** posterior draws, particles, scenarios, parameter bins, or ensemble members can supply that representation. The manuscript explicitly avoids claiming a universal continuous-state convergence theorem and requires discretization adequacy to be checked against the target.

**Language to avoid:** "applies directly to arbitrary continuous models" or "guarantees are unchanged under discretization."

## 5. "The benchmark changes reporting rules between methods"

**Answer:** all strategies start from the same screening posterior and use the same risk-limited terminal report. Only the selected follow-up experiment differs. This is tested in the schema-v5 benchmark.

## 6. "The ecological consequence is unclear"

**Answer:** the invasion example distinguishes occurrence, eradication response, and source-pathway targets. Each target justifies a different observation, showing a changed management-facing experiment rather than a generic recommendation for more monitoring.

## 7. Claims that remain conditional

- The world set may omit relevant mechanisms.
- Priors and likelihood kernels may be misspecified.
- A finite approximation may hide target-relevant distinctions.
- Target-safe design does not replace management utility when utilities are available and defensible.
- The current benchmark demonstrates a possibility and mechanism, not universal dominance over EIG or VOI.

## Merge gate

Before any submission-facing merge:

1. Python 3.10--3.12 tests pass.
2. Deterministic benchmark and reviewer-robustness artifacts regenerate.
3. `paper_b_compiled.tex` compiles.
4. Generated tables match the JSON source.
5. No prose claims universal superiority over VOI, EIG, or continuous-state methods.
