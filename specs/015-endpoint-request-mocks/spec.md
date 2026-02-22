# Feature Specification: Endpoint Request Mocks

**Feature Branch**: `015-endpoint-request-mocks`
**Created**: 2026-02-22
**Status**: Draft
**Input**: User description: "review progress, make an attempt to implement missing endpoints. where a mock is required, add a json file like AddressIsValidRequest.json, then update examples and test to load and use that file instead of having hardcoded values. if I run pytest on address it should fail saying request model validation failed, because the mock with None values for non-option fields raised an error."

## Clarifications

### Session 2026-02-22

- Q: Address model has all Optional fields — null fixture won't trigger validation error. How to resolve? → A: Update model to make all fields required. `AddressValidateParams` fields become `line1: str = Field(...)` etc. The API requires these values; the model should reflect that.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Request Mock Fixture Scaffolding (Priority: P1)

A developer maintaining the SDK needs request mock fixtures for all endpoints that accept input parameters or request bodies. Currently, test and example data is hardcoded inline. By generating JSON fixture files (one per request/params model) with `null` values for all fields, the developer creates a visible inventory of what request data is needed. Running tests against these null-populated mocks immediately reveals which fields are required (non-optional) because model validation raises errors — turning the fixture set into a living checklist of work remaining.

**Why this priority**: This is the foundation. Without the fixture files on disk, there is nothing for examples or tests to load, and no mechanism to surface incomplete request data via validation failures.

**Independent Test**: After generating fixtures, running `pytest tests/integration/test_address.py` should fail with a request model validation error because the address request fixture contains `null` for fields that the API requires. The fixture file itself must exist on disk in `tests/fixtures/requests/`.

**Acceptance Scenarios**:

1. **Given** an endpoint has a defined `params_model` or `request_model` on its Route, **When** mock fixtures are generated, **Then** a JSON file named after the model class is created in `tests/fixtures/requests/` with all fields set to `null`.
2. **Given** a request fixture already exists with real data (e.g., `CompanySearchRequest.json`), **When** mock generation runs, **Then** the existing fixture is preserved and not overwritten.
3. **Given** a model has non-optional fields (no `Optional` wrapper, no default), **When** the fixture is loaded and parsed by the model, **Then** pydantic validation raises an error identifying the required fields.

---

### User Story 2 - Examples Load Request Data from Fixtures (Priority: P2)

A developer working on examples wants to stop hardcoding request parameters inline. Instead, example runners load parameter values from the corresponding request fixture JSON file. This centralizes test data, makes it easier to update, and ensures examples and tests share the same inputs.

**Why this priority**: Examples are the primary way developers learn the SDK. Moving from hardcoded values to fixture-loaded values makes them maintainable and consistent with the test infrastructure.

**Independent Test**: Running `python -m examples address` loads parameters from the request fixture file instead of using hardcoded `line1="12742 E Caley Av"` values.

**Acceptance Scenarios**:

1. **Given** an example entry has a corresponding request fixture file, **When** the example is executed, **Then** parameters are loaded from the fixture file rather than hardcoded inline.
2. **Given** an example entry has no request fixture file, **When** the example is executed, **Then** it falls back to its existing inline parameters (backward compatibility).
3. **Given** a request fixture contains `null` values for required fields, **When** the example tries to use it, **Then** validation fails with a clear error identifying the null required fields.

---

### User Story 3 - Tests Use Fixture-Loaded Request Data (Priority: P2)

A developer running integration tests wants test request data loaded from the same fixture files used by examples. When a request fixture has `null` for required fields, the test fails with a validation error — making it obvious which fixtures need real data filled in.

**Why this priority**: Tests and examples sharing the same fixture data prevents drift. Validation failures on null-populated mocks create a clear TODO list for the developer.

**Independent Test**: Running `pytest tests/integration/test_address.py` fails with a pydantic `ValidationError` because the address request fixture has `null` values for non-optional fields. After filling in real values, the test passes.

**Acceptance Scenarios**:

1. **Given** an integration test has a corresponding request fixture, **When** the test runs, **Then** it loads request parameters from the fixture file.
2. **Given** a request fixture has `null` for required (non-optional) fields, **When** the test runs, **Then** it fails with a model validation error identifying the null fields.
3. **Given** a request fixture has been populated with valid values, **When** the test runs, **Then** it uses those values to call the API and validates the response.

