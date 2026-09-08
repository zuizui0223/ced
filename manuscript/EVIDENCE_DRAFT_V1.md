# Evidence for ecological distinctions: identification boundaries, measurement choice and honest reporting

Status: **integrated Evidence-paper draft v1** under the two-paper submission architecture.

Source repositories: `zuizui0223/boundary`, `zuizui0223/mrod`, `zuizui0223/ced`.

The source repositories remain the authoritative provenance and reproducibility homes for their theorem witnesses, frozen results, software and source-specific analyses. This manuscript is the submission-facing integration layer.

## Abstract

Ecological monitoring often asks three questions as though they were one: what the current data identify, what should be measured next, and when the resulting evidence is sufficient to support a scientific report. We separate these questions within a common compatible-world framework. First, the current observation map induces an identification boundary: latent worlds that generate the same retained record remain observationally equivalent, and greater precision along an existing observation direction need not reduce that structural ambiguity. Second, the distinctions worth resolving depend on the scientific objective. Mechanism-learning value asks how much a candidate observation is expected to reduce residual mechanism uncertainty, whereas target-licensing value asks whether the observation resolves the distinctions required for a declared target under an explicit reliability, error and cost contract. These utilities need not agree. Third, a nominally discriminating measurement is evidentially useful only when its failure architecture supports the claimed split.

We combine exact identification results, finite reportability theory and controlled observation-design benchmarks. In positive log-linear systems with observation matrix \(M\), the structural unidentified dimension is \(k-\mathrm{rank}(M)\), and a new scalar observation reduces it only if its row adds a new direction outside the current row span. A finite experiment induces an exact compatible-world quotient; deterministic target reporting is justified only when the target is constant over the compatible class, while a target-safe refinement retains only distinctions that can change the declared future report. In the frozen MROD benchmark, information-guided observation selection resolved all initial confounding edges at budget two versus 0.6045 under random ordering and converged in 0.990 versus 0.435 of systems while using fewer observations. We then introduce an eight-world integration witness in which a target-irrelevant four-level measurement provides 2 bits of full mechanism information but never licenses the binary target, whereas a target-splitting observation provides only 1 bit of mechanism information and licenses the target with probability one. Mechanism-learning and target-licensing values therefore rank the same equal-cost candidates differently.

Evidence quality also depends on reliability architecture. Repetition inside one shared failure domain is not equivalent to independent failure diversity, and unsupported terminal records must remain ambiguous rather than being forced into singleton reports. We therefore formulate evidence-directed monitoring as an objective-relative loop: declare the current boundary, declare whether the immediate objective is mechanism learning or target licensing, credit only observation directions supported by the failure contract, select before the outcome is revealed, update compatible worlds, and stop at target resolution, information limits, budget limits or explicit risk boundaries. The framework does not claim a universal observation utility, universal optimality over undeclared experiment vocabularies, or natural causal identification without a declared model world.

## 1. Introduction

### 1.1 More data, more information and more evidence are different claims

Ecological monitoring is often improved by collecting more observations, but “more” can refer to several different quantities. Repeated measurements can increase precision without resolving a structural mechanism ambiguity. An experiment can provide substantial information about latent biological detail while leaving the prediction of interest unchanged. Conversely, a modest measurement can be decisive if it separates the worlds that imply different target values. Even a nominally discriminating measurement may be unreliable when repeated observations share a common failure mode.

These distinctions matter whenever a monitoring programme moves from description toward explanation, intervention or prediction. A current record may fit several mechanisms. A manager may need only one future-facing target rather than a complete mechanistic reconstruction. An experiment may appear to distinguish two worlds under an idealized record model but fail to support that distinction under realistic detection or access failures. A principled evidence design must therefore keep separate the structural boundary of the current record, the scientific utility assigned to candidate measurements, and the reliability contract that licenses a report.

We call this the Evidence problem: given the compatible worlds surviving observation, what can be identified now, which unresolved distinctions matter, what should be measured next, and when does the evidence justify a deterministic report?

### 1.2 Evidence begins where Observation ends

A companion Observation paper treats how scientific records gain, lose and collapse distinctions through retained augmentation, row-entry selection and semantic coarsening. Evidence starts after those operations have produced a retained record and its compatible-world set. It does not re-claim observation refinement, support deletion or semantic coarsening as novelty.

