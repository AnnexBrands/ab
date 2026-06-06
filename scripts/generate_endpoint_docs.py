#!/usr/bin/env python3
"""Per-endpoint documentation generator and docstring footer sync.

This tool has two jobs, both driven by live route introspection (no
hand-maintained lists), scoped to the endpoint groups named in
``TOP_GROUPS`` (every route-backed top-level group):

1. **Per-endpoint Sphinx pages** — one ``docs/api/<top>/<slug>.md`` page per
   route-backed method, rendering the HTTP line, the Python signature, the
   CLI invocation, the human docstring prose, and request/response model
   field tables. This is the "friendly Sphinx page" a method's ``help()``
   footer links to.

2. **Docstring ``Docs:`` footers** — appends (idempotently) the RTD page URL
   plus request/response/query model names to each route-backed method's
   docstring, so ``help(api.jobs.transfer)`` surfaces the link. The footer
   text comes from :mod:`ab.api.rtd` (shared with the verification test).

It also backfills ``"Deprecated. Use api.jobs.X(...)."`` docstrings onto the
``forms``/``payments``/``shipments`` deprecation shims that never got one.

Usage::

    python scripts/generate_endpoint_docs.py --pages            # write pages
    python scripts/generate_endpoint_docs.py --check            # pages freshness gate
    python scripts/generate_endpoint_docs.py --sync-docstrings  # (re)apply footers + backfill
    python scripts/generate_endpoint_docs.py --check-docstrings # footers/backfill freshness gate

Source surgery operates on the *source text* of each docstring literal
(never decode/re-encode), so existing prose and escapes stay byte-identical.
"""

from __future__ import annotations

import ast
import inspect
import re
import sys
import types
import typing
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from ab.api import rtd  # noqa: E402
from ab.cli.discovery import discover_endpoints_from_class  # noqa: E402

# Top-level endpoint groups whose route-backed methods get pages + footers.
# This is every group that exposes at least one route-backed method; the
# ``forms``/``payments`` pure deprecation-shim groups are intentionally absent
# (no route-backed methods -> no pages). Completeness is enforced by
# ``tests/unit/test_docstring_rtd_links.py`` (``test_top_groups_cover_every_routed_group``)
# so a new endpoint group cannot silently ship without help()->RTD docs.
TOP_GROUPS = [
    "address",
    "autoprice",
    "catalog",
    "commodities",
    "commodity_maps",
    "companies",
    "contacts",
    "dashboard",
    "documents",
    "jobs",
    "lookup",
    "lots",
    "notes",
    "partners",
    "reports",
    "rfq",
    "sellers",
    "shipments",
    "users",
    "views",
    "web2lead",
]

DOCS_API = REPO_ROOT / "docs" / "api"

# Deprecation shims that ship without a docstring. The canonical target is
# read from each method's ``_deprecated(...)`` call, so the backfilled text is
# always accurate. (Group, method) -> source is introspected; we only need the
# set of classes to scan.
_BACKFILL_GROUPS = ["forms", "payments", "shipments"]


# ---------------------------------------------------------------------------
# Inventory
# ---------------------------------------------------------------------------


@dataclass
class Entry:
    group: str          # discovery group name, e.g. "jobs" or "jobs.timeline"
    method: str         # python method name
    cls: type
    func: object
    route: object       # ab.api.route.Route
    method_info: object # ab.cli.discovery.MethodInfo


def _iter_routed(top_groups: list[str]):
    """Yield Entry for every route-backed method in the given top groups."""
    eps = discover_endpoints_from_class()
    for group in sorted(eps):
        if rtd.endpoint_top_group(group) not in top_groups:
            continue
        info = eps[group]
        cls = info.endpoint_class
        for m in info.methods:
            if m.route is None:
                continue
            func = getattr(cls, m.name, None)
            if func is None:
                continue
            yield Entry(group=group, method=m.name, cls=cls, func=func, route=m.route, method_info=m)


# ---------------------------------------------------------------------------
# Annotation / model rendering
# ---------------------------------------------------------------------------


