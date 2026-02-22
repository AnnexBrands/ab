# Fixture Tracking

Tracks capture status and quality gates for all endpoint fixtures in `tests/fixtures/`.

**Constitution**: v2.3.0, Principles I–V
**Quality Gates**: G1 (Model Fidelity), G2 (Fixture Status), G3 (Test Quality), G4 (Doc Accuracy), G5 (Param Routing)
**Rule**: Status is "complete" only when ALL applicable gates pass.

## Summary

- **Total endpoints**: 161
- **Complete (all gates pass)**: 24
- **G1 Model Fidelity**: 30/161 pass
- **G2 Fixture Status**: 35/161 pass
- **G3 Test Quality**: 123/161 pass
- **G4 Doc Accuracy**: 116/161 pass
- **G5 Param Routing**: 153/161 pass

## Status Legend

- **complete**: All applicable quality gates pass
- **incomplete**: One or more gates fail
- **PASS/FAIL**: Per-gate status

## ACPortal Endpoints

| Endpoint Path | Method | Req Model | Resp Model | G1 | G2 | G3 | G4 | G5 | Status | Notes |
|---------------|--------|-----------|------------|----|----|----|----|----|--------|-------|
| /companies/{id} | GET | — | CompanySimple | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /companies/{id}/details | GET | — | CompanyDetails | PASS | PASS | PASS | PASS | PASS | complete | HTTP 500 on staging — needs company UUID with populated details |
| /companies/{id}/fulldetails | GET | — | CompanyDetails | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /companies/{companyId}/fulldetails | PUT | CompanyDetails | CompanyDetails | PASS | PASS | PASS | PASS | PASS | complete | Needs valid CompanyDetails kwargs |
| /companies/fulldetails | POST | CompanyDetails | str | FAIL | FAIL | PASS | PASS | PASS | incomplete | Needs valid CompanyDetails kwargs for new company |
| /companies/search/v2 | POST | CompanySearchRequest | List[SearchCompanyResponse] | PASS | PASS | PASS | PASS | PASS | complete | Request fixture captured; response needs valid search that returns results |
| /companies/list | POST | ListRequest | List[CompanySimple] | PASS | PASS | PASS | PASS | PASS | complete | Needs valid ListRequest kwargs |
| /companies/availableByCurrentUser | GET | — | SearchCompanyResponse | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /contacts/user | GET | — | ContactSimple | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /contacts/{id}/primarydetails | GET | — | ContactPrimaryDetails | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /contacts/{id}/editdetails | GET | — | ContactDetailedInfo | FAIL | PASS | PASS | PASS | PASS | incomplete | HTTP 500 on staging — was previously captured but now fails |
| /contacts/v2/search | POST | SearchContactEntityResult | SearchContactEntityResult | FAIL | PASS | PASS | PASS | PASS | incomplete | HTTP 400 — needs PageSize (1-32767) and PageNumber (1-32767) in request body |
| /documents | GET | — | Document | PASS | PASS | PASS | PASS | PASS | complete | HTTP 500 on staging — was previously captured but now fails |
| /address/isvalid | GET | — | AddressIsValidResult | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-14, staging |
| /address/propertytype | GET | — | PropertyType | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | Query params: needs valid address1, city, state, zip_code for a real address |
| /lookup/contacttypes | GET | — | ContactTypeEntity | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /lookup/countries | GET | — | CountryCodeDto | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /lookup/jobstatuses | GET | — | JobStatus | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /lookup/items | GET | — | LookupItem | FAIL | FAIL | PASS | PASS | PASS | incomplete | Returns 204 — research ABConnectTools for required query params |
| /users/list | POST | — | User | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging. Model warning: response is paginated wrapper (totalCount, data) |
| /users/roles | GET | — | UserRole | FAIL | PASS | FAIL | FAIL | PASS | incomplete | Fixed — route uses List[str]; API returns plain strings, not UserRole objects |
| /job/{id} | GET | — | Job | FAIL | PASS | PASS | PASS | PASS | incomplete | HTTP 500 on staging |
| /job/{id}/price | GET | — | JobPrice | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /job/{id}/calendaritems | GET | — | CalendarItem | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /job/{id}/updatePageConfig | GET | — | JobUpdatePageConfig | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /job/search | GET | — | JobSearchResult | FAIL | PASS | PASS | PASS | PASS | incomplete | HTTP 404 on staging |
| /job/{id}/timeline | GET | — | TimelineTask | FAIL | FAIL | PASS | PASS | PASS | incomplete | Needs job ID with active timeline |
| /job/{id}/timeline/{taskCode}/agent | GET | — | TimelineAgent | FAIL | FAIL | PASS | PASS | PASS | incomplete | Needs job ID + task code |
| /job/{id}/tracking | GET | — | TrackingInfo | FAIL | FAIL | PASS | PASS | PASS | incomplete | Works but no fixture_file set in example |
| /v3/job/{id}/tracking/{historyAmount} | GET | — | TrackingInfoV3 | FAIL | FAIL | PASS | PASS | PASS | incomplete | Works but no fixture_file set in example |
| /job/{id}/payment | GET | — | PaymentInfo | FAIL | FAIL | PASS | FAIL | FAIL | incomplete | Works but no fixture_file set in example |
| /job/{id}/payment/sources | GET | — | PaymentSource | FAIL | FAIL | PASS | FAIL | PASS | incomplete | Works but no fixture_file set in example |
| /job/{id}/payment/ACHPaymentSession | POST | ACHSessionResponse | ACHSessionResponse | FAIL | FAIL | PASS | FAIL | PASS | incomplete | Needs ACH session params |
| /job/{id}/note | GET | — | JobNote | FAIL | FAIL | PASS | PASS | PASS | incomplete | Model bug — id field typed as str but API returns int |
| /job/{id}/parcelitems | GET | — | ParcelItem | FAIL | FAIL | PASS | PASS | PASS | incomplete | Returns empty list — needs job with parcel items |
| /job/{id}/parcel-items-with-materials | GET | — | ParcelItemWithMaterials | FAIL | FAIL | PASS | PASS | PASS | incomplete | Returns empty list — needs job with packed items |
| /job/{id}/packagingcontainers | GET | — | PackagingContainer | FAIL | FAIL | PASS | PASS | PASS | incomplete | Model has warning fields — works but model incomplete |
| /job/{id}/shipment/ratequotes | GET | — | RateQuote | PASS | PASS | PASS | FAIL | FAIL | incomplete | 2026-02-14, staging |
| /job/{id}/shipment/accessorials | GET | — | Accessorial | PASS | PASS | PASS | FAIL | PASS | incomplete | 2026-02-14, staging |
| /job/{id}/shipment/origindestination | GET | — | ShipmentOriginDestination | PASS | PASS | PASS | FAIL | PASS | incomplete | 2026-02-14, staging |
| /job/{id}/shipment/ratesstate | GET | — | RatesState | PASS | PASS | PASS | FAIL | PASS | incomplete | 2026-02-14, staging |
| /shipment | GET | — | ShipmentInfo | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-14, staging |
| /shipment/accessorials | GET | — | GlobalAccessorial | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-14, staging |
| /job/{id}/form/shipments | GET | — | FormsShipmentPlan | PASS | PASS | PASS | FAIL | PASS | incomplete | 2026-02-14, staging |
| /AutoPrice/QuickQuote | POST | QuoteRequestModel | QuickQuoteResponse | PASS | PASS | PASS | PASS | PASS | complete | Request model validation error — field names don't match (originZip vs OriginZip) |
| /AutoPrice/QuoteRequest | POST | QuoteRequestModel | QuoteRequestResponse | FAIL | FAIL | PASS | PASS | PASS | incomplete | Needs items array with weight, class fields and valid origin/destination |
| /rfq/{rfqId} | GET | — | QuoteRequestDisplayInfo | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 — run examples/rfq.py |
| /rfq/forjob/{jobId} | GET | — | List[QuoteRequestDisplayInfo] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /rfq/{rfqId}/accept | POST | AcceptModel | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 — mutating |
| /rfq/{rfqId}/decline | POST | — | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 — mutating |
| /rfq/{rfqId}/cancel | POST | — | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 — mutating |
| /rfq/{rfqId}/acceptwinner | POST | — | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 — mutating |
| /rfq/{rfqId}/comment | POST | AcceptModel | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /job/{id}/rfq | GET | — | List[QuoteRequestDisplayInfo] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /job/{id}/rfq/statusof/{type}/forcompany/{id} | GET | — | QuoteRequestStatus | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /job/{id}/onhold | GET | — | List[ExtendedOnHoldInfo] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /job/{id}/onhold | POST | SaveOnHoldRequest | SaveOnHoldResponse | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /job/{id}/onhold | DELETE | — | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 — destructive |
| /job/{id}/onhold/{id} | GET | — | OnHoldDetails | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /job/{id}/onhold/{id} | PUT | SaveOnHoldRequest | SaveOnHoldResponse | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /job/{id}/onhold/followupuser/{contactId} | GET | — | OnHoldUser | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /job/{id}/onhold/followupusers | GET | — | List[OnHoldUser] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /job/{id}/onhold/{id}/comment | POST | — | OnHoldNoteDetails | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /job/{id}/onhold/{id}/dates | PUT | SaveOnHoldDatesModel | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /job/{id}/onhold/{id}/resolve | PUT | — | ResolveJobOnHoldResponse | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /reports/insurance | POST | InsuranceReportRequest | InsuranceReport | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /reports/sales | POST | SalesForecastReportRequest | SalesForecastReport | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /reports/sales/summary | POST | SalesForecastSummaryRequest | SalesForecastSummary | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /reports/salesDrilldown | POST | Web2LeadRevenueFilter | List[RevenueCustomer] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /reports/topRevenueCustomers | POST | Web2LeadRevenueFilter | List[RevenueCustomer] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /reports/topRevenueSalesReps | POST | Web2LeadRevenueFilter | List[RevenueCustomer] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /reports/referredBy | POST | ReferredByReportRequest | ReferredByReport | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /reports/web2Lead | POST | Web2LeadV2RequestModel | Web2LeadReport | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /job/{id}/email | POST | — | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 — fire-and-forget |
| /job/{id}/email/senddocument | POST | SendDocumentEmailModel | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /job/{id}/email/createtransactionalemail | POST | — | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /job/{id}/email/{templateGuid}/send | POST | — | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /job/{id}/sms | GET | — | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /job/{id}/sms | POST | SendSMSModel | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /job/{id}/sms/read | POST | MarkSmsAsReadModel | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /job/{id}/sms/templatebased/{templateId} | GET | — | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /lookup/{masterConstantKey} | GET | — | List[LookupValue] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /lookup/{masterConstantKey}/{valueId} | GET | — | LookupValue | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /lookup/accessKeys | GET | — | List[AccessKey] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /lookup/accessKey/{accessKey} | GET | — | AccessKey | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /lookup/PPCCampaigns | GET | — | List[LookupValue] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /lookup/parcelPackageTypes | GET | — | List[ParcelPackageType] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /lookup/documentTypes | GET | — | List[LookupValue] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /lookup/comonInsurance | GET | — | List[LookupValue] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /lookup/densityClassMap | GET | — | List[DensityClassEntry] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /lookup/referCategory | GET | — | List[LookupValue] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /lookup/referCategoryHeirachy | GET | — | List[LookupValue] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /lookup/resetMasterConstantCache | GET | — | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 — mutating |
| /commodity/{id} | GET | — | Commodity | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /commodity/{id} | PUT | CommodityUpdateRequest | Commodity | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /commodity | POST | CommodityCreateRequest | Commodity | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /commodity/search | POST | CommoditySearchRequest | List[Commodity] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /commodity/suggestions | POST | CommoditySuggestionRequest | List[Commodity] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /commodity-map/{id} | GET | — | CommodityMap | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /commodity-map/{id} | PUT | CommodityMapUpdateRequest | CommodityMap | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /commodity-map/{id} | DELETE | — | ServiceBaseResponse | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /commodity-map | POST | CommodityMapCreateRequest | CommodityMap | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /commodity-map/search | POST | CommodityMapSearchRequest | List[CommodityMap] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /dashboard | GET | — | DashboardSummary | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /dashboard/gridviews | GET | — | List[GridViewInfo] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /dashboard/gridviewstate/{id} | GET | — | GridViewState | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /dashboard/gridviewstate/{id} | POST | GridViewState | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /dashboard/inbound | POST | — | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /dashboard/inhouse | POST | — | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /dashboard/outbound | POST | — | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /dashboard/local-deliveries | POST | — | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /dashboard/recentestimates | POST | — | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /views/all | GET | — | List[GridViewDetails] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /views/{viewId} | GET | — | GridViewDetails | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /views | POST | GridViewCreateRequest | GridViewDetails | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /views/{viewId} | DELETE | — | ServiceBaseResponse | FAIL | FAIL | FAIL | PASS | PASS | incomplete | 008 |
| /views/{viewId}/accessinfo | GET | — | GridViewAccess | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /views/{viewId}/access | PUT | GridViewAccess | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /views/datasetsps | GET | — | List[StoredProcedureColumn] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /views/datasetsp/{spName} | GET | — | List[StoredProcedureColumn] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /companies/brands | GET | — | List[CompanyBrand] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /companies/brandstree | GET | — | List[BrandTree] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /companies/geoAreaCompanies | GET | — | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /companies/{id}/geosettings | GET | — | GeoSettings | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /companies/{id}/geosettings | POST | GeoSettingsSaveRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /companies/geosettings | GET | — | GeoSettings | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /companies/search/carrier-accounts | GET | — | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /companies/suggest-carriers | GET | — | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /companies/{id}/carrierAcounts | GET | — | List[CarrierAccount] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /companies/{id}/carrierAcounts | POST | CarrierAccountSaveRequest | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /companies/{id}/packagingsettings | GET | — | PackagingSettings | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /companies/{id}/packagingsettings | POST | — | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /companies/{id}/packaginglabor | GET | — | PackagingLabor | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /companies/{id}/packaginglabor | POST | — | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /companies/{id}/inheritedPackagingTariffs | GET | — | List[PackagingTariff] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /companies/{id}/inheritedpackaginglabor | GET | — | PackagingLabor | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /contacts/{contactId}/history | POST | — | ContactHistory | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /contacts/{contactId}/history/aggregated | GET | — | ContactHistoryAggregated | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /contacts/{contactId}/history/graphdata | GET | — | ContactGraphData | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /contacts/{mergeToId}/merge/preview | POST | — | ContactMergePreview | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /contacts/{mergeToId}/merge | PUT | — | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 — destructive |
| /job/{id}/freightproviders | GET | — | List[PricedFreightProvider] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /job/{id}/freightproviders | POST | ShipmentPlanProvider | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /job/{id}/freightproviders/{idx}/ratequote | POST | — | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /job/{id}/freightitems | POST | — | — | FAIL | FAIL | FAIL | FAIL | PASS | incomplete | 008 |
| /note | GET | — | List[GlobalNote] | FAIL | FAIL | PASS | PASS | FAIL | incomplete | 008 |
| /note | POST | GlobalNoteCreateRequest | GlobalNote | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /note/{id} | PUT | GlobalNoteUpdateRequest | GlobalNote | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /note/suggestUsers | GET | — | List[SuggestedUser] | FAIL | FAIL | PASS | PASS | FAIL | incomplete | 008 |
| /partner | GET | — | List[Partner] | FAIL | FAIL | PASS | PASS | FAIL | incomplete | 008 |
| /partner/{id} | GET | — | Partner | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /partner/search | POST | PartnerSearchRequest | List[Partner] | FAIL | FAIL | PASS | PASS | PASS | incomplete | 008 |
| /Seller/{id} | GET | — | SellerDto | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /Seller/{id} | GET | — | SellerExpandedDto | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |
| /Seller | GET | — | SellerExpandedDto | PASS | PASS | PASS | PASS | FAIL | incomplete | 2026-02-14, staging |
| /Catalog | GET | — | CatalogWithSellersDto | FAIL | FAIL | PASS | PASS | FAIL | incomplete | Returns empty — research ABConnectTools for required params |
| /Catalog/{id} | GET | — | CatalogExpandedDto | FAIL | FAIL | PASS | PASS | PASS | incomplete | Needs valid catalog ID |
| /Lot | GET | — | LotDto | FAIL | FAIL | PASS | PASS | FAIL | incomplete | Needs valid catalog ID param |
| /Lot/{id} | GET | — | LotDataDto | FAIL | FAIL | PASS | FAIL | PASS | incomplete | Needs valid lot ID |
| /Lot/overrides | POST | LotOverrideDto | LotOverrideDto | FAIL | FAIL | PASS | PASS | PASS | incomplete | Needs lot override params |
| /Web2Lead | GET | — | Web2LeadResponse | PASS | PASS | PASS | PASS | PASS | complete | 2026-02-13, staging |

