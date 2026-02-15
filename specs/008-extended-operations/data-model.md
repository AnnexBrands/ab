# Data Model: Extended Operations Endpoints

**Feature**: 008-extended-operations
**Date**: 2026-02-14

All models follow Constitution Principle I: `ResponseModel` (`extra="allow"`) for API responses, `RequestModel` (`extra="forbid"`) for outbound bodies. Fields are `snake_case` with `camelCase` aliases.

## New Model Files

### rfq.py — RFQ Models

| Model | Base | Purpose | Key Fields |
|-------|------|---------|------------|
| `QuoteRequestDisplayInfo` | ResponseModel | RFQ listing entry for a job | rfq_id, provider_company_id, service_type, quoted_price, transit_days, status |
| `QuoteRequestStatus` | ResponseModel | RFQ status for a service/company combo | status, rfq_id, is_active |
| `AcceptModel` | RequestModel | Body for accepting an RFQ | notes (Optional) |

### reports.py — Report Models

| Model | Base | Purpose | Key Fields |
|-------|------|---------|------------|
| `InsuranceReportRequest` | RequestModel | Filter for insurance report | start_date, end_date |
| `InsuranceReport` | ResponseModel | Insurance report result | claims, total_amount, by_status |
| `SalesForecastReportRequest` | RequestModel | Filter for sales forecast | start_date, end_date, agent_code |
| `SalesForecastReport` | ResponseModel | Sales forecast result | projected_revenue, actual_revenue, by_rep |
| `SalesForecastSummaryRequest` | RequestModel | Filter for sales summary | start_date, end_date |
| `SalesForecastSummary` | ResponseModel | Sales summary result | total_revenue, count |
| `Web2LeadRevenueFilter` | RequestModel | Filter for revenue/drilldown reports | start_date, end_date |
| `RevenueCustomer` | ResponseModel | Revenue by customer or sales rep | name, total_revenue, job_count, average_value |
| `ReferredByReportRequest` | RequestModel | Filter for referral report | start_date, end_date |
| `ReferredByReport` | ResponseModel | Referral report result | referrals, by_source |
| `Web2LeadV2RequestModel` | RequestModel | Filter for web lead report | start_date, end_date |
| `Web2LeadReport` | ResponseModel | Web lead report result | leads, by_campaign |

### dashboard.py — Dashboard Models

| Model | Base | Purpose | Key Fields |
|-------|------|---------|------------|
| `DashboardSummary` | ResponseModel | Aggregated dashboard data | inbound_count, outbound_count, in_house_count |
| `GridViewState` | ResponseModel | Saved grid view state | id, columns, filters, sort_order |
| `GridViewInfo` | ResponseModel | Grid view metadata | id, name, is_default |

### views.py — Views/Grids Models

| Model | Base | Purpose | Key Fields |
|-------|------|---------|------------|
| `GridViewDetails` | ResponseModel | Full view configuration | view_id, name, dataset_sp, columns, filters, access |
| `GridViewAccess` | ResponseModel | View access control | view_id, users, roles |
| `StoredProcedureColumn` | ResponseModel | Dataset SP column definition | name, data_type, is_sortable |
| `GridViewCreateRequest` | RequestModel | Body for creating a view | name, dataset_sp, columns |

### commodities.py — Commodity Models

| Model | Base | Purpose | Key Fields |
|-------|------|---------|------------|
| `Commodity` | ResponseModel | Commodity record | id, description, freight_class, nmfc_code |
| `CommodityCreateRequest` | RequestModel | Body for creating a commodity | description, freight_class, nmfc_code, weight_min, weight_max |
| `CommodityUpdateRequest` | RequestModel | Body for updating a commodity | description, freight_class, nmfc_code |
| `CommoditySearchRequest` | RequestModel | Search filter for commodities | search_text, page, page_size |
| `CommoditySuggestionRequest` | RequestModel | Suggestion filter | search_text |
| `CommodityMap` | ResponseModel | Commodity mapping record | id, custom_name, commodity_id |
| `CommodityMapCreateRequest` | RequestModel | Body for creating a map | custom_name, commodity_id |
| `CommodityMapUpdateRequest` | RequestModel | Body for updating a map | custom_name, commodity_id |
| `CommodityMapSearchRequest` | RequestModel | Search filter for maps | search_text, page, page_size |

### notes.py — Global Note Models

| Model | Base | Purpose | Key Fields |
|-------|------|---------|------------|
| `GlobalNote` | ResponseModel | Global note record | id, comment, author, modify_date, category |
| `GlobalNoteCreateRequest` | RequestModel | Body for creating a note | comment, category, job_id, contact_id, company_id |
| `GlobalNoteUpdateRequest` | RequestModel | Body for updating a note | comment, is_important, is_completed |
| `SuggestedUser` | ResponseModel | User suggestion for mentions | contact_id, name, email |

### partners.py — Partner Models

| Model | Base | Purpose | Key Fields |
|-------|------|---------|------------|
| `Partner` | ResponseModel | Partner record | id, name, type, contact_info |
| `PartnerSearchRequest` | RequestModel | Search filter for partners | search_text, page, page_size |