def _annotation_str(ann) -> str:
    if ann is None or ann is type(None):
        return "None"
    origin = typing.get_origin(ann)
    args = typing.get_args(ann)
    if origin is None:
        return getattr(ann, "__name__", str(ann).replace("typing.", ""))
    if origin is typing.Union or origin is getattr(types, "UnionType", object()):
        non_none = [a for a in args if a is not type(None)]
        inner = " | ".join(_annotation_str(a) for a in non_none)
        if any(a is type(None) for a in args):
            return f"Optional[{inner}]" if len(non_none) == 1 else f"{inner} | None"
        return inner
    if origin in (list, typing.List):
        return f"list[{_annotation_str(args[0])}]" if args else "list"
    if origin in (dict, typing.Dict):
        return f"dict[{_annotation_str(args[0])}, {_annotation_str(args[1])}]" if args else "dict"
    name = getattr(origin, "__name__", str(origin))
    return f"{name}[{', '.join(_annotation_str(a) for a in args)}]" if args else name


def _resolve_model(name: str | None):
    if not rtd.is_model_type(name):
        return None
    from ab.api import models

    inner = name[len("List[") : -1] if name.startswith("List[") else name
    return getattr(models, inner, None)


def _model_field_table(model_cls) -> list[str]:
    """Render a pydantic model's fields as a Markdown table."""
    fields = getattr(model_cls, "model_fields", None)
    if not fields:
        return ["_No documented fields._", ""]
    rows = ["| Field | Type | Required | Description |", "|---|---|---|---|"]
    for fname, field in fields.items():
        wire = field.alias or fname
        typ = _annotation_str(field.annotation)
        req = "yes" if field.is_required() else "no"
        desc = (field.description or "").replace("\n", " ").replace("|", "\\|")
        rows.append(f"| `{wire}` | `{typ}` | {req} | {desc} |")
    rows.append("")
    return rows


# ---------------------------------------------------------------------------
# Page rendering
# ---------------------------------------------------------------------------

_SURFACE = {"acportal": "ACPortal", "abc": "ABC", "catalog": "Catalog"}


def _prose(func) -> str:
    """The human docstring, with any generated footer block removed."""
    doc = inspect.getdoc(func) or ""
    return rtd.strip_footer_block(doc).strip()


def _cli_syntax(entry: Entry) -> str:
    parts = ["ab", *entry.group.split(".")]
    parts.append(entry.method)
    for p in entry.method_info.positional_params:
        parts.append(f"<{p.name}>")
    for p in entry.method_info.keyword_params:
        parts.append(f"[{p.cli_name} ...]")
    return " ".join(parts)


def _ann_text(ann) -> str:
    # Under ``from __future__ import annotations`` the SDK's annotations reach
    # us as source strings (e.g. ``"JobCreateRequest | dict"``); use them
    # verbatim. Anything already resolved is rendered structurally.
    return ann if isinstance(ann, str) else _annotation_str(ann)


def _py_signature(entry: Entry) -> str:
    empty = inspect.Parameter.empty
    try:
        sig = inspect.signature(entry.func)
    except (TypeError, ValueError):
        return f"api.{entry.group}.{entry.method}(...)"
    parts: list[str] = []
    star_emitted = False
    for name, p in sig.parameters.items():
        if name == "self":
            continue
        if p.kind == p.KEYWORD_ONLY and not star_emitted:
            parts.append("*")
            star_emitted = True
        if p.kind == p.VAR_POSITIONAL:
            star_emitted = True
            token = f"*{name}"
        elif p.kind == p.VAR_KEYWORD:
            token = f"**{name}"
        else:
            token = name
        if p.annotation is not empty:
            token += f": {_ann_text(p.annotation)}"
        if p.default is not empty:
            token += f" = {p.default!r}"
        parts.append(token)
    ret = ""
    if sig.return_annotation is not inspect.Signature.empty:
        ret = f" -> {_ann_text(sig.return_annotation)}"
    return f"api.{entry.group}.{entry.method}({', '.join(parts)}){ret}"


