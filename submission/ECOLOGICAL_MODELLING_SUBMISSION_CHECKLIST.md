# Ecological Modelling submission checklist — standalone CED

Status: **journal-facing production checklist; scientific core unchanged**.  
Target: **Ecological Modelling — Original Research / Research Paper route**.  
Live scope rechecked: **2026-09-11**.

## 1. Scope fit confirmed from current journal information

Current journal information states that *Ecological Modelling* publishes new mathematical models and systems analysis for ecological processes, welcomes mathematical and conceptual modelling, computer simulation and ecological theory, and currently publishes original research articles as well as reviews, viewpoints and short communications.

CED should therefore be framed as a **finite ecological evidence/reportability model**, not as a generic statistics or machine-learning paper.

### CED model contribution to foreground

- experiment-induced compatible-world quotient;
- target-safe quotient and exact compatible target reports;
- failure-aware observation architecture;
- false-resolution / ambiguity / cost contract;
- finite adaptive reporting and stopping;
- exact finite benchmark showing that full latent-world information and target resolution can rank the same candidate observations differently.

### Fit risk to manage explicitly

The paper models the **evidence/reporting system around ecological states and futures**, rather than one named population or ecosystem process. The Introduction and Discussion must therefore keep ecological targets, monitoring architectures and environmental-management use cases visible. Do not let the paper read as a generic information-theory note with ecology names inserted afterwards.

## 2. Canonical manuscript surface

- [x] Standalone scientific source: `manuscript/paper_b_main.tex`.
- [x] Supplement: `manuscript/paper_b_supplement.tex`.
- [x] Current publication route: `manuscript/PUBLICATION_ROUTE_2026-09-11.md`.
- [x] Current standalone status: `manuscript/CED_SUBMISSION_STATUS_2026-09-11.json`.
- [x] Integrated `EVIDENCE_*` files are synthesis/provenance artifacts, not the submission unit.
- [ ] Replace residual journal-specific MEE wording in active standalone metadata/front matter, if any, without changing scientific claims.
- [ ] Verify the final article-type label against the live Elsevier submission system immediately before upload.

## 3. Title and abstract

Current working title:

> **When full-world information misses the ecological target: Failure-diverse evidence for distinguishable futures**

- [x] Title names the target-level problem rather than Boundary/MROD integration.
- [x] Abstract already leads with target relevance and shared failure architecture.
- [ ] Final abstract length/format check against the live *Ecological Modelling* Guide for Authors at upload time.
- [ ] Ensure the abstract states the ecological modelling object, exact finite validation and main consequence without claiming universal optimality.

## 4. Highlights

Elsevier's current general author guidance describes Highlights as **3–5 short bullets**, normally **85 characters or fewer including spaces**. A standalone editable highlights file is prepared at `submission/ECOLOGICAL_MODELLING_HIGHLIGHTS.md`.

- [ ] Recheck whether Highlights remain mandatory for *Ecological Modelling* in the live journal Guide before upload.
- [ ] If mandatory, upload the editable highlights file separately.

## 5. Graphical abstract

Elsevier's current graphical-abstract guidance states that journal-specific requirements control whether one is required. If used, it should be submitted separately and visually summarize the article.

Potential CED graphical abstract:

```text
realized record
      -> compatible worlds
      -> target-safe distinctions
      -> failure contract
      -> singleton report / set-valued report / measure again
```

- [ ] Check the live *Ecological Modelling* Guide for whether a graphical abstract is required, optional or unsupported.
- [ ] If used, build it from deterministic scientific geometry rather than generative-AI imagery.

## 6. Ecological modelling content gate

Before submission the main text must make the following explicit:

- [x] what constitutes a latent ecological world;
- [x] what constitutes a realized ecological record;
- [x] what target/future is being reported;
- [x] why full state identification can be unnecessary for a declared ecological target;
- [x] how shared weather/access/sensor/observer failure changes evidence;
- [x] how ambiguity is retained when evidence does not license a singleton;
- [ ] ensure at least one worked ecological example is visually or narratively prominent enough that a modelling editor can see the ecological use case immediately;
- [ ] state clearly that finite enumeration is validation of the model logic, not natural-system empirical validation.

## 7. Figures and equations

- [x] Core quotient and failure-contract mathematics are explicit.
- [x] Benchmark and sensitivity outputs are reproducible.
- [ ] Verify every model object/state variable/action/failure factor is defined before use.
- [ ] Add or retain one conceptual model diagram early in the paper.
- [ ] Final journal-size visual inspection of all figure labels.
- [ ] Confirm equation numbering and supplement cross-references after final build.

## 8. Code, data and reproducibility

Current Elsevier guidance encourages sharing research data and code and supports explicit data-availability statements.

CED is primarily exact finite theory/simulation and requires no external empirical dataset for its headline results.

- [x] Code and tests reproduce the finite results.
- [x] Reproducibility workflow exists and passes.
- [x] Scientific source is repository-pinned.
- [ ] Prepare final Data/Code Availability Statement for Elsevier submission.
- [ ] Decide double-anonymous versus identified public-code timing from the live journal review policy.
- [ ] If a DOI/archive is required or strategically desirable, mint only after the final submission snapshot is fixed.

## 9. AI disclosure

Elsevier's current policy requires reproducible disclosure when AI tools form part of the research design or research methods, and separately governs AI-assisted writing and image generation.

- [ ] Recheck the live Elsevier generative-AI policy immediately before submission.
- [ ] Confirm manuscript-preparation disclosure wording with all authors.
- [ ] Do not use general-purpose generative-AI image tools for a graphical abstract.

## 10. Declarations / human metadata

- [ ] Author list and affiliations.
- [ ] Corresponding-author email and postal address.
- [ ] CRediT contribution statement.
- [ ] Funding statement.
- [ ] Acknowledgements.
- [ ] Declaration of competing interests.
- [ ] Data/code availability statement.
- [ ] Any ethics/inclusion statement required by the live journal workflow.

## 11. Reference and novelty firewall

CED may cite Boundary, MROD and the C2 synthesis where relevant, but must not absorb their novelty.

- Boundary owns structural identification geometry such as `k-rank(M)`.
- MROD owns mechanism-learning next-observation design and frozen G2 validation.
- C2 owns only the cross-programme four-failure synthesis.
- CED owns target-safe reportability, failure-aware evidence and risk-limited reporting/stopping.

- [ ] Final reference-scope audit after all retargeting edits.
- [ ] Final long-text overlap audit against archived integrated Evidence draft.

## 12. Final upload gate

Do not submit until:

1. live *Ecological Modelling* Guide for Authors is rechecked;
2. journal-specific article type, abstract, keyword, Highlights and graphical-abstract rules are confirmed;
3. all author metadata/declarations are complete;
4. final manuscript/SI/figures compile cleanly;
5. reproducibility tests remain green;
6. no Boundary/MROD/C2 novelty has leaked into the standalone CED claim surface.

## Current decision

**No new scientific analysis is required merely to retarget CED from the abandoned integrated Evidence manuscript to Ecological Modelling.** The next work is journal-facing packaging and ecological framing, with the scientific core frozen unless a genuine scope or reviewer problem is discovered.
