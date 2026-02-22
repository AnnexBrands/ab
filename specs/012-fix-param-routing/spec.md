# Feature Specification: Fix Parameter Routing

**Feature Branch**: `012-fix-param-routing`
**Created**: 2026-02-21
**Status**: Draft
**Input**: User description: "api.address.validate() fails because the handler expects values like query parameters (e.g., `Line1` in query). Reconsider all gates and progress HTML. Clarify whether we need to provide request path (params) or query (json), and ensure we always pass to the request handler in the way it expects. Design a clean, DRY, elegant approach. Should we pass all incoming to pydantic model check, and will it know how to separate path from query?"

## Clarifications

### Session 2026-02-21

- Q: Should endpoint methods use `**kwargs` (DRY, loses IDE autocomplete) or typed signatures + params_model validation? → A: Typed signatures + params_model. Methods keep explicit named parameters for IDE autocomplete; the Route's params_model validates at the `_request()` dispatch layer.
- Q: Should G5 (Parameter Routing) be required for overall "complete" status? → A: G5 required only for endpoints that have query or body params. Endpoints with no params (path-only or parameterless) auto-pass G5 and their overall_status is unaffected.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - SDK Callers Get Correct Parameter Routing (Priority: P1)

As an SDK user calling any endpoint method, I want my arguments to arrive at the API server in the correct HTTP transport mechanism (URL path segment, URL query string, or JSON request body) without me needing to know or care about the distinction, so that every API call succeeds on the first attempt.

**Why this priority**: This is the root-cause fix. When parameters are routed to the wrong transport (e.g., query params sent as body JSON, or path params not substituted), the API server rejects the request. Nothing else matters if calls fail.

**Independent Test**: Can be verified by calling `api.address.validate(line1="123 Main St", city="Columbus", state="OH", zip="43213")` and confirming the HTTP request sends `Line1`, `City`, `State`, `Zip` as URL query string parameters (not in the JSON body), and the API returns a valid response.

**Acceptance Scenarios**:

1. **Given** an endpoint whose OpenAPI spec defines parameters as `"in": "query"`, **When** an SDK user calls the method with those arguments, **Then** the arguments are sent as URL query string parameters.
2. **Given** an endpoint whose OpenAPI spec defines parameters as `"in": "path"`, **When** an SDK user calls the method with those arguments, **Then** the arguments are substituted into the URL path.
3. **Given** an endpoint with a `requestBody` in its OpenAPI spec, **When** an SDK user calls the method with body data, **Then** the data is sent as a JSON request body.
4. **Given** an endpoint that combines path parameters with query parameters (e.g., `GET /companies/{companyId}/search?term=...`), **When** the SDK user provides all arguments, **Then** path params are substituted and query params are sent in the query string — without the caller specifying which is which.

---

### User Story 2 - Single Unified Pattern for All Endpoint Methods (Priority: P1)

As an SDK developer implementing new endpoints, I want a single, consistent pattern that automatically routes caller arguments to the correct HTTP transport based on the Route definition, so that I do not manually build parameter dicts in every endpoint method and cannot accidentally route params to the wrong transport.

**Why this priority**: The current codebase has multiple ad-hoc patterns: some endpoints manually build `params` dicts, some pass `**kwargs` as `json=`, some use `Route.bind()` for path params. This inconsistency is the source of routing bugs and makes the SDK hard to maintain.

**Independent Test**: Can be verified by implementing a new endpoint using the unified pattern and confirming: (a) the endpoint method has a clean signature, (b) path params are auto-detected and bound, (c) query params are auto-detected and sent in the query string, (d) body params are auto-detected and sent as JSON — all without per-method dict construction.

**Acceptance Scenarios**:

1. **Given** a Route with path template parameters and a params_model, **When** an SDK developer writes an endpoint method, **Then** the method does not contain manual dict construction for query params.
2. **Given** a Pydantic model that declares fields for an endpoint's parameters, **When** the base request handler receives those fields, **Then** it separates path params from query params from body params based on metadata available in the Route definition.
3. **Given** two endpoints — one with query params and one with body params — **When** both use the same unified dispatch pattern, **Then** each routes params correctly without endpoint-specific routing logic.

---

### User Story 3 - Quality Gates and Progress Report Reflect Parameter Correctness (Priority: P2)

As a project stakeholder reviewing SDK completion status, I want quality gates and the progress HTML report to account for whether endpoints correctly define and route their parameters (not just response models), so that I can see which endpoints are fully correct versus which have parameter routing gaps.

**Why this priority**: Current quality gates (G1-G4) focus exclusively on response models and fixtures. An endpoint can pass all four gates but still fail at runtime because its parameters are incorrectly routed. Including parameter correctness in the quality assessment gives an accurate picture of true endpoint readiness.

**Independent Test**: Can be verified by generating the progress report and confirming that it shows, per endpoint: (a) whether path/query/body param routing is defined, (b) whether a params_model exists for endpoints with query parameters, (c) overall readiness that factors in parameter correctness.

**Acceptance Scenarios**:

1. **Given** an endpoint with query parameters that lacks a params_model, **When** the quality assessment runs, **Then** the endpoint is flagged as incomplete with a specific note about missing parameter definition.
2. **Given** the progress HTML report, **When** a stakeholder views it, **Then** each endpoint row shows parameter routing status alongside existing gate statuses.
3. **Given** all endpoints have been updated, **When** the progress report is generated, **Then** the count of endpoints with correct parameter routing is visible in the summary.

