from ced.robustness import CommonModeProfile


def test_replication_inside_one_failure_mode_is_not_failure_diversity():
    profile = CommonModeProfile(
        pair_separators=(frozenset({"c1", "c2", "c3"}),),
        failure_modes=(frozenset({"c1", "c2", "c3"}),),
    )
    assert profile.mode_cover_number(0) == 1
    assert profile.common_mode_tolerance == 0
    assert profile.survives(0)
    assert not profile.survives(1)


def test_site_diversity_controls_common_mode_tolerance():
    profile = CommonModeProfile(
        pair_separators=(frozenset({"site-a", "site-b", "site-c"}),),
        failure_modes=(frozenset({"site-a"}), frozenset({"site-b"}), frozenset({"site-c"})),
    )
    assert profile.mode_cover_number(0) == 3
    assert profile.common_mode_tolerance == 2
    assert profile.survives(2)


def test_singleton_modes_recover_raw_separator_count():
    profile = CommonModeProfile.singleton_modes((("x", "y"), ("y",)))
    assert profile.mode_cover_number(0) == 2
    assert profile.mode_cover_number(1) == 1
    assert profile.common_mode_tolerance == 0
