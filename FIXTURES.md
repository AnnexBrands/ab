# Fixture Tracking

Tracks capture status for all endpoint fixtures in `tests/fixtures/`.

**Constitution**: v2.0.0, Principles II & V
**Rule**: Fabricated fixtures are prohibited. Every fixture MUST
come from a real API response (human-captured or legacy-validated).

## Summary

- **Captured**: 22
- **Pending**: 27

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

## Pending Fixtures

Endpoints below have models and skeleton tests but need real
fixtures captured by a human. Run the endpoint against staging
and save the JSON response to `tests/fixtures/{ModelName}.json`.

The **ABConnectTools Ref** column shows fixtures in the legacy
project that can be referenced for response shape (do NOT copy —
capture fresh from staging).

| Endpoint Path | Method | Model Name | Capture Instructions | Blocker | ABConnectTools Ref |
|---------------|--------|------------|---------------------|---------|-------------------|
| /address/isvalid | GET | AddressIsValidResult | `api.address.validate(...)` — needs valid address params | Returns 400 in staging with test params | — |
| /address/propertytype | GET | PropertyType | `api.address.get_property_type(...)` | Returns 204 in staging | — |
| /lookup/items | GET | LookupItem | `api.lookup.get_items(...)` | Returns 204 in staging | — |
| /Catalog | GET | CatalogWithSellersDto | `api.catalog.list()` | No catalog data in staging | — |
| /Catalog/{id} | GET | CatalogExpandedDto | `api.catalog.get(catalog_id)` | No catalog data in staging | — |
| /Lot | GET | LotDto | `api.lots.list(catalog_id)` | No lot data in staging | — |
| /Lot/{id} | GET | LotDataDto | `api.lots.get(lot_id)` | No lot data in staging | — |
| /Lot/overrides | POST | LotOverrideDto | `api.lots.get_overrides(...)` | No lot data in staging | — |
| /AutoPrice/QuoteRequest | POST | QuoteRequestResponse | `api.autoprice.quote_request(...)` — needs valid job with items | Requires certified quote-eligible job | — |
| /job/{id}/timeline | GET | TimelineTask | `api.jobs.get_timeline(job_id)` — use job with active timeline | Needs job with timeline data | — |
| /job/{id}/timeline/{taskCode}/agent | GET | TimelineAgent | `api.jobs.get_timeline_agent(job_id, task_code)` | Needs job with timeline agent | — |
| /job/{id}/tracking | GET | TrackingInfo | `api.jobs.get_tracking(job_id)` — use shipped job | Needs job with shipment tracking | — |
| /v3/job/{id}/tracking/{historyAmount} | GET | TrackingInfoV3 | `api.jobs.get_tracking_v3(job_id, 5)` | Needs job with shipment tracking | — |
| /job/{id}/shipment/ratequotes | GET | RateQuote | `api.shipments.get_rate_quotes(job_id)` | Needs job with rate quotes | — |
| /job/{id}/shipment/origindestination | GET | ShipmentOriginDestination | `api.shipments.get_origin_destination(job_id)` | Needs job with shipment addresses | — |
| /job/{id}/shipment/accessorials | GET | Accessorial | `api.shipments.get_accessorials(job_id)` | Needs job with shipment | `ShipmentAccessorials.json` |
| /job/{id}/shipment/ratesstate | GET | RatesState | `api.shipments.get_rates_state(job_id)` | Needs job in rating phase | — |
| /shipment | GET | ShipmentInfo | `api.shipments.get_shipment(shipment_id)` | Needs valid shipment ID | — |
| /shipment/accessorials | GET | GlobalAccessorial | `api.shipments.get_global_accessorials()` | May need specific carrier config | `ShipmentAccessorials.json` |
| /job/{id}/payment | GET | PaymentInfo | `api.payments.get(job_id)` | Needs job with payment data | — |
| /job/{id}/payment/sources | GET | PaymentSource | `api.payments.get_sources(job_id)` | Needs job with payment sources | — |
| /job/{id}/payment/ACHPaymentSession | POST | ACHSessionResponse | `api.payments.create_ach_session(job_id, ...)` | Needs ACH-eligible job | — |
| /job/{id}/form/shipments | GET | FormsShipmentPlan | `api.forms.get_shipments(job_id)` | Needs job with shipment plan | — |
| /job/{id}/note | GET | JobNote | `api.jobs.get_notes(job_id)` — use job with notes | Needs job with notes | — |
| /job/{id}/parcelitems | GET | ParcelItem | `api.jobs.get_parcel_items(job_id)` | Needs job with parcel items | — |
| /job/{id}/parcel-items-with-materials | GET | ParcelItemWithMaterials | `api.jobs.get_parcel_items_with_materials(job_id)` | Needs job with packed items | — |
| /job/{id}/packagingcontainers | GET | PackagingContainer | `api.jobs.get_packaging_containers(job_id)` | Needs job with containers | — |
