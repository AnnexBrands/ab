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
