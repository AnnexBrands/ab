# Feature Specification: CLI Gate Sweep

**Feature Branch**: `026-cli-gate-sweep`
**Created**: 2026-03-01
**Status**: Draft
**Input**: CLI listing cleanup + systematic GET endpoint quality gate fixes

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Clean CLI Method Listing (Priority: P1)

As a developer using the CLI, when I run `ab payments` to list methods in an endpoint, I want to see only the method name, parameters, and return type — not the raw route path. The route is useful detail for individual method help (`ab payments get --help`) but clutters the listing view.

**Why this priority**: The CLI listing is the first thing developers see. A clean, scannable view helps them quickly find the method they need without visual noise.

**Independent Test**: Run `ab payments` and verify the output shows method names and parameter summaries without HTTP method/route paths. Then run `ab payments get --help` and verify the route IS shown there.

**Acceptance Scenarios**:

1. **Given** the CLI is installed, **When** the user runs `ab payments`, **Then** the output lists method names and parameter summaries without route paths
2. **Given** the CLI is installed, **When** the user runs `ab payments get --help`, **Then** the output includes the full route path (e.g., `GET /job/{jobDisplayId}/payment`)
3. **Given** the CLI is installed, **When** the user runs `ab jobs`, **Then** helper methods (no route) and API methods are both listed without route clutter

---

### User Story 2 - GET Endpoints Pass Quality Gates Without Manual Input (Priority: P1)

As a developer running the example runner (`ex jobs get_tracking`), I should not have to manually supply path parameter values. The system should automatically resolve required path parameters (like `jobDisplayId`) to known test constants (like `TEST_JOB_DISPLAY_ID`). Every GET endpoint example should run zero-config against staging.

**Why this priority**: This is the core deliverable. GET endpoints that fail quality gates because they can't find their required constants represent broken developer experience and false negatives in the progress report.

**Independent Test**: Run `ex jobs get_tracking` and verify it automatically uses `TEST_JOB_DISPLAY_ID` without any explicit argument. Check the progress report and confirm the endpoint's gate status improves.

**Acceptance Scenarios**:

1. **Given** a GET endpoint requires `jobDisplayId`, **When** the example is run, **Then** the system automatically maps to `TEST_JOB_DISPLAY_ID` from constants
2. **Given** a GET endpoint requires `historyAmount` (not in constants), **When** the constant is missing, **Then** a sensible default is added to constants using the `TEST_` prefix naming convention (e.g., `TEST_HISTORY_AMOUNT = 3`)
3. **Given** the example runner returns "received extras" errors, **When** the response model has extra fields, **Then** the model is updated to match ground truth from swagger or the captured fixture

---

### User Story 3 - Chain Discovery for Missing Constants (Priority: P2)

As a developer, when a GET endpoint requires an ID that isn't in constants (e.g., `rfqId`), the system should be smart enough to discover it by chaining API calls. For example, first list RFQs for the known `TEST_JOB_DISPLAY_ID`, then extract an `rfqId` from the response to use in subsequent calls.

**Why this priority**: Some endpoints require IDs that can only be obtained from parent resources. Without chain discovery, these endpoints remain untestable and permanently fail gates.

**Independent Test**: Run an example that requires an `rfqId`. Verify it first calls a listing endpoint using `TEST_JOB_DISPLAY_ID`, extracts the ID, then uses it for the target call.

**Acceptance Scenarios**:

1. **Given** a GET endpoint requires `rfqId`, **When** no `TEST_RFQ_ID` constant exists, **Then** the system lists RFQs for `TEST_JOB_DISPLAY_ID` and extracts a valid ID
2. **Given** a chain discovery call returns results, **When** an ID is extracted, **Then** it is stored as a constant for reuse (e.g., `TEST_RFQ_ID`)
3. **Given** a chain discovery call returns empty results, **When** no valid ID can be found, **Then** the endpoint is skipped with a clear message rather than failing silently

