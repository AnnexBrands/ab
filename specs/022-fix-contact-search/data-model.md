# Data Model: Contact Search

## Request Sub-Models (new)

### ContactSearchParams

Maps to swagger `MergeContactsSearchRequestParameters` — the `mainSearchRequest` sub-object.

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| `contact_display_id` | `Optional[int]` | `contactDisplayId` | Filter by contact display ID |
| `full_name` | `Optional[str]` | `fullName` | Filter by contact name |
| `company_name` | `Optional[str]` | `companyName` | Filter by company name |
| `company_code` | `Optional[str]` | `companyCode` | Filter by company code |
| `email` | `Optional[str]` | — | Filter by email |
| `phone` | `Optional[str]` | — | Filter by phone |
| `company_display_id` | `Optional[int]` | `companyDisplayId` | Filter by company display ID |

### PageOrderedRequest

Maps to swagger `PageOrderedRequestModel` — the `loadOptions` sub-object. Maps to C# `PagedOrderedRequest` base class.

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| `page_number` | `int` | `pageNumber` | Page number (1-based, required) |
| `page_size` | `int` | `pageSize` | Items per page (required, 1-32767) |
| `sorting_by` | `Optional[str]` | `sortingBy` | Sort field name |
| `sorting_direction` | `Optional[int]` | `sortingDirection` | Sort direction (0=asc, 1=desc) |

## Updated ContactSearchRequest

Replaces current `PaginatedRequestMixin + SearchableRequestMixin` inheritance with nested structure.

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| `main_search_request` | `Optional[ContactSearchParams]` | `mainSearchRequest` | Search filter parameters |
| `load_options` | `PageOrderedRequest` | `loadOptions` | Pagination and sorting (required) |

## Updated SearchContactEntityResult

Replaces current 5-field model with full C# source fields (22 fields).

| Field | Type | Alias | C# Source |
|-------|------|-------|-----------|
| `contact_id` | `Optional[int]` | `contactID` | `ContactID` |
| `customer_cell` | `Optional[str]` | `customerCell` | `CustomerCell` |
| `contact_display_id` | `Optional[str]` | `contactDisplayId` | `ContactDisplayId` |
| `contact_full_name` | `Optional[str]` | `contactFullName` | `ContactFullName` |
| `contact_phone` | `Optional[str]` | `contactPhone` | `ContactPhone` |
| `contact_home_phone` | `Optional[str]` | `contactHomePhone` | `ContactHomePhone` |
| `contact_email` | `Optional[str]` | `contactEmail` | `ContactEmail` |
| `master_constant_value` | `Optional[str]` | `masterConstantValue` | `MasterConstantValue` |
| `contact_dept` | `Optional[str]` | `contactDept` | `ContactDept` |
| `address1` | `Optional[str]` | — | `Address1` |
| `address2` | `Optional[str]` | — | `Address2` |
| `city` | `Optional[str]` | — | `City` |
| `state` | `Optional[str]` | — | `State` |
| `zip_code` | `Optional[str]` | `zipCode` | `ZipCode` |
| `country_name` | `Optional[str]` | `countryName` | `CountryName` |
| `company_code` | `Optional[str]` | `companyCode` | `CompanyCode` |
| `company_id` | `Optional[str]` | `companyID` | `CompanyID` (Guid?) |
| `company_name` | `Optional[str]` | `companyName` | `CompanyName` |
| `company_display_id` | `Optional[str]` | `companyDisplayId` | `CompanyDisplayId` |
| `is_prefered` | `Optional[bool]` | `isPrefered` | `IsPrefered` |
| `industry_type` | `Optional[str]` | `industryType` | `IndustryType` |
| `total_records` | `Optional[int]` | `totalRecords` | `TotalRecords` (int?) |

### Fields removed from current model

| Old Field | Old Alias | Reason |
|-----------|-----------|--------|
| `id` | — | Replaced by `contact_id` (alias `contactID`) |
| `full_name` | `fullName` | Replaced by `contact_full_name` (alias `contactFullName`) |
| `email` | — | Replaced by `contact_email` (alias `contactEmail`) |

Note: `company_name` and `contact_display_id` keep their aliases — they match C# source.