Let \(W\) be the declared finite or finitely represented world set, and let the current record induce compatible class \(C\subseteq W\). Evidence asks what scientific distinctions remain variable over \(C\), how candidate measurements partition \(C\), and which resulting reports are warranted.

### 1.3 Current identification is a property of the observation map

The Boundary line of work separates structural identification from statistical precision. In a positive log-linear observation system, the rows of an observation matrix \(M\) encode the independent directions through which latent mechanism coordinates affect the observations. Conditional on compatibility, the residual structural dimension is

\[
 k-\operatorname{rank}(M).
\]

A new scalar measurement changes structural rank only when its row lies outside the span of existing observation rows. Replication, rescaling or greater precision along an existing row can be valuable statistically without adding a new identification direction.

This is the correct starting point for evidence design: before asking which measurement is optimal, declare what the current map has failed to distinguish.

### 1.4 Full mechanism identification is not the only scientific objective

The MROD line of work asks how a candidate observation reduces residual mechanism ambiguity. Given an admissible mechanism region and candidate observation \(Q\), its learning value is based on conditional mechanism-observation information. This is appropriate when the scientific objective is to learn mechanism identity.

The CED line of work asks a different question. A finite experiment induces compatible-world classes, but a scientific target may be constant over several biologically distinct worlds. In that case full world identification is unnecessary. Conversely, if the current compatible class contains several target values, a deterministic target report is not justified even if other details are well identified. CED therefore defines target-safe resolution and explicit false-resolution/cost contracts for adaptive reporting.

The central integration claim of this paper is that these utilities are both valid and are not interchangeable:

\[
\boxed{\text{mechanism-learning value}\neq\text{target-licensing value}.}
\]

### 1.5 Reliability determines whether a nominal split counts as evidence

Neither mechanism information nor target resolution should be credited from an ideal record map when the observation architecture cannot reliably realize the split. Repeated reads inside a shared weather, access, sensor, observer or laboratory failure domain do not provide the same evidence as observations distributed across independent failure opportunities. CED's failure-aware results therefore sit between a desired refinement and a trustworthy report.

### 1.6 Questions and contribution

We address five questions.

1. What is the structural identification boundary under the current observation map?
2. Which unresolved distinctions are required for a declared scientific target?
3. Can mechanism-learning and target-licensing utilities rank the same candidate observations differently?
4. When does observation failure architecture invalidate an otherwise discriminating measurement?
5. How should monitoring select, update and stop under explicit learning, licensing, reliability, risk and cost contracts?

The contribution is not a universal optimal-design criterion. It is a modular evidence interface: current identification, objective-relative value, trustworthy refinement and reportability are separated so that each claim can be audited under its own assumptions.

## 2. Materials and Methods

### 2.1 Compatible worlds and the current evidence class

Let \(W\) denote a declared finite world set or a finite support approximation to a broader model. A realized record \(x\) under observation design \(D\) induces compatible class

\[
C_D(x)=\{w\in W:x\text{ is allowed under }w\text{ and }D\}.
\]

For scientific target \(T:W\to Y\), the sharp exact target report is

\[
T(C_D(x))=\{T(w):w\in C_D(x)\}.
\]

A deterministic report is exact only when this set is a singleton. Otherwise the compatible target set is the honest support-level report.

### 2.2 Boundary layer: structural identification under the current map

For a declared positive log-linear observation family with \(k\) latent mechanism coordinates and observation matrix \(M\), the structural unidentified dimension is

\[
d_{\rm unid}=k-\operatorname{rank}(M).
\]

For a new scalar candidate with observation row \(m_q\), structural dimension decreases by one exactly when

\[
m_q\notin \operatorname{rowspan}(M).
\]

This criterion distinguishes a new identification direction from greater precision along an existing direction. The result is model-family specific and does not claim that every ecological observation admits a log-linear representation.

### 2.3 Experiment-induced quotient and target-safe requirement

For deterministic complete record map \(\operatorname{record}_D\), define

\[
w\sim_Dw'\iff \operatorname{record}_D(w)=\operatorname{record}_D(w').
\]

The quotient \(W/{\sim_D}\) is the experiment-induced information partition. A target-safe refinement begins from the current evidence partition and refines only when target values differ or when declared actions send worlds to different current blocks. On a finite world set this procedure reaches a fixed point and yields the coarsest record-preserving, target-constant, action-stable refinement under the declared action grammar.

