# Tasks: Progress Report

**Input**: Design documents from `/specs/003-progress-report/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, quickstart.md

**Tests**: Not explicitly requested — test tasks omitted.

**Organization**: Tasks grouped by user story for independent implementation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story (US1–US4) this task belongs to
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Create project structure and package scaffolding

- [x] T001 Create `ab/progress/` package with `__init__.py` and `scripts/` directory per plan.md project structure

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Data models, parsers, and scanners that ALL user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T002 [P] Define dataclasses (`Endpoint`, `EndpointGroup`, `Fixture`, `Constant`, `ActionItem`) in `ab/progress/models.py` per data-model.md entity definitions
- [x] T003 [P] Implement `parse_api_surface(path) -> list[EndpointGroup]` in `ab/progress/parsers.py` — regex-based parser for `specs/api-surface.md` tables extracting all endpoint groups across ACPortal, Catalog, and ABC surfaces with per-row status (`done`/`pending`/`—` → `not_started`) and group-level summary metadata (`ab_file`, `ref_file`, `priority`)
- [x] T004 [P] Implement `parse_fixtures(path) -> list[Fixture]` in `ab/progress/parsers.py` — parse both `## Captured Fixtures` and `## Pending Fixtures` tables from `FIXTURES.md`, extracting model name, endpoint path, method, blocker reason, and capture instructions
- [x] T005 [P] Implement `scan_fixture_files(dir) -> set[str]` and `parse_constants(path) -> list[Constant]` in `ab/progress/scanner.py` — scan `tests/fixtures/*.json` for existing fixture filenames and regex-parse `tests/constants.py` for `LIVE_*` assignments

**Checkpoint**: All data sources can be parsed — user story implementation can begin

---

## Phase 3: User Story 1 — View Implementation Progress (Priority: P1)

**Goal**: Summary table showing total/done/pending/not-started counts per API surface with color-coded status indicators

**Independent Test**: Open generated HTML, verify summary counts match `specs/api-surface.md` coverage data

- [x] T006 [US1] Implement HTML document skeleton with inline CSS in `ab/progress/renderer.py` — define `render_report(groups, fixtures, constants, fixture_files) -> str` that produces a complete self-contained HTML document with `<style>` block (green=done, amber=pending, gray=not-started) and page header with generation timestamp
- [x] T007 [US1] Implement `render_summary(groups) -> str` in `ab/progress/renderer.py` — aggregate `EndpointGroup` data into per-surface (ACPortal, Catalog, ABC) and overall totals, render as an HTML table with color-coded cells for each status category

**Checkpoint**: Running the generator produces an HTML file with a correct coverage summary

---

## Phase 4: User Story 2 — Identify Items Requiring Input (Priority: P1)

**Goal**: "Action Required" section listing every unimplemented endpoint, organized into Tier 1 (scaffolded, needs fixture) and Tier 2 (not started, needs implementation), grouped by endpoint group

**Independent Test**: Every endpoint from `api-surface.md` not marked "done" appears in the action-required section with status and blocker type

- [x] T008 [US2] Implement `classify_action_items(groups, fixtures, fixture_files, constants) -> list[ActionItem]` in `ab/progress/models.py` — for each non-done endpoint, determine `blocker_type` (`capture`, `constant_needed`, `env_blocked`, `not_implemented`) and `tier` (1 or 2) using the status classification logic from data-model.md
- [x] T009 [US2] Implement `render_action_required(action_items) -> str` in `ab/progress/renderer.py` — render Tier 1 and Tier 2 sections with collapsible `<details>` elements per endpoint group, each showing endpoint path, method, response model, status badge, and blocker type
- [x] T010 [US2] Integrate action-required rendering into `render_report()` in `ab/progress/renderer.py` — call `render_action_required()` after summary section

**Checkpoint**: HTML shows all unimplemented endpoints organized by tier and group

---

## Phase 5: User Story 3 — Step-by-Step Instructions (Priority: P1)

**Goal**: Each action-required item has tailored step-by-step instructions the reviewer can follow to resolve the blocker

**Independent Test**: Pick any pending fixture item, follow its instructions, and confirm the test passes

