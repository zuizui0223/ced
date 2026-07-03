import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_ced_core.py"


def test_replay_report_matches_declared_witnesses():
    completed = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    report = json.loads(completed.stdout)
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
