"""Gate test: every ExampleEntry with response_model must also set fixture_file.

Enforces the contract from ``contracts/fixture-completeness.md``.
"""

from __future__ import annotations

import importlib
import pkgutil

import pytest

import examples


def _collect_violations() -> list[str]:
    """Scan all example modules and return entries violating the invariant."""
    violations: list[str] = []
    for _importer, modname, _ispkg in pkgutil.iter_modules(examples.__path__):
        if modname.startswith("_"):
            continue
        mod = importlib.import_module(f"examples.{modname}")
        runner = getattr(mod, "runner", None)
        if runner is None:
            continue
        for entry in runner.entries:
            rm = getattr(entry, "response_model", None)
            ff = getattr(entry, "fixture_file", None)
            if rm and rm not in ("bytes", "str") and not ff:
                violations.append(
                    f"examples/{modname}.py :: {entry.name} "
                    f"(response_model={rm!r}, fixture_file=None)"
                )
    return violations


def test_all_response_models_have_fixture_file():
    """Every entry with response_model (except bytes/str) must have fixture_file."""
    violations = _collect_violations()
    if violations:
        msg = (
            f"{len(violations)} entry(ies) have response_model without "
            f"fixture_file:\n" + "\n".join(f"  - {v}" for v in violations)
        )
        pytest.fail(msg)
