# Mock Fixture Tracking

Tracks all fabricated (non-live) fixtures in `tests/fixtures/`.

## Summary

- **Live fixtures**: 12
- **Mock fixtures**: 19
- **Total**: 31

## Mock Fixtures

| Endpoint Path | HTTP Method | Model Name | Reason | Date | Status |
|---------------|-------------|------------|--------|------|--------|
| /address/isvalid | GET | AddressIsValidResult | Returns 400 with various param combos in staging | 2026-02-13 | mock |
| /address/propertytype | GET | PropertyType | Returns 204 No Content in staging | 2026-02-13 | mock |
| /job/{id} | GET | Job | No known job display IDs in staging | 2026-02-13 | mock |
| /job/{id}/price | GET | JobPrice | No known job display IDs in staging | 2026-02-13 | mock |
| /job/search | GET | JobSearchResult | No known job display IDs in staging | 2026-02-13 | mock |
| /job/{id}/calendaritems | GET | CalendarItem | No known job display IDs in staging | 2026-02-13 | mock |
| /job/{id}/updatePageConfig | GET | JobUpdatePageConfig | No known job display IDs in staging | 2026-02-13 | mock |
| /document/list | GET | Document | Requires valid job ID with documents | 2026-02-13 | mock |
| /lookup/items | GET | LookupItem | Returns 204 No Content in staging | 2026-02-13 | mock |
| /companies/search/v2 | POST | SearchCompanyResponse | Returns 500 in staging | 2026-02-13 | mock |
| /Catalog | GET | CatalogWithSellersDto | No catalog data in staging | 2026-02-13 | mock |
| /Catalog/{id} | GET | CatalogExpandedDto | No catalog data in staging | 2026-02-13 | mock |
| /Lot | GET | LotDto | No lot data in staging | 2026-02-13 | mock |
| /Lot/{id} | GET | LotDataDto | No lot data in staging | 2026-02-13 | mock |
| /Lot/overrides | POST | LotOverrideDto | No lot data in staging | 2026-02-13 | mock |
| /Seller/{id} | GET | SellerDto | Basic seller without expanded fields | 2026-02-13 | mock |
| /AutoPrice/QuickQuote | POST | QuickQuoteResponse | Requires ABC API accessKey | 2026-02-13 | mock |
| /AutoPrice/QuoteRequest | POST | QuoteRequestResponse | Requires ABC API accessKey | 2026-02-13 | mock |
| /Web2Lead | GET | Web2LeadResponse | Requires ABC API accessKey | 2026-02-13 | mock |

## Live Fixtures

| Endpoint Path | HTTP Method | Model Name | Date | Status |
|---------------|-------------|------------|------|--------|
| /companies/{id} | GET | CompanySimple | 2026-02-13 | live |
| /companies/{id}/fulldetails | GET | CompanyDetails | 2026-02-13 | live |
| /contacts/user | GET | ContactSimple | 2026-02-13 | live |
| /contacts/{id}/editdetails | GET | ContactDetailedInfo | 2026-02-13 | live |
| /contacts/{id}/primarydetails | GET | ContactPrimaryDetails | 2026-02-13 | live |
| /contacts/{id}/editdetails | GET | SearchContactEntityResult | 2026-02-13 | live |
| /lookup/contacttypes | GET | ContactTypeEntity | 2026-02-13 | live |
| /lookup/countries | GET | CountryCodeDto | 2026-02-13 | live |
| /lookup/jobstatuses | GET | JobStatus | 2026-02-13 | live |
| /Seller/{id} | GET | SellerExpandedDto | 2026-02-13 | live |
| /users/list | POST | User | 2026-02-13 | live |
| /users/roles | GET | UserRole | 2026-02-13 | live |
