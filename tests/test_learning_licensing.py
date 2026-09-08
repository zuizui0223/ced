from __future__ import annotations

from ced.learning_licensing import (
    benchmark,
    constant_probe,
    exact_target_resolution_probability,
    mechanism_information_bits,
    nuisance_detail,
    target_split,
)


def test_exact_candidate_values() -> None:
    assert mechanism_information_bits(nuisance_detail) == 2.0
    assert mechanism_information_bits(target_split) == 1.0
    assert mechanism_information_bits(constant_probe) == 0.0

    assert exact_target_resolution_probability(nuisance_detail) == 0.0
    assert exact_target_resolution_probability(target_split) == 1.0
    assert exact_target_resolution_probability(constant_probe) == 0.0


def test_learning_and_licensing_rank_candidates_differently() -> None:
    result = benchmark()
    assert result["world_count"] == 8
    assert result["learning_rank"][0] == "nuisance_detail"
    assert result["licensing_rank"][0] == "target_split"
    assert result["divergence"] is True


def test_target_sets_make_divergence_exact() -> None:
    result = benchmark()["candidates"]
    nuisance_sets = result["nuisance_detail"]["outcome_target_sets"]
    assert set(tuple(values) for values in nuisance_sets.values()) == {(0, 1)}

    target_sets = result["target_split"]["outcome_target_sets"]
    assert sorted(tuple(values) for values in target_sets.values()) == [(0,), (1,)]
