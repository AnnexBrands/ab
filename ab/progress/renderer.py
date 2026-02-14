"""HTML renderer for progress report."""

from __future__ import annotations

from datetime import datetime, timezone
from html import escape
from itertools import groupby

from ab.progress.models import ActionItem, Constant, EndpointGroup, Fixture

CSS = """\
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
       max-width: 1100px; margin: 0 auto; padding: 20px; color: #1a1a1a;
       background: #fafafa; line-height: 1.5; }
h1 { font-size: 1.6rem; margin-bottom: 4px; }
.subtitle { color: #666; font-size: 0.85rem; margin-bottom: 24px; }
h2 { font-size: 1.25rem; margin: 28px 0 12px; border-bottom: 2px solid #e0e0e0;
     padding-bottom: 6px; }
h3 { font-size: 1.05rem; margin: 16px 0 8px; }
table { width: 100%; border-collapse: collapse; margin-bottom: 16px; }
th, td { padding: 8px 12px; text-align: left; border: 1px solid #ddd; font-size: 0.9rem; }
th { background: #f5f5f5; font-weight: 600; }
tr:hover { background: #f9f9f9; }
.done { background: #d4edda; color: #155724; }
.pending { background: #fff3cd; color: #856404; }
.not-started { background: #e9ecef; color: #495057; }
.env-blocked { background: #f8d7da; color: #721c24; }
.badge { display: inline-block; padding: 2px 8px; border-radius: 3px;
         font-size: 0.75rem; font-weight: 600; }
.badge-done { background: #28a745; color: #fff; }
.badge-pending { background: #ffc107; color: #333; }
.badge-ns { background: #6c757d; color: #fff; }
.badge-request { background: #17a2b8; color: #fff; }
.badge-constant { background: #fd7e14; color: #fff; }
details { margin: 6px 0; border: 1px solid #ddd; border-radius: 4px; }
details[open] { border-color: #aaa; }
summary { padding: 8px 12px; cursor: pointer; font-size: 0.9rem;
          background: #f8f9fa; border-radius: 4px; }
summary:hover { background: #e9ecef; }
.detail-body { padding: 8px 16px 12px; }
.endpoint-row { display: flex; align-items: center; gap: 8px; padding: 4px 0;
                border-bottom: 1px solid #f0f0f0; font-size: 0.85rem; }
.endpoint-row:last-child { border-bottom: none; }
.ep-method { font-weight: 600; min-width: 55px; font-family: monospace; }
.ep-path { font-family: monospace; flex: 1; }
.ep-model { color: #666; font-size: 0.8rem; }
ol.instructions { margin: 4px 0 8px 20px; font-size: 0.83rem; }
ol.instructions li { margin-bottom: 3px; }
code { background: #f0f0f0; padding: 1px 4px; border-radius: 2px;
       font-size: 0.85em; }
.tier-header { font-size: 1.1rem; margin: 20px 0 8px; color: #333; }
.totals-row { font-weight: 700; background: #f0f0f0 !important; }
.progress-bar { height: 18px; background: #e9ecef; border-radius: 3px;
                overflow: hidden; display: flex; }
.progress-bar .seg-done { background: #28a745; }
.progress-bar .seg-pending { background: #ffc107; }
.progress-bar .seg-ns { background: #6c757d; }
"""


