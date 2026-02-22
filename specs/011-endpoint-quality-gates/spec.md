# Feature Specification: Endpoint Quality Gates

**Feature Branch**: `011-endpoint-quality-gates`
**Created**: 2026-02-21
**Status**: Implemented
**Input**: User description: "Perform a detailed analysis on the companies endpoint. The FIXTURES.md file states /companies/{id}/fulldetails status is complete. Does our constitution require that the test_get_fulldetails response is an instance of the expected response_model and that casting to the response does not emit any warnings? It should. Calling pytest tests/integration/test_companies.py results in four passing tests of no substance. Calling python -m examples companies get_fulldetails DLC outputs several warnings that the model. The sphinx docs gives the incorrect response schema of Any when it should be CompanyDetails. There should be a models section in the docs that shows collapsed elements of companydetails such as address. The companydetails model should contain address in the first place. We need to take strong action to create a TRUE fixtures.md and progress.html file for all endpoints, which must address all endpoint return types, tests are meaningful, docs are comprehensive. Write the file failing all, and create robust gates to mark items as passing."

## Clarifications

### Session 2026-02-21

- Q: When FR-003 adds missing fields to models, how deep should the nested typing go? → A: Full depth — typed Pydantic sub-models for ALL nesting levels. Every nested object gets a proper model class (CompanyAddress, CompanyPricing, TransportationCharge, CarrierFreightMarkups, FedExConfig, etc.). Maximum type safety, full autodoc coverage. Estimated ~50+ new sub-model classes across 15 response models.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - SDK Developer Trusts Endpoint Status (Priority: P1)

As an SDK developer, I need FIXTURES.md and progress reporting to reflect the **true** readiness of every endpoint so that I can trust the tracking documents and know exactly what work remains. Today, endpoints marked "complete" in FIXTURES.md may have models with missing fields (emitting warnings), tests that only assert `is not None`, and docs showing `Any` instead of the actual response type. "Complete" must mean complete across all four Constitution artifacts.

**Why this priority**: The entire SDK development pipeline depends on accurate status tracking. If "complete" is unreliable, developers waste time re-investigating endpoints they believe are done, and stakeholders receive false progress signals. This is the foundation for all other quality work.

**Independent Test**: Run the new quality-gate audit against every endpoint currently marked "complete" in FIXTURES.md. Each endpoint must pass all gates to retain "complete" status. Any failure demotes the endpoint to the appropriate incomplete status.

**Acceptance Scenarios**:

1. **Given** an endpoint marked "complete" in FIXTURES.md, **When** the quality-gate audit runs, **Then** the endpoint retains "complete" status only if ALL gates pass: (a) fixture exists and validates without warnings against the declared response model, (b) integration test asserts the response is an instance of the declared response model and produces zero model warnings, (c) fixture-validation test loads the fixture and validates without warnings, (d) Sphinx docs reference the correct response model (not `Any`).
2. **Given** `/companies/{id}/fulldetails` is currently marked "complete", **When** the audit runs, **Then** it is demoted because CompanyDetails is missing 7+ fields (address, accountInformation, pricing, insurance, finalMileTariff, taxes, readOnlyAccess) that produce warnings on construction from the fixture.
3. **Given** a new FIXTURES.md is generated, **When** a developer reads it, **Then** every endpoint row shows granular pass/fail per gate (model fidelity, test quality, fixture status, doc accuracy) rather than a single "complete" status.

---

### User Story 2 - Models Fully Represent API Reality (Priority: P1)

As an SDK consumer, I need Pydantic response models to declare all fields that the API actually returns so that I can access data like `company.address` without relying on undeclared `extra="allow"` passthrough and without seeing warnings in my logs.

**Why this priority**: The Constitution (Principle I) requires model fidelity. Models with missing fields produce `logger.warning` on every construction, polluting consumer logs and signaling that the SDK is out of sync with the API. This directly degrades the developer experience.

