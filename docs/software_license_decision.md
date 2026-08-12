# Software license decision for the MEE submission

## Why this is a blocker

The planned *Methods in Ecology and Evolution* submission includes executable code. The MEE code policy requires submitted code to carry a fully open-source software license. The repository currently has no `LICENSE` file and no project-level license metadata, so the anonymous review archive builder intentionally refuses to create the final ZIP.

This document does **not** select a license. Software ownership, institutional policy, collaborator rights, and desired reuse conditions are author decisions.

## Current repository facts relevant to the decision

- The Python package is primarily a small finite-mathematics / simulation implementation.
- `pyproject.toml` declares no runtime third-party Python dependencies; the development extra requires `pytest>=8`.
- The manuscript and code are intended to be inspectable and reproducible during peer review.
- The final public version is expected to be reusable as a methods implementation rather than held as closed source.
- No license is currently declared, so default copyright restrictions apply until the authors explicitly choose one.

These facts do not determine which open-source license should be used.

## Common author choices to consider

### MIT

Typical reason to choose it:
- minimal, permissive reuse conditions;
- simple attribution/copyright notice requirement;
- broad compatibility with academic and commercial reuse.

Trade-off:
- downstream modified versions can be redistributed under different licensing terms, provided the MIT notice is retained.

### BSD 3-Clause

Typical reason to choose it:
- similarly permissive to MIT;
- includes a non-endorsement clause preventing use of contributor names to promote derived products without permission.

Trade-off:
- still permits proprietary downstream reuse.

### Apache License 2.0

Typical reason to choose it:
- permissive reuse plus explicit patent-license language and contributor protections;
- often preferred when patent clarity matters.

Trade-off:
- longer and administratively more complex than MIT/BSD-3-Clause;
- check institutional guidance if patentable material is involved.

### GPL v3

Typical reason to choose it:
- strong copyleft: redistributed derivative software generally must remain GPL-compatible and source-available.

Trade-off:
- can limit integration into proprietary or incompatibly licensed downstream software;
- may reduce adoption for a general ecological methods package if permissive reuse is a priority.

## Decision questions for the authors / institution

1. Who legally owns the code: individual author(s), university/employer, or a joint arrangement?
2. Are any coauthors or institutions required to approve open-source release?
3. Is there any patentable or commercially sensitive component?
4. Is maximal reuse/adoption more important than requiring downstream derivatives to remain open?
5. Is non-endorsement language desired?
6. Does the institution recommend a standard research-software license?
7. Are any copied/adapted code portions subject to incompatible third-party license terms?

## After a license is chosen

Complete all of the following on one submission branch:

1. Add the canonical license text as `LICENSE`.
2. Add matching project metadata in `pyproject.toml` using the packaging convention appropriate to the chosen license.
3. Add/confirm copyright holder/year only after ownership is confirmed.
4. Run:

```bash
pytest
python scripts/check_mee_submission.py
python scripts/build_mee_review_archive.py
```

5. Verify `paper_b_mee_review_archive_check.json` reports:

```text
license_present: true
identity_scan_pass: true
archive_ready: true
```

6. Inspect the generated ZIP before upload and confirm the chosen `LICENSE` is included.
7. Ensure the manuscript/title-page Data Availability statement matches the public-release plan.

## Do not do automatically

- do not infer copyright ownership from the GitHub account;
- do not choose MIT merely because it is common;
- do not add an author name from account metadata without author confirmation;
- do not create a release/tag before the license and author-facing disclosure decisions are final.
