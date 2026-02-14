# API Surface Reference

Single source of truth for all ABConnect API endpoints. Built from
ABConnectTools `routes.py` (validated against real API) and our swagger
specs. Updated incrementally as groups are implemented.

**Last updated**: 2026-02-14
**Source**: `/usr/src/pkgs/ABConnectTools/ABConnect/api/routes.py` (399 lines, 30 groups)

## API Surfaces

### ACPortal

- **Base URL**: `https://portal.{env}.abconnect.co/api/api`
- **Auth**: Bearer JWT via `/connect/token` (OAuth2 password grant)
- **Swagger**: `ab/api/schemas/acportal.json` (unreliable — treat as hint)
- **Environments**: `staging`, production (no prefix)

### Catalog

- **Base URL**: `https://catalog-api.{env}.abconnect.co/api`
- **Auth**: Same JWT
- **Swagger**: `ab/api/schemas/catalog.json` (reliable)

### ABC

- **Base URL**: `https://api.{env}.abconnect.co/api`
- **Auth**: Same JWT
- **Swagger**: `ab/api/schemas/abc.json` (mostly reliable)

## Coverage Summary

| API | Total Groups | Implemented | Remaining |
|-----|-------------|-------------|-----------|
| ACPortal | 30 | 8 (partial) | 22 fully missing + partial gaps |
| Catalog | 3 | 3 | 0 (100%) |
| ABC | 2 | 2 | 0 (58% of endpoints) |

## Endpoint Groups — ACPortal

Legend: Done = implemented in AB, Total = routes in ABConnectTools, Ref = ABConnectTools has fixtures

### Account

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | DELETE_PAYMENTSOURCE | DELETE | /account/paymentsource/{sourceId} | ServiceBaseResponse | — | — |
| 2 | GET_PROFILE | GET | /account/profile | AccountProfile | — | JSON |
| 3 | GET_VERIFYRESETTOKEN | GET | /account/verifyresettoken | ServiceBaseResponse | — | — |
| 4 | POST_CONFIRM | POST | /account/confirm | ServiceBaseResponse | — | — |
| 5 | POST_FORGOT | POST | /account/forgot | ServiceBaseResponse | — | — |
| 6 | POST_REGISTER | POST | /account/register | ServiceBaseResponse | — | — |
| 7 | POST_RESETPASSWORD | POST | /account/resetpassword | ServiceBaseResponse | — | — |
| 8 | POST_SEND_CONFIRMATION | POST | /account/sendConfirmation | ServiceBaseResponse | — | — |
| 9 | POST_SETPASSWORD | POST | /account/setpassword | ServiceBaseResponse | — | — |
| 10 | PUT_PAYMENTSOURCE | PUT | /account/paymentsource/{sourceId} | ServiceBaseResponse | — | — |

**Total**: 10 | **AB done**: 0 | **ABConnectTools fixtures**: AccountProfile.json
**AB file**: — | **ABConnectTools file**: `endpoints/account.py`, `models/account.py`
**Priority**: Low (auth/account management)

---

### Address

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET_ISVALID | GET | /address/isvalid | AddressIsValidResult | pending | — |
| 2 | GET_PROPERTYTYPE | GET | /address/propertytype | PropertyType | pending | — |
| 3 | POST_AVOID_VALIDATION | POST | /address/{addressId}/avoidValidation | ServiceBaseResponse | — | — |
| 4 | POST_VALIDATED | POST | /address/{addressId}/validated | ServiceBaseResponse | — | — |

**Total**: 4 | **AB done**: 2 (pending fixtures) | **ABConnectTools fixtures**: —
**AB file**: `endpoints/address.py` | **ABConnectTools file**: `endpoints/address.py`, `models/address.py`

---

### Admin

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | DELETE_ADVANCEDSETTINGS | DELETE | /admin/advancedsettings/{id} | ServiceBaseResponse | — | — |
| 2 | GET_ADVANCEDSETTINGS | GET | /admin/advancedsettings/{id} | AdvancedSettingsEntitySaveModel | — | — |
| 3 | GET_ADVANCEDSETTINGS_ALL | GET | /admin/advancedsettings/all | List[AdvancedSettingsEntitySaveModel] | — | — |
| 4 | GET_CARRIERERRORMESSAGE_ALL | GET | /admin/carriererrormessage/all | List[CarrierErrorMessage] | — | — |
| 5 | GET_GLOBALSETTINGS_COMPANYHIERARCHY | GET | /admin/globalsettings/companyhierarchy | CompanyHierarchyInfo | — | — |
| 6 | GET_GLOBALSETTINGS_COMPANYHIERARCHY_COMPANY | GET | /admin/globalsettings/companyhierarchy/company/{companyId} | CompanyHierarchyInfo | — | — |
| 7 | POST_ADVANCEDSETTINGS | POST | /admin/advancedsettings | ServiceBaseResponse | — | — |
| 8 | POST_CARRIERERRORMESSAGE | POST | /admin/carriererrormessage | ServiceBaseResponse | — | — |
| 9 | POST_GLOBALSETTINGS_APPROVEINSURANCEEXCEPTION | POST | /admin/globalsettings/approveinsuranceexception | ServiceBaseResponse | — | — |
| 10 | POST_GLOBALSETTINGS_GETINSURANCEEXCEPTIONS | POST | /admin/globalsettings/getinsuranceexceptions | List[SelectApproveInsuranceResult] | — | — |
| 11 | POST_GLOBALSETTINGS_INTACCT | POST | /admin/globalsettings/intacct | ServiceBaseResponse | — | — |
| 12 | POST_LOGBUFFER_FLUSH | POST | /admin/logbuffer/flush | ServiceBaseResponse | — | — |
| 13 | POST_LOGBUFFER_FLUSH_ALL | POST | /admin/logbuffer/flushAll | ServiceBaseResponse | — | — |

