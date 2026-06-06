---
description: "Task list for 037-example-coverage"
---

# Tasks: Runnable Example Coverage with Run-and-Verify Progress

**Input**: Design documents from `/specs/037-example-coverage/`
**Prerequisites**: plan.md, spec.md, research.md (D1–D11), data-model.md, contracts/

**Tests**: Included **only** where the test IS the deliverable — the coverage gate
(FR-008), comparison policy (FR-009), no-drift artifact (FR-007), and ingest validation
(FR-013). These are features, not tests-of-implementation.

**Organization**: Grouped by user story. Phases map to plan.md A→D.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependency on an incomplete task)
- **[Story]**: US1–US4 (user-story phases only)
- All paths are repo-relative to `/usr/src/pkgs/AB/`

## Path Conventions

Single project. SDK + tooling at repo root: `ab/progress/`, `examples/`, `scripts/`,
`tests/`, `html/`. Canonical venv: `.venv/` (use `source .venv/bin/activate`).

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Make the live/non-live split usable and record the starting state.

- [X] T001 Ensure the `live` pytest marker is registered in `pyproject.toml` (`[tool.pytest.ini_options].markers`) so `@pytest.mark.live` and `pytest -m "not live"` run without warnings; do not change existing markers.
- [X] T002 Record baseline: run `.venv/bin/pytest -m "not live" -q` and `.venv/bin/python scripts/generate_progress.py`, and note the current pass count + that the report renders, in `specs/037-example-coverage/baseline.md`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared building blocks every story depends on.

**⚠️ CRITICAL**: No user-story work begins until this phase is complete.

- [X] T003 Create `examples/_capture.py` exposing `save(name, payload) -> Path | None` per `contracts/example-contract.md` §2: writes to `AB_EXAMPLE_CAPTURE_DIR` when set else `tests/fixtures/`; pydantic/list serialization identical to `examples/dashboard.py::_save` (`model_dump(by_alias=True, mode="json")`, `indent=2, ensure_ascii=False, +"\n"`); bytes → skip + print binary note (D10).
- [X] T004 [P] In `ab/progress/models.py`, add a `RunStatus` enum (`passing|failing|awaiting_data|awaiting_paste|binary|missing_example`) and extend `MethodProgress` with `run_status: RunStatus`, `run_checked: str | None = None`, `run_detail: str | None = None` (additive; per data-model.md).
- [X] T005 Create `ab/progress/example_index.py`: `CanonicalExample` dataclass + `build_example_index()`, `routed_endpoint_keys()`, `uncovered_endpoints()`, `legacy_only_endpoints()` — precise AST scan of `examples/**/*.py` resolving `api.<group>[.<sub>].<method>(...)` chains to registry keys, counting a method covered only when backed by a **non-underscore plain script** that resolves to a real `Route` (fixes the negative-count bug in `route_index.py::_scan_example_entries`).
- [X] T006 [P] Create `ab/progress/example_gen.py` with `render_example(endpoint_key, route, model) -> str` emitting the canonical skeleton from `contracts/example-contract.md` §1 (docstring + RTD link, `ABConnectAPI`, `from examples._capture import save`, real call using `TEST_*` constants, `print(format_result(...))`, `save("<Model>.json", result)`); shared by US1 fill and US3 ingest.

**Checkpoint**: Capture helper, status model, precise index, and generator exist.

---

## Phase 3: User Story 1 — Every endpoint has a canonical example (Priority: P1) 🎯 MVP

**Goal**: Each routed endpoint has exactly one canonical plain-script example showing a
real call + real printed pydantic response.

**Independent Test**: `pytest -m "not live" -k example_coverage` is green; every
`api.<group>.<method>` resolves to a non-underscore plain-script example.

