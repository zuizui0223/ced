"""Common-mode robustness of canonical distinguishing panels.

The core point is that raw replicate count is not failure diversity.  A panel
remains exact after r declared common-mode failures precisely when every
canonical class pair retains a separator outside every union of r modes.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable


@dataclass(frozen=True)
class CommonModeProfile:
    """Separator supports and declared common-mode failure architecture.

    ``pair_separators`` lists the selected cells that distinguish each abstract
    pair. ``failure_modes`` lists the cells lost together under each named mode.
    The mode-cover number of a pair is the least number of modes whose union
    covers all its separators.
    """

    pair_separators: tuple[frozenset[str], ...]
    failure_modes: tuple[frozenset[str], ...]

    def __post_init__(self) -> None:
        if not self.pair_separators or any(not support for support in self.pair_separators):
            raise ValueError("every pair must have a nonempty separator support")
        if not self.failure_modes or any(not mode for mode in self.failure_modes):
            raise ValueError("at least one nonempty failure mode is required")
        all_cells = set().union(*self.failure_modes)
        if any(not support <= all_cells for support in self.pair_separators):
            raise ValueError("every separator cell must occur in a declared failure mode")

    def mode_cover_number(self, pair_index: int) -> int:
        if not isinstance(pair_index, int) or isinstance(pair_index, bool) or not 0 <= pair_index < len(self.pair_separators):
            raise ValueError("pair_index outside support list")
        support = self.pair_separators[pair_index]
        for size in range(1, len(self.failure_modes) + 1):
            for choice in combinations(self.failure_modes, size):
                if support <= set().union(*choice):
                    return size
        raise AssertionError("all separator cells lie in declared modes")

    @property
    def common_mode_tolerance(self) -> int:
        return min(self.mode_cover_number(index) for index in range(len(self.pair_separators))) - 1

    def survives(self, failure_budget: int) -> bool:
        if not isinstance(failure_budget, int) or isinstance(failure_budget, bool) or failure_budget < 0:
            raise ValueError("failure_budget must be a nonnegative integer")
        return self.common_mode_tolerance >= failure_budget

    @classmethod
    def singleton_modes(cls, supports: Iterable[Iterable[str]]) -> "CommonModeProfile":
        normalized = tuple(frozenset(support) for support in supports)
        cells = sorted(set().union(*normalized))
        return cls(normalized, tuple(frozenset({cell}) for cell in cells))
