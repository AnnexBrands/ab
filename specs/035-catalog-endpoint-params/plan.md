# Implementation Plan: Catalog Endpoint Params & Pagination

**Branch**: `035-catalog-endpoint-params` | **Date**: 2026-03-16 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/035-catalog-endpoint-params/spec.md`

## Summary

Expose all swagger-defined query parameters as typed keyword arguments on `catalog.list()`, `sellers.list()`, and `lots.list()`, with Pydantic validation via the existing params models. Add a standalone `paginate()` generator for automatic page iteration. Update examples/tests to use named constants. Add docstrings to all catalog/seller/lot endpoint methods.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: pydantic>=2.0, requests (existing SDK deps — no new dependencies)
**Storage**: N/A — SDK, no local storage
**Testing**: pytest (existing)
**Target Platform**: Python library (pip install ab)
**Project Type**: Library
**Constraints**: Sync-only (requests library, no async)
**Scale/Scope**: 3 endpoint files, 3 model files, 1 new helper module, 3 example files

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | PASS | Params models (CatalogListParams, SellerListParams, LotListParams) already exist as RequestModel with extra="forbid", snake_case fields, camelCase aliases |
| II. Example-Driven Fixture Capture | PASS | Examples will be updated to use filter params and run against staging for fixture capture |
| III. Four-Way Harmony | PASS | Will update all four artifacts: implementation, examples, fixtures/tests, Sphinx docs |
| IV. Swagger-Informed, Reality-Validated | PASS | Params models already derived from swagger; will validate against real API responses |
| V. Endpoint Status Tracking | PASS | FIXTURES.md will be updated for filtered query fixtures |
| VI. Documentation Completeness | PASS | Docstrings added to all endpoint methods (US4); Sphinx docs updated in polish phase |
| VII. Flywheel Evolution | N/A | Enhancement feature, not a new pattern |
| VIII. Phase-Based Context Recovery | PASS | tasks.md uses checkbox format; work organized in phases with checkpoints |
| IX. Endpoint Input Validation | PASS | Core goal of this feature: wire params_model validation into _paginated_request() |

## Project Structure

### Documentation (this feature)

```text
specs/035-catalog-endpoint-params/
├── plan.md              # This file
├── spec.md              # Feature specification
├── checklists/          # Generated checklists
└── tasks.md             # Task list
```

### Source Code (repository root)

```text
ab/
├── api/
│   ├── base.py              # MODIFY: _paginated_request() params validation
│   ├── pagination.py        # NEW: standalone paginate() generator
│   ├── __init__.py          # MODIFY: export paginate
│   ├── endpoints/
│   │   ├── catalog.py       # MODIFY: expand list() signature, add docstrings
│   │   ├── sellers.py       # MODIFY: expand list() signature, add docstrings
│   │   └── lots.py          # MODIFY: expand list() signature, add docstrings
│   └── models/
│       ├── catalog.py       # EXISTING: CatalogListParams (10 fields)
│       ├── sellers.py       # EXISTING: SellerListParams (6 fields)
│       └── lots.py          # EXISTING: LotListParams (5 fields)
├── __init__.py              # MODIFY: export paginate

tests/
├── constants.py             # MODIFY: add catalog/seller/lot test constants

examples/
├── catalog.py               # MODIFY: use filter params + named constants
├── sellers.py               # MODIFY: use filter params + named constants
└── lots.py                  # MODIFY: use filter params + named constants
```

**Structure Decision**: Single-project library structure (existing). No new directories except `ab/api/pagination.py` module.

## Design Decisions

### D1: Expand list() signatures with explicit keyword arguments

**Decision**: Add all params model fields as explicit keyword arguments to `list()` methods, not `**kwargs`.

**Rationale**: Explicit kwargs provide IDE autocomplete, type checking, and self-documenting signatures. The existing `**kwargs` pattern from feature 007 is for the request layer plumbing; the user-facing method signatures should enumerate all parameters.

**Implementation**: Each list method constructs a params dict from its explicit kwargs, filtering out `None` values, then passes `params=dict` to `_paginated_request()`.

### D2: Wire params validation into _paginated_request()

**Decision**: Add params model validation to `_paginated_request()` in `base.py`, mirroring what `_request()` already does.

**Rationale**: Currently `_paginated_request()` bypasses `route.params_model` validation entirely — it calls `self._client.request()` directly instead of going through `_request()`. This means any params dict passed to paginated endpoints is never validated against the Pydantic model. Wiring validation here ensures all filter params are validated before the HTTP call (FR-004, Constitution IX).

**Alternative rejected**: Having `_paginated_request()` delegate to `_request()` — this would require refactoring the response parsing logic since `_request()` handles response model casting differently than pagination.

### D3: Standalone paginate() generator

**Decision**: Implement `paginate()` as a standalone generator function in `ab/api/pagination.py` that accepts a callable (the list method) and filter kwargs, yielding `PaginatedList` pages.

**Rationale**: Spec clarification explicitly chose this over methods on PaginatedList (FR-008: PaginatedList stays data-only). A standalone generator keeps the pagination model clean and works with any list endpoint.

**Signature**:
```python
def paginate(
    list_fn: Callable[..., PaginatedList[T]],
    **kwargs: Any,
) -> Generator[PaginatedList[T], None, None]:
```

The generator calls `list_fn(page_number=1, **kwargs)`, yields the result, increments page_number while `has_next_page` is True.

### D4: Param name mapping — page vs page_number

**Decision**: Rename existing `page` parameter to `page_number` in method signatures to match the params model field name (`CatalogListParams.page_number`).

**Rationale**: Consistency between the method signature and the underlying params model eliminates confusion. The API parameter is `PageNumber` (PascalCase alias), the Python field is `page_number`, so the kwarg should also be `page_number`.

**Breaking change note**: This renames `page` → `page_number` on all three list methods. Callers using `page=` will need to update to `page_number=`.

### D5: Request body validation already handled

**Decision**: FR-011 (request body validation on create/update) is already satisfied by existing code.

**Rationale**: `_request()` in `base.py` (lines 103-107) already validates outbound JSON bodies against `route.request_model` when present. All create/update routes define `request_model`. No additional work needed — just verify in testing.

## Complexity Tracking

No constitution violations to justify.
