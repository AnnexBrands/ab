# Fixture Tracking

Tracks capture status and quality gates for all endpoint fixtures in `tests/fixtures/`.

**Constitution**: v2.3.0, Principles I–V
**Quality Gates**: G1 (Model Fidelity), G2 (Fixture Status), G3 (Test Quality), G4 (Doc Accuracy), G5 (Param Routing), G6 (Request Quality)
**Rule**: Status is "complete" only when ALL applicable gates pass.

## Summary

- **Total endpoints**: 231
- **Complete (all gates pass)**: 28
- **G1 Model Fidelity**: 39/231 pass
- **G2 Fixture Status**: 43/231 pass
- **G3 Test Quality**: 139/231 pass
- **G4 Doc Accuracy**: 157/231 pass
- **G5 Param Routing**: 216/231 pass
- **G6 Request Quality**: 223/231 pass

## Status Legend

- **complete**: All applicable quality gates pass
- **incomplete**: One or more gates fail
- **PASS/FAIL**: Per-gate status

## ACPortal Endpoints

| Endpoint Path | Method | Req Model | Resp Model | G1 | G2 | G3 | G4 | G5 | G6 | Status | Notes |
|---------------|--------|-----------|------------|----|----|----|----|----|----|--------|-------|
| /companies/{id} | GET | — | CompanySimple | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /companies/{companyId}/details | GET | — | CompanyDetails | PASS | PASS | PASS | PASS | PASS | PASS | complete | HTTP 500 on staging — needs company UUID with populated details |
| /companies/{companyId}/fulldetails | GET | — | CompanyDetails | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /companies/{companyId}/fulldetails | PUT | CompanyDetails | CompanyDetails | PASS | PASS | PASS | PASS | PASS | PASS | complete | Needs valid CompanyDetails kwargs |
| /companies/fulldetails | POST | CompanyDetails | str | PASS | PASS | PASS | PASS | PASS | PASS | complete | Needs valid CompanyDetails kwargs for new company |
| /companies/search/v2 | POST | CompanySearchRequest | List[SearchCompanyResponse] | PASS | PASS | PASS | PASS | PASS | PASS | complete | Request fixture captured; response needs valid search that returns results |
| /companies/list | POST | ListRequest | List[CompanySimple] | PASS | PASS | PASS | PASS | PASS | PASS | complete | Needs valid ListRequest kwargs |
| /companies/availableByCurrentUser | GET | — | List[CompanySimple] | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /contacts/user | GET | — | ContactSimple | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /contacts/{contactId}/primarydetails | GET | — | ContactPrimaryDetails | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /contacts/{contactId}/editdetails | GET | — | ContactDetailedInfo | PASS | PASS | PASS | PASS | PASS | PASS | complete | HTTP 500 on staging — was previously captured but now fails |
| /contacts/v2/search | POST | ContactSearchRequest | List[SearchContactEntityResult] | FAIL | PASS | PASS | PASS | PASS | PASS | incomplete | HTTP 400 — needs PageSize (1-32767) and PageNumber (1-32767) in request body |
| /documents | GET | — | Document | PASS | PASS | PASS | PASS | PASS | PASS | complete | HTTP 500 on staging — was previously captured but now fails |
| /address/isvalid | GET | — | AddressIsValidResult | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-14, staging |
| /address/propertytype | GET | — | int | PASS | PASS | PASS | PASS | PASS | PASS | complete | Query params: needs valid address1, city, state, zip_code for a real address |
| /lookup/contactTypes | GET | — | List[ContactTypeEntity] | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /lookup/countries | GET | — | List[CountryCodeDto] | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /lookup/jobStatuses | GET | — | List[JobStatus] | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /lookup/items | GET | — | List[LookupItem] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | Returns 204 — research ABConnectTools for required query params |
| /users/list | POST | ListRequest | List[User] | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging. Model warning: response is paginated wrapper (totalCount, data) |
| /users/roles | GET | — | List[str] | PASS | PASS | PASS | PASS | PASS | PASS | complete | Fixed — route uses List[str]; API returns plain strings, not UserRole objects |
| /job/{jobDisplayId} | GET | — | Job | FAIL | PASS | PASS | PASS | PASS | PASS | incomplete | HTTP 500 on staging |
| /job/{jobDisplayId}/price | GET | — | JobPrice | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /job/{jobDisplayId}/calendaritems | GET | — | List[CalendarItem] | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /job/{jobDisplayId}/updatePageConfig | GET | — | JobUpdatePageConfig | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /job/search | GET | — | List[JobSearchResult] | FAIL | PASS | PASS | PASS | PASS | PASS | incomplete | HTTP 404 on staging |
| /job/{jobDisplayId}/timeline | GET | — | List[TimelineTask] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | Needs job ID with active timeline |
| /job/{jobDisplayId}/timeline/{taskCode}/agent | GET | — | TimelineAgent | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | Needs job ID + task code |
| /job/{jobDisplayId}/tracking | GET | — | TrackingInfo | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | Works but no fixture_file set in example |
| /v3/job/{jobDisplayId}/tracking/{historyAmount} | GET | — | TrackingInfoV3 | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | Works but no fixture_file set in example |
| /job/{jobDisplayId}/payment | GET | — | PaymentInfo | FAIL | FAIL | PASS | FAIL | FAIL | PASS | incomplete | Works but no fixture_file set in example |
| /job/{jobDisplayId}/payment/sources | GET | — | List[PaymentSource] | FAIL | FAIL | PASS | FAIL | PASS | PASS | incomplete | Works but no fixture_file set in example |
| /job/{jobDisplayId}/payment/ACHPaymentSession | POST | ACHSessionRequest | ACHSessionResponse | FAIL | FAIL | PASS | FAIL | PASS | PASS | incomplete | Needs ACH session params |
| /job/{jobDisplayId}/note | GET | — | List[JobNote] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | Model bug — id field typed as str but API returns int |
| /job/{jobDisplayId}/parcelitems | GET | — | List[ParcelItem] | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | Returns empty list — needs job with parcel items |
| /job/{jobDisplayId}/parcel-items-with-materials | GET | — | List[ParcelItemWithMaterials] | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | Returns empty list — needs job with packed items |
| /job/{jobDisplayId}/packagingcontainers | GET | — | List[PackagingContainer] | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | Model has warning fields — works but model incomplete |
| /job/{jobDisplayId}/shipment/ratequotes | GET | — | List[RateQuote] | PASS | PASS | PASS | FAIL | FAIL | PASS | incomplete | 2026-02-14, staging |
| /job/{jobDisplayId}/shipment/accessorials | GET | — | List[Accessorial] | PASS | PASS | PASS | FAIL | PASS | PASS | incomplete | 2026-02-14, staging |
| /job/{jobDisplayId}/shipment/origindestination | GET | — | ShipmentOriginDestination | PASS | PASS | PASS | FAIL | PASS | PASS | incomplete | 2026-02-14, staging |
| /job/{jobDisplayId}/shipment/ratesstate | GET | — | RatesState | PASS | PASS | PASS | FAIL | PASS | PASS | incomplete | 2026-02-14, staging |
| /shipment | GET | — | ShipmentInfo | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-14, staging |
| /shipment/accessorials | GET | — | List[GlobalAccessorial] | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-14, staging |
| /job/{jobDisplayId}/form/shipments | GET | — | List[FormsShipmentPlan] | PASS | PASS | PASS | FAIL | PASS | PASS | incomplete | 2026-02-14, staging |
| /autoprice/quickquote | POST | QuoteRequestModel | QuickQuoteResponse | PASS | PASS | PASS | PASS | PASS | FAIL | incomplete | Request model validation error — field names don't match (originZip vs OriginZip) |
| /AutoPrice/QuoteRequest | POST | QuoteRequestModel | QuoteRequestResponse | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | Needs items array with weight, class fields and valid origin/destination |
| /rfq/{rfqId} | GET | — | QuoteRequestDisplayInfo | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 — run examples/rfq.py |
| /rfq/forjob/{jobId} | GET | — | List[QuoteRequestDisplayInfo] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /rfq/{rfqId}/accept | POST | AcceptModel | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 — mutating |
| /rfq/{rfqId}/decline | POST | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 — mutating |
| /rfq/{rfqId}/cancel | POST | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 — mutating |
| /rfq/{rfqId}/acceptwinner | POST | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 — mutating |
| /rfq/{rfqId}/comment | POST | AcceptModel | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/rfq | GET | — | List[QuoteRequestDisplayInfo] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/rfq/statusof/{rfqServiceType}/forcompany/{companyId} | GET | — | QuoteRequestStatus | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/onhold | GET | — | List[ExtendedOnHoldInfo] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/onhold | POST | SaveOnHoldRequest | SaveOnHoldResponse | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/onhold | DELETE | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 — destructive |
| /job/{jobDisplayId}/onhold/{id} | GET | — | OnHoldDetails | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/onhold/{onHoldId} | PUT | SaveOnHoldRequest | SaveOnHoldResponse | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/onhold/followupuser/{contactId} | GET | — | OnHoldUser | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/onhold/followupusers | GET | — | List[OnHoldUser] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/onhold/{onHoldId}/comment | POST | OnHoldCommentRequest | OnHoldNoteDetails | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/onhold/{onHoldId}/dates | PUT | SaveOnHoldDatesModel | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/onhold/{onHoldId}/resolve | PUT | ResolveOnHoldRequest | ResolveJobOnHoldResponse | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /reports/insurance | POST | InsuranceReportRequest | InsuranceReport | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /reports/sales | POST | SalesForecastReportRequest | SalesForecastReport | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /reports/sales/summary | POST | SalesForecastSummaryRequest | SalesForecastSummary | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /reports/salesDrilldown | POST | Web2LeadRevenueFilter | List[RevenueCustomer] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /reports/topRevenueCustomers | POST | Web2LeadRevenueFilter | List[RevenueCustomer] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /reports/topRevenueSalesReps | POST | Web2LeadRevenueFilter | List[RevenueCustomer] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /reports/referredBy | POST | ReferredByReportRequest | ReferredByReport | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /reports/web2Lead | POST | Web2LeadV2RequestModel | Web2LeadReport | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/email | POST | SendEmailRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 — fire-and-forget |
| /job/{jobDisplayId}/email/senddocument | POST | SendDocumentEmailModel | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/email/createtransactionalemail | POST | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/email/{emailTemplateGuid}/send | POST | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/sms | GET | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/sms | POST | SendSMSModel | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/sms/read | POST | MarkSmsAsReadModel | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/sms/templatebased/{templateId} | GET | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /lookup/{masterConstantKey} | GET | — | List[LookupValue] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /lookup/{masterConstantKey}/{valueId} | GET | — | LookupValue | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /lookup/accessKeys | GET | — | List[AccessKey] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /lookup/accessKey/{accessKey} | GET | — | AccessKey | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /lookup/PPCCampaigns | GET | — | List[LookupValue] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /lookup/parcelPackageTypes | GET | — | List[ParcelPackageType] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /lookup/documentTypes | GET | — | List[LookupValue] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /lookup/comonInsurance | GET | — | List[LookupValue] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /lookup/densityClassMap | GET | — | List[DensityClassEntry] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /lookup/referCategory | GET | — | List[LookupValue] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /lookup/referCategoryHeirachy | GET | — | List[LookupValue] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /lookup/resetMasterConstantCache | GET | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 — mutating |
| /commodity/{id} | GET | — | Commodity | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /commodity/{id} | PUT | CommodityUpdateRequest | Commodity | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /commodity | POST | CommodityCreateRequest | Commodity | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /commodity/search | POST | CommoditySearchRequest | List[Commodity] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /commodity/suggestions | POST | CommoditySuggestionRequest | List[Commodity] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /commodity-map/{id} | GET | — | CommodityMap | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /commodity-map/{id} | PUT | CommodityMapUpdateRequest | CommodityMap | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /commodity-map/{id} | DELETE | — | ServiceBaseResponse | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /commodity-map | POST | CommodityMapCreateRequest | CommodityMap | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /commodity-map/search | POST | CommodityMapSearchRequest | List[CommodityMap] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /dashboard | GET | — | DashboardSummary | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /dashboard/gridviews | GET | — | List[GridViewInfo] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /dashboard/gridviewstate/{id} | GET | — | GridViewState | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /dashboard/gridviewstate/{id} | POST | GridViewState | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /dashboard/inbound | POST | DashboardCompanyRequest | — | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /dashboard/inhouse | POST | DashboardCompanyRequest | — | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /dashboard/outbound | POST | DashboardCompanyRequest | — | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /dashboard/local-deliveries | POST | DashboardCompanyRequest | — | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /dashboard/recentestimates | POST | DashboardCompanyRequest | — | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /views/all | GET | — | List[GridViewDetails] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /views/{viewId} | GET | — | GridViewDetails | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /views | POST | GridViewCreateRequest | GridViewDetails | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /views/{viewId} | DELETE | — | ServiceBaseResponse | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /views/{viewId}/accessinfo | GET | — | GridViewAccess | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /views/{viewId}/access | PUT | GridViewAccess | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /views/datasetsps | GET | — | List[StoredProcedureColumn] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /views/datasetsp/{spName} | GET | — | List[StoredProcedureColumn] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /companies/brands | GET | — | List[CompanyBrand] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /companies/brandstree | GET | — | List[BrandTree] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /companies/geoAreaCompanies | GET | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /companies/{companyId}/geosettings | GET | — | GeoSettings | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /companies/{companyId}/geosettings | POST | GeoSettingsSaveRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /companies/geosettings | GET | — | GeoSettings | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /companies/search/carrier-accounts | GET | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /companies/suggest-carriers | GET | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /companies/{companyId}/carrierAcounts | GET | — | List[CarrierAccount] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /companies/{companyId}/carrierAcounts | POST | CarrierAccountSaveRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /companies/{companyId}/packagingsettings | GET | — | PackagingSettings | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /companies/{companyId}/packagingsettings | POST | PackagingSettingsSaveRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /companies/{companyId}/packaginglabor | GET | — | PackagingLabor | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /companies/{companyId}/packaginglabor | POST | PackagingLaborSaveRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /companies/{companyId}/inheritedPackagingTariffs | GET | — | List[PackagingTariff] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /companies/{companyId}/inheritedpackaginglabor | GET | — | PackagingLabor | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /contacts/{contactId}/history | POST | ContactHistoryCreateRequest | ContactHistory | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /contacts/{contactId}/history/aggregated | GET | — | ContactHistoryAggregated | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /contacts/{contactId}/history/graphdata | GET | — | ContactGraphData | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /contacts/{mergeToId}/merge/preview | POST | ContactMergeRequest | ContactMergePreview | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /contacts/{mergeToId}/merge | PUT | ContactMergeRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 — destructive |
| /job/{jobDisplayId}/freightproviders | GET | — | List[PricedFreightProvider] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/freightproviders | POST | ShipmentPlanProvider | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/freightproviders/{optionIndex}/ratequote | POST | RateQuoteRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/freightitems | POST | FreightItemsRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /note | GET | — | List[GlobalNote] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /note | POST | GlobalNoteCreateRequest | GlobalNote | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /note/{id} | PUT | GlobalNoteUpdateRequest | GlobalNote | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /note/suggestUsers | GET | — | List[SuggestedUser] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /partner | GET | — | List[Partner] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /partner/{id} | GET | — | Partner | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /partner/search | POST | PartnerSearchRequest | List[Partner] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /Seller/{id} | GET | — | SellerExpandedDto | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /Seller | GET | — | PaginatedList[SellerExpandedDto] | FAIL | FAIL | FAIL | PASS | FAIL | PASS | incomplete | 2026-02-14, staging |
| /Catalog | GET | — | PaginatedList[CatalogExpandedDto] | FAIL | FAIL | FAIL | PASS | FAIL | PASS | incomplete | Returns empty — research ABConnectTools for required params |
| /Catalog/{id} | GET | — | CatalogExpandedDto | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | Needs valid catalog ID |
| /Lot | GET | — | PaginatedList[LotDto] | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | Needs valid catalog ID param |
| /Lot/{id} | GET | — | LotDto | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | Needs valid lot ID |
| /Lot/overrides | POST | LotOverrideDto | LotOverrideDto | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | Needs lot override params |
| /Web2Lead | GET | — | Web2LeadResponse | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /Web2Lead/post | POST | Web2LeadRequest | Web2LeadResponse | PASS | PASS | PASS | PASS | PASS | FAIL | incomplete | 020 |
| /job | POST | JobCreateRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /job/update | POST | JobUpdateRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /job/save | PUT | JobSaveRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /job/transfer/{jobDisplayId} | POST | TransferModel | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/status/quote | POST | — | ServiceBaseResponse | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/shipment/ratequotes | POST | ShipmentRateQuoteRequest | List[RateQuote] | PASS | PASS | PASS | FAIL | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/shipment/book | POST | ShipmentBookRequest | ServiceBaseResponse | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/shipment | DELETE | — | ServiceBaseResponse | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/shipment/accessorial | POST | AccessorialAddRequest | ServiceBaseResponse | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/shipment/accessorial/{addOnId} | DELETE | — | ServiceBaseResponse | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/shipment/exportdata | POST | ShipmentExportRequest | ServiceBaseResponse | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/payment/bysource | POST | PayBySourceRequest | ServiceBaseResponse | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/payment/ACHCreditTransfer | POST | ACHCreditTransferRequest | ServiceBaseResponse | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/payment/attachCustomerBank | POST | AttachBankRequest | ServiceBaseResponse | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/payment/verifyJobACHSource | POST | VerifyACHRequest | ServiceBaseResponse | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/payment/banksource | POST | BankSourceRequest | ServiceBaseResponse | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/payment/cancelJobACHVerification | POST | — | ServiceBaseResponse | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | 020 |
| /contacts/editdetails | POST | ContactEditRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /contacts/{contactId}/editdetails | PUT | ContactEditRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /documents | POST | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /documents/update/{docId} | PUT | DocumentUpdateRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /users/user | POST | UserCreateRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /users/user | PUT | UserUpdateRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /autoprice/v2/quoterequest | POST | QuoteRequestModel | QuoteRequestResponse | FAIL | FAIL | PASS | PASS | PASS | FAIL | incomplete | auto-discovered |
| /Catalog/{id} | DELETE | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /Catalog/{id} | PUT | UpdateCatalogRequest | CatalogWithSellersDto | FAIL | FAIL | PASS | PASS | PASS | FAIL | incomplete | 020 |
| /Bulk/insert | POST | BulkInsertRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | FAIL | incomplete | 020 |
| /Seller | POST | AddSellerRequest | SellerDto | PASS | PASS | PASS | PASS | PASS | FAIL | incomplete | 020 |
| /Seller/{id} | PUT | UpdateSellerRequest | SellerDto | PASS | PASS | PASS | PASS | PASS | FAIL | incomplete | 020 |
| /Seller/{id} | DELETE | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /Lot | POST | AddLotRequest | LotDto | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 020 |
| /Lot/{id} | PUT | UpdateLotRequest | LotDto | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 020 |
| /Lot/{id} | DELETE | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /Lot/get-overrides | POST | — | List[LotOverrideDto] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 020 |
| /Catalog | POST | AddCatalogRequest | CatalogWithSellersDto | FAIL | FAIL | PASS | PASS | PASS | FAIL | incomplete | auto-discovered |
| /contacts/{id} | GET | — | ContactSimple | PASS | PASS | PASS | PASS | PASS | PASS | complete | auto-discovered |
| /documents/get/{docPath} | GET | — | bytes | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | auto-discovered |
| /documents/list | GET | — | List[Document] | PASS | PASS | PASS | PASS | PASS | PASS | complete | auto-discovered |
| /job/{jobDisplayId}/form/address-label | GET | — | bytes | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/bill-of-lading | GET | — | bytes | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/credit-card-authorization | GET | — | bytes | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/customer-quote | GET | — | bytes | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/invoice | GET | — | bytes | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/invoice/editable | GET | — | bytes | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/item-labels | GET | — | bytes | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/operations | GET | — | bytes | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/packaging-labels | GET | — | bytes | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/packaging-specification | GET | — | bytes | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/packing-slip | GET | — | bytes | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/quick-sale | GET | — | bytes | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/usar | GET | — | bytes | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/usar/editable | GET | — | bytes | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/parcelitems/{parcelItemId} | DELETE | — | ServiceBaseResponse | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/timeline/{timelineTaskId} | DELETE | — | ServiceBaseResponse | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/note/{id} | GET | — | JobNote | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/timeline/{timelineTaskIdentifier} | GET | — | TimelineTask | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/timeline/incrementjobstatus | POST | IncrementStatusRequest | ServiceBaseResponse | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/timeline/{timelineTaskId} | PATCH | TimelineTaskUpdateRequest | TimelineTask | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/item/notes | POST | ItemNotesRequest | ServiceBaseResponse | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/note | POST | JobNoteCreateRequest | JobNote | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/parcelitems | POST | ParcelItemCreateRequest | ParcelItem | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/timeline | POST | TimelineTaskCreateRequest | TimelineTask | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/item/{itemId} | PUT | ItemUpdateRequest | ServiceBaseResponse | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/note/{id} | PUT | JobNoteUpdateRequest | JobNote | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | auto-discovered |
| /job/searchByDetails | POST | JobSearchRequest | List[JobSearchResult] | FAIL | PASS | PASS | PASS | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/timeline/undoincrementjobstatus | POST | IncrementStatusRequest | ServiceBaseResponse | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/payment/create | GET | — | PaymentInfo | FAIL | FAIL | PASS | FAIL | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/shipment/exportdata | GET | — | ShipmentExportData | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | auto-discovered |
| /shipment/document/{docId} | GET | — | bytes | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | auto-discovered |
| /Web2Lead/get | GET | — | Web2LeadResponse | PASS | PASS | PASS | PASS | FAIL | PASS | incomplete | auto-discovered |

