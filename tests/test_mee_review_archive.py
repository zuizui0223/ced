import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_mee_review_archive.py"


def test_review_archive_preflight_is_anonymous_and_blocked_only_by_license():
    module = runpy.run_path(str(SCRIPT))
    report = module["preflight"]()

    assert report["schema_version"] == 1
    assert report["identity_scan_pass"]
    assert report["identity_hits"] == []
    assert report["curated_file_count"] > 0

    # Current branch deliberately leaves the rights-holder license decision unresolved.
    assert not report["license_present"]
    assert report["license_files"] == []
    assert not report["archive_ready"]


def test_archive_builder_refuses_unlicensed_submission_bundle():
    module = runpy.run_path(str(SCRIPT))
    try:
        module["build_archive"]()
    except RuntimeError as error:
        assert "author-approved open-source LICENSE" in str(error)
    else:
        raise AssertionError("unlicensed review archive should not be created")
