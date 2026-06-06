# Phase 0 Research & Design Decisions: Example Coverage

**Feature**: 037-example-coverage · **Date**: 2026-06-05

This resolves every open design question from `plan.md` Technical Context. Format per
decision: **Decision / Rationale / Alternatives rejected**. References to
ABConnectTools and prior departures follow the repo convention (CLAUDE.md design
principles; constitution Sources of Truth).

---

## D1 — How does the harness verify an example's *real* output without the example returning a value?

**Decision**: Examples remain plain `main()` scripts that print and call a shared
`examples/_capture.py::save(model_or_name, payload)` helper. The live harness
(`scripts/run_examples.py`) runs each example **in a subprocess** with environment
variable `AB_EXAMPLE_CAPTURE_DIR=<tmp>` set. When that var is present, `save()` writes
the produced JSON to `<tmp>/<Model>.json` instead of `tests/fixtures/<Model>.json`. The
harness then compares `<tmp>` against the committed `tests/fixtures/` (after volatile
normalization, D3). Default (var unset) behavior is unchanged: `save()` writes the real
fixture — so an operator running `python -m examples dashboard` still captures fixtures.

**Rationale**: Keeps the example honest and readable (Constitution II: "examples are
the capture instrument") — no `return`-value plumbing, no test-shaped indirection (the
exact sin the deprecated runner committed). Subprocess isolation prevents one example's
import-time side effects or `sys.exit` from poisoning the harness, and gives a clean
per-example pass/fail. One env var is the entire contract.

**Alternatives rejected**:
- *Import `main()` and capture the return* — requires every example to return its model,
  re-introducing harness-shaped examples and losing multi-call examples.
- *Parse stdout* — `format_result` emits human `cli_format` text for many models;
  brittle and lossy vs. structural JSON.
- *Harness re-derives and runs the call itself (ignores the example file)* — decouples
  verification from the example; we'd verify the harness, not the documented example.

---

## D2 — What is compared against the fixture?

**Decision**: The JSON produced by `model.model_dump(by_alias=True, mode="json")` (for a
single model) or the list thereof — i.e. exactly what `_capture.save()` /
`format_result` already serialize and what existing fixtures contain (verified against
`examples/dashboard.py::_save` and `ab/cli/formatter.format_result`). Comparison is on
parsed JSON values, not raw text.

**Rationale**: Fixtures are already written this way; comparing the same representation
makes "produced result matches the fixture" exact and alias-stable.

**Alternatives rejected**: Comparing Python `repr`, or `model_dump()` without
`by_alias`/`mode="json"` — would diverge from on-disk fixture form.

---

## D3 — Comparison policy: how to avoid false drift from volatile fields (FR-009)?

**Decision**: A single normalization pass in `ab/progress/example_verify.py` before
equality:
1. Recursively drop keys in a documented global allowlist `VOLATILE_KEYS` (camelCase as
   they appear in JSON), initially: `correlationId`, `requestId`, `traceId`,
   `serverTime`, `timestamp`, plus any field whose name ends in `Date`/`DateTime` **only
   when** its value parses as an ISO datetime within the configured tolerance. (Most GET
   records keyed off the stable staging constants are otherwise deterministic.)
2. Compare dicts key-by-key; compare lists by length then element-wise in order.
3. On mismatch, emit a compact `difflib` unified diff of the two normalized JSON blobs
   (capped) for the report/console.

The allowlist lives in one place, is unit-tested, and is documented in
`example-contract.md`. Per-endpoint overrides are out of scope for v1 (add only if a
real endpoint needs it).

**Rationale**: Strict-by-default equality keeps the signal meaningful; a small, audited
volatile list removes the only systematic source of false negatives. Centralizing it
prevents the per-example fudging the deprecated runner enabled.

**Alternatives rejected**: Fuzzy/loose matching (hides real drift); ignoring ordering
globally (ordering is sometimes meaningful, e.g. sorted lookups).

---

## D4 — Which endpoints auto-run vs. paste? (FR-005/FR-006)

**Decision**: `route.method == "GET"` → **auto-run** (read-only). All of
`POST/PUT/PATCH/DELETE` → **awaiting-paste** (mutating), never executed by the harness.
A small explicit denylist may additionally force specific GETs to awaiting-data when
they require an identifier with no configured `TEST_*` constant.

**Rationale**: Matches the user's decided mutation-safety policy and prevents the harness
from mutating/destroying staging data on every run. HTTP method is the authoritative,
already-available signal (`Route.method`).

