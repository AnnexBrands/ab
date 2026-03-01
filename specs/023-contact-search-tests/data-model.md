# Data Model: Contact Search Tests

This feature creates no new models. It tests existing models from feature 022.

## Models Under Test

### ContactSearchRequest (request body)

Top-level body for `POST /contacts/v2/search`. Uses `RequestModel` base (`extra="forbid"`).

| Field | Type | Required | Alias | Notes |
|-------|------|----------|-------|-------|
| `main_search_request` | `Optional[ContactSearchParams]` | No | `mainSearchRequest` | Omittable for unfiltered search |
| `load_options` | `PageOrderedRequest` | **Yes** | `loadOptions` | Pagination is mandatory |

### ContactSearchParams (nested sub-model)

7 optional filter fields within `mainSearchRequest`.

| Field | Type | Alias |
|-------|------|-------|
| `contact_display_id` | `Optional[int]` | `contactDisplayId` |
| `full_name` | `Optional[str]` | `fullName` |
| `company_name` | `Optional[str]` | `companyName` |
| `company_code` | `Optional[str]` | `companyCode` |
| `email` | `Optional[str]` | `email` |
| `phone` | `Optional[str]` | `phone` |
| `company_display_id` | `Optional[int]` | `companyDisplayId` |

### PageOrderedRequest (nested sub-model)

2 required + 2 optional pagination/sort fields within `loadOptions`.

| Field | Type | Required | Alias |
|-------|------|----------|-------|
| `page_number` | `int` | **Yes** | `pageNumber` |
| `page_size` | `int` | **Yes** | `pageSize` |
| `sorting_by` | `Optional[str]` | No | `sortingBy` |
| `sorting_direction` | `Optional[int]` | No | `sortingDirection` |

### SearchContactEntityResult (response)

22-field response model. All fields Optional. Tested against mock fixture.

See `specs/022-fix-contact-search/data-model.md` for the full 22-field mapping.

## Fixture Sources

| Fixture | Path | Type |
|---------|------|------|
| Request | `tests/fixtures/requests/ContactSearchRequest.json` | Live-captured |
| Response | `tests/fixtures/mocks/SearchContactEntityResult.json` | Mock (C# sourced) |
