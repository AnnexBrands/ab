# Feature Specification: Catalog Endpoint Params & Pagination

**Feature Branch**: `035-catalog-endpoint-params`
**Created**: 2026-03-16
**Status**: Draft
**Input**: User description: "Add typed params, docstrings, pagination helpers, and Pydantic validation to all catalog/seller/lot endpoint methods. Tests and examples use specific constants. PaginatedList gets page navigation."

## Clarifications

### Session 2026-03-16

- Q: How should pagination navigation work — methods on PaginatedList, a standalone iterator, or params-only helpers? → A: Keep PaginatedList as a data-only model; add a standalone `paginate()` iterator/helper that yields all pages given an endpoint and params.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Full Filter Parameters on List Methods (Priority: P1)

As an SDK consumer, when I call `catalog.list()`, `sellers.list()`, or `lots.list()`, I can pass all swagger-defined filter parameters (e.g., title, agent, is_completed, customer_item_id) as typed keyword arguments with full IDE autocomplete and Pydantic validation, not just page/page_size.

**Why this priority**: The list methods currently expose only pagination params. All swagger-defined filter params (8 for catalog, 4 for sellers, 3 for lots) are inaccessible from the method signature, forcing users to bypass the SDK or construct raw dicts.

**Independent Test**: Call `catalog.list(title="Fall 2026")` and verify the request sends `?Title=Fall+2026` to the API, with the parameter validated by the params model.

**Acceptance Scenarios**:

1. **Given** a catalog list method, **When** a developer calls `catalog.list(agent="Smith")`, **Then** the request includes `?Agent=Smith` in query params and the IDE provides autocomplete for all filter parameters.
2. **Given** a seller list method, **When** a developer calls `sellers.list(is_active=True)`, **Then** the request includes `?IsActive=true` and invalid parameter names raise a validation error.
3. **Given** a lot list method, **When** a developer calls `lots.list(lot_number="L001")`, **Then** the request includes `?LotNumber=L001`.
4. **Given** any list method, **When** a developer passes an invalid parameter type (e.g., `catalog.list(id="not_an_int")`), **Then** a validation error is raised before the HTTP request.

---

### User Story 2 - Pagination Navigation on Response Objects (Priority: P2)

As an SDK consumer, when I receive a paginated list response, I can easily navigate to the next or previous page without manually constructing parameters, so I can iterate through large result sets efficiently.

**Why this priority**: Paginated responses currently return metadata (has_next_page, total_pages) but provide no convenient way to fetch the next page. Users must manually track page numbers and re-call the list method.

**Independent Test**: Call `catalog.list()`, receive a paginated response, and call a navigation method to fetch the next page.

**Acceptance Scenarios**:

1. **Given** a catalog list endpoint and params, **When** a developer calls the paginate helper, **Then** it yields successive pages of results automatically.
2. **Given** a paginate helper iterating through pages, **When** the last page is reached, **Then** iteration stops cleanly (no error).
3. **Given** a paginate helper, **When** a developer iterates through all pages, **Then** every item across all pages is accessible without duplicates.

---

### User Story 3 - Examples and Tests with Realistic Constants (Priority: P2)

As a developer maintaining or learning the SDK, when I look at examples and tests for catalog/seller/lot operations, I see realistic test constants (e.g., CATALOG_CUSTOMER_SELLER_ID = 1103, CATALOG_CUSTOMER_CATALOG_ID = 398425) that demonstrate proper usage of filter parameters and produce meaningful results against the staging API.

**Why this priority**: Current examples only demonstrate `list(page=1, page_size=25)` with no filter params. Realistic constants and filter examples serve as living documentation and enable fixture capture for filtered queries.

**Independent Test**: Run catalog/seller/lot examples against staging and verify they use filter constants and capture fixtures with filtered results.

**Acceptance Scenarios**:

1. **Given** the catalog example file, **When** a developer reads it, **Then** it demonstrates listing with at least one filter parameter using a defined constant.
2. **Given** the test suite, **When** catalog list tests run, **Then** they use named constants (not magic numbers) for seller IDs, catalog IDs, etc.
3. **Given** all three example files (catalog, sellers, lots), **When** run against staging, **Then** they produce meaningful fixture data showing filtered results.

---

