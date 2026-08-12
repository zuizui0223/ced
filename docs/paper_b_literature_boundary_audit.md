# Paper B primary-literature boundary audit

## Purpose

This is the submission-facing nearest-neighbour audit for Paper B. It records what adjacent literatures already establish, what the manuscript must not claim as new, and the narrower object added by the current four-result framework.

The guiding rule is conservative:

> When an adjacent literature can already express a Paper B idea in a broader formalism, concede that fact explicitly. Novelty must be attached to the combined finite reportability contract, not to familiar ingredients in isolation.

## 1. Occupancy and imperfect detection

### Primary neighbours

- MacKenzie et al. (2002), *Ecology*, “Estimating site occupancy rates when detection probabilities are less than one.” DOI: `10.1890/0012-9658(2002)083[2248:ESORWD]2.0.CO;2`.
- Royle & Link (2006), *Ecology*, “Generalized site occupancy models allowing for false positive and false negative errors.” DOI: `10.1890/0012-9658(2006)87[835:GSOMAF]2.0.CO;2`.

### Already established

Occupancy models explicitly separate latent occurrence from an observation process, and nondetection is not treated as absence when detection probability is below one. Extensions already accommodate both false-negative and false-positive observation errors.

### Do not claim

- that Paper B invents imperfect-detection modelling;
- that ecology lacks methods for separating presence from observation error;
- that false positives are absent from the occupancy literature.

### Paper B addition

Occupancy or related latent-state models may supply posterior mass over worlds. Paper B asks a downstream question: whether the remaining worlds imply one target value or several, which latent distinctions must remain separate under future interventions, and whether the declared observation architecture can support a deterministic target report at the stated risk level.

## 2. Partial identification and set-valued inference

### Primary neighbour

- Manski (2003), *Partial Identification of Probability Distributions*, Springer. DOI: `10.1007/b97478`.

### Already established

When data and maintained assumptions do not point-identify a quantity, a set of feasible values can be the appropriate inferential object. Sharp identified sets are not a Paper B invention.

### Do not claim

- that set-valued reporting is novel in statistics/econometrics;
- that forcing a point estimate under underidentification is a previously unrecognized general problem.

### Paper B addition

The compatible target set is attached to a declared finite ecological experiment, a target-relative action-stable quotient, observation-failure contracts, and an adaptive rule for deciding whether to stop with that set or collect another target-relevant observation.

## 3. Risk-controlled prediction sets and abstention

### Primary neighbour

- Bates, Angelopoulos, Lei, Malik & Jordan (2021), *Journal of the ACM*, “Distribution-Free, Risk-Controlling Prediction Sets.” DOI: `10.1145/3478535`.

### Already established

Set-valued predictive output can be paired with a user-specified risk criterion and finite-sample guarantees. Therefore neither “return a prediction set” nor “attach an explicit risk bound to a set-valued prediction” is a Paper B novelty in isolation. Selective-prediction and conformal-prediction literatures also make abstention/coverage trade-offs explicit.

### Do not claim

- that Paper B is the first framework to output sets rather than points;
- that user-specified finite-sample risk control for prediction sets is new;
- that abstention itself creates the paper's novelty.

### Paper B addition

Paper B's exact target set is the image of the ecological worlds compatible with a declared record, not a generic predictive set calibrated only through a marginal coverage/risk objective. The framework then asks which latent distinctions must remain separate under declared future actions and whether observation-failure architecture supports the required refinement. Posterior false-resolution control is a second, explicitly distinguished layer built on top of that compatible-world object.

## 4. Structural uncertainty, multimodel inference, and ecological prediction

### Primary neighbours

- Dormann et al. (2018), *Ecological Monographs*, “Model averaging in ecology: a review of Bayesian, information-theoretic, and tactical approaches for predictive inference.” DOI: `10.1002/ecm.1309`.
- Dietze (2017), *Ecological Applications*, “Prediction in ecology: a first-principles framework.” DOI: `10.1002/eap.1589`.
- Dietze et al. (2018), *PNAS*, “Iterative near-term ecological forecasting: Needs, opportunities, and challenges.” DOI: `10.1073/pnas.1710231115`.

### Already established

Ecologists already recognize structural/model uncertainty, predictive uncertainty, model averaging, iterative forecasting, and the need to connect models to future trajectories and decisions.

### Do not claim

- that Paper B introduces ecological prediction as a scientific objective;
- that multimodel approaches cannot retain structural uncertainty;
- that ecological forecasts ordinarily assume one mechanism is certainly true.

