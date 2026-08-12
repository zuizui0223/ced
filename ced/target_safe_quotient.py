"""Minimal target-safe quotients for finite ecological latent-world systems.

A deterministic experiment or current observation supplies an initial partition of
latent worlds. A requested finite-valued target and declared actions may require
further distinctions because worlds that look identical now can imply different
reports now or after an intervention. This module constructs the unique coarsest
refinement that preserves the initial record, is target-constant, and has
deterministic successor classes under every declared action.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Hashable, Iterable

World = Hashable
Record = Hashable
Target = Hashable
Action = Hashable


def _hashable_tuple(name: str, values: Iterable[Hashable], *, nonempty: bool = True) -> tuple[Hashable, ...]:
    result = tuple(values)
    if nonempty and not result:
        raise ValueError(f"{name} must be nonempty")
    if len(set(result)) != len(result):
        raise ValueError(f"{name} values must be unique")
    for value in result:
        try:
            hash(value)
        except TypeError as error:
            raise ValueError(f"{name} values must be hashable") from error
    return result


def _canonical(signatures: Iterable[Hashable]) -> tuple[int, ...]:
    labels: dict[Hashable, int] = {}
    result: list[int] = []
    for signature in signatures:
        if signature not in labels:
            labels[signature] = len(labels)
        result.append(labels[signature])
    return tuple(result)


@dataclass(frozen=True)
class TargetSafeQuotient:
    """A finite observation-preserving, target-constant, action-stable quotient."""

    worlds: tuple[World, ...]
    records: tuple[Record, ...]
    targets: tuple[Target, ...]
    actions: tuple[Action, ...]
    successors: tuple[tuple[World, ...], ...]
    class_labels: tuple[int, ...]

    def __post_init__(self) -> None:
        worlds = _hashable_tuple("worlds", self.worlds)
        actions = _hashable_tuple("actions", self.actions, nonempty=False)
        records = tuple(self.records)
        targets = tuple(self.targets)
        successors = tuple(tuple(row) for row in self.successors)
        labels = tuple(self.class_labels)

        if len(records) != len(worlds) or len(targets) != len(worlds):
            raise ValueError("records and targets must align with worlds")
        if len(successors) != len(worlds) or any(len(row) != len(actions) for row in successors):
            raise ValueError("successors must provide one successor per world and action")
        if any(successor not in worlds for row in successors for successor in row):
            raise ValueError("every successor must belong to worlds")
        if len(labels) != len(worlds) or any(
            not isinstance(label, int) or isinstance(label, bool) or label < 0
            for label in labels
        ):
            raise ValueError("class_labels must be nonnegative integers aligned with worlds")
        if labels != _canonical(labels):
            raise ValueError("class_labels must use canonical first-occurrence numbering")

        object.__setattr__(self, "worlds", worlds)
        object.__setattr__(self, "actions", actions)
        object.__setattr__(self, "records", records)
        object.__setattr__(self, "targets", targets)
        object.__setattr__(self, "successors", successors)
        object.__setattr__(self, "class_labels", labels)

        world_index = {world: index for index, world in enumerate(worlds)}
        for left in range(len(worlds)):
            for right in range(left + 1, len(worlds)):
                if labels[left] != labels[right]:
                    continue
                if records[left] != records[right]:
                    raise ValueError("quotient classes must preserve the initial record")
                if targets[left] != targets[right]:
                    raise ValueError("quotient classes must be target-constant")
                for action_index in range(len(actions)):
                    left_successor = world_index[successors[left][action_index]]
                    right_successor = world_index[successors[right][action_index]]
                    if labels[left_successor] != labels[right_successor]:
                        raise ValueError("quotient classes must have deterministic action successors")

    @property
    def state_count(self) -> int:
        return max(self.class_labels) + 1

    @property
    def blocks(self) -> tuple[tuple[World, ...], ...]:
        return tuple(
            tuple(
                world
                for world, label in zip(self.worlds, self.class_labels)
                if label == block
            )
            for block in range(self.state_count)
        )

    def class_of(self, world: World) -> int:
        try:
            return self.class_labels[self.worlds.index(world)]
        except ValueError as error:
            raise ValueError("unknown latent world") from error

    def successor_class(self, quotient_state: int, action: Action) -> int:
        if action not in self.actions:
            raise ValueError("unknown action")
        if (
            not isinstance(quotient_state, int)
            or isinstance(quotient_state, bool)
            or not 0 <= quotient_state < self.state_count
        ):
            raise ValueError("quotient state outside quotient")
        representative_index = self.class_labels.index(quotient_state)
        action_index = self.actions.index(action)
        return self.class_of(self.successors[representative_index][action_index])

    def refines(self, other: "TargetSafeQuotient") -> bool:
        """Whether every class of this quotient lies inside a class of ``other``."""
        if self.worlds != other.worlds:
            raise ValueError("quotients must use the same ordered latent worlds")
        return all(
            self.class_labels[left] != self.class_labels[right]
            or other.class_labels[left] == other.class_labels[right]
            for left in range(len(self.worlds))
            for right in range(len(self.worlds))
        )

    def verify(self) -> bool:
        return bool(self.blocks) and sum(map(len, self.blocks)) == len(self.worlds)


def minimal_target_safe_quotient(
    worlds: Iterable[World],
    record_function,
    target_function,
    actions: Iterable[Action],
    successor_function,
) -> TargetSafeQuotient:
    """Construct the unique coarsest target-safe refinement of a finite record partition.

    Starting from worlds with equal current records, refinement repeatedly separates
    worlds whose target values differ or whose successors under a declared action
    fall into different current blocks. Finiteness guarantees termination. The
    fixed point is the coarsest partition preserving the initial records, making
    the target deterministic inside every class, and giving every quotient class a
    deterministic successor under every declared action.
    """

    world_tuple = _hashable_tuple("worlds", worlds)
    action_tuple = _hashable_tuple("actions", actions, nonempty=False)
    records = tuple(record_function(world) for world in world_tuple)
    targets = tuple(target_function(world) for world in world_tuple)
    world_index = {world: index for index, world in enumerate(world_tuple)}
    successors = tuple(
        tuple(successor_function(world, action) for action in action_tuple)
        for world in world_tuple
    )
    if any(successor not in world_index for row in successors for successor in row):
        raise ValueError("successor_function must map declared worlds back into worlds")

    labels = _canonical(records)
    while True:
        signatures = []
        for index in range(len(world_tuple)):
            successor_labels = tuple(
                labels[world_index[successor]] for successor in successors[index]
            )
            signatures.append((labels[index], targets[index], successor_labels))
        refined = _canonical(signatures)
        if refined == labels:
            return TargetSafeQuotient(
                worlds=world_tuple,
                records=records,
                targets=targets,
                actions=action_tuple,
                successors=successors,
                class_labels=labels,
            )
        labels = refined
