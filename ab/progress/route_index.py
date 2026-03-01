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
    """Import all endpoint modules and collect Route instances."""
    routes: list[Route] = []
    for _importer, mod_name, _ispkg in pkgutil.iter_modules(endpoints_pkg.__path__):
        module = importlib.import_module(f"ab.api.endpoints.{mod_name}")
        for attr_name in dir(module):
            obj = getattr(module, attr_name)
            if isinstance(obj, Route):
                routes.append(obj)
    return routes


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
    """Scan example files to discover which methods have entries.

    Returns ``{endpoint_attr: {method_name, ...}}``.
    """
    import importlib
    import pkgutil
    from pathlib import Path

    examples_dir = Path(__file__).resolve().parent.parent.parent / "examples"
    if not examples_dir.exists():
        return {}

    result: dict[str, set[str]] = {}
    for _importer, mod_name, _ispkg in pkgutil.iter_modules([str(examples_dir)]):
        if mod_name.startswith("_"):
            continue
        try:
            module = importlib.import_module(f"examples.{mod_name}")
        except Exception:
            continue
        runner = getattr(module, "runner", None)
        if runner is None:
            continue
        endpoint_attr = getattr(runner, "endpoint_attr", None) or mod_name
        methods: set[str] = set()
        for entry in getattr(runner, "entries", []):
            methods.add(entry.name)
        if methods:
            result[endpoint_attr] = methods

    return result


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
