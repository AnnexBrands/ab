"""Static guard: every canonical example's api.* calls bind to the real signature.

Non-live. Catches — offline — the class of bug a live run would otherwise surface:
an example calling an endpoint with the wrong keyword (e.g. splatting PascalCase
request-fixture keys into a snake_case method) or omitting a required argument.

For each canonical (non-underscore) example, every ``api.<group>[.<sub>].<method>(...)``
call with concrete args (no ``*``/``**`` splat) must ``inspect.Signature.bind`` to the
resolved endpoint method. Calls that splat, or resolve to no known routed method, are
skipped (they can't be checked statically).
"""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

import pytest

from ab.cli.discovery import discover_endpoints_from_class

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples"
_SKIP_STEMS = {"__init__", "__main__", "_runner", "_capture", "constants"}


def _canonical_example_files() -> list[Path]:
    return [
        p for p in sorted(EXAMPLES_DIR.rglob("*.py"))
        if not p.name.startswith("_") and p.stem not in _SKIP_STEMS
    ]


def _attr_chain(node: ast.Attribute) -> list[str]:
    parts: list[str] = []
    cur: ast.expr = node
    while isinstance(cur, ast.Attribute):
        parts.append(cur.attr)
        cur = cur.value
    if isinstance(cur, ast.Name):
        parts.append(cur.id)
        parts.reverse()
        return parts
    return []


def _iter_api_calls(tree: ast.AST):
    """Yield (group, method, n_positional, kw_names) for checkable api.* calls."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        chain = _attr_chain(node.func)
        if len(chain) < 3 or chain[0] != "api":
            continue
        if any(isinstance(a, ast.Starred) for a in node.args):
            continue  # *args splat — can't check
        if any(kw.arg is None for kw in node.keywords):
            continue  # **kwargs splat — can't check
        yield ".".join(chain[1:-1]), chain[-1], len(node.args), [kw.arg for kw in node.keywords]


def _registry():
    return discover_endpoints_from_class()


def test_canonical_example_calls_bind_to_signatures() -> None:
    reg = _registry()
    failures: list[str] = []
    checked = 0

    for path in _canonical_example_files():
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError):
            continue
        rel = path.relative_to(REPO_ROOT)
        for group, method, n_pos, kw_names in _iter_api_calls(tree):
            info = reg.get(group)
            if info is None:
                continue
            func = getattr(info.endpoint_class, method, None)
            if func is None or not callable(func):
                continue
            try:
                sig = inspect.signature(func)
            except (TypeError, ValueError):
                continue
            args = [None] + ["_"] * n_pos  # None = self
            kwargs = {k: "_" for k in kw_names}
            try:
                sig.bind(*args, **kwargs)
                checked += 1
            except TypeError as exc:
                failures.append(f"{rel}: api.{group}.{method}(...) — {exc}")

    assert checked > 0, "no checkable example calls found"
    assert not failures, "Example calls that do not match the endpoint signature:\n  " + "\n  ".join(failures)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
