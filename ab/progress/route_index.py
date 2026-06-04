"""Route discovery and path normalization for FIXTURES.md sync.

Introspects all endpoint classes in ``ab/api/endpoints/`` to collect Route
objects, then provides a normalized-path lookup so FIXTURES.md rows can be
matched to their authoritative Route definitions.
"""

from __future__ import annotations

import importlib
import pkgutil
import re
from dataclasses import dataclass

import ab.api.endpoints as endpoints_pkg
from ab.api.route import Route


@dataclass
class RouteInfo:
    """Flattened view of a Route for FIXTURES.md sync."""

    path: str  # canonical path from Route, e.g. "/companies/{companyId}/fulldetails"
    method: str  # "GET", "POST", etc.
    request_model: str | None
    params_model: str | None
    response_model: str | None
    api_surface: str  # "acportal" | "catalog" | "abc"


def normalize_path(path: str) -> str:
    """Normalize path parameters for matching.

    Replaces ``{anything}`` with ``{_}`` so that
    ``/companies/{companyId}/details`` and ``/companies/{id}/details``
    both become ``/companies/{_}/details``.
    """
    return re.sub(r"\{[^}]+\}", "{_}", path)


def _collect_routes() -> list[Route]:
    """Import all endpoint modules (including subpackage modules like
    ``ab.api.endpoints.jobs.note``) and collect Route instances.
    """
    routes: list[Route] = []
    seen: set[int] = set()
    for module in _iter_endpoint_modules(endpoints_pkg):
        for attr_name in dir(module):
            obj = getattr(module, attr_name)
            if isinstance(obj, Route) and id(obj) not in seen:
                routes.append(obj)
                seen.add(id(obj))
    return routes


def _iter_endpoint_modules(pkg):
    """Yield every module under *pkg* recursively."""
    for _importer, mod_name, ispkg in pkgutil.iter_modules(pkg.__path__):
        full = f"{pkg.__name__}.{mod_name}"
        module = importlib.import_module(full)
        yield module
        if ispkg:
            yield from _iter_endpoint_modules(module)


def index_all_routes() -> dict[tuple[str, str], RouteInfo]:
    """Discover all Route objects, return keyed by (normalized_path, method).

    If multiple Routes share the same normalized key (e.g. two GETs on
    ``/Seller/{id}`` with different response models), the last one wins.
    This mirrors FIXTURES.md which may have duplicate rows for such cases.
    """
    routes = _collect_routes()
    index: dict[tuple[str, str], RouteInfo] = {}
    for route in routes:
        key = (normalize_path(route.path), route.method)
        info = RouteInfo(
            path=route.path,
            method=route.method,
            request_model=route.request_model,
            params_model=route.params_model,
            response_model=route.response_model,
            api_surface=route.api_surface,
        )
        index[key] = info
    return index


def build_endpoint_class_progress(
    example_methods: dict[str, set[str]] | None = None,
) -> list:
    """Build per-endpoint-class progress data for the HTML report.

    Returns a list of ``EndpointClassProgress`` instances.
    """
    from ab.cli.discovery import discover_endpoints_from_class
    from ab.progress.models import EndpointClassProgress, MethodProgress

    if example_methods is None:
        example_methods = _scan_example_entries()

    registry = discover_endpoints_from_class()
    results: list[EndpointClassProgress] = []

    for name in sorted(registry):
        info = registry[name]
        helpers: list[MethodProgress] = []
        sub_groups: dict[str, list[MethodProgress]] = {}
        total_with_route = 0
        total_with_example = 0
        total_with_cli = 0
        ep_examples = example_methods.get(name, set())

        for m in info.methods:
            has_route = m.route is not None
            has_example = m.name in ep_examples
            has_cli = True  # all discovered methods are CLI-callable

            if has_route:
                total_with_route += 1
                http_method = m.route.method
                http_path = m.route.path
                return_type = m.return_annotation or m.route.response_model or "Any"
                sub_root = _extract_sub_root(http_path, info.path_root)
            else:
                http_method = ""
                http_path = ""
                return_type = m.return_annotation or "Any"
                sub_root = ""

            if has_example:
                total_with_example += 1
            if has_cli:
                total_with_cli += 1

            mp = MethodProgress(
                dotted_path=f"api.{name}.{m.name}",
                method_name=m.name,
                http_method=http_method,
                http_path=http_path,
                return_type=return_type,
                has_example=has_example,
                has_cli=has_cli,
                has_route=has_route,
                path_sub_root=sub_root,
                has_docstring=bool(m.docstring),
            )

            if not has_route:
                helpers.append(mp)
            else:
                sub_groups.setdefault(sub_root, []).append(mp)

        # Sort sub-groups by path
        for key in sub_groups:
            sub_groups[key].sort(key=lambda x: x.http_path)

        progress = EndpointClassProgress(
            class_name=name,
            display_name=name.replace("_", " ").title(),
            aliases=info.aliases,
            path_root=info.path_root or "",
            helpers=helpers,
            sub_groups=sub_groups,
            total_methods=len(info.methods),
            total_with_route=total_with_route,
            total_with_example=total_with_example,
            total_with_cli=total_with_cli,
        )
        results.append(progress)

    return results


