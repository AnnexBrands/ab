# Phase 1 Data Model: Example Coverage

**Feature**: 037-example-coverage · **Date**: 2026-06-05

These are the in-memory structures and on-disk artifacts the feature introduces or
extends. They are dataclasses/JSON (not pydantic API models) — internal tooling state,
consistent with the existing `ab/progress/models.py` style.

---

## Enum: RunStatus

The per-endpoint verification status. Single source of truth for the report column,
the gate, and the results artifact.

| Value | Meaning | How reached |
|-------|---------|-------------|
| `passing` | Example ran (or was pasted) and output matches the fixture. | Live harness diff equal, or ingest of a validated paste. |
| `failing` | Read-only example ran but output ≠ fixture. | Live harness diff not equal (after volatile normalization). |
| `awaiting_data` | Read-only (GET) with an example but no fixture / no usable `TEST_*` constant. | Derived (no artifact entry) or harness could not run. |
| `awaiting_paste` | Mutating endpoint (POST/PUT/PATCH/DELETE) — never auto-run. | Derived from `route.method`. |
| `binary` | Response is bytes / no-content; covered-as-binary, excluded from comparison. | Derived from response type (D10). |
| `missing_example` | No canonical example exists for the endpoint. | Derived: not in example index. |

**Coverage rule**: an endpoint is *covered* (passes the gate, SC-005) iff its status is
anything other than `missing_example`. An endpoint is *verified-green* (SC-002) iff
`passing`. `binary` is covered but never compared.

---

## Extended: MethodProgress (`ab/progress/models.py`)

Add one field to the existing dataclass (additive — no field removed):

```text
MethodProgress:
  ... existing fields (dotted_path, method_name, http_method, http_path,
      return_type, has_example, has_cli, has_route, path_sub_root,
      has_docstring, gate_status) ...
  run_status: RunStatus            # NEW — defaults to derived value when no artifact
  run_checked: str | None = None   # NEW — ISO date from the results artifact, if any
  run_detail: str | None = None    # NEW — short diff/why summary for failing/awaiting
```

`has_example` is recomputed by the precise `example_index` (D9) and now means
"covered by a **canonical** plain-script example resolving to this route."

---

## New: CanonicalExample (`ab/progress/example_index.py`)

The result of statically mapping endpoints → their one canonical example.

```text
CanonicalExample:
  endpoint_key: str        # "api.<group>[.<sub>].<method>"  (matches registry)
  group: str               # registry group name, e.g. "jobs.payment"
  method_name: str         # e.g. "list"
  example_path: str        # "examples/jobs/payment.py" (relative)
  is_canonical: bool       # True only for non-underscore plain scripts
  is_legacy_runner: bool   # True if backed only by a "_"-prefixed/runner file
```

Index API: `build_example_index() -> dict[endpoint_key, CanonicalExample]`, plus
`uncovered_endpoints()` and `legacy_only_endpoints()` helpers used by the gate (D8).

---

## New on-disk artifact: `tests/example_run_results.json` (committed)

Last-verified run status per endpoint, written by `scripts/run_examples.py` and by
`scripts/ingest_captures.py`, read by `report.py`. Stable key order for no-drift.
Full contract: `contracts/example_run_results.schema.json`.

```json
{
  "schema": 1,
  "results": {
    "api.dashboard.get_grid_views": {
      "status": "passing",
      "checked": "2026-06-05",
      "source": "live",
      "fixture": "GridViewInfo.json",
      "detail": null
    },
    "api.jobs.payment.add": {
      "status": "passing",
      "checked": "2026-06-05",
      "source": "paste",
      "fixture": "JobPayment.json",
      "detail": null
    }
  }
}
```

- `source`: `live` (auto-run), `paste` (ingested), or `binary`.
- Entries are only written for endpoints that were actually verified; derived statuses
  are NOT persisted (kept computed, so adding/removing a route needs no artifact edit).

---

## New transient artifact: `captures.json` (operator export, not committed)

Produced client-side by the report's "Download captures.json" button; consumed by
`scripts/ingest_captures.py`. Full contract: `contracts/captures.schema.json`.

```json
{
  "schema": 1,
  "captures": {
    "api.jobs.payment.add": {
      "endpoint": "api.jobs.payment.add",
      "http_method": "POST",
      "path": "/job/{jobId}/payment",
      "response_model": "JobPayment",
      "request_model": "JobPaymentRequest",
      "response": { "...": "pasted real JSON response" },
      "request":  { "...": "pasted real JSON request body (optional)" }
    }
  }
}
```

`response`/`request` are the operator's pasted JSON (parsed; if unparseable the JS keeps
the raw string and ingest reports it as malformed → FR-013).

---

## Relationships

```text
Route (live code)
  │  normalize_path+method → registry key (api.<group>.<method>)
  ├──> CanonicalExample      (example_index: which plain script calls it)
  ├──> Fixture file          (derive_fixtures_from_routes: tests/fixtures/<Model>.json)
  ├──> RunStatus             (artifact entry OR derived from method+example+fixture)
  └──> MethodProgress        (renderer row: + Run column + paste block)

captures.json ──ingest──> Fixture file + CanonicalExample + results-artifact entry
live harness  ──verify──> results-artifact entry (passing/failing) + optional re-capture
```

---

## Validation rules (from FRs)

- An endpoint with `run_status == missing_example` MUST fail the coverage gate (FR-008).
- Ingest MUST construct the response model from a paste before writing a fixture; failure
  MUST NOT write a fixture (FR-013).
- Mutating endpoints MUST never appear with `source == "live"` in the results artifact
  (FR-006) — only `paste`.
- The results artifact and the generated report MUST be byte-stable across regenerations
  with unchanged inputs (FR-007 / no-drift); key ordering is sorted.
- `binary` endpoints MUST NOT carry a fixture-comparison result (FR-017).
