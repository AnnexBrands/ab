"""Generate FIXTURES.md from source artifacts with per-gate quality columns.

Reads the existing FIXTURES.md to extract endpoint rows and Notes,
syncs model names against Route definitions (the single source of truth),
evaluates all quality gates, and regenerates the file with per-gate
pass/fail columns. Status is "complete" only when all applicable gates pass.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

from ab.progress.gates import evaluate_endpoint_gates
from ab.progress.route_index import RouteInfo, index_all_routes_multi, normalize_path

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURES_MD = REPO_ROOT / "FIXTURES.md"

# Regex for table rows (not headers/separators)
_TABLE_ROW_RE = re.compile(r"^\|[^|]+\|")
_SECTION_RE = re.compile(r"^## (ACPortal|Catalog|ABC) Endpoints", re.IGNORECASE)


@dataclass
class SyncReport:
    """Summary of route-driven sync results."""

    matched: int = 0
    mismatches: list[str] = field(default_factory=list)
    new_endpoints: list[str] = field(default_factory=list)
    unmatched_rows: list[str] = field(default_factory=list)


def parse_existing_fixtures(path: Path | None = None) -> list[dict[str, str]]:
    """Parse existing FIXTURES.md into a list of endpoint dicts.

    Supports gate-column formats (10 or 11 cols) and legacy format (8 cols).
    G5 format: Path | Method | Req Model | Resp Model | G1 | G2 | G3 | G4 | G5 | Status | Notes
    G4 format: Path | Method | Req Model | Resp Model | G1 | G2 | G3 | G4 | Status | Notes
    Legacy format: Path | Method | Req Model | Req Fixture | Resp Model | Resp Fixture | Status | Notes
    """
    path = path or FIXTURES_MD
    if not path.exists():
        return []

    text = path.read_text()
    lines = text.splitlines()

    endpoints: list[dict[str, str]] = []
    in_table = False
    header_seen = False
    is_gate_format = False

    for line in lines:
        if _SECTION_RE.match(line):
            in_table = True
            header_seen = False
            continue
        if line.startswith("## ") and not _SECTION_RE.match(line):
            in_table = False
            header_seen = False
            continue
        if not in_table:
            continue
        if not _TABLE_ROW_RE.match(line):
            continue
        if "---" in line or "Endpoint Path" in line:
            header_seen = True
            # Detect gate-column format by checking for G1 header
            if "G1" in line and "G2" in line:
                is_gate_format = True
            continue
        # (is_gate_format covers both 10-col G4 and 11-col G5 layouts)
        if not header_seen:
            continue

        cells = [c.strip() for c in line.split("|")]
        cells = [c for c in cells if c != ""]

        if is_gate_format:
            # G5 format (11 cols): Path | Method | Req | Resp | G1 | G2 | G3 | G4 | G5 | Status | Notes
            # G4 format (10 cols): Path | Method | Req | Resp | G1 | G2 | G3 | G4 | Status | Notes
            if len(cells) < 9:
                continue
            # Status and Notes are always the last two columns
            endpoints.append({
                "endpoint_path": cells[0],
                "method": cells[1],
                "request_model": cells[2] if cells[2] != "—" else "",
                "response_model": cells[3] if cells[3] != "—" else "",
                "old_status": cells[-2] if len(cells) >= 2 else "",
                "notes": cells[-1] if len(cells) >= 1 else "",
            })
        else:
            # Legacy format: Path | Method | Req Model | Req Fixture | Resp Model | Resp Fixture | Status | Notes
            if len(cells) < 7:
                continue
            endpoints.append({
                "endpoint_path": cells[0],
                "method": cells[1],
                "request_model": cells[2] if cells[2] != "—" else "",
                "response_model": cells[4] if cells[4] != "—" else "",
                "old_status": cells[6],
                "notes": cells[7] if len(cells) > 7 else "",
            })

    return endpoints


def _sync_with_routes(
    endpoints: list[dict[str, str]],
) -> tuple[list[dict[str, str]], SyncReport]:
    """Sync parsed FIXTURES.md rows against Route definitions.

    Route definitions are the single source of truth for model names.
    This function:
    1. Matches each existing row to a Route by (normalized_path, method)
    2. Updates request_model, response_model, endpoint_path from Route
    3. Preserves notes and capture dates
    4. Appends any Routes not yet in FIXTURES.md
    5. Deduplicates rows that collapse to the same identity after sync
    """
    route_index = index_all_routes_multi()
    report = SyncReport()

    # Build case-insensitive fallback index
    ci_index: dict[tuple[str, str], list[RouteInfo]] = {}
    for key, infos in route_index.items():
        ci_key = (key[0].lower(), key[1])
        ci_index.setdefault(ci_key, []).extend(infos)

    # Track which route-infos have been consumed by existing rows.
    # Key: (normalized_path, method), Value: set of consumed response_models
    consumed: dict[tuple[str, str], set[str | None]] = {}

    synced: list[dict[str, str]] = []

    for ep in endpoints:
        norm_key = (normalize_path(ep["endpoint_path"]), ep["method"])
        route_infos = route_index.get(norm_key)

        # Case-insensitive fallback
        if not route_infos:
            ci_key = (norm_key[0].lower(), norm_key[1])
            route_infos = ci_index.get(ci_key)

        if not route_infos:
            # No matching Route — keep row, flag it
            report.unmatched_rows.append(
                f"{ep['method']} {ep['endpoint_path']} — no matching Route"
            )
            synced.append(ep)
            continue

        # Try to find the best matching route for this row
        matched_route = _match_route_for_row(ep, route_infos)

        # Track consumption using Route's canonical key (not FIXTURES.md key)
        route_norm_key = (normalize_path(matched_route.path), matched_route.method)
        consumed.setdefault(route_norm_key, set()).add(
            matched_route.response_model
        )

        # Detect and log mismatches before overwriting
        changes: list[str] = []
        if ep["endpoint_path"] != matched_route.path:
            changes.append(f"path: {ep['endpoint_path']} → {matched_route.path}")
        old_req = ep.get("request_model", "") or None
        if old_req != matched_route.request_model:
            changes.append(
                f"req_model: {old_req or '—'} → {matched_route.request_model or '—'}"
            )
        old_resp = ep.get("response_model", "") or None
        if old_resp != matched_route.response_model:
            changes.append(
                f"resp_model: {old_resp or '—'} → {matched_route.response_model or '—'}"
            )

        if changes:
            detail = ", ".join(changes)
            report.mismatches.append(
                f"UPDATED: {matched_route.method} {matched_route.path} ({detail})"
            )

        # Apply Route values (source of truth)
        ep["endpoint_path"] = matched_route.path
        ep["request_model"] = matched_route.request_model or ""
        ep["response_model"] = matched_route.response_model or ""

        report.matched += 1
        synced.append(ep)

    # Append Routes not yet represented in FIXTURES.md
    for norm_key, route_infos in route_index.items():
        consumed_models = consumed.get(norm_key, set())
        for ri in route_infos:
            if ri.response_model not in consumed_models:
                report.new_endpoints.append(
                    f"NEW: {ri.method} {ri.path}"
                    f" ({ri.request_model or '—'} → {ri.response_model or '—'})"
                )
                synced.append({
                    "endpoint_path": ri.path,
                    "method": ri.method,
                    "request_model": ri.request_model or "",
                    "response_model": ri.response_model or "",
                    "old_status": "",
                    "notes": "auto-discovered",
                })

    # Deduplicate rows that now share (path, method, response_model)
    synced = _deduplicate(synced)

    return synced, report


def _match_route_for_row(
    ep: dict[str, str],
    route_infos: list[RouteInfo],
) -> RouteInfo:
    """Pick the best matching RouteInfo for a FIXTURES.md row.

    Prefers an exact response_model match; falls back to first available.
    """
    ep_resp = ep.get("response_model", "") or None
    # Exact match on response_model
    for ri in route_infos:
        if ri.response_model == ep_resp:
            return ri
    # Fallback: first route
    return route_infos[0]


def _deduplicate(endpoints: list[dict[str, str]]) -> list[dict[str, str]]:
    """Remove duplicate rows sharing (path, method, response_model).

    When duplicates exist, keep the row with the longest notes (most context).
    """
    seen: dict[tuple[str, str, str], int] = {}
    result: list[dict[str, str]] = []

    for ep in endpoints:
        key = (ep["endpoint_path"], ep["method"], ep.get("response_model", ""))
        if key in seen:
            # Keep the one with more notes
            existing_idx = seen[key]
            existing_notes = result[existing_idx].get("notes", "")
            new_notes = ep.get("notes", "")
            if len(new_notes) > len(existing_notes):
                result[existing_idx] = ep
            continue
        seen[key] = len(result)
        result.append(ep)

    return result


def _gate_badge(passed: bool) -> str:
    """Return a pass/fail badge string."""
    return "PASS" if passed else "FAIL"


def generate_fixtures_md(
    output_path: Path | None = None,
) -> tuple[str, SyncReport]:
    """Generate FIXTURES.md with per-gate quality columns.

    Returns:
        Tuple of (generated markdown content, route sync report).
    """
    output_path = output_path or FIXTURES_MD
    endpoints = parse_existing_fixtures()

    # Sync with Route definitions (source of truth for model names)
    endpoints, sync_report = _sync_with_routes(endpoints)

    if not endpoints:
        content = "# Fixture Tracking\n\nNo endpoints found.\n"
        try:
            output_path.write_text(content)
        except OSError as exc:
            logger.error("Failed to write %s: %s", output_path, exc)
            raise
        return content, sync_report

    # Evaluate gates for all endpoints (suppress noisy import warnings)
    prev_level = logging.root.level
    logging.root.setLevel(logging.ERROR)
    try:
        gate_results = []
        for ep in endpoints:
            resp_model = ep.get("response_model", "")
            status = evaluate_endpoint_gates(
                endpoint_path=ep["endpoint_path"],
                method=ep["method"],
                response_model=resp_model if resp_model else None,
                request_model=ep.get("request_model") or None,
                notes=ep.get("notes", ""),
            )
            gate_results.append((ep, status))
    finally:
        logging.root.setLevel(prev_level)

    # Compute summary stats
    total = len(gate_results)
    complete = sum(1 for _, s in gate_results if s.overall_status == "complete")
    g1_pass = sum(1 for _, s in gate_results if s.g1_model_fidelity and s.g1_model_fidelity.passed)
    g2_pass = sum(1 for _, s in gate_results if s.g2_fixture_status and s.g2_fixture_status.passed)
    g3_pass = sum(1 for _, s in gate_results if s.g3_test_quality and s.g3_test_quality.passed)
    g4_pass = sum(1 for _, s in gate_results if s.g4_doc_accuracy and s.g4_doc_accuracy.passed)
    g5_pass = sum(1 for _, s in gate_results if s.g5_param_routing and s.g5_param_routing.passed)
    g6_pass = sum(1 for _, s in gate_results if s.g6_request_quality and s.g6_request_quality.passed)

    # Build dotted-path lookup from endpoint class progress
    dotted_path_map: dict[tuple[str, str], str] = {}
    try:
        from ab.progress.route_index import build_endpoint_class_progress

        ecp_list = build_endpoint_class_progress()
        for ecp in ecp_list:
            for mp in ecp.helpers:
                if mp.http_path and mp.http_method:
                    dotted_path_map[(mp.http_path, mp.http_method)] = mp.dotted_path
            for methods in ecp.sub_groups.values():
                for mp in methods:
                    dotted_path_map[(mp.http_path, mp.http_method)] = mp.dotted_path
    except Exception:
        pass  # graceful fallback

    lines = [
        "# Fixture Tracking",
        "",
        "Tracks capture status and quality gates for all endpoint fixtures in `tests/fixtures/`.",
        "",
        "**Constitution**: v2.3.0, Principles I–V",
        "**Quality Gates**: G1 (Model Fidelity), G2 (Fixture Status), "
        "G3 (Test Quality), G4 (Doc Accuracy), G5 (Param Routing), G6 (Request Quality)",
        "**Rule**: Status is \"complete\" only when ALL applicable gates pass.",
        "",
        "## Summary",
        "",
        f"- **Total endpoints**: {total}",
        f"- **Complete (all gates pass)**: {complete}",
        f"- **G1 Model Fidelity**: {g1_pass}/{total} pass",
        f"- **G2 Fixture Status**: {g2_pass}/{total} pass",
        f"- **G3 Test Quality**: {g3_pass}/{total} pass",
        f"- **G4 Doc Accuracy**: {g4_pass}/{total} pass",
        f"- **G5 Param Routing**: {g5_pass}/{total} pass",
        f"- **G6 Request Quality**: {g6_pass}/{total} pass",
        "",
        "## Status Legend",
        "",
        "- **complete**: All applicable quality gates pass",
        "- **incomplete**: One or more gates fail",
        "- **PASS/FAIL**: Per-gate status",
        "",
        "## ACPortal Endpoints",
        "",
        "| Endpoint Path | Method | Python Path | Req Model | Resp Model "
        "| G1 | G2 | G3 | G4 | G5 | G6 | Status | Notes |",
        "|---------------|--------|-------------|-----------|------------"
        "|----|----|----|----|----|----|----|-------|",
    ]

    for ep, status in gate_results:
        g1 = _gate_badge(status.g1_model_fidelity.passed) if status.g1_model_fidelity else "—"
        g2 = _gate_badge(status.g2_fixture_status.passed) if status.g2_fixture_status else "—"
        g3 = _gate_badge(status.g3_test_quality.passed) if status.g3_test_quality else "—"
        g4 = _gate_badge(status.g4_doc_accuracy.passed) if status.g4_doc_accuracy else "—"
        g5 = _gate_badge(status.g5_param_routing.passed) if status.g5_param_routing else "—"
        g6 = _gate_badge(status.g6_request_quality.passed) if status.g6_request_quality else "—"

        req_model = ep.get("request_model", "") or "—"
        resp_model = ep.get("response_model", "") or "—"
        notes = ep.get("notes", "")
        dotted = dotted_path_map.get(
            (ep["endpoint_path"], ep["method"]), "—"
        )

        lines.append(
            f"| {ep['endpoint_path']} | {ep['method']} | {dotted} | {req_model} | {resp_model} "
            f"| {g1} | {g2} | {g3} | {g4} | {g5} | {g6} | {status.overall_status} | {notes} |"
        )

    # Add Model Warning Summary
    lines.extend([
        "",
        "## Model Warning Summary",
        "",
        "Models with `__pydantic_extra__` fields when validated against their fixtures:",
        "",
    ])

    # Collect models with G1 failures
    failed_models: dict[str, str] = {}
    for ep, status in gate_results:
        if (status.g1_model_fidelity
                and not status.g1_model_fidelity.passed
                and status.g1_model_fidelity.reason
                and "undeclared" in status.g1_model_fidelity.reason):
            model = ep.get("response_model", "")
            if model and model not in failed_models:
                failed_models[model] = status.g1_model_fidelity.reason

    if failed_models:
        lines.append("| Model | Issue |")
        lines.append("|-------|-------|")
        for model, reason in sorted(failed_models.items()):
            lines.append(f"| {model} | {reason} |")
    else:
        lines.append("No model warnings — all captured fixtures validate cleanly.")

    lines.append("")

    content = "\n".join(lines)
    try:
        output_path.write_text(content)
    except OSError as exc:
        logger.error("Failed to write %s: %s", output_path, exc)
        raise
    return content, sync_report
