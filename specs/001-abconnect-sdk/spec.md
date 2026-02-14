# Feature Specification: ABConnect API SDK

**Feature Branch**: `001-abconnect-sdk`
**Created**: 2026-02-13
**Status**: Draft
**Input**: User description: "Create an API SDK for the set of ABConnect APIs with fixture-driven Pydantic models, Four-Way Harmony, Sphinx documentation, and mock tracking"

## Clarifications

### Session 2026-02-13

- Q: What is the relationship to ABConnectTools? → A: Clean rebuild, independent coexisting package. High-quality patterns only; ABConnectTools is reference material, not a code source.
- Q: Should the initial release target all endpoints or a subset? → A: Core subset first (~30-50 endpoints across all 3 APIs). Auth, client, models, tests, docs, and endpoint infrastructure MUST be optimal and production-quality from the start. Foundation quality over breadth.
- Q: Should the SDK include a CLI interface? → A: Python API only for the initial release. CLI deferred to a future feature.
- Q: Should Django session-based auth be included? → A: Yes. Both FileTokenStorage and SessionTokenStorage from the start.
- Q: What should the installable package be named? → A: `ab`. Import as `from ab.api import ...`, install as `pip install ab`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Call Any Endpoint and Get a Typed Response (Priority: P1)

A developer integrating with ABConnect wants to call any API endpoint
and receive a validated, typed Pydantic model as the response. The
`ab` package handles authentication, URL routing (ACPortal vs Catalog
vs ABC), and response parsing transparently so the developer works
with Python objects rather than raw JSON.

**Why this priority**: This is the foundational value proposition of
the SDK. Without typed endpoint access, nothing else (docs, fixtures,
tests) has a target to validate against. A working endpoint call with
a correct model is the minimum viable product.

**Independent Test**: Can be fully tested by calling a single
read-only endpoint (e.g., GET /companies/{id}) and verifying the
response is a valid Pydantic model with all expected fields accessible
as typed Python attributes.

**Acceptance Scenarios**:

1. **Given** valid credentials and a staging environment, **When** a
   developer calls `api.companies.get_by_id(company_id)`, **Then**
   the SDK returns a Pydantic model with typed fields (not a raw dict)
   and no validation errors.
2. **Given** an endpoint on the Catalog API, **When** the developer
   calls `api.catalog.get(catalog_id)`, **Then** the SDK routes to
   the correct base URL (`catalog-api.staging.abconnect.co/api`) and
   returns a validated model.
3. **Given** an endpoint on the ABC API, **When** the developer
   calls `api.autoprice.quick_quote(request)`, **Then** the SDK
   routes to `api.staging.abconnect.co/api` and returns a validated
   quote response model.
4. **Given** an expired access token, **When** the developer makes
   any API call, **Then** the SDK transparently refreshes the token
   and retries the request without developer intervention.
5. **Given** a Django application using SessionTokenStorage, **When**
   the developer initializes the client with a Django request object,
   **Then** tokens are stored in the Django session and persist across
   requests.

---

### User Story 2 - Validate Models Against Real Fixtures (Priority: P2)

A developer maintaining the SDK wants to verify that every Pydantic
model accurately represents real API responses. They capture a live
response as a JSON fixture and run a test that validates the fixture
against the model. When the API changes, the fixture test fails and
identifies exactly which fields are new, missing, or changed.

**Why this priority**: Fixtures are the source of truth for model
correctness (per the constitution). Without fixture validation, models
drift from reality and the SDK produces runtime errors for consumers.

**Independent Test**: Can be tested by loading a single fixture file,
passing it to the corresponding Pydantic model constructor, and
asserting no validation errors occur and all fields are accessible.

**Acceptance Scenarios**:

1. **Given** a captured fixture file `tests/fixtures/CompanySimple.json`,
   **When** a test loads it and constructs `CompanySimple(**data)`,
   **Then** the model validates without error and all fields match
   expected types.
2. **Given** a model whose swagger definition is known to be incorrect,
   **When** the fixture is captured from a live API call, **Then** the
   model matches the fixture (reality) and includes comments
   documenting where it deviates from swagger.
3. **Given** an endpoint where a live fixture cannot be obtained,
   **When** a mock fixture is created, **Then** the mock is listed in
   `MOCKS.md` with the endpoint path, reason, date, and status.

---

### User Story 3 - Browse Endpoint Documentation with Examples (Priority: P3)

A developer new to the ABConnect APIs wants to find an endpoint, read
its documentation, see an example of how to call it, and understand
the shape of the response model. Sphinx-generated documentation
provides a page for each endpoint group with inline code examples and
cross-reference links to the Pydantic model classes.