- [X] T007 [US1] Write the coverage gate `tests/test_example_coverage.py` (non-live) per `contracts/example-contract.md` §4: assert `uncovered_endpoints()` is empty (names each gap); add a companion `legacy_only_endpoints()` assertion as a **warning/xfail for now** (hardened in US4 T031). Expected to FAIL initially.
- [X] T008 [US1] Rewire `ab/progress/route_index.py::build_endpoint_class_progress` to source `has_example` from `example_index.build_example_index()` instead of `_scan_example_entries` (keep `_scan_example_entries` in place — no deletion — but stop relying on it); confirm no method shows a negative "missing" count.
- [X] T009 [US1] Run the gate and write `specs/037-example-coverage/coverage-gaps.md` enumerating the real uncovered + legacy-only endpoints per group (the authoritative work-list for T010–T012).
- [ ] T010 [P] [US1] Author canonical examples for the zero-coverage **read-only** `jobs.*` subgroups (e.g. `jobs.tracking`, `jobs.status`, `jobs.note` getters, `jobs.freight_providers` get, `jobs.parcel_items` get) as `examples/jobs/<sub>.py` (real call + `print` + `save`).
- [ ] T011 [P] [US1] Author canonical examples for the zero-coverage **mutating** `jobs.*` subgroups (`jobs.payment`, `jobs.on_hold`, `jobs.sms`, `jobs.email`, `jobs.rfq`, `jobs.shipment`, `jobs.form`, parcel mutations) as `examples/jobs/<sub>.py` — real call + `print` (fixtures arrive via paste in US3; never auto-run).
- [ ] T012 [P] [US1] Author/extend canonical examples for the remaining non-`jobs` gaps surfaced in T009 (e.g. `dashboard` remaining methods) in `examples/<group>.py`.
- [ ] T013 [US1] Re-run `pytest -m "not live" -k example_coverage` until the `uncovered_endpoints()` assertion is green (legacy-only may remain pending US4). Validates SC-001, SC-005.

**Checkpoint**: Every routed endpoint has a canonical example — MVP deliverable.

---

## Phase 4: User Story 2 — Progress expects examples to run and match fixtures (Priority: P2)

**Goal**: Read-only examples run and are diffed against fixtures; the report shows a
per-endpoint Run status; mutations are never auto-run.

**Independent Test**: `python scripts/run_examples.py` (live) marks read-only endpoints
`passing`/`failing`; the report shows a Run column; flipping a fixture turns one red.

- [X] T014 [P] [US2] Create `ab/progress/example_verify.py`: `VOLATILE_KEYS` (D3), `normalize(obj)`, and `compare(produced, fixture) -> (bool, detail)` (dict key-by-key, list length-then-elementwise, capped `difflib` unified-diff summary on mismatch).
- [X] T015 [P] [US2] Write `tests/unit/test_example_verify.py` (non-live): equal payloads pass; volatile-only differences pass; list-length and value diffs fail with a detail string.
- [X] T016 [US2] Create `scripts/run_examples.py` (live; per `contracts/example-contract.md` §3): for each read-only (GET) covered endpoint, subprocess-run its example with `AB_EXAMPLE_CAPTURE_DIR=<tmp>`, `compare()` temp vs `tests/fixtures/`, write sorted `tests/example_run_results.json` (schema 1); flags `--group <name>` and `--capture` (re-capture to `tests/fixtures/`); never run mutating endpoints. Depends on T003, T005, T014.
- [X] T017 [US2] In `ab/progress/report.py::_gather()` load `tests/example_run_results.json` (if present) and compute each `MethodProgress.run_status`/`run_checked`/`run_detail`: artifact entry → `passing|failing|binary`; otherwise derive `runnable→awaiting_data / awaiting_paste / binary / missing_example` from method + example + fixture. Depends on T004, T005.
- [X] T018 [US2] Add a **Run** column with status badges to the helpers and sub-group tables in `ab/progress/renderer.py::render_endpoint_class_progress` (reuse/extend `_yn_badge` with a status-badge variant); add a coverage summary card. Depends on T017.
- [X] T019 [P] [US2] Write `tests/test_example_run_results_drift.py` (non-live): `tests/example_run_results.json` validates against `contracts/example_run_results.schema.json`, keys are sorted, and `is_report_current()` stays true after regeneration (no-drift incl. the artifact).
- [ ] T020 [US2] Run `scripts/generate_progress.py`; confirm the Run column renders and existing no-drift tests pass. Validates SC-004.