**Independent Test**: For every captured fixture, construct the response model from the fixture JSON and assert that zero warnings are emitted. Any fixture that triggers warnings indicates a model with missing fields.

**Acceptance Scenarios**:

1. **Given** the CompanyDetails fixture (captured from `/companies/{id}/fulldetails`), **When** `CompanyDetails.model_validate(fixture_data)` is called, **Then** zero warnings are emitted — all fields present in the fixture are declared in the model.
2. **Given** any captured fixture in `tests/fixtures/`, **When** validated against its declared response model, **Then** zero warnings are emitted. The complete list of models needing updates is tracked in the Model Warning Summary.
3. **Given** a model is updated to add missing fields, **When** the field types are chosen, **Then** the types match the actual API response data (validated by the fixture), not the swagger spec where it conflicts.

---

### User Story 3 - Tests Are Substantive and Enforceable (Priority: P1)

As a quality gatekeeper, I need every integration test and fixture-validation test to make substantive assertions — verifying the response is an instance of the declared model and that no warnings are emitted — so that "all tests pass" is a meaningful quality signal.

**Why this priority**: Tests that only assert `result is not None` provide no assurance of model correctness, field completeness, or API contract adherence. They pass when the response is a raw dict, a wrong model type, or a model that emits dozens of warnings. Substantive tests are the enforcement mechanism for Principles I and III.

**Independent Test**: Run the full test suite and verify that every endpoint with a captured fixture has a test that (a) asserts `isinstance(result, ExpectedModel)`, (b) captures warnings during model construction and asserts the warning count is zero, and (c) validates at least one domain-specific field beyond `id`.

**Acceptance Scenarios**:

1. **Given** the current `test_companies.py` with `assert result is not None`, **When** the new quality standard is applied, **Then** all four tests are rewritten to assert `isinstance(result, ExpectedModel)` and zero-warning construction.
2. **Given** the fixture-validation tests in `tests/models/`, **When** executed, **Then** each test captures warnings during `model_validate()` and asserts zero warnings. Tests for models with known missing fields initially fail (driving model updates).
3. **Given** a new endpoint is added with a captured fixture, **When** its test is written, **Then** the test template enforces instance checking and zero-warning validation by default.

---

### User Story 4 - Documentation Shows Correct Types and Model Structure (Priority: P2)

As a documentation reader, I need Sphinx docs to show the actual response model type (e.g., `CompanyDetails`) instead of `Any`, and I need a models reference section that shows model fields including nested structures like addresses so that I can understand what data the SDK returns.

**Why this priority**: Documentation showing `Any` as the return type is actively misleading — it tells consumers there is no structured model when one exists. The Constitution (Principle VI) requires comprehensive Sphinx docs. This story ensures docs match implementation reality.

**Independent Test**: Build the Sphinx docs and verify (a) every endpoint method's documented return type matches its declared `response_model`, (b) every response model has an autodoc page showing all fields with descriptions, (c) nested models (like address within CompanyDetails) are cross-referenced.

**Acceptance Scenarios**:

1. **Given** the Sphinx docs for the companies endpoint group, **When** built, **Then** `get_fulldetails()` shows return type `CompanyDetails` (not `Any`).
2. **Given** the models section of the docs, **When** a reader views CompanyDetails, **Then** they see all declared fields including `address`, `account_information`, `pricing`, etc., with field descriptions and types.
3. **Given** `make html` is run in `/docs/`, **Then** the build completes with zero warnings related to unresolved references or missing autodoc members.

---

### User Story 5 - Progress Dashboard Reflects Gate Status (Priority: P2)

As a project stakeholder, I need an HTML progress dashboard (`progress.html`) that shows every endpoint's status across all quality gates so that I can see at a glance how much work remains and where the gaps are.

**Why this priority**: A single "complete/incomplete" status hides the specific gap. A stakeholder needs to see which endpoints have models but no tests, which have tests but emit warnings, which have docs but wrong return types. This multi-dimensional view drives prioritization.