**Why this priority**: Documentation is the primary discovery
mechanism for SDK consumers. Without it, developers must read source
code to understand endpoint behavior and response shapes.

**Independent Test**: Can be tested by building the Sphinx
documentation (`make html`) and verifying that each documented
endpoint has: a description, a code example, and a working
cross-reference link to the response model class.

**Acceptance Scenarios**:

1. **Given** the Sphinx documentation is built, **When** a developer
   navigates to the Companies endpoint page, **Then** they see each
   method (get_by_id, search, get_details, etc.) with a description,
   HTTP method/path, Python example, and a link to the response model.
2. **Given** a response model page (e.g., CompanySimple), **When** a
   developer opens it, **Then** they see all fields with types,
   descriptions, and which mixin base classes the model inherits from.
3. **Given** the documentation build, **When** `make html` completes,
   **Then** there are zero Sphinx warnings about broken
   cross-references.

---

### User Story 4 - Track Mock Coverage and Replace with Live Data (Priority: P4)

An SDK maintainer wants to see which endpoints still rely on mock
fixtures versus live-captured data. They open `MOCKS.md` and see a
table of every mocked fixture with the reason it was mocked and
whether it has been resolved. As access becomes available, they
replace mocks with live fixtures and update the tracking file.

**Why this priority**: Mock tracking ensures transparency about SDK
coverage quality. Without it, consumers cannot assess which parts of
the SDK are validated against real APIs.

**Independent Test**: Can be tested by verifying that `MOCKS.md`
exists, every fixture file is accounted for (either as live in
`tests/fixtures/` or listed in `MOCKS.md`), and pytest markers
distinguish mock-validated from live-validated tests.

**Acceptance Scenarios**:

1. **Given** a new endpoint is added with a mock fixture, **When** the
   developer creates the fixture, **Then** an entry MUST be added to
   `MOCKS.md` with: endpoint path, HTTP method, model name, reason,
   date, and status "mock".
2. **Given** an endpoint previously mocked, **When** a live fixture
   becomes available, **Then** the mock fixture is replaced, the
   `MOCKS.md` entry is updated to status "live", and the test marker
   changes from `@pytest.mark.mock` to `@pytest.mark.live`.

---

### Edge Cases

- What happens when the API returns a field not declared in the
  Pydantic model? Response models use `extra="ignore"`, so
  deserialization succeeds. The next fixture capture detects the
  new field via snapshot comparison, prompting a model update.
- What happens when the API removes a previously required field?
  The fixture test fails, prompting a model update to make the field
  Optional or remove it.
- What happens when ACPortal swagger declares a model that does not
  match reality? The model follows reality (the fixture), and a
  comment documents the swagger deviation on the affected field(s).
- What happens when authentication fails during fixture capture?
  The test is marked with `@pytest.mark.mock`, a mock fixture is
  created, and the endpoint is tracked in `MOCKS.md`.
- What happens when the same model is returned by multiple endpoints?
  The model is defined once and shared; each endpoint's fixture
  validates against the same model class.
- What happens when an endpoint exists in swagger but has no
  implementation yet? A swagger compliance test alerts that the
  endpoint is unimplemented, but no fixture or model is required
  until implementation begins.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: SDK MUST provide typed client methods for all
  implemented endpoints across ACPortal, Catalog, and ABC APIs.
  Initial release targets 59 core endpoints (37 ACPortal +
  17 Catalog + 5 ABC) covering Companies, Contacts, Jobs,
  Documents, Address, Lookup, Users, Catalog, Lots, Sellers,
  AutoPrice, and Web2Lead.
- **FR-002**: SDK MUST authenticate via OAuth2 password grant and
  automatically refresh tokens before expiration. MUST support both
  FileTokenStorage (standalone) and SessionTokenStorage (Django).
- **FR-003**: SDK MUST route requests to the correct base URL based
  on the API surface (ACPortal double `/api/api/`, Catalog single
  `/api/`, ABC single `/api/`).
- **FR-004**: Every model MUST inherit from `ABConnectBaseModel`
  and use mixin-based inheritance (IdentifiedModel,
  TimestampedModel, etc.). Request models MUST use
  `extra="forbid"` (via `RequestModel`) to catch invalid
  outbound fields. Response models MUST use `extra="ignore"`
  (via `ResponseModel`) to survive API field additions without
  breaking deserialization.
- **FR-005**: Every response model MUST use snake_case field names
  with camelCase aliases matching actual API JSON keys.
- **FR-006**: Every implemented endpoint MUST have a corresponding
  fixture file in `tests/fixtures/` that validates against its
  Pydantic model.
- **FR-007**: Every endpoint where a live fixture cannot be obtained
  MUST have a mock fixture tracked in `MOCKS.md` with endpoint path,
  HTTP method, model name, reason, date, and status.
