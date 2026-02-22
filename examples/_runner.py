"""Example runner with structured entries and automated fixture capture.

Provides :class:`ExampleRunner` for registering endpoint method
demonstrations as structured entries, executing them via CLI, and
saving response fixtures to ``tests/fixtures/``.

Usage in an example file::

    from examples._runner import ExampleRunner

    runner = ExampleRunner("Address", env="staging")

    runner.add(
        "validate",
        lambda api: api.address.validate(street="123 Main St", city="Columbus", state="OH", zip_code="43213"),
        response_model="AddressIsValidResult",
        fixture_file="AddressIsValidResult.json",
    )

    if __name__ == "__main__":
        runner.run()

Run from the repo root::

    python -m examples.address             # run all entries
    python -m examples.address validate    # run one entry
    python -m examples.address --list      # show entry metadata
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "tests" / "fixtures"
REQUESTS_DIR = FIXTURES_DIR / "requests"


@dataclass
class ExampleEntry:
    """A single endpoint method demonstration with capture metadata."""

    name: str
    call: Callable[..., Any]
    response_model: Optional[str] = None
    request_model: Optional[str] = None
    fixture_file: Optional[str] = None
    request_fixture_file: Optional[str] = None


class ExampleRunner:
    """Manages structured example entries and automated fixture capture.

    Parameters
    ----------
    title:
        Display name for this example group (e.g. ``"Address"``).
    **api_kwargs:
        Keyword arguments forwarded to :class:`ab.ABConnectAPI`.
    """

    def __init__(self, title: str, **api_kwargs: Any) -> None:
        self.title = title
        self.api_kwargs = api_kwargs
        self.entries: list[ExampleEntry] = []
        self._api: Any = None

    @property
    def api(self) -> Any:
        """Lazy-initialised ABConnectAPI client."""
        if self._api is None:
            from ab import ABConnectAPI

            self._api = ABConnectAPI(**self.api_kwargs)
        return self._api

    def add(
        self,
        name: str,
        call: Callable[..., Any],
        *,
        response_model: Optional[str] = None,
        request_model: Optional[str] = None,
        fixture_file: Optional[str] = None,
        request_fixture_file: Optional[str] = None,
    ) -> None:
        """Register a structured entry."""
        self.entries.append(
            ExampleEntry(
                name=name,
                call=call,
                response_model=response_model,
                request_model=request_model,
                fixture_file=fixture_file,
                request_fixture_file=request_fixture_file,
            )
        )

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def run(self, names: list[str] | None = None) -> None:
        """Execute entries selected by *names* or ``sys.argv``."""
        if names is None:
            args = sys.argv[1:]
        else:
            args = list(names)

        if "--list" in args:
            self._list_entries()
            return

        if args:
            targets = [e for e in self.entries if e.name in args]
            unknown = set(args) - {e.name for e in self.entries}
            if unknown:
                print(f"Unknown entries: {', '.join(sorted(unknown))}")
                print(f"Available: {', '.join(e.name for e in self.entries)}")
                return
        else:
            targets = list(self.entries)

        for entry in targets:
            self._run_entry(entry)

    def _list_entries(self) -> None:
        """Print metadata for every registered entry."""
        print(f"\n  {self.title} — {len(self.entries)} entries\n")
        print(f"  {'Name':<25} {'Resp Model':<25} {'Req Model':<22} {'Fixture':<28} {'Req Fixture'}")
        print(f"  {'─' * 25} {'─' * 25} {'─' * 22} {'─' * 28} {'─' * 25}")
        for e in self.entries:
            print(
                f"  {e.name:<25} "
                f"{(e.response_model or '—'):<25} "
                f"{(e.request_model or '—'):<22} "
                f"{(e.fixture_file or '—'):<28} "
                f"{e.request_fixture_file or '—'}"
            )
        print()

    @staticmethod
    def _load_request_data(filename: str) -> dict:
        """Load a request fixture JSON file from ``tests/fixtures/requests/``."""
        path = REQUESTS_DIR / filename
        return json.loads(path.read_text())

    @staticmethod
    def _fixture_to_kwargs(model_name: str, data: dict) -> dict:
        """Convert fixture alias keys to Python field names using model metadata."""
        import ab.api.models as models_pkg

        model_cls = getattr(models_pkg, model_name, None)
        if model_cls is None:
            return data
        alias_map: dict[str, str] = {}
        for field_name, field_info in model_cls.model_fields.items():
            alias = field_info.alias if field_info.alias else field_name
            alias_map[alias] = field_name
        return {alias_map.get(k, k): v for k, v in data.items()}

    def _run_entry(self, entry: ExampleEntry) -> None:
        """Execute a single entry: call → display → save fixture."""
        print(f"\n{'=' * 64}")
        print(f"  {self.title} :: {entry.name}")
        if entry.response_model:
            print(f"  Response Model : {entry.response_model}")
        if entry.request_model:
            print(f"  Request Model  : {entry.request_model}")
        if entry.fixture_file:
            print(f"  Fixture        : tests/fixtures/{entry.fixture_file}")
        if entry.request_fixture_file:
            print(f"  Req Fixture    : tests/fixtures/requests/{entry.request_fixture_file}")
        print(f"{'=' * 64}\n")

        try:
            if entry.request_fixture_file:
                raw = self._load_request_data(entry.request_fixture_file)
                if entry.request_model:
                    data = self._fixture_to_kwargs(entry.request_model, raw)
                else:
                    data = raw
                result = entry.call(self.api, data)
            else:
                result = entry.call(self.api)
        except Exception as exc:
            print(f"  ERROR: {exc}")
            return

        if result is None:
            print("  (no content)")
            return

        print(f"  Result: {_summarise(result)}")

        if entry.fixture_file and result is not None:
            self._save_fixture(result, entry)

    # ------------------------------------------------------------------
    # Fixture persistence
    # ------------------------------------------------------------------

    def _save_fixture(self, result: Any, entry: ExampleEntry) -> None:
        """Serialise *result* to JSON and write to the fixtures directory."""
        from pydantic import BaseModel

        if isinstance(result, list):
            data: Any = [
                item.model_dump(by_alias=True, mode="json")
                if isinstance(item, BaseModel)
                else item
                for item in result
            ]
        elif isinstance(result, BaseModel):
            data = result.model_dump(by_alias=True, mode="json")
        elif isinstance(result, bytes):
            print("  (binary response — fixture save skipped)")
            return
        else:
            data = result

        path = FIXTURES_DIR / entry.fixture_file
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        print(f"  Fixture saved → {path}")


def _summarise(obj: Any, max_len: int = 200) -> str:
    """Return a truncated string representation of *obj*."""
    text = repr(obj)
    if len(text) > max_len:
        return text[: max_len - 3] + "..."
    return text
