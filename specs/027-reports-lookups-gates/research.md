# Research: Reports & Lookups Quality Gates

**Branch**: `027-reports-lookups-gates` | **Date**: 2026-03-01

## C# Ground Truth Findings

### Sources of Truth Hierarchy Applied

1. **Tier 1 — C# Source** (`/src/ABConnect/`): Read actual DTO classes
2. **Tier 3 — Swagger** (`ab/api/schemas/acportal.json`): Cross-referenced field names
3. **Tier 2 — Fixtures**: Will be captured from staging to validate

### Report Response Models

#### InsuranceReportModel (C# entity: `AB.ABCEntities/InsuranceReportModel.cs`)

The C# entity is dual-purpose (request + response). Swagger shows the response subset:

| C# Property | Type | Nullable | Swagger Name | Python Alias |
|-------------|------|----------|-------------|-------------|
| Jobnum | string | yes | jobNumber | job_number |
| Franchisee | string | yes | franchisee | franchisee |
| InsuranceType | string | yes | insuranceType | insurance_type |
| numpiece | int? | yes | noOfPiece | no_of_piece |
| TotalCost | decimal? | yes | totalCost | total_cost |
| Jobdate | string | yes | jobDate | job_date |
| InsuranceCost | decimal? | yes | insuranceCost | insurance_cost |
| Carrier | string | yes | carrier | carrier |
| Inaccdate | string | yes | intacctDate | intacct_date |
| TotalRecord | int? | yes | totalRecords | total_records |

**Decision**: Use swagger field names as aliases (they match the JSON serialization). All fields Optional since C# nullable.

#### Salesforecast (C# entity: `AB.ABCEntities/Salesforecast.cs`)

Dual-purpose entity. Swagger response subset:

| C# Property | Type | Nullable | Swagger Name | Python Alias |
|-------------|------|----------|-------------|-------------|
| Franchisee | string | yes | franchisee | franchisee |
| Company | string | yes | company | company |
| JobID | string | yes | jobID | job_id |
| JobType | string | yes | jobType | job_type |
| QuoteDate | string | yes | quoteDate | quote_date |
| BookedDate | string | yes | bookedDate | booked_date |
| Revenue | decimal? | yes | revenue | revenue |
| Profit | decimal? | yes | profit | profit |
| GrossMargin | decimal? | yes | grossMargin | gross_margin |
| Status | string | yes | status | status |
| Industry | string | yes | industry | industry |
| CustomerZipCode | string | yes | customerZipCode | customer_zip_code |
| IntacctDate | string | yes | intacctDate | intacct_date |
| TotalRecords | int? | yes | totalRecords | total_records |

**Decision**: Use swagger subset. Additional C# fields (pagination, sorting, userID, etc.) are request-side; they may appear in response but will be caught by `extra="allow"`.

#### SalesForecastSummary (swagger-only, no dedicated C# class)

| Swagger Name | Type | Nullable | Python Alias |
|-------------|------|----------|-------------|
| revenue | number/double | yes | revenue |
| profit | number/double | yes | profit |
| grossMargin | number/double | yes | gross_margin |
| closeRatio | number/double | yes | close_ratio |

**Decision**: Matches Salesforecast entity subset. Create from swagger.

#### RevenueCustomer (C# entity: `AB.ABCEntities/ReportModels/RevenueCustomer.cs`)

| C# Property | Type | Nullable | Swagger Name | Python Alias |
|-------------|------|----------|-------------|-------------|
| Id | string | yes | id | id |
| Name | string | yes | name | name |

**Decision**: Simple 2-field model. Current Python model has 4 invented fields (total_revenue, job_count, average_value) — remove them.

#### ReferedData (C# entity: `AB.ABCEntities/ReferedData.cs`)

