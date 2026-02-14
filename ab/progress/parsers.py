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

_CAPTURED_SECTION_RE = re.compile(r"^## Captured Fixtures", re.IGNORECASE)
_PENDING_SECTION_RE = re.compile(r"^## Pending Fixtures", re.IGNORECASE)
_FIXTURE_ROW_RE = re.compile(r"^\|[^|]+\|")


def parse_fixtures(path: Path) -> list[Fixture]:
    """Parse FIXTURES.md into Fixture objects."""
    text = path.read_text()
    lines = text.splitlines()

    fixtures: list[Fixture] = []
    section: str | None = None  # "captured" or "pending"
    header_seen = False

    for line in lines:
        if _CAPTURED_SECTION_RE.match(line):
            section = "captured"
            header_seen = False
            continue
        if _PENDING_SECTION_RE.match(line):
            section = "pending"
            header_seen = False
            continue

        if section is None:
            continue

        # Skip non-table lines
        if not _FIXTURE_ROW_RE.match(line):
            continue

        # Skip header row and separator
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
            f = _parse_pending_row(cells)

        if f:
            fixtures.append(f)

    return fixtures


def _parse_captured_row(cells: list[str]) -> Fixture | None:
    """Parse a captured fixture row.

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


def _parse_pending_row(cells: list[str]) -> Fixture | None:
    """Parse a pending fixture row.

    Columns: Endpoint Path | Method | Model Name | Capture Instructions | Blocker | ABConnectTools Ref
    """
    if len(cells) < 5:
        return None
    return Fixture(
        endpoint_path=cells[0],
        method=cells[1],
        model_name=cells[2],
        status="pending",
        capture_instructions=cells[3] if len(cells) > 3 else None,
        blocker=cells[4] if len(cells) > 4 else None,
        ref=cells[5] if len(cells) > 5 and cells[5] != "—" else None,
    )