---

### Edge Cases

- What happens when an endpoint has zero parameters (no path, no query, no body)? The routing mechanism must handle this gracefully with no validation step.
- What happens when a query parameter value is `None` or empty string? `None` values must be excluded from the query string; empty strings should be included only if the API expects them.
- What happens when a caller passes an argument name that matches neither a path param, query param, nor body field? The system must raise a clear validation error before sending the HTTP request.
- What happens when the same parameter name exists in both path and query for an endpoint? Path params take precedence (they are structurally embedded in the URL template), and the SDK must not send the same value in both locations.
- What happens for endpoints with pagination query params (`pageNumber`, `pageSize`)? These must continue to route as query string parameters.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The SDK MUST automatically route caller-provided arguments to the correct HTTP transport (path substitution, query string, or JSON body) based on the endpoint's Route definition and OpenAPI specification.
- **FR-002**: Every endpoint with query parameters (as defined by `"in": "query"` in the OpenAPI spec) MUST have those parameters sent via URL query string encoding — never as JSON body content.
- **FR-003**: Every endpoint with path parameters (as defined by `"in": "path"` in the OpenAPI spec) MUST have those parameters substituted into the URL path template before the request is sent.
- **FR-004**: Every endpoint with a request body (as defined by `requestBody` in the OpenAPI spec) MUST have body data sent as JSON — never as URL query string parameters.
- **FR-005**: The SDK MUST provide a single, reusable dispatch mechanism (params_model on Route + validation in `_request()`) that endpoint methods use to route parameters. Endpoint methods MUST retain explicit typed parameter signatures for IDE autocomplete; the params_model validates and aliases at the dispatch layer.
- **FR-006**: Pydantic models used for parameter validation MUST be capable of distinguishing which fields belong to path, query, or body based on information available at the Route level — callers MUST NOT need to specify this distinction.
- **FR-007**: When a caller provides an argument that does not correspond to any known parameter for the endpoint, the SDK MUST raise a validation error before the HTTP request is sent.
- **FR-008**: `None`-valued parameters MUST be excluded from query strings and request bodies (only non-`None` values should be transmitted).
- **FR-009**: The quality assessment system MUST evaluate whether each endpoint has correct parameter routing definitions (params_model for query params, request_model for body, path params in route template). Endpoints with no query or body parameters MUST auto-pass G5; G5 only counts toward overall "complete" status for endpoints that have query or body params.
- **FR-010**: The progress report MUST display per-endpoint parameter routing status alongside existing quality gate results.
- **FR-011**: All existing endpoints that currently have ad-hoc parameter routing (manual dict construction) MUST be updated to use the unified dispatch pattern.

### Key Entities

- **Parameter Route**: The classification of a caller argument into one of three HTTP transport mechanisms: path substitution, query string, or JSON body. Determined by the endpoint's OpenAPI specification and the SDK's Route definition.
- **Params Model**: A Pydantic model that validates and serializes query string parameters for a specific endpoint. Contains field-level metadata (aliases, types, optionality) derived from the OpenAPI spec.
- **Request Model**: A Pydantic model that validates and serializes JSON request body content for a specific endpoint. Already exists in the SDK for POST/PUT/PATCH endpoints.
- **Unified Dispatch**: The single mechanism in the base endpoint class that accepts caller arguments and automatically routes them to the correct HTTP transport based on Route metadata — replacing per-endpoint manual dict construction.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of endpoints with query parameters route those parameters via URL query string — zero instances of query params incorrectly sent as JSON body.
- **SC-002**: 100% of endpoints with request bodies route body data via JSON — zero instances of body data incorrectly sent as query string.
- **SC-003**: Zero endpoint methods contain manual dict construction for parameter routing (e.g., `params = {}; if x: params["X"] = x`). All use the unified dispatch pattern with typed signatures validated by params_model.
- **SC-004**: The progress report displays parameter routing completeness, and 100% of implemented endpoints show correct routing status.
- **SC-005**: Any SDK user calling an endpoint with incorrect or unknown arguments receives a clear validation error message before the HTTP request is sent.
- **SC-006**: `api.address.validate(line1="...", city="...", state="...", zip="...")` succeeds and returns a valid response (the original reported failure is resolved).

## Assumptions

- The existing `Route` dataclass's `_path_params` field (auto-extracted from `{param}` placeholders in the path template) is a reliable indicator of which parameters are path parameters.
- The existing `params_model` field on `Route` is the intended mechanism for query parameter validation but is currently underutilized — this feature will make it the standard.
- The existing `request_model` field on `Route` is the intended mechanism for body validation and is already functional — this feature does not change its behavior, only ensures it is used consistently.
- The OpenAPI/Swagger specification files already present in the repository are the authoritative source of truth for which parameters go where (path, query, body).
- Pydantic's alias system (camelCase aliases on snake_case fields) is sufficient for mapping SDK-style field names to API-expected parameter names.
- Endpoints with only simple scalar path parameters (e.g., a single `company_id: str`) do not need a params_model — the Route.bind() mechanism is sufficient for path-only endpoints.
- Existing tests will need updates to reflect the new unified pattern, but test coverage expectations remain unchanged.
