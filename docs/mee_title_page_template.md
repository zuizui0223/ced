# MEE title page — author-completion template

> **Not for peer review.** Replace bracketed placeholders only after all authors confirm the final metadata and statements.

## Manuscript title

From ecological states to distinguishable futures: Target-safe prediction from finite evidence

## Authors and affiliations

- [AUTHOR 1 FULL NAME] — [AFFILIATION 1, FULL POSTAL ADDRESS]
- [AUTHOR 2 FULL NAME, IF ANY] — [AFFILIATION 2, FULL POSTAL ADDRESS]

## Corresponding author

[NAME]  
[INSTITUTION]  
[EMAIL]

## Acknowledgements

[CONFIRM FUNDING, FIELD/LAB/COMPUTING SUPPORT, COLLEAGUES, OR "None" AS APPROPRIATE]

## Author contributions

Use the journal's requested contribution format and ensure every author approves it.

Draft structure:

- Conceptualization: [NAME(S)]
- Methodology: [NAME(S)]
- Software: [NAME(S)]
- Formal analysis: [NAME(S)]
- Validation: [NAME(S)]
- Visualization: [NAME(S)]
- Writing — original draft: [NAME(S)]
- Writing — review and editing: [NAME(S)]
- Supervision: [NAME(S), IF APPLICABLE]

If AI/LLM-assisted code or text is included in the submission, identify the corresponding or senior author who reviewed and takes responsibility for that material, consistent with MEE policy.

## Data availability

Draft:

> No empirical dataset underlies the reported results. All code required to reproduce the finite theorems, deterministic benchmarks, sensitivity analyses, posterior-support demonstration, tables and figures will be archived in a public version-of-record repository upon acceptance. An anonymized code archive is supplied for peer review.

Confirm the final repository/DOI only after the archive is frozen.

## Conflict of interest

[CONFIRM THE JOURNAL-APPROPRIATE STATEMENT, E.G. "The authors declare no conflicts of interest," ONLY IF TRUE]

## AI / LLM disclosure — draft for author confirmation

MEE requires AI/LLM use in the work to be disclosed in the Methods section, including application and version, and requires a corresponding or senior author to take responsibility for generated code/text.

Proposed factual draft:

> OpenAI ChatGPT (GPT-5.6 Sol) was used during code review, debugging, and manuscript drafting/editing. All mathematical claims, numerical outputs, tests, and submitted source were checked through deterministic code execution and continuous-integration tests. [RESPONSIBLE CORRESPONDING/SENIOR AUTHOR] reviewed and takes responsibility for the submitted text and code.

Before submission, confirm:

- [ ] the wording accurately describes the extent of AI use;
- [ ] the responsible author is named in Author Contributions;
- [ ] all authors approve the disclosure;
- [ ] code portions requiring explicit AI-generation annotations have been identified and annotated;
- [ ] the main Methods section contains the confirmed disclosure.

## Software license

[INSERT THE AUTHOR-APPROVED OPEN-SOURCE LICENSE NAME AFTER THE LICENSE FILE IS ADDED]

Do not submit the MEE code archive until `python scripts/build_mee_review_archive.py` reports `archive_ready: true`.
