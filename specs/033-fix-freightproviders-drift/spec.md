# Feature Specification: Fix FreightProviders Drift

**Feature Branch**: `033-fix-freightproviders-drift`
**Created**: 2026-03-15
**Status**: Draft
**Input**: User description: "progress.html states get freightproviders is 100% passing gates, but cli abs job list_freight_providers 2000000 gives warning output response has extra fields not in model. Then under tier2 in progress get_freightproviders says not started. fix drift on progress artifacts vs reality, and target this endpoint for complete tests, docs, examples, models, and updated progress."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Accurate Response Model (Priority: P1)

A developer calls `list_freight_providers` via the SDK or CLI and receives the full API response with no "extra fields not in model" warnings. Every field returned by the live API is captured in the `PricedFreightProvider` response model with correct types and aliases.

**Why this priority**: The model is the foundation — tests, docs, fixtures, and gate evaluations all depend on a faithful model. Currently the model has only 3 stub fields while the live API returns many more, causing runtime warnings that erode trust in the SDK.

**Independent Test**: Call `api.jobs.list_freight_providers(<jobId>)` against a live environment and confirm no extra-field warnings are emitted and all returned fields are accessible as typed attributes.

**Acceptance Scenarios**:

1. **Given** a live API response for GET /job/{id}/freightproviders, **When** the response is validated against `PricedFreightProvider`, **Then** zero extra-field warnings are produced.
2. **Given** the updated model, **When** a developer inspects `PricedFreightProvider` in their IDE, **Then** every field has a type annotation, alias, and description.
3. **Given** the `ShipmentPlanProvider` and `RateQuoteRequest` request models, **When** compared to the API's accepted payloads, **Then** all accepted fields are represented with correct types.

---

### User Story 2 - Realistic Fixtures and Passing Tests (Priority: P1)

The response fixture `PricedFreightProvider.json` contains a realistic, populated payload (not an empty list) captured from the live API. All model-validation tests exercise real data and pass without skipping.

**Why this priority**: An empty fixture (`[]`) allows tests to pass trivially and masks model gaps — this is the mechanism by which the drift went undetected.

**Independent Test**: Run `pytest tests/models/test_freight_models.py` and confirm all assertions execute against populated data with no skips.

**Acceptance Scenarios**:

1. **Given** the fixture file `tests/fixtures/PricedFreightProvider.json`, **When** opened, **Then** it contains at least one fully populated freight-provider object.
2. **Given** the updated fixture, **When** `PricedFreightProvider.model_validate(item)` runs, **Then** it succeeds with no extra-field warnings and no validation errors.
3. **Given** request fixtures for `ShipmentPlanProvider`, `RateQuoteRequest`, and `FreightProvidersParams`, **When** opened, **Then** they contain realistic non-null values.

---

### User Story 3 - Consistent Progress Artifacts (Priority: P1)

All progress tracking artifacts — `api-surface.md`, `FIXTURES.md`, and `progress.html` — agree on the implementation status of the three freightproviders endpoints. No endpoint is simultaneously reported as "complete" in one artifact and "not started" in another.

**Why this priority**: Contradictory progress data undermines planning and prioritization decisions. The `api-surface.md` currently says "AB done: 0 of 3" while `FIXTURES.md` says all gates pass — this must be reconciled.

**Independent Test**: Regenerate `progress.html` and `FIXTURES.md` and confirm the freightproviders entries are internally consistent and match reality.

**Acceptance Scenarios**:

1. **Given** the corrected `api-surface.md`, **When** the freightproviders section is read, **Then** it reflects the actual implementation status (done count matches implemented endpoints).
2. **Given** the regenerated `FIXTURES.md`, **When** gate columns are evaluated, **Then** gates that were falsely passing (due to empty fixtures) now reflect true status.
3. **Given** the regenerated `progress.html`, **When** the freightproviders group is viewed, **Then** tier classification matches reality — no "not started" labels for implemented endpoints.

---

### User Story 4 - Updated Documentation and Examples (Priority: P2)

