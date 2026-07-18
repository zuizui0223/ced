# Paper B novelty and journal strategy

## Fixed claim

**Honest Ecological Prediction from Finite Evidence** is not presented as a new occupancy model, a new generic equivalence relation, or a universal adaptive-design algorithm. Its contribution is the integration of four objects that are usually treated separately:

1. an experiment-induced partition of finite latent ecological worlds;
2. the exact boundary between deterministic and set-valued target reporting;
3. the unique coarsest observation-preserving, action-stable quotient retaining only target-relevant distinctions;
4. failure-aware adaptive experiment selection under explicit false-resolution and cost constraints.

The central question is:

> Given finite evidence, mechanism ambiguity, imperfect observation, and a declared management target, what is the sharpest ecological report the experiment honestly supports, and what additional experiment can safely sharpen it?

## Nearest prior literatures and the boundary

### 1. Occupancy and imperfect detection

Occupancy models beginning with MacKenzie et al. separate ecological state from observation and estimate presence when detection is below one. Multi-method and multispecies extensions address heterogeneous detection and richer ecological structure.

**Overlap:** nondetection does not imply absence; replication and observation models matter.

**Difference:** Paper B does not compete as a better occupancy estimator. It treats presence as only one coordinate of a finite latent world and asks whether the complete compatible class supports a deterministic *target report*, including intervention-response mechanism. A presence estimate can therefore be resolved while the management response remains honestly set-valued.

### 2. Partial identification and set-valued inference

Manski, Imbens--Manski, Tamer, and later work show that data and assumptions may identify sets rather than points and that reporting should respect the identified set.

**Overlap:** observationally equivalent latent states and set-valued conclusions.

**Difference:** Paper B uses a finite operational quotient tied to a declared experiment, future actions, and ecological target. Its central minimality result removes observable distinctions irrelevant to the target while retaining distinctions required for future intervention reports. The paper must cite partial-identification theory explicitly and must not claim that honest set-valued reporting itself is new.

### 3. Latent-class identifiability and observational equivalence

Latent-class and diagnostic-test theory characterize when experimental designs identify latent types or parameters.

**Overlap:** design-dependent indistinguishability and partial identifiability.

**Difference:** Paper B's object is not merely parameter identifiability. It connects record equivalence to target-safe action-stable abstraction, failure architecture, and stopping decisions under a wrong-resolution budget.

### 4. Bisimulation, state abstraction, and sufficient representations

Bisimulation and quotient methods construct coarsest behavior-preserving state abstractions. MDP representation learning and state aggregation similarly preserve rewards or value functions relevant to a task.

**Overlap:** coarsest quotient, successor stability, target relevance.

**Difference:** Paper B starts from finite experiment records and candidate latent worlds. The quotient is both experiment-relative and target-relative, with an exact set-valued fallback when deterministic reporting is unsupported. The theorem should be sold as a target-safe evidence quotient, not a new generic minimization algorithm.

### 5. Bayesian and optimal experimental design

Bayesian experimental design, value of information, active learning, adaptive sensing, and sequential decision theory choose informative experiments. Ecological adaptive monitoring applies related principles to management and survey design.

**Overlap:** conditional experiment choice, costs, information gain, stopping.

**Difference:** the objective in Paper B is not full identification or generic information gain. Policies are assessed by correct, wrong, and ambiguous target-report probabilities, and may stop with an honest set-valued report. A least-cost policy is sought only within a declared finite family and explicit risk contract.

### 6. Reliability, common-cause failure, and sensor diversity

Reliability engineering and dependent-failure models show that repeated units sharing one failure cause do not provide independent redundancy.

**Overlap:** common-cause ceilings and heterogeneous failure factors.

**Difference:** Paper B maps failure architecture directly to which experiment-induced quotient splits are trustworthy for an ecological target. The probability inequalities are supporting calculations, not the main novelty.

## Defensible novelty statement

Use this wording consistently:

> Occupancy analysis, partial identification, state abstraction, and adaptive design each address part of the ecological evidence problem. We connect them through a finite target-relative object. A declared experiment partitions latent ecological worlds by complete records; deterministic reporting is valid exactly when the management target is constant on the compatible class, otherwise the exact report is set-valued. We then characterize the unique coarsest observation-preserving and action-stable quotient retaining every distinction required for present and future target reports. Finally, the declared failure architecture determines which intended refinements are reliable, and adaptive policies are compared under explicit correct-, wrong-, ambiguity-, and cost constraints.

