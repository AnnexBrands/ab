"""Filesystem scanner for fixture files and test constants."""

from __future__ import annotations

import ast
import re
from pathlib import Path

from ab.progress.models import Constant

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def scan_fixture_files(directory: Path) -> set[str]:
    """Scan a directory for fixture JSON files.

    Returns:
        Set of model names (filename stems), e.g. {"CompanySimple", "Job"}.
    """
    if not directory.is_dir():
        return set()
    return {f.stem for f in directory.glob("*.json")}


def parse_constants(path: Path) -> list[Constant]:
    """Discover the ``TEST_*`` constants exposed by a constants module.

    Uses :mod:`ast` (no import/exec, no side effects) so it works whether the
    module assigns the constants directly *or* re-exports them via
    ``from examples.constants import (...)``. Re-exported names are resolved
    back to their source module to recover the literal value where possible.

    Returns:
        List of Constant objects with name, value, and inferred type.
    """
    if not path.is_file():
        return []

    try:
        tree = ast.parse(path.read_text())
    except (OSError, SyntaxError):
        return []

    values = _module_assignments(tree)

    # Names re-exported via ``from <module> import (TEST_*, ...)`` — resolve
    # their literal values from the source module when it is local.
    for name, module in _imported_test_names(tree).items():
        if name in values:
            continue
        source = _resolve_module_file(module)
        src_values = (
            _module_assignments(_safe_parse(source)) if source else {}
        )
        values[name] = src_values.get(name, "")

    return [
        Constant(name=name, value=value, value_type=_infer_type(value))
        for name, value in sorted(values.items())
    ]


def _module_assignments(tree: ast.AST | None) -> dict[str, str]:
    """Return ``{TEST_NAME: literal_value_str}`` for direct assignments."""
    out: dict[str, str] = {}
    if tree is None:
        return out
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            targets, value = node.targets, node.value
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            targets, value = [node.target], node.value
        else:
            continue
        for target in targets:
            if isinstance(target, ast.Name) and target.id.startswith("TEST_"):
                try:
                    out[target.id] = ast.unparse(value).strip()
                except Exception:  # pragma: no cover - defensive
                    out[target.id] = ""
    return out


def _imported_test_names(tree: ast.AST) -> dict[str, str]:
    """Return ``{TEST_NAME: source_module}`` for re-exported constants."""
    out: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                if alias.name.startswith("TEST_"):
                    out.setdefault(alias.name, node.module)
    return out


def _resolve_module_file(module: str) -> Path | None:
    """Resolve a dotted module name to a file under the repo root."""
    candidate = REPO_ROOT / Path(*module.split(".")).with_suffix(".py")
    return candidate if candidate.is_file() else None


def _safe_parse(path: Path | None) -> ast.AST | None:
    if path is None or not path.is_file():
        return None
    try:
        return ast.parse(path.read_text())
    except (OSError, SyntaxError):
        return None


def _infer_type(raw_value: str) -> str:
    """Infer the type of a constant value from its string representation."""
    stripped = raw_value.strip("\"'")
    # UUID pattern
    if re.match(
        r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        stripped,
        re.IGNORECASE,
    ):
        return "uuid"
    # Integer
    try:
        int(raw_value)
        return "int"
    except ValueError:
        pass
    return "str"
