# Contract: Canonical Example File + Capture Helper

**Feature**: 037-example-coverage · **Date**: 2026-06-05

Defines the shape every **canonical** example MUST follow and the `examples/_capture.py`
helper API the harness depends on. This is the interface the coverage gate (D8), the
live harness (D1), and the example generator/ingest (D9/D7) all rely on.

---

## 1. Canonical example file shape

A canonical example is a **plain `main()` script** under `examples/` whose filename does
**not** begin with `_`. Reference implementation: `examples/dashboard.py`. It MUST:

1. Carry a module docstring ending with the endpoint's RTD link
   (`https://ab-sdk.readthedocs.io/en/latest/api/<group>.html`).
2. `from ab import ABConnectAPI` and construct `api = ABConnectAPI(env="staging")`.
3. `from examples._capture import save` (the shared helper, §2) and
   `from ab.cli.formatter import format_result`.
4. Make a **real** call: `result = api.<group>[.<sub>].<method>(<args from TEST_* constants>)`.
5. **Print** the response: `print(format_result(result))`.
6. **Save** it: `save("<Model>.json", result)` (single) or the list form.
7. Expose `def main() -> None:` and the `if __name__ == "__main__": main()` guard so the
   `examples/__main__.py` dispatcher and the harness can run it.

A file MAY demonstrate several methods of the same group (one `print`+`save` per call), as
the existing plain examples do. Coverage is computed per `api.<group>.<method>` call found
(D9), so multi-call files are fine.

A canonical example MUST NOT import `examples._runner` / `ExampleRunner` (that is the
deprecated path; such files are not canonical).

### Generated skeleton (emitted by the generator / ingest)

```python
"""Example: <Group> <method>.

Live SDK example — real call, real printed pydantic response.
See also: https://ab-sdk.readthedocs.io/en/latest/api/<group>.html
"""
from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import save
from examples.constants import TEST_...  # only what the call needs


def main() -> None:
    api = ABConnectAPI(env="staging")

    print("\n# api.<group>.<method>(...)")
    result = api.<group>.<method>(...)
    print(format_result(result))
    save("<Model>.json", result)


if __name__ == "__main__":
    main()
```

---

## 2. `examples/_capture.py` helper API

A single shared helper replaces each example's bespoke `_save` and adds harness
redirection. Signature and behavior:

```python
def save(name: str, payload: Any) -> Path:
    """Serialize *payload* (pydantic model, list of models, or JSON-able) and write it.

    Destination:
      - If env AB_EXAMPLE_CAPTURE_DIR is set  -> <that dir>/<name>   (verify mode)
      - Otherwise                              -> tests/fixtures/<name> (capture mode)

    Serialization (identical to format_result/dashboard._save):
      - BaseModel        -> model_dump(by_alias=True, mode="json")
      - list[BaseModel]  -> [item.model_dump(by_alias=True, mode="json"), ...]
      - bytes            -> NO file written; returns None and prints a binary note (D10)
      - other JSON-able  -> written as-is
    Output is json.dumps(..., indent=2, ensure_ascii=False) + "\n" (matches existing
    fixtures so a re-capture is byte-identical and verifies clean).
    Returns the path written, or None for binary/skipped.
    """
```

Contract guarantees relied on by the harness:

- **Same bytes**: a value captured via `save()` in capture mode equals (after volatile
  normalization) what `ingest_captures.py` writes for the same value — so a freshly
  pasted/captured fixture immediately verifies `passing`.
- **Redirection is total**: in verify mode `save()` MUST NOT touch `tests/fixtures/`.
- **Binary-safe**: bytes payloads never produce a fixture (supports the `binary` status).

---

## 3. Harness ↔ example interface (D1)

```text
scripts/run_examples.py, per read-only endpoint:
  1. tmp = mkdtemp()
  2. subprocess: AB_EXAMPLE_CAPTURE_DIR=tmp  python -m examples <module>   (or run file)
  3. read tmp/<Model>.json  (produced by save())
  4. compare to tests/fixtures/<Model>.json via example_verify.compare() (D2/D3)
  5. record result -> tests/example_run_results.json   (status passing|failing)
Mutating endpoints are skipped here (status derived awaiting_paste; never run).
```

Exit/usage:
- `python scripts/run_examples.py` — run all read-only, write results, print summary.
- `python scripts/run_examples.py --group jobs.timeline` — scope to a group.
- `python scripts/run_examples.py --capture` — re-capture fixtures from live (capture
  mode, overwrites `tests/fixtures/`), for the lock-step refresh.
- Marked `@pytest.mark.live` when invoked from the test suite; never on the CI no-live path.

---

## 4. Coverage gate interface (D8) — non-live

```text
tests/test_example_coverage.py:
  idx = build_example_index()
  uncovered = [k for k in routed_endpoint_keys() if k not in idx or not idx[k].is_canonical]
  assert not uncovered, f"endpoints lacking a canonical example: {uncovered}"
  # companion (warning→error as migration completes):
  legacy = [k for k,v in idx.items() if v.is_legacy_runner]
  assert not legacy, f"endpoints still backed only by deprecated runner: {legacy}"
```

`routed_endpoint_keys()` derives from live `Route` objects (the existing
`discover_endpoints_from_class()` / `route_index`), so a new route with no example fails
CI automatically (FR-001/FR-008).
