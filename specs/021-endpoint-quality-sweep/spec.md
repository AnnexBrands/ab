# Feature Specification: Endpoint Quality Sweep

**Feature Branch**: `021-endpoint-quality-sweep`
**Created**: 2026-02-28
**Status**: Draft
**Input**: User description: "Systematic endpoint quality gate sweep — fix every gate (docs, tests, examples, fixtures, IDE hints) for each endpoint one by one, ensuring docs, tests, examples, fixtures, and IDE hints for both input params and response objects meet standards."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - SDK developer fixes a single endpoint to pass all gates (Priority: P1)

A developer picks an endpoint from FIXTURES.md that shows one or more failing gates, works through a repeatable checklist to fix every quality dimension, and verifies the endpoint reaches "complete" status.

**Why this priority**: This is the core repeatable unit of work. Every subsequent improvement is an instance of this workflow. Establishing the workflow on a concrete endpoint (GET /contacts/{contactId}/editdetails with ContactDetailedInfo) validates the process.

**Independent Test**: Can be fully tested by running `python scripts/generate_progress.py --fixtures` and confirming the target endpoint shows PASS on all 6 gates, then running `pytest tests/ -x -q -m "not live"` with zero failures.

**Acceptance Scenarios**:

1. **Given** an endpoint with G1=FAIL due to undeclared model fields, **When** the developer adds all missing fields to the Pydantic model with correct types and aliases, **Then** the model validates against its fixture with zero `__pydantic_extra__` entries and G1=PASS.
2. **Given** an endpoint model with a live fixture on disk, **When** the generator evaluates G2, **Then** G2=PASS because the fixture file exists.
3. **Given** an endpoint with integration and model tests, **When** the tests include both `isinstance` type assertion and `assert_no_extra_fields` (not commented out), **Then** G3=PASS.
4. **Given** an endpoint method with a typed return annotation (not `Any`), **When** the generator evaluates G4, **Then** G4=PASS because Sphinx autodoc can extract the return type.
5. **Given** an endpoint that uses query parameters defined in swagger, **When** the Route has a `params_model` set, **Then** G5=PASS.
6. **Given** an endpoint with a request model whose fields all have `Field(description=...)` and no `# TODO: verify optionality`, **When** the generator evaluates G6, **Then** G6=PASS.
7. **Given** all 6 gates pass, **When** the generator evaluates overall status, **Then** status="complete" in FIXTURES.md.

---

### User Story 2 - Developer uses the per-endpoint checklist to ensure nothing is missed (Priority: P1)

Before marking an endpoint "done", the developer runs through a standard checklist covering all quality dimensions: model completeness, fixture accuracy, test coverage, documentation, example code, and IDE ergonomics.

**Why this priority**: Without a checklist, developers will fix the obvious gate failures but miss subtler issues (e.g., missing field descriptions, uncommented test assertions, missing docstring parameters).

**Independent Test**: Can be validated by reviewing the checklist items against the endpoint artifacts and confirming every item is satisfied.

**Acceptance Scenarios**:

1. **Given** a per-endpoint checklist exists, **When** a developer completes all items for an endpoint, **Then** all 6 quality gates pass and the endpoint has complete docs, tests, examples, and IDE hints.
2. **Given** a developer skips a checklist item, **When** they run the gate evaluator, **Then** at least one gate fails, preventing premature "complete" status.

---

### User Story 3 - Developer processes endpoints in priority order (Priority: P2)

The developer uses FIXTURES.md and progress.html to identify which endpoints to fix next, prioritizing endpoints that are closest to "complete" (fewest failing gates) and endpoints with live fixtures already captured.

**Why this priority**: Maximizes velocity by tackling low-hanging fruit first (endpoints needing only G1 model fixes vs endpoints needing fixture capture, tests, docs, and examples).

**Independent Test**: Can be validated by sorting FIXTURES.md rows by number of PASS gates and confirming the developer works top-down.

**Acceptance Scenarios**:

1. **Given** FIXTURES.md shows endpoints sorted with gate statuses, **When** a developer filters for endpoints with G2=PASS (fixture exists) and G1=FAIL (model incomplete), **Then** they find the highest-ROI targets for model completion.
2. **Given** an endpoint with no fixture (G2=FAIL), **When** the developer captures a live fixture by running the example script, **Then** both G1 and G2 become evaluable.

---

### Edge Cases

- What happens when a model field exists in the fixture but the API no longer returns it? Remove the field from the model and update the fixture.
- How do we handle endpoints with no response model (fire-and-forget POSTs, DELETEs)? G1-G4 auto-pass for scalar/void responses. G5 and G6 still apply.
- What if the fixture data is from a different API version than the current code? Re-capture the fixture from the live staging environment.
- What about endpoints that return `List[Model]`? The gate evaluator already handles list fixtures by validating the first element.
- What about paginated responses (`PaginatedList[Model]`)? The evaluator drills into `{data: [...]}` wrappers.

## Requirements *(mandatory)*

### Functional Requirements

#### Per-Endpoint Quality Checklist (the repeatable workflow)

