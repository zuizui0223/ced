# Methods in Ecology and Evolution submission package

## Purpose

This document is the journal-specific submission gate for Paper B. It records the current *Methods in Ecology and Evolution* (MEE) requirements that affect the repository and separates machine-checkable readiness from author decisions that must not be guessed.

Official sources checked 2026-08-12:

- Author Guidelines: https://besjournals.onlinelibrary.wiley.com/hub/journal/2041210x/author-guidelines
- Policy on Publishing Code: https://besjournals.onlinelibrary.wiley.com/hub/journal/2041210x/policyonpublishingcode.html
- MEE LLM/code editorial: https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.14325

## Article type

**Planned article type:** Standard Research Article.

The manuscript is a new ecological analytical/conceptual method supported by exact finite mathematics, executable software, simulation/benchmark comparison, sensitivity analyses, and a formal Supplement. It is not being positioned as a taxon-specific application or as an Application paper centered mainly on software uptake.

## Machine-checkable initial-submission requirements

- [x] Double-anonymous main manuscript: author identity replaced by an anonymous placeholder.
- [x] Abstract organized as four numbered items.
- [x] Data/Code for peer review statement included before Keywords.
- [x] 5--8 Keywords supplied.
- [x] Main top-level structure is Introduction / Materials and Methods / Results / Discussion.
- [x] Four headline Paper B Results remain visible inside Results.
- [x] Code and deterministic artifacts can be bundled as an anonymized review archive.
- [x] Simulation/benchmark testing is a primary validation component.
- [x] Python 3.10--3.12 test matrix and deterministic replay are CI-tested.
- [x] Main and Supplement PDFs are built by CI.
- [x] Novelty is positioned as the finite ecological reportability interface rather than target-oriented OED, prediction sets, occupancy, or partition refinement in isolation.

Run:

```bash
python scripts/check_mee_submission.py
```

for the current machine-readable status.

## Human decisions / blocking submission items

### 1. Open-source software license — REQUIRED, unresolved

MEE states that submitted code must include a fully open-source software license. The repository currently has no `LICENSE` file and no project license metadata.

**Do not choose a license automatically.** The author(s) must select an appropriate license after considering ownership, institutional rules, collaborator expectations, and desired reuse conditions. Once chosen, add the license text and project metadata before submission.

### 2. Separate title page — REQUIRED, unresolved author metadata

Prepare a separate title-page file containing the final:

- manuscript title;
- author full names;
- institutions and addresses;
- corresponding author;
- acknowledgements;
- author-contribution statement;
- data-availability statement / data sources where appropriate;
- conflict-of-interest statement as required by the submission system.

The review manuscript should remain anonymous. Do not populate final author metadata from guesses.

### 3. LLM / AI disclosure — REQUIRED TO CONFIRM WITH AUTHORS

MEE requires a clear Methods statement when LLMs/comparable AI tools were used, including the application name/version and use. MEE also requires a corresponding or senior author to take responsibility for generated code/text, and LLM-generated code should be annotated.

A factual **draft for author confirmation** is:

> OpenAI ChatGPT (GPT-5.6 Sol) was used during code review, debugging, and manuscript drafting/editing. All mathematical claims, numerical outputs, tests, and submitted source were independently checked through deterministic code execution and CI. The responsible author(s) reviewed and take responsibility for the submitted text and code.

Before submission, the authors must:

1. confirm that this accurately describes the extent of use;
2. identify the responsible corresponding/senior author in the final Author Contributions statement;
3. determine which code portions, if any, require explicit LLM-generation annotations under MEE policy;
4. ensure all coauthors approve the disclosure and submitted material.

The current anonymous manuscript deliberately does **not** assert author approval or responsibility that has not yet been confirmed.

### 4. Final word count — check after generated submission source is frozen

MEE Standard Research Articles should remain within the journal's stated 7,000--8,000-word maximum range, including references, captions, and statements. The automated checker reports a conservative rough LaTeX-source estimate; perform the journal/submission-system count on the frozen PDF/source before upload.

## Data / code review archive

For initial double-anonymous review, create a clean archive from the submission commit rather than pointing reviewers at the identifying public GitHub URL.

The archive should include at minimum:

- `ced/` source package;
- deterministic benchmark and analysis scripts;
- tests;
- `pyproject.toml`;
- environment / installation instructions;
- generated JSON/CSV/TikZ artifacts needed to verify manuscript numbers;
- a short anonymous README with exact reproduce commands;
- the selected open-source license once the author decision is made.

Before upload, scan the archive for author names, email addresses, GitHub usernames, absolute local paths, image metadata, and README links that reveal identity.

## Final editorial checks

- [ ] resolve remaining overfull-box warnings in the generated manuscript if they persist after MEE formatting;
- [x] replace the Supplement's legacy binomial notation with `\binom`;
- [ ] verify all DOI, journal, volume, page/article metadata one final time;
- [ ] verify abstract word count and 1--4 numbering in the final generated PDF;
- [ ] verify Keywords remain no more than eight short terms/phrases;
- [ ] ensure the final title/abstract/cover letter use **finite reportability** as the contribution and do not claim novelty for target-oriented design itself.

## Frozen journal-facing novelty statement

> Paper B provides a finite ecological reportability interface: a realized record induces compatible latent worlds and a sharp target set; a unique coarsest action-stable quotient retains exactly the distinctions needed for the declared future; observation-failure architecture determines whether those distinctions can be trusted; and an explicit false-resolution contract governs adaptive stopping and singleton reporting.
