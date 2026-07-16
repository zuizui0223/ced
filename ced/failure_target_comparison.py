"""Equal-cost comparison of failure architectures for ecological target resolution."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .target_resolution import CostedTargetResolutionDesign


@dataclass(frozen=True)
class EqualCostFailureComparison:
    """Compare target-resolution designs that spend the same declared cost."""

    designs: tuple[CostedTargetResolutionDesign, ...]

    def __post_init__(self) -> None:
        designs = tuple(self.designs)
        if len(designs) < 2:
            raise ValueError("at least two designs are required")
        if not all(isinstance(design, CostedTargetResolutionDesign) for design in designs):
            raise ValueError("designs must be costed target-resolution designs")
        if len({design.name for design in designs}) != len(designs):
            raise ValueError("design names must be unique")
        if max(design.cost for design in designs) - min(design.cost for design in designs) > 1e-12:
            raise ValueError("all compared designs must have equal declared cost")
        object.__setattr__(self, "designs", designs)

    @property
    def shared_cost(self) -> float:
        return self.designs[0].cost

    @property
    def ranked_by_correct_resolution(self) -> tuple[str, ...]:
        return tuple(
            design.name
            for design in sorted(
                self.designs,
                key=lambda item: (
                    -item.resolution.correct_resolution_probability,
                    item.resolution.wrong_resolution_probability,
                    item.resolution.ambiguity_probability,
                    item.name,
                ),
            )
        )

    @property
    def ranked_by_wrong_resolution(self) -> tuple[str, ...]:
        return tuple(
            design.name
            for design in sorted(
                self.designs,
                key=lambda item: (
                    item.resolution.wrong_resolution_probability,
                    -item.resolution.correct_resolution_probability,
                    item.name,
                ),
            )
        )

    def feasible_designs(
        self, minimum_correct: float, maximum_wrong: float
    ) -> tuple[str, ...]:
        return tuple(
            design.name
            for design in self.designs
            if design.resolution.meets(minimum_correct, maximum_wrong)
        )

    def dominant_designs(self) -> tuple[str, ...]:
        """Return designs not Pareto-dominated in correct/wrong/ambiguity risk."""
        survivors: list[str] = []
        for candidate in self.designs:
            c = candidate.resolution
            dominated = False
            for other in self.designs:
                if other is candidate:
                    continue
                o = other.resolution
                weakly_better = (
                    o.correct_resolution_probability >= c.correct_resolution_probability
                    and o.wrong_resolution_probability <= c.wrong_resolution_probability
                    and o.ambiguity_probability <= c.ambiguity_probability
                )
                strictly_better = (
                    o.correct_resolution_probability > c.correct_resolution_probability
                    or o.wrong_resolution_probability < c.wrong_resolution_probability
                    or o.ambiguity_probability < c.ambiguity_probability
                )
                if weakly_better and strictly_better:
                    dominated = True
                    break
            if not dominated:
                survivors.append(candidate.name)
        return tuple(survivors)

    @classmethod
    def from_iterable(
        cls, designs: Iterable[CostedTargetResolutionDesign]
    ) -> "EqualCostFailureComparison":
        return cls(tuple(designs))