- **FR-008**: Every public endpoint method, request model, and
  response model MUST have Sphinx documentation with description,
  HTTP method/path, Python code example, and cross-reference to the
  model class.
- **FR-009**: SDK MUST include runnable example files in `examples/`
  for each endpoint group demonstrating usage and expected output.
- **FR-010**: SDK MUST include swagger compliance tests that alert
  when endpoints appear in swagger that are not yet implemented.
- **FR-011**: SDK MUST support both staging and production
  environments via configuration (environment variable or parameter).
- **FR-012**: SDK MUST support cache-based code-to-UUID resolution
  (e.g., CompanyCode "9999AZ" resolved to a CompanyId UUID) for any
  parameter that accepts a UUID.
- **FR-013**: Route definitions MUST declare expected request and
  response model names so validation is automatic on every call.
- **FR-014**: SDK MUST distinguish mock-validated tests from
  live-validated tests via pytest markers (`@pytest.mark.mock`,
  `@pytest.mark.live`).
- **FR-015**: SDK MUST be installable as the `ab` package
  (`pip install ab`) with imports under the `ab` namespace
  (e.g., `from ab.api import ABConnectAPI`).
- **FR-016**: SDK is a clean-room rebuild. No code MUST be copied
  from ABConnectTools. ABConnectTools serves as architectural
  reference only.
- **FR-017**: Initial release is Python API only. No CLI interface.

### Key Entities

- **Endpoint**: A callable API operation defined by HTTP method, URL
  path, optional request model, and response model. Grouped by API
  surface (ACPortal, Catalog, ABC) and resource (companies, jobs,
  catalogs, etc.).
- **Model**: A Pydantic class representing an API request or response
  body. Uses mixin inheritance for common fields (id, timestamps,
  audit trails). Field names are snake_case with camelCase aliases.
- **Fixture**: A JSON file containing a captured API response used to
  validate model correctness. Lives in `tests/fixtures/` and is named
  `{ModelName}.json`.
- **Mock**: A fabricated fixture used when a live response cannot be
  captured. Tracked in `MOCKS.md` with metadata about why and when.
- **Route**: A dataclass binding an HTTP method and URL path template
  to request/response model names and parameter specifications.
- **Client**: The top-level SDK object that manages authentication,
  environment configuration, and provides access to all endpoint
  groups as attributes (e.g., `client.companies`, `client.catalog`).
- **TokenStorage**: Abstract base for authentication token
  persistence. Two implementations: FileTokenStorage (caches tokens
  on disk for standalone scripts) and SessionTokenStorage (stores
  tokens in Django request.session for web apps).

### Assumptions

- Authentication uses the same identity server for all three APIs
  (staging: `login.staging.abconnect.co`, production:
  `login.abconnect.co`) with OAuth2 password + refresh token grants.
- The SDK targets Python 3.11+ with Pydantic v2.
- Sphinx documentation uses the ReadTheDocs theme with MyST-parser
  for Markdown support.
- The existing ABConnectTools project at `/usr/src/pkgs/ABConnectTools/`
  serves as the architectural reference for patterns and conventions
  but no code is copied from it.
- ACPortal swagger is the most unreliable of the three specs; Catalog
  and ABC swagger are generally more accurate but still require
  fixture validation.
- Fixture capture requires valid staging credentials configured via
  environment variables.
- The initial core endpoint subset will be determined during planning
  by selecting the most-used operations from Companies, Contacts,
  Jobs, Catalog, and Quoting groups.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every implemented endpoint returns a validated Pydantic
  model (zero raw-dict responses in the public API).
- **SC-002**: 100% of implemented endpoints have a fixture file that
  validates against the corresponding model without error.
- **SC-003**: Sphinx documentation builds with zero warnings and every
  endpoint page includes a code example and model cross-reference.
- **SC-004**: `MOCKS.md` accounts for every endpoint where a live
  fixture is unavailable, with no untracked mocks.
- **SC-005**: Swagger compliance tests identify 100% of unimplemented
  endpoints across all three API surfaces.
- **SC-006**: Every endpoint documentation page includes a
  runnable Python code example and a cross-reference link to the
  response model class, enabling a developer unfamiliar with the
  SDK to find and call any documented endpoint using only the
  Sphinx documentation.
- **SC-007**: Model validation catches field changes (additions,
  removals, type changes) within one test run after an API update.
- **SC-008**: Token refresh is seamless — zero authentication failures
  during normal usage within a session, for both FileTokenStorage and
  SessionTokenStorage modes.
- **SC-009**: Package installs cleanly via `pip install ab` with no
  dependency conflicts against ABConnectTools.