**Independent Test**: Generate `progress.html` and verify it shows per-endpoint rows with columns for each gate dimension (model fidelity, fixture captured, test quality, doc accuracy), with pass/fail indicators and summary statistics.

**Acceptance Scenarios**:

1. **Given** `progress.html` is generated, **When** a stakeholder views it, **Then** every tracked endpoint shows separate pass/fail indicators for: model exists, fixture captured, fixture validates without warnings, integration test is substantive, fixture-validation test exists, docs show correct return type.
2. **Given** the current state of the codebase (where many "complete" endpoints fail quality gates), **When** `progress.html` is generated for the first time with all gates enforced, **Then** the initial pass rates are low (reflecting true state), and the dashboard clearly shows what needs fixing.
3. **Given** a developer fixes a model (adding missing fields), **When** `progress.html` is regenerated, **Then** the model-fidelity gate flips from fail to pass for that endpoint.

---

### Edge Cases

- What happens when a fixture file exists but the response model class has been renamed or moved? The gate audit must report "model not found" rather than silently passing.
- How does the system handle endpoints that legitimately return no body (204 responses, fire-and-forget POSTs)? These endpoints are exempt from model-fidelity and fixture gates but still require test existence and documentation.
- What happens when an endpoint returns a `List[Model]` but the fixture is a single object? The gate must handle both single-object and list-of-objects fixture shapes.
- What happens when the model warning logging is configured at a different level? The gate must detect undeclared fields regardless of log configuration by inspecting the model's `__pydantic_extra__` directly rather than relying on log capture.
- How are endpoints with the `User` model handled, where the API returns a paginated wrapper (`{totalCount, data}`) instead of the flat model? The gate must flag response-shape mismatches (wrapper vs flat) as a distinct failure category.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST define a multi-dimensional quality gate for every tracked endpoint. The gate dimensions are: (G1) Model Fidelity — response model declares all fields from the captured fixture with zero warnings on validation; (G2) Fixture Status — fixture file exists in `tests/fixtures/` and was captured from a real API response; (G3) Test Quality — integration test asserts `isinstance(result, ExpectedModel)` and zero warnings; fixture-validation test loads fixture and asserts zero warnings; (G4) Documentation Accuracy — Sphinx docs show the correct return type and model autodoc page exists with all fields.
- **FR-002**: System MUST regenerate FIXTURES.md with per-gate pass/fail columns for every endpoint, replacing the single "complete/partial/needs-data" status with granular gate results. An endpoint is "complete" only when ALL gates pass.
- **FR-003**: System MUST update all response models that have entries in the "Model Warning Summary" (FIXTURES.md) to declare the missing fields with correct types derived from captured fixtures. All nested objects MUST become fully typed Pydantic sub-models at every nesting level (e.g., CompanyDetails.address becomes `Optional[CompanyAddress]`, CompanyAddress.coordinates becomes `Optional[Coordinates]`, CompanyDetails.pricing.transportationCharge becomes `Optional[TransportationCharge]`). No nested structure may remain as `Optional[dict]` when the fixture provides a clear schema. The initial set of top-level models includes: CompanyDetails, CompanySimple, ContactPrimaryDetails, ContactSimple, ContactTypeEntity, CountryCodeDto, FormsShipmentPlan, GlobalAccessorial, RatesState, SellerExpandedDto, ShipmentInfo, User, Web2LeadResponse, AddressIsValidResult, CalendarItem.
- **FR-004**: System MUST rewrite all integration tests that use trivial assertions (`assert result is not None`) to instead assert: (a) response is an instance of the declared model, (b) model construction produces zero warnings (validated via `__pydantic_extra__` being empty), (c) at least one domain-specific field is asserted.
- **FR-005**: System MUST rewrite all fixture-validation tests to capture and assert zero warnings during `model_validate()` and verify that the model's `__pydantic_extra__` dict is empty (no undeclared fields accepted via `extra="allow"`).
- **FR-006**: System MUST fix Sphinx documentation so that every endpoint method's documented return type reflects the actual response model, not `Any`. Every response model MUST have an autodoc page showing all declared fields with descriptions.
- **FR-007**: System MUST generate a `progress.html` dashboard that shows per-endpoint gate status across all dimensions, with summary statistics (total endpoints, per-gate pass rates, overall completion percentage).
- **FR-008**: System MUST provide a mechanism to regenerate FIXTURES.md and progress.html from the current codebase state (running a single command), so that status is always derivable from source artifacts rather than manually maintained.
- **FR-009**: System MUST ensure that the quality-gate definitions align with the Constitution's Four-Way Harmony principle (Principle III) and Model Fidelity principle (Principle I). The gate for "zero warnings" directly enforces the Constitution's requirement that extra fields MUST be logged via `logger.warning`.
- **FR-010**: System MUST handle endpoints that return no body (HTTP 204, fire-and-forget operations) by exempting them from model-fidelity and fixture gates while still requiring test existence and documentation.

