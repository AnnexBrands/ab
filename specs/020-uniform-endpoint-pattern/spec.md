# Feature Specification: Uniform Endpoint Pattern

**Feature Branch**: `020-uniform-endpoint-pattern`
**Created**: 2026-02-28
**Status**: Draft
**Input**: User description: "Standardize all body-accepting SDK endpoint methods on a uniform data: ModelType | dict pattern, eliminating duplicated field definitions and untyped dict passthrough. Fix broken example calling conventions and restore incorrectly demoted required fields."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - One Calling Convention for All Body-Accepting Endpoints (Priority: P1)

A developer using the SDK encounters the same calling pattern for every endpoint that sends a JSON body: `api.<service>.<method>(path_params, data=ModelOrDict)`. They never need to guess whether an endpoint takes inline keyword arguments, a `data: dict | None`, or a `data: Model | dict` — it is always `data: ModelType | dict` for POST/PUT/PATCH methods. IDE autocomplete on the model constructor shows all available fields with types and descriptions.

**Why this priority**: The current codebase has three competing patterns for the same problem (inline kwargs→dict, `data: Model|dict`, `data: dict|None`). Developers must learn which convention each method uses. Unifying on one pattern is the primary goal of this feature.

**Independent Test**: Pick any 5 body-accepting endpoint methods across different services. All 5 must accept a `data: ModelType | dict` keyword argument. No method should accept `**kwargs`, inline body kwargs with a manual `dict()` call, or `data: dict | None`.

**Acceptance Scenarios**:

1. **Given** a developer calls `api.jobs.create_note(job_display_id, data=JobNoteCreateRequest(comments="hi"))`, **When** the call executes, **Then** the request body is validated by the model and sent as camelCase JSON.
2. **Given** a developer calls `api.jobs.create_note(job_display_id, data={"comments": "hi"})`, **When** the call executes, **Then** the dict is validated through `JobNoteCreateRequest.check()` and sent identically.
3. **Given** a developer searches for `body = dict(` in the endpoint source files, **When** they review the results, **Then** zero hits are returned — no endpoint method manually constructs a body dict from inline kwargs.
4. **Given** a developer searches for `data: dict | None` in the endpoint source files, **When** they review the results, **Then** zero hits are returned — no untyped passthrough exists.

---

### User Story 2 - GET Endpoints Keep Explicit Query Parameters (Priority: P1)

A developer calling a GET endpoint sees explicit keyword arguments for query parameters directly on the method signature: `api.jobs.get_notes(job_display_id, category="shipping")`. GET methods never use `data:` — their parameters are few, belong on the URL, and benefit from direct IDE visibility in the method signature.

**Why this priority**: Tied with P1 because it clarifies the boundary between the two calling conventions. Without this rule, developers would be confused about when to use `data:` vs kwargs.

**Independent Test**: Pick any 5 GET endpoint methods with query parameters. All 5 must expose query params as explicit keyword arguments, not through a `data:` parameter.

**Acceptance Scenarios**:

1. **Given** a developer calls `api.jobs.get_notes(job_display_id, category="shipping")`, **When** the IDE shows autocomplete, **Then** the developer sees `category` and `task_code` as explicit keyword arguments with types.
2. **Given** a GET endpoint has no query parameters, **When** a developer views the method signature, **Then** only path parameters appear — no `data:` argument.

---

### User Story 3 - Examples Work Without Runtime Errors (Priority: P1)

A developer runs any example file and all examples execute without `TypeError` from incorrect argument passing. Currently, many example lambdas pass `data or {}` positionally to methods that require keyword-only arguments, causing immediate crashes.

**Why this priority**: Broken examples prevent onboarding and validation. This is a regression from PR #19 that must be fixed.

**Independent Test**: Run example files for jobs, reports, and companies — all complete without `TypeError`.

**Acceptance Scenarios**:

1. **Given** an example lambda calls a body-accepting method, **When** it executes, **Then** it passes the data using `data=data or {}` keyword syntax.
2. **Given** an example lambda previously used `**(data or {})` kwargs unpacking for inline kwargs, **When** the method now uses `data: Model | dict`, **Then** the lambda is updated to `data=data or {}`.