**Checkpoint**: The report verifiably expects read-only examples to match fixtures.

---

## Phase 5: User Story 3 — Paste-capture for endpoints that can't auto-run (Priority: P2)

**Goal**: Non-runnable endpoints get a paste slot in `progress.html`; exported
`captures.json` ingests into fixtures + examples.

**Independent Test**: The report lists every awaiting-paste endpoint with a textarea +
counter; pasting + Download + `ingest_captures.py` produces a fixture and example and
flips status.

- [X] T021 [US3] Extend `ab/progress/renderer.py` with a paste-capture section: for each `awaiting_paste`/`awaiting_data` endpoint, a collapsible block carrying `data-endpoint/-method/-path/-response-model/-request-model` and response (+ request, when a request model exists) `<textarea>`s, plus a live "N endpoints still awaiting paste" counter. Depends on T018.
- [X] T022 [US3] Embed vanilla JS in the rendered report (via `renderer.py`) that, on "Download captures.json", walks non-empty textareas, builds the object per `contracts/captures.schema.json` (parse JSON; keep raw string if unparseable), and triggers a `Blob` + `<a download>` — no fetch/server. Confirm generated HTML has empty textareas so no-drift holds. Depends on T021.
- [X] T023 [P] [US3] Create `ab/progress/captures.py`: load+shape-validate `captures.json`, resolve each endpoint→response/request model + fixture path, and validate each pasted payload by constructing the pydantic model (single or `List[...]`), returning structured ok/malformed results (FR-013).
- [X] T024 [US3] Create `scripts/ingest_captures.py`: use `captures.py` to validate, write `tests/fixtures/<Model>.json` (+ `tests/fixtures/requests/<ReqModel>.json` when a request is present), generate/update the canonical example via `example_gen` (T006), and record `passing`(source=`paste`) in `tests/example_run_results.json`; malformed entries are reported and skipped (no fixture written). Depends on T006, T023.
- [X] T025 [P] [US3] Write `tests/unit/test_captures_ingest.py` (non-live): a malformed paste is rejected with no fixture written; a valid sample paste yields a fixture + example + a `paste` results entry; a sample `captures.json` validates against the schema.
- [ ] T026 [US3] Roundtrip per `quickstart.md`: regenerate the report, simulate a paste, download `captures.json`, run `ingest_captures.py`, and confirm `pytest -m "not live"` stays green and the endpoint is no longer awaiting paste. Validates SC-003.

**Checkpoint**: Every non-runnable endpoint is coverable via paste.

---

## Phase 6: User Story 4 — Migrate deprecated-runner examples (Priority: P3)

**Goal**: No endpoint's canonical example depends on `ExampleRunner`; `_`-prefixed files
retained but non-canonical.

**Independent Test**: `legacy_only_endpoints()` is empty; `rm_runner.html` shows zero
remaining; each migrated endpoint reads as a plain script.

- [ ] T027 [P] [US4] Migrate batch 1 of `_`-prefixed examples → plain `examples/<group>.py` (address, agent, autoprice, catalog, commodities, commodity_maps) using `_capture.save`; leave the `_`-files in place (no deletion).
- [ ] T028 [P] [US4] Migrate batch 2 (companies, companies_extended, contacts, contacts_extended, lookup, lookup_extended, reports, rfq, views) → plain scripts; leave `_`-files in place.
- [ ] T029 [P] [US4] Migrate batch 3 (notes/notes_global, parcels, partners, payments, sellers, shipments, users, web2lead, forms, email_sms, onhold, freight_providers, tracking, lots, documents) → plain scripts; leave `_`-files in place.
- [ ] T030 [US4] Update `html/rm_runner.html` to mark every migrated file done and show remaining count = 0.
- [ ] T031 [US4] Harden the `legacy_only_endpoints()` assertion in `tests/test_example_coverage.py` from warning/xfail to a hard failure; run the gate → zero legacy-only. Validates SC-006.
- [ ] T032 [US4] Record the explicit retain-vs-delete decision for `examples/_runner.py` and the `_`-files in `specs/037-example-coverage/research.md` (under D11) per the no-deletion policy; **do not delete** any file as part of this feature.

