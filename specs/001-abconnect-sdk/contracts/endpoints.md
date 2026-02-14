# API Contracts: Core Endpoint Subset

**Branch**: `001-abconnect-sdk` | **Date**: 2026-02-13
**Total**: 59 endpoints (37 ACPortal + 17 Catalog + 5 ABC)

## ACPortal API (37 endpoints)

Base URL: `https://portal.{env}.abconnect.co/api/api`
Auth: Bearer JWT

### Companies (8)

| Method | Path | Request Model | Response Model | Schema Reliable |
|--------|------|---------------|----------------|-----------------|
| GET | `/companies/{id}` | — | CompanySimple | No |
| GET | `/companies/{companyId}/details` | — | CompanyDetails | No |
| GET | `/companies/{companyId}/fulldetails` | — | CompanyDetails | Yes |
| PUT | `/companies/{companyId}/fulldetails` | CompanyDetails | CompanyDetails | Yes |
| POST | `/companies/fulldetails` | CompanyDetails | str (id) | No |
| POST | `/companies/search/v2` | CompanySearchRequest | List[SearchCompanyResponse] | Yes |
| POST | `/companies/list` | ListRequest | List[CompanySimple] | No |
| GET | `/companies/availableByCurrentUser` | — | List[CompanySimple] | No |

### Contacts (7)

| Method | Path | Request Model | Response Model | Schema Reliable |
|--------|------|---------------|----------------|-----------------|
| GET | `/contacts/{id}` | — | ContactSimple | No |
| GET | `/contacts/{contactId}/editdetails` | — | ContactDetailedInfo | Yes |
| PUT | `/contacts/{contactId}/editdetails` | ContactEditRequest | — | No |
| POST | `/contacts/editdetails` | ContactEditRequest | — | No |
| POST | `/contacts/v2/search` | ContactSearchRequest | List[SearchContactEntityResult] | Yes |
| GET | `/contacts/{contactId}/primarydetails` | — | ContactPrimaryDetails | Yes |
| GET | `/contacts/user` | — | ContactSimple | No |

### Jobs (8)

| Method | Path | Request Model | Response Model | Schema Reliable |
|--------|------|---------------|----------------|-----------------|
| POST | `/job` | JobCreateRequest | — | No |
| PUT | `/job/save` | JobSaveRequest | — | No |
| GET | `/job/{jobDisplayId}` | — | Job | No |
| GET | `/job/search` | — (query params) | List[JobSearchResult] | No |
| POST | `/job/searchByDetails` | JobSearchRequest | List[JobSearchResult] | No |
| GET | `/job/{jobDisplayId}/price` | — | JobPrice | No |
| GET | `/job/{jobDisplayId}/calendaritems` | — | List[CalendarItem] | No |
| GET | `/job/{jobDisplayId}/updatePageConfig` | — | JobUpdatePageConfig | Yes |

### Documents (4)

| Method | Path | Request Model | Response Model | Schema Reliable |
|--------|------|---------------|----------------|-----------------|
| POST | `/documents` | multipart (file) | — | No |
| GET | `/documents/list` | — (query params) | List[Document] | No |
| GET | `/documents/get/{docPath}` | — | bytes | No |
| PUT | `/documents/update/{docId}` | DocumentUpdateRequest | — | No |

### Address (2)

| Method | Path | Request Model | Response Model | Schema Reliable |
|--------|------|---------------|----------------|-----------------|
| GET | `/address/isvalid` | — (query params) | AddressIsValidResult | Yes |
| GET | `/address/propertytype` | — (query params) | PropertyType | Yes |

### Lookup (4)

| Method | Path | Request Model | Response Model | Schema Reliable |
|--------|------|---------------|----------------|-----------------|
| GET | `/lookup/contactTypes` | — | List[ContactTypeEntity] | Yes |
| GET | `/lookup/countries` | — | List[CountryCodeDto] | Yes |
| GET | `/lookup/jobStatuses` | — | List[JobStatus] | No |
| GET | `/lookup/items` | — | List[LookupItem] | No |