---

### User Story 4 - Required Fields Reject Invalid Requests (Priority: P2)

A developer who omits a field that the API server actually requires gets a clear client-side validation error, not a cryptic server-side 500 error. Fields that were incorrectly demoted from required to optional in PR #19 are restored where the server-side code uses them without null checks.

**Why this priority**: Correctness matters but is secondary to pattern consistency. The demotion only affects 5 fields, and incorrect requests would still fail (just on the server instead of the client).

**Independent Test**: For each restored required field, construct a request model instance omitting that field — a validation error is raised immediately.

**Acceptance Scenarios**:

1. **Given** a request model has a required field (e.g., `task_code` on `TimelineTaskCreateRequest`), **When** a developer constructs the model without that field, **Then** a validation error is raised immediately.
2. **Given** a field is truly optional per the server's controller source code, **When** the model is reviewed, **Then** it remains optional with a default value.

---

### Edge Cases

- What happens when a developer passes `None` to `data:`? The Route's `request_model` triggers validation. A `None` value should either be rejected at the method level or result in no body being sent — behavior must match the endpoint's HTTP semantics.
- What happens when a developer passes a dict with camelCase keys (e.g., `{"taskCode": "PKG"}`) to `data:`? The model accepts both camelCase and snake_case keys. This must continue working.
- What happens when a Pattern C endpoint has no documented request body schema? A minimal placeholder model is created, preserving the ability to pass any dict while adding the typed `data:` interface.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: All POST, PUT, and PATCH endpoint methods that send a JSON body MUST accept a `data: ModelType | dict` keyword argument, where `ModelType` is the specific request model subclass for that endpoint.
- **FR-002**: No endpoint method MUST use inline keyword arguments that duplicate request model field definitions (eliminates Pattern A).
- **FR-003**: No endpoint method MUST use `data: dict | None` as a parameter type (eliminates Pattern C).
- **FR-004**: All GET endpoint methods with query parameters MUST expose those parameters as explicit keyword arguments on the method signature, not through a `data:` parameter.
- **FR-005**: All example lambdas MUST pass data using `data=` keyword syntax, not positional passing or `**` unpacking.
- **FR-006**: Request model fields that the API server uses without null checks in its controller code MUST be marked as required (not optional). The 5 demoted fields from PR #19 MUST be audited and restored where appropriate.
- **FR-007**: All existing request model field descriptions, keyword-only separators, and docstrings MUST be preserved.
- **FR-008**: The G6 quality gate, description enforcement test, and request mixins MUST remain functional and passing.
- **FR-009**: Methods with both a JSON body and query parameters MUST accept the body via `data:` and keep query parameters as explicit keyword arguments.
- **FR-010**: Route definitions for Pattern C endpoints that lack a `request_model` MUST be updated to include the newly created model.

### Key Entities

- **Endpoint Method**: A method on an endpoint class that maps to one API route. Has a method signature, docstring, and dispatches via the base request handler.
- **Request Model**: A validated model with strict field checking, field descriptions, and camelCase aliases. Validated automatically during request dispatch.
- **Route**: An immutable definition linking an HTTP method + path to optional request, params, and response models.
- **Example Lambda**: A callable in the examples directory that exercises an endpoint method, used for fixture capture and validation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Zero endpoint methods use Pattern A (inline kwargs→dict construction). Verified by searching for `body = dict(` in endpoint source files and finding 0 hits.
- **SC-002**: Zero endpoint methods use Pattern C (`data: dict | None`). Verified by searching for `data: dict | None` in endpoint source files and finding 0 hits.
- **SC-003**: All existing tests pass with no regressions.
- **SC-004**: Zero example files crash with argument-passing errors when invoked.
- **SC-005**: All 5 demoted required fields are audited and either restored or explicitly documented as correctly optional with server-side evidence.
- **SC-006**: The G6 quality gate reports the same or higher pass rate after changes.