This quotient is a **resolution requirement**, not a claim that the current record has already identified the correct refined block. If a realized compatible class intersects multiple target-safe blocks, ambiguity remains.

### 2.4 Learning utility: MROD mechanism information

Let \(S\) denote residual mechanism identity over an admissible region \(A\), and let \(Q\) be a candidate observation with declared outcome model. MROD defines normalized learning value

\[
V_{\rm learn}(Q)=\frac{I(S;Q\mid A)}{K},
\]

where \(K\) normalizes by the number of declared mechanism coordinates in the implementation used by the source method. Candidate values are recomputed after each realized observation because the admissible mechanism region changes.

The sequential rule selects before outcome revelation, conditions the region on the realized outcome, recomputes candidate values, and distinguishes target resolution, budget exhaustion, prediction limits and information limits.

### 2.5 Licensing utility: target resolution under an evidence contract

CED evaluates a candidate by whether its possible records can support the distinctions required for the declared target under the observation/failure and false-resolution contracts. In the exact deterministic baseline, target licensing for an outcome occurs when the outcome-compatible target set is a singleton. Under a separately declared stochastic risk relaxation, a singleton may be reported when the corresponding decision rule satisfies the predeclared false-resolution budget; otherwise the report remains set-valued or ambiguous.

Licensing value is therefore target- and contract-relative. It is not a rescaled mechanism entropy.

### 2.6 Exact learning-versus-licensing divergence benchmark

We introduce an eight-world finite benchmark crossing binary scientific target \(T\in\{0,1\}\) with a four-level target-irrelevant mechanism attribute \(N\in\{0,1,2,3\}\). The prior is uniform over all eight worlds, and all candidate observations have equal cost.

Three deterministic candidates are compared on the same support.

1. **nuisance_detail** returns \(N\) exactly.
2. **target_split** returns \(T\) exactly.
3. **constant_probe** returns one constant outcome.

Full mechanism identity is the ordered pair \(S=(T,N)\). Because the candidates are deterministic under a uniform prior,

\[
I(S;Q)=H(Q).
\]

The nuisance candidate has four equiprobable outcomes and therefore provides 2 bits of mechanism information. The target candidate has two equiprobable outcomes and provides 1 bit. However, every nuisance outcome remains compatible with both target values, so exact target-resolution probability is zero. Every target-split outcome has a singleton target set, so exact target-resolution probability is one.

The benchmark therefore forces a strict ranking divergence on the same equal-cost candidate set.

### 2.7 Frozen MROD controlled benchmark

The source MROD G2 benchmark contains 1,000 generated systems per policy and compares information-guided observation selection with random ordering under frozen known-truth conditions. At budget two, primary outcomes include fraction of initial confounding edges resolved, system convergence, mean observations used, nuisance selections and hidden-truth false exclusion.

The benchmark is retained here as a controlled mechanism-learning stress test, not as a natural-system causal claim.

### 2.8 Failure-aware trustworthy refinement

A candidate observation can have ideal distinguishing power while failing to support the corresponding empirical split under imperfect detection or shared failure. We retain CED's failure contracts separating within-mode repeated reads, independent observation modes, overlapping factors and non-reset dependence.

For \(m\) independent modes whose operational availability is known only to be at least \(a\), within-mode repetition cannot raise the uniform worst-case guarantee above

\[
1-(1-a)^m.
\]

The statement is a guarantee ceiling under the declared lower-bound contract, not an upper bound on realized detection when true mode availability exceeds \(a\).

### 2.9 Adaptive acquisition and stopping

The integrated loop is objective-relative.

1. compute or characterize the current compatible class and structural boundary;
2. declare the immediate utility: mechanism learning, target licensing, or a separately specified combination;
3. exclude or downweight candidates whose failure architecture does not support the intended distinction;
4. score the remaining candidates under the declared utility;
5. select before outcome revelation;
6. acquire the outcome and update compatible worlds;
7. stop when the declared target is licensed, the learning objective is exhausted, budget is exhausted, or prediction/reliability limits prevent further defensible refinement.

We do not force one scalar stopping theorem to govern both objectives.

## 3. Results

### 3.1 Current observation geometry defines a structural identification boundary

