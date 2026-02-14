# Fixture Tracking

Tracks capture status for all endpoint fixtures in `tests/fixtures/`.

**Constitution**: v2.1.0, Principles II & V
**Rule**: Fabricated fixtures are prohibited. Failed API calls
mean the example needs correct request data — not a response
fixture. See Principle II (Example-Driven Fixture Capture).

## Summary

- **Captured**: 22
- **Needs Request Data**: 27

## Captured Fixtures

| Endpoint Path | Method | Model Name | Date | Source | ABConnectTools Ref |
|---------------|--------|------------|------|--------|--------------------|
| /companies/{id} | GET | CompanySimple | 2026-02-13 | staging | `CompanySimple.json` |
| /companies/{id}/fulldetails | GET | CompanyDetails | 2026-02-13 | staging | — |
| /companies/availableByCurrentUser | GET | SearchCompanyResponse | 2026-02-13 | staging | `CompanyAvailableByCurrentUser.json` |
| /contacts/user | GET | ContactSimple | 2026-02-13 | staging | `ContactUser.json` |
| /contacts/{id}/editdetails | GET | ContactDetailedInfo | 2026-02-13 | staging | `ContactDetails.json` |
| /contacts/{id}/primarydetails | GET | ContactPrimaryDetails | 2026-02-13 | staging | — |
| /contacts/v2/search | POST | SearchContactEntityResult | 2026-02-13 | staging | — |
| /job/{id} | GET | Job | 2026-02-13 | staging | — |
| /job/{id}/price | GET | JobPrice | 2026-02-13 | staging | — |
| /job/search | GET | JobSearchResult | 2026-02-13 | staging | — |
| /job/{id}/calendaritems | GET | CalendarItem | 2026-02-13 | staging | — |
| /job/{id}/updatePageConfig | GET | JobUpdatePageConfig | 2026-02-13 | staging | — |
| /documents | GET | Document | 2026-02-13 | staging | — |
| /lookup/contacttypes | GET | ContactTypeEntity | 2026-02-13 | staging | `LookupContactTypes.json` |
| /lookup/countries | GET | CountryCodeDto | 2026-02-13 | staging | `LookupCountries.json` |
| /lookup/jobstatuses | GET | JobStatus | 2026-02-13 | staging | — |
| /Seller/{id} | GET | SellerDto | 2026-02-13 | staging | — |
| /Seller/{id} | GET | SellerExpandedDto | 2026-02-13 | staging | — |
| /AutoPrice/QuickQuote | POST | QuickQuoteResponse | 2026-02-13 | staging | — |
| /Web2Lead | GET | Web2LeadResponse | 2026-02-13 | staging | — |
| /users/list | POST | User | 2026-02-13 | staging | — |
| /users/roles | GET | UserRole | 2026-02-13 | staging | `UsersRoles.json` |

## Needs Request Data

Endpoints below return errors because the example has wrong or
missing request parameters. Research ABConnectTools endpoint code,
examples, and swagger to find the correct request data. Fix the
example, re-run, and capture the fixture.

| Endpoint Path | Method | Model Name | What's Missing | ABConnectTools Ref |
|---------------|--------|------------|---------------|-------------------|
| /address/isvalid | GET | AddressIsValidResult | Query params: needs valid `street`, `city`, `state`, `zipCode` — returns 400 with test params | — |
| /address/propertytype | GET | PropertyType | Query params: needs valid `street` + `zipCode` for a real address — returns 204 with test params | — |
| /AutoPrice/QuoteRequest | POST | QuoteRequestResponse | Request body: needs items array with `weight`, `class` fields and valid origin/destination — research ABConnectTools `endpoints/autoprice.py` | — |
| /lookup/items | GET | LookupItem | Returns 204 — research ABConnectTools for required query params or correct lookup key | — |
| /Catalog | GET | CatalogWithSellersDto | Returns empty — research ABConnectTools `endpoints/catalog.py` for required params or correct staging catalog IDs | — |
| /Catalog/{id} | GET | CatalogExpandedDto | Needs valid catalog ID — research ABConnectTools examples for realistic IDs | — |
| /Lot | GET | LotDto | Needs valid catalog ID param — research ABConnectTools `endpoints/lots.py` | — |
| /Lot/{id} | GET | LotDataDto | Needs valid lot ID — research ABConnectTools examples | — |
| /Lot/overrides | POST | LotOverrideDto | Request body: needs lot override params — research ABConnectTools `endpoints/lots.py` | — |
| /job/{id}/timeline | GET | TimelineTask | Needs job ID with active timeline — research ABConnectTools `endpoints/jobs/timeline.py` for correct job selection | — |
| /job/{id}/timeline/{taskCode}/agent | GET | TimelineAgent | Needs job ID + task code — research ABConnectTools for valid task codes | — |
| /job/{id}/tracking | GET | TrackingInfo | Needs shipped job ID — research ABConnectTools `endpoints/jobs/tracking.py` for job selection criteria | — |
| /v3/job/{id}/tracking/{historyAmount} | GET | TrackingInfoV3 | Needs shipped job ID + history amount param — research ABConnectTools for v3 tracking endpoint | — |
| /job/{id}/shipment/ratequotes | GET | RateQuote | Needs job ID with rate quotes — research ABConnectTools `endpoints/jobs/shipments.py` | — |
| /job/{id}/shipment/origindestination | GET | ShipmentOriginDestination | Needs job ID with shipment — research ABConnectTools `endpoints/jobs/shipments.py` | — |
| /job/{id}/shipment/accessorials | GET | Accessorial | Needs job ID with active shipment — research ABConnectTools `endpoints/jobs/shipments.py` | `ShipmentAccessorials.json` |
| /job/{id}/shipment/ratesstate | GET | RatesState | Needs job ID in rating phase — research ABConnectTools for job state requirements | — |
| /shipment | GET | ShipmentInfo | Needs valid shipment ID — research ABConnectTools `endpoints/shipments.py` for ID lookup | — |
| /shipment/accessorials | GET | GlobalAccessorial | Research ABConnectTools `endpoints/shipments.py` for correct params | `ShipmentAccessorials.json` |
| /job/{id}/payment | GET | PaymentInfo | Needs job ID with payment data — research ABConnectTools `endpoints/jobs/payments.py` | — |
| /job/{id}/payment/sources | GET | PaymentSource | Needs job ID with payment sources — research ABConnectTools `endpoints/jobs/payments.py` | — |
| /job/{id}/payment/ACHPaymentSession | POST | ACHSessionResponse | Request body: needs ACH session params — research ABConnectTools `endpoints/jobs/payments.py` | — |
| /job/{id}/form/shipments | GET | FormsShipmentPlan | Needs job ID with shipment plan — research ABConnectTools `endpoints/jobs/forms.py` | — |
| /job/{id}/note | GET | JobNote | Needs job ID with notes — research ABConnectTools `endpoints/jobs/notes.py` | — |
| /job/{id}/parcelitems | GET | ParcelItem | Needs job ID with parcel items — research ABConnectTools `endpoints/jobs/parcels.py` | — |
| /job/{id}/parcel-items-with-materials | GET | ParcelItemWithMaterials | Needs job ID with packed items — research ABConnectTools for correct endpoint params | — |
| /job/{id}/packagingcontainers | GET | PackagingContainer | Needs job ID with containers — research ABConnectTools for correct endpoint params | — |
