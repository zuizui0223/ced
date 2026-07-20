# Paper B benchmark review fixes

This branch addresses the code-review findings that blocked use of the benchmark as manuscript evidence.

- Expected information gain is now calculated by exact posterior entropy reduction from explicit likelihood kernels.
- The benchmark no longer asserts in advance which experiment EIG must select.
- State, response, and nuisance experiments produce separate records; unperformed experiments cannot leak outcomes.
- All strategies use the same posterior risk-limited terminal report.
- The 5% false-resolution equality boundary is handled with numerical tolerance.
- Target-safe design does not pay for a follow-up experiment that cannot satisfy the reporting contract.
- The benchmark is executed by reproducibility CI and its JSON, CSV, and LaTeX outputs are uploaded.
- The focal pollinator replay was removed and the adaptive-policy tests were generalized.