## Model Warning Summary

Models with `__pydantic_extra__` fields when validated against their fixtures:

| Model | Issue |
|-------|-------|
| ContactDetailedInfo | 31 undeclared field(s): addressesList, assistant, birthDate, bolNotes, careOf, company, companyId, contactDisplayId, contactTypeId, department, editable, emailsList, fax, fullName, fullNameUpdateRequired, isBusiness, isEmpty, isPayer, isPrefered, isPrimary, isPrivate, jobTitle, jobTitleId, legacyGuid, ownerFranchiseeId, phonesList, primaryEmail, primaryPhone, rootContactId, taxId, webSite |
| Job | 85 undeclared field(s): autoPackFailed, autoPackOff, cFillId, cFillValue, cPackId, cPackValue, ceilingTransportationWeight, commodityId, companyID, companyName, containerId, containerThickness, containerType, containerWeight, customerItemId, descriptionOfProducts, doNotTip, documentExists, eccn, fillWeight, forceCrate, grossCubicFeet, inchesToAdd, isAccess, isContainerChanged, isFillChanged, isFillPercentChanged, isInchToAddChanged, isPrepacked, isValidContainer, isValidFill, itemActive, itemDescription, itemHeight, itemID, itemLength, itemName, itemNotes, itemPublic, itemSequenceNo, itemValue, itemWeight, itemWidth, jobFreightID, jobID, jobItemFillPercent, jobItemID, jobItemNotes, jobItemParcelValue, jobItemPkdHeight, jobItemPkdLength, jobItemPkdValue, jobItemPkdWeight, jobItemPkdWidth, laborCharge, laborHrs, longestDimension, materialTotalCost, materialWeight, materials, netCubicFeet, nmfcItem, nmfcSub, nmfcSubClass, notedConditions, originalJobItemId, originalQty, parcelPackageTypeId, pkdLengthPlusGirth, quantity, requestedParcelPackagings, rowNumber, scheduleB, secondDimension, stc, totalItems, totalLaborCharge, totalPackedValue, totalPcs, totalWeight, transportationHeight, transportationLength, transportationWeight, transportationWidth, userId |
| JobSearchResult | 21 undeclared field(s): completedDate, createdByUserName, delAddress1, delZipCode, destAddress, estimateDate1, expectedDeliveryDate, expectedPickUpDate, itemName, jobItemsTotalMaterialsLbs, jobMgmtId, jobMgmtStatusName, jobTotalQty, jobTotalValue, jobTotalWeight, orginAddress, psDoneBy, puAddress2, puZipcode, quoteDate1, totalItems |
| SearchContactEntityResult | 30 undeclared field(s): addressesList, assistant, birthDate, bolNotes, careOf, company, companyId, contactTypeId, department, editable, emailsList, fax, fullNameUpdateRequired, isActive, isBusiness, isEmpty, isPayer, isPrefered, isPrimary, isPrivate, jobTitle, jobTitleId, legacyGuid, ownerFranchiseeId, phonesList, primaryEmail, primaryPhone, rootContactId, taxId, webSite |
