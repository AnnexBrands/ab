# Tasks: ABConnect API SDK

**Input**: Design documents from `/specs/001-abconnect-sdk/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/endpoints.md, quickstart.md

**Tests**: Included — spec requires fixture validation tests (US2), integration tests (US1), swagger compliance tests (US2), and pytest markers (US4).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, package structure, and build configuration

- [x] T001 Create package directory structure per plan.md (`ab/`, `ab/auth/`, `ab/api/`, `ab/api/endpoints/`, `ab/api/models/`, `ab/api/schemas/`, `tests/`, `tests/unit/`, `tests/integration/`, `tests/models/`, `tests/swagger/`, `tests/fixtures/`, `examples/`, `docs/`, `docs/api/`, `docs/models/`)
- [x] T002 Create `pyproject.toml` with package metadata (name=`ab`), dependencies (pydantic>=2.0, pydantic-settings, requests, python-dotenv), dev dependencies (pytest, sphinx, myst-parser, sphinx-rtd-theme), pytest config (markers: mock, live), and build system
- [x] T003 [P] Create `ab/py.typed` PEP 561 marker file
- [x] T004 [P] Create all `__init__.py` files for package structure (`ab/__init__.py`, `ab/auth/__init__.py`, `ab/api/__init__.py`, `ab/api/endpoints/__init__.py`, `ab/api/models/__init__.py`)
- [x] T005 [P] Create `MOCKS.md` skeleton at repository root with table headers (Endpoint Path, HTTP Method, Model Name, Reason, Date, Status)
- [x] T006 [P] Copy swagger JSON specs to `ab/api/schemas/` (acportal.json, catalog.json, abc.json) from staging URLs

**Checkpoint**: Project installs with `pip install -e .` and imports `ab` without error

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Implement `ab/exceptions.py` — ABConnectError base, AuthenticationError, RequestError (with status_code, message), ConfigurationError, ValidationError
- [x] T008 Implement `ab/config.py` — ABConnectSettings using pydantic-settings with fields: username, password, client_id, client_secret, environment (staging/production), access_key (optional for ABC API), timeout (default 30), max_retries (default 3). Environment variable prefix `ABCONNECT_`. Support `.env.staging` and `.env.production` files. Validate required fields at load time with clear error messages (per D6)
- [x] T009 Implement `ab/api/models/base.py` — ABConnectBaseModel (populate_by_name=True, alias_generator=camel_case), RequestModel (extra="forbid", check() classmethod), ResponseModel (extra="allow", model_post_init logs logger.warning for each field in model_extra) per D2 and constitution Principle I
- [x] T010 Implement `ab/api/models/mixins.py` — IdentifiedModel (id: Optional[str | int]), TimestampedModel (created_date, modified_date, created_by, modified_by), ActiveModel (is_active: Optional[bool]), CompanyRelatedModel (company_id, company_name), JobRelatedModel (job_id). Composite mixins: FullAuditModel, CompanyAuditModel, JobAuditModel
- [x] T011 [P] Implement `ab/api/models/shared.py` — ServiceBaseResponse (__bool__ returns success is True, raise_for_error()), ServiceWarningResponse, PaginatedList[T] generic wrapper (items, page_number, total_pages, total_items, has_previous_page, has_next_page), ListRequest (page, page_size, filters, sort_by — shared by Companies and Users endpoints)
- [x] T012 [P] Implement `ab/api/models/enums.py` — DocumentType, CarrierAPI, and other shared enumerations referenced across models
- [x] T013 Implement `ab/api/route.py` — Frozen Route dataclass (method, path, request_model: Optional[str], response_model: Optional[str], api_surface: str). bind() method returns new instance with path params applied. String-based lazy model resolution per D1 and D9
- [x] T014 Implement `ab/auth/base.py` — TokenStorage abstract base class with methods: get_token(), save_token(), clear_token(). Token dataclass with access_token, refresh_token, expires_at, token_type fields
- [x] T015 Implement `ab/auth/file.py` — FileTokenStorage storing tokens as JSON in `~/.cache/ab/token.{env}.json`. Environment-suffixed to prevent staging/production contamination per D9
- [x] T016 [P] Implement `ab/auth/session.py` — SessionTokenStorage storing tokens in Django request.session with key `ab_token`. Accepts Django request object in constructor
- [x] T017 Implement `ab/http.py` — HttpClient wrapping requests.Session with: connection pooling, configurable base_url per API surface (ACPortal `/api/api/`, Catalog `/api/`, ABC `/api/`), Bearer JWT auth header injection, 30s default timeout, retry with exponential backoff for 429/502/503 (max 3 attempts per D5), OAuth2 password grant, token refresh (300s expiry buffer per D9), accessKey support for ABC API
- [x] T018 Implement `ab/api/base.py` — BaseEndpoint class accepting HttpClient instance (per D3). Methods: _request() dispatches Route via HttpClient, resolves response_model string to class via getattr(models, name), validates and returns typed model. Handles pagination for list endpoints
- [x] T019 Implement `ab/cache.py` — CodeResolver service for cache-based code-to-UUID resolution (per FR-012). Accepts HttpClient, maintains an in-memory dict cache of code→UUID mappings populated on first lookup. Used by any endpoint parameter that accepts either a UUID or a friendly code (e.g., CompanyCode "9999AZ" → CompanyId UUID). Cache is per-client-instance, lazily populated via a search/lookup API call
- [x] T020 Implement `ab/client.py` — ABConnectAPI orchestrator. Constructor accepts env (staging/production), env_file path, or Django request object. Initializes ABConnectSettings, creates HttpClient instances for each API surface, creates FileTokenStorage or SessionTokenStorage based on input, creates CodeResolver instance, instantiates all endpoint groups as attributes (companies, contacts, jobs, etc.)
- [x] T021 Wire up `ab/__init__.py` — Export ABConnectAPI, all exceptions, and key model classes. Export `ab/auth/__init__.py` with TokenStorage, FileTokenStorage, SessionTokenStorage. Export `ab/api/__init__.py` with endpoint group classes
- [x] T022 Wire up `ab/api/models/__init__.py` — Re-export all model classes from domain modules for lazy resolution by Route

**Checkpoint**: Foundation ready — `ABConnectAPI(env="staging")` initializes with valid credentials, authenticates, and HttpClient can make raw requests to all 3 API surfaces

---

## Phase 3: User Story 1 — Call Any Endpoint and Get a Typed Response (Priority: P1) MVP

**Goal**: A developer calls any API endpoint and receives a validated, typed Pydantic model as the response. Auth, URL routing, and response parsing are transparent.

**Independent Test**: Call a single read-only endpoint (e.g., GET /Catalog/{id}) and verify the response is a valid Pydantic model with all expected fields accessible as typed Python attributes.

### Catalog API Models & Endpoints (start here — cleanest swagger per D8)

- [x] T023 [P] [US1] Implement Catalog models in `ab/api/models/catalog.py` — CatalogWithSellersDto, CatalogExpandedDto, AddCatalogRequest, UpdateCatalogRequest, BulkInsertRequest per data-model.md and contracts/endpoints.md
- [x] T024 [P] [US1] Implement Lot models in `ab/api/models/lots.py` — LotDto, LotDataDto, LotOverrideDto, AddLotRequest, UpdateLotRequest per data-model.md
- [x] T025 [P] [US1] Implement Seller models in `ab/api/models/sellers.py` — SellerDto, SellerExpandedDto, AddSellerRequest, UpdateSellerRequest per data-model.md
- [x] T026 [US1] Implement CatalogEndpoint in `ab/api/endpoints/catalog.py` — 6 routes: create, list, get, update, delete, bulk_insert. Routes use Catalog API base URL per contracts/endpoints.md
- [x] T027 [US1] Implement LotsEndpoint in `ab/api/endpoints/lots.py` — 6 routes: create, list, get, update, delete, get_overrides per contracts/endpoints.md
- [x] T028 [US1] Implement SellersEndpoint in `ab/api/endpoints/sellers.py` — 5 routes: create, list, get, update, delete per contracts/endpoints.md

### ACPortal API Models & Endpoints

- [x] T029 [P] [US1] Implement Company models in `ab/api/models/companies.py` — CompanySimple, CompanyDetails, SearchCompanyResponse, CompanySearchRequest per data-model.md (ListRequest is in shared.py)
- [x] T030 [P] [US1] Implement Contact models in `ab/api/models/contacts.py` — ContactSimple, ContactDetailedInfo, ContactPrimaryDetails, SearchContactEntityResult, ContactEditRequest, ContactSearchRequest per data-model.md
- [x] T031 [P] [US1] Implement Job models in `ab/api/models/jobs.py` — Job, JobSearchResult, JobPrice, CalendarItem, JobUpdatePageConfig, JobCreateRequest, JobSaveRequest, JobSearchRequest, JobUpdateRequest (ABC API) per data-model.md
- [x] T032 [P] [US1] Implement Document models in `ab/api/models/documents.py` — Document, DocumentUpdateRequest per data-model.md (upload is multipart, not a Pydantic model)
- [x] T033 [P] [US1] Implement Address models in `ab/api/models/address.py` — AddressIsValidResult, PropertyType per data-model.md
- [x] T034 [P] [US1] Implement Lookup models in `ab/api/models/lookup.py` — ContactTypeEntity, CountryCodeDto, JobStatus, LookupItem per data-model.md
- [x] T035 [P] [US1] Implement User models in `ab/api/models/users.py` — User, UserRole, UserCreateRequest, UserUpdateRequest per data-model.md (ListRequest is in shared.py)
- [x] T036 [US1] Implement CompaniesEndpoint in `ab/api/endpoints/companies.py` — 8 routes: get_by_id, get_details, get_fulldetails, update_fulldetails, create, search, list, available_by_current_user. Accepts CodeResolver from client for cache-based code-to-UUID resolution per FR-012
- [x] T037 [P] [US1] Implement ContactsEndpoint in `ab/api/endpoints/contacts.py` — 7 routes: get, get_details, update_details, create, search, get_primary_details, get_current_user per contracts/endpoints.md
- [x] T038 [P] [US1] Implement JobsEndpoint in `ab/api/endpoints/jobs.py` — 8 ACPortal routes: create, save, get, search, search_by_details, get_price, get_calendar_items, get_update_page_config per contracts/endpoints.md
- [x] T039 [P] [US1] Implement DocumentsEndpoint in `ab/api/endpoints/documents.py` — 4 routes: upload (multipart), list, get (binary), update per contracts/endpoints.md
- [x] T040 [P] [US1] Implement AddressEndpoint in `ab/api/endpoints/address.py` — 2 routes: validate (is_valid), get_property_type per contracts/endpoints.md
- [x] T041 [P] [US1] Implement LookupEndpoint in `ab/api/endpoints/lookup.py` — 4 routes: get_contact_types, get_countries, get_job_statuses, get_items per contracts/endpoints.md
- [x] T042 [P] [US1] Implement UsersEndpoint in `ab/api/endpoints/users.py` — 4 routes: list, get_roles, create, update per contracts/endpoints.md

### ABC API Models & Endpoints

- [x] T043 [P] [US1] Implement AutoPrice models in `ab/api/models/autoprice.py` — QuickQuoteResponse, QuoteRequestResponse, QuoteRequestModel per data-model.md
- [x] T044 [P] [US1] Implement Web2Lead models in `ab/api/models/web2lead.py` — Web2LeadResponse, Web2LeadRequest per data-model.md
- [x] T045 [US1] Implement AutoPriceEndpoint in `ab/api/endpoints/autoprice.py` — 2 routes: quick_quote, quote_request. Uses ABC API base URL with accessKey per contracts/endpoints.md
- [x] T046 [US1] Implement Web2LeadEndpoint in `ab/api/endpoints/web2lead.py` — 2 routes: get, post per contracts/endpoints.md

### ABC Job Update Endpoint

- [x] T047 [US1] Add ABC Job update route to `ab/api/endpoints/jobs.py` — POST /job/update via ABC API surface (separate base URL from ACPortal job routes; this file handles two API surfaces — document clearly with comments). Uses JobUpdateRequest model from `ab/api/models/jobs.py`

### Wire Up All Endpoints

- [x] T048 [US1] Register all endpoint groups in `ab/client.py` — Add companies, contacts, jobs, documents, address, lookup, users, catalog, lots, sellers, autoprice, web2lead as attributes on ABConnectAPI. Update `ab/api/models/__init__.py` to re-export all new domain models

### Unit Tests for Foundation

- [x] T049 [P] [US1] Write unit tests in `tests/unit/test_config.py` — Test ABConnectSettings loads from env vars, .env files, validates required fields, raises ConfigurationError on missing credentials
- [x] T050 [P] [US1] Write unit tests in `tests/unit/test_route.py` — Test Route is frozen, bind() returns new instance with params applied, string model resolution works
- [x] T051 [P] [US1] Write unit tests in `tests/unit/test_auth.py` — Test FileTokenStorage save/load/clear, token expiry calculation, 300s buffer, SessionTokenStorage with mock Django request
- [x] T052 [P] [US1] Write unit tests in `tests/unit/test_http.py` — Test HttpClient retry logic, timeout behavior, base_url routing per API surface, Bearer header injection

### Test Infrastructure

- [x] T053 [US1] Create `tests/conftest.py` — Session-scoped API client fixture, fixture file loader utility (load_fixture(model_name) returns parsed JSON from tests/fixtures/), pytest markers registration (mock, live)
- [x] T054 [US1] Create `tests/constants.py` — Test UUIDs, display IDs, company codes, and other reusable test identifiers

**Checkpoint**: `api = ABConnectAPI(env="staging"); catalog = api.catalog.get(1)` returns a typed CatalogExpandedDto. All unit tests pass. All 59 endpoints are callable and return typed models.

---

## Phase 4: User Story 2 — Validate Models Against Real Fixtures (Priority: P2)

**Goal**: Every Pydantic model accurately represents real API responses. Fixtures are the source of truth.

**Independent Test**: Load a single fixture file, pass it to the corresponding Pydantic model constructor, and assert no validation errors occur and all fields are accessible.

### Fixture Capture

- [x] T055 [US2] Capture Catalog API fixtures in `tests/fixtures/` — CatalogWithSellersDto.json, CatalogExpandedDto.json, LotDto.json, LotOverrideDto.json, LotDataDto.json, SellerDto.json, SellerExpandedDto.json (7 fixtures from live Catalog API)
- [x] T056 [US2] Capture ACPortal API fixtures in `tests/fixtures/` — CompanySimple.json, CompanyDetails.json, SearchCompanyResponse.json, ContactSimple.json, ContactDetailedInfo.json, ContactPrimaryDetails.json, SearchContactEntityResult.json, Job.json, JobSearchResult.json, JobPrice.json, CalendarItem.json, JobUpdatePageConfig.json, Document.json, AddressIsValidResult.json, PropertyType.json, ContactTypeEntity.json, CountryCodeDto.json, JobStatus.json, LookupItem.json, User.json, UserRole.json (21 fixtures)
- [x] T057 [US2] Capture or mock ABC API fixtures in `tests/fixtures/` — QuickQuoteResponse.json, QuoteRequestResponse.json, Web2LeadResponse.json (3 fixtures — mock if live capture requires special credentials, track in MOCKS.md)

### Fixture Validation Tests

- [x] T058 [P] [US2] Write fixture validation tests in `tests/models/test_catalog_models.py` — Load each Catalog fixture, construct model, assert no validation errors, verify key fields are typed and accessible
- [x] T059 [P] [US2] Write fixture validation tests in `tests/models/test_company_models.py` — CompanySimple, CompanyDetails, SearchCompanyResponse against fixtures
- [x] T060 [P] [US2] Write fixture validation tests in `tests/models/test_contact_models.py` — ContactSimple, ContactDetailedInfo, ContactPrimaryDetails, SearchContactEntityResult against fixtures
- [x] T061 [P] [US2] Write fixture validation tests in `tests/models/test_job_models.py` — Job, JobSearchResult, JobPrice, CalendarItem, JobUpdatePageConfig against fixtures
- [x] T062 [P] [US2] Write fixture validation tests in `tests/models/test_document_models.py` — Document against fixture
- [x] T063 [P] [US2] Write fixture validation tests in `tests/models/test_lookup_models.py` — ContactTypeEntity, CountryCodeDto, JobStatus, LookupItem, AddressIsValidResult, PropertyType against fixtures
- [x] T064 [P] [US2] Write fixture validation tests in `tests/models/test_user_models.py` — User, UserRole against fixtures
- [x] T065 [P] [US2] Write fixture validation tests in `tests/models/test_autoprice_models.py` — QuickQuoteResponse, QuoteRequestResponse against fixtures
- [x] T066 [P] [US2] Write fixture validation tests in `tests/models/test_web2lead_models.py` — Web2LeadResponse against fixture

### Model Corrections from Fixtures

- [x] T067 [US2] Correct models that fail fixture validation — Update field types, add missing Optional annotations, add swagger deviation comments to fields where model follows fixture over swagger. Re-run fixture tests until all pass

### Swagger Compliance Tests

- [x] T068 [US2] Write swagger compliance tests in `tests/swagger/test_coverage.py` — Parse all 3 swagger JSON specs, list every endpoint path. Compare against implemented Routes. Alert on unimplemented endpoints. Assert all 59 core endpoints are present in Routes (per FR-010)

### Integration Tests

- [x] T069 [P] [US2] Write integration tests in `tests/integration/test_catalog.py` — @pytest.mark.live tests calling live Catalog API endpoints, verifying response model types
- [x] T070 [P] [US2] Write integration tests in `tests/integration/test_companies.py` — @pytest.mark.live tests for company get, search, fulldetails
- [x] T071 [P] [US2] Write integration tests in `tests/integration/test_contacts.py` — @pytest.mark.live tests for contact get, search, details
- [x] T072 [P] [US2] Write integration tests in `tests/integration/test_jobs.py` — @pytest.mark.live tests for job get, search, price
- [x] T073 [P] [US2] Write integration tests in `tests/integration/test_documents.py` — @pytest.mark.live tests for document list
- [x] T074 [P] [US2] Write integration tests in `tests/integration/test_address.py` — @pytest.mark.live tests for address validate, get_property_type
- [x] T075 [P] [US2] Write integration tests in `tests/integration/test_lookup.py` — @pytest.mark.live tests for lookup get_contact_types, get_countries, get_job_statuses, get_items
- [x] T076 [P] [US2] Write integration tests in `tests/integration/test_users.py` — @pytest.mark.live tests for users list, get_roles
- [x] T077 [P] [US2] Write integration tests in `tests/integration/test_lots.py` — @pytest.mark.live tests for lot list, get
- [x] T078 [P] [US2] Write integration tests in `tests/integration/test_sellers.py` — @pytest.mark.live tests for seller list, get
- [x] T079 [P] [US2] Write integration tests in `tests/integration/test_autoprice.py` — @pytest.mark.live tests for quick_quote (may need mock marker if credentials unavailable)
- [x] T080 [P] [US2] Write integration tests in `tests/integration/test_web2lead.py` — @pytest.mark.live tests for web2lead get

**Checkpoint**: `pytest tests/models/ -v` passes with 100% fixture coverage. `pytest tests/swagger/ -v` identifies all unimplemented endpoints. `pytest tests/integration/ -m live -v` passes for all accessible endpoints.

---

## Phase 5: User Story 3 — Browse Endpoint Documentation with Examples (Priority: P3)

**Goal**: Sphinx-generated documentation with endpoint pages, code examples, model cross-references, and zero broken links.

**Independent Test**: Build Sphinx docs (`make html`), verify each endpoint has description + code example + model cross-reference link. Zero warnings.

### Sphinx Setup

- [x] T081 [US3] Create `docs/conf.py` — Sphinx config with RTD theme, MyST-parser for Markdown, autodoc extensions, intersphinx for Python stdlib, project metadata (ab SDK)
- [x] T082 [US3] Create `docs/Makefile` — Standard Sphinx Makefile with html, clean targets
- [x] T083 [US3] Create `docs/index.md` — Landing page with SDK overview, installation, quickstart link, API reference toctree, model reference toctree

### Endpoint Documentation

- [x] T084 [P] [US3] Create `docs/api/companies.md` — CompaniesEndpoint reference: each method (get_by_id, search, get_fulldetails, etc.) with HTTP method/path, Python code example, parameter docs, and cross-reference link to response model class
- [x] T085 [P] [US3] Create `docs/api/contacts.md` — ContactsEndpoint reference with all 7 methods documented
- [x] T086 [P] [US3] Create `docs/api/jobs.md` — JobsEndpoint reference with all 8 ACPortal + 1 ABC methods documented
- [x] T087 [P] [US3] Create `docs/api/documents.md` — DocumentsEndpoint reference with all 4 methods documented
- [x] T088 [P] [US3] Create `docs/api/address.md` — AddressEndpoint reference with validate, get_property_type documented
- [x] T089 [P] [US3] Create `docs/api/lookup.md` — LookupEndpoint reference with all 4 methods documented
- [x] T090 [P] [US3] Create `docs/api/users.md` — UsersEndpoint reference with all 4 methods documented
- [x] T091 [P] [US3] Create `docs/api/catalog.md` — CatalogEndpoint reference with all 6 methods documented
- [x] T092 [P] [US3] Create `docs/api/lots.md` — LotsEndpoint reference with all 6 methods documented
- [x] T093 [P] [US3] Create `docs/api/sellers.md` — SellersEndpoint reference with all 5 methods documented
- [x] T094 [P] [US3] Create `docs/api/autoprice.md` — AutoPriceEndpoint reference with quick_quote, quote_request documented
- [x] T095 [P] [US3] Create `docs/api/web2lead.md` — Web2LeadEndpoint reference with get, post documented

### Model Documentation

- [x] T096 [US3] Create `docs/models/base.md` — ABConnectBaseModel, RequestModel, ResponseModel, all mixins with autodoc directives showing field types and descriptions
- [x] T097 [P] [US3] Create model docs for each domain — `docs/models/companies.md`, `docs/models/contacts.md`, `docs/models/jobs.md`, `docs/models/documents.md`, `docs/models/address.md`, `docs/models/lookup.md`, `docs/models/users.md`, `docs/models/catalog.md`, `docs/models/lots.md`, `docs/models/sellers.md`, `docs/models/autoprice.md`, `docs/models/web2lead.md` — Each with autodoc showing fields, types, inheritance, descriptions

### Quickstart & Examples

- [x] T098 [US3] Create `docs/quickstart.md` — Copy and adapt from specs/001-abconnect-sdk/quickstart.md with Sphinx cross-references to model and endpoint docs

### Example Files

- [x] T099 [P] [US3] Create `examples/companies.py` — Runnable example demonstrating company get, search, fulldetails with expected output comments
- [x] T100 [P] [US3] Create `examples/contacts.py` — Runnable example demonstrating contact get, search, details
- [x] T101 [P] [US3] Create `examples/jobs.py` — Runnable example demonstrating job get, search, price
- [x] T102 [P] [US3] Create `examples/catalog.py` — Runnable example demonstrating catalog CRUD and listing
- [x] T103 [P] [US3] Create `examples/lots.py` — Runnable example demonstrating lot CRUD and overrides
- [x] T104 [P] [US3] Create `examples/sellers.py` — Runnable example demonstrating seller CRUD
- [x] T105 [P] [US3] Create `examples/autoprice.py` — Runnable example demonstrating quick_quote and quote_request
- [x] T106 [P] [US3] Create `examples/documents.py` — Runnable example demonstrating document list, upload, download
- [x] T107 [P] [US3] Create `examples/web2lead.py` — Runnable example demonstrating web2lead get and post

### Docs Build Validation

- [x] T108 [US3] Build Sphinx docs and fix all warnings — Run `make html` in docs/, verify zero warnings about broken cross-references, verify every endpoint page has code example and model link

**Checkpoint**: `cd docs && make html` completes with 0 warnings. Every endpoint page has description + code example + model cross-reference. Every model page shows fields, types, and inheritance.

---

## Phase 6: User Story 4 — Track Mock Coverage and Replace with Live Data (Priority: P4)

**Goal**: Every endpoint fixture is accounted for — either as live in `tests/fixtures/` or tracked in `MOCKS.md`.

**Independent Test**: Verify `MOCKS.md` exists, every fixture file is accounted for, pytest markers distinguish mock from live tests.

- [x] T109 [US4] Populate `MOCKS.md` with all mock fixtures — For every fixture in tests/fixtures/ that was fabricated (not captured from live API), add entry with: endpoint path, HTTP method, model name, reason (e.g., "No staging credentials for ABC API"), date, and status "mock"
- [x] T110 [US4] Add pytest markers to all fixture validation tests — Mark tests backed by live-captured fixtures with `@pytest.mark.live`, tests backed by mock fixtures with `@pytest.mark.mock` per FR-014
- [x] T111 [US4] Write mock coverage verification test in `tests/test_mock_coverage.py` — Assert every fixture file in tests/fixtures/ is either: (a) tested by a @pytest.mark.live test, or (b) listed in MOCKS.md with status. Assert no untracked mocks exist

**Checkpoint**: `MOCKS.md` accounts for every mock fixture. `pytest -m mock` runs only mock-backed tests. `pytest -m live` runs only live-backed tests. Coverage verification test passes.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final quality, packaging, and documentation completeness

- [x] T112 [P] Create `README.md` at repository root — Project overview, installation, quick example, link to full docs, link to MOCKS.md, badges (if applicable)
- [x] T113 [P] Validate quickstart.md scenarios — Run through each code example in specs/001-abconnect-sdk/quickstart.md against live API, verify all snippets work as documented
- [x] T114 Ensure all model docstrings include field descriptions for Sphinx autodoc — Review all models in `ab/api/models/` and add Field(description=...) where missing
- [x] T115 Final `pyproject.toml` review — Verify all dependencies pinned with minimum versions, classifiers correct, entry points (if any), version set to 0.1.0
- [x] T116 Run full test suite and fix any failures — `pytest tests/ -v --tb=short`, ensure all unit, fixture validation, swagger compliance, and mock coverage tests pass

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
- **User Story 2 (Phase 4)**: Depends on User Story 1 (needs endpoints and models to test against)
- **User Story 3 (Phase 5)**: Depends on User Story 1 (needs endpoints and models to document). Can overlap with US2
- **User Story 4 (Phase 6)**: Depends on User Story 2 (needs fixtures captured to track)
- **Polish (Phase 7)**: Depends on all user stories being complete

### Within Each User Story

- Models before endpoints (endpoints reference models)
- Endpoints before integration tests
- Foundation unit tests can run in parallel with endpoint implementation
- Catalog endpoints before ACPortal (proven pattern before harder API surface per D8)
- Fixture capture before fixture validation tests
- All fixture tests pass before swagger compliance test

### Parallel Opportunities

**Phase 1 — Setup**:
```
T001 (structure) → then T002 (pyproject) → then in parallel: T003, T004, T005, T006
```

**Phase 2 — Foundational**:
```
T007 (exceptions) ─┐
T008 (config) ─────┤─→ T013 (route) ─→ T017 (http) ─→ T018 (base endpoint) ─→ T019 (cache) ─→ T020 (client) ─→ T021, T022
T009 (base models) ┤
T010 (mixins) ─────┘
T011 (shared) ──── in parallel with T009/T010
T012 (enums) ───── in parallel with T009/T010
T014 (auth base) ─→ T015 (file auth) ── in parallel ── T016 (session auth)
```

**Phase 3 — US1 Models** (all [P] models in parallel):
```
T023, T024, T025 (Catalog models) — all in parallel
T029, T030, T031, T032, T033, T034, T035 (ACPortal models) — all in parallel
T043, T044 (ABC models) — in parallel with above
```

**Phase 3 — US1 Endpoints** (after their respective models):
```
T026, T027, T028 (Catalog endpoints) — after T023-T025
T036-T042 (ACPortal endpoints) — after T029-T035, T037-T042 in parallel
T045, T046 (ABC endpoints) — after T043-T044
T047 (ABC job update in jobs.py) — after T031
```

**Phase 4 — US2 Fixture Tests** (all [P] tests in parallel after fixtures captured):
```
T058-T066 (fixture validation tests) — all in parallel
T069-T080 (integration tests) — all in parallel
```

**Phase 5 — US3 Docs** (all [P] docs in parallel):
```
T084-T095 (endpoint docs) — all in parallel
T099-T107 (examples) — all in parallel
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Story 1 (Catalog first, then ACPortal, then ABC)
4. **STOP and VALIDATE**: `api.catalog.get(1)` returns a typed CatalogExpandedDto
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → MVP!
3. Add User Story 2 → Fixture validation → Confidence in model correctness
4. Add User Story 3 → Docs → Discoverable by other developers
5. Add User Story 4 → Mock tracking → Full transparency on coverage
6. Polish → Production-ready

### Recommended Execution Order

For a single developer working sequentially:

1. Phase 1 (Setup) — T001-T006
2. Phase 2 (Foundational) — T007-T022 (core infrastructure)
3. Phase 3 Catalog models + endpoints (T023-T028) — prove the pattern
4. Phase 3 remaining ACPortal + ABC models + endpoints (T029-T048) — expand coverage
5. Phase 3 unit tests (T049-T054) — validate foundation
6. Phase 4 fixture capture + validation (T055-T068) — validate models against reality
7. Phase 4 integration tests (T069-T080) — end-to-end verification
8. Phase 5 docs + examples (T081-T108) — documentation
9. Phase 6 mock tracking (T109-T111) — transparency
10. Phase 7 polish (T112-T116) — final quality

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Start with Catalog API (D8) to establish patterns before tackling harder ACPortal
- Fixture capture (T055-T057) requires valid staging credentials via environment variables
- ABC API endpoints may need mock fixtures if accessKey credentials are unavailable
- jobs.py handles routes from two API surfaces (ACPortal + ABC) — see T047 note
- ListRequest is defined in shared.py (T011) and shared by Companies and Users endpoints
- Total: 116 tasks across 7 phases
