"""Generate null-populated request fixture JSON files for all Route models.

Introspects all endpoint classes in ``ab/api/endpoints/``, finds Route class
attributes with ``params_model`` or ``request_model``, resolves each model
class from ``ab.api.models``, and writes null-populated JSON fixtures to
``tests/fixtures/requests/``.

Existing fixture files are never overwritten.

Usage::

    python scripts/generate_request_fixtures.py
"""

from __future__ import annotations

import importlib
import json
import pkgutil
from pathlib import Path

import ab.api.endpoints as endpoints_pkg
import ab.api.models as models_pkg
from ab.api.route import Route

REQUESTS_DIR = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "requests"


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


def _collect_model_names(routes: list[Route]) -> set[str]:
    """Extract unique params_model and request_model names from routes."""
    names: set[str] = set()
    for route in routes:
        if route.params_model:
            names.add(route.params_model)
        if route.request_model:
            names.add(route.request_model)
    return names


def _generate_null_fixture(model_name: str) -> dict[str, None]:
    """Resolve a model class and produce a dict with all fields set to null.

    Uses the field alias (camelCase) as the JSON key.
    """
    model_cls = getattr(models_pkg, model_name)
    fixture: dict[str, None] = {}
    for field_name, field_info in model_cls.model_fields.items():
        key = field_info.alias if field_info.alias else field_name
        fixture[key] = None
    return fixture


def main() -> None:
    REQUESTS_DIR.mkdir(parents=True, exist_ok=True)

    routes = _collect_routes()
    model_names = _collect_model_names(routes)

    generated = 0
    skipped = 0

    for name in sorted(model_names):
        filepath = REQUESTS_DIR / f"{name}.json"
        if filepath.exists():
            skipped += 1
            print(f"  SKIP  {name}.json (already exists)")
            continue

        try:
            fixture = _generate_null_fixture(name)
        except AttributeError:
            print(f"  ERROR {name} — model class not found in ab.api.models")
            continue

        filepath.write_text(json.dumps(fixture, indent=2) + "\n")
        generated += 1
        print(f"  NEW   {name}.json ({len(fixture)} fields)")

    print(f"\nSummary: {generated} generated, {skipped} skipped, {len(model_names)} total models")


if __name__ == "__main__":
    main()
