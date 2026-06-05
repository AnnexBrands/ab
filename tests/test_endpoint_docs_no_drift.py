"""No-drift gate for per-endpoint pages and in-source RTD footers.

Mirrors the progress-report freshness gate (``test_progress_no_drift``): both
the generated ``docs/api/jobs/*.md`` pages and the ``Docs:`` footers written
into endpoint docstrings are regenerated in memory and compared against what
is committed. A route/model/signature change that forgets to rerun
``scripts/generate_endpoint_docs.py`` turns the build red, so the docs the
``help()`` footers link to can never silently rot.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "generate_endpoint_docs.py"


def _load_generator():
    spec = importlib.util.spec_from_file_location("generate_endpoint_docs", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod  # so module-level @dataclass can resolve itself
    spec.loader.exec_module(mod)
    return mod


_gen = _load_generator()


def test_per_endpoint_pages_are_current():
    problems = _gen.check_pages()
    assert not problems, (
        "Per-endpoint pages are stale — regenerate with "
        "`python scripts/generate_endpoint_docs.py --pages` "
        "(orphan pages, whose route was removed, must be deleted by hand):\n  " + "\n  ".join(problems)
    )


def test_docstring_footers_are_current():
    problems = _gen.check_docstrings()
    assert not problems, (
        "In-source Docs: footers are stale — regenerate with "
        "`python scripts/generate_endpoint_docs.py --sync-docstrings`:\n  " + "\n  ".join(problems)
    )