## Extended Model Files

### jobs.py — On-Hold, Email, SMS, Freight Models (added to existing file)

| Model | Base | Purpose | Key Fields |
|-------|------|---------|------------|
| `ExtendedOnHoldInfo` | ResponseModel | On-hold listing entry | id, reason, description, follow_up_user, follow_up_date, status |
| `OnHoldDetails` | ResponseModel | Full on-hold detail | id, reason, description, comments, dates, follow_up_user |
| `SaveOnHoldRequest` | RequestModel | Create/update on-hold | reason, description, follow_up_contact_id, follow_up_date |
| `SaveOnHoldResponse` | ResponseModel | On-hold create/update response | on_hold_id, status |
| `ResolveJobOnHoldResponse` | ResponseModel | On-hold resolution response | resolved, status |
| `SaveOnHoldDatesModel` | RequestModel | Update on-hold dates | follow_up_date, due_date |
| `OnHoldUser` | ResponseModel | Follow-up user info | contact_id, name, email |
| `OnHoldNoteDetails` | ResponseModel | On-hold comment response | id, comment, author, date |
| `SendDocumentEmailModel` | RequestModel | Email request body | to, cc, bcc, subject, body, document_type |
| `SendSMSModel` | RequestModel | SMS request body | phone_number, message, template_id |
| `MarkSmsAsReadModel` | RequestModel | Mark SMS read body | sms_ids |
| `PricedFreightProvider` | ResponseModel | Freight provider with pricing | provider_name, service_types, rate_available |
| `ShipmentPlanProvider` | RequestModel | Save freight provider selection | provider data |

### lookup.py — Extended Lookup Models (added to existing file)

| Model | Base | Purpose | Key Fields |
|-------|------|---------|------------|
| `LookupValue` | ResponseModel | Generic lookup value | id, name, description, value |
| `AccessKey` | ResponseModel | Access key record | key, description |
| `ParcelPackageType` | ResponseModel | Parcel package type | id, name, dimensions |
| `DensityClassEntry` | ResponseModel | Density-to-class mapping | density_min, density_max, freight_class |

### companies.py — Extended Company Models (added to existing file)

| Model | Base | Purpose | Key Fields |
|-------|------|---------|------------|
| `CompanyBrand` | ResponseModel | Brand record | id, name, parent_id |
| `BrandTree` | ResponseModel | Hierarchical brand tree | id, name, children |
| `GeoSettings` | ResponseModel | Geographic settings | company_id, service_areas, restrictions |
| `GeoSettingsSaveRequest` | RequestModel | Save geo settings body | service_areas, restrictions |
| `CarrierAccount` | ResponseModel | Carrier account | id, carrier_name, account_number |
| `CarrierAccountSaveRequest` | RequestModel | Save carrier account body | carrier_name, account_number |
| `PackagingSettings` | ResponseModel | Packaging config | company_id, settings |
| `PackagingLabor` | ResponseModel | Packaging labor config | company_id, labor_rates |
| `PackagingTariff` | ResponseModel | Inherited packaging tariff | tariff_id, rates |

### contacts.py — Extended Contact Models (added to existing file)

| Model | Base | Purpose | Key Fields |
|-------|------|---------|------------|
| `ContactHistory` | ResponseModel | Contact interaction history | events, total_count |
| `ContactHistoryAggregated` | ResponseModel | Aggregated history | summary, by_type |
| `ContactGraphData` | ResponseModel | Contact graph data | data_points, labels |
| `ContactMergePreview` | ResponseModel | Merge preview result | merge_to, merge_from, conflicts |

## Model Count Summary

| Category | Response Models | Request Models | Total |
|----------|----------------|----------------|-------|
| RFQ | 2 | 1 | 3 |
| Reports | 7 | 5 | 12 |
| Dashboard | 3 | 0 | 3 |
| Views | 3 | 1 | 4 |
| Commodities | 3 | 5 | 8 |
| Commodity Maps | 1 | 3 | 4 |
| Notes | 2 | 2 | 4 |
| Partners | 1 | 1 | 2 |
| On-Hold (jobs.py) | 5 | 2 | 7 |
| Email/SMS (jobs.py) | 0 | 3 | 3 |
| Freight (jobs.py) | 1 | 1 | 2 |
| Lookup (extended) | 4 | 0 | 4 |
| Companies (extended) | 5 | 2 | 7 |
| Contacts (extended) | 4 | 0 | 4 |
| **TOTAL** | **41** | **26** | **67** |

## Notes

- The "Key Fields" columns above list representative attributes, not exhaustive field lists. See the actual Pydantic model source files in `ab/api/models/` for the complete field definitions.
- All response models use `extra="allow"` with drift logging. Field definitions are initial best-guesses from swagger; actual fields will be refined during fixture capture (Constitution Principle IV).
- Many swagger schemas for these endpoints are incomplete or missing. Initial models will have `Optional[dict]` or `Optional[List[dict]]` fields for complex nested structures, to be refined when live API responses reveal the actual shape.
- Request models will be validated against swagger parameter definitions and ABConnectTools implementations during Phase D of each batch.
