"""Compatibility entry point for the corrected Paper B benchmark."""
from __future__ import annotations

import runpy
from pathlib import Path

_IMPLEMENTATION = Path(__file__).with_name("paper_b_benchmark_core.py")
_namespace = runpy.run_path(str(_IMPLEMENTATION))
globals().update({key: value for key, value in _namespace.items() if not key.startswith("__")})


if __name__ == "__main__":
    main()