**Checkpoint**: Canonical example set is entirely plain scripts.

---

## Phase 7: Polish & Cross-Cutting Concerns

- [ ] T033 [P] Update `README.md` and the discoverability section of `CLAUDE.md` with the example contract, `scripts/run_examples.py`, and `scripts/ingest_captures.py` workflow.
- [ ] T034 [P] Reconcile `FIXTURES.md` notes with the new run-status source (cross-reference, no functional change).
- [ ] T035 Full certification: `.venv/bin/pytest -m "not live" -q` green, `.venv/bin/ruff check .` clean, regenerate `html/progress.html`, confirm `is_report_current()` (no-drift). Validates SC-007.
- [ ] T036 Checkpoint commits per phase boundary (Constitution VIII): one commit per completed phase with the phase name in the message.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (P1)**: none — start immediately.
- **Foundational (P2)**: after Setup — **blocks all stories**.
- **US1 (Phase 3)**: after Foundational. MVP.
- **US2 (Phase 4)**: after Foundational; consumes US1's examples in practice (harness runs them) but is independently testable with whatever examples exist.
- **US3 (Phase 5)**: after Foundational; builds on US2's renderer Run column (T021 depends on T018).
- **US4 (Phase 6)**: after Foundational; independent of US2/US3 (pure example authoring) but its hard gate (T031) finalizes US1's legacy assertion.
- **Polish (Phase 7)**: after all desired stories.

### Critical path

T003 → T005 → T007/T008 (US1 gate) → fill examples (T010–T012) → T013 ➜
then T014→T016→T017→T018 (US2) ➜ T021→T022→T024 (US3) ➜ T031 (US4) ➜ T035.

### Within each story

- Write the gate/verify/ingest test before its implementation where listed (T007 before fills; T015 before/with T014–T016; T025 with T023–T024).
- `models.py`/`example_index.py` (foundational) before report wiring; report wiring (T017) before renderer (T018); renderer (T018) before paste UI (T021).

### Parallel Opportunities

- **Foundational**: T004 and T006 run parallel to T003/T005 (different files).
- **US1**: T010, T011, T012 are parallel (different `examples/` files).
- **US2**: T014+T015 parallel to nothing blocking; T019 parallel once artifact shape exists.
- **US3**: T023 and T025 parallel to T021/T022 (different files).
- **US4**: T027, T028, T029 fully parallel (disjoint file sets).

---

## Parallel Example: User Story 1 fills

```bash
# After T007–T009, author example batches concurrently (different files):
Task: "T010 read-only jobs.* subgroup examples in examples/jobs/<sub>.py"
Task: "T011 mutating jobs.* subgroup examples in examples/jobs/<sub>.py"
Task: "T012 remaining non-jobs gap examples in examples/<group>.py"
```

---

## Implementation Strategy

### MVP First (User Story 1)

1. Phase 1 Setup → 2. Phase 2 Foundational → 3. Phase 3 US1 → **STOP & validate**:
   `pytest -m "not live" -k example_coverage` green = every endpoint has a canonical
   example. Demo-able MVP.

### Incremental Delivery

US1 (coverage) → US2 (run-and-verify report) → US3 (paste-capture + ingest) →
US4 (migration). Each phase ends green and is independently demoable; commit at each
checkpoint (T036).

---

## Notes

- [P] = different files, no incomplete dependency.
- Honor the no-deletion policy throughout (FR-016): migrations and rewires are additive;
  `_runner.py` and `_`-files stay.
- `ab` public imports are a frozen contract (FR-015): all new code is additive tooling.
- Mutating endpoints are never auto-run (FR-006): their fixtures only ever arrive via paste/ingest.
