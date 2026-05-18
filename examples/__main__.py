"""Unified example dispatcher with module aliases and prefix matching.

Run examples from the repo root::

    python -m examples --list                  # list all modules
    python -m examples notes                   # run one plain example
    python -m examples jobs.notes              # run one package example
    python -m examples contacts.get_details    # run one runner entry (dot syntax)
    python -m examples cont.get_d              # prefix match
    ex addr.val                                # console script + alias
"""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any, Callable

from ab.cli.aliases import ALIASES


@dataclass
class ExampleTarget:
    """Runnable example module.

    A target is either a legacy ``ExampleRunner`` module or a plain script
    exposing ``main()``. New examples should use ``main()``.
    """

    name: str
    module: ModuleType
    runner: Any | None = None
    main: Callable[[], None] | None = None

    @property
    def entries(self) -> list[Any]:
        if self.runner is None:
            return []
        return list(self.runner.entries)

    def run(self, args: list[str] | None = None) -> None:
        if self.runner is not None:
            self.runner.run(args)
            return
        if args:
            print(f"Example '{self.name}' does not define entries; run it without an entry name.")
            return
        if self.main is None:
            print(f"Example '{self.name}' is not runnable.")
            return
        self.main()

    def list_entries(self) -> None:
        if self.runner is not None:
            self.runner._list_entries()
            return
        print(f"\n  {self.name} — plain script")
        if self.main is not None:
            print(f"  Run: ex {self.name}\n")
        else:
            print("  No main() found.\n")


def _is_runnable_source(path: Path) -> bool:
    """Return whether *path* is safe to import for example discovery.

    Some old snippet files instantiate ``ABConnectAPI`` and call live routes at
    import time. Restricting discovery imports to modules that visibly expose a
    runner or ``main()`` avoids triggering those side effects.
    """
    source = path.read_text(encoding="utf-8")
    return "runner =" in source or "def main(" in source


def _import_module_from_path(qual: str, path: Path) -> ModuleType | None:
    """Import a module by file path, avoiding namespace-package collisions."""
    spec = importlib.util.spec_from_file_location(qual, path)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[qual] = mod
    spec.loader.exec_module(mod)
    return mod


def _register_module(registry: dict[str, ExampleTarget], name: str, path: Path) -> None:
    """Import and register *path* when it exposes a runner or ``main()``."""
    if not _is_runnable_source(path):
        return
    qual = f"examples.{name}"
    mod = _import_module_from_path(qual, path)
    if mod is None:
        return
    runner = getattr(mod, "runner", None)
    main = getattr(mod, "main", None)
    if runner is None and main is None:
        return
    registry[name] = ExampleTarget(
        name=name,
        module=mod,
        runner=runner,
        main=main if callable(main) else None,
    )


def _discover_runners() -> dict[str, ExampleTarget]:
    """Import runnable examples and return ``{name: ExampleTarget}``."""
    registry: dict[str, ExampleTarget] = {}
    examples_dir = Path(__file__).resolve().parent

    for path in sorted(examples_dir.glob("*.py")):
        if path.name.startswith("_"):
            continue
        if path.stem in {"__init__", "__main__"}:
            continue
        _register_module(registry, path.stem, path)

    for package_dir in sorted(p for p in examples_dir.iterdir() if p.is_dir()):
        if package_dir.name.startswith("_"):
            continue
        if not (package_dir / "__init__.py").exists():
            continue
        for path in sorted(package_dir.glob("*.py")):
            if path.name.startswith("_") or path.stem in {"__init__", "__main__"}:
                continue
            _register_module(registry, f"{package_dir.name}.{path.stem}", path)

    return registry


def _resolve_module(name: str, registry: dict[str, ExampleTarget]) -> tuple[str, ExampleTarget] | None:
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


def _resolve_entry(name: str, target: ExampleTarget) -> object | None:
    """Resolve *name* to an entry within *runner* via exact or prefix match."""
    entries = target.entries

    if not entries:
        print(f"Example '{target.name}' does not define entries; run it as 'ex {target.name}'.")
        return None

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


def _list_all(registry: dict[str, ExampleTarget]) -> None:
    """Print all modules with entry counts and aliases."""
    reverse_aliases: dict[str, list[str]] = {}
    for alias, mod in ALIASES.items():
        reverse_aliases.setdefault(mod, []).append(alias)

    total_entries = 0
    print(f"\n  {'Module':<20} {'Entries':>7}   Aliases")
    print(f"  {'─' * 20} {'─' * 7}   {'─' * 30}")
    for name in sorted(registry):
        target = registry[name]
        count = len(target.entries)
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

    # Prefer exact runnable module names before interpreting dots as
    # legacy runner entry syntax. This lets package examples run as
    # ``ex jobs.notes``.
    if raw in registry:
        target = registry[raw]
        rest = args[1:]
        if rest == ["--list"]:
            target.list_entries()
            return
        target.run(rest)
        return

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
        runner.run([entry.name])
        return

    # Space syntax or bare module
    resolved = _resolve_module(raw, registry)
    if resolved is None:
        sys.exit(1)
    mod_name, runner = resolved

    rest = args[1:]
    if not rest:
        # bare module → run all entries
        runner.run([])
        return

    if rest == ["--list"]:
        runner.list_entries()
        return

    # Space-separated entry name(s)
    entry = _resolve_entry(rest[0], runner)
    if entry is None:
        sys.exit(1)
    runner.run([entry.name])


if __name__ == "__main__":
    main()
