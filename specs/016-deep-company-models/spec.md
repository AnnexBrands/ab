# Feature Specification: Deep Pydantic Models for Company Response

**Feature Branch**: `016-deep-company-models`
**Created**: 2026-02-22
**Status**: Draft
**Input**: User description: "Issue 1: Full depth pydantic objects required — currently forced to mix pydantic and dict getters (e.g., `elabel.company_info['companyId']`). Issue 2: Swagger does not list a response object for /details/, but lists CompanyDetails entity for get_fulldetails — bad assumption they would be similar. Check the C# controllers and entities to provide correct pydantic response models."

## Clarifications

### Session 2026-02-22

- Q: Should we split into two distinct response models for /details and /fulldetails, or keep one unified model? → A: Keep single `CompanyDetails` model for both endpoints — the live fixture proves `/fulldetails` returns both envelope fields AND flat Company entity fields in one response. Splitting would create a model where half the fields are always None.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Typed Access to Company Info (Priority: P1)

An SDK consumer calls `api.companies.get_details(code)` and accesses nested data using attribute notation throughout — no dict bracket access required. For example, `company.company_info.company_id` instead of `company.company_info['companyId']`.

**Why this priority**: This is the core usability issue. Dict access defeats the purpose of a typed SDK — users lose autocomplete, type checking, and documentation discoverability. Every nested `dict` field is a gap in the type contract.

**Independent Test**: Call `api.companies.get_details(TEST_COMPANY_CODE)`, then access `result.company_info.company_id` — it returns a string UUID without raising `AttributeError`. All nested objects are pydantic model instances, not dicts.

**Acceptance Scenarios**:

1. **Given** a valid company code, **When** calling `get_details()`, **Then** `result.company_info` is a typed model with `.company_id`, `.company_name`, `.main_address` attributes
2. **Given** a valid company code, **When** calling `get_details()`, **Then** `result.address_data` is a typed model with `.company`, `.address_line1`, `.city` etc.
3. **Given** a valid company code, **When** calling `get_details()`, **Then** `result.overridable_address_data` is a typed model whose fields (`.company`, `.address_line1` etc.) are each typed override containers with `.default_value`, `.override_value`, `.force_empty`, `.value`
4. **Given** a valid company code, **When** calling `get_details()`, **Then** `result.contact_info` is a typed model (not a dict) when the field is non-null. When `contact_info` is `null`, it remains `None`.

---

### User Story 2 — Unified Model with Typed Nested Fields (Priority: P2)

Both `/details` and `/fulldetails` endpoints use the same `CompanyDetails` response model. The live API fixture confirms `/fulldetails` returns a superset containing both the nested envelope sections (details, preferences, pricing, etc.) and the flat Company entity fields (companyName, companyCode, companyInfo, etc.) in a single response. The single model accepts both shapes via Optional fields. The focus is on typing the nested dict fields, not splitting models.

**Why this priority**: A single well-typed model is simpler to maintain and avoids duplication. Both endpoints benefit from the same typed nested structures.

**Independent Test**: Call both `get_details()` and `get_fulldetails()` — both return `CompanyDetails`. All nested objects (`company_info`, `address_data`, `overridable_address_data`) are typed pydantic models in both responses.

**Acceptance Scenarios**:

1. **Given** the `/details` endpoint, **When** called, **Then** the response is a `CompanyDetails` with flat Company entity fields populated and nested envelope fields as `None`
2. **Given** the `/fulldetails` endpoint, **When** called, **Then** the response is a `CompanyDetails` with both envelope and flat fields populated
3. **Given** both endpoints, **Then** nested sub-structures (`CompanyInfo`, `AddressData`, `OverridableAddressData`) are shared typed models

---

### User Story 3 — Fixture and Test Alignment (Priority: P3)

Existing test fixtures and integration tests validate against the new typed models. The fixture file `CompanyDetails.json` validates correctly against the updated `CompanyDetails` model with typed nested fields. Tests confirm no extra or missing fields.

**Why this priority**: Tests are the safety net — they must reflect the corrected models to prevent regressions.

**Independent Test**: Run `pytest tests/ -k company` — all company-related tests pass. Fixture validation confirms no `extra_fields` warnings on the new nested models.

