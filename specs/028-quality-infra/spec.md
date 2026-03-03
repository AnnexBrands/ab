# Feature Specification: Quality Infrastructure Sprint

**Feature Branch**: `028-quality-infra`
**Created**: 2026-03-02
**Status**: Draft
**Input**: User description: "Quality infrastructure sprint derived from 027 PR analysis (specs/027-reports-lookups-gates/pr-analysis.md) — recommendations R1-R9"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Gate Regression Ratchet (Priority: P1)

A developer merges a PR that changes a model field name. An endpoint that previously passed G1 (Model Fidelity) now silently fails. No automated check catches it. Over successive features (#21, #24, #32), 7 test failures accumulated without detection. The project needs a one-directional ratchet that prevents any previously-passing gate from regressing.

After this story, a baseline file records which individual gates each endpoint passes (per-endpoint-per-gate granularity). Any PR that causes a previously-passing gate on any endpoint to fail is caught automatically by the test suite before merge — even if the endpoint never passed all 6 gates.

**Why this priority**: This is the single highest-impact improvement. Without a ratchet, every future feature risks undoing prior gate gains. The 7 pre-existing failures prove the problem is real and recurring.

**Independent Test**: Intentionally break a passing model (e.g., rename a field), run the test suite, and confirm the regression test fails with a clear message identifying which endpoint regressed and which gate failed.

**Acceptance Scenarios**:

1. **Given** a baseline file records per-gate pass status for each endpoint (e.g., endpoint X passes G1, G2, G5), **When** a model change causes endpoint X to fail G1, **Then** the regression test fails and names the regressed endpoint and gate — even though X never passed all 6 gates
2. **Given** a new endpoint passes some gates, **When** the baseline is updated, **Then** each passing gate for that endpoint is recorded and future regressions on any of them are caught
3. **Given** a developer intentionally changes a model (legitimate refactor), **When** they update the baseline file, **Then** the regression test passes with the new baseline

---

### User Story 2 - Unified Fixture Handling (Priority: P2)

Three competing patterns exist for handling list-shaped fixtures across the codebase: inline `isinstance` checks in `test_lookup_models.py`, duplicated `_first_or_skip` helpers in `test_report_models.py` and `test_extended_lookup_models.py`, and a different `isinstance` pattern in `gates.py`. When a fixture changes shape, each location may break independently.

After this story, a single canonical helper exists in `tests/conftest.py` for tests and a single helper exists in the gate evaluation module. All test files use the canonical helper.

**Why this priority**: Eliminates an entire class of fixture-shape-mismatch bugs. Every future model test file benefits immediately.

**Independent Test**: Change a fixture from dict to list (or vice versa), run the full test suite, and confirm the canonical helper handles it correctly everywhere.

**Acceptance Scenarios**:

1. **Given** a `first_or_skip` helper exists in `tests/conftest.py`, **When** any model test encounters a list-shaped fixture, **Then** it extracts the first element or skips on empty list using the shared helper
2. **Given** a gate evaluation `unwrap_fixture` helper exists, **When** gates evaluate a list-shaped fixture, **Then** it unwraps consistently using the same logic as the test helper
3. **Given** all duplicated `_first_or_skip` definitions are removed from individual test files, **When** `grep -r "_first_or_skip" tests/` is run, **Then** only `conftest.py` contains the definition

---

### User Story 3 - Fix Pre-Existing Test Failures (Priority: P3)

7 pre-existing test failures create noise that obscures real regressions. 5 of these are easy fixes (wrong argument style, empty-list handling, missing fixture, undeclared model fields). The remaining 2 involve FIXTURES.md structural drift. All 7 must be resolved to establish a clean baseline for the gate ratchet.

**Why this priority**: The gate ratchet (US1) requires a clean test suite to establish a meaningful baseline. Fixing these failures is a prerequisite.

**Independent Test**: Run `pytest` and confirm zero failures (excluding expected xfails).

**Acceptance Scenarios**:

1. **Given** `test_list_users` fails due to a positional argument after keyword-only refactor, **When** the call is fixed to use keyword syntax, **Then** the test passes
2. **Given** `test_priced_freight_provider` fails because the test expects a dict but the fixture is an empty list, **When** the test uses the canonical `first_or_skip` helper, **Then** the test skips gracefully on empty-list fixtures
3. **Given** `test_user_role` fails due to a missing `UserRole.json` fixture, **When** the test is updated to handle the `List[str]` return type, **Then** the test passes or skips with an actionable message
4. **Given** `test_search_contact_entity_result` and `test_response_field_values` fail due to 31 undeclared extra fields, **When** the `SearchContactEntityResult` model is expanded with the missing fields, **Then** both tests pass
5. **Given** `test_all_fixture_files_tracked` fails because 62 fixtures are untracked and `test_captured_fixtures_exist_on_disk` fails because request fixtures live in a `requests/` subdirectory, **When** FIXTURES.md tracking and mock coverage scanning are corrected, **Then** both tests pass

---

### User Story 4 - FIXTURES.md Integrity Repair (Priority: P4)

`test_mock_coverage.py` scans raw fixture directories and compares against FIXTURES.md entries, but the two use different organizational models. FIXTURES.md is route-centric while the directory scan is file-centric. Request fixtures in `tests/fixtures/requests/` are not scanned, yet FIXTURES.md lists them as captured. This produces 62 untracked files and 18 "captured but missing" false positives.

After this story, the mock coverage test correctly scans all fixture subdirectories and FIXTURES.md accurately reflects reality.

**Why this priority**: FIXTURES.md is the central tracking artifact (Constitution Principle V). When it drifts from reality, all downstream tooling and human decision-making is based on inaccurate data.

**Independent Test**: Run `pytest tests/test_mock_coverage.py` and confirm all assertions pass. Manually compare FIXTURES.md entries against actual files on disk and confirm agreement.

**Acceptance Scenarios**:

1. **Given** the mock coverage test scans `tests/fixtures/`, `tests/fixtures/mocks/`, and `tests/fixtures/requests/`, **When** run against the current fixture set, **Then** no "untracked" or "missing" fixtures are reported
2. **Given** FIXTURES.md is regenerated with current fixture state, **When** compared to the file system, **Then** every listed fixture has a corresponding file and every file on disk is listed
3. **Given** a developer adds a new request fixture in `tests/fixtures/requests/`, **When** FIXTURES.md is regenerated, **Then** the new fixture appears in the tracking

---

### User Story 5 - Batch Fixture Capture Tooling (Priority: P5)

Closing the G2 gap (106 passing out of 231) requires capturing approximately 125 more fixtures. At the current manual rate of ~20 fixtures per feature, this would take 6-7 more features. A batch capture script that reads FIXTURES.md, identifies G2-failing endpoints, checks for existing examples, and runs them in sequence would dramatically accelerate progress.

**Why this priority**: The binding constraint toward 100% gates is G1 -> G2 -> G3 (model -> fixture -> test). Batch fixture capture directly attacks the bottleneck.

**Independent Test**: Run the batch capture script, confirm it produces a summary listing captured, failed, and needs-example endpoints, and verify that newly captured fixtures pass G1 validation.

**Acceptance Scenarios**:

1. **Given** the batch script reads FIXTURES.md for all G2-FAIL endpoints, **When** an example exists for a failing endpoint, **Then** the script runs the example and captures the fixture if a 200 response is received
2. **Given** an endpoint has no example, **When** the batch script encounters it, **Then** it reports the endpoint as "needs-example" without erroring
3. **Given** a batch run completes, **When** the summary is printed, **Then** it shows counts of captured, failed, and needs-example endpoints

---

### User Story 6 - Auto-Generate Model Test Stubs (Priority: P6)

96 endpoints fail G3 (Test Quality) because they lack `isinstance()` and `assert_no_extra_fields()` assertions. Writing these tests by hand is tedious and follows a mechanical pattern. A generator that reads Route definitions and produces test stubs would close most of the G3 gap in a single run.

**Why this priority**: G3 is the third gate in the dependency chain. Once G1 and G2 improve via earlier stories, G3 becomes the new bottleneck. Generated stubs auto-skip when fixtures are missing.

**Independent Test**: Run the generator, confirm it produces test files, and run `pytest` on the generated tests to verify they either pass (if fixtures exist) or skip (if fixtures are missing).

**Acceptance Scenarios**:

1. **Given** the generator reads all Route definitions with a `response_model`, **When** run, **Then** it produces test functions with `isinstance` and `assert_no_extra_fields` assertions
2. **Given** a model already has a test, **When** the generator encounters it, **Then** it skips generation to avoid duplicates
3. **Given** a generated test references a model without a fixture, **When** pytest runs, **Then** the test skips with an actionable message naming the missing fixture

---

### User Story 7 - Return Type Annotation Sweep (Priority: P7)

78 endpoints fail G4 (Doc Accuracy) because their return type annotation is `Any` or missing. The correct return type is known from each Route's `response_model` field. This is a mechanical fix: replace `-> Any` with `-> ModelName` or `-> list[ModelName]`.

**Why this priority**: G4 is a low-effort, high-reward cleanup. The fixes are mechanical and the correct values are already defined on Route objects.

**Independent Test**: Run `pytest` with gate evaluation and confirm G4 pass count increases by at least 50 endpoints.

**Acceptance Scenarios**:

1. **Given** an endpoint method returns `-> Any` and its Route has a `response_model`, **When** the return type is updated, **Then** G4 passes for that endpoint
2. **Given** an endpoint returns a list, **When** the return type is updated, **Then** it uses `list[ModelName]` syntax
3. **Given** all mechanical fixes are applied, **When** the gate evaluation runs, **Then** G4 pass count is at least 200 out of 231

---

### User Story 8 - No-Response Endpoint Exemptions (Priority: P8)

Approximately 52 endpoints have no `response_model` (DELETE operations, fire-and-forget POSTs, byte-stream returns). They count against the 231 total denominator, distorting gate percentages. Adding an exemption flag to Route and adjusting gate counting makes the denominator honest and the 100% target realistic.

**Why this priority**: Without this, 100% is unreachable for G1-G3 since void endpoints cannot meaningfully have model fidelity or fixture tests.

**Independent Test**: Add the exemption flag, run gate evaluation, and confirm the denominator changes from 231 to approximately 179 (231 minus exempted endpoints).

**Acceptance Scenarios**:

1. **Given** a Route has `no_response=True`, **When** gate evaluation runs, **Then** that endpoint is excluded from G1, G2, and G3 denominators
2. **Given** all void/byte-stream endpoints are flagged, **When** the progress report runs, **Then** the "all pass" percentage reflects only meaningful endpoints
3. **Given** an exempted endpoint is later given a response model, **When** `no_response` is removed, **Then** it re-enters the gate denominator

---

### Edge Cases

- What happens when the gate baseline file does not yet exist (first run)? The ratchet test should generate it automatically from the current state.
- What happens when the batch capture script encounters an API timeout or 500 error? It should record the failure and continue to the next endpoint, not abort.
- What happens when the test stub generator encounters an endpoint with multiple response models (e.g., different models for list vs detail)? It should generate one test per Route entry.
- What happens when a fixture is legitimately removed (endpoint deprecated)? The baseline update process should support both additions and removals.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a gate regression test that loads a per-endpoint-per-gate baseline and fails if any individual gate that previously passed for an endpoint now fails
- **FR-002**: System MUST provide a command to update the gate baseline after intentional changes
- **FR-003**: System MUST provide a canonical `first_or_skip` helper in the shared test configuration that handles dict passthrough, list-first-element extraction, and empty-list skipping
- **FR-004**: System MUST provide a canonical `unwrap_fixture` helper in the gate evaluation module with equivalent logic
- **FR-005**: System MUST remove all duplicated fixture-unwrapping patterns from individual test files and replace them with the canonical helper
- **FR-006**: System MUST fix all 7 pre-existing test failures to establish a clean suite baseline
- **FR-007**: System MUST update fixture tracking to correctly scan response fixtures, request fixtures, and mock fixtures in their respective subdirectories
- **FR-008**: System MUST ensure FIXTURES.md reflects the actual state of fixtures on disk after regeneration
- **FR-009**: System MUST provide a batch capture script that reads fixture status, runs existing examples, captures 200 responses, and reports results
- **FR-010**: System MUST provide a test stub generator that reads Route definitions and produces model validation test functions
- **FR-011**: System MUST update return type annotations on endpoint methods to match their Route's `response_model`
- **FR-012**: System MUST provide a Route-level flag to exempt endpoints with no meaningful response from gate evaluation denominators
- **FR-013**: System MUST not introduce any new test failures — all existing passing tests must continue to pass
- **FR-014**: System MUST expand the `SearchContactEntityResult` model with the 31 undeclared fields found in the captured fixture

### Key Entities

- **Gate Baseline**: A per-endpoint-per-gate record mapping each endpoint to the set of gates it currently passes (e.g., `{"/api/reports/sales POST": ["G1", "G2", "G5"]}`). Used as the ratchet reference point — any gate that appears in the baseline for an endpoint must continue to pass
- **Route Exemption**: A flag on Route definitions indicating the endpoint has no meaningful response model and should be excluded from model-related gate denominators
- **Batch Capture Summary**: Output of the batch fixture capture tool listing captured, failed, and needs-example endpoints

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Zero test failures in the full pytest suite (excluding expected xfails) — down from 7 pre-existing failures
- **SC-002**: Gate regression ratchet test exists and prevents previously-passing endpoints from silently regressing
- **SC-003**: All duplicated `_first_or_skip` patterns are consolidated into a single canonical location — grep confirms only one definition
- **SC-004**: FIXTURES.md integrity tests pass — zero untracked files and zero "captured but missing" false positives
- **SC-005**: Batch fixture capture tool can process all G2-failing endpoints in a single run and report results
- **SC-006**: Test stub generator produces valid test functions that pass or skip appropriately for at least 40 endpoints
- **SC-007**: G4 (Doc Accuracy) pass count increases to at least 200 out of 231 after the return type annotation sweep
- **SC-008**: Gate evaluation denominator adjusts to exclude exempted no-response endpoints, reducing from 231 to approximately 179
- **SC-009**: Overall "all gates pass" count increases to at least 130 endpoints (up from 69)

## Clarifications

### Session 2026-03-02

- Q: Should the gate ratchet track per-endpoint-per-gate (each individual gate an endpoint passes) or only the "all gates pass" set? → A: Per-endpoint-per-gate — the baseline records which individual gates each endpoint passes, and any individual gate regression is caught even if the endpoint never passed all 6 gates.

## Assumptions

- The 7 pre-existing test failures documented in the 027 PR analysis are still the current set of failures — no additional failures have been introduced since
- The gate evaluation infrastructure in `ab/progress/gates.py` is stable and its `evaluate_all_gates()` function can be called programmatically for the ratchet test
- The approximately 52 no-response endpoints can be identified from Route definitions by checking for missing `response_model` fields
- The staging API is available for batch fixture capture runs, though individual endpoints may return errors (which the batch tool will handle gracefully)
- The `SearchContactEntityResult` fixture contains the 31 extra fields needed to expand the model — the fixture is the source of truth for field names and types
- Generated test stubs follow the existing pattern in `tests/models/` and integrate with the existing `conftest.py` fixtures and helpers
