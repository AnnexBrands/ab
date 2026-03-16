# Tasks: Catalog Endpoint Params & Pagination

**Input**: Design documents from `/specs/035-catalog-endpoint-params/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Not explicitly requested — test tasks omitted. Existing tests must continue to pass.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish constants and ensure params models are correct before wiring

- [x] T001 Add catalog/seller/lot test constants to tests/constants.py (CATALOG_CUSTOMER_SELLER_ID=1103, CATALOG_CUSTOMER_CATALOG_ID=398425, TEST_LOT_ID, TEST_LOT_NUMBER, etc.)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Wire params_model validation into `_paginated_request()` per plan D2, so all filter kwargs are validated before HTTP calls

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T002 Update `_paginated_request()` in ab/api/base.py to resolve and validate query params against `route.params_model` using `model_cls.check()` — mirror the validation pattern from `_request()` lines 110-114
- [x] T003 Verify existing tests still pass after T002 (`cd src && pytest`)

**Checkpoint**: Foundation ready — params validation works for paginated endpoints

---

## Phase 3: User Story 1 — Full Filter Parameters on List Methods (Priority: P1) 🎯 MVP

**Goal**: Expose all swagger-defined filter parameters as typed keyword arguments on `catalog.list()`, `sellers.list()`, and `lots.list()` with IDE autocomplete and Pydantic validation.

**Independent Test**: Call `catalog.list(title="Fall 2026")` and verify the request sends `?Title=Fall+2026`.

### Implementation for User Story 1

Per plan D1: use explicit keyword arguments (not `**kwargs`). Per plan D4: rename `page` → `page_number` to match params models. Each method builds a params dict from kwargs, filters None values, and passes to `_paginated_request()`.

- [x] T004 [P] [US1] Expand `catalog.list()` signature in ab/api/endpoints/catalog.py: rename `page` → `page_number`, add kwargs for all CatalogListParams fields (id, customer_catalog_id, agent, title, start_date, end_date, is_completed, seller_ids, page_size, page_number), build params dict filtering None values, pass to `_paginated_request()`
- [x] T005 [P] [US1] Expand `sellers.list()` signature in ab/api/endpoints/sellers.py: rename `page` → `page_number`, add kwargs for all SellerListParams fields (id, name, customer_display_id, is_active, page_size, page_number), build params dict filtering None values, pass to `_paginated_request()`
- [x] T006 [P] [US1] Expand `lots.list()` signature in ab/api/endpoints/lots.py: rename `page` → `page_number`, add kwargs for all LotListParams fields (id, customer_item_id, lot_number, page_size, page_number), build params dict filtering None values, pass to `_paginated_request()`
- [x] T007 [US1] Run full test suite to confirm all existing tests pass and param validation works (`cd src && pytest`)

**Checkpoint**: All three list methods accept typed filter params with validation. MVP complete.

---

## Phase 4: User Story 2 — Pagination Navigation (Priority: P2)

**Goal**: Provide a standalone `paginate()` sync generator per plan D3 that yields all pages of any list endpoint without manual page tracking.

**Independent Test**: Call `paginate(api.catalog.list, page_size=10)` and iterate through all pages automatically.

### Implementation for User Story 2

Per plan D3: standalone generator in `ab/api/pagination.py`. Signature: `paginate(list_fn: Callable[..., PaginatedList[T]], **kwargs) -> Generator[PaginatedList[T], None, None]`. Sync-only (no async — SDK uses requests library).

- [x] T008 [US2] Create `ab/api/pagination.py` with standalone `paginate()` sync generator that accepts a list endpoint callable and filter kwargs, calls `list_fn(page_number=1, **kwargs)`, yields each PaginatedList page, increments page_number while `has_next_page` is True
- [x] T009 [US2] Export `paginate` from ab/api/__init__.py and ab/__init__.py so it is importable as `from ab import paginate`

**Checkpoint**: Standalone paginate helper works with any list endpoint.

---

## Phase 5: User Story 3 — Examples and Tests with Realistic Constants (Priority: P2)

**Goal**: Update examples and tests to use named constants for catalog/seller/lot IDs, demonstrating filter parameters with meaningful values. Run examples against staging to capture fixtures per Constitution II.

**Independent Test**: Run catalog/seller/lot examples and see filter constants used throughout, no magic numbers.

### Implementation for User Story 3

- [x] T010 [P] [US3] Update examples/catalog.py to import and use named constants from tests/constants.py and demonstrate at least one filter parameter in the list call (e.g., `catalog.list(title="...")` or `catalog.list(agent="...")`)
- [x] T011 [P] [US3] Update examples/sellers.py to import and use named constants from tests/constants.py and demonstrate a filter parameter in the list call (e.g., `sellers.list(is_active=True)`)
- [x] T012 [P] [US3] Update examples/lots.py to import and use named constants from tests/constants.py and demonstrate a filter parameter in the list call (e.g., `lots.list(customer_item_id="...")`)
- [x] T013 [US3] Audit all test files touching catalog/seller/lot for magic numbers and replace with named constants from tests/constants.py
- [ ] T014 [US3] Run examples against staging (requires live API access — deferred) API to capture filtered-response fixtures in tests/fixtures/ per Constitution II fixture capture loop

**Checkpoint**: Zero magic numbers for entity IDs in examples and tests. Filtered fixtures captured.

---

## Phase 6: User Story 4 — Docstrings on All Endpoint Methods (Priority: P3)

**Goal**: Add docstrings to every catalog/seller/lot endpoint method describing purpose, parameters with types, and return type per Constitution VI.

**Independent Test**: Hover over `catalog.list()` in an IDE and see all parameters documented.

### Implementation for User Story 4

- [x] T015 [P] [US4] Add docstrings to all methods in ab/api/endpoints/catalog.py (list, get, create, update, delete, bulk_insert) with one-line summary, parameter descriptions with types, and return types
- [x] T016 [P] [US4] Add docstrings to all methods in ab/api/endpoints/sellers.py (list, get, create, update, delete) with one-line summary, parameter descriptions with types, and return types
- [x] T017 [P] [US4] Add docstrings to all methods in ab/api/endpoints/lots.py (list, get, create, update, delete, get_overrides) with one-line summary, parameter descriptions with types, and return types

**Checkpoint**: All endpoint methods have complete docstrings visible in IDE hover.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Four-Way Harmony completion, final validation, and cleanup

- [x] T018 Update Sphinx docs for catalog/seller/lot endpoints and the new `paginate()` helper per Constitution III and VI
- [x] T019 Update FIXTURES.md to reflect filtered query fixture status for catalog/seller/lot list endpoints per Constitution V
- [x] T020 Run full test suite and linter (`cd src && pytest && ruff check .`)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Phase 2 — exposes params on method signatures
- **US2 (Phase 4)**: Depends on Phase 2 — paginate helper uses validated params; can run in parallel with US1
- **US3 (Phase 5)**: Depends on US1 (needs filter params in method signatures to demonstrate them)
- **US4 (Phase 6)**: Depends on US1 (needs final method signatures to document); can run in parallel with US3
- **Polish (Phase 7)**: Depends on all previous phases

### User Story Dependencies

- **US1 (P1)**: Depends on Phase 2 only — no story dependencies
- **US2 (P2)**: Depends on Phase 2 only — independent of US1
- **US3 (P2)**: Depends on US1 (needs typed filter params to demo in examples)
- **US4 (P3)**: Depends on US1 (needs final method signatures to document)

### Parallel Opportunities

- T004, T005, T006 can run in parallel (different endpoint files)
- T010, T011, T012 can run in parallel (different example files)
- T015, T016, T017 can run in parallel (different endpoint files)
- US1 and US2 can proceed in parallel after Phase 2
- US3 and US4 can proceed in parallel after US1

---

## Parallel Example: User Story 1

```
# Launch all endpoint signature expansions together:
T004: Expand catalog.list() in ab/api/endpoints/catalog.py
T005: Expand sellers.list() in ab/api/endpoints/sellers.py
T006: Expand lots.list() in ab/api/endpoints/lots.py
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001)
2. Complete Phase 2: Foundational (T002–T003)
3. Complete Phase 3: User Story 1 (T004–T007)
4. **STOP and VALIDATE**: All list methods accept typed filter kwargs with validation
5. This alone closes the biggest gap — all swagger params accessible from SDK

### Incremental Delivery

1. Setup + Foundational → params validation in paginated requests
2. US1 → typed filter kwargs on all list methods (MVP!)
3. US2 → paginate() helper for automatic page iteration
4. US3 → examples and tests use realistic named constants + fixture capture
5. US4 → docstrings complete the IDE discoverability story
6. Polish → Sphinx docs, FIXTURES.md, final validation pass
