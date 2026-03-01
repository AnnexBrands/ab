"""Endpoint and method introspection for the CLI.

Discovers endpoint groups and their public methods by inspecting the
ABConnectAPI class and its endpoint attributes — without instantiation.
"""

from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from typing import Any

from ab.api.route import Route


@dataclass
class ParamInfo:
    """Metadata about a single method parameter."""

    name: str
    cli_name: str
    annotation: Any = None
    default: Any = inspect.Parameter.empty
    required: bool = True
    kind: str = "keyword"  # "positional" or "keyword"


@dataclass
class MethodInfo:
    """Metadata about a callable endpoint method."""

    name: str
    callable: Any = None
    positional_params: list[ParamInfo] = field(default_factory=list)
    keyword_params: list[ParamInfo] = field(default_factory=list)
    docstring: str | None = None
    route: Route | None = None
    return_annotation: str | None = None


@dataclass
class EndpointInfo:
    """Metadata about an endpoint group."""

    name: str
    endpoint_class: type | None = None
    methods: list[MethodInfo] = field(default_factory=list)
    aliases: list[str] = field(default_factory=list)
    path_root: str | None = None


def _python_to_cli(name: str) -> str:
    """Convert a Python parameter name to CLI flag form."""
    return f"--{name.replace('_', '-')}"


def _extract_params(sig: inspect.Signature) -> tuple[list[ParamInfo], list[ParamInfo]]:
    """Extract positional and keyword parameters from a method signature."""
    positional: list[ParamInfo] = []
    keyword: list[ParamInfo] = []

    for param_name, param in sig.parameters.items():
        if param_name == "self":
            continue

        annotation = param.annotation if param.annotation is not inspect.Parameter.empty else None
        default = param.default
        required = default is inspect.Parameter.empty

        info = ParamInfo(
            name=param_name,
            cli_name=_python_to_cli(param_name),
            annotation=annotation,
            default=default,
            required=required,
        )

        if param.kind in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        ):
            info.kind = "positional"
            positional.append(info)
        elif param.kind == inspect.Parameter.KEYWORD_ONLY:
            info.kind = "keyword"
            keyword.append(info)
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            # **kwargs — accept JSON body via --body
            info = ParamInfo(
                name="body",
                cli_name="--body",
                annotation=dict,
                default=inspect.Parameter.empty,
                required=False,
                kind="keyword",
            )
            keyword.append(info)

    return positional, keyword


def _extract_methods(cls: type) -> list[MethodInfo]:
    """Extract all public methods from an endpoint class."""
    methods: list[MethodInfo] = []

    for name in sorted(dir(cls)):
        if name.startswith("_"):
            continue
        attr = getattr(cls, name, None)
        if attr is None or not callable(attr):
            continue
        # Skip inherited object methods
        if hasattr(object, name):
            continue

        try:
            sig = inspect.signature(attr)
        except (ValueError, TypeError):
            continue

        positional, keyword = _extract_params(sig)

        # Capture return annotation as a string
        ret_ann = None
        if sig.return_annotation is not inspect.Parameter.empty:
            ret_ann = _format_return_annotation(sig.return_annotation)

        methods.append(
            MethodInfo(
                name=name,
                positional_params=positional,
                keyword_params=keyword,
                docstring=inspect.getdoc(attr),
                return_annotation=ret_ann,
            )
        )

    return methods


def _format_return_annotation(ann: Any) -> str:
    """Convert a return annotation to a readable string."""
    origin = getattr(ann, "__origin__", None)
    args = getattr(ann, "__args__", ())

    if origin is list:
        if args:
            inner = _format_return_annotation(args[0])
            return f"list[{inner}]"
        return "list"

    if hasattr(ann, "__name__"):
        return ann.__name__

    return str(ann)


def discover_endpoints_from_class() -> dict[str, EndpointInfo]:
    """Discover endpoint groups by inspecting ABConnectAPI._init_endpoints.

    This approach avoids instantiating the client (no credentials needed)
    by parsing the attribute assignments in ``_init_endpoints``.
    """
    import re

    from ab.api.base import BaseEndpoint
    from ab.cli.aliases import ALIASES
    from ab.cli.route_resolver import resolve_routes_for_class
    from ab.client import ABConnectAPI

    endpoints: dict[str, EndpointInfo] = {}

    # Build reverse alias map: endpoint_name → [alias1, alias2, ...]
    reverse_aliases: dict[str, list[str]] = {}
    for alias, target in ALIASES.items():
        reverse_aliases.setdefault(target, []).append(alias)

    # Inspect _init_endpoints source to find attribute name → class mappings
    source = inspect.getsource(ABConnectAPI._init_endpoints)
    # Parse lines like: self.address = AddressEndpoint(self._acportal)

    for match in re.finditer(r"self\.(\w+)\s*=\s*(\w+Endpoint)\(", source):
        attr_name = match.group(1)
        class_name = match.group(2)

        # Resolve the class from the endpoints package
        from ab.api import endpoints as ep_module

        cls = getattr(ep_module, class_name, None)
        if cls is None or not (isinstance(cls, type) and issubclass(cls, BaseEndpoint)):
            continue

        methods = _extract_methods(cls)

        # Resolve method → Route mapping
        method_routes = resolve_routes_for_class(cls)
        for m in methods:
            if m.name in method_routes:
                m.route = method_routes[m.name]

        # Compute path_root from collected Route paths
        path_root = _compute_path_root(method_routes)

        endpoints[attr_name] = EndpointInfo(
            name=attr_name,
            endpoint_class=cls,
            methods=methods,
            aliases=sorted(reverse_aliases.get(attr_name, [])),
            path_root=path_root,
        )

    return endpoints


def _compute_path_root(method_routes: dict[str, Route]) -> str | None:
    """Extract the common first path segment from a set of Routes."""
    if not method_routes:
        return None
    paths = [r.path for r in method_routes.values()]
    # Extract first path segment (e.g., "/job" from "/job/{id}/timeline")
    segments: set[str] = set()
    for path in paths:
        parts = path.strip("/").split("/")
        if parts:
            segments.add(f"/{parts[0]}")
    if len(segments) == 1:
        return segments.pop()
    # Multiple roots — return the most common one
    if segments:
        from collections import Counter

        counter = Counter(
            f"/{path.strip('/').split('/')[0]}" for path in paths
        )
        return counter.most_common(1)[0][0]
    return None


def discover_endpoints_from_instance(api: object) -> dict[str, EndpointInfo]:
    """Discover endpoint groups from a live ABConnectAPI instance.

    Used when an actual API client is available (method calls need bound methods).
    """
    from ab.api.base import BaseEndpoint

    endpoints: dict[str, EndpointInfo] = {}

    for attr_name in sorted(dir(api)):
        if attr_name.startswith("_"):
            continue
        attr = getattr(api, attr_name, None)
        if not isinstance(attr, BaseEndpoint):
            continue

        methods: list[MethodInfo] = []
        for method_name in sorted(dir(attr)):
            if method_name.startswith("_"):
                continue
            method = getattr(attr, method_name, None)
            if method is None or not callable(method):
                continue
            if hasattr(object, method_name):
                continue

            try:
                sig = inspect.signature(method)
            except (ValueError, TypeError):
                continue

            positional, keyword = _extract_params(sig)
            methods.append(
                MethodInfo(
                    name=method_name,
                    callable=method,
                    positional_params=positional,
                    keyword_params=keyword,
                    docstring=inspect.getdoc(method),
                )
            )

        endpoints[attr_name] = EndpointInfo(
            name=attr_name,
            endpoint_class=type(attr),
            methods=methods,
        )

    return endpoints