Within the positive log-linear class, the residual structural dimension is exactly \(k-\operatorname{rank}(M)\). A duplicate, rescaled or more precise version of an existing observation direction leaves the rank unchanged. A scalar candidate reduces the structural dimension only if its row lies outside the current row span.

Thus “more precise evidence” and “new identifying evidence” are different claims. The Boundary result supplies a necessary first diagnostic before candidate-observation optimization.

### 3.2 Target-safe resolution can be coarser than full mechanism identification

The experiment-induced quotient gives the exact information supplied by a finite record. A deterministic target report is justified only when the target is constant across the realized compatible class. However, biological distinctions that do not change the target or declared successor reports need not be resolved.

The coarsest target-safe refinement therefore formalizes a resolution requirement that can be strictly coarser than full latent-world identity. This does not imply that the current observation has achieved that refinement; if the current compatible class crosses several required blocks, the honest report remains set-valued.

### 3.3 Mechanism-learning and target-licensing values rank the same observations differently

The new eight-world benchmark gives an exact divergence witness. The equal-cost nuisance_detail observation returns the four-level target-irrelevant attribute and provides

\[
I(S;Q_{\rm nuisance})=2\text{ bits}.
\]

It is the highest-valued candidate under full mechanism-learning information. Yet each nuisance outcome remains compatible with both scientific target values, giving exact target-resolution probability 0.

The target_split observation provides only

\[
I(S;Q_{\rm target})=1\text{ bit},
\]

but every outcome determines the target exactly, giving target-resolution probability 1. The constant probe provides 0 bits and never resolves the target.

Hence the learning ranking is

```text
nuisance_detail > target_split > constant_probe
```

whereas the licensing ranking begins

```text
target_split > nuisance_detail/constant_probe
```

with the precise tie handling depending on secondary cost/information rules. The top-ranked candidate is unambiguously different.

This result is not a critique of information theory or mechanism learning. It shows that scientific utility must be declared: an observation can be maximally informative about residual mechanism detail while irrelevant to the requested report.

### 3.4 Information-guided acquisition efficiently resolves controlled mechanism ambiguity

In the frozen MROD G2 benchmark at budget two, information-guided selection resolved 1.000 of initial confounding edges compared with 0.6045 under random order. Systems converged in 0.990 versus 0.435 of cases. Mean observations used were 1.505 versus 1.821, and nuisance selections were 0.001 versus 0.974. Hidden-truth false exclusion was zero in the frozen policy-by-budget cells.

At budget four, both information-guided and random policies eventually resolved all initial confounding edges on average, but the information-guided policy used fewer observations and almost no mechanism-independent nuisance measurements. The result supports mechanism-information-guided acquisition in the controlled declared candidate family; it does not establish universal optimality over arbitrary real measurements.

### 3.5 Reliability architecture determines whether an ideal split can be credited

The CED failure results show that nominal record diversity is not equivalent to evidential independence. With shared mode-level failure, arbitrarily many reads inside the same mode cannot eliminate the uncertainty that the mode itself was unavailable. Independent modes can strengthen the worst-case guarantee under equal raw effort because they diversify failure opportunities.

Therefore a Boundary candidate that adds a mathematically new direction does not automatically become trustworthy evidence. The direction must also be realized under a reliability architecture that supports the intended split.

### 3.6 Adaptive evidence design has distinct learning and licensing stopping states

The combined architecture yields two legitimate stopping patterns. A mechanism-learning programme can stop when no declared remaining candidate has positive estimable mechanism information or when budget/prediction limits are reached, even if a downstream target remains unresolved. A target-licensing programme can stop as soon as the target is resolved under the declared reliability and false-resolution contract, even if mechanism ambiguity remains.

These conditions are not contradictory because they answer different scientific questions. A single observation campaign can switch utilities only by explicitly changing the scientific contract; it should not silently reinterpret one objective as the other after seeing outcomes.

## 4. Discussion

### 4.1 Evidence design should start with the unresolved distinction, not the available sensor

The integrated framework reverses a common workflow. Instead of beginning with a list of sensors and asking which produces the largest statistical signal, first state which worlds remain compatible with the current record and which scientific distinction matters. Boundary characterizes the unresolved geometry. CED identifies the target-relevant portion of that geometry. MROD quantifies mechanism-learning value when mechanism identity itself is the objective.

