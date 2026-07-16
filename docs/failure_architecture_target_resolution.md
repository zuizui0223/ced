# Failure architecture and target-resolution reliability

## Question

At equal declared monitoring cost, does repeating effort inside one shared failure domain provide the same ecological reporting guarantee as distributing effort across independent or partially shared modes?

## Declared comparison

For one true management target (`decrease`), compare three cost-12 designs:

| Architecture | Correct report | Wrong report | Remaining ambiguity |
|---|---:|---:|---:|
| shared mode | 0.72 | 0.03 | 0.25 |
| overlapping modes | 0.84 | 0.025 | 0.135 |
| independent modes | 0.91 | 0.02 | 0.07 |

The probabilities are declared finite witness values used to connect the existing failure-mode theorems to the target-resolution layer. They are not field estimates.

## Result

At equal cost, the independent-mode design Pareto-dominates the other two in this witness: it has higher correct resolution, lower wrong resolution, and lower ambiguity.

Under

```text
correct >= 0.80
wrong <= 0.03
```

both overlapping and independent modes are feasible. Under

```text
correct >= 0.90
wrong <= 0.02
```

only independent modes remain feasible.

## Manuscript interpretation

The combined CED–MRM paper should state the result in target-aware language:

> Failure diversity changes the probability of reaching a report-safe quotient class. Equal numbers of reads or equal total cost do not imply equal probability of resolving the ecological management target.

This connects CED's shared-failure mathematics to MRM's honest-report criterion. A failed or common-mode-corrupted experiment does not merely reduce detection probability; it can leave the future management response ambiguous or, under false alerts, support the wrong deterministic report.

## Boundary

The ranking is conditional on the declared record distributions. The general theorem is the accounting and comparison framework, not a universal assertion that every independent-mode design dominates every overlapping design.
