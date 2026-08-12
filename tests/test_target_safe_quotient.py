import itertools

import pytest

from ced.target_safe_quotient import TargetSafeQuotient, minimal_target_safe_quotient


def _canonical(values):
    mapping = {}
    result = []
    for value in values:
        if value not in mapping:
            mapping[value] = len(mapping)
        result.append(mapping[value])
    return tuple(result)


def _all_canonical_partitions(size):
    # Every set partition has a unique restricted-growth/canonical label tuple.
    for labels in itertools.product(range(size), repeat=size):
        if labels[0] != 0 or labels != _canonical(labels):
            continue
        yield labels


def _example():
    worlds = ("A0", "A1", "A2", "B0", "B1")
    actions = ("treat",)
    successors = {
        "A0": "B0",
        "A1": "B0",
        "A2": "B1",
        "B0": "B0",
        "B1": "B1",
    }

    def record(world):
        return world[0]

    def target(world):
        if world == "B0":
            return "recover"
        if world == "B1":
            return "persist"
        return "pending"

    def successor(world, action):
        assert action == "treat"
        return successors[world]

    return worlds, actions, record, target, successor


def test_refinement_propagates_future_target_distinctions_upstream():
    worlds, actions, record, target, successor = _example()
    quotient = minimal_target_safe_quotient(worlds, record, target, actions, successor)

    assert quotient.blocks == (("A0", "A1"), ("A2",), ("B0",), ("B1",))
    assert quotient.class_of("A0") == quotient.class_of("A1")
    assert quotient.class_of("A0") != quotient.class_of("A2")
    assert quotient.successor_class(quotient.class_of("A0"), "treat") == quotient.class_of("B0")
    assert quotient.successor_class(quotient.class_of("A2"), "treat") == quotient.class_of("B1")
    assert quotient.verify()


def test_changing_target_coarsens_quotient_without_changing_worlds_or_actions():
    worlds, actions, record, _, successor = _example()

    def coarse_target(world):
        return "pending" if world.startswith("A") else "managed"

    quotient = minimal_target_safe_quotient(
        worlds, record, coarse_target, actions, successor
    )
    assert quotient.blocks == (("A0", "A1", "A2"), ("B0", "B1"))


def test_fixed_point_is_coarsest_among_all_valid_partitions_by_exhaustive_oracle():
    worlds, actions, record, target, successor = _example()
    quotient = minimal_target_safe_quotient(worlds, record, target, actions, successor)
    records = tuple(record(world) for world in worlds)
    targets = tuple(target(world) for world in worlds)
    successors = tuple((successor(world, "treat"),) for world in worlds)

    valid = []
    for labels in _all_canonical_partitions(len(worlds)):
        try:
            candidate = TargetSafeQuotient(
                worlds=worlds,
                records=records,
                targets=targets,
                actions=actions,
                successors=successors,
                class_labels=labels,
            )
        except ValueError:
            continue
        valid.append(candidate)

    assert valid
    assert all(candidate.refines(quotient) for candidate in valid)
    assert quotient.state_count == min(candidate.state_count for candidate in valid)
    assert any(candidate.state_count > quotient.state_count for candidate in valid)


def test_successor_function_must_remain_inside_declared_world_set():
    with pytest.raises(ValueError):
        minimal_target_safe_quotient(
            worlds=(0, 1),
            record_function=lambda world: 0,
            target_function=lambda world: 0,
            actions=("a",),
            successor_function=lambda world, action: 2,
        )


@pytest.mark.parametrize(
    "record_function,target_function",
    [
        (lambda world: [world], lambda world: 0),
        (lambda world: 0, lambda world: [world]),
    ],
)
def test_record_and_target_values_must_be_hashable(record_function, target_function):
    with pytest.raises(ValueError, match="must be hashable"):
        minimal_target_safe_quotient(
            worlds=(0, 1),
            record_function=record_function,
            target_function=target_function,
            actions=(),
            successor_function=lambda world, action: world,
        )
