# Equal-effort repeat-versus-mode allocation theorem

Status: exact corollary of the declared common-mode imperfect-detection contract.

## Question

The existing theorem proves that unlimited repetition inside one shared failure domain cannot remove the all-modes-fail ceiling, and the paper shows an example where independent failure modes outperform concentrated repetition.

That can be misread as the slogan

> “diversify failure modes whenever possible.”

For a multi-coordinate target this is not always correct at finite effort. The sharper design question is:

> With the **same number of reads**, when is it better to spend the second read deepening one mode, and when is it better to spend it creating an independent failure opportunity?

We answer this exactly for the smallest equal-effort comparison: two reads per coordinate.

## Contract

There are `k>=1` truly present coordinates. A mode operates with probability `a`, independently across modes. Conditional on operation, every read is positive with probability `p`, independently, with no false positives. The lower-bound contract is evaluated at its least-favourable boundary `a,p`; larger true values can yield higher realized detection.

Both designs use exactly `2k` reads.

### Depth design R

Use one mode and take two repeats per coordinate.

### Diversity design D

Use two independent modes and take one read per coordinate in each mode.

The target is **joint detection of all k coordinates**.

## Theorem D1 — exact two-read allocation boundary

Let

\[
p_k^*=2-2^{1/k}.
\]

For `0<a<1` and `p>0`:

\[
\boxed{
G_D>G_R
\iff
p>p_k^*
}
\]

and

\[
\boxed{
G_D<G_R
\iff
p<p_k^*.
}
\]

At `p=p_k^*` the two equal-effort designs tie. Boundary cases `a=0`, `a=1`, or `p=0` also remove the failure-diversity advantage and produce the corresponding tie in this comparison.

Thus failure-mode diversification is not uniformly preferable at finite effort: its benefit depends on both per-read sensitivity and how many coordinates must all be recovered.

## Proof

Let

\[
d=1-(1-p)^2=p(2-p)
\]

be the probability that one present coordinate is detected at least once in two independent reads, conditional on those reads being available.

### Depth design

The single shared mode must operate, probability `a`. Conditional on operation, all `k` coordinates must each be detected in their two reads. Therefore

\[
G_R=a d^k=a[p(2-p)]^k.
\]

This is exactly Theorem 1 of `mode_diverse_detection_theorem.md` with `m=1,r=2`.

### Diversity design

Condition on the number of operating modes.

- Exactly one of the two modes operates with probability `2a(1-a)`. Then every one of the `k` coordinates has only one available read, so joint detection probability is `p^k`.
- Both modes operate with probability `a^2`. Then every coordinate has two independent available reads, so joint detection probability is `d^k`.
- If neither mode operates, detection fails.

Hence

\[
G_D=2a(1-a)p^k+a^2d^k.
\]

Subtract:

\[
\begin{aligned}
G_D-G_R
&=2a(1-a)p^k+a^2d^k-ad^k\\
&=a(1-a)\left(2p^k-d^k\right)\\
&=a(1-a)p^k\left[2-(2-p)^k\right].
\end{aligned}
\]

For `0<a<1` and `p>0`, the prefactor `a(1-a)p^k` is strictly positive, so the sign is exactly the sign of

\[
2-(2-p)^k.
\]

Therefore

\[
G_D>G_R
\iff
(2-p)^k<2
\iff
2-p<2^{1/k}
\iff
p>2-2^{1/k}.
\]

The reverse inequality and equality case follow identically. ∎

## Corollary D1a — one coordinate is qualitatively different from joint multi-coordinate recovery

For `k=1`,

\[
p_1^*=0.
\]

Thus with any `0<a<1` and `p>0`, splitting the two reads across independent modes is strictly better for detection of a single coordinate.

For `k>1`, however, `p_k^*>0`. At sufficiently low per-read sensitivity, concentrating two reads within one operating mode gives a stronger all-coordinate guarantee than splitting them across modes.

The intuition is exact: diversity protects against shared mode failure, while depth increases the chance that **every** coordinate is recovered once a mode operates. Joint recovery of many coordinates can make the second effect dominate at low `p`.

## Corollary D1b — the sensitivity threshold rises with coordinate count

Because `2^{1/k}` decreases toward 1 as `k` grows,

\[
p_k^*=2-2^{1/k}
\]

is increasing in `k` and tends to 1.

Therefore the more coordinates that must all be detected, the higher per-read sensitivity must be before one-read-per-mode diversification dominates two reads in one mode at this fixed equal effort.

Examples:

| k | threshold `p_k*` |
|---:|---:|
| 1 | `0` |
| 2 | `2-sqrt(2) ≈ 0.5858` |
| 3 | `2-2^(1/3) ≈ 0.7401` |
| 5 | `≈0.8513` |

This is why “replication is not failure diversity” must not be turned into “failure diversity always dominates replication.”

## Relation to the existing availability ceiling

Theorem D1 is a **finite-effort local allocation result**. The existing ceiling theorem remains true:

\[
1-(1-a)^m
\]

is the supremum of the uniform guarantee as repeats within `m` modes become unlimited.

Thus two statements coexist:

1. at a small fixed budget, low sensitivity and a stringent all-coordinate target can favor deeper repetition;
2. at large repeat effort, a fixed number of modes eventually hits its availability ceiling, so additional independent modes become necessary to certify higher confidence.

The design problem therefore has a real depth-versus-diversity tradeoff rather than a one-direction slogan.

## Claim ceiling

This theorem assumes:

- equal availability lower bound `a` for both independent modes;
- equal sensitivity lower bound `p` for all reads and coordinates;
- independent mode availability;
- independent reads conditional on mode operation;
- no false positives;
- exactly two reads per coordinate in the comparison;
- a target requiring detection of **all** `k` truly present coordinates.

Heterogeneous costs, correlated mode failures, unequal sensitivities, partial-coordinate targets, false positives or adaptive allocation require separate design results.

## Executable obligations

`tests/test_repeat_vs_mode_allocation_boundary.py` must:

1. cross-check both closed forms against `ModeDiverseDetectionPanel`;
2. verify the sign boundary over grids of `k,a,p`;
3. verify equality at `p=2-2^(1/k)`;
4. verify the `k=1` always-diversify corollary for interior `a,p`;
5. verify the threshold increases with `k`;
6. reproduce both sides of the boundary, including a case where repeats beat diversity and one where diversity wins.