This order prevents repeated precision from being mistaken for structural resolution and prevents target-irrelevant information from being mistaken for reportability.

### 4.2 Learning and licensing are complementary scientific utilities

The new divergence benchmark makes explicit a distinction that otherwise appears as a competition between MROD and CED. There is no conflict. If the scientific goal is mechanism discovery, the two-bit nuisance-detail measurement is genuinely more informative about the full residual mechanism identity. If the goal is the binary target report, that same measurement is useless and the one-bit target split is decisive.

The appropriate utility therefore depends on the contract. A multi-objective design can of course combine learning and licensing, but the combination must be declared rather than assumed to exist as one universal value scalar.

### 4.3 Target-safe abstraction avoids unnecessary full identification

CED's quotient results clarify why complete state reconstruction can waste evidence. If several worlds imply the same target under all declared successor actions, distinguishing them is unnecessary for that report. This can reduce observation burden and prevent the monitoring programme from optimizing details that do not change the scientific decision.

The converse is equally important: a seemingly small latent distinction cannot be discarded if it changes the target. Target-safe abstraction is therefore not generic compression but contract-relative preservation.

### 4.4 A new mathematical direction is not enough without a reliability contract

Boundary's row-span criterion identifies when a new measurement can reduce structural dimension under the declared model. CED's failure architecture adds a second requirement: the observation must be reliable enough for the split to be credited. These statements operate at different layers. One is about ideal structural geometry; the other is about evidential realization.

This distinction is especially relevant in ecological monitoring, where repeated observations can share weather, access, sensor, observer, laboratory or processing failures. Equal raw sample size does not imply equal evidence.

### 4.5 Honest ambiguity is an endpoint, not a failure to decide

A set-valued report is the correct output when the realized evidence leaves multiple target values compatible. Adaptive monitoring should not be evaluated only by how often it returns a singleton. Wrong deterministic resolution and honest ambiguity have different scientific costs. Explicit false-resolution contracts make that asymmetry visible.

### 4.6 Relationship to Observation

Observation determines which distinctions survive the sensing and recording system. Evidence governs what those surviving distinctions license and what additional measurement is warranted. An Evidence procedure cannot claim a distinction that Observation has already irreversibly removed unless genuinely independent new information is acquired.

This two-paper separation avoids treating acquisition design, selection loss, semantic representation, mechanism identification and target reportability as one monolithic notion of “accuracy.”

### 4.7 Boundaries and next empirical layer

All headline mathematical and design claims remain conditional on declared world/model, candidate-observation and reliability vocabularies. The MROD and CED benchmarks are controlled finite or synthetic systems. The new learning-versus-licensing benchmark is an exact divergence witness, not an ecological effect-size estimate. Boundary's rank result applies to the stated log-linear model family.

Prospective physical validation is therefore a separate layer. The frozen InsePi V13 experiment can test whether controlled physical interventions produce reproducible observation directions across held-out days and scenes. Natural PolliPi deployments can later test evidence-directed acquisition with real targets and nuisance processes. Neither result is silently assumed here.

## 5. Conclusion

Evidence design is not one optimization problem. The current observation map determines what is structurally unidentified; the scientific target determines which of those distinctions matter; mechanism-learning and target-licensing utilities can value the same candidate observations differently; and reliability architecture determines whether a nominal distinction can be trusted at all.

A defensible monitoring programme should therefore declare its boundary, objective and evidence contract before choosing the next measurement. Select the observation that serves the declared scientific utility, reveal the outcome only after selection, update the compatible worlds, and preserve ambiguity when the target or mechanism remains unresolved. More information can be valuable without being report-relevant, and a report can be licensed without full mechanism identification.

## Source provenance for this integration draft

- Boundary structural-identification source: `zuizui0223/boundary` current Paper A / implementation.
- MROD learning-value source: frozen G2 benchmark and submission manifest in `zuizui0223/mrod`.
- CED reportability/failure source: current Paper B theorem consolidation, manuscript and Supplement in `zuizui0223/ced`.
- Integrated divergence source: `ced/learning_licensing.py`, `tests/test_learning_licensing.py`, and `manuscript/evidence_learning_licensing_result.json`.

Final bibliography merge, quantitative figure-data integration, source-commit pinning, LaTeX migration, and cross-manuscript overlap audit remain submission-production tasks.