| C# Property | Type | Nullable | Swagger Name | Python Alias |
|-------------|------|----------|-------------|-------------|
| ReferredBy | string | yes | referredBy | referred_by |
| ReferredName | string | yes | referredName | referred_name |
| ReferedByCategory | string | yes | referredByCategory | referred_by_category |
| QuoteDate | string | yes | quoteDate | quote_date |
| BookedDate | string | yes | bookedDate | booked_date |
| Revenue | decimal? | yes | revenue | revenue |
| Profit | decimal? | yes | profit | profit |
| Customer | string | yes | customer | customer |
| JobDisplayID | string | yes | jobDisplayID | job_display_id |
| Industry | string | yes | industry | industry |
| CustomerZipCode | string | yes | customerZipCode | customer_zip_code |
| IntacctDate | string | yes | intacctDate | intacct_date |
| TotalRecords | int? | yes | totalRecords | total_records |

**Note**: C# has additional fields (jobID as Guid, status, jobIsQuickSale, jobStatusID, rowID) that may appear in response. Use swagger subset as baseline; extras will be caught by `extra="allow"` and logged.

#### Web2Lead (C# entity: `AB.ABCEntities/ReportModels/Web2Lead.cs`)

| C# Property | Type | Nullable | Swagger Name | Python Alias |
|-------------|------|----------|-------------|-------------|
| Franchisee | string | yes | franchiseeID | franchisee_id |
| Type | string | yes | type | type |
| JobID | string | yes | jobDisplayID | job_display_id |
| IntacctStatus | string | yes | intacctStatus | intacct_status |
| LeadDate | string | yes | leadDate | lead_date |
| CompanyName | string | yes | companyName | company_name |
| ReferPage | string | yes | referPage | refer_page |
| EntryURL | string | yes | entryURL | entry_url |
| SubmissionPage | string | yes | submissionPage | submission_page |
| HowHeard | string | yes | howHeard | how_heard |
| Email | string | yes | email | email |
| Phone | string | yes | phone | phone |
| ShipFrom | string | yes | shipFrom | ship_from |
| ShipTo | string | yes | shipTo | ship_to |
| ReferedName | string | yes | referredName | referred_name |
| CustomerComments | string | yes | customerComments | customer_comments |
| CurrentBookPrice | decimal? | yes | currentBookPrice | current_book_price |
| CurrentBookProfit | decimal? | yes | currentBookProfit | current_book_profit |
| ReferedByCategory | string | yes | referredByCategory | referred_by_category |
| TotalRecords | int? | yes | totalRecords | total_records |

### Lookup Response Models

#### MasterData → LookupValue (C# entity: `AB.ABCEntities/MasterData.cs`)

| C# Property | Type | Nullable | JSON Key | Python Alias |
|-------------|------|----------|----------|-------------|
| Key | string | yes | key | key |
| Name | string | yes | name | name |
| Value | Guid | no | value | value |

**Decision**: Current Python LookupValue has id/name/description/value — completely wrong. C# MasterData has key/name/value (Guid). Must rewrite.

**BUT**: The lookup controller at `LookupController.cs` transforms to anonymous `{Id, Name}` for some endpoints. Need to verify via live fixture which shape each endpoint actually returns.

#### APIAccessKey (C# entity: `AB.ABCEntities/Common/APIAccessKey.cs`)

| C# Property | Type | JSON Key | Python Alias |
|-------------|------|----------|-------------|
| AccessKey | string | accessKey | access_key |
| FriendlyName | string | friendlyName | friendly_name |

**Decision**: Current Python AccessKey has key/description — wrong aliases. Must fix to accessKey/friendlyName.

#### APIAccessKeySetup (C# entity: `ABC.Services.Interfaces/Entities/APIAccessKey.cs`)

Used for GET /lookup/accessKey/{accessKey} — returns detailed setup, NOT the simple AccessKey.

