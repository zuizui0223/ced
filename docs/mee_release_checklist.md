# Final MEE submission and release checklist

Use this only after the author decisions in Issue #41 are complete. The scientific content and benchmark values should remain frozen unless a genuine error is found.

## A. Author decisions

- [ ] open-source software license selected and institution/coauthors approve release;
- [ ] `LICENSE` added and `pyproject.toml` metadata matches it;
- [ ] final author names, affiliations and corresponding author confirmed;
- [ ] Author Contributions approved by all authors;
- [ ] conflict-of-interest statement confirmed;
- [ ] AI/LLM disclosure wording confirmed by all authors;
- [ ] responsible corresponding/senior author for AI-assisted code/text identified as required by journal policy;
- [ ] funding/acknowledgements confirmed.

## B. Freeze the submission commit

From a clean branch based on current `main`:

```bash
python -m pip install -e '.[dev]'
pytest
python scripts/simulate_paper_b_benchmark.py
python scripts/analyze_paper_b_reviewer_robustness.py
python scripts/analyze_paper_b_posterior_bridge.py
python scripts/render_paper_b_figures.py
python scripts/check_mee_submission.py
python scripts/build_mee_review_archive.py
```

Required outcomes:

- [ ] Python 3.10, 3.11 and 3.12 CI all green;
- [ ] `mee_submission_check.json` has `hard_checks_pass: true`;
- [ ] review-archive report has `identity_scan_pass: true`;
- [ ] review-archive report has `archive_ready: true`;
- [ ] final review ZIP exists;
- [ ] main manuscript PDF builds;
- [ ] Supplement PDF builds;
- [ ] no unresolved citation/reference warnings;
- [ ] every manuscript numerical value matches generated JSON/CSV/TikZ output.

## C. Complete author-facing files

Use `docs/mee_title_page_template.md` to prepare the separate non-anonymous title page.

Required items:

- [ ] exact manuscript title;
- [ ] full author names;
- [ ] full affiliations/postal addresses;
- [ ] corresponding author/email;
- [ ] acknowledgements/funding;
- [ ] Author Contributions;
- [ ] Data Availability statement;
- [ ] conflict-of-interest statement;
- [ ] confirmed AI/LLM disclosure/responsibility wording where required.

Use `docs/mee_cover_letter_template.md` for the cover letter and remove all bracketed placeholders.

## D. Manual anonymity audit

Before uploading review files:

- [ ] open the main PDF and inspect document properties/metadata;
- [ ] inspect the Supplement PDF metadata;
- [ ] inspect every file name in the review ZIP;
- [ ] search extracted ZIP contents for author names, email addresses and GitHub usernames;
- [ ] remove public GitHub URLs that reveal authorship from reviewer-facing README/material;
- [ ] check image/PDF metadata if externally generated figures are later added;
- [ ] verify the separate title page is uploaded only in the non-reviewer-facing slot.

The archive builder provides a source-text identity scan, but it does not replace this final manual audit.

## E. MEE upload order

Prepare these distinct submission objects:

1. anonymous main manuscript;
2. anonymous Supplement;
3. separate title page with author metadata;
4. anonymized licensed review code ZIP;
5. cover letter;
6. any submission-system declarations/forms.

Do not upload the public GitHub repository URL in a reviewer-visible field if it reveals identity during double-anonymous review.

## F. After acceptance / public release

Only after the manuscript/repository disclosure plan is final:

- [ ] replace anonymous review-archive wording with final public repository information;
- [ ] archive the frozen release in a DOI-capable service if desired/required;
- [ ] create a stable Git tag/release from the exact version-of-record code commit;
- [ ] record the DOI/release URL in the final Data Availability statement;
- [ ] verify the license is preserved in the public archive;
- [ ] cross-link paper DOI and software/archive DOI after publication.

Suggested tag naming convention after acceptance:

```text
paper-b-v1.0.0
```

Do not create this tag before the license, author metadata and disclosure decisions are resolved.

## G. No-regression rule

After the submission commit is frozen, do not add:

- a new theorem family;
- a weak empirical case study;
- a new benchmark objective merely for breadth;
- claims of novelty for GO-OED, VOI, prediction sets, occupancy or partition refinement.

Only accept changes that fix an error, satisfy a journal requirement, or materially improve clarity without changing the frozen scientific claim.