**Alternatives rejected**: Running mutations against staging (data-destructive); a
hand-maintained per-endpoint safe/unsafe flag (drift-prone vs. deriving from method).

---

## D5 — How does the static report show a *run* status without making live calls at generation time? (FR-007, no-drift)

**Decision**: The live harness writes a committed artifact
`tests/example_run_results.json` mapping endpoint key →
`{status, checked, fixture, detail}`. `ab/progress/report.py::_gather()` loads it (if
present) and the renderer shows, per endpoint:
- artifact says `pass`/`fail` → that, with `checked` date;
- no artifact entry → a **derived expected** status from code + fixtures:
  `runnable` (GET + example + fixture on disk), `awaiting-data` (GET + example, no
  fixture/constant), `awaiting-paste` (mutation), `binary` (D10), or `missing-example`.
The no-drift canonicalization (`report.py::_canonical`) already strips only the
timestamp; including the artifact's content in the inputs keeps regeneration stable.

**Rationale**: Report generation must stay deterministic and CI-safe (no network). A
committed results artifact is the standard way to surface "last verified" state without
coupling generation to live execution — same spirit as captured fixtures being Tier-2
truth.

**Alternatives rejected**: Running examples during report generation (non-deterministic,
needs creds in CI, slow); showing only derived/expected status (fails the user's
explicit "expect all examples to run and **produce a result that matches**" — we want
real verified pass/fail surfaced).

---

## D6 — Paste-capture mechanism with no backend (FR-010/FR-011)

**Decision**: The renderer emits, for every `awaiting-paste`/`awaiting-data` endpoint, a
collapsible block carrying `data-*` attributes (dotted path, http method, path,
response model, request model) and a `<textarea>` (and a second textarea for the request
body where a request model exists). A single page-level **"Download captures.json"**
button runs embedded vanilla JS that walks all non-empty textareas, builds the
`captures.json` object (contract in `contracts/captures.schema.json`), and triggers a
client-side download via `Blob` + an `<a download>` click. A live counter shows "N
endpoints still awaiting paste." No fetch/XHR, no server.

**Rationale**: Keeps `progress.html` a single static artifact that opens offline and is
safe to regenerate in CI (matches the existing report's nature and the user's selected
option). The generated HTML has empty textareas, so report output stays byte-stable
(no-drift unaffected).

**Alternatives rejected**: A local capture server (adds a live, non-CI surface and a
process to run); one-file-per-paste downloads (more files for the operator to shuttle,
no atomic hand-off).

---

## D7 — Ingesting `captures.json` (FR-012/FR-013)

**Decision**: `scripts/ingest_captures.py` reads `captures.json` and, per entry:
1. Resolves the endpoint's response model from live routes;
2. **Validates** the pasted response by constructing the pydantic model (single or list)
   — on failure, prints a clear, actionable error and skips that entry (no fixture
   written);
3. Writes `tests/fixtures/<Model>.json` as `model_dump(by_alias=True, mode="json")`
   (canonical form, identical to harness/example output);
4. If a request body was pasted and the endpoint has a `request_model`, validates and
   writes `tests/fixtures/requests/<ReqModel>.json`;
5. Creates or updates the **plain-script canonical example** for that endpoint (D9
   generator), so the pasted endpoint now has both fixture and example;
6. Records the endpoint in `example_run_results.json` as `pass` with source `paste`.

**Rationale**: Validation-before-write enforces Constitution II's "no fabricated
fixtures" — a paste that doesn't satisfy the model is a bad paste, surfaced, not stored.
Re-using the same serialization path guarantees the ingested fixture is byte-identical to
one the harness would later produce, so the endpoint immediately verifies clean.

**Alternatives rejected**: Writing the raw paste verbatim (skips validation/normalization,
risks invalid fixtures); manual fixture authoring (the fabrication anti-pattern).

---

## D8 — Coverage gate (FR-008, SC-005)

**Decision**: `tests/test_example_coverage.py` (non-live, runs under
`pytest -m "not live"`): builds the precise endpoint→example index
(`ab/progress/example_index.py`) from live routes and asserts every routed endpoint has
exactly one canonical example. Failure message lists each uncovered
`api.<group>.<method>`. A companion assertion flags endpoints whose canonical example is
still a `_`-prefixed/runner file (drives D9 migration to zero).

**Rationale**: Puts the guarantee where CI already runs (`pytest -m "not live"` is the
certification command per the quality baseline), so coverage can't silently regress.

**Alternatives rejected**: A standalone script not wired to CI (coverage rots); a new
G-gate in `gates.py` (heavier than needed; a plain test is clearer and matches existing
doc-gate tests like `test_docstring_coverage.py`).