def render_page(entry: Entry) -> str:
    r = entry.route
    surface = _SURFACE.get(r.api_surface, r.api_surface)
    top = rtd.endpoint_top_group(entry.group)
    dotted = f"{entry.group}.{entry.method}"
    out: list[str] = []
    out.append("<!-- Generated by scripts/generate_endpoint_docs.py — do not edit by hand. -->")
    out.append(f"# `api.{dotted}`")
    out.append("")
    out.append(f"> `{r.method} {r.path}` — {surface}")
    out.append("")
    out.append("**Python**")
    out.append("")
    out.append("```python")
    out.append(_py_signature(entry))
    out.append("```")
    out.append("")
    out.append("**CLI**")
    out.append("")
    out.append("```bash")
    out.append(_cli_syntax(entry))
    out.append("```")
    out.append("")

    prose = _prose(entry.func)
    if prose:
        out.append(prose)
        out.append("")

    # Request model
    if rtd.is_model_type(r.request_model):
        out.append(f"## Request body — `{r.request_model}`")
        out.append("")
        model = _resolve_model(r.request_model)
        out += _model_field_table(model) if model is not None else ["_Model not introspectable._", ""]

    # Query params model
    if rtd.is_model_type(r.params_model):
        out.append(f"## Query parameters — `{r.params_model}`")
        out.append("")
        model = _resolve_model(r.params_model)
        out += _model_field_table(model) if model is not None else ["_Model not introspectable._", ""]

    # Response
    out.append("## Response")
    out.append("")
    if r.response_model is None:
        out.append("No response body.")
        out.append("")
    elif not rtd.is_model_type(r.response_model):
        out.append(f"Returns `{r.response_model}`.")
        out.append("")
    else:
        is_list = r.response_model.startswith("List[")
        out.append(f"Returns {'a list of ' if is_list else ''}`{r.response_model}`.")
        out.append("")
        model = _resolve_model(r.response_model)
        out += _model_field_table(model) if model is not None else ["_Model not introspectable._", ""]

    out.append("---")
    out.append("")
    out.append(f"[← Back to api.{top}](../{top}.md)")
    out.append("")
    return "\n".join(out)


def _page_path(entry: Entry) -> Path:
    top = rtd.endpoint_top_group(entry.group)
    slug = rtd.endpoint_page_slug(entry.group, entry.method)
    return DOCS_API / top / f"{slug}.md"


def _expected_pages() -> dict[Path, str]:
    return {_page_path(e): render_page(e) for e in _iter_routed(TOP_GROUPS)}


def write_pages() -> int:
    pages = _expected_pages()
    for path in sorted(pages):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(pages[path], encoding="utf-8")
    print(f"Wrote {len(pages)} per-endpoint page(s) under {DOCS_API.relative_to(REPO_ROOT)}/")
    return 0


def check_pages() -> list[str]:
    """Return a list of human-readable staleness problems (empty == fresh)."""
    problems: list[str] = []
    expected = _expected_pages()
    for path, content in sorted(expected.items()):
        rel = path.relative_to(REPO_ROOT)
        if not path.exists():
            problems.append(f"missing: {rel}")
        elif path.read_text(encoding="utf-8") != content:
            problems.append(f"stale:   {rel}")
    # Orphan pages (generated dir entries no longer backed by a route)
    expected_set = set(expected)
    for top in TOP_GROUPS:
        d = DOCS_API / top
        if d.is_dir():
            for f in d.glob("*.md"):
                if f not in expected_set:
                    problems.append(f"orphan:  {f.relative_to(REPO_ROOT)}")
    return problems


# ---------------------------------------------------------------------------
# Docstring source surgery
# ---------------------------------------------------------------------------


def _index(src: str) -> tuple[list[str], list[int]]:
    """Return (lines-with-endings, char-offset-of-each-line-start)."""
    lines = src.splitlines(keepends=True)
    starts = [0]
    for line in lines:
        starts.append(starts[-1] + len(line))
    return lines, starts


def _abs(lines: list[str], starts: list[int], lineno: int, byte_col: int) -> int:
    """Convert a (1-based line, UTF-8 *byte* column) AST position to a char index.

    Python's ``ast`` reports ``col_offset``/``end_col_offset`` as UTF-8 byte
    offsets, not character offsets — so a docstring line containing a
    multi-byte character (e.g. an em-dash) would otherwise mis-slice. We
    convert the byte column to a character column against the line's own bytes
    (AST positions always fall on character boundaries).
    """
    line = lines[lineno - 1]
    char_col = len(line.encode("utf-8")[:byte_col].decode("utf-8"))
    return starts[lineno - 1] + char_col


