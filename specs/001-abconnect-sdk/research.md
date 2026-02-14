# Research: ABConnect API SDK

**Branch**: `001-abconnect-sdk` | **Date**: 2026-02-13

## Decision Log

### D1: Route Immutability

**Decision**: Routes MUST be frozen dataclasses with a `bind()` method
that returns a new instance with params applied.

**Rationale**: ABConnectTools mutates shared Route instances in-place
(`route.params = {...}`), which is a thread-safety bug. Two concurrent
calls to the same endpoint overwrite each other's params.

**Alternatives considered**:
- Deep-copy Routes before mutation — adds overhead, still semantically
  wrong.
- Lock-based thread safety — adds complexity, masks the design flaw.

### D2: Split Request vs Response Model Config

**Decision**: Define two base classes:
- `RequestModel(ABConnectBaseModel)` with `extra="forbid"` — strict
  outbound validation catches typos and invalid fields.
- `ResponseModel(ABConnectBaseModel)` with `extra="allow"` — resilient
  inbound deserialization survives API additions without breaking.
  Extra fields are stored in `model_extra` and logged via
  `logger.warning` in `model_post_init` to surface drift immediately.

**Rationale**: ABConnectTools uses `extra="forbid"` for all models.
When the API adds a new field, all response deserialization breaks
until the model is updated. Response models should accept unknown
fields while making them visible. `extra="allow"` + warning logging
gives production resilience with immediate developer visibility.

**Alternatives considered**:
- Single `extra="forbid"` everywhere (current) — breaks on API
  changes.
- `extra="ignore"` for responses — silently drops unknown fields,
  drift goes unnoticed until fixture re-capture.
- Single `extra="forbid"` everywhere with fast model updates —
  requires SDK release for every API field addition.

### D3: Instance-Level Request Handler

**Decision**: Pass `RequestHandler` through endpoint constructors, not
via class-level `set_request_handler()`.

**Rationale**: Class-level injection prevents multiple simultaneous API
clients (e.g., staging + production, or two users in Django). Each
client instance MUST own its own handler chain.

**Alternatives considered**:
- Thread-local storage — still prevents two clients in same thread.
- Context variables — Python-native but adds complexity.

### D4: Unified HTTP Client with Session

**Decision**: Use a single `HttpClient` class wrapping `requests.Session`
for all API surfaces (ACPortal, Catalog, ABC). The session provides
connection pooling and persistent headers. URL routing is based on a
`base_url` parameter per API surface.

**Rationale**: ABConnectTools has `RequestHandler` and
`CatalogRequestHandler` as near-duplicate classes. Unifying them with
a base URL parameter eliminates duplication while enabling connection
reuse.

**Alternatives considered**:
- Separate handler per API surface (current) — duplicated code.
- httpx instead of requests — better async story but heavier
  dependency; defer to future.

### D5: Timeouts and Retry

**Decision**: All HTTP calls MUST have a configurable timeout (default
30s). Transient failures (429, 502, 503) MUST be retried with
exponential backoff (max 3 attempts).

**Rationale**: ABConnectTools has no timeouts or retry logic. A hung
API call blocks indefinitely; transient errors cause immediate failure.

**Alternatives considered**:
- No retry (current) — fragile in production.
- tenacity library — adds a dependency; use stdlib `time.sleep` with
  manual backoff instead.

### D6: Configuration via pydantic-settings

**Decision**: Use `pydantic-settings` for typed configuration with
validation. All required keys (client ID, client secret) MUST be
validated at load time with clear error messages.

**Rationale**: ABConnectTools uses a custom Config singleton with
untyped `dict` storage and no validation. Missing keys cause cryptic
runtime errors deep in the auth flow.

**Alternatives considered**:
- Custom singleton (current) — no validation, dual state in
  os.environ.
- dataclasses — no automatic env var loading.
- dynaconf — heavier dependency.

### D7: Core Endpoint Subset (59 endpoints)

**Decision**: Initial release targets 59 endpoints:
- ACPortal: 37 (Companies 8, Contacts 7, Jobs 8, Documents 4,
  Address 2, Lookup 4, Users 4)
- Catalog: 17 (all — cleanest API surface)
- ABC: 5 (AutoPrice 2, Job update 1, Web2Lead 2)

**Rationale**: This covers the primary CRUD and search operations
across all three APIs. Catalog is included in full because it is small
(17 endpoints) with the best swagger quality. Deferred endpoints are
specialized features (scheduling, payments, SMS, forms, etc.).

**Alternatives considered**:
- All 328 endpoints — too large for initial quality-focused release.
- Catalog only — too narrow, doesn't prove multi-API architecture.

### D8: Start with Catalog API for Model Development

**Decision**: Begin model and fixture development with the Catalog API.

