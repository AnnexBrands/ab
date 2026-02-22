# Research: Endpoint Quality Gates

**Date**: 2026-02-21
**Feature**: 011-endpoint-quality-gates

## R1: Return Type Annotation Strategy

**Decision**: Fix endpoint method return types from `-> Any` to actual model types.

**Rationale**: All endpoint methods currently declare `-> Any` (e.g., `def get_fulldetails(...) -> Any`). The actual return types are declared in `Route.response_model` strings and resolved at runtime in `BaseEndpoint._request()`. Sphinx autodoc reads method annotations, so `-> Any` propagates to docs. Fixing requires adding proper return type annotations to every endpoint method.

**Alternatives considered**:
- Sphinx autodoc override (`:rtype:` directive) — Rejected: diverges annotation from reality, manual maintenance.
- Custom Sphinx extension to read Route objects — Rejected: over-engineered, fragile.
- **Chosen**: Add proper return type annotations to endpoint methods (e.g., `-> CompanyDetails`). This is the simplest fix and provides IDE autocompletion as a bonus.

## R2: Extra Field Detection Mechanism

**Decision**: Use `model.__pydantic_extra__` (Pydantic v2) as the canonical detection mechanism for undeclared fields.

**Rationale**: `ResponseModel` uses `extra="allow"` and logs warnings in `model_post_init()` via `self.model_extra.keys()`. The `model_extra` property returns the same dict as `__pydantic_extra__`. Checking `model.__pydantic_extra__` is deterministic and doesn't require log capture. Tests should assert `not model.__pydantic_extra__` (empty dict = no undeclared fields).

**Alternatives considered**:
- Capture log warnings during model construction — Rejected: depends on logger configuration, fragile.
- **Chosen**: Direct `__pydantic_extra__` check is reliable regardless of log level.

## R3: Sub-Model Count Estimate

**Decision**: ~30-35 new sub-model classes needed across 15 top-level models.

**Breakdown by complexity**:

| Model | Sub-models Needed | Complexity |
|-------|-------------------|-----------|
| CompanyDetails | ~20 | Very High — address, accountInfo (10 carrier sub-models), pricing (7 sub-objects), insurance, taxes, tariff |
| ContactPrimaryDetails | ~5 | High — company object has nested mainAddress, companyInfo, overridableAddressData |
| GlobalAccessorial | 2 | Medium — options with radioButtonOptions |
| ShipmentInfo | 1 | Low — Weight sub-model |
| SellerExpandedDto | 0 | Low — paginated wrapper (PaginatedList already exists) |
| User | 0 | Low — paginated wrapper + field additions |
| Web2LeadResponse | 0 | Low — existing Web2LeadGETResult already handles nesting |
| Others (8 models) | 0 | Flat — only scalar field additions |

**Shared sub-models** (reusable across models):
- `Coordinates` (lat/lon) — used in CompanyDetails.address, ContactPrimaryDetails.address
- `Address` — used in CompanyDetails, ContactPrimaryDetails
- These should live in a shared module (e.g., `ab/api/models/common.py`)

## R4: Progress Module Architecture

**Decision**: Extend existing `ab.progress` module rather than rewrite.

**Current architecture**:
- `models.py` — `Endpoint`, `EndpointGroup`, `Fixture`, `ActionItem` dataclasses
- `parsers.py` — Parses `api-surface.md` and `FIXTURES.md`
- `scanner.py` — Scans fixture files and constants
- `renderer.py` — HTML generation with CSS styling
- `instructions.py` — Builds step-by-step instructions per endpoint
- `generate_progress.py` — Orchestration script

**Extension plan**: Add gate dimensions to `Endpoint`/`Fixture` dataclasses. Add gate evaluation functions. Extend renderer with per-gate columns. Add FIXTURES.md generation alongside HTML.

## R5: FIXTURES.md Generation Strategy

**Decision**: Generate FIXTURES.md from source artifacts while preserving hand-maintained Notes.

**Rationale**: Current FIXTURES.md has hand-maintained Notes like "HTTP 500 on staging — needs company UUID with populated details." These contain institutional knowledge about what's blocking each endpoint. The generator should:
1. Scan source code for Route definitions → extract endpoint paths, methods, models
2. Scan `tests/fixtures/` for existing files → determine fixture status
3. Evaluate gate criteria programmatically → determine per-gate pass/fail
4. Read existing FIXTURES.md Notes column → preserve
5. Output updated FIXTURES.md with gate columns + preserved notes

## R6: User Model Paginated Wrapper

**Decision**: Create `UserListResponse` wrapper model. Update endpoint to use `_paginated_request()`.

**Rationale**: The `/users/list` endpoint returns `{totalCount, data: [...]}` but the current Route declares `response_model="User"`. The fixture confirms this mismatch. The existing `_paginated_request()` method in `BaseEndpoint` already handles paginated responses using `PaginatedList`. The fix is: (a) update the endpoint method to use `_paginated_request()`, (b) update the `User` model to add the 18+ missing fields from the fixture.

## R7: Integration Test Pattern

**Decision**: Standard test pattern for substantive assertions.

**Pattern**:
```python
def test_get_fulldetails(self, api):
    result = api.companies.get_fulldetails(LIVE_COMPANY_UUID)
    assert isinstance(result, CompanyDetails)
    assert not result.__pydantic_extra__, (
        f"Undeclared fields: {list(result.__pydantic_extra__)}"
    )
    assert result.id is not None
```

**Key elements**:
1. `isinstance` check — verifies the endpoint returned the correct model type
2. `__pydantic_extra__` check — verifies no undeclared fields (model fidelity)
3. Domain-specific assertion — verifies meaningful data was returned

## R8: Fixture Validation Test Pattern

**Decision**: Standard test pattern for zero-warning fixture validation.

**Pattern**:
```python
def test_company_details(self):
    data = require_fixture("CompanyDetails", "GET", "/companies/{id}/fulldetails", required=True)
    model = CompanyDetails.model_validate(data)
    assert not model.__pydantic_extra__, (
        f"CompanyDetails has undeclared fields: {list(model.__pydantic_extra__)}"
    )
    assert model.id is not None
```
