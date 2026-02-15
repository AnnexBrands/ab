# Tasks: Verify Artifact Integrity

**Input**: Design documents from `/specs/006-verify-artifact-integrity/`
**Prerequisites**: plan.md (required), spec.md (required), contracts/audit-checks.md

**Tests**: Not applicable — this is a verification/audit feature, not new code.

**Organization**: Tasks grouped by user story. US1 runs examples and audits outputs. US2 cross-references artifacts. US3 corrects discrepancies.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: User Story 1 — Run All Examples and Audit Outputs (Priority: P1)

**Goal**: Run every example module against staging. Flag any that error, warn, or produce unexpected output. Verify every "captured" fixture file exists on disk.

**Independent Test**: Every entry with `fixture_file` in `examples/` succeeds against staging and the named file exists in `tests/fixtures/`.

### Audit Execution

- [x] T001 [US1] Run `python -m examples address` against staging, capture output, record pass/fail for each entry
- [x] T002 [P] [US1] Run `python -m examples autoprice` against staging, capture output, record pass/fail
- [x] T003 [P] [US1] Run `python -m examples companies` against staging, capture output, record pass/fail
- [x] T004 [P] [US1] Run `python -m examples contacts` against staging, capture output, record pass/fail
- [x] T005 [P] [US1] Run `python -m examples documents` against staging, capture output, record pass/fail
- [x] T006 [P] [US1] Run `python -m examples jobs` against staging, capture output, record pass/fail
- [x] T007 [P] [US1] Run `python -m examples lookup` against staging, capture output, record pass/fail
- [x] T008 [P] [US1] Run `python -m examples sellers` against staging, capture output, record pass/fail
- [x] T009 [P] [US1] Run `python -m examples shipments` against staging, capture output, record pass/fail
- [x] T010 [P] [US1] Run `python -m examples users` against staging, capture output, record pass/fail
- [x] T011 [P] [US1] Run `python -m examples web2lead` against staging, capture output, record pass/fail
- [x] T012 [P] [US1] Run `python -m examples forms` against staging, capture output, record pass/fail
- [x] T013 [P] [US1] Run `python -m examples timeline` against staging, capture output, record pass/fail
- [x] T014 [P] [US1] Run `python -m examples tracking` against staging, capture output, record pass/fail
- [x] T015 [P] [US1] Run `python -m examples payments` against staging, capture output, record pass/fail
- [x] T016 [P] [US1] Run `python -m examples notes` against staging, capture output, record pass/fail
- [x] T017 [P] [US1] Run `python -m examples parcels` against staging, capture output, record pass/fail
- [x] T018 [P] [US1] Run `python -m examples lots` against staging, capture output, record pass/fail
- [x] T019 [P] [US1] Run `python -m examples catalog` against staging, capture output, record pass/fail

### Audit Analysis

- [x] T020 [US1] Compile audit results: list all entries that errored or warned, grouped by module. Note which were expected failures (needs-request-data) vs unexpected failures (claimed captured but failed).

**Checkpoint**: Full audit log of all example outputs. Every unexpected failure identified.

---

## Phase 2: User Story 2 — Cross-Reference Artifact Consistency (Priority: P2)

**Goal**: Verify FIXTURES.md, api-surface.md, examples/, and tests/fixtures/ all agree.

**Independent Test**: Zero discrepancies between any two tracking artifacts.

### Cross-Reference Checks

- [x] T021 [US2] Check 1 (from contracts/audit-checks.md): Verify every `.json` file in `tests/fixtures/` has a corresponding "captured" row in `FIXTURES.md`, and every captured row has a file on disk
- [x] T022 [P] [US2] Check 4: Verify every `runner.add()` entry with `fixture_file` param in `examples/*.py` has the named file in `tests/fixtures/`
- [x] T023 [P] [US2] Check 6: Count rows in FIXTURES.md captured and needs-request-data tables, compare against summary counts in the Summary section
- [x] T024 [US2] Check 2: Verify every fixture file in `tests/fixtures/` parses against its Pydantic model by running `pytest tests/models/ -v`
- [x] T025 [US2] Compile cross-reference findings: list all discrepancies with endpoint path, claimed status, actual status, and source document

**Checkpoint**: Complete list of all cross-reference discrepancies.

---

## Phase 3: User Story 3 — Fix and Update Tracking Documents (Priority: P3)

**Goal**: Correct all discrepancies found in US1 and US2. Update FIXTURES.md, api-surface.md, and regenerate progress report.

**Independent Test**: Re-run US1 and US2 audits and confirm zero findings.

### Corrections

- [x] T026 [US3] Fix FIXTURES.md: move any falsely-captured endpoints to needs-request-data section with failure description. Update summary counts to match actual row counts.
- [x] T027 [P] [US3] Fix api-surface.md: downgrade any falsely-done endpoints to pending with note. Correct any endpoints missing from tracking.
- [x] T028 [P] [US3] Fix examples: update any example entries with wrong `fixture_file` references or incorrect parameters discovered during audit.
- [x] T029 [US3] Regenerate progress report by running `python scripts/generate_progress.py > progress.html`

### Re-verification

- [x] T030 [US3] Re-run FIXTURES.md count check (T023 logic): summary counts match row counts
- [x] T031 [US3] Re-run fixture file cross-reference (T021 logic): every captured entry has a file, every file has an entry
- [x] T032 [US3] Run `pytest --ignore=tests/integration -q` to confirm no test regressions from corrections

**Checkpoint**: All tracking artifacts internally consistent. Zero discrepancies on re-audit.

---

## Phase 4: Polish & Cross-Cutting Concerns

- [x] T033 Run `ruff check .` on any modified files
- [x] T034 Verify FIXTURES.md, api-surface.md, and progress.html are all current

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (US1)**: No prerequisites — can start immediately
- **Phase 2 (US2)**: Can start in parallel with Phase 1 (T021-T024 don't need example output)
- **Phase 3 (US3)**: Depends on both US1 and US2 findings
- **Phase 4 (Polish)**: After US3 corrections

### Within Phase 1

- T001-T019 are all independent — can run in parallel
- T020 depends on all T001-T019 completing

### Within Phase 2

- T021-T024 are independent cross-reference checks — can run in parallel
- T025 depends on all checks completing

### Parallel Opportunities

```
T001 ─┐
T002 ─┤
...   ├→ T020 ─┐
T019 ─┘        │
               ├→ T026 → T027 → T028 → T029 → T030 → T031 → T032 → T033 → T034
T021 ─┐        │
T022 ─┤        │
T023 ─├→ T025 ─┘
T024 ─┘
```

## Implementation Strategy

### MVP First (US1 Only)

1. Run all 19 example modules against staging (T001-T019)
2. Compile findings (T020)
3. **STOP and ASSESS**: How many unexpected failures?

### Full Delivery

1. US1: Run examples (T001-T020)
2. US2: Cross-reference artifacts (T021-T025)
3. US3: Fix discrepancies (T026-T032)
4. Polish (T033-T034)

---

## Notes

- T001-T019 require staging API credentials to be configured
- Examples with `# TODO` comments indicating needs-request-data are expected to fail — not discrepancies
- The audit only downgrades status (captured→needs-request-data, done→pending), never upgrades
- All corrections go into existing tracking files — no new files created