**Rationale**: Catalog has the cleanest swagger spec (OpenAPI 3.0.4)
with 16 of 17 endpoints having reliable response schemas. This
establishes the model/fixture/test patterns on solid ground before
tackling ACPortal where 29 of 37 core endpoints have NO swagger
response schema.

**Alternatives considered**:
- Start with ACPortal — higher business value but much harder to
  model correctly without swagger support.
- Start in parallel — risks inconsistent patterns before the
  foundation is proven.

### D9: Preserve Proven Patterns

**Decision**: The following ABConnectTools patterns MUST be preserved
in the rebuild (with improvements noted above):

- **Mixin hierarchy**: IdentifiedModel, TimestampedModel, ActiveModel,
  CompanyRelatedModel, JobRelatedModel, FullAuditModel,
  CompanyAuditModel, JobAuditModel.
- **ServiceBaseResponse**: `__bool__` returns `self.success is True`;
  `raise_for_error()` for error surfacing.
- **String-based lazy model resolution**: Route dataclass stores model
  names as strings; resolved at request time via
  `getattr(models, name)`.
- **`check()` class method**: Validates and serializes request bodies
  with `by_alias=True`.
- **Dual test pattern**: Fixture validation tests (fast, offline) +
  integration tests (live API, marked).
- **Token sharing**: Single `TokenStorage` shared across all API
  surface clients.
- **300-second expiry buffer**: Refresh tokens 5 minutes before
  actual expiration.
- **Environment-suffixed token files**: Prevents staging/production
  token contamination.
- **Cache-based code-to-UUID resolution**: `get_cache(code)` via
  external cache service.

### D10: Package Structure

**Decision**: Single Python package `ab` with flat module layout:

```
ab/
├── __init__.py          # Public API exports
├── client.py            # ABConnectAPI orchestrator
├── config.py            # pydantic-settings configuration
├── exceptions.py        # Custom exceptions
├── http.py              # HttpClient (requests.Session wrapper)
├── auth/
│   ├── __init__.py
│   ├── base.py          # TokenStorage ABC
│   ├── file.py          # FileTokenStorage
│   └── session.py       # SessionTokenStorage (Django)
├── api/
│   ├── __init__.py
│   ├── route.py         # Frozen Route dataclass
│   ├── base.py          # BaseEndpoint
│   ├── endpoints/       # One file per endpoint group
│   │   ├── companies.py
│   │   ├── contacts.py
│   │   ├── jobs.py
│   │   ├── documents.py
│   │   ├── address.py
│   │   ├── lookup.py
│   │   ├── users.py
│   │   ├── catalog.py
│   │   ├── lots.py
│   │   ├── sellers.py
│   │   ├── autoprice.py
│   │   └── web2lead.py
│   ├── models/          # Pydantic models
│   │   ├── __init__.py  # Re-exports all models
│   │   ├── base.py      # ABConnectBaseModel, RequestModel, ResponseModel
│   │   ├── mixins.py    # IdentifiedModel, TimestampedModel, etc.
│   │   ├── shared.py    # ServiceBaseResponse, pagination wrappers
│   │   ├── companies.py
│   │   ├── contacts.py
│   │   ├── jobs.py
│   │   ├── documents.py
│   │   ├── address.py
│   │   ├── lookup.py
│   │   ├── users.py
│   │   ├── catalog.py
│   │   ├── lots.py
│   │   ├── sellers.py
│   │   ├── autoprice.py
│   │   └── web2lead.py
│   └── schemas/         # Swagger JSON specs (reference)
│       ├── acportal.json
│       ├── catalog.json
│       └── abc.json
└── py.typed             # PEP 561 type stub marker
```

## API Surface Analysis

### Schema Reliability by API

| API | Core Endpoints | Schema Reliable | Needs Fixture |
|-----|---------------|-----------------|---------------|
| Catalog | 17 | 16 | 1 |
| ACPortal | 37 | 8 | 29 |
| ABC | 5 | 0 | 5 |
| **Total** | **59** | **24** | **35** |

### Key API Differences

| Concern | ACPortal | Catalog | ABC |
|---------|----------|---------|-----|
| OpenAPI version | 3.0.1 | 3.0.4 | 3.0.1 |
| URL prefix | `/api/api/` (double) | `/api/` (single) | `/api/` (single) |
| Auth | Bearer JWT | Bearer JWT | Bearer JWT + accessKey |
| ID types | UUID (mostly) | int32 | UUID |
| Pagination | Unknown (no schemas) | PaginatedList wrapper | N/A |
| Response schemas | ~30% defined | ~95% defined | 0% defined |

### ABC API Auth Note

ABC API uses `accessKey` in addition to Bearer JWT for some
endpoints. The `accessKey` is passed as a query parameter or body
field. The SDK MUST support both mechanisms transparently.
