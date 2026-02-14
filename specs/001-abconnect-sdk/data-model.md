# Data Model: ABConnect API SDK

**Branch**: `001-abconnect-sdk` | **Date**: 2026-02-13

## Model Hierarchy

### Base Classes

```
ABConnectBaseModel
├── RequestModel          # extra="forbid" — strict outbound
└── ResponseModel         # extra="ignore" — lenient inbound
```

### Mixins (composed via multiple inheritance)

```
IdentifiedModel           # id: Optional[str | int]
TimestampedModel          # created_date, modified_date, created_by, modified_by
ActiveModel               # is_active: Optional[bool]
CompanyRelatedModel       # company_id, company_name
JobRelatedModel           # job_id
```

### Composite Mixins

```
FullAuditModel = IdentifiedModel + TimestampedModel + ActiveModel
CompanyAuditModel = FullAuditModel + CompanyRelatedModel
JobAuditModel = FullAuditModel + JobRelatedModel
```

### Shared Response Patterns

```
ServiceBaseResponse       # success, error_message; __bool__, raise_for_error()
ServiceWarningResponse    # extends ServiceBaseResponse with warning_message
PaginatedList[T]          # items, page_number, total_pages, total_items,
                          # has_previous_page, has_next_page (Catalog pattern)
```

## Entity Models (Core Subset)

### Companies (ACPortal)

| Model | Base | Key Fields | Source |
|-------|------|------------|--------|
| CompanySimple | ResponseModel | id, name, code, company_type | GET /companies/{id} |
| CompanyDetails | ResponseModel + FullAuditModel | addresses, contacts, capabilities, settings | GET /companies/{id}/fulldetails |
| SearchCompanyResponse | ResponseModel | id, name, code, city, state | POST /companies/search/v2 |
| CompanySearchRequest | RequestModel | search_text, page, page_size, filters | POST /companies/search/v2 |
| ListRequest | RequestModel | page, page_size, filters, sort_by | POST /companies/list, POST /users/list |

### Contacts (ACPortal)

| Model | Base | Key Fields | Source |
|-------|------|------------|--------|
| ContactSimple | ResponseModel + IdentifiedModel | first_name, last_name, email, phone | GET /contacts/{id} |
| ContactDetailedInfo | ResponseModel + FullAuditModel | addresses, phones, emails, company_info | GET /contacts/{id}/editdetails |
| ContactPrimaryDetails | ResponseModel | id, full_name, email, phone, company | GET /contacts/{id}/primarydetails |
| SearchContactEntityResult | ResponseModel | id, name, email, company_name | POST /contacts/v2/search |
| ContactEditRequest | RequestModel | first_name, last_name, email, phone, addresses | PUT /contacts/{id}/editdetails |
| ContactSearchRequest | RequestModel | search_text, page, page_size | POST /contacts/v2/search |

### Jobs (ACPortal)

| Model | Base | Key Fields | Source |
|-------|------|------------|--------|
| Job | ResponseModel + FullAuditModel | job_display_id, status, customer, pickup, delivery, items | GET /job/{jobDisplayId} |
| JobSearchResult | ResponseModel | job_display_id, status, customer_name, agent | GET /job/search |
| JobUpdatePageConfig | ResponseModel | config fields per swagger | GET /job/{id}/updatePageConfig |
| JobCreateRequest | RequestModel | customer, pickup, delivery, items, services | POST /job |
| JobSaveRequest | RequestModel | job fields for update | PUT /job/save |
| JobSearchRequest | RequestModel | search criteria, page, page_size | POST /job/searchByDetails |
| JobUpdateRequest | RequestModel | job fields for ABC API update | POST /job/update (ABC API) |

### Documents (ACPortal)

| Model | Base | Key Fields | Source |
|-------|------|------------|--------|
| Document | ResponseModel + IdentifiedModel | doc_path, doc_type, file_name, sharing_level | GET /documents/list |
| DocumentUploadRequest | — (multipart form) | file, document_type, job_id, sharing_level | POST /documents (not a Pydantic model; handled as multipart upload) |

### Address (ACPortal)

| Model | Base | Key Fields | Source |
|-------|------|------------|--------|
| AddressIsValidResult | ResponseModel | is_valid, validated_address, suggestions | GET /address/isvalid |
| PropertyType | ResponseModel | property_type, confidence | GET /address/propertytype |

### Lookup (ACPortal)