def render_report(
    groups: list[EndpointGroup],
    fixtures: list[Fixture],
    constants: list[Constant],
    fixture_files: set[str],
    action_items: list[ActionItem],
) -> str:
    """Render the complete progress report as self-contained HTML."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    parts = [
        "<!DOCTYPE html>",
        "<html lang='en'>",
        "<head>",
        "<meta charset='utf-8'>",
        "<meta name='viewport' content='width=device-width, initial-scale=1'>",
        "<title>ABConnect SDK — Progress Report</title>",
        f"<style>{CSS}</style>",
        "</head>",
        "<body>",
        "<h1>ABConnect SDK — Progress Report</h1>",
        f"<p class='subtitle'>Generated {now}</p>",
        render_summary(groups),
        render_action_required(action_items),
        "</body>",
        "</html>",
    ]
    return "\n".join(parts)


def render_summary(groups: list[EndpointGroup]) -> str:
    """Render the coverage summary table."""
    # Aggregate by surface
    surface_data: dict[str, dict[str, int]] = {}
    for g in groups:
        s = g.api_surface
        if s not in surface_data:
            surface_data[s] = {"total": 0, "done": 0, "pending": 0, "not_started": 0}
        surface_data[s]["total"] += g.total
        surface_data[s]["done"] += g.done
        surface_data[s]["pending"] += g.pending
        surface_data[s]["not_started"] += g.not_started

    rows = []
    grand = {"total": 0, "done": 0, "pending": 0, "not_started": 0}

    for surface in ("ACPortal", "Catalog", "ABC"):
        d = surface_data.get(surface, {"total": 0, "done": 0, "pending": 0, "not_started": 0})
        grand["total"] += d["total"]
        grand["done"] += d["done"]
        grand["pending"] += d["pending"]
        grand["not_started"] += d["not_started"]

        pct = f"{d['done'] / d['total'] * 100:.0f}%" if d["total"] > 0 else "—"
        bar = _progress_bar(d) if d["total"] > 0 else "<em>Not individually listed</em>"

        rows.append(
            f"<tr>"
            f"<td><strong>{escape(surface)}</strong></td>"
            f"<td>{d['total']}</td>"
            f"<td class='done'>{d['done']}</td>"
            f"<td class='pending'>{d['pending']}</td>"
            f"<td class='not-started'>{d['not_started']}</td>"
            f"<td>{pct}</td>"
            f"<td>{bar}</td>"
            f"</tr>"
        )

    pct = f"{grand['done'] / grand['total'] * 100:.0f}%" if grand["total"] > 0 else "—"
    bar = _progress_bar(grand) if grand["total"] > 0 else ""

    rows.append(
        f"<tr class='totals-row'>"
        f"<td>Total</td>"
        f"<td>{grand['total']}</td>"
        f"<td class='done'>{grand['done']}</td>"
        f"<td class='pending'>{grand['pending']}</td>"
        f"<td class='not-started'>{grand['not_started']}</td>"
        f"<td>{pct}</td>"
        f"<td>{bar}</td>"
        f"</tr>"
    )

    return (
        "<h2>Coverage Summary</h2>"
        "<table>"
        "<tr><th>API Surface</th><th>Total</th><th>Done</th>"
        "<th>Pending</th><th>Not Started</th><th>%</th><th>Progress</th></tr>"
        + "\n".join(rows)
        + "</table>"
    )


def _progress_bar(d: dict[str, int]) -> str:
    """Render a CSS progress bar from counts."""
    total = d["total"]
    if total == 0:
        return ""
    done_pct = d["done"] / total * 100
    pending_pct = d["pending"] / total * 100
    ns_pct = d["not_started"] / total * 100
    return (
        f"<div class='progress-bar'>"
        f"<div class='seg-done' style='width:{done_pct:.1f}%'></div>"
        f"<div class='seg-pending' style='width:{pending_pct:.1f}%'></div>"
        f"<div class='seg-ns' style='width:{ns_pct:.1f}%'></div>"
        f"</div>"
    )


def render_action_required(action_items: list[ActionItem]) -> str:
    """Render the Action Required section with tiered grouping."""
    if not action_items:
        return "<h2>Action Required</h2><p>No action items — all endpoints are done!</p>"

    tier1 = [i for i in action_items if i.tier == 1]
    tier2 = [i for i in action_items if i.tier == 2]

    parts = ["<h2>Action Required</h2>"]

    if tier1:
        parts.append(
            f"<p class='tier-header'>"
            f"<span class='badge badge-pending'>Tier 1</span> "
            f"Scaffolded — needs correct request data "
            f"({len(tier1)} endpoints)</p>"
        )
        parts.append(_render_tier_groups(tier1))

    if tier2:
        parts.append(
            f"<p class='tier-header'>"
            f"<span class='badge badge-ns'>Tier 2</span> "
            f"Not started — needs implementation "
            f"({len(tier2)} endpoints)</p>"
        )
        parts.append(_render_tier_groups(tier2))

    return "\n".join(parts)


def _render_tier_groups(items: list[ActionItem]) -> str:
    """Render action items grouped by endpoint group as collapsible details."""
    parts = []
    sorted_items = sorted(items, key=lambda i: i.endpoint.group_name)

    for group_name, group_items_iter in groupby(
        sorted_items, key=lambda i: i.endpoint.group_name
    ):
        group_items = list(group_items_iter)
        blocker_counts = _blocker_summary(group_items)

        parts.append(
            f"<details>"
            f"<summary>"
            f"<strong>{escape(group_name)}</strong> — "
            f"{len(group_items)} endpoints "
            f"{blocker_counts}"
            f"</summary>"
            f"<div class='detail-body'>"
        )

        for item in group_items:
            parts.append(_render_action_item(item))

        parts.append("</div></details>")

    return "\n".join(parts)


def _render_action_item(item: ActionItem) -> str:
    """Render a single action item with instructions."""
    ep = item.endpoint
    badge = _blocker_badge(item.blocker_type)

    parts = [
        f"<div class='endpoint-row'>",
        f"<span class='ep-method'>{escape(ep.method)}</span>",
        f"<span class='ep-path'>{escape(ep.path)}</span>",
        f"<span class='ep-model'>{escape(ep.response_model)}</span>",
        f"{badge}",
        f"</div>",
    ]

    if item.instructions:
        parts.append("<ol class='instructions'>")
        for step in item.instructions:
            parts.append(f"<li>{step}</li>")
        parts.append("</ol>")

    return "\n".join(parts)


def _blocker_badge(blocker_type: str) -> str:
    """Render a badge for the blocker type."""
    labels = {
        "needs_request_data": ("Needs Request Data", "badge-request"),
        "constant_needed": ("Needs Constant", "badge-constant"),
        "not_implemented": ("Not Started", "badge-ns"),
    }
    label, cls = labels.get(blocker_type, ("Unknown", "badge-ns"))
    return f"<span class='badge {cls}'>{label}</span>"


def _blocker_summary(items: list[ActionItem]) -> str:
    """Summarize blocker types for a group."""
    counts: dict[str, int] = {}
    for item in items:
        counts[item.blocker_type] = counts.get(item.blocker_type, 0) + 1

    parts = []
    for bt, count in sorted(counts.items()):
        badge = _blocker_badge(bt)
        parts.append(f"{badge}&nbsp;{count}")

    return " ".join(parts)
