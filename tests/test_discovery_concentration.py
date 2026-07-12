import pytest

from ced.discovery_concentration import IndependentFalseDiscoveryConcentration


def test_independent_false_discovery_concentration():
    design = IndependentFalseDiscoveryConcentration((0.01, 0.02, 0.03, 0.04, 0.05))
    assert design.coordinate_count == 5
    assert design.expected_false_discoveries_upper_bound == pytest.approx(0.15)
    assert design.exact_independent_tail_upper_bound(2) == pytest.approx(0.008058172)
    assert design.chernoff_tail_upper_bound(2) == pytest.approx(0.035773984814635305)
    assert design.markov_tail_upper_bound(2) == pytest.approx(0.075)
    assert design.exact_independent_tail_upper_bound(3) == pytest.approx(0.000216852)
    assert design.exact_zero_false_discovery_probability_lower_bound() == pytest.approx(
        0.858277728
    )
    assert design.verify()


def test_tail_bound_boundaries():
    design = IndependentFalseDiscoveryConcentration((0.0, 0.0, 0.0))
    assert design.exact_independent_tail_upper_bound(0) == 1.0
    assert design.exact_independent_tail_upper_bound(1) == 0.0
    assert design.chernoff_tail_upper_bound(1) == 0.0
    assert design.exact_independent_tail_upper_bound(4) == 0.0


def test_rejects_invalid_contracts():
    with pytest.raises(ValueError):
        IndependentFalseDiscoveryConcentration(())
    with pytest.raises(ValueError):
        IndependentFalseDiscoveryConcentration((-0.1,))
    with pytest.raises(ValueError):
        IndependentFalseDiscoveryConcentration((1.1,))
    design = IndependentFalseDiscoveryConcentration((0.1,))
    with pytest.raises(ValueError):
        design.markov_tail_upper_bound(0)
    with pytest.raises(ValueError):
        design.chernoff_tail_upper_bound(0)
    with pytest.raises(ValueError):
        design.exact_independent_tail_upper_bound(-1)
