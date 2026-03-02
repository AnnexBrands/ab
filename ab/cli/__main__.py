"""Endpoint CLI dispatcher — ``ab`` (production) and ``abs`` (staging).

Calls ABConnect API endpoints directly from the terminal::

    ab --list                            # list all endpoint groups
    ab addr validate --line1="123 Main"  # call endpoint (production)
    abs addr validate --line1="123 Main" # call endpoint (staging)
    ab addr.validate --line1="123 Main"  # dot syntax
    ab addr --list                       # list methods in endpoint
    ab addr validate --help              # show method parameters
"""

from __future__ import annotations

import inspect
import sys
from typing import Any

from ab.cli.aliases import ALIASES
from ab.cli.discovery import EndpointInfo, MethodInfo, discover_endpoints_from_class
from ab.cli.formatter import format_result
from ab.cli.parser import parse_cli_args

# ------------------------------------------------------------------
# Resolution helpers (mirrors examples/__main__.py semantics)
# ------------------------------------------------------------------


def _resolve_module(
    name: str, registry: dict[str, EndpointInfo]
) -> tuple[str, EndpointInfo] | None:
    """Resolve *name* to an endpoint via exact/alias/prefix match."""
    if name in registry:
        return name, registry[name]

    if name in ALIASES and ALIASES[name] in registry:
        target = ALIASES[name]
        return target, registry[target]

    # Prefix match on endpoint names
    matches = [(k, v) for k, v in registry.items() if k.startswith(name)]

    # Prefix match on alias keys
    alias_matches = [
        (ALIASES[k], registry[ALIASES[k]])
        for k in ALIASES
        if k.startswith(name) and ALIASES[k] in registry
    ]
    seen = {m for m, _ in matches}
    for mod_name, info in alias_matches:
        if mod_name not in seen:
            matches.append((mod_name, info))
            seen.add(mod_name)

    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        names = ", ".join(sorted(m for m, _ in matches))
        print(f"Ambiguous module '{name}' — matches: {names}", file=sys.stderr)
        return None
    print(f"Unknown module '{name}'", file=sys.stderr)
    print(f"Available: {', '.join(sorted(registry))}", file=sys.stderr)
    return None


def _resolve_method(
    name: str, endpoint: EndpointInfo
) -> MethodInfo | None:
    """Resolve *name* to a method via exact or prefix match."""
    for m in endpoint.methods:
        if m.name == name:
            return m

    matches = [m for m in endpoint.methods if m.name.startswith(name)]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        names = ", ".join(m.name for m in matches)
        print(f"Ambiguous method '{name}' — matches: {names}", file=sys.stderr)
        return None

    print(f"Unknown method '{name}'", file=sys.stderr)
    print(
        f"Available: {', '.join(m.name for m in endpoint.methods)}",
        file=sys.stderr,
    )
    return None


# ------------------------------------------------------------------
# Listing helpers
# ------------------------------------------------------------------


def _list_all(registry: dict[str, EndpointInfo]) -> None:
    """Print all endpoint groups with method counts, path roots, and aliases."""
    total_methods = 0
    print(f"\n  {'Endpoint':<20} {'Methods':>7}   {'Path Root':<15}   Aliases", file=sys.stderr)
    print(f"  {'─' * 20} {'─' * 7}   {'─' * 15}   {'─' * 30}", file=sys.stderr)
    for name in sorted(registry):
        info = registry[name]
        count = len(info.methods)
        total_methods += count
        aliases = ", ".join(info.aliases) or "—"
        path_root = info.path_root or "—"
        print(f"  {name:<20} {count:>7}   {path_root:<15}   {aliases}", file=sys.stderr)
    print(f"\n  {len(registry)} endpoints, {total_methods} methods\n", file=sys.stderr)


def _list_methods(endpoint: EndpointInfo) -> None:
    """Print methods in an endpoint group, separated into helpers and API methods."""
    w = sys.stderr.write
    w(f"\n  {endpoint.name} — {len(endpoint.methods)} methods\n\n")

    helpers = [m for m in endpoint.methods if m.route is None]
    api_methods = [m for m in endpoint.methods if m.route is not None]

    # Helpers section
    if helpers:
        w("  Helpers (no API route):\n")
        w(f"  {'─' * 50}\n")
        for m in helpers:
            params = _param_summary(m)
            w(f"  {m.name:<30} {params}\n")
        w("\n")

    # API methods section
    if api_methods:
        w("  API Methods:\n")
        w(f"  {'─' * 50}\n")
        api_methods.sort(key=lambda m: m.name)
        for m in api_methods:
            route = m.route
            ret = m.return_annotation or route.response_model or ""
            ret_str = f" -> {ret}" if ret else ""
            params = _param_summary(m)
            w(f"  {m.name:<30} ({params}){ret_str}\n")

    w("\n")


