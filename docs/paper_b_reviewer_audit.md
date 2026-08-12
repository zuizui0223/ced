# Paper B reviewer audit

This document records the strongest likely reviewer objections and the repository evidence that answers them. It is not manuscript prose and should be updated whenever a claim, benchmark contract, theorem placement, or generated artifact changes.

## 0. "This is a collection of methods without one ecological conclusion"

**Answer:** the main text is frozen around four linked results, not around the full repository theorem inventory:

1. experiment-induced ecological quotient + honest report criterion;
2. unique coarsest target-safe quotient;
3. failure architecture as the constraint on trustworthy refinement;
4. adaptive risk-limited target resolution.

The ecological conclusion is that monitoring should resolve distinctions among possible futures rather than maximize latent-state resolution as such. Full identification can be unnecessary when remaining distinctions do not change the target, and additional information can be insufficient when it is target-irrelevant or collected under a shared failure architecture.

**Repository authority:** `docs/paper_b_theorem_consolidation.md` and `docs/publication_completion_spine.md` define the combined-paper hierarchy. The older `docs/manuscript_architecture.md` remains provenance for standalone CED and must not be used to re-promote the delayed-closure, calibration, threshold, or multiple-testing theorem families into equal-weight Paper B Results.

**Story gate:** a new submission-facing section must state which of the four results it strengthens. If it does not strengthen one of them or close a reviewer-visible logical gap, it belongs in Supplement, future work, or a companion paper.

## 1. "This is only value of information with another utility"

**Concede:** target-safe design can be represented inside Bayesian decision theory by a constrained loss or utility.

**Distinct modelling contribution:** the framework makes the prediction target, admissible false-resolution rate, abstention rule, set-valued report, and target-preserving quotient explicit without requiring a cardinal management utility over all outcomes.

**Repository evidence:**

- `manuscript/paper_b_reviewer_sections.tex`, method-boundary subsection and comparison table;
- `scripts/analyze_paper_b_reviewer_robustness.py`, target-switch analysis;
- `tests/test_paper_b_reviewer_robustness.py`, experiment-choice reversal under a changed target;
- `docs/paper_b_literature_boundary_audit.md`, primary-source boundary with Bayesian design and ecological VOI.

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

**Repository evidence:** `scripts/analyze_paper_b_posterior_bridge.py` demonstrates the finite-support bridge while explicitly disclaiming empirical status.

**Language to avoid:** "applies directly to arbitrary continuous models" or "guarantees are unchanged under discretization."

## 5. "The benchmark changes reporting rules between methods"

**Answer:** all strategies start from the same screening posterior and use the same risk-limited terminal report. Only the selected follow-up experiment differs. This is tested in the schema-v5 benchmark.

## 6. "The ecological consequence is unclear"

**Answer:** the invasion example distinguishes occurrence, eradication response, and source-pathway targets. Each target justifies a different observation, showing a changed management-facing experiment rather than a generic recommendation for more monitoring. The manuscript conclusion states the corresponding general principle explicitly: measure distinctions that separate possible futures, not latent state for its own sake.

## 7. "Why is the closure/imperfect-detection/calibration mathematics not a fifth or sixth main result?"

**Answer:** those theorem families remain valid repository mathematics, but the combined Paper B has a different explanatory hierarchy. Delayed exposure motivates the finite-evidence boundary; imperfect detection and calibration justify observation contracts; threshold, concentration, and adaptive-spending results support failure-aware refinement. They do not each define an additional ecological conclusion beyond the four-result spine.

**Language to avoid:** describing demoted results as discarded, obsolete, or unimportant. They are supporting mathematics and theorem provenance.

## 8. "The shared-mode ceiling has the probability inequality backwards"

**Concede the distinction:** a declared mode availability of **at least** `a` is a lower bound, so `1-(1-a)^m` cannot be an upper bound on the realized detection probability of every admissible system. A system with true availability above `a` may detect more often.

**Correct claim:** the least-favourable admissible system has availability exactly `a`. Therefore `1-(1-a)^m` is the supremum of the joint-detection guarantee that can be certified uniformly over the lower-bound contract using arbitrarily many within-mode repeats. It becomes an actual realized ceiling only when the true availability is exactly the stated value (or exact failure probabilities are separately specified).

**Repository evidence:**

- `docs/mode_diverse_detection_theorem.md` states the least-favourable theorem and exact-bound case;
- `ced/mode_detection.py` computes `joint_detection_lower_bound` and labels `availability_ceiling` as a worst-case guarantee ceiling for backward API compatibility;
- `ced/overlapping_modes.py` uses exact factor failure probabilities, so its availability ceiling is an actual probability ceiling under that separate contract.

**Language to avoid:** "availability at least `a` implies actual detection cannot exceed `1-(1-a)^m`."

## 9. "The paper relabels established ideas as novelty"

**Answer:** the nearest-neighbour audit explicitly concedes the established ingredients and restricts novelty to their combined ecological reportability role.

**Primary boundaries that must remain explicit:**

- occupancy and generalized occupancy already model imperfect detection, including false positives;
- partial-identification theory already legitimizes sharp set-valued conclusions;
- model averaging and ecological forecasting already address structural and predictive uncertainty;
- Bayesian experimental design already permits target-specific utilities and losses;
- ecological VOI already values data through management consequences;
- adaptive monitoring/management are already question-driven and iterative;
- bisimulation and model minimization already provide state aggregation and partition-refinement machinery.

**Repository authority:** `docs/paper_b_literature_boundary_audit.md` and `tests/test_paper_b_literature_contract.py`.

**Safe novelty statement:** Paper B links a finite experiment-induced latent-world partition to a declared ecological target, computes the coarsest action-stable target-preserving refinement, checks whether observation failure permits that refinement to be trusted, and evaluates adaptive stopping/experiment choices under an explicit false-resolution contract.

**Language to avoid:** any novelty claim attached to equivalence classes, partition refinement, set-valued inference, imperfect detection, question-driven monitoring, Bayesian utility design, or VOI in isolation.

## 10. Claims that remain conditional

- The world set may omit relevant mechanisms.
- Priors and likelihood kernels may be misspecified.
- A finite approximation may hide target-relevant distinctions.
- Failure-mode partitions, independence, sensitivity, and calibration representativeness are declared assumptions unless separately estimated.
- Lower-bound availability parameters support worst-case guarantees, not upper bounds on realized detection.
- Target-safe design does not replace management utility when utilities are available and defensible.
- The current benchmark demonstrates a possibility and mechanism, not universal dominance over EIG or VOI.
- The posterior-sample bridge is a methodological demonstration, not an empirical validation.

## Merge gate

Before any submission-facing merge:

1. Python 3.10--3.12 tests pass.
2. Deterministic benchmark, reviewer-robustness, and posterior-bridge artifacts regenerate.
3. `paper_b_compiled.tex` compiles with figures, tables, reviewer sections, and bibliography.
4. Generated tables match the JSON source.
5. The title, abstract, Introduction contribution hierarchy, Result headings, Discussion, and Conclusion all express the same four-result spine.
6. No prose claims universal superiority over VOI, EIG, or continuous-state methods.
7. No lower-bound observation parameter is described as an upper bound on realized performance unless an exact or upper-bounded failure contract justifies that direction.
8. Every submission-facing novelty claim has a nearest-neighbour boundary in `docs/paper_b_literature_boundary_audit.md` and does not attribute novelty to an established ingredient in isolation.
9. No new theorem family is promoted to main text without identifying which of the four headline conclusions it changes or which reviewer-visible logical gap it closes.
