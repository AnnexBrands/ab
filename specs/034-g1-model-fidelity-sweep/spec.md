# Feature Specification: G1 Model Fidelity Sweep

**Feature Branch**: `034-g1-model-fidelity-sweep`
**Created**: 2026-03-15
**Status**: Draft
**Input**: User description: "bring G1 current with G2. check that examples, tests, sphinx docs are all complete."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Close G1 Gap for All G2-Passing Endpoints (Priority: P1)

An SDK maintainer wants every endpoint that already has a captured fixture (G2 pass) to also pass G1 (model fidelity). Currently **21 endpoints** have fixtures on disk but their response models are incomplete — `__pydantic_extra__` reports undeclared fields. The maintainer expands each model to declare all fields present in the fixture, eliminating extra-field warnings and achieving G1 parity with G2.

**Why this priority**: G1 is the foundation — typed models are the SDK's core value proposition. Every fixture that exposes undeclared fields is a drift bug waiting to surface at runtime.

**Independent Test**: Run the gate evaluation for all 21 endpoints; each must report G1=pass. The gate baseline ratchet test must pass with the updated baseline.

**Acceptance Scenarios**:

1. **Given** an endpoint passes G2 but not G1, **When** the model is expanded to declare all fixture fields, **Then** `__pydantic_extra__` is empty when validating the fixture and the gate evaluator reports G1=pass.
2. **Given** all 21 gap endpoints have been expanded, **When** the full gate regression test runs, **Then** G1 pass count rises from 71 to at least 92 (71 + 21) with zero regressions on other gates.
3. **Given** a model expansion adds new fields, **When** field names and types are chosen, **Then** they match the swagger schema definition (alias, type, optionality).

---

### User Story 2 - Verify Test Coverage for Expanded Models (Priority: P2)

An SDK maintainer wants every expanded model to have a fixture-validation test that asserts `isinstance()` and checks `__pydantic_extra__` is empty, ensuring G3 passes for all newly-G1-compliant endpoints.

**Why this priority**: Expanding models without tests means drift can silently reappear. Tests lock in the fidelity gains.

**Independent Test**: Run `pytest tests/models/` — every expanded endpoint has at least one test that loads its fixture, validates the model, and asserts no extra fields.

**Acceptance Scenarios**:

1. **Given** an endpoint model was expanded in this feature, **When** `pytest tests/models/` runs, **Then** a test exists that loads the fixture, calls `model_validate`, and asserts `assert_no_extra_fields`.
2. **Given** a model has nested sub-models, **When** the test runs, **Then** nested models are also validated for extra fields.

---

### User Story 3 - Verify Example Script Coverage (Priority: P3)

An SDK maintainer wants to confirm that example scripts exist for all endpoint groups affected by this sweep and that they demonstrate the expanded models without errors.

**Why this priority**: Examples are the primary onboarding tool. If expanded models aren't exercised in examples, users won't discover the new fields.

**Independent Test**: Review examples directory — each endpoint group touched by this feature has a corresponding example script that imports and uses the expanded models.

**Acceptance Scenarios**:

1. **Given** a model was expanded in an endpoint group (payments, shipments, timeline, etc.), **When** the corresponding example script is checked, **Then** it imports the expanded model and runs without import errors.
2. **Given** no example script exists for an affected endpoint group, **When** the gap is identified, **Then** a new example script is created or the existing one is updated.

---

### User Story 4 - Verify Sphinx Documentation Completeness (Priority: P3)

An SDK maintainer wants Sphinx autodoc pages to reflect all expanded models with complete field documentation, so API users can discover new fields via the generated docs.

**Why this priority**: Docs are the second discovery path after IDE autocomplete. Incomplete docs undermine the value of typed models.

**Independent Test**: Run `sphinx-build` — all expanded models appear in the generated docs with field descriptions, and no build warnings reference missing models.

**Acceptance Scenarios**:

1. **Given** a new model was added (e.g., nested sub-model), **When** Sphinx builds, **Then** the model appears in the appropriate docs page with all fields documented.
2. **Given** an existing model was expanded with new fields, **When** Sphinx builds, **Then** the new fields appear in the model's doc page.
3. **Given** all models are documented, **When** `sphinx-build` runs, **Then** zero warnings reference undefined or missing model cross-references.

---

### Edge Cases