### Key Entities

- **Quality Gate**: A set of pass/fail criteria applied to each endpoint. Dimensions: Model Fidelity (G1), Fixture Status (G2), Test Quality (G3), Documentation Accuracy (G4). An endpoint passes only when all applicable gates pass.
- **Endpoint Status Record**: Per-endpoint tracking row containing: endpoint path, HTTP method, request model, response model, and pass/fail for each gate dimension. Replaces the current single-status column.
- **Model Warning**: A record of fields present in a captured fixture but not declared in the response model. Each warning maps to a specific model class and lists the missing field names and their inferred types.
- **Progress Dashboard**: An HTML report aggregating all endpoint status records with visual pass/fail indicators, summary statistics, and filtering/sorting capabilities.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every endpoint currently marked "complete" in FIXTURES.md passes all applicable quality gates, or is demoted to accurately reflect its true status. Zero false "complete" entries remain.
- **SC-002**: All 15 models listed in the Model Warning Summary have their missing fields declared as fully typed Pydantic sub-models (no `Optional[dict]` for nested structures). Running `model_validate()` against every captured fixture produces zero warnings across the entire test suite. All sub-models are documented via Sphinx autodoc.
- **SC-003**: Every integration test makes substantive assertions (instance check + zero-warning validation). No integration test contains only `assert result is not None`.
- **SC-004**: Every fixture-validation test asserts zero `__pydantic_extra__` keys after model validation. No fixture-validation test passes while the model has undeclared fields.
- **SC-005**: Sphinx documentation builds with zero cross-reference warnings, every endpoint method shows its actual return type, and every response model has a complete field listing in the docs.
- **SC-006**: `progress.html` accurately reflects per-gate status for all 156 tracked endpoints and is regenerable from source artifacts via a single command.
- **SC-007**: FIXTURES.md reflects true multi-dimensional status and is regenerable from source artifacts, eliminating manual status maintenance that can drift from reality.

## Assumptions

- The existing `ResponseModel` base class with `extra="allow"` and `model_post_init` warning behavior is the correct pattern — the fix is to add missing fields to models, not to change the base class behavior.
- Captured fixtures in `tests/fixtures/` are trustworthy representations of real API responses (per Constitution Principle II, fabricated fixtures are prohibited).
- The `__pydantic_extra__` attribute on response models is the reliable mechanism for detecting undeclared fields — if it is non-empty after validation, the model is missing fields.
- Sphinx autodoc with the existing configuration (`autodoc_typehints: "description"`) will correctly render field types and descriptions when models are properly annotated. Fully typed sub-models will produce collapsible/cross-referenced field listings in the docs.
- Full-depth typing will produce an estimated ~50+ new sub-model classes across the 15 response models. Each sub-model follows the same ResponseModel conventions (extra="allow", camelCase aliases, Field descriptions).
- The progress.html generator in `scripts/generate_progress.py` can be extended to support multi-dimensional gate status rather than requiring a full rewrite.
- Endpoints with 106 "needs-fixture (new 008)" entries will initially fail most gates, which is the correct and expected behavior — this feature establishes the honest baseline.