---

## D9 — Precise endpoint→example mapping & example generation

**Decision**: New `ab/progress/example_index.py` replaces the noisy logic in
`route_index.py::_scan_example_entries`. It statically (AST, no import) scans
`examples/*.py` and `examples/**/*.py`, resolves each `api.<group>[.<sub>].<method>(...)`
call chain to a registry key, and — crucially — only counts a method as covered when the
example file is a **canonical (non-underscore) plain script** and the method resolves to a
real `Route` in the registry (eliminating the current negative "missing" counts caused by
counting helper names and double-counting `jobs`/`jobs.note`). The canonical example for
an endpoint is the single plain-script file that calls it; ties are resolved by group →
`examples/<group>.py` (or `examples/<group>/<sub>.py` for subgroups).

Example generation (used by ingest and by scaffolding new examples) emits the
`examples/dashboard.py` shape: module docstring with the RTD link, `from ab import
ABConnectAPI`, `from examples._capture import save`, a real call using the appropriate
`TEST_*` constant(s), `print(format_result(result))`, and `save("<Model>.json", result)`.

**Rationale**: A precise index is the foundation for both the gate (D8) and the report
column (D5); deriving "canonical" = plain-script keeps Principle II honest and makes the
migration measurable.

**Alternatives rejected**: Keeping/patching the existing scanner in place (its
group-keying conflates subgroups and counts non-routed helpers); a hand-maintained
manifest mapping endpoints→examples (drift-prone, violates no-drift).

---

## D10 — Binary / no-content responses (FR-017, Edge Cases)

**Decision**: Endpoints whose `response_model` is bytes/`None`/file-download (detected
from the route's response type and the existing `format_result` "binary response"
branch) are classified `binary` (covered-as-binary). They satisfy the coverage gate with
an example that performs the call and prints a binary/size summary, but are **excluded**
from fixture comparison and from "awaiting-paste". `_capture.save()` already skips binary.

**Rationale**: Such endpoints can neither print a pydantic model nor store a JSON fixture;
counting them as failing or as gaps would be wrong. Explicit classification keeps SC-001
("every endpoint has an example") true without forcing an impossible fixture.

**Alternatives rejected**: Forcing a JSON fixture (fabrication); marking them failing
forever (false red).

---

## D11 — Migration order & no-deletion compliance (FR-016)

**Decision**: Migrate `_`-prefixed examples to plain scripts in dependency-light batches
(start with zero-coverage `jobs.*` subgroups, then the rest). Each migration **adds**
`examples/<group>.py` (or `examples/<group>/<sub>.py`) and **leaves** the `_<group>.py`
file and `examples/_runner.py` untouched. `html/rm_runner.html` is updated to show the
file as migrated. Whether to eventually delete the deprecated files is surfaced as an
explicit decision at feature end, never done silently (honors the no-deletion policy and
keeps `examples/__main__.py`'s legacy-runner support intact during transition).

**Rationale**: Satisfies "every endpoint has a plain-script canonical example" while
honoring the repo's no-file-deletion rule and avoiding any breaking change to the
`examples` dispatcher mid-flight.

**Alternatives rejected**: Rename/delete-in-place (a delete; violates policy and could
break `examples/__main__.py` discovery); big-bang migration (high blast radius, hard to
checkpoint per Constitution VIII).

---

## D11.1 — Retain-vs-delete decision for deprecated files (T032)

**Decision (explicit, per the no-file-deletion policy)**: `examples/_runner.py` and every
`_`-prefixed example file are **retained** for the lifetime of this feature and are NOT
deleted. They simply stop being *canonical* (the precise `example_index` excludes
underscore files), so each migrated endpoint's canonical example is its new plain
script. `examples/__main__.py`'s legacy-runner support also stays, so the dispatcher
keeps working during the transition. Any future removal of these files must be a
separate, explicitly-approved change — never a silent side effect of migration.

**Rationale**: Honors FR-016 and the repo's no-deletion rule; avoids any breaking change
to `examples/` discovery mid-migration. The deprecation is enforced by the coverage gate
(`legacy_only_endpoints()` → 0), not by deleting code.

## Open questions deferred to implementation (non-blocking)

- Exact initial membership of `VOLATILE_KEYS` will be tuned once the harness runs against
  staging and reveals which GET responses carry per-request volatile fields (D3).
- Whether any GET legitimately needs to be forced to `awaiting-paste` (e.g. returns
  user-specific PII unsafe to commit) — handled by the D4 denylist as cases arise.
