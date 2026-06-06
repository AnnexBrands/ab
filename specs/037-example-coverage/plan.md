# Implementation Plan: Runnable Example Coverage with Run-and-Verify Progress

**Branch**: `037-example-coverage` | **Date**: 2026-06-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/037-example-coverage/spec.md`

## Summary

Guarantee that **every routed endpoint** (ACPortal + Catalog + ABC, ~209 routed
methods across 36 endpoint classes) has exactly one **canonical example** — a plain
`main()` script that makes a real call and prints the real pydantic response
(reference: `examples/dashboard.py`), never the deprecated `ExampleRunner`. A
**run-and-verify harness** executes read-only (GET) examples against staging and
compares the produced `model_dump(by_alias=True, mode="json")` to the committed
fixture; mutating endpoints (POST/PUT/PATCH/DELETE) are never auto-run and are routed
to a **paste-capture** flow in `html/progress.html` (editable textareas + a single
"Download captures.json" button, no backend). The existing no-drift progress report
(`ab/progress/`) gains a per-endpoint **run-status** column derived from live code +
fixtures + a committed run-results artifact, and a **non-live pytest gate** fails if
any endpoint lacks a canonical example. An **ingest** step turns `captures.json` into
fixtures + generated examples. All changes are additive (no breaking imports, no file
deletions).

## Technical Context

**Language/Version**: Python 3.11+ (matches existing SDK)
**Primary Dependencies**: pydantic>=2.0, requests (existing — no new runtime deps);
stdlib only for tooling (`ast`, `json`, `pathlib`, `subprocess`, `argparse`,
`difflib`); report UI uses vanilla embedded JavaScript (no framework, no CDN).
**Storage**: Filesystem — response fixtures `tests/fixtures/*.json`, request fixtures
`tests/fixtures/requests/*.json`, committed run-results artifact
`tests/example_run_results.json`, transient operator export `captures.json`, report
`html/progress.html`.
**Testing**: pytest. Non-live gates run under `pytest -m "not live"` (CI). The
run-and-verify harness is operator-run and `@pytest.mark.live` (staging creds in
`.env.staging`).
**Target Platform**: Linux dev + GitHub Actions CI.
**Project Type**: Single project — SDK library plus repo tooling (`ab/progress/`,
`scripts/`, `examples/`).
**Performance Goals**: Report generation deterministic and sub-second-to-few-seconds
(static, no network). Live harness latency is bounded by API round-trips and is not on
the CI path.
**Constraints**: Report regeneration MUST be byte-stable modulo the timestamp
(no-drift). The report MUST remain a single static HTML file safe to open offline and
generate in CI (no server, no backend on the capture path). Additive only — `ab`'s
public import surface is a frozen contract for `/usr/src/AnnexIq`. No file deletion
(honor the no-deletion policy); migrating a `_`-prefixed example produces a new
plain-script file and leaves the original in place.
**Scale/Scope**: ~209 routed methods / 36 endpoint classes / 3 API surfaces; ~35
underscore-prefixed legacy example files to migrate.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

This feature **enforces** the constitution rather than challenging it:

| Principle | Effect of this feature | Status |
|-----------|------------------------|--------|
| II. Example-Driven Fixture Capture | Makes "every endpoint has a runnable example" *measured and gated*; examples remain the capture instrument; fixtures stay in lock-step via shared `_save`. | ✅ Reinforces |
| III. Four-Way Harmony | Adds an automated check that the Example↔Fixture pair exists and agrees for every endpoint. | ✅ Reinforces |
| V. Endpoint Status Tracking | Run-status (passing/failing/awaiting-data/awaiting-paste/binary) is a per-endpoint, no-drift, machine-derived status — stronger than hand-maintained `FIXTURES.md` rows. | ✅ Reinforces |
| IV / IX (swagger/params) | Unaffected; existing `tests/test_example_params.py` keeps running. | ✅ No change |
| VIII. Phase-Based Recovery | Work is phased (US1→US4) with committed checkpoints; tasks.md uses checkbox tasks. | ✅ Complies |

**Sources of Truth**: Comparison treats the **captured fixture** (Tier 2) as the
expectation, consistent with the hierarchy. Read-only verification re-captures from the
live API; on conflict, the fixture is re-captured (never fabricated).

**No violations.** Complexity Tracking table omitted (nothing to justify).

One nuance recorded for `/speckit.tasks`: the deprecated `ExampleRunner`
(`examples/_runner.py`) and the `_`-prefixed files are **retained** (no-deletion
policy); they are simply excluded from the *canonical* example set. Their continued
existence does not violate Principle II once each backed endpoint has a plain-script
canonical example.

## Project Structure

### Documentation (this feature)

```text
specs/037-example-coverage/
├── plan.md              # This file
├── research.md          # Phase 0 — design decisions (D1..D10)
├── data-model.md        # Phase 1 — entities & status model
├── quickstart.md        # Phase 1 — operator + maintainer runbook
├── contracts/
│   ├── captures.schema.json            # operator export contract
│   ├── example_run_results.schema.json # committed run-results artifact contract
│   └── example-contract.md             # canonical example file + capture-helper API
├── checklists/
│   └── requirements.md  # spec quality checklist (done)
└── tasks.md             # Phase 2 — created by /speckit.tasks (NOT here)
```

### Source Code (repository root)

```text
ab/
└── progress/                       # existing no-drift report package — EXTENDED
    ├── route_index.py              # MODIFY: precise endpoint→example map; run_status feed
    ├── models.py                   # MODIFY: MethodProgress.run_status + RunStatus enum
    ├── renderer.py                 # MODIFY: add "Run" column + paste-capture UI + JS
    ├── report.py                   # MODIFY: load run-results artifact into _gather()
    ├── example_index.py            # NEW: canonical example discovery (method→file, precise)
    ├── example_verify.py           # NEW: run/compare logic + volatile-field normalization
    └── captures.py                 # NEW: captures.json parse/validate + ingest helpers

examples/
├── _capture.py                     # NEW: shared save()/print helper honoring capture-dir env
├── <group>.py                      # NEW/MIGRATED: plain-script canonical examples
└── _*.py, _runner.py               # RETAINED (deprecated), excluded from canonical set

scripts/
├── run_examples.py                 # NEW: live harness — run read-only, verify, write results
├── ingest_captures.py              # NEW: captures.json → fixtures + generated examples
└── generate_progress.py           # (existing) regenerates html/progress.html

tests/
├── example_run_results.json        # NEW: committed last-verified run statuses (artifact)
├── test_example_coverage.py        # NEW (non-live): every routed endpoint has an example
├── test_example_run_results_drift.py # NEW (non-live): results artifact shape/no-drift
└── fixtures/ , fixtures/requests/  # (existing) captured fixtures, kept in lock-step

html/
├── progress.html                   # (existing) gains Run column + paste-capture section
└── rm_runner.html                  # (existing) migration tracker — updated per migration
```

**Structure Decision**: Single project. The feature extends the existing
`ab/progress/` report package (new modules `example_index.py`, `example_verify.py`,
`captures.py`; targeted edits to `models.py`/`renderer.py`/`report.py`/`route_index.py`),
adds two `scripts/` entrypoints (`run_examples.py`, `ingest_captures.py`), a shared
`examples/_capture.py`, and non-live pytest gates. No new top-level packages; nothing
removed.

## Key Design Decisions (detail in research.md)

- **D1 — Example is the instrument, harness redirects its save.** The live harness
  runs each plain example via subprocess with `AB_EXAMPLE_CAPTURE_DIR` set; the shared
  `examples/_capture.py::save()` writes to that temp dir instead of `tests/fixtures/`,
  then the harness diffs temp-vs-committed. The example stays a real, readable script
  that really runs and really prints — no return-value plumbing.
- **D2 — Compare on `model_dump(by_alias=True, mode="json")`, not stdout.** Matches how
  fixtures are written; structural, stable.
- **D3 — Volatile-field normalization in one place** (`example_verify.py`): a documented
  global key allowlist (timestamps, server-generated ids) stripped before equality;
  lists compared length-then-element-wise.
- **D4 — Read-only = GET auto-run; everything else = awaiting-paste.** From `route.method`.
- **D5 — Run-status is CI-deterministic.** The static report reads a committed
  `tests/example_run_results.json`; absent entry → derived "expected" status. No live
  calls at report-generation time; no-drift canonicalization includes the artifact.
- **D6 — Paste-capture is pure client-side JS.** Textareas keyed by dotted path; one
  Blob download builds `captures.json`. No server, CI-safe, offline-openable.
- **D7 — Ingest validates against the response model before writing** (FR-013); writes
  fixture + request fixture; generates/updates the plain example.
- **D8 — Coverage gate is non-live pytest** over the precise example index (SC-005).
- **D9 — Migration is additive**; `_`-prefixed files retained, excluded from canonical
  scan; `rm_runner.html` tracks remaining.
- **D10 — Binary/no-content endpoints** classified `covered-as-binary` (not failing,
  not a gap).

## Phasing (maps to user stories)

- **Phase A (US1, P1)**: example index + `_capture.py` + coverage gate + fill missing
  examples (esp. zero-coverage `jobs.*` subgroups). MVP: every endpoint has an example.
- **Phase B (US2, P2)**: `run_examples.py` harness + results artifact + report Run column.
- **Phase C (US3, P2)**: paste-capture UI + `captures.json` contract + `ingest_captures.py`.
- **Phase D (US4, P3)**: migrate `_`-prefixed examples to plain scripts; update tracker.

## Complexity Tracking

*No constitution violations — table intentionally omitted.*