### Paper B addition

Paper B does not average candidate futures into one forecast by default. For a declared finite support it asks whether model distinctions are *necessary for the target*: worlds may be collapsed when their target reports and declared future successors agree, while subtle distinctions must remain when they imply different futures. The output may remain a target set rather than a single averaged target.

## 5. Bayesian experimental design

### Primary neighbour

- Chaloner & Verdinelli (1995), *Statistical Science*, “Bayesian experimental design: A review.” DOI: `10.1214/ss/1177009939`.

### Already established

Bayesian experimental design is decision-theoretic. An experiment can be optimized for a declared utility or loss, so targeted design is not unique to Paper B.

### Do not claim

- that information gain is the only Bayesian design objective;
- that Bayesian design cannot prioritize a specific prediction or decision;
- that Paper B lies outside decision theory.

### Paper B addition

The framework makes a specific reportability contract primitive: a declared target, an admissible false-resolution rate, explicit abstention/set-valued output, observation failure structure, and experiment cost. These objects can be embedded in a broader loss formulation, but Paper B gives them an auditable finite quotient interpretation without requiring a cardinal utility over all management outcomes.

## 6. Targeted and goal-oriented optimal experimental design

### Primary neighbours

- Vanlier, Tiemann, Hilbers & van Riel (2012), *Bioinformatics*, “A Bayesian approach to targeted experiment design.” DOI: `10.1093/bioinformatics/bts092`.
- Attia, Alexanderian & Saibaba (2018), *Inverse Problems*, “Goal-oriented optimal design of experiments for large-scale Bayesian linear inverse problems.” DOI: `10.1088/1361-6420/aad210`.
- Zhong, Shen, Catanach & Huan (2026), *SIAM/ASA Journal on Uncertainty Quantification*, “Goal-Oriented Bayesian Optimal Experimental Design for Nonlinear Models Using Markov Chain Monte Carlo.” DOI: `10.1137/24M1649344`.

### Already established

Targeting the downstream prediction or quantity of interest rather than the full parameter/state is established experimental-design methodology. Vanlier et al. explicitly target reduction of uncertainty in a selected prediction of interest. Attia et al. seek designs that reduce posterior uncertainty in the experiment end-goal or quantity of interest. Zhong et al. extend predictive goal-oriented OED to nonlinear models by maximizing expected information gain on predictive quantities of interest rather than on model parameters.

### Do not claim

- that Paper B is the first method to choose experiments for a prediction rather than the full latent state;
- that the observation “high parameter/state EIG need not imply high prediction/QoI EIG” is novel;
- that avoiding target-irrelevant data collection is unique to Paper B;
- that the 16-world full-state-EIG counterexample establishes novelty over targeted or goal-oriented OED.

### Paper B addition

Paper B addresses a different finite interface around targeted prediction. It starts with the equivalence/compatible-world structure induced by the declared ecological record, returns a sharp set-valued target when deterministic reporting is unsupported, computes the coarsest action-stable target-preserving quotient, and asks whether observation failure permits the required quotient refinement to be trusted under an explicit false-resolution contract. Targeted/goal-oriented OED and Paper B may select the same experiment; the additional Paper B object is the reportability-and-abstraction contract, not target orientation itself.

## 7. Ecological value of information

### Primary neighbour

- Canessa et al. (2015), *Methods in Ecology and Evolution*, “When do we need more data? A primer on calculating the value of information for applied ecologists.” DOI: `10.1111/2041-210X.12423`.

### Already established

Ecological VOI evaluates whether additional information is worthwhile through its expected improvement in management outcomes.

### Do not claim

- that VOI rewards information irrespective of management relevance;
- that Paper B universally outperforms VOI;
- that management utility is intrinsically inferior to a reportability contract.

### Paper B addition

The benchmark contrasts target-safe design specifically with *full-world entropy reduction*, not with an optimally specified management-VOI or goal-oriented OED objective. Target-safe reporting is most distinct when investigators can defend the target and an error contract but cannot or do not wish to assign a cardinal utility to every ecological/management consequence.

## 8. Monitoring, adaptive monitoring, and adaptive management

### Primary neighbours

- Nichols & Williams (2006), *Trends in Ecology & Evolution*, “Monitoring for conservation.” DOI: `10.1016/j.tree.2006.08.007`.
- Lindenmayer & Likens (2009), *Trends in Ecology & Evolution*, “Adaptive monitoring: a new paradigm for long-term research and monitoring.” DOI: `10.1016/j.tree.2009.03.005`.
- Williams (2011), *Journal of Environmental Management*, “Adaptive management of natural resources—framework and issues.” DOI: `10.1016/j.jenvman.2010.10.041`.

