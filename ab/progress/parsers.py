"""Markdown parsers for api-surface.md and FIXTURES.md."""

from __future__ import annotations

import re
from pathlib import Path

from ab.progress.models import Endpoint, EndpointGroup, Fixture

# --- api-surface.md parsing ---

_SURFACE_HEADER_RE = re.compile(r"^## Endpoint Groups — (ACPortal|Catalog|ABC)")
_GROUP_HEADER_RE = re.compile(r"^###+ (.+)")
_TABLE_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|")
_SUMMARY_TOTAL_RE = re.compile(r"\*\*Total\*\*:\s*(\d+)")
_SUMMARY_DONE_RE = re.compile(r"\*\*AB done\*\*:\s*(\d+)")
_AB_FILE_RE = re.compile(r"\*\*AB file\*\*:\s*`?([^`|]+?)`?\s*(?:\||$)")
_REF_FILE_RE = re.compile(
    r"\*\*ABConnectTools file\*\*:\s*`?([^`|]+(?:,\s*`[^`]+`)*)"
)
_PRIORITY_RE = re.compile(r"\*\*Priority\*\*:\s*(.+)")


def parse_api_surface(path: Path) -> list[EndpointGroup]:
    """Parse specs/api-surface.md into EndpointGroup objects."""
    text = path.read_text()
    lines = text.splitlines()

    groups: list[EndpointGroup] = []
    current_surface: str | None = None
    current_group: EndpointGroup | None = None

    for line in lines:
        # Detect API surface section
        m = _SURFACE_HEADER_RE.match(line)
        if m:
            current_surface = m.group(1)
            current_group = None
            continue

        # Any ## header that isn't a surface header ends the current surface
        if line.startswith("## ") and not _SURFACE_HEADER_RE.match(line):
            current_surface = None
            current_group = None
            continue

        # Skip lines outside a surface section
        if current_surface is None:
            continue

        # Detect group header (### or ####)
        m = _GROUP_HEADER_RE.match(line)
        if m:
            group_name = m.group(1).strip()
            current_group = EndpointGroup(
                name=group_name,
                api_surface=current_surface,
            )
            groups.append(current_group)
            continue

        if current_group is None:
            continue

        # Parse table rows
        m = _TABLE_ROW_RE.match(line)
        if m:
            ep = _parse_table_row(line, current_group)
            if ep:
                current_group.endpoints.append(ep)
            continue

        # Parse group metadata lines
        m = _AB_FILE_RE.search(line)
        if m:
            val = m.group(1).strip()
            if val and val != "—":
                current_group.ab_file = val

        m = _REF_FILE_RE.search(line)
        if m:
            current_group.ref_file = m.group(1).strip()

        m = _PRIORITY_RE.search(line)
        if m:
            current_group.priority = m.group(1).strip()

    # Recount and filter out empty groups (e.g. parent headers with no tables)
    for g in groups:
        g.recount()

    return [g for g in groups if g.total > 0]


def _parse_table_row(line: str, group: EndpointGroup) -> Endpoint | None:
    """Parse a single endpoint table row."""
    cells = [c.strip() for c in line.split("|")]
    # Remove empty strings from leading/trailing pipes
    cells = [c for c in cells if c]
    if len(cells) < 7:
        return None

    # Cells: #, Route Key, Method, Path, Response Model, AB, Ref
    try:
        index = int(cells[0])
    except (ValueError, IndexError):
        return None

    route_key = cells[1].strip()
    method = cells[2].strip()
    path = cells[3].strip()
    response_model = cells[4].strip()

    ab_raw = cells[5].strip() if len(cells) > 5 else "—"
    ref_raw = cells[6].strip() if len(cells) > 6 else "—"

    # Normalize status
    if ab_raw == "done":
        ab_status = "done"
    elif ab_raw == "pending":
        ab_status = "pending"
    else:
        ab_status = "not_started"

    # Normalize ref
    if ref_raw in ("JSON", "PDF"):
        ref_status = ref_raw
    else:
        ref_status = "none"

    return Endpoint(
        group_name=group.name,
        api_surface=group.api_surface,
        index=index,
        route_key=route_key,
        method=method,
        path=path,
        response_model=response_model,
        ab_status=ab_status,
        ref_status=ref_status,
    )


# --- FIXTURES.md parsing ---

# Legacy format sections
_CAPTURED_SECTION_RE = re.compile(r"^## Captured Fixtures", re.IGNORECASE)
_NEEDS_REQUEST_RE = re.compile(r"^## Needs Request Data", re.IGNORECASE)
_NEEDS_ACCESS_RE = re.compile(r"^## Needs Access", re.IGNORECASE)
# Unified 4D format sections
_SURFACE_SECTION_RE = re.compile(
    r"^## (ACPortal|Catalog|ABC) Endpoints", re.IGNORECASE
)
_FIXTURE_ROW_RE = re.compile(r"^\|[^|]+\|")


