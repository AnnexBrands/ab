"""Fixture coverage verification test.

Asserts every fixture file in tests/fixtures/ is tracked in
FIXTURES.md, and every captured entry in FIXTURES.md has a
corresponding fixture file on disk.
"""

from __future__ import annotations

import re
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / "fixtures"
FIXTURES_MD = Path(__file__).parent.parent / "FIXTURES.md"


def _extract_models_from_section(content: str, section_header: str) -> set[str]:
    """Extract model names from a FIXTURES.md table section."""
    models: set[str] = set()
    in_section = False
    header_rows = 0
    for line in content.splitlines():
        if section_header in line:
            in_section = True
            header_rows = 0
            continue
        if line.startswith("## ") and in_section:
            break
        if in_section and line.startswith("|"):
            header_rows += 1
            if header_rows <= 2:
                # Skip table header row and separator row
                continue
            match = re.match(
                r"\|\s*\S+.*?\|\s*\w+\s*\|\s*(\w+)\s*\|", line
            )
            if match:
                models.add(match.group(1))
    return models


class TestFixtureCoverage:
    def test_fixtures_md_exists(self):
        assert FIXTURES_MD.exists(), "FIXTURES.md not found at repository root"

    def test_all_fixture_files_tracked(self):
        """Every fixture file on disk must appear in FIXTURES.md."""
        all_files = {p.stem for p in FIXTURES_DIR.glob("*.json")}
        content = FIXTURES_MD.read_text()
        captured = _extract_models_from_section(content, "## Captured Fixtures")
        pending = _extract_models_from_section(content, "## Pending Fixtures")
        needs_data = _extract_models_from_section(content, "## Needs Request Data")
        tracked = captured | pending | needs_data
        untracked = all_files - tracked
        assert not untracked, (
            f"Fixture files not tracked in FIXTURES.md: {untracked}"
        )

    def test_captured_fixtures_exist_on_disk(self):
        """Every 'captured' entry in FIXTURES.md must have a file."""
        content = FIXTURES_MD.read_text()
        captured = _extract_models_from_section(content, "## Captured Fixtures")
        all_files = {p.stem for p in FIXTURES_DIR.glob("*.json")}
        missing = captured - all_files
        assert not missing, (
            f"FIXTURES.md lists as captured but file missing: {missing}"
        )

    def test_pending_fixtures_do_not_exist_on_disk(self):
        """Pending entries should NOT have fixture files (they need capture)."""
        content = FIXTURES_MD.read_text()
        pending = _extract_models_from_section(content, "## Pending Fixtures")
        all_files = {p.stem for p in FIXTURES_DIR.glob("*.json")}
        present = pending & all_files
        if present:
            # Fixture was captured but FIXTURES.md not updated — warn
            assert not present, (
                f"Fixtures exist on disk but still listed as pending in "
                f"FIXTURES.md — move to Captured section: {present}"
            )