def _find_func(tree: ast.AST, qualname: str, name: str):
    """Locate a FunctionDef by class.method qualname within a parsed module."""
    cls_name = qualname.split(".")[-2] if "." in qualname else None
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and (cls_name is None or node.name == cls_name):
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == name:
                    return item
    return None


def _docstring_node(func_node) -> ast.Constant | None:
    if func_node.body and isinstance(func_node.body[0], ast.Expr):
        val = func_node.body[0].value
        if isinstance(val, ast.Constant) and isinstance(val.value, str):
            return val
    return None


def _footer_block(entry: Entry, indent: str) -> str:
    lines = rtd.docstring_footer_lines(
        entry.group,
        entry.method,
        request_model=entry.route.request_model,
        params_model=entry.route.params_model,
        response_model=entry.route.response_model,
    )
    # Guard the ruff line-length limit at generation time, using the *real*
    # docstring indentation — a too-long footer would otherwise only surface as
    # a downstream ruff failure (or slip past a test that assumes 8-space indent).
    for line in lines:
        if len(indent) + len(line) > 120:
            raise ValueError(
                f"{entry.group}.{entry.method}: footer line exceeds 120 cols "
                f"({len(indent) + len(line)}): {line!r}"
            )
    return "\n\n" + "\n".join(indent + line for line in lines) + "\n" + indent


def _rewrite_docstring_literal(src: str, doc_node: ast.Constant, footer: str) -> tuple[int, int, str]:
    """Return (start, end, new_literal) replacing the docstring's quoted body.

    Operates on the literal's *source text* so prose/escapes are preserved.
    """
    lines, starts = _index(src)
    start = _abs(lines, starts, doc_node.lineno, doc_node.col_offset)
    end = _abs(lines, starts, doc_node.end_lineno, doc_node.end_col_offset)
    seg = src[start:end]
    # Robustly split off any string prefix (r/b/f...) and opening quote, which
    # may be triple (""") or single ("). A one-line docstring promoted to a
    # multi-line one must use a triple quote so the footer's newlines are legal.
    m = re.match(r"""^[A-Za-z]*('''|\"\"\"|'|")""", seg)
    open_tok = m.group(0)
    quote = m.group(1)
    prefix = open_tok[: -len(quote)]
    body = seg[len(open_tok) : -len(quote)]
    # Strip any prior generated footer (trailing block only) for idempotency.
    body = rtd.strip_footer_block(body)
    new_body = body.rstrip() + footer
    triple = quote * 3 if len(quote) == 1 else quote
    return start, end, f"{prefix}{triple}{new_body}{triple}"


def _insert_docstring(src: str, func_node, text: str) -> tuple[int, int, str]:
    """Insert a brand-new one-line docstring as the first body statement."""
    first = func_node.body[0]
    indent = " " * first.col_offset
    _, starts = _index(src)
    line_start = starts[first.lineno - 1]
    literal = f'{indent}"""{text}"""\n'
    return line_start, line_start, literal


# How each shim module encodes the canonical target in its ``_deprecated(...)``
# call: (prefix, arg-index, expected-arg-count). forms/shipments pass (old, new);
# payments passes only the (unchanged) method name.
_BACKFILL_CANON = {
    "forms": ("", -1, 2),                        # 2nd arg is already the full path
    "payments": ("api.jobs.payment.", 0, 1),     # prefix + 1st arg
    "shipments": ("api.jobs.shipment.", -1, 2),  # prefix + 2nd arg
}


def _deprecation_target(func_node, group: str) -> str | None:
    """Read the canonical ``api.jobs.X.y`` target from a shim's _deprecated().

    Returns ``None`` (skip backfill, surfacing as an undocumented method rather
    than a silently wrong target) if the call's argument count doesn't match the
    group's known convention.
    """
    spec = _BACKFILL_CANON.get(group)
    if spec is None:
        return None
    prefix, idx, expected = spec
    for node in ast.walk(func_node):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "_deprecated":
            args = [a.value for a in node.args if isinstance(a, ast.Constant)]
            if len(args) != expected:
                return None
            return f"{prefix}{args[idx]}"
    return None


