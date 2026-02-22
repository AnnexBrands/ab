"""Generate FIXTURES.md from source artifacts with per-gate quality columns.

Reads the existing FIXTURES.md to extract endpoint rows and Notes,
evaluates all four quality gates, and regenerates the file with
per-gate pass/fail columns. Status is "complete" only when all
applicable gates pass.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

from ab.progress.gates import evaluate_endpoint_gates

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURES_MD = REPO_ROOT / "FIXTURES.md"

# Regex for table rows (not headers/separators)
_TABLE_ROW_RE = re.compile(r"^\|[^|]+\|")
_SECTION_RE = re.compile(r"^## (ACPortal|Catalog|ABC) Endpoints", re.IGNORECASE)


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


def _gate_badge(passed: bool) -> str:
    """Return a pass/fail badge string."""
    return "PASS" if passed else "FAIL"


def generate_fixtures_md(output_path: Path | None = None) -> str:
    """Generate FIXTURES.md with per-gate quality columns.

    Returns:
        The generated markdown content.
    """
    output_path = output_path or FIXTURES_MD
    endpoints = parse_existing_fixtures()

    if not endpoints:
        return "# Fixture Tracking\n\nNo endpoints found.\n"

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

    lines = [
        "# Fixture Tracking",
        "",
        "Tracks capture status and quality gates for all endpoint fixtures in `tests/fixtures/`.",
        "",
        "**Constitution**: v2.3.0, Principles I–V",
        "**Quality Gates**: G1 (Model Fidelity), G2 (Fixture Status), "
        "G3 (Test Quality), G4 (Doc Accuracy), G5 (Param Routing)",
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
        "",
        "## Status Legend",
        "",
        "- **complete**: All applicable quality gates pass",
        "- **incomplete**: One or more gates fail",
        "- **PASS/FAIL**: Per-gate status",
        "",
        "## ACPortal Endpoints",
        "",
        "| Endpoint Path | Method | Req Model | Resp Model | G1 | G2 | G3 | G4 | G5 | Status | Notes |",
        "|---------------|--------|-----------|------------|----|----|----|----|----|--------|-------|",
    ]

    for ep, status in gate_results:
        g1 = _gate_badge(status.g1_model_fidelity.passed) if status.g1_model_fidelity else "—"
        g2 = _gate_badge(status.g2_fixture_status.passed) if status.g2_fixture_status else "—"
        g3 = _gate_badge(status.g3_test_quality.passed) if status.g3_test_quality else "—"
        g4 = _gate_badge(status.g4_doc_accuracy.passed) if status.g4_doc_accuracy else "—"
        g5 = _gate_badge(status.g5_param_routing.passed) if status.g5_param_routing else "—"

        req_model = ep.get("request_model", "") or "—"
        resp_model = ep.get("response_model", "") or "—"
        notes = ep.get("notes", "")

        lines.append(
            f"| {ep['endpoint_path']} | {ep['method']} | {req_model} | {resp_model} "
            f"| {g1} | {g2} | {g3} | {g4} | {g5} | {status.overall_status} | {notes} |"
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
    return content