- [x] T011 [US3] Implement `build_instructions(action_item, constants) -> list[str]` in `ab/progress/instructions.py` — template-based instruction builder with 4 templates keyed on `blocker_type`: (1) `capture`: SDK method call + fixture save path + pytest command, (2) `constant_needed`: add constant to `tests/constants.py` + then capture, (3) `env_blocked`: explain staging limitation + suggest alternatives, (4) `not_implemented`: list required artifacts (model, endpoint, test, fixture)
- [x] T012 [US3] Implement `detect_required_constants(endpoint) -> list[str]` in `ab/progress/instructions.py` — map path parameters (`{companyId}` → `LIVE_COMPANY_UUID`, `{jobDisplayId}` / `{id}` → `LIVE_JOB_DISPLAY_ID`, `{contactId}` → `LIVE_CONTACT_ID`) and flag unknown params as needing new constants
- [x] T013 [US3] Integrate instructions into action items and renderer — call `build_instructions()` during `classify_action_items()` to populate `ActionItem.instructions`, render as `<ol>` within each endpoint's `<details>` element in `ab/progress/renderer.py`

**Checkpoint**: Every action-required item has clear, tailored instructions rendered in the HTML

---

## Phase 6: User Story 4 — Regenerate After Changes (Priority: P2)

**Goal**: Single-command entry point that regenerates `progress.html` reflecting current project state

**Independent Test**: Capture one fixture, regenerate, confirm item moved from pending to done

- [x] T014 [US4] Create entry point `scripts/generate_progress.py` — import from `ab.progress`, call parsers and scanners with correct relative paths from repo root, call `render_report()`, write output to `progress.html`, print summary to stdout
- [x] T015 [US4] Add input validation and error handling in `scripts/generate_progress.py` — check that `specs/api-surface.md`, `FIXTURES.md`, `tests/fixtures/`, and `tests/constants.py` exist before parsing; fail with clear error message identifying which file is missing (edge case from spec)
- [x] T016 [US4] Add `progress.html` to `.gitignore` as a generated build artifact

**Checkpoint**: `python scripts/generate_progress.py` produces correct `progress.html` from current project state

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: End-to-end validation and final quality checks

- [x] T017 Run full generation and validate output: verify endpoint count matches `specs/api-surface.md` (SC-001), all pending fixtures appear with instructions (SC-002), HTML renders without external requests (SC-005)
- [x] T018 Verify idempotent regeneration: run generator twice with no file changes and confirm output is identical (US4 acceptance scenario 2)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Phase 2 — can start immediately after
- **US2 (Phase 4)**: Depends on Phase 2 — can run in parallel with US1
- **US3 (Phase 5)**: Depends on Phase 4 (US2) — needs action item classification
- **US4 (Phase 6)**: Depends on Phases 3, 4, 5 — glues everything together
- **Polish (Phase 7)**: Depends on Phase 6

### User Story Dependencies

- **US1 (Summary)**: Independent — only needs foundational parsers
- **US2 (Action Items)**: Independent — only needs foundational parsers + classification
- **US3 (Instructions)**: Depends on US2 — builds on action item data structure
- **US4 (Entry Point)**: Depends on US1 + US2 + US3 — orchestrates all components

### Within Each Story

- Models/dataclasses before business logic
- Business logic before rendering
- Rendering before integration

### Parallel Opportunities

**Phase 2** — all 4 foundational tasks (T002–T005) can run in parallel:
```
T002 (models.py) | T003 (api-surface parser) | T004 (fixtures parser) | T005 (scanner)
```

**Phases 3+4** — US1 and US2 can run in parallel after Phase 2:
```
T006–T007 (summary rendering) | T008–T010 (action item classification + rendering)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (parsers + scanner)
3. Complete Phase 3: US1 (summary rendering)
4. Create minimal entry point to generate summary-only HTML
5. **STOP and VALIDATE**: Open progress.html, verify summary counts

### Incremental Delivery

1. Setup + Foundational → Data pipeline ready
2. Add US1 (summary) → Visual coverage overview
3. Add US2 (action items) → Full endpoint listing by tier
4. Add US3 (instructions) → Actionable step-by-step guidance
5. Add US4 (entry point) → Single-command generation
6. Polish → Validation and edge cases

---

## Notes

- All source files use stdlib only — no pip install needed
- Parsers are regex-based per research.md decision R1/R2
- HTML is self-contained (inline CSS, no external resources)
- `progress.html` is a build artifact, not committed to git
- Commit after each phase checkpoint
