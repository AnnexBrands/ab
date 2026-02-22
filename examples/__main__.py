"""Unified example dispatcher with module aliases and prefix matching.

Run examples from the repo root::

    python -m examples --list                  # list all modules
    python -m examples contacts                # run all contacts entries
    python -m examples contacts.get_details    # run one entry (dot syntax)
    python -m examples cont.get_d              # prefix match
    ex addr.val                                # console script + alias
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from ab.cli.aliases import ALIASES


def _discover_runners() -> dict[str, object]:
    """Import each example module and return ``{name: runner}``."""
    registry: dict[str, object] = {}
    examples_dir = Path(__file__).resolve().parent
    for path in sorted(examples_dir.glob("*.py")):
        if path.name.startswith("_"):
            continue
        module_name = path.stem
        # Import from file path directly to avoid namespace-package collisions
        # when other editable installs (e.g. ABConnectTools) also have examples/.
        qual = f"examples.{module_name}"
        spec = importlib.util.spec_from_file_location(qual, path)
        if spec is None or spec.loader is None:
            continue
        mod = importlib.util.module_from_spec(spec)
        sys.modules[qual] = mod
        spec.loader.exec_module(mod)
        runner = getattr(mod, "runner", None)
        if runner is not None:
            registry[module_name] = runner
    return registry


def _resolve_module(name: str, registry: dict[str, object]) -> tuple[str, object] | None:
    """Resolve *name* to a ``(module_name, runner)`` via exact/alias/prefix match."""
    # Exact module name
    if name in registry:
        return name, registry[name]

    # Exact alias
    if name in ALIASES and ALIASES[name] in registry:
        return ALIASES[name], registry[ALIASES[name]]

    # Prefix match on module names
    matches = [(k, v) for k, v in registry.items() if k.startswith(name)]

    # Prefix match on alias keys
    alias_matches = [
        (ALIASES[k], registry[ALIASES[k]]) for k in ALIASES if k.startswith(name) and ALIASES[k] in registry
    ]
    # Merge, dedup by module name
    seen = {m for m, _ in matches}
    for mod_name, runner in alias_matches:
        if mod_name not in seen:
            matches.append((mod_name, runner))
            seen.add(mod_name)

    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        names = ", ".join(sorted(m for m, _ in matches))
        print(f"Ambiguous module '{name}' — matches: {names}")
        return None
    print(f"Unknown module '{name}'")
    print(f"Available: {', '.join(sorted(registry))}")
    return None


def _resolve_entry(name: str, runner: object) -> object | None:
    """Resolve *name* to an entry within *runner* via exact or prefix match."""
    entries = runner.entries  # type: ignore[attr-defined]

    # Exact match
    for entry in entries:
        if entry.name == name:
            return entry

    # Prefix match
    matches = [e for e in entries if e.name.startswith(name)]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        names = ", ".join(e.name for e in matches)
        print(f"Ambiguous entry '{name}' — matches: {names}")
        return None

    print(f"Unknown entry '{name}'")
    print(f"Available: {', '.join(e.name for e in entries)}")
    return None


def _list_all(registry: dict[str, object]) -> None:
    """Print all modules with entry counts and aliases."""
    reverse_aliases: dict[str, list[str]] = {}
    for alias, mod in ALIASES.items():
        reverse_aliases.setdefault(mod, []).append(alias)

    total_entries = 0
    print(f"\n  {'Module':<20} {'Entries':>7}   Aliases")
    print(f"  {'─' * 20} {'─' * 7}   {'─' * 30}")
    for name in sorted(registry):
        runner = registry[name]
        count = len(runner.entries)  # type: ignore[attr-defined]
        total_entries += count
        aliases = ", ".join(sorted(reverse_aliases.get(name, []))) or "—"
        print(f"  {name:<20} {count:>7}   {aliases}")
    print(f"\n  {len(registry)} modules, {total_entries} entries\n")


def main(argv: list[str] | None = None) -> None:
    """Entry point for ``python -m examples`` and the ``ex`` console script."""
    args = argv if argv is not None else sys.argv[1:]
    registry = _discover_runners()

    # No args or --list → show all modules
    if not args or args == ["--list"]:
        _list_all(registry)
        return

    raw = args[0]

    # Dot syntax: module.entry
    if "." in raw:
        mod_part, entry_part = raw.split(".", 1)
        resolved = _resolve_module(mod_part, registry)
        if resolved is None:
            sys.exit(1)
        mod_name, runner = resolved
        entry = _resolve_entry(entry_part, runner)
        if entry is None:
            sys.exit(1)
        runner.run([entry.name])  # type: ignore[attr-defined]
        return

    # Space syntax or bare module
    resolved = _resolve_module(raw, registry)
    if resolved is None:
        sys.exit(1)
    mod_name, runner = resolved

    rest = args[1:]
    if not rest:
        # bare module → run all entries
        runner.run([])  # type: ignore[attr-defined]
        return

    if rest == ["--list"]:
        runner._list_entries()  # type: ignore[attr-defined]
        return

    # Space-separated entry name(s)
    entry = _resolve_entry(rest[0], runner)
    if entry is None:
        sys.exit(1)
    runner.run([entry.name])  # type: ignore[attr-defined]


if __name__ == "__main__":
    main()
