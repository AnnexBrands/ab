"""Shared capture helper for canonical examples.

Every canonical (plain-script) example imports :func:`save` to persist the response
it just printed. This replaces each example's bespoke ``_save`` and adds the one
piece of magic the run-and-verify harness depends on: **destination redirection**.

- Normal use (an operator running ``python -m examples dashboard``): ``save`` writes
  the fixture to ``tests/fixtures/<name>`` — examples are the fixture-capture
  instrument (Constitution II).
- Harness use (``scripts/run_examples.py``): the harness sets
  ``AB_EXAMPLE_CAPTURE_DIR`` before running the example in a subprocess; ``save``
  then writes to that directory instead, so the harness can diff the freshly
  produced JSON against the committed fixture **without touching** ``tests/fixtures/``.

Serialization is byte-identical to ``examples/dashboard.py``'s original ``_save`` and
to ``ab.cli.formatter.format_result`` (``model_dump(by_alias=True, mode="json")``),
so a re-capture or an ingested paste produces the same bytes a prior capture did.

See ``specs/037-example-coverage/contracts/example-contract.md`` §2.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

#: Environment variable the harness sets to redirect captures to a temp dir.
CAPTURE_DIR_ENV = "AB_EXAMPLE_CAPTURE_DIR"

#: Default destination — the committed fixtures directory.
FIXTURES_DIR = Path(__file__).resolve().parent.parent / "tests" / "fixtures"
#: Request fixtures (bodies / params) live here.
REQUESTS_DIR = FIXTURES_DIR / "requests"


def load_request(name: str) -> dict:
    """Load a request fixture (body or params) from ``tests/fixtures/requests/``.

    Lets a plain example demonstrate a POST/param call with the same real request
    data the operator captured, e.g. ``api.address.validate(**load_request(
    "AddressValidateParams.json"))``.
    """
    return json.loads((REQUESTS_DIR / name).read_text(encoding="utf-8"))


def capture_dir() -> Path:
    """Return the directory ``save`` writes to.

    ``AB_EXAMPLE_CAPTURE_DIR`` when set (harness verify mode), else
    ``tests/fixtures/`` (operator capture mode).
    """
    override = os.environ.get(CAPTURE_DIR_ENV)
    return Path(override) if override else FIXTURES_DIR


#: Env var an operator sets to opt INTO running state-mutating example calls.
RUN_MUTATIONS_ENV = "AB_RUN_MUTATIONS"


def mutations_enabled() -> bool:
    """True only when the operator explicitly opts into mutating calls.

    Examples wrap create/update/delete (and other state-writing) calls in
    ``if mutations_enabled():`` so a default run — and the verify harness, which
    never sets this — exercises only the safe read-only calls. Set
    ``AB_RUN_MUTATIONS=1`` to run them deliberately.
    """
    return os.environ.get(RUN_MUTATIONS_ENV, "").strip().lower() in {"1", "true", "yes", "on"}


def to_jsonable(payload: Any) -> Any:
    """Convert *payload* to the JSON shape fixtures are stored in.

    - ``BaseModel``        -> ``model_dump(by_alias=True, mode="json")``
    - ``list``             -> element-wise (models dumped, others passed through)
    - other JSON-able      -> returned as-is
    """
    from pydantic import BaseModel

    if isinstance(payload, list):
        return [
            item.model_dump(by_alias=True, mode="json")
            if isinstance(item, BaseModel)
            else item
            for item in payload
        ]
    if isinstance(payload, BaseModel):
        return payload.model_dump(by_alias=True, mode="json")
    return payload


def save(name: str, payload: Any) -> Path | None:
    """Serialize *payload* and write it to ``<capture_dir>/<name>``.

    Binary (``bytes``) payloads are never written (they cannot be a JSON fixture);
    a note is printed and ``None`` is returned (supports the ``binary`` run status).

    Returns the path written, or ``None`` for binary/skipped payloads.
    """
    if isinstance(payload, bytes):
        print(f"  (binary response, {len(payload)} bytes — fixture save skipped)")
        return None

    # An empty live result (no data on the test account) must NOT overwrite a
    # committed fixture that may hold real captured rows.
    if isinstance(payload, list) and not payload:
        print(f"  (empty list — not overwriting {capture_dir() / name})")
        return None

    data = to_jsonable(payload)
    out = capture_dir() / name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  saved -> {out}")
    return out
