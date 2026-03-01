# Feature Specification: Fix Contact Search

**Feature Branch**: `022-fix-contact-search`
**Created**: 2026-02-28
**Status**: Draft
**Input**: User description: "Fix contact search request model and response model to match C# source of truth. Request fixture fails validation because pydantic models don't match the nested structure. Response fixture is mislabeled. Tests need contactDisplayId and company fields excluded from SearchContactEntityResult."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Request model matches the API's nested structure (Priority: P1)

An SDK developer calls `api.contacts.search()` with search parameters. The request model must match the API's expected nested structure (with `mainSearchRequest` and `loadOptions` sub-objects) so that the API returns valid results instead of HTTP 400 errors.

**Why this priority**: The request fixture currently fails pydantic validation. The model uses a flat structure (`page`, `page_size`, `search_text`) but the API expects a nested structure with `mainSearchRequest` (search fields) and `loadOptions` (pagination/sort). Without this fix, the SDK cannot successfully call the search endpoint.

**Independent Test**: Validate the request fixture (`tests/fixtures/requests/ContactSearchRequest.json`) against the updated `ContactSearchRequest` model with zero validation errors and zero extra fields.

**Acceptance Scenarios**:

1. **Given** the request fixture JSON with nested `mainSearchRequest` and `loadOptions`, **When** validated against the updated `ContactSearchRequest` model, **Then** validation succeeds with zero extra fields.
2. **Given** a developer constructs a `ContactSearchRequest` with search parameters and pagination, **When** serialized to JSON, **Then** the output matches the API's expected nested structure.
3. **Given** the test suite runs `test_request_fixture_validates` for `ContactSearchRequest`, **When** all assertions execute, **Then** the test passes (isinstance, assert_no_extra_fields, round-trip).

---

### User Story 2 - Response model declares all API-returned fields (Priority: P1)

An SDK developer receives search results from `api.contacts.search()`. The response model (`SearchContactEntityResult`) must declare all fields the API actually returns so that developers get IDE autocomplete and type safety on search results. The model must NOT include `contactDisplayId` or `company` as they don't belong to the search result shape.

**Why this priority**: The current response fixture is mislabeled — it contains a full `ContactDetailedInfo` object instead of a search result entity. The actual search result shape (per C# source/swagger) has ~21 fields (contactID, contactFullName, contactEmail, companyName, address fields, etc.) that differ from the current 5-field model. Without correct field declarations, G1 fails.

**Independent Test**: Validate the corrected response fixture against the updated `SearchContactEntityResult` model with zero extra fields. Uncomment `assert_no_extra_fields` in `test_search_contact_entity_result`.

**Acceptance Scenarios**:

1. **Given** a corrected response fixture containing actual search result fields, **When** validated against the updated `SearchContactEntityResult` model, **Then** validation succeeds with zero extra fields.
2. **Given** the model does NOT declare `contactDisplayId` or `company` fields, **When** a developer accesses search results, **Then** only fields present in the actual search response are available.
3. **Given** the test suite runs `test_search_contact_entity_result`, **When** `assert_no_extra_fields` is active (not commented out), **Then** the test passes.

---

### Edge Cases

- What if the API returns a search result with no matching contacts? The response should be an empty list. The model handles this naturally.
- What if `mainSearchRequest` fields are all null? The API should still return results (unfiltered). The model must allow all search fields to be optional.
- What if the response fixture needs re-capture from live API? Replace the mislabeled fixture with a mock fixture matching the swagger schema until live re-capture is possible.
- What about the `totalRecords` field in search results? It appears on each result row (denormalized per swagger). The model must declare it.

## Requirements *(mandatory)*

### Functional Requirements

**Request Model (ContactSearchRequest)**

- **FR-001**: The request model MUST accept a nested structure with `mainSearchRequest` (search parameters) and `loadOptions` (pagination/sort).
- **FR-002**: The `mainSearchRequest` sub-object MUST support fields: contactDisplayId (optional int), fullName (optional str), companyName (optional str), companyCode (optional str), email (optional str), phone (optional str), companyDisplayId (optional int).
- **FR-003**: The `loadOptions` sub-object MUST support fields: pageNumber (required int), pageSize (required int), sortingBy (optional str), sortingDirection (optional int).
- **FR-004**: The request fixture MUST validate against the model with zero extra fields and survive round-trip serialization.

**Response Model (SearchContactEntityResult)**

- **FR-005**: The response model MUST declare all fields from the C# `SearchContactEntityResult` DTO: contactID, customerCell, contactFullName, contactPhone, contactHomePhone, contactEmail, masterConstantValue, contactDept, address1, address2, city, state, zipCode, countryName, companyCode, companyID, companyName, companyDisplayId, isPrefered, industryType, totalRecords.
- **FR-006**: The response model MUST NOT include `contactDisplayId` or `company` (dict) as these belong to `ContactDetailedInfo`, not search results.
- **FR-007**: The response fixture MUST contain actual search result data (not a mislabeled `ContactDetailedInfo` object).
- **FR-008**: All model fields MUST have `Field(description=...)` for IDE tooltips.

**Tests**

- **FR-009**: The request fixture test (`test_request_fixture_validates[ContactSearchRequest]`) MUST pass with isinstance, assert_no_extra_fields, and round-trip assertions.
- **FR-010**: The response model test (`test_search_contact_entity_result`) MUST have `assert_no_extra_fields` uncommented and passing.
- **FR-011**: The full test suite MUST pass with zero regressions after changes.

### Key Entities

- **ContactSearchRequest**: The request body for POST /contacts/v2/search, containing nested search parameters and pagination options.
- **ContactSearchParams**: Sub-model for the `mainSearchRequest` object containing search filter fields.
- **PageOrderedRequest**: Sub-model for the `loadOptions` object containing pagination and sorting fields.
- **SearchContactEntityResult**: A single search result row with contact details, address, company info, and metadata.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The request fixture (`ContactSearchRequest.json`) validates against the model with zero extra fields and zero validation errors.
- **SC-002**: The response fixture validates against `SearchContactEntityResult` with zero extra fields.
- **SC-003**: Both `contactDisplayId` and `company` dict fields are absent from `SearchContactEntityResult`.
- **SC-004**: All quality gates (G1-G6) pass for POST /contacts/v2/search after the fix.
- **SC-005**: The full test suite passes with zero failures and zero regressions.

## Assumptions

- The swagger `MergeContactsSearchRequestModel` schema accurately represents the request structure (matches the captured fixture).
- The swagger `SearchContactEntityResult` schema accurately represents the response field names (to be validated against C# source).
- The current response fixture (`SearchContactEntityResult.json`) is incorrectly captured and must be replaced with a mock fixture.
- The `contactDisplayId` and `company` fields the user wants excluded are artifacts of the mislabeled fixture, not actual search result fields.

## Scope

### In Scope

- Restructuring `ContactSearchRequest` to match the API's nested structure
- Creating typed sub-models for `mainSearchRequest` and `loadOptions`
- Updating `SearchContactEntityResult` with all C# source fields
- Fixing or replacing the mislabeled response fixture
- Uncommenting `assert_no_extra_fields` in tests
- Ensuring all quality gates pass

### Out of Scope

- Changing the endpoint method signature beyond model name updates
- Adding new endpoints
- Sweeping other contact models beyond the search pair