### Already established

Monitoring should be linked to scientific or management objectives rather than treated as undirected surveillance, and adaptive management uses learning and management iteratively under uncertainty.

### Do not claim

- that question-driven monitoring is new;
- that adaptive monitoring has not considered changing information needs;
- that Paper B invents iterative learning-management cycles.

### Paper B addition

Paper B supplies an exact finite object for one particular design question: the quotient of latent worlds produced by the experiment, the coarsest quotient still sufficient for the declared future, the failure-aware reliability of the necessary split, and a terminal correct/wrong/ambiguous report contract.

## 9. State abstraction, bisimulation, and model minimization

### Primary neighbour

- Givan, Dean & Greig (2003), *Artificial Intelligence*, “Equivalence notions and model minimization in Markov decision processes.” DOI: `10.1016/S0004-3702(02)00376-4`.

### Already established

State aggregation, behavioural equivalence/bisimulation, partition refinement, and reduced models that preserve relevant control properties are established mathematical ideas.

### Do not claim

- that equivalence classes, partition refinement, fixed-point minimization, or behavioural state reduction are new mathematical inventions;
- that the existence of a minimal action-stable partition alone establishes ecological novelty.

### Paper B addition

The target-safe quotient is an experiment- and target-relative ecological interface: it begins with the partition induced by a declared finite observation record, preserves a declared target under future actions, admits sharp set-valued fallback when that target is unresolved, and is coupled to observation-failure and false-resolution contracts.

## 10. Nearest-neighbour claim map

| Paper B claim | Nearest established literature | Safe novelty wording |
|---|---|---|
| nondetection does not certify absence | occupancy / imperfect detection | use as premise, not novelty |
| compatible uncertainty may be set-valued | partial identification | target set tied to experiment/action quotient |
| set-valued output with user-specified risk | risk-controlling prediction sets | not novelty; Paper B set is induced by compatible ecological worlds and future actions |
| several mechanisms can imply different predictions | structural uncertainty / forecasting | characterize which distinctions are target-necessary |
| choose informative experiments | Bayesian design | explicit finite reportability/risk contract |
| choose experiments for prediction/QoI rather than full state | targeted / goal-oriented OED | not novelty; add compatible-world quotient, action stability, failure contract |
| collect data for management value | ecological VOI | do not use VOI as entropy straw man |
| monitoring should answer declared questions | adaptive monitoring/management | exact target-compatible stopping/refinement object |
| minimize state descriptions | bisimulation/model minimization | experiment-induced + target-relative + failure-aware ecological quotient |
| information gain can select irrelevant latent detail | goal-oriented OED already recognizes analogous parameter-vs-QoI issue | benchmark is only a counterexample to full-world EIG, not a novelty proof |

## 11. Manuscript language gate

The manuscript should explicitly or implicitly respect the following concessions:

1. occupancy models already handle imperfect detection, including false positives;
2. partial identification already legitimizes set-valued conclusions;
3. risk-controlling prediction sets already combine set-valued prediction with user-specified finite-sample risk control;
4. model averaging and forecasting already address structural/predictive uncertainty;
5. Bayesian design and VOI can be target/decision specific;
6. targeted/goal-oriented OED already selects experiments for predictions or quantities of interest rather than full parameter/state uncertainty;
7. adaptive monitoring is already question driven;
8. bisimulation/model minimization already provides state-partition machinery.

The paper's contribution should then be stated positively:

> Paper B links a finite experiment-induced compatible-world structure to a sharp ecological target set, computes the coarsest action-stable target-preserving refinement, checks whether observation failure permits that refinement to be trusted, and evaluates adaptive stopping/experiment choices under an explicit false-resolution contract.

## 12. Remaining literature checks before submission

- verify final journal-specific citation style and exact page/volume metadata;
- add Bates et al. (2021) to the submission bibliography if the final manuscript retains a novelty-adjacent claim about risk-controlled set-valued reporting;
- consider one focused reference on false-positive occupancy if Royle & Link (2006) is insufficient for the chosen ecological example;
- consider one primary source on robust decision making only if Discussion expands beyond reportability into management choice;
- monitor fast-moving goal-oriented/decision-focused OED literature only for claims that overlap the finite reportability interface;
- avoid expanding the bibliography simply for breadth: each added source must bound one manuscript claim.