---

### User Story 4 - Handle "Received Extras" Model Mismatches (Priority: P2)

As a developer, when running an example and the API returns fields not declared in the response model, I need clear guidance on how to fix it. The system should compare against swagger definitions and captured fixtures, then update models to match ground truth.

**Why this priority**: "Received extras" errors are the most common gate failure. They indicate the model is incomplete, which blocks fixture validation and test coverage.

**Independent Test**: Run an example that produces "received extras". Verify the error message identifies which fields are missing. Update the model, re-run, and confirm the error is resolved.

**Acceptance Scenarios**:

1. **Given** an API response contains fields not in the model, **When** the example runs, **Then** the error message lists the extra field names
2. **Given** extra fields are identified, **When** the swagger definition is consulted, **Then** the model is updated with correct field types and optionality
3. **Given** a model is updated with extra fields, **When** the example is re-run, **Then** it passes without "received extras" warnings

---

### Edge Cases

- What happens when a path parameter has no matching constant and no parent listing endpoint exists? The endpoint should be skipped with a log message, not crash.
- What happens when the staging environment has no data for a test constant (e.g., no jobs exist for `TEST_JOB_DISPLAY_ID`)? The example should report the HTTP error clearly without masking the root cause.
- What happens when a constant name derived from camelCase is ambiguous (e.g., `jobSubKey` could be `TEST_JOB_SUB_KEY`)? The naming convention is deterministic: camelCase → SCREAMING_SNAKE with TEST_ prefix.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: CLI method listing (`ab <endpoint>`) MUST show only method names and parameter summaries, omitting route paths
- **FR-002**: CLI method help (`ab <endpoint> <method> --help`) MUST continue showing the full route path, HTTP method, parameters, and return type
- **FR-003**: The example runner MUST automatically resolve path parameters to test constants using the `camelCase → TEST_SCREAMING_SNAKE` naming convention
- **FR-004**: Missing constants MUST be added to `tests/constants.py` with educated defaults and the `TEST_` prefix
- **FR-005**: When a required ID cannot be found in constants, the system MUST attempt chain discovery by calling a parent listing endpoint with a known constant
- **FR-006**: Response models that produce "received extras" warnings MUST be updated to match the swagger definition or captured fixture ground truth
- **FR-007**: After all fixes, the progress report MUST show improved gate pass rates for GET endpoints
- **FR-008**: Constants naming MUST follow the deterministic `path_param_to_constant()` convention: `camelCase → TEST_SCREAMING_SNAKE`

### Key Entities

- **Test Constant**: A named value in `tests/constants.py` used as a default path parameter for staging API calls (e.g., `TEST_JOB_DISPLAY_ID = 2000000`)
- **Route**: Frozen metadata object that defines an endpoint's HTTP method, path template, request/response models, and parameter schema
- **Quality Gate**: An automated check (G1-G6) that evaluates whether an endpoint's SDK implementation meets completeness and correctness standards

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Running `ab <endpoint>` shows a clean listing without route paths for all 23 endpoints
- **SC-002**: 100% of GET endpoints that previously failed gates due to missing constants now auto-resolve their path parameters
- **SC-003**: The number of GET endpoints passing all quality gates increases by at least 10 from the current baseline
- **SC-004**: Zero GET endpoint examples require manual parameter input to execute against staging
- **SC-005**: All new constants follow the `TEST_SCREAMING_SNAKE` naming convention and are sourced from staging data or educated defaults

## Assumptions

- The staging environment has sufficient test data for the known constants (e.g., job 2000000 exists and has tracking info, payments, forms, etc.)
- The swagger/OpenAPI specs in `specs/` accurately reflect the current API surface
- Endpoints that require POST bodies or authentication beyond standard OAuth2 are out of scope for this sweep (GET only)
- The `path_param_to_constant()` utility already handles the camelCase → SCREAMING_SNAKE conversion correctly