| C# Property | Type | Nullable | JSON Key | Python Alias |
|-------------|------|----------|----------|-------------|
| UserId | Guid | no | userId | user_id |
| UserIdentifier | int | no | userIdentifier | user_identifier |
| ReferredById | Guid? | yes | referredById | referred_by_id |
| ReferredBy | string | yes | referredBy | referred_by |
| UseAgentSearch | bool | no | useAgentSearch | use_agent_search |
| AllowJobInfoUpdate | bool | no | allowJobInfoUpdate | allow_job_info_update |
| AllowJobInfoUpdateWithoutBookingKey | bool | no | allowJobInfoUpdateWithoutBookingKey | allow_job_info_update_without_booking_key |
| IpProtections | List<APIIpProtection> | yes | ipProtections | ip_protections |
| ParcelTransportationMultiplier | decimal? | yes | parcelTransportationMultiplier | parcel_transportation_multiplier |
| ParcelAccessorialMultiplier | decimal? | yes | parcelAccessorialMultiplier | parcel_accessorial_multiplier |
| ItemsCombineMaxInches | byte? | yes | itemsCombineMaxInches | items_combine_max_inches |
| UsePackLaborCalculation | bool | no | usePackLaborCalculation | use_pack_labor_calculation |
| UseBasePickupFeeCalculation | bool | no | useBasePickupFeeCalculation | use_base_pickup_fee_calculation |
| ForceAgentPickup | bool | no | forceAgentPickup | force_agent_pickup |

**Decision**: Need a new model `AccessKeySetup` for GET /lookup/accessKey/{accessKey}. The Route's response_model must be updated from `AccessKey` to `AccessKeySetup`.

#### DocumentTypeBySource (C# entity: `AB.ABCEntities/Common/DocumentTypeBySource.cs`)

| C# Property | Type | JSON Key | Python Alias |
|-------------|------|----------|-------------|
| Name | string | name | name |
| Value | int | value | value |
| DocumentSource | byte | documentSource | document_source |

**Decision**: Currently using LookupValue as response model — wrong. Need dedicated DocumentTypeBySource model.

#### PPCCampaign (C# entity: `AB.ABCEntities/PPCCampaign.cs`)

| C# Property | Type | JSON Key | Python Alias |
|-------------|------|----------|-------------|
| Id | int | id | id |
| Name | string | name | name |

**Decision**: Currently using LookupValue — wrong shape. Need PPCCampaign model or can reuse a simple {id, name} pattern.

#### ContactTypeEntity (C# entity: `AB.ABCEntities/ContactEntities/ContactTypeEntity.cs`)

| C# Property | Type | JSON Key |
|-------------|------|----------|
| Id | int | id |
| Value | string | value |

**Decision**: Current Python model has name/description fields that don't exist in C#. Need to verify against live fixture — if fixture passes, leave as-is (extra fields allowed on response models). If fixture shows extras, fix.

#### CountryEntity (C# entity: `AB.ABCEntities/Common/CountryEntity.cs`)

Controller transforms to anonymous `{Id = CountryId, Name = CountryName}` but also passes IATACode. Live fixture needed to confirm.

### Request Model Observations

The request models (InsuranceReportRequest, SalesForecastReportRequest, etc.) extend DateRangeRequestMixin with startDate/endDate. The C# entities show the full filter shapes are more complex (Web2LeadRevenueFilter has userID, franchisees, industryTypes, etc.). Current request models are simplified — they work for basic calls but may need enrichment for filtering. This is out of scope for this PR (focused on response models and gates).

## Decisions

1. **Rewrite all 6 report response models** to match C#/swagger field definitions
2. **Rewrite LookupValue** to match MasterData (key/name/value)
3. **Rewrite AccessKey** to match APIAccessKey (accessKey/friendlyName)
4. **Create AccessKeySetup** model for GET /lookup/accessKey/{accessKey}
5. **Create DocumentTypeBySource** model for GET /lookup/documentTypes
6. **Create PPCCampaign** model for GET /lookup/PPCCampaigns
7. **Verify basic lookups** (contactTypes, countries, jobStatuses) against live fixtures — fix only if needed
8. **Capture all missing fixtures** via example runner with date range params
9. **Trust live response over swagger** when they disagree (Tier 2 > Tier 3)
