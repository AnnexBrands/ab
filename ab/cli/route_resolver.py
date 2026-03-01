"""Route-to-method resolver via source-code introspection.

Maps each public method of an endpoint class to its Route constant by
parsing the method's source code for ``self._request(_ROUTE_NAME`` calls,
then matching against module-level Route instances.
"""

from __future__ import annotations

import inspect
import re

from ab.api.route import Route

_ROUTE_REF_RE = re.compile(r"(?:self\._request|_request)\(\s*(_[A-Z_][A-Z0-9_]*)")


def resolve_routes_for_class(cls: type) -> dict[str, Route]:
    """Map method names to their Route constants via source introspection."""
    module = inspect.getmodule(cls)
    if module is None:
        return {}

    # Collect all Route constants in the module
    route_vars: dict[str, Route] = {}
    for name in dir(module):
        obj = getattr(module, name, None)
        if isinstance(obj, Route):
            route_vars[name] = obj

    # For each public method, find which Route it references
    method_routes: dict[str, Route] = {}
    for method_name in dir(cls):
        if method_name.startswith("_"):
            continue
        method = getattr(cls, method_name, None)
        if method is None or not callable(method):
            continue
        try:
            source = inspect.getsource(method)
        except (OSError, TypeError):
            continue
        match = _ROUTE_REF_RE.search(source)
        if match:
            route_name = match.group(1)
            if route_name in route_vars:
                method_routes[method_name] = route_vars[route_name]

    return method_routes


def path_param_to_constant(param: str) -> str:
    """Convert a camelCase path parameter to a TEST_SCREAMING_SNAKE constant name.

    >>> path_param_to_constant("jobDisplayId")
    'TEST_JOB_DISPLAY_ID'
    >>> path_param_to_constant("contactId")
    'TEST_CONTACT_ID'
    """
    snake = re.sub(r"([A-Z])", r"_\1", param).upper()
    if snake.startswith("_"):
        snake = snake[1:]
    return f"TEST_{snake}"
