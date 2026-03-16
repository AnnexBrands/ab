# Feature Specification: Fix Catalog Model Typing

**Feature Branch**: `033-fix-catalog-model-typing`
**Created**: 2026-03-16
**Status**: Draft
**Input**: User description: "All endpoints (except response.content is bytes) are expected to return nested pydantic objects. Ensure correct typing of CatalogExpandedDto.lots, CatalogSellerDto, CatalogExpandedDto, CatalogWithSellersDto"

## Clarifications

### Session 2026-03-16

- Q: Does "CatalogSellerDto" refer to the existing SellerDto or a new model? → A: CatalogSellerDto refers to the existing SellerDto — use it directly, no new model needed.
- Q: Should scope include only catalog models, or also directly-referenced models with `List[dict]`? → A: Fix catalog models plus directly-referenced models (SellerExpandedDto, LotDto) where they also have `List[dict]` and a typed model exists.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - IDE Discoverability for Catalog Nested Fields (Priority: P1)

As an SDK consumer, when I access nested fields on catalog response objects (e.g., `catalog.sellers[0].name` or `catalog.lots[0].data.qty`), my IDE provides autocomplete, type checking, and inline documentation rather than treating them as untyped dictionaries.

**Why this priority**: Without proper typing, developers lose all IDE support for nested catalog data and must consult documentation or inspect raw JSON to discover field names and types. This is the core value of a typed SDK.

**Independent Test**: Access `.sellers[0].name` on a CatalogExpandedDto instance and verify the IDE resolves the type to `str` (via SellerDto) rather than `Any`.

**Acceptance Scenarios**:

1. **Given** a CatalogExpandedDto response, **When** a developer accesses `.sellers[0]`, **Then** the IDE reports the type as SellerDto with full field autocomplete.
2. **Given** a CatalogExpandedDto response, **When** a developer accesses `.lots[0]`, **Then** the IDE reports a properly typed lot model with full field autocomplete.
3. **Given** a CatalogWithSellersDto response, **When** a developer accesses `.sellers[0]` or `.lots[0]`, **Then** the IDE reports correctly typed nested models.

---

### User Story 2 - Pydantic Validation of Nested Catalog Structures (Priority: P1)

As an SDK consumer, when I receive a catalog API response containing nested sellers and lots, the SDK automatically validates and deserializes the nested JSON into proper Pydantic model instances rather than leaving them as raw dictionaries.

**Why this priority**: Proper nested model typing ensures data integrity -- malformed nested data is caught at deserialization time rather than silently passing through as dicts and failing later at point of use.

**Independent Test**: Deserialize a catalog JSON fixture containing nested seller and lot objects and verify each nested item is a Pydantic model instance (not a dict).

**Acceptance Scenarios**:

1. **Given** a JSON response with nested seller objects, **When** the response is deserialized into CatalogExpandedDto, **Then** each item in `.sellers` is an instance of SellerDto.
2. **Given** a JSON response with nested lot objects, **When** the response is deserialized into CatalogExpandedDto, **Then** each item in `.lots` is an instance of the schema-correct lot model.
3. **Given** a JSON response with nested seller objects, **When** the response is deserialized into CatalogWithSellersDto, **Then** each item in `.sellers` and `.lots` is a properly typed Pydantic model instance.

---

### User Story 3 - Existing Fixture and Test Compatibility (Priority: P2)

As a developer maintaining the SDK, when I update catalog model field types from `List[dict]` to proper nested Pydantic models, all existing fixture-based tests and integration tests continue to pass without modification (or with minimal, predictable adjustments).

**Why this priority**: Backward compatibility ensures the typing fix does not introduce regressions. Existing consumers who access nested fields via dictionary syntax should still work via Pydantic model attribute access.

**Independent Test**: Run the full test suite after model type changes and verify all catalog-related tests pass.

**Acceptance Scenarios**:

1. **Given** updated catalog model types, **When** the existing test suite runs, **Then** all fixture validation tests pass.
2. **Given** updated catalog model types, **When** existing integration tests run, **Then** catalog API responses deserialize correctly.

---

### Edge Cases

- What happens when the API returns `null` for a nested seller or lot list? (The `Optional` wrapper must be preserved.)
- What happens when the API returns an empty list `[]` for sellers or lots? (Should deserialize to an empty list of the typed model.)
- What happens when a nested object contains unexpected extra fields? (Pydantic's existing model config should handle this consistently.)
- Are there any circular reference risks between catalog and seller models if SellerExpandedDto references CatalogExpandedDto? (Forward references or deferred annotations may be needed.)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: CatalogExpandedDto.sellers MUST be typed as a list of the appropriate seller Pydantic model (not `List[dict]`).
- **FR-002**: CatalogExpandedDto.lots MUST be typed as a list of the appropriate lot Pydantic model (not `List[dict]`).
- **FR-003**: CatalogWithSellersDto.sellers MUST be typed as a list of the appropriate seller Pydantic model (not `List[dict]`).
- **FR-004**: CatalogWithSellersDto.lots MUST be typed as a list of the appropriate lot Pydantic model (not `List[dict]`).
- **FR-005**: If a referenced nested model does not yet exist in the codebase (e.g., LotCatalogInformationDto from the OpenAPI schema), it MUST be created with fields matching the API schema.
- **FR-006**: All nested model types MUST match the definitions in the OpenAPI/Swagger schema for the Catalog API.
- **FR-007**: Existing `Optional` wrappers on nullable fields MUST be preserved to maintain backward compatibility.
- **FR-008**: All existing tests MUST pass after the type changes, or test fixtures MUST be updated to match the corrected types.
- **FR-009**: SellerExpandedDto.catalogs MUST be typed with the correct catalog Pydantic model (not `List[dict]`).
- **FR-010**: LotDto fields that contain nested objects (catalogs, image_links) MUST be typed with correct Pydantic models where a schema definition exists (not `List[dict]` or untyped `list`).

### Key Entities

- **CatalogExpandedDto**: Full catalog representation returned by GET /Catalog/{id}; contains nested sellers and lots collections.
- **CatalogWithSellersDto**: Catalog representation returned by POST/PUT operations; contains nested sellers and lots collections.
- **SellerDto**: Nested seller summary (id, name, display_id) used within catalog responses.
- **LotCatalogInformationDto**: Nested lot-in-catalog representation referenced by the OpenAPI schema; may need to be created if not yet defined.
- **SellerExpandedDto**: Extended seller representation; its `catalogs` field uses `List[dict]` and is in scope for typing correction.
- **LotDto**: Existing lot model; its `catalogs` and `image_links` fields use `List[dict]`/untyped `list` and are in scope for typing correction.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of in-scope model fields that contain nested objects are typed with their corresponding Pydantic model class (zero `List[dict]` remaining on CatalogExpandedDto, CatalogWithSellersDto, SellerExpandedDto, and LotDto).
- **SC-002**: IDE autocomplete resolves all nested catalog fields to their concrete types (verified by static type checker reporting no `dict` access on typed fields).
- **SC-003**: All existing fixture validation tests pass without regression after the type changes.
- **SC-004**: Nested objects in API responses are deserialized as Pydantic model instances (verified by `isinstance` checks in tests).

## Assumptions

- The OpenAPI/Swagger schema is the source of truth for determining correct nested types.
- The SellerDto model already exists and is correctly defined for use as the nested seller type.
- Lot-related nested models may need to be created or adjusted based on what the OpenAPI schema specifies (e.g., LotCatalogInformationDto).
- The fix scope covers catalog models (CatalogExpandedDto, CatalogWithSellersDto) plus directly-referenced models (SellerExpandedDto, LotDto) where they also have `List[dict]` fields with a typed model available. Other models codebase-wide are out of scope.
- Forward references (string annotations) will be used where circular imports would otherwise occur.
