# Feature Specification: Scaffold Examples & Fixtures

**Feature Branch**: `004-scaffold-examples-fixtures`
**Created**: 2026-02-14
**Status**: Draft
**Input**: User description: "Review progress, surface area, etc. Ensure all examples and fixtures are scaffolded and commented with TODO. All examples should be wrapped in a runner and include request params, request body model, response body model, and response fixture file path. When I add the missing request body and run examples.address.isvalid, the example should cast to the model, then to json, then call save fixture for the response body."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Run an Example to Capture a Fixture (Priority: P1)

A developer working on fixture capture opens `examples/address.py`. They see a structured example for `address.validate` that includes the expected request parameters, the response model name, and the fixture file path — but the request parameters are marked with `# TODO: provide valid street, city, state, zipCode`. The developer fills in real parameter values, runs the example (e.g., `python -m examples.address`), and the runner automatically makes the API call, casts the response to the declared response model, serializes it to JSON, and saves it to the declared fixture file path. The developer then commits the new fixture file.

**Why this priority**: This is the core value proposition — examples become the fixture-capture mechanism, closing the loop between "needs request data" in FIXTURES.md and actually capturing that data.

**Independent Test**: Can be tested by running any example whose request data is complete and verifying that the fixture file is created at the declared path with valid JSON matching the response model schema.

**Acceptance Scenarios**:

1. **Given** an example with complete request parameters, **When** the developer runs it, **Then** the runner calls the API, casts the response to the declared response model, serializes to JSON, and saves to the declared fixture file path.
2. **Given** an example with incomplete request parameters (TODO markers), **When** the developer runs it, **Then** the runner reports which parameters are still needed and does not overwrite any existing fixture file.
3. **Given** an example that runs successfully, **When** the fixture file is saved, **Then** the JSON uses camelCase keys (as returned by the API) and the file is named after the response model class.

---

### User Story 2 - Discover All SDK Methods via Structured Examples (Priority: P2)

A developer exploring the SDK opens any example file and sees every public method of that endpoint module represented as a structured entry. Each entry declares: the method call with request parameters, the request body model (if any), the response body model, and the fixture file path. Methods with captured fixtures are clearly distinguished from those still needing data. The developer can scan the file to understand the full surface area of that endpoint.

**Why this priority**: Structured examples serve as both documentation and an executable surface-area inventory. Every public method is visible, not just the ones a previous developer thought to include.

**Independent Test**: Can be tested by comparing the set of structured entries in each example file against the public methods of the corresponding endpoint class. Every public method should appear exactly once.

**Acceptance Scenarios**:

1. **Given** any endpoint module with N public methods, **When** the developer opens its example file, **Then** all N methods are represented as structured entries with their request/response metadata.
2. **Given** a method that requires a request body, **When** the developer views its entry, **Then** the request body model name is declared and the body contents are either populated (for captured fixtures) or stubbed with `# TODO` comments.
3. **Given** a method with no request body (query-parameter-only), **When** the developer views its entry, **Then** the request parameters are explicitly listed as keyword arguments.

---

### User Story 3 - Create Missing Example Files for All Endpoint Modules (Priority: P3)

A developer checks the `examples/` directory and finds that every endpoint module has a corresponding example file — including `address`, `lookup`, and `users`, which were previously missing. Each new file follows the same runner-wrapped, structured-entry pattern as all other examples.

**Why this priority**: 100% coverage of endpoint modules with structured examples eliminates blind spots and ensures the fixture-capture workflow is available for every part of the API.

**Independent Test**: Can be tested by listing endpoint modules and verifying a 1:1 mapping to example files.

**Acceptance Scenarios**:

1. **Given** a developer lists files in `examples/`, **When** they compare against endpoint modules, **Then** every endpoint module has a corresponding example file.
2. **Given** any newly created example file, **When** the developer opens it, **Then** it follows the same runner-wrapped, structured-entry pattern as existing examples.