**Total**: 13 | **AB done**: 0 | **ABConnectTools fixtures**: —
**AB file**: — | **ABConnectTools file**: `endpoints/admin.py`, `models/advancedsettings.py`, `models/globalsettings.py`
**Priority**: Low (internal admin)

---

### Commodity

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET | GET | /commodity/{id} | CommodityWithParentsServiceResponse | — | — |
| 2 | POST | POST | /commodity | CommodityServiceResponse | — | — |
| 3 | POST_SEARCH | POST | /commodity/search | List[CommodityDetails] | — | — |
| 4 | POST_SUGGESTIONS | POST | /commodity/suggestions | List[CommodityWithParents] | — | — |
| 5 | PUT | PUT | /commodity/{id} | CommodityServiceResponse | — | — |

**Total**: 5 | **AB done**: 0 | **ABConnectTools fixtures**: —
**AB file**: — | **ABConnectTools file**: `endpoints/commodity.py`, `models/commodity.py`

---

### CommodityMap

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | DELETE | DELETE | /commodity-map/{id} | ServiceBaseResponse | — | — |
| 2 | GET | GET | /commodity-map/{id} | CommodityMapDetailsServiceResponse | — | — |
| 3 | POST | POST | /commodity-map | CommodityMapServiceResponse | — | — |
| 4 | POST_SEARCH | POST | /commodity-map/search | List[CommodityMapDetails] | — | — |
| 5 | PUT | PUT | /commodity-map/{id} | CommodityMapServiceResponse | — | — |

**Total**: 5 | **AB done**: 0 | **ABConnectTools fixtures**: —
**AB file**: — | **ABConnectTools file**: `endpoints/commoditymap.py`, `models/commodity.py`

---

### Companies

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET | GET | /companies/{id} | CompanySimple | done | JSON |
| 2 | GET_AVAILABLE_BY_CURRENT_USER | GET | /companies/availableByCurrentUser | List[CompanySimple] | done | JSON |
| 3 | GET_BRANDS | GET | /companies/brands | List[CompanyBrandTreeNode] | — | JSON |
| 4 | GET_BRANDSTREE | GET | /companies/brandstree | List[CompanyBrandTreeNode] | — | JSON |
| 5 | GET_CAPABILITIES | GET | /companies/{companyId}/capabilities | CommercialCapabilities | — | — |
| 6 | GET_CARRIER_ACOUNTS | GET | /companies/{companyId}/carrierAcounts | FranchiseeCarrierAccounts | — | — |
| 7 | GET_DETAILS | GET | /companies/{companyId}/details | Company | done | — |
| 8 | GET_FRANCHISEE_ADDRESSES | GET | /companies/{companyId}/franchiseeAddresses | List[CompanyAddressInfo] | — | — |
| 9 | GET_FULLDETAILS | GET | /companies/{companyId}/fulldetails | CompanyDetails | done | — |
| 10 | GET_GEOSETTINGS | GET | /companies/geosettings | List[SaveGeoSettingModel] | — | — |
| 11 | GET_GEO_AREA_COMPANIES | GET | /companies/geoAreaCompanies | List[CompanyGeoAreaCompanies] | — | JSON |
| 12 | GET_INFO_FROM_KEY | GET | /companies/infoFromKey | CompanyInfo | — | — |
| 13 | GET_INHERITEDPACKAGINGLABOR | GET | /companies/{companyId}/inheritedpackaginglabor | PackagingLaborSettings | — | — |
| 14 | GET_INHERITED_PACKAGING_TARIFFS | GET | /companies/{companyId}/inheritedPackagingTariffs | PackagingTariffSettings | — | — |
| 15 | GET_PACKAGINGLABOR | GET | /companies/{companyId}/packaginglabor | PackagingLaborSettings | — | — |
| 16 | GET_PACKAGINGSETTINGS | GET | /companies/{companyId}/packagingsettings | PackagingTariffSettings | — | — |
| 17 | GET_SEARCH | GET | /companies/search | List[SearchCompanyResponse] | done | JSON |
| 18 | GET_SEARCH_CARRIER_ACCOUNTS | GET | /companies/search/carrier-accounts | List[CarrierAccountInfo] | — | — |
| 19 | GET_SUGGEST_CARRIERS | GET | /companies/suggest-carriers | List[CarrierCompanyInfo] | — | — |
| 20 | POST_CAPABILITIES | POST | /companies/{companyId}/capabilities | ServiceBaseResponse | — | — |
| 21 | POST_CARRIER_ACOUNTS | POST | /companies/{companyId}/carrierAcounts | ServiceBaseResponse | — | — |
| 22 | POST_FILTERED_CUSTOMERS | POST | /companies/filteredCustomers | ServiceBaseResponse | — | — |
| 23 | POST_FULLDETAILS | POST | /companies/fulldetails | ServiceBaseResponse | — | — |
| 24 | POST_GEOSETTINGS | POST | /companies/{companyId}/geosettings | ServiceBaseResponse | — | — |
| 25 | POST_LIST | POST | /companies/list | ServiceBaseResponse | — | — |
| 26 | POST_PACKAGINGLABOR | POST | /companies/{companyId}/packaginglabor | ServiceBaseResponse | — | — |
| 27 | POST_PACKAGINGSETTINGS | POST | /companies/{companyId}/packagingsettings | ServiceBaseResponse | — | — |
| 28 | POST_SEARCH_V2 | POST | /companies/search/v2 | List[SearchCompanyResponse] | — | — |
| 29 | POST_SIMPLELIST | POST | /companies/simplelist | ServiceBaseResponse | — | — |
| 30 | PUT_FULLDETAILS | PUT | /companies/{companyId}/fulldetails | CompanyDetails | — | — |