def parse_fixtures(path: Path) -> list[Fixture]:
    """Parse FIXTURES.md into Fixture objects.

    Supports both the legacy two-section format and the unified 4D format
    (feature 007). Auto-detects format by looking for surface-section headers.
    """
    text = path.read_text()
    lines = text.splitlines()

    # Detect format: unified 4D has "## ACPortal Endpoints" etc.
    is_unified = any(_SURFACE_SECTION_RE.match(line) for line in lines)

    if is_unified:
        return _parse_unified_fixtures(lines)
    return _parse_legacy_fixtures(lines)


def _parse_unified_fixtures(lines: list[str]) -> list[Fixture]:
    """Parse unified 4D FIXTURES.md format.

    Columns: Endpoint Path | Method | Req Model | Req Fixture | Resp Model | Resp Fixture | Status | Notes
    """
    fixtures: list[Fixture] = []
    in_table = False
    header_seen = False

    for line in lines:
        if _SURFACE_SECTION_RE.match(line):
            in_table = True
            header_seen = False
            continue
        if line.startswith("## ") and not _SURFACE_SECTION_RE.match(line):
            in_table = False
            header_seen = False
            continue

        if not in_table:
            continue
        if not _FIXTURE_ROW_RE.match(line):
            continue
        if "---" in line or "Endpoint Path" in line:
            header_seen = True
            continue
        if not header_seen:
            continue

        cells = [c.strip() for c in line.split("|")]
        cells = [c for c in cells if c != ""]

        f = _parse_unified_row(cells)
        if f:
            fixtures.append(f)

    return fixtures


def _parse_unified_row(cells: list[str]) -> Fixture | None:
    """Parse a unified 4D row.

    Columns: Endpoint Path | Method | Req Model | Req Fixture | Resp Model | Resp Fixture | Status | Notes
    """
    if len(cells) < 7:
        return None

    endpoint_path = cells[0]
    method = cells[1]
    req_model = cells[2] if cells[2] != "—" else None
    req_fixture = cells[3] if cells[3] != "—" else None
    resp_model = cells[4] if cells[4] != "—" else None
    resp_fixture = cells[5] if cells[5] != "—" else None
    status = cells[6]
    notes = cells[7] if len(cells) > 7 else None

    # Map unified status to legacy status for compatibility
    if status == "complete":
        legacy_status = "captured"
    elif status == "needs-request-data":
        legacy_status = "needs-request-data"
    else:
        legacy_status = "needs-request-data" if resp_fixture == "needs-data" else "captured"

    return Fixture(
        endpoint_path=endpoint_path,
        method=method,
        model_name=resp_model or "",
        status=legacy_status,
        blocker=notes,
        request_model=req_model,
        request_fixture_status=req_fixture,
    )


def _parse_legacy_fixtures(lines: list[str]) -> list[Fixture]:
    """Parse legacy two-section FIXTURES.md format."""
    fixtures: list[Fixture] = []
    section: str | None = None
    header_seen = False

    for line in lines:
        if _CAPTURED_SECTION_RE.match(line):
            section = "captured"
            header_seen = False
            continue
        if _NEEDS_REQUEST_RE.match(line):
            section = "needs-request-data"
            header_seen = False
            continue
        if _NEEDS_ACCESS_RE.match(line):
            section = "needs-access"
            header_seen = False
            continue
        if line.startswith("## "):
            section = None
            continue

        if section is None:
            continue
        if not _FIXTURE_ROW_RE.match(line):
            continue
        if "---" in line or "Endpoint Path" in line:
            header_seen = True
            continue
        if not header_seen:
            continue

        cells = [c.strip() for c in line.split("|")]
        cells = [c for c in cells if c != ""]

        if section == "captured":
            f = _parse_captured_row(cells)
        else:
            f = _parse_non_captured_row(cells, section)

        if f:
            fixtures.append(f)

    return fixtures


def _parse_captured_row(cells: list[str]) -> Fixture | None:
    """Parse a captured fixture row (legacy format).

    Columns: Endpoint Path | Method | Model Name | Date | Source | ABConnectTools Ref
    """
    if len(cells) < 5:
        return None
    return Fixture(
        endpoint_path=cells[0],
        method=cells[1],
        model_name=cells[2],
        status="captured",
        capture_date=cells[3] if len(cells) > 3 else None,
        source=cells[4] if len(cells) > 4 else None,
        ref=cells[5] if len(cells) > 5 and cells[5] != "—" else None,
    )


def _parse_non_captured_row(cells: list[str], status: str) -> Fixture | None:
    """Parse a needs-request-data or needs-access fixture row (legacy format).

    Columns: Endpoint Path | Method | Model Name | What's Missing or Access Required | ABConnectTools Ref
    """
    if len(cells) < 4:
        return None
    return Fixture(
        endpoint_path=cells[0],
        method=cells[1],
        model_name=cells[2],
        status=status,
        blocker=cells[3] if len(cells) > 3 else None,
        ref=cells[4] if len(cells) > 4 and cells[4] != "—" else None,
    )