## Model Warning Summary

Models with `__pydantic_extra__` fields when validated against their fixtures:

| Model | Issue |
|-------|-------|
| Job | 85 undeclared field(s): autoPackFailed, autoPackOff, cFillId, cFillValue, cPackId, cPackValue, ceilingTransportationWeight, commodityId, companyID, companyName, containerId, containerThickness, containerType, containerWeight, customerItemId, descriptionOfProducts, doNotTip, documentExists, eccn, fillWeight, forceCrate, grossCubicFeet, inchesToAdd, isAccess, isContainerChanged, isFillChanged, isFillPercentChanged, isInchToAddChanged, isPrepacked, isValidContainer, isValidFill, itemActive, itemDescription, itemHeight, itemID, itemLength, itemName, itemNotes, itemPublic, itemSequenceNo, itemValue, itemWeight, itemWidth, jobFreightID, jobID, jobItemFillPercent, jobItemID, jobItemNotes, jobItemParcelValue, jobItemPkdHeight, jobItemPkdLength, jobItemPkdValue, jobItemPkdWeight, jobItemPkdWidth, laborCharge, laborHrs, longestDimension, materialTotalCost, materialWeight, materials, netCubicFeet, nmfcItem, nmfcSub, nmfcSubClass, notedConditions, originalJobItemId, originalQty, parcelPackageTypeId, pkdLengthPlusGirth, quantity, requestedParcelPackagings, rowNumber, scheduleB, secondDimension, stc, totalItems, totalLaborCharge, totalPackedValue, totalPcs, totalWeight, transportationHeight, transportationLength, transportationWeight, transportationWidth, userId |
| List[JobSearchResult] | 21 undeclared field(s): completedDate, createdByUserName, delAddress1, delZipCode, destAddress, estimateDate1, expectedDeliveryDate, expectedPickUpDate, itemName, jobItemsTotalMaterialsLbs, jobMgmtId, jobMgmtStatusName, jobTotalQty, jobTotalValue, jobTotalWeight, orginAddress, psDoneBy, puAddress2, puZipcode, quoteDate1, totalItems |
| List[SearchContactEntityResult] | 30 undeclared field(s): addressesList, assistant, birthDate, bolNotes, careOf, company, companyId, contactTypeId, department, editable, emailsList, fax, fullNameUpdateRequired, isActive, isBusiness, isEmpty, isPayer, isPrefered, isPrimary, isPrivate, jobTitle, jobTitleId, legacyGuid, ownerFranchiseeId, phonesList, primaryEmail, primaryPhone, rootContactId, taxId, webSite |