**Total**: 30 | **AB done**: 5 | **ABConnectTools fixtures**: CompanySimple, CompanyAvailableByCurrentUser, CompanyBrands, CompanyBrandsTree, CompanyGeoAreaCompanies, CompanySearch_Training
**AB file**: `endpoints/companies.py` | **ABConnectTools file**: `endpoints/companies.py`, `models/companies.py`

---

### Company (single-entity settings)

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | DELETE_ACCOUNTS_STRIPE | DELETE | /company/{companyId}/accounts/stripe | ServiceBaseResponse | — | — |
| 2 | DELETE_CONTAINERTHICKNESSINCHES | DELETE | /company/{companyId}/containerthicknessinches | ServiceBaseResponse | — | — |
| 3 | DELETE_MATERIAL | DELETE | /company/{companyId}/material/{materialId} | ServiceBaseResponse | — | — |
| 4 | DELETE_TRUCK | DELETE | /company/{companyId}/truck/{truckId} | ServiceWarningResponse | — | — |
| 5 | GET_ACCOUNTS_STRIPE_CONNECTURL | GET | /company/{companyId}/accounts/stripe/connecturl | — | — | — |
| 6 | GET_CALENDAR | GET | /company/{companyId}/calendar/{date} | Calendar | — | — |
| 7 | GET_CALENDAR_BASEINFO | GET | /company/{companyId}/calendar/{date}/baseinfo | BaseInfoCalendar | — | — |
| 8 | GET_CALENDAR_ENDOFDAY | GET | /company/{companyId}/calendar/{date}/endofday | — | — | — |
| 9 | GET_CALENDAR_STARTOFDAY | GET | /company/{companyId}/calendar/{date}/startofday | — | — | — |
| 10 | GET_CONTAINERTHICKNESSINCHES | GET | /company/{companyId}/containerthicknessinches | List[ContainerThickness] | — | — |
| 11 | GET_GRIDSETTINGS | GET | /company/{companyId}/gridsettings | GridSettingsEntity | — | — |
| 12 | GET_MATERIAL | GET | /company/{companyId}/material | List[CompanyMaterial] | — | — |
| 13 | GET_PLANNER | GET | /company/{companyId}/planner | List[PlannerTask] | — | — |
| 14 | GET_SETUPDATA | GET | /company/{companyId}/setupdata | CompanySetupData | — | — |
| 15 | GET_TRUCK | GET | /company/{companyId}/truck | List[Truck] | — | — |
| 16 | POST_ACCOUNTS_STRIPE_COMPLETECONNECTION | POST | /company/{companyId}/accounts/stripe/completeconnection | ServiceBaseResponse | — | — |
| 17 | POST_CONTAINERTHICKNESSINCHES | POST | /company/{companyId}/containerthicknessinches | ServiceBaseResponse | — | — |
| 18 | POST_GRIDSETTINGS | POST | /company/{companyId}/gridsettings | ServiceBaseResponse | — | — |
| 19 | POST_MATERIAL | POST | /company/{companyId}/material | CompanyMaterial | — | — |
| 20 | POST_TRUCK | POST | /company/{companyId}/truck | SaveEntityResponse | — | — |
| 21 | PUT_MATERIAL | PUT | /company/{companyId}/material/{materialId} | CompanyMaterial | — | — |
| 22 | PUT_TRUCK | PUT | /company/{companyId}/truck/{truckId} | SaveEntityResponse | — | — |

**Total**: 22 | **AB done**: 0 | **ABConnectTools fixtures**: —
**AB file**: — | **ABConnectTools file**: `endpoints/company.py`, `models/calendar.py`, `models/companysettings.py`, `models/truck.py`
**Priority**: Medium (company settings & calendar)

---

### Contacts

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET | GET | /contacts/{id} | ContactDetails | — | JSON |
| 2 | GET_EDITDETAILS | GET | /contacts/{contactId}/editdetails | ContactDetailedInfo | done | — |
| 3 | HISTORY_AGGREGATED | GET | /contacts/{contactId}/history/aggregated | ContactHistoryAggregatedCost | — | — |
| 4 | HISTORY_GRAPHDATA | GET | /contacts/{contactId}/history/graphdata | ContactHistoryGraphData | — | — |
| 5 | PRIMARYDETAILS | GET | /contacts/{contactId}/primarydetails | ContactPrimaryDetails | done | — |
| 6 | USER | GET | /contacts/user | ContactUser | done | JSON |
| 7 | CUSTOMERS | POST | /contacts/customers | ServiceBaseResponse | — | — |
| 8 | POST_EDITDETAILS | POST | /contacts/editdetails | ServiceBaseResponse | — | — |
| 9 | HISTORY | POST | /contacts/{contactId}/history | ContactHistoryInfo | — | — |
| 10 | MERGE_PREVIEW | POST | /contacts/{mergeToId}/merge/preview | MergeContactsPreviewInfo | — | — |
| 11 | SEARCH | POST | /contacts/search | ServiceBaseResponse | — | — |
| 12 | V2_SEARCH | POST | /contacts/v2/search | List[SearchContactEntityResult] | done | — |
| 13 | PUT_EDITDETAILS | PUT | /contacts/{contactId}/editdetails | ServiceBaseResponse | — | — |
| 14 | MERGE | PUT | /contacts/{mergeToId}/merge | ServiceBaseResponse | — | — |

**Total**: 14 | **AB done**: 4 | **ABConnectTools fixtures**: ContactDetails, ContactUser
**AB file**: `endpoints/contacts.py` | **ABConnectTools file**: `endpoints/contacts.py`, `models/contacts.py`, `models/contacthistory.py`, `models/contactmerge.py`

---