def _param_summary(m: MethodInfo) -> str:
    """Build a short parameter summary for listing."""
    parts: list[str] = []
    for p in m.positional_params:
        parts.append(p.name)
    for p in m.keyword_params:
        if p.default is not inspect.Parameter.empty:
            parts.append(f"{p.name}={p.default!r}")
        else:
            parts.append(p.name)
    return ", ".join(parts) if parts else ""


# ------------------------------------------------------------------
# API client creation
# ------------------------------------------------------------------


def _create_api(env: str | None) -> Any:
    """Create ABConnectAPI with user-friendly error handling."""
    try:
        from ab.client import ABConnectAPI

        return ABConnectAPI(env=env)
    except FileNotFoundError:
        env_file = f".env.{env}" if env else ".env"
        print("Credentials not found.", file=sys.stderr)
        print(
            f"Create {env_file} with ABCONNECT_USERNAME, ABCONNECT_PASSWORD, "
            f"ABCONNECT_CLIENT_ID, ABCONNECT_CLIENT_SECRET",
            file=sys.stderr,
        )
        sys.exit(2)
    except Exception as exc:
        # Pydantic ValidationError or other config issues
        if "ValidationError" in type(exc).__name__:
            print(f"Configuration error: {exc}", file=sys.stderr)
        else:
            print(f"Failed to initialize API client: {exc}", file=sys.stderr)
        sys.exit(2)


# ------------------------------------------------------------------
# Main dispatch
# ------------------------------------------------------------------


def main(env: str | None = None) -> None:
    """Core CLI dispatcher.

    Args:
        env: ``None`` for production, ``"staging"`` for staging.
    """
    args = sys.argv[1:]

    # --list at top level doesn't need credentials
    if not args or args == ["--list"]:
        registry = discover_endpoints_from_class()
        _list_all(registry)
        return

    raw = args[0]

    # Dot syntax: module.method
    if "." in raw:
        mod_part, method_part = raw.split(".", 1)
        rest = args[1:]
    else:
        mod_part = raw
        method_part = None
        rest = args[1:]

    # Class-level discovery for --list operations (no credentials)
    registry = discover_endpoints_from_class()

    resolved = _resolve_module(mod_part, registry)
    if resolved is None:
        sys.exit(1)
    mod_name, endpoint_info = resolved

    # module with no method → list methods (no credentials needed)
    if method_part is None and (not rest or rest == ["--list"]):
        _list_methods(endpoint_info)
        return

    # Resolve method name
    method_name = method_part or (rest[0] if rest else None)
    if method_name is None:
        _list_methods(endpoint_info)
        return

    # Remove method name from rest if it came from space syntax
    if method_part is None and rest:
        rest = rest[1:]

    method = _resolve_method(method_name, endpoint_info)
    if method is None:
        sys.exit(1)

    # --help doesn't need credentials
    if "--help" in rest:
        from ab.cli.parser import print_method_help

        print_method_help(method, module_name=mod_name)
        sys.exit(0)

    # Parse arguments
    positional, keyword = parse_cli_args(rest, method)

    # Now we need a live client — create it
    api = _create_api(env)

    # Get the live endpoint instance and bound method
    live_endpoint = getattr(api, mod_name)
    live_method = getattr(live_endpoint, method.name)

    # Handle --body for JSON request bodies
    body = keyword.pop("__body__", None)

    # Call the method
    try:
        if body is not None:
            result = live_method(*positional, data=body, **keyword)
        else:
            result = live_method(*positional, **keyword)
    except Exception as exc:
        # requests HTTP errors
        if hasattr(exc, "response") and hasattr(exc.response, "status_code"):
            print(f"HTTP {exc.response.status_code}: {exc.response.text}", file=sys.stderr)
            sys.exit(2)
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)

    # Format and print result
    print(format_result(result))
