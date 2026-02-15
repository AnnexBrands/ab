# Fixture Tracking

Tracks capture status for all endpoint fixtures in `tests/fixtures/`.

**Constitution**: v2.2.0, Principles II & V
**Rule**: Fabricated fixtures are prohibited. Failed API calls
mean the example needs correct request data — not a response
fixture. See Principle II (Example-Driven Fixture Capture).

## Summary

- **Captured (response)**: 24
- **Captured (request)**: 1
- **Needs Request Data**: 26
- **Total tracked**: 50

## Status Legend

- **captured**: Fixture file exists and validates against model
- **needs-data**: Example fails — see Notes for what's missing
- **—**: Not applicable (e.g., GET with no request body)

## ACPortal Endpoints

| Endpoint Path | Method | Req Model | Req Fixture | Resp Model | Resp Fixture | Status | Notes |
|---------------|--------|-----------|-------------|------------|--------------|--------|-------|
| /companies/{id} | GET | — | — | CompanySimple | captured | complete | 2026-02-13, staging |
| /companies/{id}/details | GET | — | — | CompanyDetails | needs-data | partial | HTTP 500 on staging — needs company UUID with populated details |
| /companies/{id}/fulldetails | GET | — | — | CompanyDetails | captured | complete | 2026-02-13, staging |
| /companies/{companyId}/fulldetails | PUT | CompanyDetails | needs-data | CompanyDetails | needs-data | needs-request-data | Needs valid CompanyDetails kwargs |
| /companies/fulldetails | POST | CompanyDetails | needs-data | str | needs-data | needs-request-data | Needs valid CompanyDetails kwargs for new company |
| /companies/search/v2 | POST | CompanySearchRequest | captured | List[SearchCompanyResponse] | needs-data | partial | Request fixture captured; response needs valid search that returns results |
| /companies/list | POST | ListRequest | needs-data | List[CompanySimple] | needs-data | needs-request-data | Needs valid ListRequest kwargs |
| /companies/availableByCurrentUser | GET | — | — | SearchCompanyResponse | captured | complete | 2026-02-13, staging |
| /contacts/user | GET | — | — | ContactSimple | captured | complete | 2026-02-13, staging |
| /contacts/{id}/primarydetails | GET | — | — | ContactPrimaryDetails | captured | complete | 2026-02-13, staging |
| /contacts/{id}/editdetails | GET | — | — | ContactDetailedInfo | needs-data | needs-request-data | HTTP 500 on staging — was previously captured but now fails |
| /contacts/v2/search | POST | SearchContactEntityResult | needs-data | SearchContactEntityResult | needs-data | needs-request-data | HTTP 400 — needs PageSize (1-32767) and PageNumber (1-32767) in request body |
| /documents | GET | — | — | Document | needs-data | needs-request-data | HTTP 500 on staging — was previously captured but now fails |
| /address/isvalid | GET | — | — | AddressIsValidResult | captured | complete | 2026-02-14, staging |
| /address/propertytype | GET | — | — | PropertyType | needs-data | needs-request-data | Query params: needs valid address1, city, state, zip_code for a real address |
| /lookup/contacttypes | GET | — | — | ContactTypeEntity | captured | complete | 2026-02-13, staging |
| /lookup/countries | GET | — | — | CountryCodeDto | captured | complete | 2026-02-13, staging |
| /lookup/jobstatuses | GET | — | — | JobStatus | captured | complete | 2026-02-13, staging |
| /lookup/items | GET | — | — | LookupItem | needs-data | needs-request-data | Returns 204 — research ABConnectTools for required query params |
| /users/list | POST | — | — | User | captured | partial | 2026-02-13, staging. Model warning: response is paginated wrapper (totalCount, data) |
| /users/roles | GET | — | — | UserRole | needs-data | needs-request-data | Model mismatch — API returns list of strings, model expects dict |
| /job/{id} | GET | — | — | Job | needs-data | needs-request-data | HTTP 500 on staging |
| /job/{id}/price | GET | — | — | JobPrice | captured | complete | 2026-02-13, staging |
| /job/{id}/calendaritems | GET | — | — | CalendarItem | captured | complete | 2026-02-13, staging |
| /job/{id}/updatePageConfig | GET | — | — | JobUpdatePageConfig | captured | complete | 2026-02-13, staging |
| /job/search | GET | — | — | JobSearchResult | needs-data | needs-request-data | HTTP 404 on staging |
| /job/{id}/timeline | GET | — | — | TimelineTask | needs-data | needs-request-data | Needs job ID with active timeline |
| /job/{id}/timeline/{taskCode}/agent | GET | — | — | TimelineAgent | needs-data | needs-request-data | Needs job ID + task code |
| /job/{id}/tracking | GET | — | — | TrackingInfo | needs-data | needs-request-data | Works but no fixture_file set in example |
| /v3/job/{id}/tracking/{historyAmount} | GET | — | — | TrackingInfoV3 | needs-data | needs-request-data | Works but no fixture_file set in example |
| /job/{id}/payment | GET | — | — | PaymentInfo | needs-data | needs-request-data | Works but no fixture_file set in example |
| /job/{id}/payment/sources | GET | — | — | PaymentSource | needs-data | needs-request-data | Works but no fixture_file set in example |
| /job/{id}/payment/ACHPaymentSession | POST | ACHSessionResponse | needs-data | ACHSessionResponse | needs-data | needs-request-data | Needs ACH session params |
| /job/{id}/note | GET | — | — | JobNote | needs-data | needs-request-data | Model bug — id field typed as str but API returns int |
| /job/{id}/parcelitems | GET | — | — | ParcelItem | needs-data | needs-request-data | Returns empty list — needs job with parcel items |
| /job/{id}/parcel-items-with-materials | GET | — | — | ParcelItemWithMaterials | needs-data | needs-request-data | Returns empty list — needs job with packed items |
| /job/{id}/packagingcontainers | GET | — | — | PackagingContainer | needs-data | needs-request-data | Model has warning fields — works but model incomplete |
| /job/{id}/shipment/ratequotes | GET | — | — | RateQuote | captured | complete | 2026-02-14, staging |
| /job/{id}/shipment/accessorials | GET | — | — | Accessorial | captured | complete | 2026-02-14, staging |
| /job/{id}/shipment/origindestination | GET | — | — | ShipmentOriginDestination | captured | complete | 2026-02-14, staging |
| /job/{id}/shipment/ratesstate | GET | — | — | RatesState | captured | complete | 2026-02-14, staging |
| /shipment | GET | — | — | ShipmentInfo | captured | complete | 2026-02-14, staging |
| /shipment/accessorials | GET | — | — | GlobalAccessorial | captured | complete | 2026-02-14, staging |
| /job/{id}/form/shipments | GET | — | — | FormsShipmentPlan | captured | complete | 2026-02-14, staging |
| /AutoPrice/QuickQuote | POST | QuoteRequestModel | needs-data | QuickQuoteResponse | needs-data | needs-request-data | Request model validation error — field names don't match (originZip vs OriginZip) |
| /AutoPrice/QuoteRequest | POST | QuoteRequestModel | needs-data | QuoteRequestResponse | needs-data | needs-request-data | Needs items array with weight, class fields and valid origin/destination |

