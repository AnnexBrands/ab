# Research: Contact Search C# Source Analysis

## Decision: Use C# `SearchContactEntityResult` entity as response field source

**Rationale**: Constitution Sources of Truth ranks API server source as Tier 1. The C# entity is at `/src/ABConnect/AB.ABCEntities/ContactEntities/SearchContactEntityResult.cs` with 22 properties. Swagger confirms the same 22 fields. The current Python model has only 5 fields with wrong alias names (e.g., `id` instead of `contactID`, `full_name` instead of `contactFullName`).

**Alternatives considered**: Using the mislabeled fixture (rejected — it contains `ContactDetailedInfo` data, not search results).

## Decision: Use swagger `MergeContactsSearchRequestModel` as request structure source

**Rationale**: The C# controller for `/contacts/v2/search` was not found in the source tree. The older `/contacts/search` (v1) uses DevExtreme's `WebApiDataSourceLoadOptions` binding, which is a different pattern. However, the swagger spec defines `MergeContactsSearchRequestModel` with nested `mainSearchRequest` + `loadOptions`, and the captured request fixture matches this shape exactly. The swagger is therefore the best available source for the v2 request structure.

The C# `SearchContactRequest` entity (at `AB.ABCEntities/ContactEntities/SearchContactRequest.cs`) extends `PagedOrderedRequest` and has additional fields (City, State, ZipCode, UserId, Type) beyond what swagger/fixture show. These may be service-layer parameters not exposed in the v2 API.

**Alternatives considered**: Inheriting from `PaginatedRequestMixin` + `SearchableRequestMixin` (rejected — the API expects a nested structure, not flat fields).

## Decision: Replace mislabeled response fixture with mock

**Rationale**: `tests/fixtures/SearchContactEntityResult.json` currently contains a `ContactDetailedInfo` object (434 lines with emailsList, addressesList, editable, etc.). This is clearly wrong — a search result entity should be a flat object with ~22 fields per the C# source. Since live API re-capture requires staging access, we create a mock fixture at `tests/fixtures/mocks/SearchContactEntityResult.json` matching the C# schema. The gate evaluator already supports mock fixtures (G2 checks mocks/ fallback).

## Decision: Drop `ContactSearchRequest` inheritance from mixins, use nested structure

**Rationale**: The current model inherits `PaginatedRequestMixin` (page, pageSize) + `SearchableRequestMixin` (searchText). But the API expects:
```json
{
  "mainSearchRequest": { "fullName": "...", "email": "...", ... },
  "loadOptions": { "pageNumber": 1, "pageSize": 10, ... }
}
```
The mixin-provided flat fields (`page`, `pageSize`, `searchText`) will be sent at the wrong nesting level, causing HTTP 400. The model must be restructured with typed sub-models.

## C# Source Cross-Reference

### SearchContactEntityResult (Response)

Source: `/src/ABConnect/AB.ABCEntities/ContactEntities/SearchContactEntityResult.cs`

| C# Property | C# Type | Python Field | Python Type | Alias |
|---|---|---|---|---|
| `ContactID` | `int` | `contact_id` | `Optional[int]` | `contactID` |
| `CustomerCell` | `string` | `customer_cell` | `Optional[str]` | `customerCell` |
| `ContactDisplayId` | `string` | `contact_display_id` | `Optional[str]` | `contactDisplayId` |
| `ContactFullName` | `string` | `contact_full_name` | `Optional[str]` | `contactFullName` |
| `ContactPhone` | `string` | `contact_phone` | `Optional[str]` | `contactPhone` |
| `ContactHomePhone` | `string` | `contact_home_phone` | `Optional[str]` | `contactHomePhone` |
| `ContactEmail` | `string` | `contact_email` | `Optional[str]` | `contactEmail` |
| `MasterConstantValue` | `string` | `master_constant_value` | `Optional[str]` | `masterConstantValue` |
| `ContactDept` | `string` | `contact_dept` | `Optional[str]` | `contactDept` |
| `Address1` | `string` | `address1` | `Optional[str]` | — |
| `Address2` | `string` | `address2` | `Optional[str]` | — |
| `City` | `string` | `city` | `Optional[str]` | — |
| `State` | `string` | `state` | `Optional[str]` | — |
| `ZipCode` | `string` | `zip_code` | `Optional[str]` | `zipCode` |
| `CountryName` | `string` | `country_name` | `Optional[str]` | `countryName` |
| `CompanyCode` | `string` | `company_code` | `Optional[str]` | `companyCode` |
| `CompanyID` | `Guid?` | `company_id` | `Optional[str]` | `companyID` |
| `CompanyName` | `string` | `company_name` | `Optional[str]` | `companyName` |
| `CompanyDisplayId` | `string` | `company_display_id` | `Optional[str]` | `companyDisplayId` |
| `IsPrefered` | `bool` | `is_prefered` | `Optional[bool]` | `isPrefered` |
| `IndustryType` | `string` | `industry_type` | `Optional[str]` | `industryType` |
| `TotalRecords` | `int?` | `total_records` | `Optional[int]` | `totalRecords` |

### PagedOrderedRequest (Pagination base)

Source: `/src/ABConnect/AB.ABCEntities/Common/PagedOrderedRequest.cs` + `PagedRequest.cs`

| C# Property | C# Type | Swagger Name | Notes |
|---|---|---|---|
| `PageIndex` | `int` | `pageNumber` | Swagger renames to pageNumber |
| `PageSize` | `int` | `pageSize` | Same name |
| `TotalCount` | `int` | — | Not in swagger request |
| `SortingBy` | `string` | `sortingBy` | Same name |
| `SortingDirection` | `ListSortDirection` | `sortingDirection` | Enum: 0=Ascending, 1=Descending |

### MergeContactsSearchRequestParameters (Search fields)

Source: Swagger (C# controller for v2 not found in source tree)

| Swagger Property | Type | Notes |
|---|---|---|
| `contactDisplayId` | `int?` | Filter by display ID |
| `fullName` | `string?` | Filter by name |
| `companyName` | `string?` | Filter by company name |
| `companyCode` | `string?` | Filter by company code |
| `email` | `string?` | Filter by email |
| `phone` | `string?` | Filter by phone |
| `companyDisplayId` | `int?` | Filter by company display ID |

### Fields to REMOVE from current Python model

The current `SearchContactEntityResult` has these fields that use wrong names:

| Current Field | Current Alias | Should Be | Correct Alias |
|---|---|---|---|
| `id` | — | `contact_id` | `contactID` |
| `full_name` | `fullName` | `contact_full_name` | `contactFullName` |
| `email` | — | `contact_email` | `contactEmail` |
| `company_name` | `companyName` | `company_name` | `companyName` (keep) |
| `contact_display_id` | `contactDisplayId` | `contact_display_id` | `contactDisplayId` (keep) |

Note: `contact_display_id` and `company_name` have correct aliases already. The other 3 fields need renamed aliases to match C# property casing.