Avoid claiming novelty for occupancy correction, observational equivalence, identified sets, concentration bounds, posterior updating, or brute-force finite policy search.

## The most vulnerable claims

1. **The experiment-induced quotient is elementary.** Present it as the organizing object, not the main mathematical breakthrough.
2. **Set-valued reporting has deep prior art.** Cite partial identification and imprecise/robust inference; novelty is the ecological operational integration.
3. **The target-safe quotient resembles task-specific bisimulation.** The theorem must visibly require observation preservation, target reports under declared future actions, successor stability, coarseness, and uniqueness.
4. **Adaptive design may look like finite enumeration.** The contribution is the target-safe risk objective and stopping semantics, not computational novelty.
5. **Failure architecture may look like reliability engineering relabelled.** The paper must show that different failure structures change the ecological reportability partition, not just detection probability.
6. **A toy example will not support a top methods journal.** The joint presence × response-type example needs numerical replay and at least one realistic design scenario.

## Required literature groups

- single- and multi-method occupancy with imperfect detection;
- partial identification, identified sets, and set-valued decisions;
- latent-class identifiability and diagnostic-test design;
- bisimulation/state aggregation/task-relevant representations;
- Bayesian experimental design, value of information, and adaptive monitoring;
- common-cause and dependent-failure reliability;
- ecological structural uncertainty and intervention prediction.

Representative anchors include MacKenzie et al. (2002); Manski (2003); Imbens & Manski (2004); Tamer (2010); Chaloner & Verdinelli (1995); classical and modern bisimulation/state-aggregation work; and ecological sampling-design literature separating state and observation processes.

## Journal ranking

### First choice after validation: Methods in Ecology and Evolution

**Fit:** MEE explicitly publishes new analytical, conceptual, computational, and practical methods and prioritizes uptake. Paper B is closer to a reusable ecological method than Paper A because it directly addresses monitoring, imperfect detection, management reporting, and adaptive design.

**Submission condition:** add a user-facing workflow, software/API documentation, simulation benchmarking against at least occupancy-only, information-gain-only, and full-identification policies, plus one realistic ecological case or calibrated scenario. MEE's emphasis is method dissemination and uptake, so theorem-only presentation is insufficient.

### Current-form first choice: Ecological Modelling

**Fit:** strong. The paper supplies a mathematical systems framework for ecological evidence and management experiments, with reproducible finite analyses and direct implications for environmental decision-making.

**Submission condition:** develop the plant-pollinator example quantitatively and state design recommendations rather than only theorem boundaries.

### Strong theoretical alternative: Bulletin of Mathematical Biology

**Fit:** appropriate for the integrated quotient/minimality/failure/adaptive-policy theorem package at the biology-mathematics interface.

**Risk:** editors may expect deeper mathematical development than the current finite exact framework, while ecological-method users may be less central.

### Ambitious alternative: PLOS Computational Biology, Methods

**Fit:** possible only after substantial software and real-data validation. The journal requires exceptional importance, broad adoption potential, reproducibility, and concrete biological insight; methods papers are expected to show a major advance rather than an elegant finite framework alone.

**Current verdict:** not ready. The method would need a polished open-source tool, benchmarks, and real ecological applications demonstrating conclusions that standard workflows miss.

### Secondary option: Theoretical Ecology

**Fit:** good if the paper is reframed around the ecological consequences of underdetermined mechanisms and failure-dependent monitoring, rather than method uptake.

**Risk:** the adaptive-design and reliability components may make the paper feel more methodological than ecological-theoretical unless the example carries the narrative.

## Final recommendation

Use a two-stage target decision:

1. **If the next revision adds software, comparative simulations, and a realistic application:** submit to **Methods in Ecology and Evolution**.
2. **If the manuscript remains primarily finite theory with one worked example:** submit first to **Ecological Modelling**, with **Bulletin of Mathematical Biology** as the theoretical transfer option.

Do not submit to PLOS Computational Biology in the present form.

## Revision gate before journal selection

- add an explicit related-work section covering all six boundaries;
- implement a complete reproducible workflow from latent-world declaration to recommended next experiment;
- benchmark against presence-only occupancy reporting, full-world identification, and expected-information-gain design;
- show a common-cause failure case where nominal replication increases but target reportability does not;
- include correct, wrong, ambiguous, and expected-cost curves across policies;
- add one realistic or real-data ecological case;
- ensure the abstract states one practical decision delivered by the method;
- prepare two cover-letter versions: uptake-oriented for MEE and systems-modeling-oriented for Ecological Modelling.