def _extract_sub_root(path: str, path_root: str | None) -> str:
    """Extract the sub-root segment from a path.

    E.g., ``/job/{id}/timeline/{code}`` with root ``/job`` → ``timeline``.
    ``/job/{id}`` → ``""`` (root level).
    """
    if not path_root:
        return ""
    # Remove the root prefix
    remainder = path[len(path_root):].strip("/")
    if not remainder:
        return ""
    parts = remainder.split("/")
    # Skip path parameters and find the first non-param segment after root
    for part in parts:
        if not part.startswith("{"):
            return part
    return ""


def _scan_example_entries() -> dict[str, set[str]]:
    """Statically discover which endpoint methods each example exercises.

    Parses every ``examples/*.py`` with :mod:`ast` — *without importing it* —
    and records every ``api.<group>[.<subgroup>].<method>(...)`` call chain it
    finds. Returns ``{endpoint_attr: {method_name, ...}}`` keyed to match the
    endpoint registry (e.g. ``"contacts"``, ``"jobs.note"``).

    Static parsing (vs. the previous import-based scan) is deliberate: it sees
    underscore-prefixed runner files *and* plain ``main()`` scripts, and it
    never executes example code, so report generation triggers no live API
    calls. Demonstrations whose client variable is not named ``api`` are not
    counted.
    """
    import ast
    from pathlib import Path

    examples_dir = Path(__file__).resolve().parent.parent.parent / "examples"
    if not examples_dir.exists():
        return {}

    result: dict[str, set[str]] = {}
    for py in sorted(examples_dir.glob("*.py")):
        if py.name in {"__init__.py", "__main__.py", "_runner.py"}:
            continue
        try:
            tree = ast.parse(py.read_text(encoding="utf-8"))
        except (OSError, SyntaxError):
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(
                node.func, ast.Attribute
            ):
                continue
            chain = _attr_chain(node.func)
            # Require api.<group>.<method> (>= 3 segments) rooted at ``api``.
            if len(chain) < 3 or chain[0] != "api":
                continue
            group = ".".join(chain[1:-1])
            result.setdefault(group, set()).add(chain[-1])

    return result


def _attr_chain(node) -> list[str]:
    """Flatten an attribute chain to ``[root_name, attr, attr, ...]``.

    Returns an empty list when the chain is not rooted at a simple Name.
    """
    import ast

    parts: list[str] = []
    cur = node
    while isinstance(cur, ast.Attribute):
        parts.append(cur.attr)
        cur = cur.value
    if isinstance(cur, ast.Name):
        parts.append(cur.id)
        parts.reverse()
        return parts
    return []


def index_all_routes_multi() -> dict[tuple[str, str], list[RouteInfo]]:
    """Like index_all_routes but preserves multiple routes per key.

    Some endpoints have two Route objects for the same path+method but
    different response models (e.g. GET /Seller/{id} → SellerDto and
    SellerExpandedDto). FIXTURES.md has separate rows for each.
    """
    routes = _collect_routes()
    index: dict[tuple[str, str], list[RouteInfo]] = {}
    for route in routes:
        key = (normalize_path(route.path), route.method)
        info = RouteInfo(
            path=route.path,
            method=route.method,
            request_model=route.request_model,
            params_model=route.params_model,
            response_model=route.response_model,
            api_surface=route.api_surface,
        )
        index.setdefault(key, []).append(info)
    return index


# ----------------------------------------------------------------------
# No-drift report feeds
#
# These derive the progress report's inputs directly from live Route
# objects (and the endpoint registry), so the report can be regenerated
# from code alone — never from hand-maintained markdown that rots.
# ----------------------------------------------------------------------