For each endpoint to reach "complete" status, the following must all be satisfied:

**Model Completeness (G1)**
- **FR-001**: The response model MUST declare every field the API returns, with correct Python types and camelCase aliases matching the JSON keys.
- **FR-002**: The response model MUST validate against its fixture file with zero `__pydantic_extra__` entries.
- **FR-003**: New fields MUST include `Field(description="...")` with a meaningful description for IDE tooltips.
- **FR-004**: Field types MUST use `Optional[T]` or `T | None` for fields that can be null in the API response.

**Fixture Accuracy (G2)**
- **FR-005**: A live-captured fixture file MUST exist at `tests/fixtures/{ModelName}.json` representing a real API response.
- **FR-006**: Fixtures MUST NOT be fabricated — they must come from actual API calls to staging or production.

**Test Coverage (G3)**
- **FR-007**: An integration test MUST exist that calls the endpoint and asserts `isinstance(result, ModelName)`.
- **FR-008**: The integration test MUST call `assert_no_extra_fields(result)` (not commented out).
- **FR-009**: A model test MUST exist that loads the fixture, validates it against the model, and asserts zero extra fields.

**Documentation (G4)**
- **FR-010**: The endpoint method MUST have a typed return annotation (not `Any`) so Sphinx autodoc generates correct docs.
- **FR-011**: The endpoint method MUST have a docstring documenting parameters and the request model (if applicable).
- **FR-012**: The endpoint MUST appear in the API docs (`docs/api/{module}.md`) with usage examples.

**Parameter Routing (G5)**
- **FR-013**: If the endpoint accepts query parameters (per swagger spec), the Route definition MUST include `params_model="ModelName"`.
- **FR-014**: The params model MUST declare all query parameters with matching names.

**Request Quality (G6)**
- **FR-015**: The endpoint method MUST use typed signatures (not `**kwargs` or `data: Any`).
- **FR-016**: Every field in the request model and params model MUST have `Field(description="...")`.
- **FR-017**: No `# TODO: verify optionality` markers may remain in request/params model source.

**IDE Hints & Ergonomics (beyond gates)**
- **FR-018**: The endpoint method MUST have a complete type signature so IDEs can provide autocomplete for both input parameters and return types.
- **FR-019**: Request model fields MUST have aliases matching the API's expected JSON keys so IDE users get correct serialization.

#### Workflow Automation
- **FR-020**: Running `python scripts/generate_progress.py --fixtures` MUST re-evaluate all gates and produce an accurate FIXTURES.md.
- **FR-021**: Running `python scripts/generate_progress.py` MUST produce an HTML report showing per-endpoint gate status.

### Key Entities

- **Endpoint**: A single API route (path + method) implemented as a Python method on an endpoint class.
- **Response Model**: A Pydantic model (`ResponseModel` subclass with `extra="allow"`) representing the API's JSON response.
- **Request Model**: A Pydantic model (`RequestModel` subclass with `extra="forbid"`) representing the API's expected JSON body.
- **Params Model**: A Pydantic model for query parameters dispatched via Route's `params_model`.
- **Fixture**: A JSON file containing a real API response, used for offline model validation testing.
- **Quality Gate**: One of 6 automated checks (G1-G6) that determine endpoint completeness.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The immediate target endpoint (GET /contacts/{contactId}/editdetails with ContactDetailedInfo) passes all 6 quality gates after applying the checklist.
- **SC-002**: The per-endpoint checklist is documented and repeatable — any developer can apply it to any endpoint and reach "complete" status.
- **SC-003**: After completing the sweep for an endpoint, `pytest tests/ -x -q -m "not live"` passes with zero failures and zero new regressions.
- **SC-004**: The FIXTURES.md gate summary shows monotonically increasing pass counts as endpoints are swept (no regressions).
- **SC-005**: Every "complete" endpoint has all 5 artifacts present and consistent: model, fixture, test, docs, example.

## Assumptions

- The live staging API is accessible for capturing fixtures and running integration tests.
- The existing gate evaluation logic (G1-G6) in `ab/progress/gates.py` is correct and authoritative.
- The ContactDetailedInfo fixture (`tests/fixtures/ContactDetailedInfo.json`) represents a current, valid API response.
- Fields present in the fixture but absent from the model are legitimately returned by the API (not artifacts of a different API version).
- The `ContactSimple` model (which already declares most of the missing fields) provides the correct type mappings for reuse in `ContactDetailedInfo`.

## Scope

### In Scope
- Defining the per-endpoint quality checklist
- Fixing GET /contacts/{contactId}/editdetails (ContactDetailedInfo) as the first exemplar
- Updating model, tests, docs for the target endpoint
- Establishing the repeatable pattern for all subsequent endpoints

### Out of Scope
- Sweeping all 231 endpoints in this single feature (this spec establishes the workflow; the sweep is ongoing work)
- Capturing new live fixtures for endpoints that have no fixture yet (G2 failures) — that requires API access per endpoint
- Changing the gate evaluation logic itself
- Adding new endpoints or routes
