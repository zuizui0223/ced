"""Finite compatible-world closure relations for the integrated Evidence paper.

This module does not define one universal utility or stopping theorem. It makes the
minimal exact relations among three distinct states explicit:

- mechanism_resolved: the declared mechanism state is constant on the current block;
- target_resolved: the declared scientific target is constant on the current block;
- candidate_exhausted: every declared deterministic candidate is constant on the block.

When target is a deterministic function of mechanism, mechanism resolution implies
target resolution. The converse need not hold. Candidate exhaustion need not imply
either resolution state.
"""
from __future__ import annotations

from math import log2
from typing import Callable, Hashable, Iterable, Sequence, TypeVar

W = TypeVar("W")


def compatible_block(
    worlds: Sequence[W],
    observation: Callable[[W], Hashable],
    realized_index: int,
) -> tuple[W, ...]:
    if realized_index < 0 or realized_index >= len(worlds):
        raise IndexError("realized_index out of range")
    value = observation(worlds[realized_index])
    return tuple(world for world in worlds if observation(world) == value)


def value_set(block: Iterable[W], mapping: Callable[[W], Hashable]) -> frozenset[Hashable]:
    return frozenset(mapping(world) for world in block)


def mechanism_resolved(block: Iterable[W], mechanism: Callable[[W], Hashable]) -> bool:
    return len(value_set(block, mechanism)) == 1


def target_resolved(block: Iterable[W], target: Callable[[W], Hashable]) -> bool:
    return len(value_set(block, target)) == 1


def deterministic_information_bits(
    block: Sequence[W], observation: Callable[[W], Hashable]
) -> float:
    """Mutual information I(W;Q) for deterministic Q under a uniform block prior."""
    if not block:
        raise ValueError("block must be non-empty")
    counts: dict[Hashable, int] = {}
    for world in block:
        counts[observation(world)] = counts.get(observation(world), 0) + 1
    total = len(block)
    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * log2(p)
    return entropy


def candidate_exhausted(
    block: Sequence[W], candidates: Iterable[Callable[[W], Hashable]]
) -> bool:
    """True exactly when every declared deterministic candidate is constant on block."""
    return all(deterministic_information_bits(block, candidate) == 0.0 for candidate in candidates)


def augmentation_block(
    block: Sequence[W],
    observation: Callable[[W], Hashable],
    realized_world: W,
) -> tuple[W, ...]:
    """Condition a current compatible block on one realized additional observation."""
    q = observation(realized_world)
    return tuple(world for world in block if observation(world) == q)
