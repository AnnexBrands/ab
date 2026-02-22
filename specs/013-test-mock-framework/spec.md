# Feature Specification: Unified Test Mock Framework

**Feature Branch**: `013-test-mock-framework`
**Created**: 2026-02-21
**Status**: Draft
**Input**: User description: "attempt to resolve failing endpoints. we should have tests constants already, but perhaps we need a better framework for test mocks to provide information acceptable to provide in examples, tests, and sphinx"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Centralized Test Constants and Mock Data (Priority: P1)

A developer working on the SDK needs a single, authoritative source of realistic test identifiers and mock data values that can be used consistently across unit tests, integration tests, example scripts, and Sphinx documentation. Currently, identifiers like `LIVE_COMPANY_UUID` are duplicated between `tests/constants.py` and individual example files (e.g., `examples/companies.py`). The developer needs one shared constants module that all consumers import from, eliminating drift and providing acceptable placeholder values for every entity type the SDK covers.

**Why this priority**: Without consistent, centralized test data, every other improvement (offline testing, fixture generation, documentation) is built on a fragile foundation. This is the prerequisite for all subsequent stories.

**Independent Test**: Can be fully tested by verifying that all test files, example scripts, and documentation reference a single constants source, and that no duplicate identifier definitions exist outside that source.

**Acceptance Scenarios**:

1. **Given** a developer imports test constants, **When** they use any entity identifier (company UUID, contact ID, job ID, catalog ID, etc.), **Then** the value comes from a single shared constants module with no duplicated definitions elsewhere.
2. **Given** the constants module exists, **When** a new entity type is added to the SDK, **Then** there is a clear pattern for adding the corresponding test constant with documentation of what it represents and where it was sourced.
3. **Given** example scripts reference constants, **When** Sphinx autodoc processes those examples, **Then** the rendered documentation shows meaningful placeholder values (not bare UUIDs or raw IDs without context).

---

### User Story 2 - Offline Model Validation Tests (Priority: P2)

A developer wants to run model validation tests without live staging credentials. Currently, model tests in `tests/models/` load JSON fixtures from disk and validate them with Pydantic, but many endpoints lack fixtures (126 of 161 endpoints have G2=FAIL). The developer needs a structured pattern for manually authoring mock fixture data for any response model, enabling tests to validate model schemas offline and identify field mismatches (like the UserRole model expecting a dict when the API returns strings).

**Why this priority**: Offline testing unblocks CI/CD pipelines and contributor workflows that cannot access staging credentials. It also surfaces model-API mismatches before live testing.

**Independent Test**: Can be tested by running the full model test suite without network access and verifying that all model tests either pass or produce meaningful xfail markers for known mismatches.

**Acceptance Scenarios**:

1. **Given** no staging credentials are configured, **When** a developer runs `pytest tests/models/`, **Then** all model fixture tests execute using locally-generated mock data and produce pass/fail results without network errors or skips due to missing credentials.
2. **Given** a fixture does not exist on disk, **When** a developer needs to test that model, **Then** there is a clear pattern for manually authoring a mock fixture with correct structure, types, and realistic values.
3. **Given** a model has a known mismatch with the API (e.g., UserRole), **When** a mock fixture is authored, **Then** it reflects the actual API response shape (not the model's expected shape), allowing the test to surface the mismatch as a clear failure.

---

### User Story 3 - Reusable Mock Data for Sphinx Documentation (Priority: P3)

A documentation author needs example response data embedded in Sphinx-generated API docs. Currently, examples rely on live API calls to capture fixture data, which means documentation builds require staging access. The mock framework should provide example-quality data that renders well in documentation — realistic field values, proper formatting, and no sensitive or nonsensical placeholder data.

**Why this priority**: Documentation quality directly affects SDK adoption. Providing realistic, well-formatted example responses in docs makes the SDK self-documenting and reduces support burden.

**Independent Test**: Can be tested by building Sphinx docs without staging credentials and verifying that example response data appears in the rendered output with realistic, non-sensitive values.

**Acceptance Scenarios**:

1. **Given** the Sphinx documentation build process, **When** docs are generated, **Then** example API responses appear with realistic placeholder data that demonstrates the shape and content of each endpoint's response.
2. **Given** mock data is used in documentation, **When** a reader views the rendered docs, **Then** all example values are plausible and non-sensitive (no real customer data, real emails, or real credentials).
3. **Given** a new endpoint model is added to the SDK, **When** the developer follows the established pattern and authors a mock fixture, **Then** mock data for the new model is available for documentation.

---

### User Story 4 - Resolve Currently Failing Endpoints (Priority: P1)

A developer needs the 13 currently failing tests and 32 xfailed tests to be resolved or triaged. Failures stem from model-API mismatches (e.g., UserRole receives `List[str]` but expects dict objects), HTTP 404 errors from staging, and missing fixture data. The mock framework should provide the data infrastructure to fix these failures, convert xfails to passing tests where possible, or properly categorize remaining issues as expected failures with clear remediation paths.

**Why this priority**: Failing tests erode confidence in the test suite. Resolving them is a direct deliverable tied to this feature.

**Independent Test**: Can be tested by running `pytest` and verifying that the 13 currently-failing tests are either fixed or converted to well-documented xfails with actionable remediation notes.

**Acceptance Scenarios**:

1. **Given** the current 13 test failures, **When** the mock framework and model fixes are applied, **Then** tests that fail due to model-API mismatches are fixed by correcting the model or test expectations to match actual API behavior.
2. **Given** tests that fail due to staging API errors (HTTP 500), **When** the mock framework is available, **Then** those tests can run against mock data offline, isolating the staging instability from the test results.
3. **Given** tests that fail due to missing fixture data, **When** the mock framework can generate structurally valid data, **Then** those tests have a path to execution without requiring a live capture first.

---

### Edge Cases

- What happens when a model defines fields that don't exist in the API response (extra fields in model)?
- How does the system handle polymorphic responses where the same endpoint returns different shapes based on query parameters?
- What happens when a fixture file exists on disk but is stale (schema has evolved since capture)?
- How does the mock framework handle paginated responses (`PaginatedList` wrappers with `data`/`items` arrays)?
- What happens when a model uses `List[str]` but the mock framework generates `List[dict]` or vice versa?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a single, authoritative constants module containing all test entity identifiers (UUIDs, IDs, codes) used across tests, examples, and documentation.
- **FR-002**: System MUST eliminate duplicate constant definitions — any test identifier currently defined in example files or individual test modules MUST be imported from the shared constants module.
- **FR-003**: System MUST provide a structured pattern and tooling for manually authoring mock fixture data for any Pydantic response model defined in the SDK, with clear guidance on required fields, types, and realistic placeholder values.
- **FR-004**: System MUST allow model validation tests to execute fully offline (no network access, no staging credentials) using generated or pre-built mock data.
- **FR-005**: System MUST produce mock data with realistic, non-sensitive values suitable for rendering in Sphinx documentation and example code.
- **FR-006**: System MUST resolve the currently known model-API mismatches (e.g., UserRole) by either correcting the model to match actual API behavior or documenting the mismatch as an expected failure with remediation guidance.
- **FR-007**: System MUST handle paginated response wrappers (`PaginatedList`, `{data: [...]}`, `{items: [...]}`) when generating mock data, producing correctly shaped wrapper structures.
- **FR-008**: System MUST support variant fixtures (e.g., `SellerExpandedDto_detail` as a variant of `SellerExpandedDto`) in the mock data framework.
- **FR-009**: System MUST integrate with the existing quality gate system (G1-G5) such that manually-authored mock fixtures count toward G2 (Fixture Status) evaluation. When both a live-captured and mock fixture exist for the same model, the live fixture takes precedence for all test and gate evaluations.
- **FR-010**: System MUST store manually-authored mock fixtures in a separate `tests/fixtures/mocks/` subdirectory, distinct from live-captured fixtures in `tests/fixtures/`. The fixture loader MUST fall back from live to mock automatically (live takes precedence when both exist).

### Key Entities

- **TestConstants**: Centralized registry of entity identifiers (UUIDs, integer IDs, display IDs, codes) sourced from staging or fabricated for mock-only use, with metadata about provenance.
- **MockFixture**: A manually-authored JSON data structure conforming to a Pydantic response model's schema, with realistic placeholder values, suitable for model validation, example rendering, and documentation.
- **FixtureManifest**: Implicit via directory structure — `tests/fixtures/` contains live-captured data, `tests/fixtures/mocks/` contains manually-authored mock data. No separate manifest file needed; provenance is determined by file location.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All model validation tests (`tests/models/`) pass or are explicitly xfailed when run without staging credentials (zero skips due to missing credentials or fixtures).
- **SC-002**: The 13 currently-failing tests are resolved — each is either fixed, converted to a documented xfail, or demonstrated to pass against mock data. Additionally, all 32 existing xfailed tests are triaged for potential fixes, with each either converted to passing or retained as xfail with updated remediation notes.
- **SC-003**: No test identifier (UUID, ID, code) is defined in more than one location — all consumers import from the shared constants module.
- **SC-004**: Sphinx documentation builds successfully without staging credentials, with example response data appearing in rendered output for all documented endpoints.
- **SC-005**: New endpoint models added to the SDK have a clear, documented pattern for manually authoring mock fixtures, with guidance on required fields and realistic values.
- **SC-006**: The fixture coverage rate (G2 gate) improves from the current 35/161 (22%) to at least 80/161 (50%) through combined live captures and mock-generated fixtures.

## Clarifications

### Session 2026-02-21

- Q: When both a live-captured and a mock fixture exist for the same model, which takes precedence? → A: Live always wins — if a live fixture exists, mock is ignored for tests and gates. Missing mock fixtures are manually authored by the developer (not auto-generated).
- Q: Should this feature address the 32 xfailed tests in addition to the 13 hard failures? → A: Yes, address both — resolve the 13 failures and triage all 32 xfails for potential fixes.
- Q: Where should mock fixtures live relative to existing `tests/fixtures/`? → A: Subdirectory — mock fixtures in `tests/fixtures/mocks/`, live fixtures stay in `tests/fixtures/`. Loader falls back from live to mock automatically.

## Assumptions

- The existing `tests/fixtures/` directory structure and naming convention (`ModelName.json`) will be preserved for live-captured fixtures. Manually-authored mock fixtures will be stored in `tests/fixtures/mocks/` using the same naming convention. The fixture loader extends to check both locations with live taking precedence.
- Live-captured fixtures remain the gold standard; mock-generated fixtures serve as scaffolding until live data can be captured.
- The Pydantic model definitions in `ab/api/models/` accurately represent the intended response schema, even where they currently mismatch with live API behavior (mismatches are bugs to be fixed, not design).
- The three OpenAPI schemas (`acportal.json`, `catalog.json`, `abc.json`) are accurate enough to use as supplementary type information when generating mock data.
- Example scripts in `examples/` will continue using the `ExampleRunner` pattern; the mock framework integrates with this pattern rather than replacing it.

## Scope Boundaries

**In scope**:
- Centralized constants module consolidation
- Mock data generation for Pydantic response models
- Resolving known test failures (13 failures + 32 xfails + model mismatches)
- Integration with existing fixture loading and quality gates
- Documentation-quality example data

**Out of scope**:
- Rewriting the ExampleRunner capture workflow
- Adding new API endpoints or models
- Changing the live integration test strategy (those remain live-only)
- Performance testing or load testing infrastructure
- Request model mock generation (beyond what exists in `tests/fixtures/requests/`)
