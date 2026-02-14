# Mock Fixture Tracking

Tracks all fabricated (non-live) fixtures in `tests/fixtures/`.

## Summary

- **Live fixtures**: 22
- **Mock fixtures**: 9
- **Total**: 31

## Mock Fixtures

| Endpoint Path | HTTP Method | Model Name | Reason | Date | Status |
|---------------|-------------|------------|--------|------|--------|
| /address/isvalid | GET | AddressIsValidResult | Returns 400 with various param combos in staging | 2026-02-13 | mock |
| /address/propertytype | GET | PropertyType | Returns 204 No Content in staging | 2026-02-13 | mock |
| /lookup/items | GET | LookupItem | Returns 204 No Content in staging | 2026-02-13 | mock |
| /Catalog | GET | CatalogWithSellersDto | No catalog data in staging | 2026-02-13 | mock |
| /Catalog/{id} | GET | CatalogExpandedDto | No catalog data in staging | 2026-02-13 | mock |
| /Lot | GET | LotDto | No lot data in staging | 2026-02-13 | mock |
| /Lot/{id} | GET | LotDataDto | No lot data in staging | 2026-02-13 | mock |
| /Lot/overrides | POST | LotOverrideDto | No lot data in staging | 2026-02-13 | mock |
| /AutoPrice/QuoteRequest | POST | QuoteRequestResponse | Requires valid job/item data for certified quote | 2026-02-13 | mock |

## Live Fixtures

| Endpoint Path | HTTP Method | Model Name | Date | Status |
|---------------|-------------|------------|------|--------|
| /companies/{id} | GET | CompanySimple | 2026-02-13 | live |
| /companies/{id}/fulldetails | GET | CompanyDetails | 2026-02-13 | live |
| /companies/availableByCurrentUser | GET | SearchCompanyResponse | 2026-02-13 | live |
| /contacts/user | GET | ContactSimple | 2026-02-13 | live |
| /contacts/{id}/editdetails | GET | ContactDetailedInfo | 2026-02-13 | live |
| /contacts/{id}/primarydetails | GET | ContactPrimaryDetails | 2026-02-13 | live |
| /contacts/v2/search | POST | SearchContactEntityResult | 2026-02-13 | live |
| /job/{id} | GET | Job | 2026-02-13 | live |
| /job/{id}/price | GET | JobPrice | 2026-02-13 | live |
| /job/search | GET | JobSearchResult | 2026-02-13 | live |
| /job/{id}/calendaritems | GET | CalendarItem | 2026-02-13 | live |
| /job/{id}/updatePageConfig | GET | JobUpdatePageConfig | 2026-02-13 | live |
| /documents (embedded in Job) | GET | Document | 2026-02-13 | live |
| /lookup/contacttypes | GET | ContactTypeEntity | 2026-02-13 | live |
| /lookup/countries | GET | CountryCodeDto | 2026-02-13 | live |
| /lookup/jobstatuses | GET | JobStatus | 2026-02-13 | live |
| /Seller/{id} | GET | SellerDto | 2026-02-13 | live |
| /Seller/{id} | GET | SellerExpandedDto | 2026-02-13 | live |
| /AutoPrice/QuickQuote | POST | QuickQuoteResponse | 2026-02-13 | live |
| /Web2Lead | GET | Web2LeadResponse | 2026-02-13 | live |
| /users/list | POST | User | 2026-02-13 | live |
| /users/roles | GET | UserRole | 2026-02-13 | live |