### Dashboard

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET | GET | /dashboard | DashboardResponse | — | JSON |
| 2 | GRIDVIEWS | GET | /dashboard/gridviews | List[GridViewDetails] | — | JSON |
| 3 | GRIDVIEWSTATE | GET | /dashboard/gridviewstate/{id} | GridViewDetails | — | — |
| 4 | POST_GRIDVIEWSTATE | POST | /dashboard/gridviewstate/{id} | ServiceBaseResponse | — | — |
| 5 | INBOUND | POST | /dashboard/inbound | List[AgentInboundViewRecord] | — | — |
| 6 | INHOUSE | POST | /dashboard/inhouse | List[AgentInhouseViewRecord] | — | — |
| 7 | LOCAL_DELIVERIES | POST | /dashboard/local-deliveries | List[AgentLocalDeliveriesViewRecord] | — | — |
| 8 | OUTBOUND | POST | /dashboard/outbound | List[AgentOutboundViewRecord] | — | — |
| 9 | RECENTESTIMATES | POST | /dashboard/recentestimates | List[AgentRecentEstimatesViewRecord] | — | — |

**Total**: 9 | **AB done**: 0 | **ABConnectTools fixtures**: Dashboard, DashboardData, DashboardGridViews
**AB file**: — | **ABConnectTools file**: `endpoints/dashboard.py`, `models/dashboard.py`
**Priority**: Medium (agent dashboard views)

---

### Documents

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET | GET | /documents/get/{docPath} | DocumentDetails | — | — |
| 2 | THUMBNAIL | GET | /documents/get/thumbnail/{docPath} | — | — | — |
| 3 | LIST | GET | /documents/list | List[DocumentDetails] | done | — |
| 4 | POST | POST | /documents | ServiceBaseResponse | — | — |
| 5 | HIDE | PUT | /documents/hide/{docId} | ServiceBaseResponse | — | — |
| 6 | UPDATE | PUT | /documents/update/{docId} | ServiceBaseResponse | — | — |

**Total**: 6 | **AB done**: 1 | **ABConnectTools fixtures**: —
**AB file**: `endpoints/documents.py` | **ABConnectTools file**: `endpoints/documents.py`, `models/documents.py`

---

### E-Sign

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET | GET | /e-sign/{jobDisplayId}/{bookingKey} | — | — | — |
| 2 | GET_RESULT | GET | /e-sign/result | — | — | — |

**Total**: 2 | **AB done**: 0 | **ABConnectTools fixtures**: —
**Priority**: Low

---

### Email

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | LABELREQUEST | POST | /email/{jobDisplayId}/labelrequest | ServiceBaseResponse | — | — |

**Total**: 1 | **AB done**: 0

---

### Job (core + all sub-domains)

The JOB group contains 99 routes. Organized by sub-domain:

#### Job — Core (CRUD, search, save)

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET | GET | /job/{jobDisplayId} | CalendarJob | done | — |
| 2 | GET_CALENDARITEMS | GET | /job/{jobDisplayId}/calendaritems | List[CalendarItem] | done | — |
| 3 | GET_DOCUMENT_CONFIG | GET | /job/documentConfig | — | — | — |
| 4 | GET_FEEDBACK | GET | /job/feedback/{jobDisplayId} | FeedbackSaveModel | — | — |
| 5 | GET_JOB_ACCESS_LEVEL | GET | /job/jobAccessLevel | JobAccessLevel | — | — |
| 6 | GET_PRICE | GET | /job/{jobDisplayId}/price | — | done | — |
| 7 | GET_SEARCH | GET | /job/search | List[SearchJobInfo] | done | — |
| 8 | GET_SUBMANAGEMENTSTATUS | GET | /job/{jobDisplayId}/submanagementstatus | — | — | — |
| 9 | GET_UPDATE_PAGE_CONFIG | GET | /job/{jobDisplayId}/updatePageConfig | JobUpdatePageConfig | done | — |
| 10 | POST | POST | /job | ServiceBaseResponse | — | — |
| 11 | POST_BOOK | POST | /job/{jobDisplayId}/book | ServiceBaseResponse | — | — |
| 12 | POST_CHANGE_AGENT | POST | /job/{jobDisplayId}/changeAgent | ServiceBaseResponse | — | JSON |
| 13 | POST_FEEDBACK | POST | /job/feedback/{jobDisplayId} | ServiceBaseResponse | — | — |
| 14 | POST_SEARCH_BY_DETAILS | POST | /job/searchByDetails | ServiceBaseResponse | — | — |
| 15 | POST_TRANSFER | POST | /job/transfer/{jobDisplayId} | ServiceBaseResponse | — | — |
| 16 | PUT_SAVE | PUT | /job/save | ServiceBaseResponse | — | — |

**AB done**: 5 of 16

#### Job — Timeline

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET_TIMELINE_LIST | GET | /job/{id}/timeline | TimelineResponse | done | — |
| 2 | GET_TIMELINE | GET | /job/{id}/timeline/{taskId} | CarrierTask | done | — |
| 3 | GET_TIMELINE_AGENT | GET | /job/{id}/timeline/{taskCode}/agent | CompanyListItem | done | — |
| 4 | POST_TIMELINE | POST | /job/{id}/timeline | SaveResponseModel | done | — |
| 5 | PATCH_TIMELINE | PATCH | /job/{id}/timeline/{taskId} | ServiceBaseResponse | done | — |
| 6 | DELETE_TIMELINE | DELETE | /job/{id}/timeline/{taskId} | DeleteTaskResponse | done | — |
| 7 | POST_TIMELINE_INCREMENTJOBSTATUS | POST | /job/{id}/timeline/incrementjobstatus | IncrementJobStatusResponseModel | done | — |
| 8 | POST_TIMELINE_UNDOINCREMENTJOBSTATUS | POST | /job/{id}/timeline/undoincrementjobstatus | ServiceBaseResponse | done | — |
| 9 | POST_STATUS_QUOTE | POST | /job/{id}/status/quote | ServiceBaseResponse | done | — |

