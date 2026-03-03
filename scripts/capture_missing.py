#!/usr/bin/env python3
"""Batch capture missing fixtures for G2-failing endpoints.

Parses FIXTURES.md for G2=FAIL endpoints, locates matching example
entries in ``examples/``, and runs them to capture fixture files.

Usage:
    python scripts/capture_missing.py --dry-run   # preview
    python scripts/capture_missing.py              # run captures
"""

from __future__ import annotations

import importlib
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES_MD = REPO_ROOT / "FIXTURES.md"
EXAMPLES_DIR = REPO_ROOT / "examples"
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures"
sys.path.insert(0, str(REPO_ROOT))

_SKIP_MODELS = {"None", "str", "bytes", "dict", "bool", "int", "float", "—"}


def _parse_g2_failures() -> list[dict]:
    """Parse FIXTURES.md for endpoints where G2=FAIL.

    Returns list of dicts: {path, method, pypath, resp_model, notes}.
    """
    content = FIXTURES_MD.read_text()
    failures: list[dict] = []

    for line in content.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|") if c.strip()]
        if len(cells) < 11:
            continue
        # Skip header/separator rows
        if cells[0] in ("Endpoint", "---") or cells[0].startswith("--"):
            continue

        # Column layout: 0=Path, 1=Method, 2=PyPath, 3=ReqModel,
        #   4=RespModel, 5=G1, 6=G2, 7=G3, 8=G4, 9=G5, 10=G6
        resp_model = cells[4].strip()
        g2 = cells[6].strip()

        if g2 != "FAIL":
            continue
        if resp_model in _SKIP_MODELS:
            continue
        if resp_model.startswith("PaginatedList"):
            continue

        # Strip List[...] wrapper
        clean = resp_model
        if clean.startswith("List[") and clean.endswith("]"):
            clean = clean[5:-1]

        failures.append({
            "path": cells[0],
            "method": cells[1],
            "pypath": cells[2],
            "resp_model": clean,
            "notes": cells[-1] if len(cells) > 11 else "",
        })

    return failures


def _discover_example_entries() -> dict[str, list[dict]]:
    """Discover all example entries across example modules.

    Returns {fixture_stem: [{module, entry_name, resp_model}]}.
    """
    entries: dict[str, list[dict]] = {}

    for py_file in sorted(EXAMPLES_DIR.glob("*.py")):
        if py_file.name.startswith("_"):
            continue

        module_name = f"examples.{py_file.stem}"
        try:
            mod = importlib.import_module(module_name)
        except Exception:
            continue

        runner = getattr(mod, "runner", None)
        if runner is None:
            continue

        for entry in runner.entries:
            if not entry.fixture_file:
                continue
            stem = Path(entry.fixture_file).stem
            entries.setdefault(stem, []).append({
                "module": module_name,
                "entry_name": entry.name,
                "resp_model": entry.response_model,
            })

    return entries


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Batch capture missing fixtures")
    parser.add_argument("--dry-run", action="store_true", help="Preview without running")
    args = parser.parse_args()

    failures = _parse_g2_failures()
    if not failures:
        print("No G2=FAIL endpoints found.")
        return

    example_entries = _discover_example_entries()

    # Match failures to example entries by response model name
    matched: list[dict] = []
    unmatched: list[dict] = []

    for fail in failures:
        model = fail["resp_model"]
        if model in example_entries:
            fail["examples"] = example_entries[model]
            matched.append(fail)
        else:
            unmatched.append(fail)

    print(f"Processing {len(failures)} endpoints with G2=FAIL...\n")

    if args.dry_run:
        for item in matched:
            exs = item["examples"]
            mod = exs[0]["module"]
            entry = exs[0]["entry_name"]
            print(f"  [HAS-EXAMPLE] {item['method']:>6} {item['path']}")
            print(f"                → {mod}::{entry} (fixture: {item['resp_model']}.json)")
        for item in unmatched:
            print(f"  [NO-EXAMPLE]  {item['method']:>6} {item['path']} → {item['resp_model']}")

        print(f"\nSummary:")
        print(f"  With examples: {len(matched)}")
        print(f"  No example:    {len(unmatched)}")
        print(f"  Total:         {len(failures)}")
        return

    # Run captures
    captured = 0
    failed = 0

    for item in matched:
        ex = item["examples"][0]
        model = item["resp_model"]
        fixture_path = FIXTURES_DIR / f"{model}.json"
        existed_before = fixture_path.exists()

        print(f"\n  Running {ex['module']}::{ex['entry_name']} for {model}...")

        try:
            result = subprocess.run(
                [sys.executable, "-m", ex["module"], ex["entry_name"]],
                cwd=str(REPO_ROOT),
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode != 0:
                print(f"  [FAILED]   {item['method']:>6} {item['path']} → exit code {result.returncode}")
                if result.stderr:
                    # Show last line of stderr for context
                    last_err = result.stderr.strip().splitlines()[-1]
                    print(f"             {last_err}")
                failed += 1
                continue

            if fixture_path.exists() and (not existed_before or fixture_path.stat().st_mtime > 0):
                print(f"  [CAPTURED] {item['method']:>6} {item['path']} → {model}.json")
                captured += 1
            else:
                print(f"  [FAILED]   {item['method']:>6} {item['path']} → fixture not written")
                failed += 1

        except subprocess.TimeoutExpired:
            print(f"  [FAILED]   {item['method']:>6} {item['path']} → timeout (30s)")
            failed += 1
        except Exception as exc:
            print(f"  [FAILED]   {item['method']:>6} {item['path']} → {exc}")
            failed += 1

    for item in unmatched:
        print(f"  [NO-EXAMPLE] {item['method']:>6} {item['path']} → No example in examples/")

    print(f"\nSummary:")
    print(f"  Captured:    {captured}")
    print(f"  Failed:      {failed}")
    print(f"  No example:  {len(unmatched)}")
    print(f"  Total:       {len(failures)}")


if __name__ == "__main__":
    main()