### User Story 4 - Docstrings on All Endpoint Methods (Priority: P3)

As an SDK consumer, when I hover over any catalog/seller/lot endpoint method in my IDE, I see a docstring describing the method's purpose, its parameters with types and descriptions, and the return type.

**Why this priority**: Docstrings complete the IDE discoverability story. Typed params without descriptions still require documentation lookup.

**Independent Test**: Hover over `catalog.list()` in an IDE and verify the docstring shows all parameters with types and descriptions.

**Acceptance Scenarios**:

1. **Given** any catalog/seller/lot endpoint method, **When** a developer views its docstring, **Then** it includes a one-line summary, parameter descriptions with types, and the return type.
2. **Given** the list methods, **When** a developer views the docstring, **Then** each filter parameter is documented with its purpose.

---

### Edge Cases

- What happens when a user passes both a params model instance and keyword arguments? (Keyword arguments should take precedence or raise a clear error.)
- What happens when `seller_ids` is passed as a single integer instead of a list? (Should coerce or raise a validation error.)
- What happens when pagination params exceed the available data (e.g., page 999)? (API returns empty items, SDK should handle gracefully.)
- What happens when date filter params are passed in wrong format? (Pydantic validation should catch this before the HTTP call.)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The `catalog.list()` method MUST accept all swagger-defined query parameters as typed keyword arguments: id, customer_catalog_id, agent, title, start_date, end_date, is_completed, seller_ids, page_size, page_number.
- **FR-002**: The `sellers.list()` method MUST accept all swagger-defined query parameters: id, name, customer_display_id, is_active, page_size, page_number.
- **FR-003**: The `lots.list()` method MUST accept all swagger-defined query parameters: id, customer_item_id, lot_number, page_size, page_number.
- **FR-004**: All keyword arguments MUST be validated against their respective params model before the HTTP request is sent.
- **FR-005**: All list method parameters MUST have proper type hints visible to IDEs and type checkers.
- **FR-006**: All catalog/seller/lot endpoint methods MUST have docstrings documenting purpose, parameters, and return types.
- **FR-007**: The SDK MUST provide a standalone paginate helper/iterator that yields all pages given a list endpoint and optional filter params.
- **FR-008**: The PaginatedList response model MUST remain a data-only model with no HTTP client references.
- **FR-009**: Examples MUST use named constants (CATALOG_CUSTOMER_SELLER_ID = 1103, CATALOG_CUSTOMER_CATALOG_ID = 398425, etc.) for test data values.
- **FR-010**: Tests MUST use the same named constants, not magic numbers.
- **FR-011**: All create/update endpoint methods MUST validate request bodies against their Pydantic request models before sending.

### Key Entities

- **CatalogListParams**: Query parameter model for catalog list filtering (10 fields per swagger).
- **SellerListParams**: Query parameter model for seller list filtering (6 fields per swagger).
- **LotListParams**: Query parameter model for lot list filtering (5 fields per swagger).
- **PaginatedList**: Generic paginated response wrapper; gains page navigation capabilities.
- **Test Constants**: Named values for catalog/seller/lot IDs used across examples and tests.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of swagger-defined query parameters for catalog/seller/lot list endpoints are accessible as typed keyword arguments on the SDK methods.
- **SC-002**: All catalog/seller/lot endpoint methods have docstrings visible in IDE hover.
- **SC-003**: A standalone paginate helper iterates through all pages of any list endpoint without manual page tracking.
- **SC-004**: All examples and tests use named constants for test data values (zero magic numbers for entity IDs).
- **SC-005**: Invalid parameter types or names are caught by validation before the HTTP request (verified by unit tests).
- **SC-006**: All existing tests continue to pass after the changes.

## Assumptions

- The existing params model classes (CatalogListParams, SellerListParams, LotListParams) already define the correct fields — they just need to be wired into the method signatures.
- Pagination navigation will use a callback or reference to the original endpoint to fetch subsequent pages.
- The constants (CATALOG_CUSTOMER_SELLER_ID = 1103, CATALOG_CUSTOMER_CATALOG_ID = 398425) are valid IDs in the staging environment.
- The `**kwargs` endpoint pattern established in feature 007 is the mechanism for passing typed params to the request layer.
- Docstrings follow existing SDK conventions (Google-style or Sphinx-style, matching current codebase).