## Catalog Endpoints

| Endpoint Path | Method | Req Model | Req Fixture | Resp Model | Resp Fixture | Status | Notes |
|---------------|--------|-----------|-------------|------------|--------------|--------|-------|
| /Seller/{id} | GET | — | — | SellerDto | captured | complete | 2026-02-13, staging |
| /Seller/{id} | GET | — | — | SellerExpandedDto | captured | complete | 2026-02-13, staging |
| /Seller | GET | — | — | SellerExpandedDto | captured | complete | 2026-02-14, staging |
| /Catalog | GET | — | — | CatalogWithSellersDto | needs-data | needs-request-data | Returns empty — research ABConnectTools for required params |
| /Catalog/{id} | GET | — | — | CatalogExpandedDto | needs-data | needs-request-data | Needs valid catalog ID |
| /Lot | GET | — | — | LotDto | needs-data | needs-request-data | Needs valid catalog ID param |
| /Lot/{id} | GET | — | — | LotDataDto | needs-data | needs-request-data | Needs valid lot ID |
| /Lot/overrides | POST | LotOverrideDto | needs-data | LotOverrideDto | needs-data | needs-request-data | Needs lot override params |

## ABC Endpoints

| Endpoint Path | Method | Req Model | Req Fixture | Resp Model | Resp Fixture | Status | Notes |
|---------------|--------|-----------|-------------|------------|--------------|--------|-------|
| /Web2Lead | GET | — | — | Web2LeadResponse | captured | complete | 2026-02-13, staging |

## Model Warning Summary

The following captured fixtures have "unexpected field" warnings,
indicating the Pydantic model is missing fields present in the API
response. Fixtures are captured correctly but models need updating:

| Model | Missing Fields |
|-------|---------------|
| AddressIsValidResult | dontValidate, countryId, countryCode, latitude, longitude, propertyType |
| CalendarItem | notedConditions |
| CompanyDetails | address, accountInformation, pricing, insurance, finalMileTariff, taxes, readOnlyAccess |
| CompanySimple | parentCompanyId, companyName, typeId |
| ContactPrimaryDetails | cellPhone, fax, address |
| ContactSimple | editable, isEmpty, fullNameUpdateRequired, emailsList, phonesList, addressesList, fax, primaryPhone, primaryEmail, +22 more |
| ContactTypeEntity | value |
| CountryCodeDto | id, iataCode |
| FormsShipmentPlan | jobShipmentID, jobID, fromAddressId, toAddressId, providerID, sequenceNo, +5 more |
| GlobalAccessorial | description, price, options, uniqueId, sourceAPIs |
| RatesState | fromZip, toZip, itemWeight, services, parcelItems, parcelServices, shipOutDate |
| SellerExpandedDto | customerDisplayId, isActive |
| ShipmentInfo | usedAPI, historyProviderName, historyStatuses, weight, jobWeight, successfully, errorMessage, multipleShipments, packages, estimatedDelivery |
| User | totalCount, data (response is paginated wrapper, not flat User) |
| Web2LeadResponse | SubmitNewLeadPOSTResult |
