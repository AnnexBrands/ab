# Tasks: Response Model Rigor

**Input**: Design documents from `/specs/017-response-model-rigor/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Not explicitly requested. Existing test suite (307+ passed) must remain green. One new test file for fixture completeness gate.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Understand current state and verify baseline

- [X] T001 Read `ab/api/base.py` to understand the current `_request` method logic, specifically lines 86-99 (list handling branch). Read the contracts `contracts/list-unwrap.md` and `contracts/fixture-completeness.md` for the target behavior.

- [X] T002 Run `pytest tests/ --tb=short -q` to establish baseline test count. Confirm all existing tests pass before making changes.

**Checkpoint**: Baseline established. Current bug behavior understood.

---

## Phase 2: Foundational

**Purpose**: No foundational/blocking tasks needed — each user story modifies independent files.

**Checkpoint**: Proceed directly to user stories.

---

## Phase 3: User Story 1 — Silent Dict Return Bug (Priority: P1) 🎯 MVP

**Goal**: Fix `BaseEndpoint._request` so that when `response_model="List[X]"` and the API returns a dict wrapper, the SDK unwraps the list instead of silently returning the raw dict.

**Independent Test**: Unit test that mocks an API returning `{"modifiedDate": "...", "parcelItems": [{...}]}` when route says `List[ParcelItem]` — result must be `list[ParcelItem]`.

- [X] T003 [US1] In `ab/api/base.py`, add a helper method `_unwrap_list_from_dict(response: dict, model_name: str, path: str) -> list` that: (a) finds all keys in the dict whose values are lists, (b) if exactly one list key, returns its value and logs a warning, (c) if multiple list keys, prefers the one matching the model name (case-insensitive substring match), (d) if no list keys, logs an error and returns an empty list.

- [X] T004 [US1] In `ab/api/base.py`, modify the `_request` method list-handling branch (currently lines 94-97). Replace the `return response` fallback at line 97 with: if `isinstance(response, dict)`, call `_unwrap_list_from_dict`, then validate each item. Log a warning with the route path and wrapper key name.

- [X] T005 [US1] Run `pytest tests/ --tb=short -q` to verify no regressions from the `_request` change. The fix only adds new behavior for the dict case — existing list behavior must remain identical.

**Checkpoint**: `_request` now unwraps dict-wrapped lists. Existing tests green. MVP delivered.

---

## Phase 4: User Story 2 — Mandatory Fixture Capture (Priority: P2)

**Goal**: Add `fixture_file` to every example entry that declares `response_model` but is missing `fixture_file`.

**Independent Test**: Run `python -m examples.parcels --list` and confirm every entry with a response_model also shows a fixture file path.

- [X] T006 [P] [US2] Add `fixture_file` to all entries in `examples/parcels.py` — `get_parcel_items` → `"ParcelItem.json"`, `get_parcel_items_with_materials` → `"ParcelItemWithMaterials.json"`, `get_packaging_containers` → `"PackagingContainer.json"`. The `create_parcel_item` entry already has `request_fixture_file` but needs `fixture_file="ParcelItem.json"`.

- [X] T007 [P] [US2] Add `fixture_file` to all entries missing it in `examples/jobs.py` — map each entry's `response_model` to `fixture_file` per convention: `List[X]` or `X` → `"X.json"`, `ServiceBaseResponse` → `"ServiceBaseResponse.json"`. Skip entries that are expected to fail (placeholder IDs) and `bytes` responses.

- [X] T008 [P] [US2] Add `fixture_file` to all entries missing it in `examples/companies.py` — `get_details` → `"CompanyDetails.json"`, `search` → `"SearchCompanyResponse.json"`, `list` → `"CompanySimple.json"`.

- [X] T009 [P] [US2] Add `fixture_file` to all entries missing it in `examples/shipments.py` — `request_rate_quotes` → `"RateQuote.json"`, `delete_shipment` → `"ServiceBaseResponse.json"`, `remove_accessorial` → `"ServiceBaseResponse.json"`, `get_export_data` → `"ShipmentExportData.json"`, `post_export_data` → `"ServiceBaseResponse.json"`. Skip `get_shipment_document` (bytes response).

- [X] T010 [P] [US2] Add `fixture_file` to all entries missing it in `examples/commodities.py` — `commodity_suggestions` → `"Commodity.json"`, `commodity_get` → `"Commodity.json"`, `commodity_create` → `"Commodity.json"`, `commodity_update` → `"Commodity.json"`, `commodity_map_get` → `"CommodityMap.json"`, `commodity_map_create` → `"CommodityMap.json"`, `commodity_map_update` → `"CommodityMap.json"`, `commodity_map_delete` → `"ServiceBaseResponse.json"`.

- [X] T011 [P] [US2] Add `fixture_file` to all entries missing it in `examples/views.py` — `get` → `"GridViewDetails.json"`, `create` → `"GridViewDetails.json"`, `delete` → `"ServiceBaseResponse.json"`, `get_dataset_sp` → `"StoredProcedureColumn.json"`.

- [X] T012 [P] [US2] Add `fixture_file` to all entries missing it in `examples/rfq.py` — `get_for_job` → `"QuoteRequestDisplayInfo.json"`, `list_rfqs` → `"QuoteRequestDisplayInfo.json"`.

- [X] T013 [P] [US2] Add `fixture_file` to all entries missing it in `examples/partners.py` — `get` → `"Partner.json"`, `search` → `"Partner.json"`.

- [X] T014 [P] [US2] Add `fixture_file` to all entries missing it in `examples/contacts.py` — `get` → `"ContactSimple.json"`.

- [X] T015 [P] [US2] Add `fixture_file` to all entries missing it in `examples/lots.py` — `list` → `"LotDto.json"`, `get` → `"LotDto.json"`, `get_overrides` → `"LotOverrideDto.json"`.

- [X] T016 [P] [US2] Add `fixture_file` to all entries missing it in `examples/catalog.py` — `list` → `"CatalogExpandedDto.json"`, `get` → `"CatalogExpandedDto.json"`.

- [X] T017 [P] [US2] Add `fixture_file` to all entries missing it in `examples/lookup_extended.py` — `get_by_key_and_id` → `"LookupValue.json"`, `get_access_key` → `"AccessKey.json"`, `get_ppc_campaigns` → `"LookupValue.json"`, `get_document_types` → `"LookupValue.json"`, `get_common_insurance` → `"LookupValue.json"`, `get_refer_categories` → `"LookupValue.json"`, `get_refer_category_hierarchy` → `"LookupValue.json"`.

- [X] T018 [P] [US2] Add `fixture_file` to all entries missing it in remaining files: `examples/tracking.py` — `get_tracking` → `"TrackingInfo.json"`, `get_tracking_v3` → `"TrackingInfoV3.json"`. `examples/reports.py` — `top_revenue_customers` → `"RevenueCustomer.json"`, `top_revenue_sales_reps` → `"RevenueCustomer.json"`. `examples/autoprice.py` — `quote_request` → `"QuoteRequestResponse.json"`. `examples/web2lead.py` — `post` → `"Web2LeadResponse.json"`.

- [X] T019 [US2] Run `pytest tests/ --tb=short -q` to verify no regressions from example file changes. Examples are metadata-only — no runtime impact on tests.

**Checkpoint**: All example entries with `response_model` now also have `fixture_file`. Zero gaps.

---

## Phase 5: User Story 3 — Fixture-Model Consistency Gate (Priority: P3)

**Goal**: Add a test that enforces the fixture completeness invariant and verifies array fixture validation.

**Independent Test**: `pytest tests/test_fixture_completeness.py -v` passes with zero violations.

- [X] T020 [US3] Create `tests/test_fixture_completeness.py` — import all example modules from `examples/`, iterate over each runner's `entries`, assert that every entry with `response_model` set (and not `"bytes"`) also has `fixture_file` set. Report violations with file, entry name, and response_model. This test enforces the contract from `contracts/fixture-completeness.md`.

- [X] T021 [US3] Review `tests/models/test_parcel_models.py` and `tests/conftest.py` `require_fixture` helper — verify that array fixtures (JSON files containing a `[...]` top-level array) are handled correctly. If `require_fixture` returns a list, the test must iterate and validate each element. Update `test_parcel_models.py` if needed to handle array fixtures.

- [X] T022 [US3] Run `pytest tests/ --tb=short -q` to verify the new test passes and no regressions.

**Checkpoint**: Fixture completeness is now enforced by a test. Array fixtures are handled.

---

## Phase 6: User Story 4 — Stale Artifact Cleanup (Priority: P4)

**Goal**: Remove stale `progress.html` from repository root.

**Independent Test**: `ls progress.html` at repo root returns "not found".

- [X] T023 [P] [US4] Delete `progress.html` from the repository root (it has been moved to `html/progress.html`). Verify `html/progress.html` still exists.

- [X] T024 [US4] Run `pytest tests/ --tb=short -q` to verify no test references the root-level `progress.html`.

**Checkpoint**: Stale artifact removed. Clean repo root.

---

## Phase 7: Polish & Final Verification

**Purpose**: End-to-end validation and cleanup.

- [X] T025 Run `ruff check ab/api/base.py` and fix any lint violations introduced by the new unwrap logic.

- [X] T026 Run `pytest tests/ --tb=short -q` final full suite verification. Document the expected test count (should be 307+ passed plus the new fixture completeness test).

- [X] T027 Verify SC-001: Confirm `_request` now handles dict-wrapped list responses by reviewing the updated code in `ab/api/base.py` lines 94+.

- [X] T028 Verify SC-002: Run `pytest tests/test_fixture_completeness.py -v` and confirm zero violations.

---

## Dependencies

```
Phase 1 (T001-T002) ──> Phase 3 (T003-T005) [understand before fixing]
Phase 3 (T003-T005) ──> Phase 5 (T020-T022) [fix must exist before gate test]
Phase 4 (T006-T019) ──> Phase 5 (T020-T022) [fixture_files must exist before gate test passes]
Phase 6 (T023-T024) is fully independent
All ──> Phase 7 (T025-T028) [final verification]
```

## Parallel Execution Opportunities

```
Phase 4: T006 || T007 || T008 || T009 || T010 || T011 || T012 || T013 || T014 || T015 || T016 || T017 || T018 (all different files)
Phase 6: T023 (independent of all other phases)
Phase 7: T025 || T026 || T027 || T028 (independent verification tasks)
```

## Implementation Strategy

### MVP First (Phase 1-3: US1 Only)

1. Complete Phase 1: Read current state, establish baseline
2. Complete Phase 3: Fix the `_request` dict-wrapper bug
3. **STOP and VALIDATE**: `_request` now unwraps dict-wrapped lists, tests green
4. This alone delivers the core value: SDK returns typed models instead of raw dicts

### Incremental from MVP

- Phase 4 (US2): Add `fixture_file` to all example entries — bulk metadata updates, no runtime changes
- Phase 5 (US3): Add gate test — closes the enforcement loop
- Phase 6 (US4): Delete stale file — trivial cleanup
- Phase 7: Final verification
