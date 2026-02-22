# Tasks: Deep Pydantic Models for Company Response

**Input**: Design documents from `/specs/016-deep-company-models/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Not explicitly requested. Existing test suite (307+ passed) must remain green. Fixture validation tests auto-discover models — no new test files needed.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Understand current state and verify baseline

- [X] T001 Read the current `ab/api/models/companies.py` to understand existing `CompanyDetails` model structure — identify all `dict`-typed fields and their line numbers. Read the C# source entities for reference: `CompanyInfo.cs`, `AddressData.cs`, `OverridableAddressData.cs`, `Overridable.cs`, `CompanyInsurancePricing.cs`, `CompanyServicePricing.cs`, `CompanyTaxPricing.cs`.

- [X] T002 Run `pytest tests/ --tb=short -q` to establish baseline test count. Confirm all existing tests pass before making changes.

- [X] T003 Read `tests/fixtures/CompanyDetails.json` and extract the exact JSON shapes for `companyInfo`, `addressData`, `overridableAddressData`, `companyInsurancePricing`, `companyServicePricing`, `companyTaxPricing` nested objects. These are the ground truth for field aliases.

**Checkpoint**: Baseline established. All existing tests green. JSON shapes documented.

---

## Phase 2: Foundational (Shared Nested Models)

**Purpose**: Create reusable nested model classes that all user stories depend on

- [X] T004 [P] Add `OverridableField` model to `ab/api/models/companies.py` — inherits `ResponseModel`, fields: `default_value: Optional[str]` (alias `defaultValue`), `override_value: Optional[str]` (alias `overrideValue`), `force_empty: Optional[bool]` (alias `forceEmpty`), `value: Optional[str]` (alias `value`). All fields Optional with Field descriptions.

- [X] T005 [P] Add `CompanyInfo` model to `ab/api/models/companies.py` — inherits `ResponseModel`, fields from C# `CompanyInfo`: `company_id` (alias `companyId`), `company_type_id`, `company_display_id`, `company_name`, `company_code`, `company_email`, `company_phone`, `thumbnail_logo`, `company_logo`, `maps_marker_image`, `main_address: Optional[CompanyAddress]` (alias `mainAddress`). All `Optional[str]` except `main_address`.

- [X] T006 [P] Add `AddressData` model to `ab/api/models/companies.py` — inherits `ResponseModel`, all fields from C# `AddressData`: `company`, `first_last_name`, `address_line1`, `address_line2`, `contact_bol_note` (alias `contactBOLNote`), `city`, `state`, `state_code`, `zip_code`, `country_name`, `property_type`, `full_city_line`, `phone`, `cell_phone`, `fax`, `email`, `country_id`, plus computed booleans `address_line2_visible`, `company_visible`, `country_name_visible`, `phone_visible`, `email_visible`, and computed strings `full_address_line`, `full_address`. All Optional.

- [X] T007 Add `OverridableAddressData` model to `ab/api/models/companies.py` — inherits `ResponseModel`. Fields `company`, `first_last_name`, `address_line1`, `address_line2`, `city`, `state`, `zip_code`, `phone`, `email` are `Optional[OverridableField]`. `full_address_line` is `Optional[str]` (plain string, not wrapped). `full_address` and `full_city_line` are `Optional[OverridableField]`. Depends on T004 (`OverridableField`).

- [X] T008 [P] Add `CompanyInsurancePricing` model to `ab/api/models/companies.py` — inherits `ResponseModel`, fields from C# entity: `insurance_slab_id` (alias `insuranceSlabID`), `deductible_amount`, `rate`, `company_id`, `is_active`, `transp_type_id` (alias `transpTypeID`), `company_name`, `created_by` (alias `createdby`), `modified_by` (alias `modifiedby`), `revision: Optional[int]`, `insurance_type`, `whole_sale_markup`, `base_markup`, `medium_markup`, `high_markup`. Strings for GUIDs, floats for decimals.

- [X] T009 [P] Add `CompanyServicePricing` model to `ab/api/models/companies.py` — inherits `ResponseModel`, fields from C# entity: `service_pricing_id`, `user_id` (alias `userID`), `company_id` (alias `companyID`), `service_category_id` (alias `serviceCategoryID`), `category_value`, markup fields, `is_active`, `is_taxable`, `tax_percent`, `created_by`, `modified_by`, `created_date`, `modified_date`, `company_code`, `service_category_name`, `company_name`, `company_type_id`, `parent_category_id` (alias `parentCategoryID`), `zip_code`.

- [X] T010 [P] Add `CompanyTaxPricing` model to `ab/api/models/companies.py` — inherits `ResponseModel`, fields from C# entity: `job_id` (alias `jobID`), `service_category_id` (alias `serviceCategoryID`), `tax_slab_id` (alias `taxSlabID`), `is_taxable`, `tax_percent`, `company_id` (alias `companyID`), `service_category_name` (alias `serviceCategotyName` — preserve C# typo in alias), `company_name`, `is_active`.

- [X] T011 Run `pytest tests/ --tb=short -q` to confirm new model class definitions don't break any existing tests (models are defined but not yet wired to `CompanyDetails`).

**Checkpoint**: All 7 new nested model classes defined. Tests still green. Models are standalone — not yet referenced by `CompanyDetails`.

---

## Phase 3: User Story 1 — Typed Access to Company Info (Priority: P1) 🎯 MVP

**Goal**: Replace `dict`-typed fields in `CompanyDetails` with the new typed models so `company.company_info.company_id` works.

**Independent Test**: Load `CompanyDetails.json` fixture, call `model_validate()`, access `obj.company_info.company_id` — returns string UUID. Access `obj.address_data.company` — returns string. Access `obj.overridable_address_data.company.value` — returns string.

- [X] T012 [US1] Update `CompanyDetails` in `ab/api/models/companies.py` — change `company_info: Optional[dict]` to `company_info: Optional[CompanyInfo]`. Keep the same field alias. Verify `CompanyDetails.json` fixture still passes `model_validate()`.

- [X] T013 [US1] Update `CompanyDetails` in `ab/api/models/companies.py` — change `address_data: Optional[dict]` to `address_data: Optional[AddressData]`. Verify fixture validation.

- [X] T014 [US1] Update `CompanyDetails` in `ab/api/models/companies.py` — change `overridable_address_data: Optional[dict]` to `overridable_address_data: Optional[OverridableAddressData]`. Verify fixture validation.

- [X] T015 [US1] Update `CompanyDetails` in `ab/api/models/companies.py` — change `company_insurance_pricing: Optional[dict]` to `company_insurance_pricing: Optional[CompanyInsurancePricing]`. Verify fixture validation.

- [X] T016 [P] [US1] Update `CompanyDetails` in `ab/api/models/companies.py` — change `company_service_pricing: Optional[dict]` to `company_service_pricing: Optional[CompanyServicePricing]`. Change `company_tax_pricing: Optional[dict]` to `company_tax_pricing: Optional[CompanyTaxPricing]`. Verify fixture validation.

- [X] T017 [US1] Run `pytest tests/ --tb=short -q` full suite verification. All tests must pass. Fixture validation for `CompanyDetails` must succeed with the typed nested models.

- [X] T018 [US1] Verify typed access works end-to-end: write a quick validation script or add assertions to verify `obj.company_info.company_id`, `obj.address_data.address_line1`, `obj.overridable_address_data.company.value`, `obj.overridable_address_data.full_address.default_value` all return expected values from the fixture. Check that `obj.company_info.main_address` is a `CompanyAddress` instance.

**Checkpoint**: All dict fields replaced with typed models. Fixture validates. Attribute access works end-to-end. Tests green.

---

## Phase 4: User Story 2 — Unified Model Validation (Priority: P2)

**Goal**: Confirm both `/details` and `/fulldetails` routes work with the single typed `CompanyDetails` model. Both routes already reference `CompanyDetails` — verify no changes needed.

**Independent Test**: Both `get_details()` and `get_fulldetails()` return `CompanyDetails` with typed nested objects.

- [X] T019 [US2] Verify Route definitions in `ab/api/endpoints/companies.py` — confirm `_GET_DETAILS` and `_GET_FULLDETAILS` both reference `response_model="CompanyDetails"`. No changes expected — document confirmation.

- [X] T020 [US2] Update `ab/api/models/__init__.py` — add the new model classes (`OverridableField`, `CompanyInfo`, `AddressData`, `OverridableAddressData`, `CompanyInsurancePricing`, `CompanyServicePricing`, `CompanyTaxPricing`) to imports and `__all__` if they need to be publicly accessible. Check if existing `__all__` in `companies.py` needs updating.

- [X] T021 [US2] Run `pytest tests/ --tb=short -q` to verify all tests pass after import updates. Check for any `extra_fields` warnings in test output related to the new nested models.

**Checkpoint**: Both endpoints confirmed to use `CompanyDetails`. New models properly exported. Tests green.

---

## Phase 5: User Story 3 — Fixture and Test Alignment (Priority: P3)

**Goal**: Ensure fixtures, examples, and integration tests work correctly with the typed nested models.

**Independent Test**: `pytest tests/ -k company` passes. No `extra_fields` warnings on nested models.

- [X] T022 [US3] Run `pytest tests/ -k company -v` and review output. Verify fixture validation for `CompanyDetails.json` passes with zero warnings. If any extra fields appear on nested models, add the missing fields to the corresponding model.

- [X] T023 [US3] Review `examples/companies.py` — verify examples still work with the typed models. No changes expected since examples call endpoint methods which return `CompanyDetails` objects. Confirm `request_fixture_file` entries are correct.

- [X] T024 [US3] Review `tests/integration/test_companies.py` — verify assertions work with typed nested models. If tests access `result.company_info` as a dict, update to attribute access. Run integration tests (if staging available) or verify test structure is correct.

- [X] T025 [US3] Update `docs/FIXTURES.md` if the company fixture section needs changes to reflect the new typed nested models.

**Checkpoint**: All company-related tests, fixtures, and examples aligned with typed models.

---

## Phase 6: Polish & Final Verification

**Purpose**: End-to-end validation and cleanup

- [X] T026 Run `ruff check ab/api/models/companies.py` and fix any lint violations introduced by the new models.

- [X] T027 Run `pytest tests/ --tb=short -q` final full suite verification. Document the expected test count (should be 307+ passed).

- [X] T028 Verify SC-001: Grep `ab/api/models/companies.py` for remaining `Optional[dict]` fields in `CompanyDetails`. Only `settings`, `addresses`, `contacts` should remain as dict (deferred by design).

- [X] T029 Verify SC-002: Load `CompanyDetails.json`, call `model_validate()`, confirm `obj.company_info.company_id`, `obj.address_data.company`, `obj.overridable_address_data.company.value` all work with attribute access.

---

## Dependencies

```
Phase 1 (T001-T003) ──> Phase 2 (T004-T011) [understand before creating]
T004 ──> T007 (OverridableField before OverridableAddressData)
Phase 2 (T004-T010) ──> Phase 3 (T012-T018) [models before wiring]
Phase 3 ──> Phase 4 (T019-T021) [wiring before validation]
Phase 3 ──> Phase 5 (T022-T025) [wiring before test alignment]
All ──> Phase 6 (T026-T029) [final verification]
```

## Parallel Execution Opportunities

```
Phase 2: T004 || T005 || T006 || T008 || T009 || T010 (independent model classes)
         T007 after T004 (depends on OverridableField)
Phase 3: T012 then T013 then T014 then T015 (sequential — each changes same file, verify after each)
         T016 after T015 (same file)
Phase 4: T019 || T020 (different files)
Phase 5: T022 || T023 || T024 || T025 (independent verification tasks)
Phase 6: T026 || T027 || T028 || T029 (independent verification)
```

## Implementation Strategy

### MVP First (Phase 1-3: US1 Only)

1. Complete Phase 1: Read current state, establish baseline
2. Complete Phase 2: Define all 7 new nested model classes
3. Complete Phase 3: Wire typed models into `CompanyDetails`, verify fixture
4. **STOP and VALIDATE**: `company.company_info.company_id` works, fixture validates, tests green
5. This alone delivers the core value: typed attribute access instead of dict brackets

### Incremental from MVP

- Phase 4 (US2): Verify route/import alignment — minimal changes expected
- Phase 5 (US3): Align fixtures, examples, tests — mostly verification
- Phase 6: Final polish and verification