def _edits_for_file(path: Path, entries_footer: list[Entry], entries_backfill: list[Entry]):
    """Compute (start, end, text) edits for one source file."""
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    edits: list[tuple[int, int, str]] = []

    for e in entries_footer:
        fn = _find_func(tree, e.func.__qualname__, e.method)
        if fn is None:
            continue
        doc = _docstring_node(fn)
        if doc is None:
            continue
        indent = " " * doc.col_offset
        edits.append(_rewrite_docstring_literal(src, doc, _footer_block(e, indent)))

    for e in entries_backfill:
        fn = _find_func(tree, e.func.__qualname__, e.method)
        if fn is None or _docstring_node(fn) is not None:
            continue
        target = _deprecation_target(fn, e.group)
        if not target:
            continue
        text = f"Deprecated. Use ``{target}(...)``."
        edits.append(_insert_docstring(src, fn, text))

    return src, edits


def _apply(src: str, edits: list[tuple[int, int, str]]) -> str:
    for start, end, text in sorted(edits, key=lambda e: e[0], reverse=True):
        src = src[:start] + text + src[end:]
    return src


def _backfill_entries() -> list[Entry]:
    eps = discover_endpoints_from_class()
    out: list[Entry] = []
    for group in _BACKFILL_GROUPS:
        info = eps.get(group)
        if info is None:
            continue
        for m in info.methods:
            func = getattr(info.endpoint_class, m.name, None)
            if func is None or (inspect.getdoc(func) or "").strip():
                continue
            out.append(Entry(group, m.name, info.endpoint_class, func, m.route, m))
    return out


def _grouped_by_file():
    footer = list(_iter_routed(TOP_GROUPS))
    backfill = _backfill_entries()
    files: dict[Path, tuple[list[Entry], list[Entry]]] = {}
    for e in footer:
        files.setdefault(Path(inspect.getsourcefile(e.func)), ([], []))[0].append(e)
    for e in backfill:
        files.setdefault(Path(inspect.getsourcefile(e.func)), ([], []))[1].append(e)
    return files


def sync_docstrings() -> int:
    changed = 0
    for path, (footer, backfill) in _grouped_by_file().items():
        src, edits = _edits_for_file(path, footer, backfill)
        new = _apply(src, edits)
        if new != src:
            ast.parse(new)  # never write un-parseable source
            path.write_text(new, encoding="utf-8")
            changed += 1
            print(f"updated {path.relative_to(REPO_ROOT)} ({len(edits)} method(s))")
    print(f"Docstring sync complete: {changed} file(s) changed.")
    return 0


def check_docstrings() -> list[str]:
    """Return staleness problems for footers + backfill (empty == fresh)."""
    problems: list[str] = []
    for path, (footer, backfill) in _grouped_by_file().items():
        src, edits = _edits_for_file(path, footer, backfill)
        if _apply(src, edits) != src:
            problems.append(f"out-of-date docstrings: {path.relative_to(REPO_ROOT)}")
    return problems


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(argv: list[str]) -> int:
    if "--sync-docstrings" in argv:
        return sync_docstrings()
    if "--check-docstrings" in argv:
        problems = check_docstrings()
        if problems:
            print("Docstring footers are STALE:\n  " + "\n  ".join(problems), file=sys.stderr)
            print("Regenerate with: python scripts/generate_endpoint_docs.py --sync-docstrings", file=sys.stderr)
            return 1
        print("Docstring footers are current.")
        return 0
    if "--check" in argv:
        problems = check_pages()
        if problems:
            print("Per-endpoint pages are STALE:\n  " + "\n  ".join(problems), file=sys.stderr)
            print("Regenerate with: python scripts/generate_endpoint_docs.py --pages", file=sys.stderr)
            # --pages writes the expected set but never deletes; an orphan page
            # (its route was renamed/removed) must be removed by hand.
            if any(p.startswith("orphan:") for p in problems):
                print(
                    "Orphan pages are no longer route-backed and --pages cannot clear "
                    "them; remove each by hand: git rm <path>",
                    file=sys.stderr,
                )
            return 1
        print("Per-endpoint pages are current.")
        return 0
    if "--pages" in argv:
        return write_pages()
    print(__doc__)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
