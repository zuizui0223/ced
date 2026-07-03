from scripts.verify_ced_core import build_report


def test_replay_report_matches_declared_witnesses():
    report = build_report()
    assert report["schema_version"] == 1
    assert report["delayed_exposure"] == {
        "module_count": 4,
        "delay": 5,
        "closed_interface_bits": 2,
        "open_interface_bits": 5,
        "revealing_horizon": 6,
    }
    assert report["no_uniform_horizon"] == {
        "proposed_horizon": 7,
        "counterexample_revealing_horizon": 8,
    }
    assert report["partial_panel"]["retained_bits"] == 4
    assert report["partial_panel"]["residual_bits"] == 2
    assert report["partial_panel"]["quotient_state_count"] == 16
    assert report["partial_panel"]["residual_class_size"] == 4
    assert report["common_mode"] == {"mode_cover_number": 3, "tolerance": 2}
