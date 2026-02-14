"""Mock coverage verification test (T111).

Asserts every fixture file in tests/fixtures/ is either:
(a) tested by a @pytest.mark.live test, or
(b) listed in MOCKS.md with status.
"""

from __future__ import annotations

import re
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / "fixtures"
MOCKS_MD = Path(__file__).parent.parent / "MOCKS.md"

# Fixtures known to be captured from live API
LIVE_FIXTURES = {
    "CompanySimple",
    "CompanyDetails",
    "ContactSimple",
    "ContactDetailedInfo",
    "ContactPrimaryDetails",
    "SearchContactEntityResult",
    "ContactTypeEntity",
    "CountryCodeDto",
    "JobStatus",
    "SellerExpandedDto",
    "User",
    "UserRole",
}


class TestMockCoverage:
    def test_all_fixtures_accounted_for(self):
        """Every fixture file must be live or tracked in MOCKS.md."""
        all_fixtures = {
            p.stem for p in FIXTURES_DIR.glob("*.json")
        }
        mocks_content = MOCKS_MD.read_text()

        # Extract model names from MOCKS.md table rows
        tracked_mocks = set()
        for line in mocks_content.splitlines():
            match = re.match(r"\|\s*\S+.*?\|\s*\w+\s*\|\s*(\w+)\s*\|", line)
            if match:
                tracked_mocks.add(match.group(1))

        accounted = LIVE_FIXTURES | tracked_mocks
        untracked = all_fixtures - accounted

        assert not untracked, (
            f"Untracked fixtures (not live and not in MOCKS.md): {untracked}"
        )

    def test_no_phantom_mocks(self):
        """Every entry in MOCKS.md mock table should have a fixture file."""
        all_fixtures = {
            p.stem for p in FIXTURES_DIR.glob("*.json")
        }
        mocks_content = MOCKS_MD.read_text()

        # Only check mock section entries
        in_mock_section = False
        phantom = set()
        for line in mocks_content.splitlines():
            if "## Mock Fixtures" in line:
                in_mock_section = True
                continue
            if line.startswith("## ") and in_mock_section:
                break
            if in_mock_section:
                match = re.match(r"\|\s*\S+.*?\|\s*\w+\s*\|\s*(\w+)\s*\|", line)
                if match:
                    name = match.group(1)
                    if name not in all_fixtures and name not in ("Model", "Name", "Date"):
                        phantom.add(name)

        assert not phantom, (
            f"MOCKS.md references fixtures that don't exist: {phantom}"
        )

    def test_mocks_md_exists(self):
        assert MOCKS_MD.exists(), "MOCKS.md not found at repository root"
