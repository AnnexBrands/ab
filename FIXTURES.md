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
- **Needs Fixture (new 008)**: 106
- **Total tracked**: 156

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
| /rfq/{rfqId} | GET | — | — | QuoteRequestDisplayInfo | needs-data | needs-fixture | 008 — run examples/rfq.py |
| /rfq/forjob/{jobId} | GET | — | — | List[QuoteRequestDisplayInfo] | needs-data | needs-fixture | 008 |
| /rfq/{rfqId}/accept | POST | AcceptModel | — | — | — | needs-fixture | 008 — mutating |
| /rfq/{rfqId}/decline | POST | — | — | — | — | needs-fixture | 008 — mutating |
| /rfq/{rfqId}/cancel | POST | — | — | — | — | needs-fixture | 008 — mutating |
| /rfq/{rfqId}/acceptwinner | POST | — | — | — | — | needs-fixture | 008 — mutating |
| /rfq/{rfqId}/comment | POST | AcceptModel | — | — | — | needs-fixture | 008 |
| /job/{id}/rfq | GET | — | — | List[QuoteRequestDisplayInfo] | needs-data | needs-fixture | 008 |
| /job/{id}/rfq/statusof/{type}/forcompany/{id} | GET | — | — | QuoteRequestStatus | needs-data | needs-fixture | 008 |
| /job/{id}/onhold | GET | — | — | List[ExtendedOnHoldInfo] | needs-data | needs-fixture | 008 |
| /job/{id}/onhold | POST | SaveOnHoldRequest | — | SaveOnHoldResponse | needs-data | needs-fixture | 008 |
| /job/{id}/onhold | DELETE | — | — | — | — | needs-fixture | 008 — destructive |
| /job/{id}/onhold/{id} | GET | — | — | OnHoldDetails | needs-data | needs-fixture | 008 |
| /job/{id}/onhold/{id} | PUT | SaveOnHoldRequest | — | SaveOnHoldResponse | needs-data | needs-fixture | 008 |
| /job/{id}/onhold/followupuser/{contactId} | GET | — | — | OnHoldUser | needs-data | needs-fixture | 008 |
| /job/{id}/onhold/followupusers | GET | — | — | List[OnHoldUser] | needs-data | needs-fixture | 008 |
| /job/{id}/onhold/{id}/comment | POST | — | — | OnHoldNoteDetails | needs-data | needs-fixture | 008 |
| /job/{id}/onhold/{id}/dates | PUT | SaveOnHoldDatesModel | — | — | — | needs-fixture | 008 |
| /job/{id}/onhold/{id}/resolve | PUT | — | — | ResolveJobOnHoldResponse | needs-data | needs-fixture | 008 |
| /reports/insurance | POST | InsuranceReportRequest | — | InsuranceReport | needs-data | needs-fixture | 008 |
| /reports/sales | POST | SalesForecastReportRequest | — | SalesForecastReport | needs-data | needs-fixture | 008 |
| /reports/sales/summary | POST | SalesForecastSummaryRequest | — | SalesForecastSummary | needs-data | needs-fixture | 008 |
| /reports/salesDrilldown | POST | Web2LeadRevenueFilter | — | List[RevenueCustomer] | needs-data | needs-fixture | 008 |
| /reports/topRevenueCustomers | POST | Web2LeadRevenueFilter | — | List[RevenueCustomer] | needs-data | needs-fixture | 008 |
| /reports/topRevenueSalesReps | POST | Web2LeadRevenueFilter | — | List[RevenueCustomer] | needs-data | needs-fixture | 008 |
| /reports/referredBy | POST | ReferredByReportRequest | — | ReferredByReport | needs-data | needs-fixture | 008 |
| /reports/web2Lead | POST | Web2LeadV2RequestModel | — | Web2LeadReport | needs-data | needs-fixture | 008 |
| /job/{id}/email | POST | — | — | — | — | needs-fixture | 008 — fire-and-forget |
| /job/{id}/email/senddocument | POST | SendDocumentEmailModel | — | — | — | needs-fixture | 008 |
| /job/{id}/email/createtransactionalemail | POST | — | — | — | — | needs-fixture | 008 |
| /job/{id}/email/{templateGuid}/send | POST | — | — | — | — | needs-fixture | 008 |
| /job/{id}/sms | GET | — | — | — | — | needs-fixture | 008 |
| /job/{id}/sms | POST | SendSMSModel | — | — | — | needs-fixture | 008 |
| /job/{id}/sms/read | POST | MarkSmsAsReadModel | — | — | — | needs-fixture | 008 |
| /job/{id}/sms/templatebased/{templateId} | GET | — | — | — | — | needs-fixture | 008 |
| /lookup/{masterConstantKey} | GET | — | — | List[LookupValue] | needs-data | needs-fixture | 008 |
| /lookup/{masterConstantKey}/{valueId} | GET | — | — | LookupValue | needs-data | needs-fixture | 008 |
| /lookup/accessKeys | GET | — | — | List[AccessKey] | needs-data | needs-fixture | 008 |
| /lookup/accessKey/{accessKey} | GET | — | — | AccessKey | needs-data | needs-fixture | 008 |
| /lookup/PPCCampaigns | GET | — | — | List[LookupValue] | needs-data | needs-fixture | 008 |
| /lookup/parcelPackageTypes | GET | — | — | List[ParcelPackageType] | needs-data | needs-fixture | 008 |
| /lookup/documentTypes | GET | — | — | List[LookupValue] | needs-data | needs-fixture | 008 |
| /lookup/comonInsurance | GET | — | — | List[LookupValue] | needs-data | needs-fixture | 008 |
| /lookup/densityClassMap | GET | — | — | List[DensityClassEntry] | needs-data | needs-fixture | 008 |
| /lookup/referCategory | GET | — | — | List[LookupValue] | needs-data | needs-fixture | 008 |
| /lookup/referCategoryHeirachy | GET | — | — | List[LookupValue] | needs-data | needs-fixture | 008 |
| /lookup/resetMasterConstantCache | GET | — | — | — | — | needs-fixture | 008 — mutating |
| /commodity/{id} | GET | — | — | Commodity | needs-data | needs-fixture | 008 |
| /commodity/{id} | PUT | CommodityUpdateRequest | — | Commodity | needs-data | needs-fixture | 008 |
| /commodity | POST | CommodityCreateRequest | — | Commodity | needs-data | needs-fixture | 008 |
| /commodity/search | POST | CommoditySearchRequest | — | List[Commodity] | needs-data | needs-fixture | 008 |
| /commodity/suggestions | POST | CommoditySuggestionRequest | — | List[Commodity] | needs-data | needs-fixture | 008 |
| /commodity-map/{id} | GET | — | — | CommodityMap | needs-data | needs-fixture | 008 |
| /commodity-map/{id} | PUT | CommodityMapUpdateRequest | — | CommodityMap | needs-data | needs-fixture | 008 |
| /commodity-map/{id} | DELETE | — | — | ServiceBaseResponse | needs-data | needs-fixture | 008 |
| /commodity-map | POST | CommodityMapCreateRequest | — | CommodityMap | needs-data | needs-fixture | 008 |
| /commodity-map/search | POST | CommodityMapSearchRequest | — | List[CommodityMap] | needs-data | needs-fixture | 008 |
| /dashboard | GET | — | — | DashboardSummary | needs-data | needs-fixture | 008 |
| /dashboard/gridviews | GET | — | — | List[GridViewInfo] | needs-data | needs-fixture | 008 |
| /dashboard/gridviewstate/{id} | GET | — | — | GridViewState | needs-data | needs-fixture | 008 |
| /dashboard/gridviewstate/{id} | POST | GridViewState | — | — | — | needs-fixture | 008 |
| /dashboard/inbound | POST | — | — | — | — | needs-fixture | 008 |
| /dashboard/inhouse | POST | — | — | — | — | needs-fixture | 008 |
| /dashboard/outbound | POST | — | — | — | — | needs-fixture | 008 |
| /dashboard/local-deliveries | POST | — | — | — | — | needs-fixture | 008 |
| /dashboard/recentestimates | POST | — | — | — | — | needs-fixture | 008 |
| /views/all | GET | — | — | List[GridViewDetails] | needs-data | needs-fixture | 008 |
| /views/{viewId} | GET | — | — | GridViewDetails | needs-data | needs-fixture | 008 |
| /views | POST | GridViewCreateRequest | — | GridViewDetails | needs-data | needs-fixture | 008 |
| /views/{viewId} | DELETE | — | — | ServiceBaseResponse | needs-data | needs-fixture | 008 |
| /views/{viewId}/accessinfo | GET | — | — | GridViewAccess | needs-data | needs-fixture | 008 |
| /views/{viewId}/access | PUT | GridViewAccess | — | — | — | needs-fixture | 008 |
| /views/datasetsps | GET | — | — | List[StoredProcedureColumn] | needs-data | needs-fixture | 008 |
| /views/datasetsp/{spName} | GET | — | — | List[StoredProcedureColumn] | needs-data | needs-fixture | 008 |
| /companies/brands | GET | — | — | List[CompanyBrand] | needs-data | needs-fixture | 008 |
| /companies/brandstree | GET | — | — | List[BrandTree] | needs-data | needs-fixture | 008 |
| /companies/geoAreaCompanies | GET | — | — | — | — | needs-fixture | 008 |
| /companies/{id}/geosettings | GET | — | — | GeoSettings | needs-data | needs-fixture | 008 |
| /companies/{id}/geosettings | POST | GeoSettingsSaveRequest | — | — | — | needs-fixture | 008 |
| /companies/geosettings | GET | — | — | GeoSettings | needs-data | needs-fixture | 008 |
| /companies/search/carrier-accounts | GET | — | — | — | — | needs-fixture | 008 |
| /companies/suggest-carriers | GET | — | — | — | — | needs-fixture | 008 |
| /companies/{id}/carrierAcounts | GET | — | — | List[CarrierAccount] | needs-data | needs-fixture | 008 |
| /companies/{id}/carrierAcounts | POST | CarrierAccountSaveRequest | — | — | — | needs-fixture | 008 |
| /companies/{id}/packagingsettings | GET | — | — | PackagingSettings | needs-data | needs-fixture | 008 |
| /companies/{id}/packagingsettings | POST | — | — | — | — | needs-fixture | 008 |
| /companies/{id}/packaginglabor | GET | — | — | PackagingLabor | needs-data | needs-fixture | 008 |
| /companies/{id}/packaginglabor | POST | — | — | — | — | needs-fixture | 008 |
| /companies/{id}/inheritedPackagingTariffs | GET | — | — | List[PackagingTariff] | needs-data | needs-fixture | 008 |
| /companies/{id}/inheritedpackaginglabor | GET | — | — | PackagingLabor | needs-data | needs-fixture | 008 |
| /contacts/{contactId}/history | POST | — | — | ContactHistory | needs-data | needs-fixture | 008 |
| /contacts/{contactId}/history/aggregated | GET | — | — | ContactHistoryAggregated | needs-data | needs-fixture | 008 |
| /contacts/{contactId}/history/graphdata | GET | — | — | ContactGraphData | needs-data | needs-fixture | 008 |
| /contacts/{mergeToId}/merge/preview | POST | — | — | ContactMergePreview | needs-data | needs-fixture | 008 |
| /contacts/{mergeToId}/merge | PUT | — | — | — | — | needs-fixture | 008 — destructive |
| /job/{id}/freightproviders | GET | — | — | List[PricedFreightProvider] | needs-data | needs-fixture | 008 |
| /job/{id}/freightproviders | POST | ShipmentPlanProvider | — | — | — | needs-fixture | 008 |
| /job/{id}/freightproviders/{idx}/ratequote | POST | — | — | — | — | needs-fixture | 008 |
| /job/{id}/freightitems | POST | — | — | — | — | needs-fixture | 008 |
| /note | GET | — | — | List[GlobalNote] | needs-data | needs-fixture | 008 |
| /note | POST | GlobalNoteCreateRequest | — | GlobalNote | needs-data | needs-fixture | 008 |
| /note/{id} | PUT | GlobalNoteUpdateRequest | — | GlobalNote | needs-data | needs-fixture | 008 |
| /note/suggestUsers | GET | — | — | List[SuggestedUser] | needs-data | needs-fixture | 008 |
| /partner | GET | — | — | List[Partner] | needs-data | needs-fixture | 008 |
| /partner/{id} | GET | — | — | Partner | needs-data | needs-fixture | 008 |
| /partner/search | POST | PartnerSearchRequest | — | List[Partner] | needs-data | needs-fixture | 008 |

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
