# Tasks: Fix Catalog Model Typing

**Input**: Design documents from `/specs/033-fix-catalog-model-typing/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Foundational (New Models)

**Purpose**: Create the 4 new Pydantic response models required as nested types. These MUST exist before any type annotation changes.

- [x] T001 [P] Add LotCatalogInformationDto, LotCatalogDto, and ImageLinkDto response models to ab/api/models/lots.py — LotCatalogInformationDto has fields: id (int), lot_number (Optional[str]); LotCatalogDto has fields: catalog_id (int), lot_number (Optional[str]); ImageLinkDto has fields: id (int), link (Optional[str]). All inherit ResponseModel. Place BEFORE LotDto class definition so they can be referenced without forward refs within the same file. See data-model.md and research.md D8 for field specs.
- [x] T002 [P] Add CatalogDto response model to ab/api/models/catalog.py — fields: id (int), customer_catalog_id (Optional[str]), agent (Optional[str]), title (Optional[str]), start_date (datetime), end_date (datetime), is_completed (bool). Inherits ResponseModel. Place BEFORE CatalogWithSellersDto so it can be referenced. See data-model.md and research.md D8.
- [x] T003 Export new models from ab/api/models/__init__.py — add CatalogDto, LotCatalogInformationDto, LotCatalogDto, ImageLinkDto to the appropriate import lines and __all__ list.

**Checkpoint**: 4 new models exist and are importable. Run `python -c "from ab.api.models import CatalogDto, LotCatalogInformationDto, LotCatalogDto, ImageLinkDto"` to verify.

---

## Phase 2: User Story 1 + 2 — Type Annotations & Nested Validation (Priority: P1) 🎯 MVP

**Goal**: Replace all `List[dict]` and untyped `list` annotations on in-scope models with correct nested Pydantic model types. This delivers both IDE discoverability (US1) and Pydantic validation of nested structures (US2) simultaneously — the same code change achieves both.

**Independent Test**: Instantiate CatalogExpandedDto from fixture JSON and verify `isinstance(obj.sellers[0], SellerDto)` returns True.

### Implementation

- [x] T004 [P] [US1] Update LotDto field types in ab/api/models/lots.py — change `catalogs: Optional[list]` to `Optional[List[LotCatalogDto]]` and `image_links: Optional[list]` to `Optional[List[ImageLinkDto]]`. No new imports needed (same file). See research.md D6, D7.
- [x] T005 [US1] Update CatalogExpandedDto and CatalogWithSellersDto field types in ab/api/models/catalog.py — add `from __future__ import annotations` and `TYPE_CHECKING` guard importing SellerDto from sellers.py and LotCatalogInformationDto from lots.py. Change sellers fields to `Optional[List[SellerDto]]` and lots fields to `Optional[List[LotCatalogInformationDto]]`. Use string annotations for the TYPE_CHECKING imports. Add `model_rebuild()` calls after all classes if needed for deferred annotation resolution. See research.md D1-D4, D9, data-model.md import dependencies.
- [x] T006 [US1] Update SellerExpandedDto.catalogs field type in ab/api/models/sellers.py — add `from __future__ import annotations` and `TYPE_CHECKING` guard importing CatalogDto from catalog.py. Change `catalogs: Optional[List[dict]]` to `Optional[List[CatalogDto]]`. Add `model_rebuild()` call if needed. See research.md D5, D9.

**Checkpoint**: All in-scope `List[dict]` and untyped `list` annotations replaced. Run `python -m pytest tests/models/test_catalog_models.py -v` to verify fixture deserialization still works.

---

## Phase 3: User Story 3 — Test Compatibility & Validation (Priority: P2)

**Goal**: Ensure all existing tests pass after the type changes and add isinstance checks to verify nested objects are proper Pydantic model instances.

**Independent Test**: `python -m pytest tests/ -v` passes with zero failures.

### Implementation

- [x] T007 [US3] Run full test suite and fix any fixture/test incompatibilities — execute `python -m pytest tests/ -v` from repo root. If CatalogExpandedDto fixture deserialization fails (e.g., nested seller objects don't match SellerDto fields), update the fixture JSON to include required fields OR adjust model field optionality. Document any fixture changes. See spec.md edge cases for null/empty list handling.
- [x] T008 [US3] Add isinstance assertions to test_catalog_expanded_dto in tests/models/test_catalog_models.py — after existing fixture validation, add checks that `sellers[0]` is instance of SellerDto (if sellers not empty) and `lots[0]` is instance of LotCatalogInformationDto (if lots not empty). Import the new model types. See spec.md SC-004.
- [x] T009 [US3] Verify no remaining `List[dict]` on in-scope models — grep ab/api/models/catalog.py, ab/api/models/sellers.py, ab/api/models/lots.py for `List[dict]` and untyped `list` on response model fields. Confirm zero matches on CatalogExpandedDto, CatalogWithSellersDto, SellerExpandedDto, and LotDto. See spec.md SC-001.

**Checkpoint**: Full test suite passes. All in-scope models have zero `List[dict]` remaining.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and cleanup.

- [x] T010 Run `ruff check .` from ab/ directory and fix any linting issues introduced by new models or import changes.
- [x] T011 Verify Pydantic model_rebuild() is called correctly for cross-file TYPE_CHECKING imports — test with `python -c "from ab.api.models import CatalogExpandedDto; print(CatalogExpandedDto.model_fields['sellers'].annotation)"` and confirm it resolves to the correct type, not a string.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Foundational (Phase 1)**: No dependencies — can start immediately
- **US1+US2 (Phase 2)**: Depends on Phase 1 (new models must exist before they can be referenced)
- **US3 (Phase 3)**: Depends on Phase 2 (type changes must be in place before tests validate them)
- **Polish (Phase 4)**: Depends on Phase 3

### Within Phase Parallelism

- **Phase 1**: T001 and T002 can run in parallel (different files). T003 depends on T001+T002.
- **Phase 2**: T004 can run in parallel with T005 (different files). T006 can run in parallel with T004 (different files). T005 and T006 are independent.
- **Phase 3**: T007 must run first. T008 and T009 can run after T007.

### Parallel Opportunities

```
Phase 1 parallel:
  T001 (lots.py new models) || T002 (catalog.py new model)
  → T003 (exports)

Phase 2 parallel:
  T004 (lots.py types) || T005 (catalog.py types) || T006 (sellers.py types)

Phase 3 sequential:
  T007 (run tests) → T008 (isinstance checks) || T009 (grep verification)
```

---

## Implementation Strategy

### MVP First (Phase 1 + Phase 2)

1. Complete Phase 1: Create 4 new models
2. Complete Phase 2: Update type annotations
3. **STOP and VALIDATE**: Run `python -m pytest tests/models/test_catalog_models.py -v`
4. Both US1 (IDE discoverability) and US2 (Pydantic validation) are delivered

### Full Delivery

1. Phase 1 + 2 → MVP complete
2. Phase 3 → Full test validation + isinstance assertions
3. Phase 4 → Linting and model_rebuild verification

---

## Notes

- [P] tasks = different files, no dependencies
- US1 and US2 share the same implementation (type annotation changes deliver both)
- No new test files created — existing test_catalog_models.py is extended
- TYPE_CHECKING imports + `from __future__ import annotations` pattern avoids circular imports at runtime
- model_rebuild() may be needed at module level for Pydantic v2 to resolve string annotations from TYPE_CHECKING
- Existing fixtures may need field adjustments if nested objects don't match the now-strict model types
