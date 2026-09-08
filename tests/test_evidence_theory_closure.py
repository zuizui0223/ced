import json
from pathlib import Path

from ced.evidence_closure import (
    augmentation_block,
    candidate_exhausted,
    mechanism_resolved,
    target_resolved,
)
from ced.learning_licensing import WORLDS, constant_probe, nuisance_detail, target_split

ROOT = Path(__file__).resolve().parents[1]


def mechanism(world):
    return (world.target, world.nuisance)


def target(world):
    return world.target


def test_target_resolution_need_not_resolve_mechanism():
    block = augmentation_block(WORLDS, target_split, WORLDS[0])
    assert target_resolved(block, target)
    assert not mechanism_resolved(block, mechanism)


def test_target_resolution_need_not_exhaust_learning_candidates():
    block = augmentation_block(WORLDS, target_split, WORLDS[0])
    assert target_resolved(block, target)
    assert not candidate_exhausted(block, [nuisance_detail])


def test_candidate_exhaustion_does_not_license_target():
    block = (WORLDS[0], WORLDS[4])
    assert candidate_exhausted(block, [constant_probe])
    assert not target_resolved(block, target)


def test_mechanism_resolution_implies_target_resolution():
    block = (WORLDS[0],)
    assert mechanism_resolved(block, mechanism)
    assert target_resolved(block, target)


def test_realized_acquisition_is_nested():
    block = tuple(WORLDS)
    updated = augmentation_block(block, nuisance_detail, WORLDS[0])
    assert set(updated).issubset(set(block))
    assert len(updated) < len(block)


def test_machine_readable_closure_is_complete():
    path = ROOT / "manuscript" / "evidence_theory_closure.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["status"] == "structural-theory-closed"
    assert data["theorem_count"] == 10
    assert len(data["theorems"]) == 10
    assert len(set(data["theorems"])) == 10
    assert all(data["interfaces_closed"].values())
