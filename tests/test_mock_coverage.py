"""Fixture coverage verification test.

Asserts every fixture file in tests/fixtures/ is tracked in
FIXTURES.md, and every captured entry in FIXTURES.md has a
corresponding fixture file on disk.

Supports both gate-column format (G1-G4 columns) and legacy format.
"""

from __future__ import annotations

import re
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / "fixtures"
FIXTURES_MD = Path(__file__).parent.parent / "FIXTURES.md"

_SECTION_RE = re.compile(r"^## (ACPortal|Catalog|ABC) Endpoints", re.IGNORECASE)


def _strip_list_wrapper(model: str) -> str:
    """Strip List[]/list[] wrappers from a model name."""
    if model.startswith("List[") and model.endswith("]"):
        return model[5:-1]
    if model.startswith("list[") and model.endswith("]"):
        return model[5:-1]
    return model


def _extract_from_gate_table(content: str) -> dict[str, set[str]]:
    """Extract response models from gate-column format FIXTURES.md.

    Returns dict with 'all', 'captured' (G2=PASS), 'pending' (G2=FAIL).
    """
    all_models: set[str] = set()
    captured: set[str] = set()
    pending: set[str] = set()

    in_table = False
    header_rows = 0

    for line in content.splitlines():
        if _SECTION_RE.match(line):
            in_table = True
            header_rows = 0
            continue
        if line.startswith("## ") and in_table:
            in_table = False
            continue
        if not in_table or not line.startswith("|"):
            continue
        if "---" in line or "Endpoint Path" in line:
            header_rows += 1
            continue
        if header_rows < 2:
            continue

        cells = [c.strip() for c in line.split("|")]
        cells = [c for c in cells if c != ""]
        if len(cells) < 9:
            continue

        resp_model = cells[3]
        if not resp_model or resp_model == "—":
            continue

        clean = _strip_list_wrapper(resp_model)
        # Skip non-model types
        if clean in ("str", "bytes", "dict", "bool", "int"):
            continue

        all_models.add(clean)

        g2 = cells[5]  # G2 column
        if g2 == "PASS":
            captured.add(clean)
        else:
            pending.add(clean)

    return {"all": all_models, "captured": captured, "pending": pending}


def _extract_models_from_section(content: str, section_header: str) -> set[str]:
    """Extract model names from a FIXTURES.md table section (legacy format)."""
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
                continue
            match = re.match(
                r"\|\s*\S+.*?\|\s*\w+\s*\|\s*(\w+)\s*\|", line
            )
            if match:
                models.add(match.group(1))
    return models


def _is_variant_tracked(filename: str, tracked: set[str]) -> bool:
    """Check if a fixture file is a variant of a tracked model.

    Handles naming like 'SellerExpandedDto_detail' as a variant of
    'SellerExpandedDto'.
    """
    return any(
        filename.startswith(model + "_") for model in tracked
    )


class TestFixtureCoverage:
    def test_fixtures_md_exists(self):
        assert FIXTURES_MD.exists(), "FIXTURES.md not found at repository root"

    def test_all_fixture_files_tracked(self):
        """Every fixture file on disk must appear in FIXTURES.md."""
        all_files = {p.stem for p in FIXTURES_DIR.glob("*.json")}
        content = FIXTURES_MD.read_text()

        gate_data = _extract_from_gate_table(content)
        if gate_data["all"]:
            tracked = gate_data["all"]
        else:
            captured = _extract_models_from_section(content, "## Captured Fixtures")
            pending = _extract_models_from_section(content, "## Pending Fixtures")
            needs_data = _extract_models_from_section(content, "## Needs Request Data")
            tracked = captured | pending | needs_data

        untracked = {
            f for f in all_files - tracked
            if not _is_variant_tracked(f, tracked)
        }
        assert not untracked, (
            f"Fixture files not tracked in FIXTURES.md: {untracked}"
        )

    def test_captured_fixtures_exist_on_disk(self):
        """Every 'captured' entry (G2=PASS) in FIXTURES.md must have a file."""
        content = FIXTURES_MD.read_text()
        gate_data = _extract_from_gate_table(content)
        if gate_data["captured"]:
            captured = gate_data["captured"]
        else:
            captured = _extract_models_from_section(content, "## Captured Fixtures")

        all_files = {p.stem for p in FIXTURES_DIR.glob("*.json")}
        missing = captured - all_files
        assert not missing, (
            f"FIXTURES.md lists as captured but file missing: {missing}"
        )

    def test_pending_fixtures_do_not_exist_on_disk(self):
        """Pending entries (G2=FAIL) should NOT have fixture files."""
        content = FIXTURES_MD.read_text()
        gate_data = _extract_from_gate_table(content)
        if gate_data["pending"]:
            pending = gate_data["pending"]
        else:
            pending = _extract_models_from_section(content, "## Pending Fixtures")

        all_files = {p.stem for p in FIXTURES_DIR.glob("*.json")}
        present = pending & all_files
        if present:
            assert not present, (
                f"Fixtures exist on disk but listed as pending (G2=FAIL) in "
                f"FIXTURES.md — run gate evaluation to update: {present}"
            )
