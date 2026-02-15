# Fixture Tracking

Tracks capture status for all endpoint fixtures in `tests/fixtures/`.

**Constitution**: v2.2.0, Principles II & V
**Rule**: Fabricated fixtures are prohibited. Failed API calls
mean the example needs correct request data — not a response
fixture. See Principle II (Example-Driven Fixture Capture).

## Summary

- **Captured**: 24
- **Needs Request Data**: 26
- **Total tracked**: 50

## Captured Fixtures

| Endpoint Path | Method | Model Name | Date | Source | ABConnectTools Ref |
|---------------|--------|------------|------|--------|--------------------|
| /companies/{id} | GET | CompanySimple | 2026-02-13 | staging | `CompanySimple.json` |
| /companies/{id}/fulldetails | GET | CompanyDetails | 2026-02-13 | staging | — |
| /companies/availableByCurrentUser | GET | SearchCompanyResponse | 2026-02-13 | staging | `CompanyAvailableByCurrentUser.json` |
| /contacts/user | GET | ContactSimple | 2026-02-13 | staging | `ContactUser.json` |
| /contacts/{id}/primarydetails | GET | ContactPrimaryDetails | 2026-02-13 | staging | — |
| /job/{id}/price | GET | JobPrice | 2026-02-13 | staging | — |
| /job/{id}/calendaritems | GET | CalendarItem | 2026-02-13 | staging | — |
| /job/{id}/updatePageConfig | GET | JobUpdatePageConfig | 2026-02-13 | staging | — |
| /lookup/contacttypes | GET | ContactTypeEntity | 2026-02-13 | staging | `LookupContactTypes.json` |
| /lookup/countries | GET | CountryCodeDto | 2026-02-13 | staging | `LookupCountries.json` |
| /lookup/jobstatuses | GET | JobStatus | 2026-02-13 | staging | — |
| /Seller/{id} | GET | SellerDto | 2026-02-13 | staging | — |
| /Seller/{id} | GET | SellerExpandedDto | 2026-02-13 | staging | — |
| /Seller | GET | SellerExpandedDto_detail | 2026-02-14 | staging | — |
| /Web2Lead | GET | Web2LeadResponse | 2026-02-13 | staging | — |
| /users/list | POST | User | 2026-02-13 | staging | — |
| /address/isvalid | GET | AddressIsValidResult | 2026-02-14 | staging | — |
| /job/{id}/shipment/ratequotes | GET | RateQuote | 2026-02-14 | staging | — |
| /job/{id}/shipment/accessorials | GET | Accessorial | 2026-02-14 | staging | `ShipmentAccessorials.json` |
| /job/{id}/shipment/origindestination | GET | ShipmentOriginDestination | 2026-02-14 | staging | — |
| /job/{id}/shipment/ratesstate | GET | RatesState | 2026-02-14 | staging | — |
| /shipment | GET | ShipmentInfo | 2026-02-14 | staging | — |
| /shipment/accessorials | GET | GlobalAccessorial | 2026-02-14 | staging | `ShipmentAccessorials.json` |
| /job/{id}/form/shipments | GET | FormsShipmentPlan | 2026-02-14 | staging | — |

## Needs Request Data

Endpoints below return errors because the example has wrong or
missing request parameters. Research ABConnectTools endpoint code,
examples, and swagger to find the correct request data. Fix the
example, re-run, and capture the fixture.

| Endpoint Path | Method | Model Name | What's Missing | ABConnectTools Ref |
|---------------|--------|------------|---------------|-------------------|
| /address/propertytype | GET | PropertyType | Query params: needs valid `address1`, `city`, `state`, `zip_code` for a real address — returns null with test params | — |
| /AutoPrice/QuickQuote | POST | QuickQuoteResponse | Request model validation error — QuoteRequestModel field names don't match example params (originZip vs OriginZip) | — |
| /AutoPrice/QuoteRequest | POST | QuoteRequestResponse | Request body: needs items array with `weight`, `class` fields and valid origin/destination — research ABConnectTools `endpoints/autoprice.py` | — |
| /contacts/{id}/editdetails | GET | ContactDetailedInfo | HTTP 500 on staging — was previously captured but now fails; investigate staging data | `ContactDetails.json` |
| /contacts/v2/search | POST | SearchContactEntityResult | HTTP 400 — needs PageSize (1-32767) and PageNumber (1-32767) in request body | — |
| /documents | GET | Document | HTTP 500 on staging — was previously captured but now fails; investigate staging data | — |
| /job/{id} | GET | Job | HTTP 500 on staging — was previously captured but now fails; investigate job ID or staging data | — |
| /job/search | GET | JobSearchResult | HTTP 404 on staging — was previously captured but now fails; investigate search endpoint path | — |
| /lookup/items | GET | LookupItem | Returns 204 — research ABConnectTools for required query params or correct lookup key | — |
| /users/roles | GET | UserRole | Model mismatch — API returns list of strings, UserRole model expects dict; fix model to accept str | `UsersRoles.json` |
| /Catalog | GET | CatalogWithSellersDto | Returns empty — research ABConnectTools `endpoints/catalog.py` for required params or correct staging catalog IDs | — |
| /Catalog/{id} | GET | CatalogExpandedDto | Needs valid catalog ID — research ABConnectTools examples for realistic IDs | — |
| /Lot | GET | LotDto | Needs valid catalog ID param — research ABConnectTools `endpoints/lots.py` | — |
| /Lot/{id} | GET | LotDataDto | Needs valid lot ID — research ABConnectTools examples | — |
| /Lot/overrides | POST | LotOverrideDto | Request body: needs lot override params — research ABConnectTools `endpoints/lots.py` | — |
| /job/{id}/timeline | GET | TimelineTask | Needs job ID with active timeline — research ABConnectTools `endpoints/jobs/timeline.py` for correct job selection | — |
| /job/{id}/timeline/{taskCode}/agent | GET | TimelineAgent | Needs job ID + task code — research ABConnectTools for valid task codes | — |
| /job/{id}/tracking | GET | TrackingInfo | Works but no fixture_file set in example — model has warning fields (statuses, success, errorMessage) | — |
| /v3/job/{id}/tracking/{historyAmount} | GET | TrackingInfoV3 | Works but no fixture_file set in example — model has warning fields (statuses, carriers) | — |
| /job/{id}/payment | GET | PaymentInfo | Works but no fixture_file set in example — model has many warning fields | — |
| /job/{id}/payment/sources | GET | PaymentSource | Works but no fixture_file set in example | — |
| /job/{id}/payment/ACHPaymentSession | POST | ACHSessionResponse | Request body: needs ACH session params — research ABConnectTools `endpoints/jobs/payments.py` | — |
| /job/{id}/note | GET | JobNote | Model bug — id field typed as str but API returns int; fix model | — |
| /job/{id}/parcelitems | GET | ParcelItem | Returns empty list — needs job with parcel items | — |
| /job/{id}/parcel-items-with-materials | GET | ParcelItemWithMaterials | Returns empty list — needs job with packed items | — |
| /job/{id}/packagingcontainers | GET | PackagingContainer | Model has warning fields (description, length, width, height, weight, totalCost) — works but model incomplete | — |

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