### Users (4)

| Method | Path | Request Model | Response Model | Schema Reliable |
|--------|------|---------------|----------------|-----------------|
| POST | `/users/list` | ListRequest | List[User] | No |
| GET | `/users/roles` | — | List[UserRole] | No |
| POST | `/users/user` | UserCreateRequest | — | No |
| PUT | `/users/user` | UserUpdateRequest | — | No |

## Catalog API (17 endpoints)

Base URL: `https://catalog-api.{env}.abconnect.co/api`
Auth: Bearer JWT

### Catalog (6)

| Method | Path | Request Model | Response Model | Schema Reliable |
|--------|------|---------------|----------------|-----------------|
| POST | `/Catalog` | AddCatalogRequest | CatalogWithSellersDto | Yes |
| GET | `/Catalog` | — (query params) | PaginatedList[CatalogExpandedDto] | Yes |
| GET | `/Catalog/{id}` | — | CatalogExpandedDto | Yes |
| PUT | `/Catalog/{id}` | UpdateCatalogRequest | CatalogWithSellersDto | Yes |
| DELETE | `/Catalog/{id}` | — | — (204) | Yes |
| POST | `/Bulk/insert` | BulkInsertRequest | — | No |

### Lots (5)

| Method | Path | Request Model | Response Model | Schema Reliable |
|--------|------|---------------|----------------|-----------------|
| POST | `/Lot` | AddLotRequest | LotDto | Yes |
| GET | `/Lot` | — (query params) | PaginatedList[LotDto] | Yes |
| GET | `/Lot/{id}` | — | LotDto | Yes |
| PUT | `/Lot/{id}` | UpdateLotRequest | LotDto | Yes |
| DELETE | `/Lot/{id}` | — | — (204) | Yes |
| POST | `/Lot/get-overrides` | List[str] | List[LotOverrideDto] | Yes |

### Sellers (5)

| Method | Path | Request Model | Response Model | Schema Reliable |
|--------|------|---------------|----------------|-----------------|
| POST | `/Seller` | AddSellerRequest | SellerDto | Yes |
| GET | `/Seller` | — (query params) | PaginatedList[SellerExpandedDto] | Yes |
| GET | `/Seller/{id}` | — | SellerExpandedDto | Yes |
| PUT | `/Seller/{id}` | UpdateSellerRequest | SellerDto | Yes |
| DELETE | `/Seller/{id}` | — | — (204) | Yes |

## ABC API (5 endpoints)

Base URL: `https://api.{env}.abconnect.co/api`
Auth: Bearer JWT + accessKey

### AutoPrice (2)

| Method | Path | Request Model | Response Model | Schema Reliable |
|--------|------|---------------|----------------|-----------------|
| POST | `/autoprice/quickquote` | QuoteRequestModel | QuickQuoteResponse | No |
| POST | `/autoprice/v2/quoterequest` | QuoteRequestModel | QuoteRequestResponse | No |

### Job (1)

| Method | Path | Request Model | Response Model | Schema Reliable |
|--------|------|---------------|----------------|-----------------|
| POST | `/job/update` | JobUpdateRequest | — | No |

### Web2Lead (2)

| Method | Path | Request Model | Response Model | Schema Reliable |
|--------|------|---------------|----------------|-----------------|
| GET | `/Web2Lead/get` | — (query params) | Web2LeadResponse | No |
| POST | `/Web2Lead/post` | Web2LeadRequest | Web2LeadResponse | No |

## Schema Reliability Summary

| Rating | Count | Action |
|--------|-------|--------|
| Reliable | 24 | Model from swagger, validate with fixture |
| Not reliable | 35 | Model from fixture only, document swagger deviation |

## Route Definition Convention

Each endpoint MUST have a Route entry:

```python
Route(
    method="GET",
    path="/companies/{companyId}/fulldetails",
    request_model=None,
    response_model="CompanyDetails",
)
```

Route is frozen (immutable). Use `route.bind(companyId=uuid)` to
create a bound copy with params applied.