_SURFACE_DISPLAY = {"acportal": "ACPortal", "catalog": "Catalog", "abc": "ABC"}

_MODEL_WRAPPERS = ("PaginatedList[", "List[", "list[")


def _strip_model_wrapper(model: str) -> str:
    """Return the innermost model name, peeling ``List[]``/``PaginatedList[]``.

    Both report feeds MUST normalize identically so a ``List[JobNote]`` route
    matches a ``JobNote.json`` fixture and lines up across the groups/fixtures
    datasets in ``classify_action_items``.
    """
    name = model.strip()
    changed = True
    while changed:
        changed = False
        for prefix in _MODEL_WRAPPERS:
            if name.startswith(prefix) and name.endswith("]"):
                name = name[len(prefix):-1].strip()
                changed = True
                break
    return name


def _all_route_infos() -> list[RouteInfo]:
    """Flatten ``index_all_routes_multi`` into a stable, sorted list."""
    infos: list[RouteInfo] = []
    for ri_list in index_all_routes_multi().values():
        infos.extend(ri_list)
    infos.sort(
        key=lambda ri: (
            ri.api_surface,
            ri.path,
            ri.method,
            ri.response_model or "",
        )
    )
    return infos


def _route_group_map() -> dict[tuple[str, str], str]:
    """Map each (normalized_path, method) to its ``api.<group>`` registry name.

    Lets the report label routes with the same dev-facing group the SDK and
    CLI expose (including subgroups like ``jobs.note``), instead of guessing
    from the URL.
    """
    from ab.cli.discovery import discover_endpoints_from_class

    out: dict[tuple[str, str], str] = {}
    for name, info in discover_endpoints_from_class().items():
        for method in info.methods:
            if method.route is not None:
                key = (normalize_path(method.route.path), method.route.method)
                out.setdefault(key, name)
    return out


def routes_as_endpoint_dicts() -> list[dict[str, str | None]]:
    """Build the ``evaluate_all_gates`` input list directly from live Routes.

    Mirrors the dict shape produced by
    :func:`ab.progress.fixtures_generator.parse_existing_fixtures` so the gate
    engine evaluates the *real* route set rather than FIXTURES.md rows.
    """
    return [
        {
            "endpoint_path": ri.path,
            "method": ri.method,
            "request_model": ri.request_model or "",
            "response_model": ri.response_model or "",
            "params_model": ri.params_model,
            "notes": "",
        }
        for ri in _all_route_infos()
    ]


def build_groups_from_routes() -> list:
    """Build the report's ``EndpointGroup`` headline list from live Routes.

    Every route is counted as ``done`` (it exists in code); the per-surface
    coverage summary therefore reflects the real implemented surface.
    """
    from ab.progress.models import Endpoint, EndpointGroup, _group_from_path

    group_map = _route_group_map()
    groups: dict[tuple[str, str], EndpointGroup] = {}

    for index, ri in enumerate(_all_route_infos(), start=1):
        surface = _SURFACE_DISPLAY.get(ri.api_surface, ri.api_surface)
        name = group_map.get(
            (normalize_path(ri.path), ri.method)
        ) or _group_from_path(ri.path)
        key = (surface, name)
        group = groups.get(key)
        if group is None:
            group = EndpointGroup(name=name, api_surface=surface)
            groups[key] = group
        group.endpoints.append(
            Endpoint(
                group_name=name,
                api_surface=surface,
                index=index,
                route_key="",
                method=ri.method,
                path=ri.path,
                response_model=_strip_model_wrapper(ri.response_model or ""),
                ab_status="done",
                ref_status="none",
            )
        )

    result = list(groups.values())
    for group in result:
        group.recount()
    return result


def derive_fixtures_from_routes(fixture_files: set[str]) -> list:
    """Build ``Fixture`` records from live Routes + on-disk fixture files.

    A route's response fixture is ``captured`` when a ``{Model}.json`` file
    exists in ``tests/fixtures/``; otherwise it is ``needs-request-data`` —
    surfacing response models that still lack a captured fixture.
    """
    from ab.progress.models import Fixture

    fixtures: list[Fixture] = []
    for ri in _all_route_infos():
        model = _strip_model_wrapper(ri.response_model or "")
        captured = bool(model) and model in fixture_files
        fixtures.append(
            Fixture(
                endpoint_path=ri.path,
                method=ri.method,
                model_name=model,
                status="captured" if captured else "needs-request-data",
                request_model=ri.request_model,
            )
        )
    return fixtures
