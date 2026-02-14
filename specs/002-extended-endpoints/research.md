# Research: Extended API Endpoints

**Branch**: `002-extended-endpoints` | **Date**: 2026-02-13

## Decision Log

### D1: Extend JobsEndpoint vs Separate Classes

**Decision**: Timeline, notes, tracking, and parcel operations are added as methods on the existing `JobsEndpoint`. Shipments, payments, and forms get their own new endpoint classes (`ShipmentsEndpoint`, `PaymentsEndpoint`, `FormsEndpoint`).

**How ABConnectTools does it**: ABConnectTools uses a `JobsPackage` composite that instantiates separate sub-endpoint classes for every job operation group: `JobShipmentEndpoint`, `JobPaymentEndpoint`, `JobFormEndpoint`, `JobTimelineEndpoint`, `JobTrackingEndpoint`, `JobNoteEndpoint`, `JobParcelItemsEndpoint`. The client exposes them as `api.jobs.shipment`, `api.jobs.payment`, `api.jobs.form`, etc. This creates a deep nesting pattern (`api.jobs.timeline.get_timeline()`).

**Rationale for departure**: Deep nesting increases cognitive load and typing. The `ab` SDK favors a flatter API surface: `api.jobs.get_timeline()` instead of `api.jobs.timeline.get_timeline()`. Groups with many methods (forms: 15, shipments: 14, payments: 10) get their own top-level class to keep `JobsEndpoint` manageable, while small groups (notes: 4, tracking: 2, parcels: 7) stay on `JobsEndpoint` since they don't overwhelm the class.

**Threshold**: Groups with 10+ methods get their own class. Groups under 10 extend `JobsEndpoint`.

**Alternatives considered**:
- Mirror ABConnectTools' `JobsPackage` pattern — creates deep nesting, more files, more indirection.
- Everything on `JobsEndpoint` — class becomes too large (~40+ new methods plus existing 8).
- Everything as separate classes — too many small classes for 2-4 method groups.

### D2: Form Binary Response Pattern

**Decision**: Form endpoints use `response_model="bytes"` on the Route and return raw `bytes` to the caller, matching the existing `documents.get()` pattern.

**How ABConnectTools does it**: ABConnectTools defines `response_model="bytes"` on form routes. The `BaseEndpoint._validate_response` method returns the response as-is when it sees `"bytes"`. However, the actual bytes come from `RequestHandler._handle_response` which detects binary content types and returns `resp.content`. This two-layer cooperation works by coincidence — the code path is fragile and undocumented.

**Rationale for alignment**: The `ab` SDK's `HttpClient._handle_response` already handles binary content types correctly (returns `resp.content` for `application/pdf`, `application/octet-stream`, etc.). The `BaseEndpoint._request` method passes `"bytes"` response_model through without attempting model validation. This pattern is proven in `documents.get()` and needs no new mechanism.

**Alternatives considered**:
- Typed wrapper `FormResponse(content=bytes, content_type=str)` — adds developer ergonomics but introduces a new pattern inconsistent with `documents.get()`. Rejected per clarification session.
- `raw=True` bypass (as `documents.get()` uses) — works but bypasses the Route system. Prefer Route-based `response_model="bytes"` for consistency and future tooling.

### D3: Tracking Version Strategy

**Decision**: Implement only v1 (basic `/tracking`) and v3 (latest with history, `/v3/job/.../tracking/{historyAmount}`). Skip v2 entirely.

**How ABConnectTools does it**: ABConnectTools has `JobTrackingEndpoint` (v1 with 2 methods), `V2Endpoint` (1 method), and `V3Endpoint` (1 method). The V2 and V3 endpoints use the **old string-based call pattern** (`self._make_request("GET", path)`) instead of Route objects, meaning they bypass request/response validation entirely. V2 also has a bug where `historyAmount` appears as both a path param and a query param.

**Rationale for departure**: V2 is a transitional version superseded by V3. Implementing v2 would add surface area with no value since v3 provides the same data with improvements. ABConnectTools' V2 implementation is broken anyway (bypasses Route system, duplicate params). V1 is retained because it provides basic tracking without requiring a `historyAmount` parameter.

**Alternatives considered**:
- All three versions — adds maintenance burden for v2 with no consumer benefit.
- V3 only — skips v1 which has a simpler interface for basic tracking.

### D4: Timeline — Typed Models vs Helper Shortcuts

**Decision**: Provide typed endpoint methods for the 9 raw API operations. Do NOT port ABConnectTools' numeric helper methods (`_2()`, `_3()`, `schedule()`, `received()`, etc.).

**How ABConnectTools does it**: `TimelineHelpers` provides status-specific convenience methods that combine a `get_task()` + `set_task()` flow with pre-built template dicts. Methods like `schedule()`, `received()`, `pack_start()` encode business logic about which task codes map to which status numbers. It also has mutable class-level template dicts that are shallow-copied per call.

**Rationale for departure**: The helper methods encode business logic that belongs in the consuming application, not the SDK. Task code → status number mappings change with ABConnect's business rules. Hardcoding them in the SDK creates a maintenance burden and breaks when new statuses are added. The SDK should be a thin, faithful wrapper over the API. Consuming applications can build their own helpers using the typed timeline models.

**Alternatives considered**:
- Port all helpers with typed models — couples SDK to ABConnect's business logic, needs constant updates.
- Port a subset of helpers — inconsistent; users would wonder why `schedule()` exists but `storage_begin()` doesn't.
- Provide helpers as a separate optional module — over-engineering for a pattern that belongs in application code.