**AB done**: 9 of 9 (feature 002)

#### Job — Shipments

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET_SHIPMENT_RATEQUOTES | GET | /job/{id}/shipment/ratequotes | JobCarrierRatesModel | done | — |
| 2 | POST_SHIPMENT_RATEQUOTES | POST | /job/{id}/shipment/ratequotes | JobCarrierRatesModel | done | — |
| 3 | POST_SHIPMENT_BOOK | POST | /job/{id}/shipment/book | ServiceBaseResponse | done | — |
| 4 | DELETE_SHIPMENT | DELETE | /job/{id}/shipment | ServiceBaseResponse | done | — |
| 5 | GET_SHIPMENT_ACCESSORIALS | GET | /job/{id}/shipment/accessorials | List[JobParcelAddOn] | done | — |
| 6 | POST_SHIPMENT_ACCESSORIAL | POST | /job/{id}/shipment/accessorial | ServiceBaseResponse | done | — |
| 7 | DELETE_SHIPMENT_ACCESSORIAL | DELETE | /job/{id}/shipment/accessorial/{addOnId} | ServiceBaseResponse | done | — |
| 8 | GET_SHIPMENT_ORIGINDESTINATION | GET | /job/{id}/shipment/origindestination | ShipmentOriginDestination | done | — |
| 9 | GET_SHIPMENT_EXPORTDATA | GET | /job/{id}/shipment/exportdata | JobExportData | done | — |
| 10 | POST_SHIPMENT_EXPORTDATA | POST | /job/{id}/shipment/exportdata | ServiceBaseResponse | done | — |
| 11 | GET_SHIPMENT_RATESSTATE | GET | /job/{id}/shipment/ratesstate | — | done | — |

**AB done**: 11 of 11 (feature 002)

#### Job — Tracking

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET_TRACKING | GET | /job/{id}/tracking | ShipmentTrackingDetails | done | — |
| 2 | GET_TRACKING_SHIPMENT | GET | /job/{id}/tracking/shipment/{proNumber} | ShipmentTrackingDetails | — | — |

**AB done**: 1 of 2 (feature 002; shipment-specific tracking not yet)

#### Job — Payments

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET_PAYMENT | GET | /job/{id}/payment | — | done | — |
| 2 | GET_PAYMENT_CREATE | GET | /job/{id}/payment/create | — | — | — |
| 3 | GET_PAYMENT_SOURCES | GET | /job/{id}/payment/sources | List[PaymentSourceDetails] | done | — |
| 4 | POST_PAYMENT_BYSOURCE | POST | /job/{id}/payment/bysource | ServiceBaseResponse | done | — |
| 5 | POST_PAYMENT_ACHPAYMENT_SESSION | POST | /job/{id}/payment/ACHPaymentSession | ServiceBaseResponse | done | — |
| 6 | POST_PAYMENT_ACHCREDIT_TRANSFER | POST | /job/{id}/payment/ACHCreditTransfer | ServiceBaseResponse | done | — |
| 7 | POST_PAYMENT_ATTACH_CUSTOMER_BANK | POST | /job/{id}/payment/attachCustomerBank | ServiceBaseResponse | done | — |
| 8 | POST_PAYMENT_VERIFY_JOB_ACHSOURCE | POST | /job/{id}/payment/verifyJobACHSource | ServiceBaseResponse | done | — |
| 9 | POST_PAYMENT_CANCEL_JOB_ACHVERIFICATION | POST | /job/{id}/payment/cancelJobACHVerification | ServiceBaseResponse | done | — |
| 10 | POST_PAYMENT_BANKSOURCE | POST | /job/{id}/payment/banksource | ServiceBaseResponse | done | — |

**AB done**: 9 of 10 (feature 002; payment/create not yet)

#### Job — Forms

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET_FORM_ADDRESS_LABEL | GET | /job/{id}/form/address-label | bytes | done | PDF |
| 2 | GET_FORM_BILL_OF_LADING | GET | /job/{id}/form/bill-of-lading | bytes | done | PDF |
| 3 | GET_FORM_CREDIT_CARD_AUTHORIZATION | GET | /job/{id}/form/credit-card-authorization | bytes | done | PDF |
| 4 | GET_FORM_CUSTOMER_QUOTE | GET | /job/{id}/form/customer-quote | bytes | done | PDF |
| 5 | GET_FORM_INVOICE | GET | /job/{id}/form/invoice | bytes | done | PDF |
| 6 | GET_FORM_INVOICE_EDITABLE | GET | /job/{id}/form/invoice/editable | USAREditableFormResponseModel | — | — |
| 7 | GET_FORM_ITEM_LABELS | GET | /job/{id}/form/item-labels | bytes | done | PDF |
| 8 | GET_FORM_OPERATIONS | GET | /job/{id}/form/operations | bytes | done | PDF |
| 9 | GET_FORM_PACKAGING_LABELS | GET | /job/{id}/form/packaging-labels | bytes | done | — |
| 10 | GET_FORM_PACKAGING_SPECIFICATION | GET | /job/{id}/form/packaging-specification | bytes | done | PDF |
| 11 | GET_FORM_PACKING_SLIP | GET | /job/{id}/form/packing-slip | bytes | done | PDF |
| 12 | GET_FORM_QUICK_SALE | GET | /job/{id}/form/quick-sale | bytes | done | PDF |
| 13 | GET_FORM_SHIPMENTS | GET | /job/{id}/form/shipments | List[FormsShipmentPlan] | done | — |
| 14 | GET_FORM_USAR | GET | /job/{id}/form/usar | bytes | done | PDF |
| 15 | GET_FORM_USAR_EDITABLE | GET | /job/{id}/form/usar/editable | USAREditableFormResponseModel | — | — |