- What happens when a fixture contains fields not present in the swagger schema (API returns undocumented fields)? — Treat as Optional fields with a comment noting they are undocumented; do not suppress with `model_config` extras.
- What happens when a fixture field has an ambiguous type (null in all samples)? — Type as `Optional[str]` (most common default) with a comment noting the assumption.
- What happens when expanding a model would break an existing test that asserts on the old field set? — Update the test to match the expanded model; the gate baseline ratchet prevents regression.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST expand response models for all 21 endpoints that currently pass G2 but fail G1, declaring every field present in the captured fixture.
- **FR-002**: Each expanded field MUST use the correct alias matching the JSON key from the swagger schema / fixture.
- **FR-003**: Each expanded field MUST use the correct Python type corresponding to the swagger schema type (string→str, integer→int, number→float, boolean→bool, object→nested model or dict, array→List).
- **FR-004**: All new fields MUST be Optional with a default of None, consistent with existing SDK conventions.
- **FR-005**: Where fixtures contain nested objects with 3+ fields, system MUST create typed sub-models rather than using `dict`.
- **FR-006**: System MUST update the gate baseline file to reflect newly-passing gates.
- **FR-007**: System MUST add fixture-validation tests for every expanded model (load fixture → validate → assert no extra fields).
- **FR-008**: System MUST verify that example scripts exist for each affected endpoint group and update them to reference expanded models where needed.
- **FR-009**: System MUST verify Sphinx docs build without warnings for all expanded models.
- **FR-010**: System MUST export all new models from the models package and include them in `__all__`.

### Key Entities

- **Response Model**: A pydantic model representing an API response payload — the primary artifact being expanded.
- **Gate Baseline**: JSON file mapping each endpoint to its list of passing quality gates — must be updated as endpoints gain G1.
- **Fixture**: Captured JSON response from the live API — the source of truth for which fields a model must declare.

### Affected Endpoints (21)

The following endpoints pass G2 but not G1:

1. `/commodity-map/{_} DELETE`
2. `/job/{_}/changeAgent POST`
3. `/job/{_}/item/notes POST`
4. `/job/{_}/item/{_} PUT`
5. `/job/{_}/parcelitems/{_} DELETE`
6. `/job/{_}/payment/ACHCreditTransfer POST`
7. `/job/{_}/payment/attachCustomerBank POST`
8. `/job/{_}/payment/banksource POST`
9. `/job/{_}/payment/bysource POST`
10. `/job/{_}/payment/cancelJobACHVerification POST`
11. `/job/{_}/payment/verifyJobACHSource POST`
12. `/job/{_}/shipment DELETE`
13. `/job/{_}/shipment/accessorial POST`
14. `/job/{_}/shipment/accessorial/{_} DELETE`
15. `/job/{_}/shipment/book POST`
16. `/job/{_}/shipment/exportdata POST`
17. `/job/{_}/status/quote POST`
18. `/job/{_}/timeline/incrementjobstatus POST`
19. `/job/{_}/timeline/undoincrementjobstatus POST`
20. `/job/{_}/timeline/{_} DELETE`
21. `/views/{_} DELETE`

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 21 G2-but-not-G1 endpoints pass G1 after model expansion (G1 count rises from 71 to ≥92).
- **SC-002**: Zero gate regressions — no endpoint loses a previously-passing gate.
- **SC-003**: Every expanded model has at least one fixture-validation test that passes.
- **SC-004**: Example scripts exist for all affected endpoint groups and execute without import errors.
- **SC-005**: Sphinx docs build completes with zero warnings referencing expanded or new models.
- **SC-006**: Full test suite passes with no new failures or skips attributable to this feature.

## Assumptions

- Captured fixtures accurately represent the current API response structure.
- The swagger schema is the authoritative source for field names, types, and aliases when fixtures are ambiguous.
- All new fields follow the existing convention: `Optional[T] = Field(None, alias="camelCase", description="...")`.
- Payment, shipment, and timeline endpoint groups already have example scripts; these may need updates but not full rewrites.

## Dependencies

- Feature 033 (freight provider model expansion) must be merged or rebased — it establishes the pattern this feature follows at scale.
- Gate evaluation infrastructure (feature 028) must be functional — used to verify G1 pass status.

## Scope Boundaries

**In scope**: Expanding existing models to declare all fixture fields; adding tests, updating examples and docs for the 21 gap endpoints.

**Out of scope**: Capturing new fixtures for endpoints that lack them (G2 failures); expanding models beyond what fixtures prove; refactoring gate infrastructure; CLI tooling changes.
