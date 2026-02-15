# Feature Specification: Request Model Methodology

**Feature Branch**: `007-request-model-methodology`
**Created**: 2026-02-14
**Status**: Draft
**Input**: User description: "update methodology to track fixtures for request model and request params model using pydantic. we need to track this in progress, fixtures, api-surface, etc. follow the existing methodology of check ABConnectTools and swagger. Ensure the endpoints are clean, rather than passing each func param to a dict of params. pass kwargs to the request model_validate"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Clean Endpoint Signatures with Request Models (Priority: P1)

As an SDK developer implementing new endpoints, I want endpoint methods to accept keyword arguments that are validated through a Pydantic request model, so that callers get IDE autocomplete, type safety, and clean method signatures instead of constructing raw dicts.

**Why this priority**: This is the core methodology change. Every future endpoint implementation depends on this pattern being defined. Without it, endpoints continue accepting `dict | Any` with no validation at the call site.

**Independent Test**: Can be verified by converting a single existing endpoint (e.g., `companies.search`) to the new pattern and confirming: (a) keyword arguments are accepted, (b) a Pydantic request model validates them, (c) the HTTP call receives the correct serialized payload.

**Acceptance Scenarios**:

1. **Given** an endpoint method using the new pattern, **When** a caller passes keyword arguments matching the request model fields, **Then** the arguments are validated through the Pydantic model and the request succeeds.
2. **Given** an endpoint method using the new pattern, **When** a caller passes an invalid or unknown keyword argument, **Then** a validation error is raised before the HTTP call is made.
3. **Given** an endpoint method using the new pattern, **When** a caller uses an IDE, **Then** autocomplete shows available parameters with types and descriptions.

---

### User Story 2 - Request Fixture Tracking (Priority: P1)

As an SDK maintainer, I want request body fixtures and request params fixtures tracked alongside response fixtures in FIXTURES.md and related tracking documents, so that every endpoint has documented, validated example inputs — not just outputs.

**Why this priority**: Without tracked request fixtures, endpoint examples use empty dicts `{}` that fail validation. Request fixtures are essential for testing, documentation, and the example runner.

**Independent Test**: Can be verified by adding request fixture entries to FIXTURES.md for a handful of endpoints and confirming the tracking format captures: model name, source (swagger/ABConnectTools/staging), fixture file path, and validation status.

**Acceptance Scenarios**:

1. **Given** a new request fixture is captured, **When** it is added to FIXTURES.md, **Then** it appears in a dedicated request fixtures section with model name, source, and status.
2. **Given** an endpoint has both a request model and a response model, **When** reviewing FIXTURES.md, **Then** both request and response fixture statuses are visible for that endpoint.
3. **Given** a request fixture is tracked, **When** the fixture file is loaded in tests, **Then** it validates successfully against the corresponding Pydantic request model.

---

### User Story 3 - Updated Progress and API Surface Tracking (Priority: P2)

As a project stakeholder reviewing coverage, I want progress reports and API surface documents to reflect request model completeness alongside response model completeness, so that I can see the full implementation status of each endpoint.

**Why this priority**: Tracking only response models gives an incomplete picture. An endpoint is not truly "complete" until its request model, request fixtures, response model, and response fixtures are all in place.

**Independent Test**: Can be verified by updating the progress report generator and API surface tracking to include request model columns, then generating a report that shows per-endpoint completeness across all four dimensions.

**Acceptance Scenarios**:

1. **Given** the progress tracking system, **When** an endpoint has a request model and fixture, **Then** the progress report shows both request and response status.
2. **Given** an endpoint with a response model but no request model, **When** viewing the API surface document, **Then** the endpoint is marked as partially complete with the request model listed as missing.

---

### User Story 4 - Methodology Documentation for Future Endpoint Work (Priority: P2)

As a developer implementing endpoints in feature 002 and beyond, I want a documented methodology that prescribes the steps for implementing an endpoint — including request model creation, fixture capture, and the kwargs-to-model pattern — so that every endpoint follows a consistent, high-quality pattern.

**Why this priority**: The methodology must be codified so that future endpoint implementation (the bulk of remaining work) follows the new pattern consistently.

**Independent Test**: Can be verified by following the documented methodology to implement a new endpoint from scratch, confirming every step is clear and produces the expected artifacts.

**Acceptance Scenarios**:

1. **Given** the updated methodology documentation, **When** a developer follows it for a new endpoint, **Then** the result includes: a request model, a request fixture, validated example params, and a clean endpoint signature.
2. **Given** the DISCOVER workflow, **When** its phases are reviewed, **Then** each phase includes request model and request fixture steps alongside the existing response model and fixture steps.

---

### Edge Cases

- What happens when an endpoint has no request body (GET with only path/query params)? The methodology must distinguish between body request models and query/path params models.
- What happens when the swagger spec defines a request body but ABConnectTools has no corresponding example? The methodology should prescribe deriving minimal valid request fixtures from the swagger schema alone.
- How does the pattern handle endpoints that accept both a request body and query parameters simultaneously? Both must be modeled and tracked separately.
- What happens when a request model field is optional and the fixture omits it? The fixture should still validate, and tests should cover both minimal and full payloads.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The SDK MUST define a standard endpoint method signature pattern where keyword arguments are validated through a Pydantic request model via `model_validate(kwargs)`.
- **FR-002**: Every endpoint with a request body MUST have a corresponding Pydantic `RequestModel` subclass with typed fields, aliases, and descriptions derived from the swagger spec.
- **FR-003**: Every endpoint with query or path parameters beyond simple IDs MUST have a corresponding Pydantic params model for validation.
- **FR-004**: FIXTURES.md MUST include a request fixtures section that tracks: endpoint path, HTTP method, request model name, fixture file path, source (swagger/ABConnectTools/staging), and capture status.
- **FR-005**: The progress tracking system MUST report per-endpoint completeness across four dimensions: request model, request fixture, response model, response fixture.
- **FR-006**: The API surface tracking MUST include request model presence and fixture status for each endpoint.
- **FR-007**: The DISCOVER workflow MUST be updated to include request model creation and request fixture capture as explicit steps in the endpoint implementation phases.
- **FR-008**: The endpoint method pattern MUST NOT require callers to manually construct dicts — callers pass keyword arguments directly.
- **FR-009**: Request fixture files MUST validate against their corresponding Pydantic request model in automated tests.
- **FR-010**: The methodology MUST prescribe checking both the swagger spec and ABConnectTools reference implementation when deriving request model field names, types, and aliases.

### Key Entities

- **Request Model**: A Pydantic model representing the body payload for a POST/PUT/PATCH endpoint. Has typed fields with camelCase aliases matching the API contract. Extends the existing `RequestModel` base class.
- **Params Model**: A Pydantic model representing query string or complex path parameters for an endpoint. Distinct from body request models. Used for endpoints with structured query parameters.
- **Request Fixture**: A JSON file containing a valid example request payload for an endpoint. Stored alongside response fixtures. Must validate against the corresponding request model.
- **Endpoint Completeness**: The four-dimensional status of an endpoint: (1) request model defined, (2) request fixture captured, (3) response model defined, (4) response fixture captured.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of newly implemented endpoints (from this feature onward) follow the kwargs-to-model pattern with no raw dict parameters in their public signatures.
- **SC-002**: FIXTURES.md tracks request fixtures for every endpoint that has a request body, with zero endpoints showing "unknown" or "untracked" request fixture status.
- **SC-003**: The progress report shows per-endpoint completeness across all four dimensions (request model, request fixture, response model, response fixture) for every implemented endpoint.
- **SC-004**: All tracked request fixtures validate successfully against their corresponding Pydantic request model in the test suite with zero validation failures.
- **SC-005**: A developer following the updated methodology documentation can implement a new endpoint — including request model, request fixture, and clean signature — without referencing any external instructions.

## Assumptions

- The existing `RequestModel` base class (with `extra="forbid"`, `populate_by_name=True`, camelCase aliasing) is sufficient for the new pattern and does not need fundamental changes.
- Path parameters that are simple scalar IDs (e.g., `company_id: str`) do not need a Pydantic params model — only complex or multi-field query parameters warrant one.
- The `model_validate(kwargs)` pattern will use `model_validate()` from Pydantic v2, which is already a project dependency.
- Existing response fixtures and response model tracking continue unchanged; this feature adds request-side tracking alongside them.
- The methodology updates apply to all future endpoint work (feature 002 and beyond) but do not require retroactively converting all 59 existing endpoints — only that newly touched endpoints adopt the new pattern.
