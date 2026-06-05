"""Harmony: every public endpoint method has a docstring.

The forms/payments/shipments deprecation shims shipped without docstrings, so
``help(api.forms.get_bol)`` was blank. They are now backfilled, and this gate
keeps the entire public method surface documented going forward — a new
endpoint method that ships without a docstring turns the build red.
"""

from __future__ import annotations

from ab.cli.discovery import discover_endpoints_from_class


def test_all_public_endpoint_methods_have_docstrings():
    eps = discover_endpoints_from_class()
    missing = [
        f"{group}.{m.name}"
        for group, info in eps.items()
        for m in info.methods
        if not (m.docstring or "").strip()
    ]
    assert not missing, "Public endpoint methods missing a docstring:\n  " + "\n  ".join(sorted(missing))