**AB done**: 13 of 15 (feature 002; 2 editable JSON forms not yet)

#### Job — Notes

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET_NOTE_LIST | GET | /job/{id}/note | List[JobTaskNote] | done | — |
| 2 | GET_NOTE | GET | /job/{id}/note/{id} | JobTaskNote | done | — |
| 3 | POST_NOTE | POST | /job/{id}/note | JobTaskNote | done | — |
| 4 | PUT_NOTE | PUT | /job/{id}/note/{id} | ServiceBaseResponse | done | — |

**AB done**: 4 of 4 (feature 002)

#### Job — Parcels & Items

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET_PARCELITEMS | GET | /job/{id}/parcelitems | List[ParcelItemWithPackage] | done | — |
| 2 | POST_PARCELITEMS | POST | /job/{id}/parcelitems | List[ParcelItemWithPackage] | done | — |
| 3 | DELETE_PARCELITEMS | DELETE | /job/{id}/parcelitems/{parcelItemId} | ServiceBaseResponse | done | — |
| 4 | GET_PARCEL_ITEMS_WITH_MATERIALS | GET | /job/{id}/parcel-items-with-materials | List[ParcelItemWithMaterials] | done | — |
| 5 | GET_PACKAGINGCONTAINERS | GET | /job/{id}/packagingcontainers | List[Packaging] | done | — |
| 6 | PUT_ITEM | PUT | /job/{id}/item/{itemId} | ServiceBaseResponse | done | — |
| 7 | POST_ITEM_NOTES | POST | /job/{id}/item/notes | ServiceBaseResponse | done | — |
| 8 | POST_FREIGHTITEMS | POST | /job/{id}/freightitems | ServiceBaseResponse | — | — |

**AB done**: 7 of 8 (feature 002; freightitems not yet)

#### Job — On Hold

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET_ONHOLD_LIST | GET | /job/{id}/onhold | List[OnHoldDetails] | — | — |
| 2 | GET_ONHOLD | GET | /job/{id}/onhold/{id} | OnHoldDetails | — | — |
| 3 | GET_ONHOLD_FOLLOWUPUSERS | GET | /job/{id}/onhold/followupusers | List[OnHoldUser] | — | — |
| 4 | GET_ONHOLD_FOLLOWUPUSER | GET | /job/{id}/onhold/followupuser/{contactId} | OnHoldUser | — | — |
| 5 | POST_ONHOLD | POST | /job/{id}/onhold | SaveOnHoldResponse | — | — |
| 6 | POST_ONHOLD_COMMENT | POST | /job/{id}/onhold/{onHoldId}/comment | OnHoldNoteDetails | — | — |
| 7 | PUT_ONHOLD | PUT | /job/{id}/onhold/{onHoldId} | SaveOnHoldResponse | — | — |
| 8 | PUT_ONHOLD_DATES | PUT | /job/{id}/onhold/{onHoldId}/dates | ResolveJobOnHoldResponse | — | — |
| 9 | PUT_ONHOLD_RESOLVE | PUT | /job/{id}/onhold/{onHoldId}/resolve | ResolveJobOnHoldResponse | — | — |
| 10 | DELETE_ONHOLD | DELETE | /job/{id}/onhold | ServiceBaseResponse | — | — |

**AB done**: 0 of 10
**ABConnectTools file**: `endpoints/jobs/onhold.py`, `models/jobonhold.py`

#### Job — RFQ

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET_RFQ | GET | /job/{id}/rfq | List[QuoteRequestDisplayInfo] | — | — |
| 2 | GET_RFQ_STATUSOF_FORCOMPANY | GET | /job/{id}/rfq/statusof/{type}/forcompany/{companyId} | QuoteRequestStatus | — | — |

**AB done**: 0 of 2

#### Job — SMS

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET_SMS | GET | /job/{id}/sms | — | — | — |
| 2 | GET_SMS_TEMPLATEBASED | GET | /job/{id}/sms/templatebased/{templateId} | SmsTemplateModel | — | — |
| 3 | POST_SMS | POST | /job/{id}/sms | ServiceBaseResponse | — | — |
| 4 | POST_SMS_READ | POST | /job/{id}/sms/read | ServiceBaseResponse | — | — |

**AB done**: 0 of 4

#### Job — Email

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | POST_EMAIL | POST | /job/{id}/email | ServiceBaseResponse | — | — |
| 2 | POST_EMAIL_CREATETRANSACTIONALEMAIL | POST | /job/{id}/email/createtransactionalemail | ServiceBaseResponse | — | — |
| 3 | POST_EMAIL_SEND | POST | /job/{id}/email/{emailTemplateGuid}/send | ServiceBaseResponse | — | — |
| 4 | POST_EMAIL_SENDDOCUMENT | POST | /job/{id}/email/senddocument | ServiceBaseResponse | — | — |

**AB done**: 0 of 4

#### Job — Freight Providers

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET_FREIGHTPROVIDERS | GET | /job/{id}/freightproviders | List[PricedFreightProvider] | — | — |
| 2 | POST_FREIGHTPROVIDERS | POST | /job/{id}/freightproviders | ServiceBaseResponse | — | — |
| 3 | POST_FREIGHTPROVIDERS_RATEQUOTE | POST | /job/{id}/freightproviders/{optionIndex}/ratequote | ServiceBaseResponse | — | — |

**AB done**: 0 of 3

---

