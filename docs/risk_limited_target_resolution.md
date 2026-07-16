# Risk-limited target resolution

## Purpose

The experiment-induced quotient says which ecological targets remain compatible with each record. A stochastic observation process adds a second question: with what probability does the design resolve the requested target correctly, resolve it incorrectly, or leave ambiguity?

## Three-way decomposition

For one declared true target and a distribution over possible records:

```text
correct resolution: the compatible-target set is exactly {true target}
wrong resolution:   the compatible-target set is a wrong singleton
ambiguity:          more than one target remains compatible.
```

These probabilities sum to one. The wrong-resolution probability is stricter than ordinary non-detection risk because it counts only records that would justify an incorrect deterministic ecological report.

## Cost-aware design criterion

For declared experiment cost `c`, minimum correct-resolution probability `gamma`, and maximum wrong-resolution probability `epsilon`, a design is feasible when

```text
P(correct target resolution) >= gamma
P(wrong deterministic report) <= epsilon.
```

Among feasible designs, choose the least-cost experiment. If no design is feasible, retain a set-valued report rather than forcing a deterministic prediction.

## Joint presence × mechanism witness

For a truly present interaction whose management response is `decrease`:

### Stop and report set-valued

```text
correct = 0
wrong = 0
ambiguous = 1
cost = 0
```

### Additional presence detection only

```text
correct = 0
wrong = 0.10
ambiguous = 0.90
cost = 1
```

Presence detection does not determine whether the response decreases or increases.

### Response intervention

```text
correct = 0.88
wrong = 0.03
ambiguous = 0.09
cost = 2.5
```

Under requirements `correct >= 0.80` and `wrong <= 0.05`, the response intervention is the cheapest feasible design.

## Manuscript interpretation

Observation-error bounds should enter the combined CED–MRM paper as reliability of quotient refinement. Detection effort is valuable only when it moves the record into a target-safe class. Repeated presence confirmation can still be insufficient when mechanism ambiguity controls the management prediction.

## Non-claims

The probabilities, costs, and compatible-target sets are declared finite inputs. The analysis does not estimate them from field data, solve a full sequential decision problem, or assign utility to ecological outcomes.
