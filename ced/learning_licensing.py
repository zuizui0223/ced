"""Exact finite-world witness separating mechanism-learning and target-licensing value.

The benchmark is intentionally small and dependency-free. Worlds cross a binary
scientific target with a four-level target-irrelevant mechanism attribute. Two
equal-cost candidate observations are compared on the same prior support:

- ``nuisance_detail`` perfectly resolves the four-level attribute (2 bits about
  full mechanism identity) but leaves both target values compatible;
- ``target_split`` resolves the binary scientific target (1 bit about full
  mechanism identity) and licenses an exact singleton target report.

This is a divergence witness, not a universal optimal-design theorem.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import log2
from typing import Callable, Hashable, Iterable


@dataclass(frozen=True, slots=True)
class World:
    target: int
    nuisance: int

    def __post_init__(self) -> None:
        if self.target not in (0, 1):
            raise ValueError("target must be binary")
        if self.nuisance not in (0, 1, 2, 3):
            raise ValueError("nuisance must be in {0,1,2,3}")


WORLDS: tuple[World, ...] = tuple(
    World(target, nuisance)
    for target in (0, 1)
    for nuisance in (0, 1, 2, 3)
)


def nuisance_detail(world: World) -> int:
    return world.nuisance


def target_split(world: World) -> int:
    return world.target


def constant_probe(world: World) -> int:
    del world
    return 0


CANDIDATES: dict[str, Callable[[World], Hashable]] = {
    "nuisance_detail": nuisance_detail,
    "target_split": target_split,
    "constant_probe": constant_probe,
}


def entropy_uniform_partition(block_sizes: Iterable[int]) -> float:
    """Entropy of a deterministic observation under the uniform prior on WORLDS."""
    sizes = tuple(block_sizes)
    total = sum(sizes)
    entropy = 0.0
    for size in sizes:
        if size <= 0:
            raise ValueError("partition block sizes must be positive")
        p = size / total
        entropy -= p * log2(p)
    return entropy


def outcome_blocks(observation: Callable[[World], Hashable]) -> dict[Hashable, tuple[World, ...]]:
    blocks: dict[Hashable, list[World]] = {}
    for world in WORLDS:
        blocks.setdefault(observation(world), []).append(world)
    return {key: tuple(value) for key, value in blocks.items()}


def mechanism_information_bits(observation: Callable[[World], Hashable]) -> float:
    """I(S;Q) for deterministic Q and uniform full mechanism identity S=WORLD."""
    blocks = outcome_blocks(observation)
    return entropy_uniform_partition(len(block) for block in blocks.values())


def target_sets(observation: Callable[[World], Hashable]) -> dict[Hashable, frozenset[int]]:
    return {
        outcome: frozenset(world.target for world in block)
        for outcome, block in outcome_blocks(observation).items()
    }


def exact_target_resolution_probability(observation: Callable[[World], Hashable]) -> float:
    """Uniform-prior probability that the realized outcome licenses a singleton target."""
    blocks = outcome_blocks(observation)
    resolved_worlds = sum(
        len(block)
        for outcome, block in blocks.items()
        if len({world.target for world in block}) == 1
    )
    return resolved_worlds / len(WORLDS)


def benchmark() -> dict[str, object]:
    candidates: dict[str, dict[str, object]] = {}
    for name, observation in CANDIDATES.items():
        sets = target_sets(observation)
        candidates[name] = {
            "mechanism_information_bits": mechanism_information_bits(observation),
            "exact_target_resolution_probability": exact_target_resolution_probability(observation),
            "outcome_target_sets": {
                str(outcome): sorted(values)
                for outcome, values in sorted(sets.items(), key=lambda item: str(item[0]))
            },
            "equal_cost": 1.0,
        }

    learning_rank = sorted(
        candidates,
        key=lambda name: (
            -float(candidates[name]["mechanism_information_bits"]),
            name,
        ),
    )
    licensing_rank = sorted(
        candidates,
        key=lambda name: (
            -float(candidates[name]["exact_target_resolution_probability"]),
            float(candidates[name]["mechanism_information_bits"]),
            name,
        ),
    )

    return {
        "schema": "ced-learning-licensing-divergence-v1",
        "world_count": len(WORLDS),
        "prior": "uniform over binary target x four-level nuisance attribute",
        "mechanism_identity": "full (target,nuisance) world",
        "scientific_target": "binary target coordinate",
        "candidates": candidates,
        "learning_rank": learning_rank,
        "licensing_rank": licensing_rank,
        "divergence": learning_rank[0] != licensing_rank[0],
        "interpretation": (
            "Mechanism-learning value and target-licensing value rank the same "
            "equal-cost candidate set differently. This finite witness does not "
            "assert a universal observation utility."
        ),
    }
