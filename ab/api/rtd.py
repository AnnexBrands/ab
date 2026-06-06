"""Read the Docs URL helpers — the single source of truth for doc links.

Route-backed endpoint methods carry a ``Docs:`` footer in their docstring
that points at the rendered per-endpoint page on
https://ab-sdk.readthedocs.io . Both the documentation generator
(:mod:`scripts.generate_endpoint_docs`) and the verification test
(``tests/unit/test_docstring_rtd_links.py``) import these helpers, so the
URL format and footer text have exactly one definition and cannot drift.

The footer deliberately carries only the page URL plus the *names* of the
request/response/query models — never the model URLs. Inlining a model
anchor URL would push the docstring line past the 120-char ruff limit, and
the per-endpoint page is where the models are actually rendered as field
tables anyway, so the page link already leads the reader to them.
"""

from __future__ import annotations

import re

RTD_BASE = "https://ab-sdk.readthedocs.io/en/latest"

# Type strings that name a primitive rather than a documented model. These
# never get a "Request/Response model:" footer line.
_PRIMITIVES = frozenset({"int", "str", "bool", "float", "bytes", "None", "dict", "list"})


def endpoint_top_group(group: str) -> str:
    """Return the top-level group for a (possibly dotted) discovery name.

    >>> endpoint_top_group("jobs")
    'jobs'
    >>> endpoint_top_group("jobs.timeline")
    'jobs'
    """
    return group.split(".")[0]


def endpoint_page_slug(group: str, method: str) -> str:
    """Page slug for a method within its top-level group directory.

    ``group`` is the discovery group name (``"jobs"`` or ``"jobs.timeline"``)
    and ``method`` is the Python method name. The page lives at
    ``docs/api/<top>/<slug>.md``.

    >>> endpoint_page_slug("jobs", "transfer")
    'transfer'
    >>> endpoint_page_slug("jobs.timeline", "list")
    'timeline.list'
    """
    sub = group.split(".")[1:]
    return ".".join([*sub, method])


def endpoint_doc_url(group: str, method: str) -> str:
    """Full RTD URL for a method's per-endpoint page.

    >>> endpoint_doc_url("jobs", "transfer")
    'https://ab-sdk.readthedocs.io/en/latest/api/jobs/transfer.html'
    >>> endpoint_doc_url("jobs.timeline", "list")
    'https://ab-sdk.readthedocs.io/en/latest/api/jobs/timeline.list.html'
    """
    top = endpoint_top_group(group)
    slug = endpoint_page_slug(group, method)
    return f"{RTD_BASE}/api/{top}/{slug}.html"


def _strip_list(name: str) -> str:
    """``List[Foo]`` -> ``Foo``; everything else unchanged."""
    if name.startswith("List[") and name.endswith("]"):
        return name[len("List[") : -1]
    return name


def is_model_type(name: str | None) -> bool:
    """True when *name* refers to a documented model (not a primitive)."""
    if not name:
        return False
    return _strip_list(name) not in _PRIMITIVES


def params_are_path_bound(path: str | None, params_model: str | None) -> bool:
    """True when *params_model* documents path segments, not query-string params.

    A ``params_model`` normally models the query string, but a route can also
    use it to model a *path* parameter — e.g. ``jobs.tracking.v3`` whose
    ``historyAmount`` is keyed as a ``{historyAmount}`` placeholder in the route
    path (and bound into the URL path at call time), even though the swagger
    contradictorily declares it ``in: query`` (which keeps gate G5 happy, so the
    ``params_model`` must stay). We detect that case structurally: every field's
    wire-name (alias or attribute name) appears as a ``{placeholder}`` in *path*.

    The single source of truth for "is this a path param?", shared by the footer
    builder, the per-endpoint page generator, and the footer-verification test so
    the page heading and the docstring footer never disagree. Model resolution is
    lazy and defensive — any failure falls back to ``False`` (treat as query).
    """
    if not path or not is_model_type(params_model):
        return False
    try:
        from ab.api import models

        model = getattr(models, _strip_list(params_model), None)
        fields = getattr(model, "model_fields", None) or {}
        wires = {(field.alias or name) for name, field in fields.items()}
    except Exception:
        return False
    if not wires:
        return False
    placeholders = set(re.findall(r"\{(\w+)\}", path))
    return wires <= placeholders


def docstring_footer_lines(
    group: str,
    method: str,
    *,
    request_model: str | None = None,
    params_model: str | None = None,
    response_model: str | None = None,
    path: str | None = None,
) -> list[str]:
    """Build the ``Docs:`` footer block appended to a method's docstring.

    The first line is always the page URL. Model lines are added only for
    real (non-primitive) models, naming them so the reader knows which
    section of the linked page to read. When *path* is given, a params_model
    whose every field is a path placeholder is labelled ``Path params:`` rather
    than ``Query params:`` (see :func:`params_are_path_bound`).
    """
    lines = [f"Docs: {endpoint_doc_url(group, method)}"]
    if is_model_type(request_model):
        lines.append(f"Request model: {request_model}")
    if is_model_type(params_model):
        label = "Path params" if params_are_path_bound(path, params_model) else "Query params"
        lines.append(f"{label}: {params_model}")
    if is_model_type(response_model):
        lines.append(f"Response model: {response_model}")
    return lines


def footer_marker() -> str:
    """The stable prefix that marks the generated footer's page-URL line.

    Used to locate (and idempotently refresh) the footer inside an existing
    docstring without disturbing the human-authored prose above it.
    """
    return f"Docs: {RTD_BASE}/"


# Prefixes the generator emits for footer lines. A line is "footer-shaped" if,
# once stripped, it is blank or begins with one of these.
_FOOTER_LINE_PREFIXES = (
    "Docs: ", "Request model: ", "Query params: ", "Path params: ", "Response model: ",
)


def _is_footer_shaped(line: str) -> bool:
    s = line.strip()
    return s == "" or s.startswith(_FOOTER_LINE_PREFIXES)


def strip_footer_block(text: str) -> str:
    """Remove a generated footer block from the *end* of *text*, if present.

    The footer is anchored on its ``Docs: <RTD base>`` page-URL line: we take
    the *last* such line and treat it (plus the contiguous model lines and the
    blank separator above it) as the footer — but only when every line after it
    is footer-shaped. This is deliberately precise so that

    * human prose lines that begin with ``Request model:`` / ``Response model:``
      (a convention used in several hand-written docstrings) are never mistaken
      for footer, and
    * a sentence in the prose that merely mentions the RTD URL is never
      silently truncated.
    """
    lines = text.split("\n")
    marker = footer_marker()
    idx = next((i for i in range(len(lines) - 1, -1, -1) if lines[i].strip().startswith(marker)), None)
    if idx is None:
        return text
    # Everything below the Docs line must be footer-shaped (model/blank lines);
    # otherwise the marker is inside the prose, not our trailing footer.
    if not all(_is_footer_shaped(line) for line in lines[idx + 1 :]):
        return text
    # Drop the footer (Docs line onward) plus any blank separator lines above it.
    j = idx
    while j > 0 and lines[j - 1].strip() == "":
        j -= 1
    return "\n".join(lines[:j])