| Model | Base | Key Fields | Source |
|-------|------|------------|--------|
| ContactTypeEntity | ResponseModel | id, name, description | GET /lookup/contactTypes |
| CountryCodeDto | ResponseModel | code, name | GET /lookup/countries |

### Users (ACPortal)

| Model | Base | Key Fields | Source |
|-------|------|------------|--------|
| User | ResponseModel + IdentifiedModel | username, email, roles, company | POST /users/list |
| UserRole | ResponseModel | id, name | GET /users/roles |

### Catalog (Catalog API)

| Model | Base | Key Fields | Source |
|-------|------|------------|--------|
| CatalogWithSellersDto | ResponseModel | id, title, agent_id, sellers, lots | POST /Catalog |
| CatalogExpandedDto | ResponseModel | id, title, sellers, lot_count, status | GET /Catalog/{id} |
| AddCatalogRequest | RequestModel | title, agent_id, seller_ids | POST /Catalog |
| UpdateCatalogRequest | RequestModel | title, agent_id, seller_ids | PUT /Catalog/{id} |
| BulkInsertRequest | RequestModel | catalog_id, items | POST /Bulk/insert |

### Lots (Catalog API)

| Model | Base | Key Fields | Source |
|-------|------|------------|--------|
| LotDto | ResponseModel | id, catalog_id, lot_number, customer_item_id, data | POST /Lot |
| LotOverrideDto | ResponseModel | customer_item_id, overrides | POST /Lot/get-overrides |
| LotDataDto | ResponseModel | qty, l, w, h, wgt, value, description | nested in LotDto |
| AddLotRequest | RequestModel | catalog_id, lot_number, data | POST /Lot |
| UpdateLotRequest | RequestModel | lot_number, data | PUT /Lot/{id} |

### Sellers (Catalog API)

| Model | Base | Key Fields | Source |
|-------|------|------------|--------|
| SellerDto | ResponseModel | id, name, display_id | POST /Seller |
| SellerExpandedDto | ResponseModel | id, name, display_id, catalogs | GET /Seller/{id} |
| AddSellerRequest | RequestModel | name, display_id | POST /Seller |
| UpdateSellerRequest | RequestModel | name, display_id | PUT /Seller/{id} |

### AutoPrice (ABC API)

| Model | Base | Key Fields | Source |
|-------|------|------------|--------|
| QuickQuoteResponse | ResponseModel | quotes, errors | POST /autoprice/quickquote |
| QuoteRequestResponse | ResponseModel | quote_id, status, results | POST /autoprice/v2/quoterequest |
| QuoteRequestModel | RequestModel | job_info, contact_info, service_info, items | POST /autoprice/v2/quoterequest |

### Web2Lead (ABC API)

| Model | Base | Key Fields | Source |
|-------|------|------------|--------|
| Web2LeadResponse | ResponseModel | success, lead_id | POST /Web2Lead/post |
| Web2LeadRequest | RequestModel | name, email, phone, company, message | POST /Web2Lead/post |

## Pagination Wrapper

The Catalog API uses a consistent pagination pattern:

```
PaginatedList[T]
├── items: List[T]
├── page_number: int
├── total_pages: int
├── total_items: int
├── has_previous_page: bool
└── has_next_page: bool
```

This generic wrapper MUST be reusable for any paginated Catalog
endpoint. ACPortal pagination patterns will be determined from
fixtures once captured.

## Model Field Conventions

- All fields use `Field(alias="camelCase")` for API compatibility.
- `populate_by_name=True` allows both snake_case and camelCase input.
- All nullable fields MUST be `Optional[T] = None`.
- Field descriptions MUST be provided for Sphinx autodoc.
- Swagger deviations MUST be documented with inline comments.

## State Transitions

### Mock → Live Fixture

```
mock (fabricated JSON) → fixture captured → model validated → mock
entry in MOCKS.md updated to status "live"
```

### Token Lifecycle

```
no_token → password_grant → token_active → (expiry - 300s) →
refresh_grant → token_active → ... → refresh_fails →
password_grant → token_active
```

## Notes

- All model field names and types listed above are preliminary and
  MUST be validated against actual API fixtures once captured.
- ACPortal response schemas are mostly undocumented in swagger;
  the field lists above are inferred from ABConnectTools patterns
  and will be corrected during fixture-driven development.
- Catalog API schemas are well-documented and should closely match
  swagger definitions.
