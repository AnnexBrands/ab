#!/usr/bin/env python3
"""Generate mechanical model test stubs for endpoints missing G3 coverage.

Scans all Route definitions, identifies models without test coverage,
and generates test stubs using the canonical fixture-validate pattern.

Usage:
    python scripts/generate_model_tests.py --dry-run   # preview
    python scripts/generate_model_tests.py              # write stubs
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TESTS_MODELS_DIR = REPO_ROOT / "tests" / "models"
OUTPUT_FILE = TESTS_MODELS_DIR / "test_generated_stubs.py"
sys.path.insert(0, str(REPO_ROOT))

_SKIP_TYPES = {"str", "bytes", "dict", "bool", "int", "float", "None"}


def _to_snake(name: str) -> str:
    """Convert PascalCase to snake_case."""
    s1 = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def _strip_list(model: str) -> str:
    if model.startswith("List[") and model.endswith("]"):
        return model[5:-1]
    if model.startswith("list[") and model.endswith("]"):
        return model[5:-1]
    return model


def _find_existing_tests() -> set[str]:
    """Find all existing test method names across tests/models/ (excluding generated output)."""
    existing: set[str] = set()
    for py_file in TESTS_MODELS_DIR.glob("test_*.py"):
        if py_file == OUTPUT_FILE:
            continue
        content = py_file.read_text()
        for m in re.finditer(r"def (test_\w+)", content):
            existing.add(m.group(1))
    return existing


def _model_has_test(model_name: str, existing_tests: set[str]) -> bool:
    """Check if a model already has a test, handling naming variations."""
    test_name = f"test_{_to_snake(model_name)}"
    if test_name in existing_tests:
        return True
    # Fuzzy match: compare lowered names without underscores
    normalized = model_name.lower()
    for test in existing_tests:
        test_body = test.removeprefix("test_").replace("_", "")
        if normalized == test_body:
            return True
    return False


def _find_model_module(model_name: str) -> str | None:
    """Find which ab.api.models.* module defines this model."""
    models_dir = REPO_ROOT / "ab" / "api" / "models"
    for py_file in models_dir.glob("*.py"):
        if py_file.name.startswith("_"):
            continue
        content = py_file.read_text()
        if re.search(rf"^class {model_name}\b", content, re.MULTILINE):
            return py_file.stem
    return None


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Generate model test stubs")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    import json

    from ab.progress.route_index import index_all_routes, normalize_path

    routes = index_all_routes()
    existing_tests = _find_existing_tests()

    # Load gate baseline to skip models where G1 fails (test would always fail)
    baseline_file = REPO_ROOT / "tests" / "gate_baseline.json"
    baseline: dict[str, list[str]] = {}
    if baseline_file.exists():
        baseline = json.loads(baseline_file.read_text())

    # Collect models needing stubs
    stubs_needed: dict[str, dict] = {}  # model_name -> {method, path, is_list, module}
    for (_norm_path, method), route_info in routes.items():
        resp = route_info.response_model
        if not resp:
            continue
        is_list = resp.startswith("List[") or resp.startswith("list[")
        clean = _strip_list(resp)
        if clean in _SKIP_TYPES:
            continue
        if clean.startswith("PaginatedList"):
            continue

        if _model_has_test(clean, existing_tests):
            continue
        if clean in stubs_needed:
            continue

        # Skip models where G1 fails — test would always fail on extra fields
        baseline_key = f"{normalize_path(route_info.path)} {method}"
        if baseline and baseline_key in baseline and "G1" not in baseline[baseline_key]:
            continue

        module = _find_model_module(clean)
        test_name = f"test_{_to_snake(clean)}"
        stubs_needed[clean] = {
            "method": method,
            "path": route_info.path,
            "is_list": is_list,
            "module": module,
            "test_name": test_name,
        }

    if not stubs_needed:
        print("No missing test stubs found.")
        return

    # Group by module for imports
    by_module: dict[str, list[tuple[str, dict]]] = {}
    for model_name, info in sorted(stubs_needed.items()):
        mod = info["module"] or "unknown"
        by_module.setdefault(mod, []).append((model_name, info))

    if args.dry_run:
        print(f"Would generate {len(stubs_needed)} test stubs:")
        for mod, models in sorted(by_module.items()):
            print(f"\n  Module: ab.api.models.{mod}")
            for name, info in models:
                print(f"    {info['test_name']}: {name} ({info['method']} {info['path']})")
        return

    # Generate test file
    lines = [
        '"""Auto-generated model test stubs for G3 coverage.',
        '',
        'Generated by scripts/generate_model_tests.py.',
        'Each test validates fixture → model → no extra fields.',
        '"""',
        '',
    ]

    # Imports
    import_models: list[str] = []
    for mod, models in sorted(by_module.items()):
        names = sorted(name for name, _ in models)
        import_models.append(f"from ab.api.models.{mod} import (")
        for name in names:
            import_models.append(f"    {name},")
        import_models.append(")")

    lines.extend(import_models)
    lines.append("from tests.conftest import assert_no_extra_fields, first_or_skip, require_fixture")
    lines.append("")
    lines.append("")
    lines.append("class TestGeneratedStubs:")

    for model_name, info in sorted(stubs_needed.items(), key=lambda x: x[1]["test_name"]):
        lines.append(f"    def {info['test_name']}(self):")
        lines.append(f'        data = require_fixture("{model_name}", "{info["method"]}", "{info["path"]}")')
        if info["is_list"]:
            lines.append("        item = first_or_skip(data)")
            lines.append(f"        model = {model_name}.model_validate(item)")
        else:
            lines.append(f"        model = {model_name}.model_validate(data)")
        lines.append(f"        assert isinstance(model, {model_name})")
        lines.append("        assert_no_extra_fields(model)")
        lines.append("")

    content = "\n".join(lines)
    OUTPUT_FILE.write_text(content)
    print(f"Generated {len(stubs_needed)} test stubs in {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
