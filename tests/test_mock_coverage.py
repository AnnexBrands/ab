"""Fixture coverage verification test.

Asserts every fixture file in tests/fixtures/ is tracked in
FIXTURES.md, and every captured entry in FIXTURES.md has a
corresponding fixture file on disk.

Supports both gate-column format (G1-G4 columns) and legacy format.
"""

from __future__ import annotations

import re
from pathlib import Path

from ab.progress.route_index import index_all_routes

FIXTURES_DIR = Path(__file__).parent / "fixtures"
MOCKS_DIR = FIXTURES_DIR / "mocks"
REQUESTS_DIR = FIXTURES_DIR / "requests"
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
    """Extract models from gate-column format FIXTURES.md.

    Column layout (0-indexed after splitting and filtering empties):
      0=Path, 1=Method, 2=PyPath, 3=ReqModel, 4=RespModel,
      5=G1, 6=G2, 7=G3, 8=G4, 9=G5, 10=G6, 11=Status, 12=Notes

    Returns dict with:
      'all'/'captured'/'pending' — response models (G2),
      'req_all'/'req_captured' — request models (G6).
    """
    all_models: set[str] = set()
    captured: set[str] = set()
    pending: set[str] = set()
    req_all: set[str] = set()
    req_captured: set[str] = set()

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
        if len(cells) < 11:
            continue

        req_model = cells[3]
        resp_model = cells[4]
        g2 = cells[6]
        g6 = cells[10]

        # Track response models
        if resp_model and resp_model != "—":
            clean = _strip_list_wrapper(resp_model)
            if clean not in ("str", "bytes", "dict", "bool"):
                all_models.add(clean)
                if g2 == "PASS":
                    captured.add(clean)
                else:
                    pending.add(clean)

        # Track request models
        if req_model and req_model != "—":
            clean_req = _strip_list_wrapper(req_model)
            req_all.add(clean_req)
            if g6 == "PASS":
                req_captured.add(clean_req)

    return {
        "all": all_models, "captured": captured, "pending": pending,
        "req_all": req_all, "req_captured": req_captured,
    }


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
        """Every fixture file on disk (live, mock, or request) must appear in FIXTURES.md."""
        resp_files = {p.stem for p in FIXTURES_DIR.glob("*.json")}
        if MOCKS_DIR.exists():
            resp_files |= {p.stem for p in MOCKS_DIR.glob("*.json")}
        req_files: set[str] = set()
        if REQUESTS_DIR.exists():
            req_files = {p.stem for p in REQUESTS_DIR.glob("*.json")}
        content = FIXTURES_MD.read_text()

        gate_data = _extract_from_gate_table(content)
        if gate_data["all"]:
            tracked_resp = gate_data["all"]
            # Request fixtures include request_model (body) and params_model
            # (query params). Route definitions are authoritative — FIXTURES.md
            # Req Model column may lag behind.
            routes = index_all_routes()
            route_req = {r.request_model for r in routes.values() if r.request_model}
            route_params = {r.params_model for r in routes.values() if r.params_model}
            tracked_req = gate_data["req_all"] | route_req | route_params
        else:
            captured = _extract_models_from_section(content, "## Captured Fixtures")
            pending = _extract_models_from_section(content, "## Pending Fixtures")
            needs_data = _extract_models_from_section(content, "## Needs Request Data")
            tracked_resp = captured | pending | needs_data
            tracked_req = set()

        untracked_resp = {
            f for f in resp_files - tracked_resp
            if not _is_variant_tracked(f, tracked_resp)
        }
        untracked_req = {
            f for f in req_files - tracked_req
            if not _is_variant_tracked(f, tracked_req)
        }
        untracked = untracked_resp | untracked_req
        assert not untracked, (
            f"Fixture files not tracked in FIXTURES.md: {untracked}"
        )

    def test_captured_fixtures_exist_on_disk(self):
        """Every 'captured' entry in FIXTURES.md must have a file on disk."""
        content = FIXTURES_MD.read_text()
        gate_data = _extract_from_gate_table(content)
        if gate_data["captured"]:
            resp_captured = gate_data["captured"]
            req_captured = gate_data.get("req_captured", set())
        else:
            resp_captured = _extract_models_from_section(content, "## Captured Fixtures")
            req_captured = set()

        resp_files = {p.stem for p in FIXTURES_DIR.glob("*.json")}
        if MOCKS_DIR.exists():
            resp_files |= {p.stem for p in MOCKS_DIR.glob("*.json")}
        req_files: set[str] = set()
        if REQUESTS_DIR.exists():
            req_files = {p.stem for p in REQUESTS_DIR.glob("*.json")}

        missing_resp = resp_captured - resp_files
        missing_req = req_captured - req_files
        missing = missing_resp | missing_req
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
        if MOCKS_DIR.exists():
            all_files |= {p.stem for p in MOCKS_DIR.glob("*.json")}
        present = pending & all_files
        if present:
            assert not present, (
                f"Fixtures exist on disk but listed as pending (G2=FAIL) in "
                f"FIXTURES.md — run gate evaluation to update: {present}"
            )