### JobIntAcct

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | DELETE | DELETE | /jobintacct/{jobDisplayId}/{franchiseeId} | ServiceBaseResponse | — | — |
| 2 | GET | GET | /jobintacct/{jobDisplayId} | CreateJobIntacctModel | — | — |
| 3 | POST | POST | /jobintacct/{jobDisplayId} | ServiceBaseResponse | — | — |
| 4 | APPLY_REBATE | POST | /jobintacct/{jobDisplayId}/applyRebate | ServiceBaseResponse | — | — |
| 5 | DRAFT | POST | /jobintacct/{jobDisplayId}/draft | ServiceBaseResponse | — | — |

**Total**: 5 | **AB done**: 0
**ABConnectTools file**: `endpoints/jobintacct.py`, `models/jobintacct.py`

---

### Lookup

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET | GET | /lookup/{masterConstantKey}/{valueId} | LookupValue | — | — |
| 2 | ACCESS_KEY | GET | /lookup/accessKey/{accessKey} | LookupAccessKey | — | JSON |
| 3 | ACCESS_KEYS | GET | /lookup/accessKeys | List[LookupAccessKey] | — | JSON |
| 4 | COMON_INSURANCE | GET | /lookup/comonInsurance | — | — | — |
| 5 | CONTACT_TYPES | GET | /lookup/contactTypes | List[ContactTypeEntity] | done | JSON |
| 6 | COUNTRIES | GET | /lookup/countries | List[CountryCodeDto] | done | JSON |
| 7 | DENSITY_CLASS_MAP | GET | /lookup/densityClassMap | List[GuidSequentialRangeValue] | — | JSON |
| 8 | DOCUMENT_TYPES | GET | /lookup/documentTypes | List[LookupDocumentType] | — | JSON |
| 9 | ITEMS | GET | /lookup/items | — | pending | — |
| 10 | PARCEL_PACKAGE_TYPES | GET | /lookup/parcelPackageTypes | List[LookupValue] | — | JSON |
| 11 | PPCCAMPAIGNS | GET | /lookup/PPCCampaigns | — | — | — |
| 12 | REFER_CATEGORY | GET | /lookup/referCategory | — | — | — |
| 13 | REFER_CATEGORY_HEIRACHY | GET | /lookup/referCategoryHeirachy | — | — | — |
| 14 | RESET_MASTER_CONSTANT_CACHE | GET | /lookup/resetMasterConstantCache | — | — | — |

**Total**: 14 | **AB done**: 3 | **ABConnectTools fixtures**: LookupAccessKeys, LookupContactTypes, LookupCountries, LookupDensityClassMap, LookupDocumentTypes, LookupParcelPackageTypes
**AB file**: `endpoints/lookup.py` | **ABConnectTools file**: `endpoints/lookup.py`, `models/lookup.py`

---

### Note (top-level, separate from job notes)

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET | GET | /note | List[Notes] | — | — |
| 2 | GET_SUGGEST_USERS | GET | /note/suggestUsers | List[SuggestedContactEntity] | — | — |
| 3 | POST | POST | /note | Notes | — | — |
| 4 | PUT | PUT | /note/{id} | ServiceBaseResponse | — | — |

**Total**: 4 | **AB done**: 0
**ABConnectTools file**: `endpoints/note.py`, `models/note.py`

---

### Notifications

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET | GET | /notifications | NotificationsResponse | — | JSON |

**Total**: 1 | **AB done**: 0 | **ABConnectTools fixtures**: Notifications.json

---

### Partner

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET | GET | /partner | List[Partner] | — | JSON |
| 2 | POST_SEARCH | POST | /partner/search | List[Partner] | — | — |

**Total**: 2 | **AB done**: 0 | **ABConnectTools fixtures**: PartnerList.json

---

### Reports

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | INSURANCE | POST | /reports/insurance | InsuranceReport | — | — |
| 2 | REFERRED_BY | POST | /reports/referredBy | ReferredByReport | — | — |
| 3 | SALES | POST | /reports/sales | SalesForecastReport | — | — |
| 4 | SALES_DRILLDOWN | POST | /reports/salesDrilldown | ServiceBaseResponse | — | — |
| 5 | SALES_SUMMARY | POST | /reports/sales/summary | SalesForecastSummary | — | — |
| 6 | TOP_REVENUE_CUSTOMERS | POST | /reports/topRevenueCustomers | RevenueCustomer | — | — |
| 7 | TOP_REVENUE_SALES_REPS | POST | /reports/topRevenueSalesReps | RevenueCustomer | — | — |
| 8 | WEB2LEAD | POST | /reports/web2Lead | Web2LeadReport | — | — |

**Total**: 8 | **AB done**: 0
**ABConnectTools file**: `endpoints/reports.py`, `models/reports.py`

---

### RFQ (top-level)

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET | GET | /rfq/{rfqId} | QuoteRequestDisplayInfo | — | — |
| 2 | FORJOB | GET | /rfq/forjob/{jobId} | List[QuoteRequestDisplayInfo] | — | — |
| 3 | ACCEPT | POST | /rfq/{rfqId}/accept | ServiceBaseResponse | — | — |
| 4 | ACCEPTWINNER | POST | /rfq/{rfqId}/acceptwinner | ServiceBaseResponse | — | — |
| 5 | CANCEL | POST | /rfq/{rfqId}/cancel | ServiceBaseResponse | — | — |
| 6 | COMMENT | POST | /rfq/{rfqId}/comment | ServiceBaseResponse | — | — |
| 7 | DECLINE | POST | /rfq/{rfqId}/decline | ServiceBaseResponse | — | — |

**Total**: 7 | **AB done**: 0
**ABConnectTools file**: `endpoints/rfq.py`, `models/rfq.py`

---

### Shipment (global, non-job-scoped)

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET | GET | /shipment | ShipmentDetails | — | — |
| 2 | ACCESSORIALS | GET | /shipment/accessorials | List[ParcelAddOn] | — | JSON |
| 3 | DOCUMENT | GET | /shipment/document/{docId} | ShippingDocument | — | — |