**Acceptance Scenarios**:

1. **Given** the updated models, **When** running fixture validation tests, **Then** the `CompanyDetails.json` fixture passes with zero extra-field warnings on typed nested models
2. **Given** the updated models, **When** running integration tests against staging, **Then** `get_details` and `get_fulldetails` both return `CompanyDetails` with typed nested objects

---

### Edge Cases

- What happens when nested objects are absent from the API response (e.g., `companyInfo` is `null`)? The model should accept `None` for optional nested objects.
- What happens when the `overridableAddressData` contains fields with `forceEmpty: true`? The `.value` computed property returns the empty default, which the model should represent faithfully.
- What happens when `capabilities` is an integer (bitmask) vs a dict? The model already handles this with `Union[int, dict]` — this should be preserved.
- What happens when `contact_info` is `null` in the response? The field stays `None` — typing only applies when the field is populated.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide typed pydantic models for all nested objects currently typed as `dict` in the company response — specifically: `company_info`, `contact_info`, `address_data`, `overridable_address_data`, `company_insurance_pricing`, `company_service_pricing`, `company_tax_pricing`
- **FR-002**: System MUST use a single `CompanyDetails` model for both `/details` and `/fulldetails` endpoints, with all dict-typed nested fields replaced by typed pydantic models
- **FR-003**: System MUST model the `Overridable<T>` pattern from C# as a pydantic model with `default_value`, `override_value`, `force_empty`, and computed `value` fields
- **FR-004**: System MUST model `CompanyInfo` as a typed model with `company_id`, `company_type_id`, `company_name`, `company_code`, `company_email`, `company_phone`, `thumbnail_logo`, `company_logo`, `maps_marker_image`, and nested `main_address` (reusing existing `CompanyAddress` model)
- **FR-005**: System MUST model `AddressData` as a typed model with all string fields from the C# entity: `company`, `first_last_name`, `address_line1`, `address_line2`, `city`, `state`, `state_code`, `zip_code`, `country_name`, `phone`, `cell_phone`, `fax`, `email`, `full_city_line`, `property_type`, `contact_bol_note`, `country_id`
- **FR-006**: System MUST preserve backward compatibility — existing code that accesses the current model via established field names and aliases should not break
- **FR-007**: Both Route definitions (`_GET_DETAILS` and `_GET_FULLDETAILS`) MUST continue to reference `CompanyDetails` as their response model
- **FR-008**: System MUST verify the existing `CompanyDetails.json` fixture validates against the updated model with typed nested fields, and update examples/tests accordingly

### Key Entities

- **CompanyInfo**: Summary of a company — ID, name, code, contact details, main address. Nested inside the response as `company_info`.
- **AddressData**: Flat address representation with all string fields — used in reports and forms context.
- **OverridableAddressData**: Container where each address field is wrapped in an `OverridableField` with default/override/forceEmpty semantics.
- **OverridableField**: Container with `default_value`, `override_value`, `force_empty`, `value` — models the C# `Overridable<T>` pattern.
- **CompanyDetails**: Single unified response model for both `/details` and `/fulldetails` — accepts both flat Company entity fields and nested envelope sections via Optional fields.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of previously `dict`-typed nested fields in the company response models are replaced with typed pydantic models — zero `dict` or `List[dict]` fields remain for known structures
- **SC-002**: SDK consumers can access all company data using attribute notation exclusively — `company.company_info.company_id` works without dict bracket access
- **SC-003**: Existing test suite passes (307+ tests) with zero regressions after the model changes
- **SC-004**: Both `get_details()` and `get_fulldetails()` return `CompanyDetails` with typed nested objects validated against the existing fixture

## Assumptions

- The C# `Company` entity at `AB.ABCEntities/Company.cs` is the authoritative source for the flat fields in the response.
- The `/fulldetails` response is a superset — it contains both envelope fields and flat Company entity fields.
- Fields like `settings`, `addresses` (list), and `contacts` (list) may remain `Optional[dict]` or `Optional[List[dict]]` if their C# types are not clearly defined or are highly polymorphic — these can be typed in a follow-up feature.
- The `CompanyAddress` model already exists and is correctly typed — it will be reused for nested address fields.
