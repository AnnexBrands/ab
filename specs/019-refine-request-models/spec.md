# Feature Specification: Refine Request Models

**Feature Branch**: `019-refine-request-models`
**Created**: 2026-02-27
**Status**: Draft
**Input**: User description: "Provide a high quality improvement to the request models. We need to accomplish several tasks for all endpoints: IDE hints for all inputs, correct resolution to path vs params, awareness of actual required vs optional fields (noting that swagger has errors, tests and /usr/src/ABConnect should be ground truth). Top tier engineering approach to make our SDK correct, DRY, and robust."

## Clarifications

### Session 2026-02-27

- Q: Should this feature create new request models for ~30 unmodeled POST/PUT endpoints, or only refine the ~65 existing models? → A: Allow incremental rollout. Refine existing models first; new models can be created incrementally. Progress tracking via `progress.html` must show which endpoints are complete vs pending. Endpoint docstrings must describe params and models. Routes/handlers must cast to request models for all updated endpoints.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - IDE-Guided Endpoint Calls (Priority: P1)

A developer using the SDK calls an endpoint method and immediately sees **every available parameter** with its type, description, and whether it is required — directly in their IDE autocomplete tooltip. They no longer need to read source code, swagger docs, or fixture files to construct a valid request.

**Why this priority**: This is the single highest-impact change for developer experience. Today, ~60% of endpoint methods accept `**kwargs: Any` or `data: dict | Any`, which means the IDE shows *nothing*. Developers must leave their editor, find the model class, read its fields, and manually construct a dict. Replacing these with explicit, typed keyword arguments turns every endpoint into a self-documenting call site.

**Independent Test**: Can be verified by opening any endpoint method in an IDE (VSCode/PyCharm) and confirming that autocomplete lists every parameter with its type and description — no documentation lookup required.

**Acceptance Scenarios**:

1. **Given** a developer calls `api.jobs.create(` in their IDE, **When** autocomplete triggers, **Then** they see named parameters (e.g., `customer`, `pickup`, `delivery`, `items`) with types and descriptions — not `**kwargs: Any`.
2. **Given** a developer passes an unknown parameter name, **When** the SDK processes the call, **Then** pydantic's `extra="forbid"` raises a clear validation error at the call site, before any HTTP request is made.
3. **Given** a developer omits a required parameter, **When** the SDK processes the call, **Then** a pydantic `ValidationError` is raised immediately with a clear message identifying the missing field.

---

### User Story 2 - Correct Required vs Optional Fields (Priority: P1)

All request model fields accurately reflect whether the API actually requires them. Developers can trust that if the SDK accepts a call without a field, the API will too — and if the SDK demands a field, the API truly needs it.

**Why this priority**: Tied with P1 because incorrect optionality is a correctness bug. Today, most request models mark everything as `Optional` regardless of whether the API actually requires the field. This lets invalid requests through to the API, producing confusing server-side 400 errors instead of clear client-side validation errors.

**Independent Test**: For each request model, the set of required fields can be compared against the ABConnect C# source (ground truth) and verified with integration test fixtures.

**Acceptance Scenarios**:

1. **Given** a request model whose API endpoint requires `companyId`, **When** the model currently marks it as `Optional`, **Then** after this feature it is marked as required and the SDK rejects calls that omit it.
2. **Given** a field that the API treats as truly optional (has a server-side default), **When** the model is updated, **Then** it remains `Optional` with a `None` default.
3. **Given** the swagger spec disagrees with the C# source code about whether a field is required, **When** determining the model's field type, **Then** the C# source code and passing test fixtures take precedence over swagger.

---

### User Story 3 - DRY Shared Patterns (Priority: P2)

Common request patterns (pagination, sorting, date ranges, search text) are defined once and reused across all models that need them, eliminating copy-paste drift and ensuring consistent behavior.

**Why this priority**: Important for long-term maintainability but not as immediately impactful as P1. Repeated field definitions across ~95 request models create maintenance burden and inconsistency risk (e.g., `page`/`page_size` defaults differ between `JobSearchRequest`, `ContactSearchRequest`, and `ListRequest`).

**Independent Test**: Can be verified by confirming that common field groups (pagination, sorting) are defined in exactly one place and that all models using those patterns inherit or compose them.

**Acceptance Scenarios**:

1. **Given** multiple request models with pagination fields (`page`, `page_size`), **When** a developer reviews the models, **Then** all pagination-enabled models share a single definition of those fields with consistent defaults and descriptions.
2. **Given** a new endpoint needs pagination, **When** a developer creates the request model, **Then** they can reuse the existing pagination pattern without redefining the fields.

---

### User Story 4 - Consistent Field Descriptions (Priority: P2)

Every field on every request model has a human-readable `description` that appears in IDE tooltips, making the SDK fully self-documenting without external references.

**Why this priority**: Enhances discoverability and reduces onboarding time, but fields already have types and names which provide partial guidance even without descriptions.

**Independent Test**: An automated check confirms that no `RequestModel` field has a `Field()` call missing the `description` parameter.

**Acceptance Scenarios**:

1. **Given** `TimelineCreateParams.create_email` currently has `Field(None, alias="createEmail")` with no description, **When** this feature is complete, **Then** it has a meaningful description explaining the parameter's purpose.
2. **Given** any request model field in the SDK, **When** a developer hovers over it in their IDE, **Then** a meaningful description appears in the tooltip.

---

### User Story 5 - Incremental Progress Tracking (Priority: P1)

