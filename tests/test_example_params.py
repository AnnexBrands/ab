"""Validate endpoint parameter names against swagger specifications.

Cross-references the query-parameter names that endpoint methods send to
the API against the swagger specs in ``ab/api/schemas/``.  Catches
parameter mismatches (wrong names, fabricated params) before they reach
production.

Also verifies that POST/PUT/PATCH endpoints with swagger-defined request
bodies use ``json=`` transport (not ``params=``).
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

import pytest

ENDPOINTS_DIR = Path(__file__).resolve().parent.parent / "ab" / "api" / "endpoints"
SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "ab" / "api" / "schemas"

# Map api_surface names to swagger files
SWAGGER_FILES = {
    "acportal": SCHEMAS_DIR / "acportal.json",
    "catalog": SCHEMAS_DIR / "catalog.json",
    "abc": SCHEMAS_DIR / "abc.json",
}


# ── Swagger parsing ──────────────────────────────────────────────────


def _load_swagger_params() -> dict[tuple[str, str], set[str]]:
    """Build ``{(METHOD, /path) → {param_names}}`` from all swagger specs.

    Only includes query parameters (not path params or headers).
    """
    registry: dict[tuple[str, str], set[str]] = {}
    for surface, path in SWAGGER_FILES.items():
        if not path.exists():
            continue
        spec = json.loads(path.read_text())
        paths = spec.get("paths", {})
        for api_path, methods in paths.items():
            for method, operation in methods.items():
                if method in ("parameters", "servers", "summary", "description"):
                    continue
                params = operation.get("parameters", [])
                query_names = set()
                for p in params:
                    if p.get("in") == "query":
                        query_names.add(p["name"])
                key = (method.upper(), api_path)
                # Merge if same path appears in multiple specs
                registry.setdefault(key, set()).update(query_names)
    return registry


def _load_swagger_request_bodies() -> set[tuple[str, str]]:
    """Return ``{(METHOD, /path)}`` for operations that define a requestBody."""
    has_body: set[tuple[str, str]] = set()
    for surface, path in SWAGGER_FILES.items():
        if not path.exists():
            continue
        spec = json.loads(path.read_text())
        paths = spec.get("paths", {})
        for api_path, methods in paths.items():
            for method, operation in methods.items():
                if method in ("parameters", "servers", "summary", "description"):
                    continue
                if "requestBody" in operation:
                    has_body.add((method.upper(), api_path))
    return has_body


# ── Endpoint source parsing ──────────────────────────────────────────


def _parse_routes(source: str) -> dict[str, tuple[str, str, str]]:
    """Extract module-level Route definitions.

    Returns ``{var_name: (method, path, api_surface)}``.
    """
    routes: dict[str, tuple[str, str, str]] = {}
    tree = ast.parse(source)
    for node in ast.iter_child_nodes(tree):
        if not isinstance(node, ast.Assign):
            continue
        if not node.targets or not isinstance(node.targets[0], ast.Name):
            continue
        var_name = node.targets[0].id
        call = node.value
        if not isinstance(call, ast.Call):
            continue
        func = call.func
        if not (isinstance(func, ast.Name) and func.id == "Route"):
            continue
        # Positional args: method, path
        if len(call.args) < 2:
            continue
        method_node, path_node = call.args[0], call.args[1]
        if not isinstance(method_node, ast.Constant) or not isinstance(path_node, ast.Constant):
            continue
        http_method = method_node.value
        api_path = path_node.value
        # Optional keyword: api_surface
        api_surface = "acportal"
        for kw in call.keywords:
            if kw.arg == "api_surface" and isinstance(kw.value, ast.Constant):
                api_surface = kw.value.value
        routes[var_name] = (http_method, api_path, api_surface)
    return routes


_PARAM_KEY_RE = re.compile(r'params\["([^"]+)"\]\s*=')
_PAGINATED_RE = re.compile(r'params\s*=\s*\{([^}]+)\}')
_PAGINATED_KEY_RE = re.compile(r'"([^"]+)"')


def _extract_method_params(source: str) -> list[dict]:
    """Extract per-method info: which Route var is used, which param keys are set.

    Returns a list of dicts with keys:
    ``method_name``, ``route_var``, ``param_keys``, ``uses_json``, ``uses_params``.
    """
    results = []
    tree = ast.parse(source)
    for cls_node in ast.walk(tree):
        if not isinstance(cls_node, ast.ClassDef):
            continue
        for node in cls_node.body:
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if node.name.startswith("_"):
                continue
            method_source = ast.get_source_segment(source, node)
            if method_source is None:
                continue

            # Find route variable reference (e.g. _IS_VALID, _SEARCH)
            route_var = None
            route_re = re.search(r'self\._(?:request|paginated_request)\(\s*(\w+)', method_source)
            if route_re:
                route_var = route_re.group(1)
            # Also check for .bind() pattern
            bind_re = re.search(r'self\._(?:request|paginated_request)\(\s*(\w+)\.bind', method_source)
            if bind_re:
                route_var = bind_re.group(1)

            # Extract param dict keys
            param_keys = set(_PARAM_KEY_RE.findall(method_source))

            # Extract paginated request params
            pag_match = _PAGINATED_RE.search(method_source)
            if pag_match:
                param_keys.update(_PAGINATED_KEY_RE.findall(pag_match.group(1)))

            # Check transport type — covers both `json=data` and `kwargs["json"] = data`
            uses_json = "json=" in method_source or '"json"' in method_source
            uses_params_kwarg = "params=" in method_source or "params=params" in method_source

            results.append({
                "method_name": node.name,
                "route_var": route_var,
                "param_keys": param_keys,
                "uses_json": uses_json,
                "uses_params": uses_params_kwarg,
            })
    return results


# ── Test collection ──────────────────────────────────────────────────


def _collect_test_cases() -> list[tuple[str, str, str, str, str, set[str]]]:
    """Collect ``(file, class, method, http_method, api_path, param_keys)`` tuples.

    Only includes methods that send explicit query parameters (param_keys non-empty).
    """
    cases = []
    for ep_file in sorted(ENDPOINTS_DIR.glob("*.py")):
        if ep_file.name.startswith("_") or ep_file.name == "base.py":
            continue
        source = ep_file.read_text()
        routes = _parse_routes(source)
        methods = _extract_method_params(source)
        for m in methods:
            route_var = m["route_var"]
            if route_var is None or route_var not in routes:
                continue
            http_method, api_path, _surface = routes[route_var]
            # Normalize path: endpoint paths don't have /api prefix, swagger does
            swagger_path = f"/api{api_path}"
            if m["param_keys"]:
                cases.append((
                    ep_file.name,
                    "",
                    m["method_name"],
                    http_method,
                    swagger_path,
                    m["param_keys"],
                ))
    return cases


def _collect_transport_cases() -> list[tuple[str, str, str, str, bool]]:
    """Collect POST/PUT/PATCH methods that should use json= but use params=."""
    cases = []
    for ep_file in sorted(ENDPOINTS_DIR.glob("*.py")):
        if ep_file.name.startswith("_") or ep_file.name == "base.py":
            continue
        source = ep_file.read_text()
        routes = _parse_routes(source)
        methods = _extract_method_params(source)
        for m in methods:
            route_var = m["route_var"]
            if route_var is None or route_var not in routes:
                continue
            http_method, api_path, _surface = routes[route_var]
            if http_method in ("POST", "PUT", "PATCH"):
                swagger_path = f"/api{api_path}"
                cases.append((
                    ep_file.name,
                    m["method_name"],
                    http_method,
                    swagger_path,
                    m["uses_json"],
                ))
    return cases


# ── Tests ────────────────────────────────────────────────────────────


_SWAGGER_PARAMS = _load_swagger_params()
_SWAGGER_BODIES = _load_swagger_request_bodies()
_PARAM_CASES = _collect_test_cases()
_TRANSPORT_CASES = _collect_transport_cases()


@pytest.mark.parametrize(
    "ep_file,cls,method_name,http_method,swagger_path,param_keys",
    _PARAM_CASES,
    ids=[f"{c[0]}::{c[2]}" for c in _PARAM_CASES],
)
def test_query_params_match_swagger(
    ep_file: str,
    cls: str,
    method_name: str,
    http_method: str,
    swagger_path: str,
    param_keys: set[str],
) -> None:
    """Every query parameter sent by an endpoint method must exist in swagger."""
    key = (http_method, swagger_path)
    swagger_params = _SWAGGER_PARAMS.get(key)

    if swagger_params is None:
        # Try without /api prefix (some paths vary)
        alt_key = (http_method, swagger_path.replace("/api/api/", "/api/"))
        swagger_params = _SWAGGER_PARAMS.get(alt_key)

    if swagger_params is None:
        pytest.skip(f"No swagger entry for {http_method} {swagger_path}")

    # Case-insensitive comparison — some servers accept camelCase variants
    # of PascalCase swagger params (e.g. pageNumber vs PageNumber).
    swagger_lower = {p.lower() for p in swagger_params}
    unknown = {p for p in param_keys if p.lower() not in swagger_lower}
    assert not unknown, (
        f"{ep_file}::{method_name} sends unknown query params {unknown} "
        f"to {http_method} {swagger_path}. "
        f"Swagger allows: {sorted(swagger_params)}"
    )


@pytest.mark.parametrize(
    "ep_file,method_name,http_method,swagger_path,uses_json",
    _TRANSPORT_CASES,
    ids=[f"{c[0]}::{c[1]}" for c in _TRANSPORT_CASES],
)
def test_post_methods_use_json_transport(
    ep_file: str,
    method_name: str,
    http_method: str,
    swagger_path: str,
    uses_json: bool,
) -> None:
    """POST/PUT/PATCH endpoints with swagger requestBody should use json= not params=."""
    key = (http_method, swagger_path)
    has_body = key in _SWAGGER_BODIES

    if not has_body:
        pytest.skip(f"No requestBody in swagger for {http_method} {swagger_path}")

    assert uses_json, (
        f"{ep_file}::{method_name} should use json= for {http_method} {swagger_path} "
        f"(swagger defines a requestBody)"
    )
