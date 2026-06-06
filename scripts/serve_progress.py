#!/usr/bin/env python
"""Launch the interactive example-capture / harmony / sign-off app (feature 037).

    python scripts/serve_progress.py            # http://127.0.0.1:8765
    python scripts/serve_progress.py --port 9000

Complements the static html/progress.html report: left-nav drill-down by tag/path,
per-endpoint Four-Way Harmony with real coverage, HTTP request/response capture to
SQLite (progress.db), and interactive sign-off (example / tests / Sphinx).

Tip: refresh coverage first so the harmony "Test" column is current::

    coverage run --source=ab -m pytest -m "not live" -q && coverage json -o coverage.json
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ab.progress.app import serve  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args(argv)
    serve(host=args.host, port=args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
