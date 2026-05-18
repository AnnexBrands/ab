"""Package dispatcher for ``python -m examples.jobs``."""

from __future__ import annotations

import sys

from examples.__main__ import _discover_runners, _list_all
from examples.__main__ import main as examples_main


def main(argv: list[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    registry = {
        name: target
        for name, target in _discover_runners().items()
        if name.startswith("jobs.")
    }

    if not args or args == ["--list"]:
        _list_all(registry)
        return

    subgroup = args[0]
    if not subgroup.startswith("jobs."):
        subgroup = f"jobs.{subgroup}"
    examples_main([subgroup, *args[1:]])


if __name__ == "__main__":
    main()