The `progress.html` report shows, for every endpoint, whether its request model has been refined (correct optionality, descriptions, typed method signature). This enables incremental delivery — developers can see at a glance which endpoints are "done" and which still need work.

**Why this priority**: Without tracking, incremental rollout becomes invisible. The team cannot prioritize remaining work or verify completeness. This is a prerequisite for the incremental approach.

**Independent Test**: After refining any endpoint's request model, regenerating `progress.html` shows that endpoint's request-model status updated from incomplete to complete.

**Acceptance Scenarios**:

1. **Given** an endpoint whose request model has been fully refined (typed signature, correct optionality, descriptions), **When** the progress report is generated, **Then** that endpoint shows "complete" for request model quality.
2. **Given** an endpoint still using `**kwargs` or missing descriptions, **When** the progress report is generated, **Then** that endpoint shows "incomplete" with specific gaps identified.

---

### Edge Cases

- What happens when an endpoint accepts both a request body and query parameters (e.g., `POST /job/{jobDisplayId}/timeline` has both `request_model` and `params_model`)? Both sets of parameters must be surfaced in the method signature, clearly distinguished.
- What happens when the C# source marks a field as required but every known test fixture omits it? The field should be marked required in the model but documented with an assumption note; the fixture should be updated.
- How does the system handle fields with server-side defaults that differ from client-side defaults? Fields with server defaults should be `Optional` in the model, with the server default documented in the description.
- What happens when an endpoint has no `request_model` on its Route but the method accepts `**kwargs`? The endpoint is tracked as "incomplete" in progress.html; a new request model may be created in a future increment.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Endpoint methods MUST expose all input parameters as explicit, typed keyword arguments — eliminating `**kwargs: Any` and `data: dict | Any` patterns. Rollout is incremental: each endpoint class can be updated independently, but all updated endpoints must meet this standard.
- **FR-002**: Every field on every `RequestModel` and params model subclass MUST include a `description` parameter in its `Field()` declaration.
- **FR-003**: Required vs optional designation for each request model field MUST be validated against the ABConnect C# source code (`/usr/src/ABConnect`) as ground truth, with test fixtures as secondary evidence. Swagger is consulted but overridden when it conflicts.
- **FR-004**: Common field patterns (pagination, sorting, date range filtering, search text) MUST be defined as reusable shared definitions and composed into models that need them.
- **FR-005**: For endpoints with both path parameters and query/body parameters, the endpoint method signature MUST clearly separate path params (positional arguments) from query/body params (keyword arguments).
- **FR-006**: All existing request fixture files (`tests/fixtures/requests/*.json`) MUST continue to validate against their updated models — no fixture regressions.
- **FR-007**: Endpoint methods that accept request bodies MUST accept both the model instance directly and a plain dict, preserving backwards compatibility for existing callers.
- **FR-008**: Every endpoint method docstring MUST describe the parameters it accepts and reference the associated request/params model by name.
- **FR-009**: Every Route that has a `request_model` or `params_model` MUST have its handler cast inputs through that model (via `check()`) — no bypassing validation for modeled endpoints.
- **FR-010**: The `progress.html` report MUST track request model refinement status per endpoint, showing which endpoints have complete typed signatures, correct optionality, and descriptions vs which remain pending.

### Key Entities

- **RequestModel**: Base for outbound request bodies with strict field validation. The central entity being refined — every field gains correct optionality and a description.
- **Params Model**: RequestModel subclasses that validate query string parameters. Same base, different transport target.
- **Endpoint Method**: The method on an endpoint class that wraps a Route. The developer-facing interface — currently uses opaque `**kwargs`, needs explicit typed signatures.
- **Field Metadata**: The `description`, `alias`, default value, and required/optional designation on each model field. The unit of IDE discoverability.
- **Progress Report**: The `progress.html` artifact that tracks per-endpoint refinement status, enabling incremental delivery visibility.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All endpoint methods updated in this increment expose inputs as explicit, typed keyword arguments — zero remaining `**kwargs: Any` or untyped `data` parameters on updated endpoints. Endpoints not yet updated are tracked as incomplete in `progress.html`.
- **SC-002**: 100% of request model fields have a non-empty `description` in their `Field()` declaration, verifiable by automated check.
- **SC-003**: Required/optional field designations match the ABConnect C# source for every request model updated in this increment, with any deliberate overrides documented in code comments.
- **SC-004**: All existing tests pass without modification — no regressions in fixture validation or endpoint behavior.
- **SC-005**: Common patterns (pagination, sorting) are defined exactly once — no duplicate field definitions exist outside the shared definition.
- **SC-006**: `progress.html` accurately reflects per-endpoint request model status, distinguishing complete from incomplete endpoints.

## Assumptions

- The ABConnect C# source at `/usr/src/ABConnect` is the authoritative reference for which API fields are required vs optional.
- Test fixtures in `tests/fixtures/requests/` represent valid API payloads and can serve as secondary evidence for field requirements.
- The swagger/OpenAPI spec may contain errors (per user input) and is treated as a tertiary reference only.
- Backwards compatibility is essential — existing callers passing dicts must continue to work even after method signatures are made explicit.
- Request models that currently use `Optional[dict]` for nested objects (e.g., `customer: Optional[dict]` in `JobCreateRequest`) should retain dict typing until those nested structures have their own typed models — nested model typing is out of scope for this feature.
- Rollout is incremental: not every endpoint must be refined in a single pass. Unrefined endpoints are tracked as incomplete, not treated as failures.
