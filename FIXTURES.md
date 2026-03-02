# Fixture Tracking

Tracks capture status and quality gates for all endpoint fixtures in `tests/fixtures/`.

**Constitution**: v2.3.0, Principles I–V
**Quality Gates**: G1 (Model Fidelity), G2 (Fixture Status), G3 (Test Quality), G4 (Doc Accuracy), G5 (Param Routing), G6 (Request Quality)
**Rule**: Status is "complete" only when ALL applicable gates pass.

## Summary

- **Total endpoints**: 231
- **Complete (all gates pass)**: 50
- **G1 Model Fidelity**: 66/231 pass
- **G2 Fixture Status**: 87/231 pass
- **G3 Test Quality**: 135/231 pass
- **G4 Doc Accuracy**: 153/231 pass
- **G5 Param Routing**: 216/231 pass
- **G6 Request Quality**: 223/231 pass

## Status Legend

- **complete**: All applicable quality gates pass
- **incomplete**: One or more gates fail
- **PASS/FAIL**: Per-gate status

## ACPortal Endpoints

| Endpoint Path | Method | Python Path | Req Model | Resp Model | G1 | G2 | G3 | G4 | G5 | G6 | Status | Notes |
|---------------|--------|-------------|-----------|------------|----|----|----|----|----|----|----|-------|
| /companies/{id} | GET | api.companies.get_by_id | — | CompanySimple | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /companies/{companyId}/details | GET | api.companies.get_details | — | CompanyDetails | PASS | PASS | PASS | PASS | PASS | PASS | complete | HTTP 500 on staging — needs company UUID with populated details |
| /companies/{companyId}/fulldetails | GET | api.companies.get_fulldetails | — | CompanyDetails | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /companies/{companyId}/fulldetails | PUT | api.companies.update_fulldetails | CompanyDetails | CompanyDetails | PASS | PASS | PASS | PASS | PASS | PASS | complete | Needs valid CompanyDetails kwargs |
| /companies/fulldetails | POST | api.companies.create | CompanyDetails | str | PASS | PASS | PASS | PASS | PASS | PASS | complete | Needs valid CompanyDetails kwargs for new company |
| /companies/search/v2 | POST | api.companies.search | CompanySearchRequest | List[SearchCompanyResponse] | PASS | PASS | PASS | PASS | PASS | PASS | complete | Request fixture captured; response needs valid search that returns results |
| /companies/list | POST | api.companies.list | ListRequest | List[CompanySimple] | PASS | PASS | PASS | PASS | PASS | PASS | complete | Needs valid ListRequest kwargs |
| /companies/availableByCurrentUser | GET | api.companies.available_by_current_user | — | List[CompanySimple] | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /contacts/user | GET | api.contacts.get_current_user | — | ContactSimple | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /contacts/{contactId}/primarydetails | GET | api.contacts.get_primary_details | — | ContactPrimaryDetails | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /contacts/{contactId}/editdetails | GET | api.contacts.get_details | — | ContactDetailedInfo | PASS | PASS | PASS | PASS | PASS | PASS | complete | HTTP 500 on staging — was previously captured but now fails |
| /contacts/v2/search | POST | api.contacts.search | ContactSearchRequest | List[SearchContactEntityResult] | FAIL | PASS | PASS | PASS | PASS | PASS | incomplete | HTTP 400 — needs PageSize (1-32767) and PageNumber (1-32767) in request body |
| /documents | GET | — | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | HTTP 500 on staging — was previously captured but now fails |
| /address/isvalid | GET | api.address.validate | — | AddressIsValidResult | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-14, staging |
| /address/propertytype | GET | api.address.get_property_type | — | int | PASS | PASS | PASS | PASS | PASS | PASS | complete | Query params: needs valid address1, city, state, zip_code for a real address |
| /lookup/contactTypes | GET | api.lookup.get_contact_types | — | List[ContactTypeEntity] | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /lookup/countries | GET | api.lookup.get_countries | — | List[CountryCodeDto] | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /lookup/jobStatuses | GET | api.lookup.get_job_statuses | — | List[JobStatus] | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /lookup/items | GET | api.lookup.get_items | — | List[LookupItem] | PASS | PASS | PASS | PASS | PASS | PASS | complete | Returns 204 — research ABConnectTools for required query params |
| /users/list | POST | api.users.list | ListRequest | List[User] | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging. Model warning: response is paginated wrapper (totalCount, data) |
| /users/roles | GET | api.users.get_roles | — | List[str] | PASS | PASS | PASS | PASS | PASS | PASS | complete | Fixed — route uses List[str]; API returns plain strings, not UserRole objects |
| /job/{jobDisplayId} | GET | api.jobs.get | — | Job | PASS | PASS | PASS | PASS | PASS | PASS | complete | HTTP 500 on staging |
| /job/{jobDisplayId}/price | GET | api.jobs.get_price | — | JobPrice | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /job/{jobDisplayId}/calendaritems | GET | api.jobs.get_calendar_items | — | List[CalendarItem] | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /job/{jobDisplayId}/updatePageConfig | GET | api.jobs.get_update_page_config | — | JobUpdatePageConfig | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /job/search | GET | api.jobs.search | — | JobSearchResult | PASS | PASS | PASS | PASS | PASS | PASS | complete | HTTP 404 on staging |
| /job/{jobDisplayId}/timeline | GET | api.jobs.get_timeline_response | — | TimelineResponse | PASS | PASS | PASS | PASS | PASS | PASS | complete | Needs job ID with active timeline |
| /job/{jobDisplayId}/timeline/{taskCode}/agent | GET | — | — | TimelineAgent | PASS | PASS | PASS | PASS | PASS | PASS | complete | Needs job ID + task code |
| /job/{jobDisplayId}/tracking | GET | api.jobs.get_tracking | — | TrackingInfo | PASS | PASS | PASS | PASS | PASS | PASS | complete | Works but no fixture_file set in example |
| /v3/job/{jobDisplayId}/tracking/{historyAmount} | GET | api.jobs.get_tracking_v3 | — | TrackingInfoV3 | PASS | PASS | PASS | PASS | PASS | PASS | complete | Works but no fixture_file set in example |
| /job/{jobDisplayId}/payment | GET | api.payments.get | — | PaymentInfo | FAIL | FAIL | PASS | FAIL | FAIL | PASS | incomplete | Works but no fixture_file set in example |
| /job/{jobDisplayId}/payment/sources | GET | api.payments.get_sources | — | List[PaymentSource] | FAIL | FAIL | PASS | FAIL | PASS | PASS | incomplete | Works but no fixture_file set in example |
| /job/{jobDisplayId}/payment/ACHPaymentSession | POST | api.payments.create_ach_session | ACHSessionRequest | ACHSessionResponse | FAIL | FAIL | PASS | FAIL | PASS | PASS | incomplete | Needs ACH session params |
| /job/{jobDisplayId}/note | GET | api.jobs.get_notes | — | List[JobNote] | PASS | PASS | PASS | PASS | PASS | PASS | complete | Model bug — id field typed as str but API returns int |
| /job/{jobDisplayId}/parcelitems | GET | api.jobs.get_parcel_items | — | List[ParcelItem] | PASS | PASS | FAIL | PASS | PASS | PASS | incomplete | Returns empty list — needs job with parcel items |
| /job/{jobDisplayId}/parcel-items-with-materials | GET | api.jobs.get_parcel_items_with_materials | — | List[ParcelItemWithMaterials] | PASS | PASS | FAIL | PASS | PASS | PASS | incomplete | Returns empty list — needs job with packed items |
| /job/{jobDisplayId}/packagingcontainers | GET | api.jobs.get_packaging_containers | — | List[PackagingContainer] | PASS | PASS | FAIL | PASS | PASS | PASS | incomplete | Model has warning fields — works but model incomplete |
| /job/{jobDisplayId}/shipment/ratequotes | GET | api.shipments.get_rate_quotes | — | List[RateQuote] | PASS | PASS | PASS | FAIL | FAIL | PASS | incomplete | 2026-02-14, staging |
| /job/{jobDisplayId}/shipment/accessorials | GET | api.shipments.get_accessorials | — | List[Accessorial] | PASS | PASS | PASS | FAIL | PASS | PASS | incomplete | 2026-02-14, staging |
| /job/{jobDisplayId}/shipment/origindestination | GET | api.shipments.get_origin_destination | — | ShipmentOriginDestination | PASS | PASS | PASS | FAIL | PASS | PASS | incomplete | 2026-02-14, staging |
| /job/{jobDisplayId}/shipment/ratesstate | GET | api.shipments.get_rates_state | — | RatesState | PASS | PASS | PASS | FAIL | PASS | PASS | incomplete | 2026-02-14, staging |
| /shipment | GET | api.shipments.get_shipment | — | ShipmentInfo | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-14, staging |
| /shipment/accessorials | GET | api.shipments.get_global_accessorials | — | List[GlobalAccessorial] | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-14, staging |
| /job/{jobDisplayId}/form/shipments | GET | api.forms.get_shipments | — | List[FormsShipmentPlan] | PASS | PASS | PASS | FAIL | PASS | PASS | incomplete | 2026-02-14, staging |
| /autoprice/quickquote | POST | api.autoprice.quick_quote | QuoteRequestModel | QuickQuoteResponse | PASS | PASS | PASS | PASS | PASS | FAIL | incomplete | Request model validation error — field names don't match (originZip vs OriginZip) |
| /AutoPrice/QuoteRequest | POST | — | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | Needs items array with weight, class fields and valid origin/destination |
| /rfq/{rfqId} | GET | api.rfq.get | — | QuoteRequestDisplayInfo | PASS | PASS | PASS | PASS | PASS | PASS | complete | 008 — run examples/rfq.py |
| /rfq/forjob/{jobId} | GET | api.rfq.get_for_job | — | List[QuoteRequestDisplayInfo] | PASS | PASS | PASS | PASS | PASS | PASS | complete | 008 |
| /rfq/{rfqId}/accept | POST | api.rfq.accept | AcceptModel | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 — mutating |
| /rfq/{rfqId}/decline | POST | api.rfq.decline | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 — mutating |
| /rfq/{rfqId}/cancel | POST | api.rfq.cancel | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 — mutating |
| /rfq/{rfqId}/acceptwinner | POST | api.rfq.accept_winner | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 — mutating |
| /rfq/{rfqId}/comment | POST | api.rfq.add_comment | AcceptModel | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/rfq | GET | api.jobs.list_rfqs | — | List[QuoteRequestDisplayInfo] | PASS | PASS | PASS | PASS | PASS | PASS | complete | 008 |
| /job/{jobDisplayId}/rfq/statusof/{rfqServiceType}/forcompany/{companyId} | GET | api.jobs.get_rfq_status | — | int | PASS | PASS | PASS | PASS | PASS | PASS | complete | 008 |
| /job/{jobDisplayId}/onhold | GET | api.jobs.list_on_hold | — | List[ExtendedOnHoldInfo] | PASS | PASS | PASS | PASS | PASS | PASS | complete | 008 |
| /job/{jobDisplayId}/onhold | POST | api.jobs.create_on_hold | SaveOnHoldRequest | SaveOnHoldResponse | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/onhold | DELETE | api.jobs.delete_on_hold | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 — destructive |
| /job/{jobDisplayId}/onhold/{id} | GET | api.jobs.get_on_hold | — | OnHoldDetails | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/onhold/{onHoldId} | PUT | api.jobs.update_on_hold | SaveOnHoldRequest | SaveOnHoldResponse | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/onhold/followupuser/{contactId} | GET | api.jobs.get_on_hold_followup_user | — | OnHoldUser | PASS | PASS | PASS | PASS | PASS | PASS | complete | 008 |
| /job/{jobDisplayId}/onhold/followupusers | GET | api.jobs.list_on_hold_followup_users | — | List[OnHoldUser] | PASS | PASS | PASS | PASS | PASS | PASS | complete | 008 |
| /job/{jobDisplayId}/onhold/{onHoldId}/comment | POST | api.jobs.add_on_hold_comment | OnHoldCommentRequest | OnHoldNoteDetails | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/onhold/{onHoldId}/dates | PUT | api.jobs.update_on_hold_dates | SaveOnHoldDatesModel | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/onhold/{onHoldId}/resolve | PUT | api.jobs.resolve_on_hold | ResolveOnHoldRequest | ResolveJobOnHoldResponse | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /reports/insurance | POST | api.reports.insurance | InsuranceReportRequest | InsuranceReport | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /reports/sales | POST | api.reports.sales | SalesForecastReportRequest | SalesForecastReport | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /reports/sales/summary | POST | api.reports.sales_summary | SalesForecastSummaryRequest | SalesForecastSummary | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /reports/salesDrilldown | POST | api.reports.sales_drilldown | Web2LeadRevenueFilter | List[RevenueCustomer] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /reports/topRevenueCustomers | POST | api.reports.top_revenue_customers | Web2LeadRevenueFilter | List[RevenueCustomer] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /reports/topRevenueSalesReps | POST | api.reports.top_revenue_sales_reps | Web2LeadRevenueFilter | List[RevenueCustomer] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /reports/referredBy | POST | api.reports.referred_by | ReferredByReportRequest | ReferredByReport | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /reports/web2Lead | POST | api.reports.web2lead | Web2LeadV2RequestModel | Web2LeadReport | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/email | POST | api.jobs.send_email | SendEmailRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 — fire-and-forget |
| /job/{jobDisplayId}/email/senddocument | POST | api.jobs.send_document_email | SendDocumentEmailModel | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/email/createtransactionalemail | POST | api.jobs.create_transactional_email | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/email/{emailTemplateGuid}/send | POST | api.jobs.send_template_email | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/sms | GET | api.jobs.list_sms | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/sms | POST | api.jobs.send_sms | SendSMSModel | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/sms/read | POST | api.jobs.mark_sms_read | MarkSmsAsReadModel | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/sms/templatebased/{templateId} | GET | api.jobs.get_sms_template | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /lookup/{masterConstantKey} | GET | api.lookup.get_by_key | — | List[LookupValue] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /lookup/{masterConstantKey}/{valueId} | GET | api.lookup.get_by_key_and_id | — | LookupValue | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /lookup/accessKeys | GET | api.lookup.get_access_keys | — | List[AccessKey] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /lookup/accessKey/{accessKey} | GET | api.lookup.get_access_key | — | AccessKey | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /lookup/PPCCampaigns | GET | api.lookup.get_ppc_campaigns | — | List[LookupValue] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /lookup/parcelPackageTypes | GET | api.lookup.get_parcel_package_types | — | List[ParcelPackageType] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /lookup/documentTypes | GET | api.lookup.get_document_types | — | List[LookupValue] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /lookup/comonInsurance | GET | api.lookup.get_common_insurance | — | List[LookupValue] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /lookup/densityClassMap | GET | api.lookup.get_density_class_map | — | List[DensityClassEntry] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /lookup/referCategory | GET | api.lookup.get_refer_categories | — | List[LookupValue] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /lookup/referCategoryHeirachy | GET | api.lookup.get_refer_category_hierarchy | — | List[LookupValue] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /lookup/resetMasterConstantCache | GET | api.lookup.reset_cache | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 — mutating |
| /commodity/{id} | GET | api.commodities.get | — | Commodity | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /commodity/{id} | PUT | api.commodities.update | CommodityUpdateRequest | Commodity | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /commodity | POST | api.commodities.create | CommodityCreateRequest | Commodity | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /commodity/search | POST | api.commodities.search | CommoditySearchRequest | List[Commodity] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /commodity/suggestions | POST | api.commodities.suggestions | CommoditySuggestionRequest | List[Commodity] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /commodity-map/{id} | GET | api.commodity_maps.get | — | CommodityMap | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /commodity-map/{id} | PUT | api.commodity_maps.update | CommodityMapUpdateRequest | CommodityMap | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /commodity-map/{id} | DELETE | api.commodity_maps.delete | — | ServiceBaseResponse | FAIL | PASS | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /commodity-map | POST | api.commodity_maps.create | CommodityMapCreateRequest | CommodityMap | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /commodity-map/search | POST | api.commodity_maps.search | CommodityMapSearchRequest | List[CommodityMap] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /dashboard | GET | api.dashboard.get | — | DashboardSummary | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /dashboard/gridviews | GET | api.dashboard.get_grid_views | — | List[GridViewInfo] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /dashboard/gridviewstate/{id} | GET | api.dashboard.get_grid_view_state | — | GridViewState | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /dashboard/gridviewstate/{id} | POST | api.dashboard.save_grid_view_state | GridViewState | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /dashboard/inbound | POST | api.dashboard.inbound | DashboardCompanyRequest | — | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /dashboard/inhouse | POST | api.dashboard.in_house | DashboardCompanyRequest | — | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /dashboard/outbound | POST | api.dashboard.outbound | DashboardCompanyRequest | — | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /dashboard/local-deliveries | POST | api.dashboard.local_deliveries | DashboardCompanyRequest | — | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /dashboard/recentestimates | POST | api.dashboard.recent_estimates | DashboardCompanyRequest | — | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /views/all | GET | api.views.list | — | List[GridViewDetails] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /views/{viewId} | GET | api.views.get | — | GridViewDetails | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /views | POST | api.views.create | GridViewCreateRequest | GridViewDetails | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /views/{viewId} | DELETE | api.views.delete | — | ServiceBaseResponse | FAIL | PASS | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /views/{viewId}/accessinfo | GET | api.views.get_access_info | — | GridViewAccess | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /views/{viewId}/access | PUT | api.views.update_access | GridViewAccess | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /views/datasetsps | GET | api.views.get_dataset_sps | — | List[StoredProcedureColumn] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /views/datasetsp/{spName} | GET | api.views.get_dataset_sp | — | List[StoredProcedureColumn] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /companies/brands | GET | api.companies.get_brands | — | List[CompanyBrand] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /companies/brandstree | GET | api.companies.get_brands_tree | — | List[BrandTree] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /companies/geoAreaCompanies | GET | api.companies.get_geo_area_companies | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /companies/{companyId}/geosettings | GET | api.companies.get_geo_settings | — | GeoSettings | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /companies/{companyId}/geosettings | POST | api.companies.save_geo_settings | GeoSettingsSaveRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /companies/geosettings | GET | api.companies.get_global_geo_settings | — | GeoSettings | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /companies/search/carrier-accounts | GET | api.companies.search_carrier_accounts | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /companies/suggest-carriers | GET | api.companies.suggest_carriers | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /companies/{companyId}/carrierAcounts | GET | api.companies.get_carrier_accounts | — | List[CarrierAccount] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /companies/{companyId}/carrierAcounts | POST | api.companies.save_carrier_accounts | CarrierAccountSaveRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /companies/{companyId}/packagingsettings | GET | api.companies.get_packaging_settings | — | PackagingSettings | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /companies/{companyId}/packagingsettings | POST | api.companies.save_packaging_settings | PackagingSettingsSaveRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /companies/{companyId}/packaginglabor | GET | api.companies.get_packaging_labor | — | PackagingLabor | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /companies/{companyId}/packaginglabor | POST | api.companies.save_packaging_labor | PackagingLaborSaveRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /companies/{companyId}/inheritedPackagingTariffs | GET | api.companies.get_inherited_packaging_tariffs | — | List[PackagingTariff] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /companies/{companyId}/inheritedpackaginglabor | GET | api.companies.get_inherited_packaging_labor | — | PackagingLabor | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /contacts/{contactId}/history | POST | api.contacts.post_history | ContactHistoryCreateRequest | ContactHistory | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /contacts/{contactId}/history/aggregated | GET | api.contacts.get_history_aggregated | — | ContactHistoryAggregated | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /contacts/{contactId}/history/graphdata | GET | api.contacts.get_history_graph_data | — | ContactGraphData | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /contacts/{mergeToId}/merge/preview | POST | api.contacts.merge_preview | ContactMergeRequest | ContactMergePreview | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /contacts/{mergeToId}/merge | PUT | api.contacts.merge | ContactMergeRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 — destructive |
| /job/{jobDisplayId}/freightproviders | GET | api.jobs.list_freight_providers | — | List[PricedFreightProvider] | PASS | PASS | PASS | PASS | PASS | PASS | complete | 008 |
| /job/{jobDisplayId}/freightproviders | POST | api.jobs.save_freight_providers | ShipmentPlanProvider | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/freightproviders/{optionIndex}/ratequote | POST | api.jobs.get_freight_provider_rate_quote | RateQuoteRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /job/{jobDisplayId}/freightitems | POST | api.jobs.add_freight_items | FreightItemsRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /note | GET | api.notes.list | — | List[GlobalNote] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /note | POST | api.notes.create | GlobalNoteCreateRequest | GlobalNote | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /note/{id} | PUT | api.notes.update | GlobalNoteUpdateRequest | GlobalNote | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /note/suggestUsers | GET | api.notes.suggest_users | — | List[SuggestedUser] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /partner | GET | api.partners.list | — | List[Partner] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /partner/{id} | GET | api.partners.get | — | Partner | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /partner/search | POST | api.partners.search | PartnerSearchRequest | List[Partner] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 008 |
| /Seller/{id} | GET | api.sellers.get | — | SellerExpandedDto | PASS | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /Seller | GET | — | — | PaginatedList[SellerExpandedDto] | FAIL | FAIL | FAIL | PASS | FAIL | PASS | incomplete | 2026-02-14, staging |
| /Catalog | GET | — | — | PaginatedList[CatalogExpandedDto] | FAIL | FAIL | FAIL | PASS | FAIL | PASS | incomplete | Returns empty — research ABConnectTools for required params |
| /Catalog/{id} | GET | api.catalog.get | — | CatalogExpandedDto | PASS | PASS | PASS | PASS | PASS | PASS | complete | Needs valid catalog ID |
| /Lot | GET | — | — | PaginatedList[LotDto] | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | Needs valid catalog ID param |
| /Lot/{id} | GET | api.lots.get | — | LotDto | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | Needs valid lot ID |
| /Lot/overrides | POST | — | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | Needs lot override params |
| /Web2Lead | GET | — | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 2026-02-13, staging |
| /Web2Lead/post | POST | api.web2lead.post | Web2LeadRequest | Web2LeadResponse | PASS | PASS | PASS | PASS | PASS | FAIL | incomplete | 020 |
| /job | POST | api.jobs.create | JobCreateRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /job/update | POST | api.jobs.update | JobUpdateRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /job/save | PUT | api.jobs.save | JobSaveRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /job/transfer/{jobDisplayId} | POST | api.jobs.transfer | TransferModel | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/status/quote | POST | api.jobs.set_quote_status | — | ServiceBaseResponse | FAIL | PASS | FAIL | PASS | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/shipment/ratequotes | POST | api.shipments.request_rate_quotes | ShipmentRateQuoteRequest | List[RateQuote] | PASS | PASS | PASS | FAIL | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/shipment/book | POST | api.shipments.book | ShipmentBookRequest | ServiceBaseResponse | FAIL | PASS | FAIL | PASS | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/shipment | DELETE | api.shipments.delete_shipment | — | ServiceBaseResponse | FAIL | PASS | FAIL | PASS | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/shipment/accessorial | POST | api.shipments.add_accessorial | AccessorialAddRequest | ServiceBaseResponse | FAIL | PASS | FAIL | PASS | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/shipment/accessorial/{addOnId} | DELETE | api.shipments.remove_accessorial | — | ServiceBaseResponse | FAIL | PASS | FAIL | PASS | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/shipment/exportdata | POST | api.shipments.post_export_data | ShipmentExportRequest | ServiceBaseResponse | FAIL | PASS | FAIL | PASS | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/payment/bysource | POST | api.payments.pay_by_source | PayBySourceRequest | ServiceBaseResponse | FAIL | PASS | FAIL | PASS | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/payment/ACHCreditTransfer | POST | api.payments.ach_credit_transfer | ACHCreditTransferRequest | ServiceBaseResponse | FAIL | PASS | FAIL | PASS | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/payment/attachCustomerBank | POST | api.payments.attach_customer_bank | AttachBankRequest | ServiceBaseResponse | FAIL | PASS | FAIL | PASS | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/payment/verifyJobACHSource | POST | api.payments.verify_ach_source | VerifyACHRequest | ServiceBaseResponse | FAIL | PASS | FAIL | PASS | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/payment/banksource | POST | api.payments.set_bank_source | BankSourceRequest | ServiceBaseResponse | FAIL | PASS | FAIL | PASS | PASS | PASS | incomplete | 020 |
| /job/{jobDisplayId}/payment/cancelJobACHVerification | POST | api.payments.cancel_ach_verification | — | ServiceBaseResponse | FAIL | PASS | FAIL | PASS | PASS | PASS | incomplete | 020 |
| /contacts/editdetails | POST | api.contacts.create | ContactEditRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /contacts/{contactId}/editdetails | PUT | api.contacts.update_details | ContactEditRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /documents | POST | — | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /documents/update/{docId} | PUT | api.documents.update | DocumentUpdateRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /users/user | POST | api.users.create | UserCreateRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /users/user | PUT | api.users.update | UserUpdateRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /autoprice/v2/quoterequest | POST | api.autoprice.quote_request | QuoteRequestModel | QuoteRequestResponse | FAIL | FAIL | PASS | PASS | PASS | FAIL | incomplete | auto-discovered |
| /Catalog/{id} | DELETE | api.catalog.delete | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /Catalog/{id} | PUT | api.catalog.update | UpdateCatalogRequest | CatalogWithSellersDto | FAIL | FAIL | PASS | PASS | PASS | FAIL | incomplete | 020 |
| /Bulk/insert | POST | api.catalog.bulk_insert | BulkInsertRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | FAIL | incomplete | 020 |
| /Seller | POST | api.sellers.create | AddSellerRequest | SellerDto | PASS | PASS | PASS | PASS | PASS | FAIL | incomplete | 020 |
| /Seller/{id} | PUT | api.sellers.update | UpdateSellerRequest | SellerDto | PASS | PASS | PASS | PASS | PASS | FAIL | incomplete | 020 |
| /Seller/{id} | DELETE | api.sellers.delete | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /Lot | POST | api.lots.create | AddLotRequest | LotDto | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 020 |
| /Lot/{id} | PUT | api.lots.update | UpdateLotRequest | LotDto | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 020 |
| /Lot/{id} | DELETE | api.lots.delete | — | — | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 020 |
| /Lot/get-overrides | POST | api.lots.get_overrides | — | List[LotOverrideDto] | FAIL | FAIL | PASS | PASS | PASS | PASS | incomplete | 020 |
| /Catalog | POST | api.catalog.create | AddCatalogRequest | CatalogWithSellersDto | FAIL | FAIL | PASS | PASS | PASS | FAIL | incomplete | auto-discovered |
| /contacts/{id} | GET | api.contacts.get | — | ContactSimple | PASS | PASS | PASS | PASS | PASS | PASS | complete | auto-discovered |
| /documents/get/{docPath} | GET | — | — | bytes | FAIL | FAIL | FAIL | PASS | PASS | PASS | incomplete | auto-discovered |
| /documents/list | GET | api.documents.list | — | List[Document] | PASS | PASS | PASS | PASS | PASS | PASS | complete | auto-discovered |
| /job/{jobDisplayId}/form/address-label | GET | — | — | bytes | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/bill-of-lading | GET | — | — | bytes | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/credit-card-authorization | GET | — | — | bytes | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/customer-quote | GET | — | — | bytes | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/invoice | GET | — | — | bytes | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/invoice/editable | GET | — | — | bytes | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/item-labels | GET | — | — | bytes | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/operations | GET | — | — | bytes | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/packaging-labels | GET | — | — | bytes | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/packaging-specification | GET | — | — | bytes | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/packing-slip | GET | — | — | bytes | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/quick-sale | GET | — | — | bytes | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/usar | GET | — | — | bytes | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/form/usar/editable | GET | — | — | bytes | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/parcelitems/{parcelItemId} | DELETE | api.jobs.delete_parcel_item | — | ServiceBaseResponse | FAIL | PASS | FAIL | PASS | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/timeline/{timelineTaskId} | DELETE | api.jobs.delete_timeline_task | — | ServiceBaseResponse | FAIL | PASS | FAIL | PASS | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/note/{id} | GET | api.jobs.get_note | — | JobNote | PASS | PASS | PASS | PASS | PASS | PASS | complete | auto-discovered |
| /job/{jobDisplayId}/timeline/{timelineTaskIdentifier} | GET | api.jobs.get_timeline_task | — | TimelineTask | PASS | PASS | PASS | PASS | PASS | PASS | complete | auto-discovered |
| /job/{jobDisplayId}/timeline/incrementjobstatus | POST | api.jobs.increment_status | IncrementStatusRequest | ServiceBaseResponse | FAIL | PASS | FAIL | PASS | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/timeline/{timelineTaskId} | PATCH | api.jobs.update_timeline_task | TimelineTaskUpdateRequest | TimelineTask | PASS | PASS | PASS | PASS | PASS | PASS | complete | auto-discovered |
| /job/{jobDisplayId}/item/notes | POST | api.jobs.add_item_notes | ItemNotesRequest | ServiceBaseResponse | FAIL | PASS | FAIL | PASS | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/note | POST | api.jobs.create_note | JobNoteCreateRequest | JobNote | PASS | PASS | PASS | PASS | PASS | PASS | complete | auto-discovered |
| /job/{jobDisplayId}/parcelitems | POST | api.jobs.create_parcel_item | ParcelItemCreateRequest | ParcelItem | PASS | PASS | FAIL | PASS | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/timeline | POST | api.jobs.create_timeline_task | — | TimelineSaveResponse | PASS | PASS | PASS | PASS | PASS | PASS | complete | auto-discovered |
| /job/{jobDisplayId}/item/{itemId} | PUT | api.jobs.update_item | ItemUpdateRequest | ServiceBaseResponse | FAIL | PASS | FAIL | PASS | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/note/{id} | PUT | api.jobs.update_note | JobNoteUpdateRequest | JobNote | PASS | PASS | PASS | PASS | PASS | PASS | complete | auto-discovered |
| /job/searchByDetails | POST | api.jobs.search_by_details | JobSearchRequest | List[JobSearchResult] | PASS | PASS | PASS | PASS | PASS | PASS | complete | auto-discovered |
| /job/{jobDisplayId}/timeline/undoincrementjobstatus | POST | api.jobs.undo_increment_status | IncrementStatusRequest | ServiceBaseResponse | FAIL | PASS | FAIL | PASS | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/payment/create | GET | api.payments.get_create | — | PaymentInfo | FAIL | FAIL | PASS | FAIL | PASS | PASS | incomplete | auto-discovered |
| /job/{jobDisplayId}/shipment/exportdata | GET | api.shipments.get_export_data | — | ShipmentExportData | PASS | PASS | FAIL | FAIL | PASS | PASS | incomplete | auto-discovered |
| /shipment/document/{docId} | GET | api.shipments.get_shipment_document | — | bytes | FAIL | FAIL | FAIL | FAIL | PASS | PASS | incomplete | auto-discovered |
| /Web2Lead/get | GET | api.web2lead.get | — | Web2LeadResponse | PASS | PASS | PASS | PASS | FAIL | PASS | incomplete | auto-discovered |

## Model Warning Summary

Models with `__pydantic_extra__` fields when validated against their fixtures:

| Model | Issue |
|-------|-------|
| List[SearchContactEntityResult] | 31 undeclared field(s): addressesList, assistant, birthDate, bolNotes, careOf, company, companyId, contactTypeId, department, editable, emailsList, fax, fullName, fullNameUpdateRequired, id, isActive, isBusiness, isEmpty, isPayer, isPrimary, isPrivate, jobTitle, jobTitleId, legacyGuid, ownerFranchiseeId, phonesList, primaryEmail, primaryPhone, rootContactId, taxId, webSite |
| ServiceBaseResponse | 13 undeclared field(s): carrierAPI, confirmRequired, currencyCode, documents, errors, fedExExpressFreightDetailRequired, internationalInfoRequired, notifications, shipOutDateRequired, shipmentAcceptIdentifier, shipmentId, totalNetChargeAmount, weight |
