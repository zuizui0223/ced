import pytest

from ced.delayed import DelayedExposureFamily, no_uniform_closure_horizon


def test_delayed_family_separates_memory_and_horizon():
    family = DelayedExposureFamily(module_count=4, delay=7)
    assert family.verify()
    assert family.closed_interface_bits == 2
    assert family.open_interface_bits == 5
    assert family.revealing_horizon == 8
    assert family.is_exterior_blind_through(7)
    assert not family.is_exterior_blind_through(8)
    assert ("wait",) * 7 + ("fire",) in family.legal_words_through(8)


@pytest.mark.parametrize("horizon", [0, 1, 4, 12])
def test_every_proposed_uniform_horizon_has_a_delayed_counterexample(horizon):
    witness = no_uniform_closure_horizon(horizon)
    assert witness.delay == horizon
    assert witness.is_exterior_blind_through(horizon)
    assert witness.revealing_horizon == horizon + 1