---

### Edge Cases

- A response from the API does not match the declared response model schema — the runner should report the validation error clearly rather than saving invalid data.
- A fixture file already exists at the declared path — the runner should overwrite it (fixtures are re-capturable from live data).
- An endpoint method returns a list of models rather than a single model — the runner should handle both cases and save the full list.
- An endpoint method returns no content (HTTP 204) — the runner should handle this gracefully and not attempt to save an empty fixture.
- A method is defined on the endpoint class but is internal (underscore-prefixed) — it should not appear in the example file.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Every endpoint module in `ab/api/endpoints/` that contains public methods MUST have a corresponding example file in `examples/`.
- **FR-002**: Each example file MUST be executable via the runner pattern (e.g., `python -m examples.address`).
- **FR-003**: Each public endpoint method MUST be represented as a structured entry in its example file, declaring: the method call with request parameters, request body model (if applicable), response body model, and fixture file path.
- **FR-004**: When an example entry is executed with complete request data, the runner MUST: call the API, cast the response to the declared response model, serialize to JSON (camelCase keys), and save to the declared fixture file path.
- **FR-005**: Example entries whose request data is incomplete MUST be annotated with `# TODO` comments specifying what parameters or body fields are needed, referencing FIXTURES.md where applicable.
- **FR-006**: Example entries whose fixtures are already captured MUST have their request data populated with the parameters that produced the captured fixture.
- **FR-007**: All example files MUST follow a consistent structural pattern: runner wrapper, grouped method entries, metadata declarations per entry.
- **FR-008**: The runner MUST provide a fixture-save capability that writes response data to the fixture directory in the standard naming convention (`{ModelClassName}.json`).
- **FR-009**: Existing example files (16 files) MUST be migrated to the new runner-wrapped, structured-entry pattern.
- **FR-010**: The `examples/jobs.py` file MUST be expanded from its current 2 methods to cover all public methods of the jobs endpoint module.
- **FR-011**: The `examples/lots.py` file MUST be expanded from its current truncated state to cover all public methods of the lots endpoint module.

### Key Entities

- **Example File**: An executable script in `examples/` that demonstrates and captures fixtures for one endpoint module. Wraps all method entries in a runner.
- **Structured Entry**: A single method demonstration within an example file, declaring: method call, request parameters/body, request model name, response model name, and fixture file path.
- **Runner**: The execution wrapper that handles API calls, model casting, JSON serialization, and fixture saving for each structured entry.
- **Fixture**: A JSON file in `tests/fixtures/` named `{ModelClassName}.json`, containing a real API response captured via the runner.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of endpoint modules with public methods have a corresponding example file (currently 80%, target 100% — 3 missing files created).
- **SC-002**: 100% of public endpoint methods appear as structured entries in their respective example files (currently incomplete for jobs, lots, and others).
- **SC-003**: Every structured entry for a fixture-pending endpoint carries a `# TODO` comment with specific guidance on what data is needed.
- **SC-004**: Running any example with complete request data produces a valid fixture file at the declared path without manual intervention beyond providing credentials.
- **SC-005**: All 16 existing example files are migrated to the runner-wrapped pattern with no loss of demonstrated functionality.

## Assumptions

- The set of endpoint modules is the 15 files currently in `ab/api/endpoints/`. New modules added in future features are out of scope.
- "Public methods" means methods defined on the endpoint class that are not prefixed with underscore.
- The fixture naming convention is `{ModelClassName}.json` (matching the response model class name), consistent with the existing 22 captured fixtures.
- The runner requires valid API credentials (staging environment) to execute — this is an existing prerequisite, not a new one.
- FIXTURES.md remains the tracking document for fixture status; the runner does not automatically update FIXTURES.md.
- Fixture files use camelCase keys as returned by the API, consistent with existing captured fixtures.
- Overwriting an existing fixture file is acceptable — fixtures represent the latest API response shape and are re-capturable.
