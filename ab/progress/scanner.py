"""Filesystem scanner for fixture files and test constants."""

from __future__ import annotations

import re
from pathlib import Path

from ab.progress.models import Constant

_CONSTANT_RE = re.compile(r"^(LIVE_\w+)\s*=\s*(.+)", re.MULTILINE)


def scan_fixture_files(directory: Path) -> set[str]:
    """Scan a directory for fixture JSON files.

    Returns:
        Set of model names (filename stems), e.g. {"CompanySimple", "Job"}.
    """
    if not directory.is_dir():
        return set()
    return {f.stem for f in directory.glob("*.json")}


def parse_constants(path: Path) -> list[Constant]:
    """Parse tests/constants.py for LIVE_* assignments.

    Returns:
        List of Constant objects with name, value, and inferred type.
    """
    if not path.is_file():
        return []

    text = path.read_text()
    constants: list[Constant] = []

    for match in _CONSTANT_RE.finditer(text):
        name = match.group(1)
        raw_value = match.group(2).strip().rstrip("#").strip()
        # Remove inline comments
        if "  #" in raw_value:
            raw_value = raw_value[: raw_value.index("  #")].strip()

        value_type = _infer_type(raw_value)
        constants.append(Constant(name=name, value=raw_value, value_type=value_type))

    return constants


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
