"""Exact equal-effort boundary between depth and failure-mode diversity.

Compare two reads per truly present coordinate allocated either as two repeats
inside one shared failure mode or as one read in each of two independent modes.
The comparison uses the least-favourable lower-bound contract from
``ModeDiverseDetectionPanel``.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class TwoReadAllocationBoundary:
    coordinate_count: int
    availability: float
    sensitivity: float
    sensitivity_threshold: float
    repeat_design_guarantee: float
    diverse_design_guarantee: float
    difference_diverse_minus_repeat: float
    preferred_design: str


def two_read_allocation_boundary(
    *, coordinate_count: int, availability: float, sensitivity: float
) -> TwoReadAllocationBoundary:
    """Compare equal-read one-mode depth against two-mode diversity.

    Both designs use exactly two reads per coordinate.

    - repeat design: one mode, two within-mode reads per coordinate;
    - diverse design: two independent modes, one read per coordinate per mode.

    For 0<a<1 and p>0, the diverse design is better iff
    ``p > 2 - 2**(1/k)``; the repeat design is better below that threshold.
    Boundary cases a in {0,1} or p=0 are ties for the failure-diversity effect.
    """
    k = int(coordinate_count)
    if k < 1:
        raise ValueError("coordinate_count must be positive")
    a = float(availability)
    p = float(sensitivity)
    if not isfinite(a) or not 0.0 <= a <= 1.0:
        raise ValueError("availability must lie in [0,1]")
    if not isfinite(p) or not 0.0 <= p <= 1.0:
        raise ValueError("sensitivity must lie in [0,1]")

    detected_with_two_reads = p * (2.0 - p)
    repeat = a * detected_with_two_reads**k
    diverse = (
        2.0 * a * (1.0 - a) * p**k
        + a**2 * detected_with_two_reads**k
    )
    difference = diverse - repeat
    threshold = 2.0 - 2.0 ** (1.0 / k)

    tol = 1e-12
    if difference > tol:
        preferred = "diverse_modes"
    elif difference < -tol:
        preferred = "within_mode_repeats"
    else:
        preferred = "tie"

    return TwoReadAllocationBoundary(
        coordinate_count=k,
        availability=a,
        sensitivity=p,
        sensitivity_threshold=threshold,
        repeat_design_guarantee=repeat,
        diverse_design_guarantee=diverse,
        difference_diverse_minus_repeat=difference,
        preferred_design=preferred,
    )