The runnable example in `examples/freight_providers.py` exercises the updated models and the generated Sphinx docs reflect the complete model fields.

**Why this priority**: Docs and examples are the public face of the endpoint — they should demonstrate the full capability once the model is correct.

**Independent Test**: Run the freight_providers example script and confirm it executes without warnings; build docs and confirm `PricedFreightProvider` shows all fields.

**Acceptance Scenarios**:

1. **Given** the updated example script, **When** executed against a live environment, **Then** it completes without extra-field warnings.
2. **Given** the Sphinx docs, **When** the `PricedFreightProvider` page is viewed, **Then** all model fields are documented with types and descriptions.

---

### Edge Cases

- What happens when the live API adds new fields in the future? Extra-field warnings should flag them for model updates without causing hard failures.
- What happens when the API returns an empty list (no freight providers for a job)? Tests should handle both populated and empty responses.
- What if `ShipmentPlanProvider` or `RateQuoteRequest` request bodies have undocumented optional fields? Capture what the API accepts and document assumptions.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The `PricedFreightProvider` response model MUST include every field returned by the live API for GET /job/{id}/freightproviders, with correct types, aliases, and descriptions.
- **FR-002**: The `ShipmentPlanProvider` and `RateQuoteRequest` request models MUST include all fields accepted by their respective endpoints.
- **FR-003**: The response fixture `PricedFreightProvider.json` MUST contain at least one fully populated object captured from the live API.
- **FR-004**: Request fixtures (`ShipmentPlanProvider.json`, `RateQuoteRequest.json`, `FreightProvidersParams.json`) MUST contain realistic, non-null sample values.
- **FR-005**: Model validation tests MUST exercise real fixture data and assert zero extra-field warnings.
- **FR-006**: The `api-surface.md` endpoint group "Job — Freight Providers" MUST show an accurate "AB done" count matching reality.
- **FR-007**: After regeneration, `FIXTURES.md` gate columns for freightproviders endpoints MUST reflect true pass/fail status based on the updated models and fixtures.
- **FR-008**: After regeneration, `progress.html` MUST show consistent status for freightproviders endpoints with no contradictory tier classifications.
- **FR-009**: The runnable example `examples/freight_providers.py` MUST work with the updated models without extra-field warnings.
- **FR-010**: Sphinx documentation MUST reflect all fields in the updated response and request models.

### Key Entities

- **PricedFreightProvider**: Response model for GET freightproviders — represents a freight carrier option with pricing, service types, and availability details. Currently has 3 stub fields; must be expanded to match the full API response.
- **ShipmentPlanProvider**: Request model for POST freightproviders — represents a freight provider selection to save. Currently has 1 stub field.
- **RateQuoteRequest**: Request model for POST freightproviders/{optionIndex}/ratequote — represents parameters for a rate quote request. Currently has 1 stub field.
- **FreightProvidersParams**: Query parameter model for GET freightproviders — filter parameters. Has 3 fields (provider_indexes, shipment_types, only_active).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Calling `list_freight_providers` via CLI or SDK against a live environment produces zero "extra fields not in model" warnings.
- **SC-002**: All model validation tests for freight provider models pass with populated fixture data (no trivial empty-list skips).
- **SC-003**: The freightproviders section in `api-surface.md`, `FIXTURES.md`, and `progress.html` all report the same implementation status with no contradictions.
- **SC-004**: Quality gates G1 through G6 for all three freightproviders endpoints pass legitimately (backed by real fixture data, not empty lists).
- **SC-005**: The runnable example completes successfully without warnings when executed against a live environment.

## Assumptions

- The live API response structure for GET /job/{id}/freightproviders can be captured by running the existing example or CLI command against a test environment.
- The `PricedFreightProvider` model expansion will be based on the actual API response shape observed at capture time; if the API evolves, follow-up updates may be needed.
- The `api-surface.md` "AB done" counter is a manually maintained field that must be updated by hand (not auto-generated).
- Request model fields for POST endpoints will be inferred from API documentation or by inspecting accepted payloads, and documented as assumptions where official documentation is unavailable.