---

### User Story 4 - Progress Review and Fixture Tracking (Priority: P3)

A project maintainer wants the fixture tracking documentation and progress report updated to reflect the new request mock fixtures. The progress report should show which endpoints now have request fixtures (even if null-populated) and which still lack them.

**Why this priority**: Visibility into fixture coverage drives prioritization of which endpoints to fill in next.

**Independent Test**: After generating request fixtures, `docs/FIXTURES.md` includes entries for every new request fixture file, and the progress report regenerates without errors.

**Acceptance Scenarios**:

1. **Given** new request fixtures are added, **When** fixture tracking is regenerated, **Then** documentation lists each request fixture with its status.
2. **Given** the progress report is regenerated, **When** reviewed, **Then** it reflects the updated fixture counts.

---

### Edge Cases

- What happens when a model inherits fields from a base class? All fields (including inherited) must appear in the fixture JSON with `null` values.
- What happens when a model has nested objects (e.g., a field typed as another model)? The nested value should be `null` in the initial mock — validation will surface whether the nesting is required.
- What happens when a Route has both `params_model` (query params) and `request_model` (body)? Both models get separate fixture files.
- What happens when multiple endpoints share the same request model? Only one fixture file is created (keyed by model class name), shared across endpoints.
- What happens when a fixture has all Optional fields? It loads successfully with all `null` values — no validation error. This indicates the endpoint can be called without parameters.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST generate one JSON fixture file per unique `params_model` and `request_model` referenced by any Route definition, placed in `tests/fixtures/requests/`.
- **FR-002**: Generated fixture files MUST be named `{ModelClassName}.json` matching the exact class name of the request/params model.
- **FR-003**: Generated fixture files MUST contain all model fields set to `null`, producing a valid JSON object whose keys match the model's serialized field aliases.
- **FR-004**: System MUST NOT overwrite existing fixture files that already contain non-null data.
- **FR-005**: Examples MUST be updated to load request parameters from fixture files when available, falling back to existing inline values when no fixture exists.
- **FR-006**: Integration tests MUST be updated to load request parameters from fixture files when available.
- **FR-007**: When a null-populated fixture is loaded and used to construct a request model with non-optional required fields, pydantic validation MUST raise an error.
- **FR-008**: Fixture tracking documentation MUST be updated to reflect the new request fixture files.

### Key Entities

- **Request Fixture**: A JSON file representing the input parameters or body for an API endpoint call. Named after the model class. Contains field values (initially `null`) that can be populated with real data over time.
- **Params Model**: A pydantic model defining query string parameters for GET endpoints (e.g., `AddressValidateParams`).
- **Request Model**: A pydantic model defining the JSON body for POST/PUT endpoints (e.g., `CompanySearchRequest`).
- **Route**: An SDK metadata object linking an HTTP method + path to its request and response models.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every endpoint Route with a `params_model` or `request_model` has a corresponding JSON file in `tests/fixtures/requests/`.
- **SC-002**: Running `pytest tests/integration/test_address.py` fails with a validation error referencing null required fields (demonstrating the fail-first pattern works).
- **SC-003**: Existing tests that were passing before this change continue to pass (zero regressions), except where tests are intentionally updated to load from fixtures.
- **SC-004**: No example or test contains hardcoded request parameter values that duplicate data available in a fixture file.
- **SC-005**: Fixture tracking documentation accurately reflects all fixture files on disk, including the new request fixtures.

## Assumptions

- Request fixture files use the model's serialized field aliases (camelCase per ABConnect API convention) as JSON keys, not the Python field names (snake_case).
- The null-populated mocks are intentionally invalid for models with required fields — this is a feature, not a bug. It creates a visible backlog of fixtures needing real data.
- "Missing endpoints" in this context means endpoints whose Routes define request/params models but lack corresponding request fixture files — not endpoints missing Route definitions entirely.
- The address endpoint is the reference case for validating the pattern. Its `AddressValidateParams` model has all fields marked as required (non-optional), so a null-populated fixture triggers a pydantic validation error. Where other models have incorrectly Optional fields for API-required parameters, those models should also be tightened as part of this feature.
- Existing response fixtures (`tests/fixtures/*.json`) are unaffected by this change.