### D5: Payment Endpoint Model Coverage

**Decision**: Define typed Pydantic models for all payment request and response bodies, even where ABConnectTools uses raw `Dict[str, Any]`.

**How ABConnectTools does it**: `JobPaymentEndpoint` has 10 methods but typed models for only 3 (`AttachCustomerBankModel`, `PaymentSourceDetails`, `VerifyBankAccountRequest`). The remaining 7 methods accept/return raw dicts. Several routes have `response_model=None`, which actually causes a `ValueError` at runtime in ABConnectTools' `_validate_response`.

**Rationale for departure**: The `ab` SDK's constitution (Principle I) requires every response to resolve to a validated Pydantic model. Raw dicts are not acceptable. Even where swagger schemas are missing, we build models from fixture data (captured or mocked). This catches API drift immediately and provides IDE autocomplete for consumers.

**Alternatives considered**:
- Mirror ABConnectTools' sparse coverage — violates constitution Principle I.
- Use `Dict[str, Any]` with a TODO comment — defers the work but creates technical debt.

### D6: Shipment Endpoint — Job-Scoped vs Global

**Decision**: `ShipmentsEndpoint` handles both job-scoped shipment operations (under `/api/job/{jobDisplayId}/shipment/...`) and global shipment operations (under `/api/shipment/...`). It accepts both `acportal_client` parameters since both use the same API surface.

**How ABConnectTools does it**: ABConnectTools splits these into `JobShipmentEndpoint` (job-scoped, 11 methods inside `JobsPackage`) and `ShipmentEndpoint` (global, 3 methods at top level). The `ShipHelper` composes both plus `JobFreightProvidersEndpoint` for rate selection convenience methods.

**Rationale for departure**: The global shipment endpoints (`/api/shipment`, `/api/shipment/accessorials`, `/api/shipment/document/{docId}`) are closely related to job-scoped shipment operations. Separating them forces consumers to discover two different access patterns for related functionality. A single `ShipmentsEndpoint` with clear method naming (e.g., `get_global_accessorials()` vs `get_accessorials(job_display_id)`) is more discoverable.

**Alternatives considered**:
- Two separate classes (matching ABConnectTools) — fragments related operations.
- Global methods on the client directly — breaks the endpoint-group pattern.

### D7: Notes — Job-Scoped Only

**Decision**: Implement only job-scoped note operations (`/api/job/{jobDisplayId}/note/...`). Do NOT implement the top-level note endpoints (`/api/note/...`).

**How ABConnectTools does it**: ABConnectTools has both `JobNoteEndpoint` (inside `JobsPackage`) and a separate `NoteEndpoint` (top-level). The top-level `NoteEndpoint` uses the broken old string-based call pattern and has auto-generated method names (`get_get`, `post_post`, `put_put`).

**Rationale for departure**: The spec scopes this feature to HIGH-priority job workflow endpoints. Top-level notes are in the MEDIUM priority group. Job-scoped notes are the primary use case for integrations. Top-level notes can be added in a future feature if needed.

**Alternatives considered**:
- Include top-level notes — scope creep beyond HIGH priority.

### D8: Form Fixture Strategy

**Decision**: Form endpoints that return binary content (PDF/HTML) do NOT get traditional JSON fixture files. Instead, they get integration tests that verify: (a) the endpoint returns bytes, (b) the content-type header matches expected format, and (c) the byte content is non-empty. The one form endpoint that returns JSON (`get_form_shipments`) gets a standard JSON fixture.

**How ABConnectTools does it**: ABConnectTools has no fixture validation for form endpoints. `FormsShipmentPlan` is the only model, and it has no corresponding fixture test.

**Rationale**: Binary content (PDFs) cannot be validated against a Pydantic model. Storing binary fixtures would bloat the test suite without adding model validation value. Constitution Principle II requires fixtures for "every endpoint" — for binary endpoints, the fixture equivalent is a content-type + non-empty assertion in integration tests. The `get_form_shipments` endpoint returns JSON and gets a standard fixture.

**Alternatives considered**:
- Store binary fixtures — large files, no model validation value, format may change.
- Skip testing forms entirely — violates Four-Way Harmony.

### D9: Preserving ABConnectTools Patterns

**Decision**: The following ABConnectTools patterns are preserved (consistent with feature 001 decisions D9):

- **Route-based dispatch**: All endpoints use frozen Route dataclasses with `bind()`. No string-based `_make_request("GET", path)` calls.
- **Model naming**: Response models follow API naming conventions (e.g., `ShipmentOriginDestination`, `FormsShipmentPlan`). Request models use `{Action}Request` suffix.
- **Mixin inheritance**: New models reuse existing mixins (IdentifiedModel, TimestampedModel, etc.) where applicable.
- **snake_case fields + camelCase aliases**: All models follow the established aliasing pattern.
- **`ServiceBaseResponse` for status responses**: Endpoints that return `{ success, errorMessage }` use the existing `ServiceBaseResponse` model.
- **Fixture naming**: `{ModelName}.json` in `tests/fixtures/`.

**Notable ABConnectTools bugs NOT carried forward**:
- Route mutation thread-safety bug (fixed by frozen dataclasses in 001)
- `response_model=None` causing ValueError (all routes must define response_model)
- Wrong request model validation (`BookShipmentRequest` used for rate quote requests)
- Fragile JSON parse error detection for DELETE responses
- Mutable class-level template dicts in timeline helpers