**Total**: 3 | **AB done**: 0 | **ABConnectTools fixtures**: ShipmentAccessorials.json

---

### SmsTemplate

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | DELETE | DELETE | /SmsTemplate/{templateId} | ServiceBaseResponse | — | — |
| 2 | GET | GET | /SmsTemplate/{templateId} | SmsTemplateModel | — | — |
| 3 | JOB_STATUSES | GET | /SmsTemplate/jobStatuses | List[SmsJobStatus] | — | JSON |
| 4 | LIST | GET | /SmsTemplate/list | List[SmsTemplateModel] | — | JSON |
| 5 | NOTIFICATION_TOKENS | GET | /SmsTemplate/notificationTokens | List[NotificationTokenGroup] | — | JSON |
| 6 | SAVE | POST | /SmsTemplate/save | ServiceBaseResponse | — | — |

**Total**: 6 | **AB done**: 0 | **ABConnectTools fixtures**: SmsTemplateJobStatuses, SmsTemplateList, SmsTemplateNotificationTokens
**ABConnectTools file**: `endpoints/SmsTemplate.py`, `models/jobsmstemplate.py`

---

### Users

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | POCUSERS | GET | /users/pocusers | List[PocUser] | — | JSON |
| 2 | ROLES | GET | /users/roles | List[str] | done | JSON |
| 3 | LIST | POST | /users/list | ServiceBaseResponse | done | — |
| 4 | USER | POST | /users/user | ServiceBaseResponse | — | — |
| 5 | USER_UPDATE | PUT | /users/user | ServiceBaseResponse | — | — |

**Total**: 5 | **AB done**: 2 | **ABConnectTools fixtures**: UsersPocUsers, UsersRoles

---

### V2

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | JOB_TRACKING | GET | /v2/job/{id}/tracking/{historyAmount} | ShipmentTrackingDetails | — | — |

**Total**: 1 | **AB done**: 0 | **Note**: Superseded by V3, skip

---

### V3

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | JOB_TRACKING | GET | /v3/job/{id}/tracking/{historyAmount} | JobTrackingResponseV3 | done | — |

**Total**: 1 | **AB done**: 1 (feature 002)

---

### Values

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | GET | GET | /Values | ValuesResponse | — | JSON |

**Total**: 1 | **AB done**: 0 | **ABConnectTools fixtures**: Values.json

---

### Views

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | DELETE | DELETE | /views/{viewId} | ServiceBaseResponse | — | — |
| 2 | GET | GET | /views/{viewId} | GridViewDetails | — | — |
| 3 | ACCESSINFO | GET | /views/{viewId}/accessinfo | GridViewAccess | — | — |
| 4 | ALL | GET | /views/all | List[GridViewDetails] | — | JSON |
| 5 | DATASETSP | GET | /views/datasetsp/{spName} | List[StoredProcedureColumn] | — | — |
| 6 | DATASETSPS | GET | /views/datasetsps | List[str] | — | JSON |
| 7 | POST | POST | /views | ServiceBaseResponse | — | — |
| 8 | PUT_ACCESS | PUT | /views/{viewId}/access | ServiceBaseResponse | — | — |

**Total**: 8 | **AB done**: 0 | **ABConnectTools fixtures**: ViewsAll, ViewsDatasetSps

---

### Webhooks

| # | Route Key | Method | Path | Response Model | AB | Ref |
|---|-----------|--------|------|---------------|-----|-----|
| 1 | POST_STRIPE_CHECKOUT_SESSION_COMPLETED | POST | /webhooks/stripe/checkout.session.completed | ServiceBaseResponse | — | — |
| 2 | POST_STRIPE_CONNECT_HANDLE | POST | /webhooks/stripe/connect/handle | ServiceBaseResponse | — | — |
| 3 | POST_STRIPE_HANDLE | POST | /webhooks/stripe/handle | ServiceBaseResponse | — | — |
| 4 | POST_TWILIO_BODY_SMS_INBOUND | POST | /webhooks/twilio/body-sms-inbound | ServiceBaseResponse | — | — |
| 5 | POST_TWILIO_FORM_SMS_INBOUND | POST | /webhooks/twilio/form-sms-inbound | ServiceBaseResponse | — | — |
| 6 | POST_TWILIO_SMS_STATUS_CALLBACK | POST | /webhooks/twilio/smsStatusCallback | ServiceBaseResponse | — | — |

**Total**: 6 | **AB done**: 0
**Priority**: Low (inbound webhook handlers)

---

## Endpoint Groups — Catalog API

100% implemented in feature 001. See `ab/api/endpoints/catalog.py`,
`sellers.py`, `lots.py`.

---

## Endpoint Groups — ABC API

Partially implemented in feature 001. See `ab/api/endpoints/autoprice.py`,
`web2lead.py`.

---

## Batch Planning

Pick groups from this document. No re-discovery needed.

### Recommended Next Batches (by fixture availability)

| Batch | Groups | Endpoints | ABConnectTools Fixtures |
|-------|--------|-----------|------------------------|
| 3a | Lookup (extended) | 11 | 6 JSON |
| 3b | SmsTemplate, Notifications, Values | 8 | 4 JSON |
| 3c | Dashboard | 9 | 3 JSON |
| 3d | Views, Partner | 10 | 3 JSON |
| 4 | Companies (extended) | 25 | 5 JSON |
| 5 | Contacts (extended) | 10 | 2 JSON |
| 6 | Job — OnHold, RFQ, FreightProviders | 20 | — |
| 7 | Job — SMS, Email + top-level Note | 13 | — |
| 8 | Company (settings), Reports | 30 | — |
| 9 | Admin, Commodity, CommodityMap | 23 | — |
| 10 | Shipment (global), RFQ, JobIntAcct | 15 | — |
