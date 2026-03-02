# Data Model: Reports & Lookups Quality Gates

**Branch**: `027-reports-lookups-gates` | **Date**: 2026-03-01

## Report Response Models (rewrite from C# ground truth)

### InsuranceReport

Source: `InsuranceReportModel.cs` + swagger `InsuranceReport`

| Field | Type | Nullable | Alias | Description |
|-------|------|----------|-------|-------------|
| job_number | str | yes | jobNumber | Job display number |
| franchisee | str | yes | franchisee | Franchisee code |
| insurance_type | str | yes | insuranceType | Insurance type |
| no_of_piece | int | yes | noOfPiece | Number of pieces |
| total_cost | float | yes | totalCost | Total declared value |
| job_date | str | yes | jobDate | Job date |
| insurance_cost | float | yes | insuranceCost | Insurance cost |
| carrier | str | yes | carrier | Carrier name |
| intacct_date | str | yes | intacctDate | Intacct sync date |
| total_records | int | yes | totalRecords | Total record count |

### SalesForecastReport

Source: `Salesforecast.cs` + swagger `SalesForecastReport`

| Field | Type | Nullable | Alias | Description |
|-------|------|----------|-------|-------------|
| franchisee | str | yes | franchisee | Franchisee code |
| company | str | yes | company | Company name |
| job_id | str | yes | jobID | Job display ID |
| job_type | str | yes | jobType | Job type |
| quote_date | str | yes | quoteDate | Quote date |
| booked_date | str | yes | bookedDate | Booked date |
| revenue | float | yes | revenue | Revenue amount |
| profit | float | yes | profit | Profit amount |
| gross_margin | float | yes | grossMargin | Gross margin percentage |
| status | str | yes | status | Job status |
| industry | str | yes | industry | Industry type |
| customer_zip_code | str | yes | customerZipCode | Customer zip code |
| intacct_date | str | yes | intacctDate | Intacct sync date |
| total_records | int | yes | totalRecords | Total record count |

### SalesForecastSummary

Source: swagger `SalesForecastSummary`

| Field | Type | Nullable | Alias | Description |
|-------|------|----------|-------|-------------|
| revenue | float | yes | revenue | Total revenue |
| profit | float | yes | profit | Total profit |
| gross_margin | float | yes | grossMargin | Gross margin percentage |
| close_ratio | float | yes | closeRatio | Close ratio |

### RevenueCustomer

Source: `RevenueCustomer.cs`

| Field | Type | Nullable | Alias | Description |
|-------|------|----------|-------|-------------|
| id | str | yes | id | Customer or rep ID |
| name | str | yes | name | Customer or rep name |

### ReferredByReport

Source: `ReferedData.cs` + swagger `ReferredByReport`

| Field | Type | Nullable | Alias | Description |
|-------|------|----------|-------|-------------|
| referred_by | str | yes | referredBy | Referral source |
| referred_name | str | yes | referredName | Referral contact name |
| referred_by_category | str | yes | referredByCategory | Referral category |
| quote_date | str | yes | quoteDate | Quote date |
| booked_date | str | yes | bookedDate | Booked date |
| revenue | float | yes | revenue | Revenue amount |
| profit | float | yes | profit | Profit amount |
| customer | str | yes | customer | Customer name |
| job_display_id | int | no | jobDisplayID | Job display ID |
| industry | str | yes | industry | Industry type |
| customer_zip_code | str | yes | customerZipCode | Customer zip code |
| intacct_date | str | yes | intacctDate | Intacct sync date |
| total_records | int | yes | totalRecords | Total record count |

### Web2LeadReport

Source: `Web2Lead.cs` + swagger

| Field | Type | Nullable | Alias | Description |
|-------|------|----------|-------|-------------|
| franchisee_id | str | yes | franchiseeID | Franchisee ID |
| type | str | yes | type | Lead type |
| job_display_id | str | yes | jobDisplayID | Job display ID |
| intacct_status | str | yes | intacctStatus | Intacct status |
| lead_date | str | yes | leadDate | Lead creation date |
| company_name | str | yes | companyName | Company name |
| refer_page | str | yes | referPage | Referring page URL |
| entry_url | str | yes | entryURL | Entry URL |
| submission_page | str | yes | submissionPage | Submission page URL |
| how_heard | str | yes | howHeard | How customer heard of us |
| email | str | yes | email | Contact email |
| phone | str | yes | phone | Contact phone |
| ship_from | str | yes | shipFrom | Ship from location |
| ship_to | str | yes | shipTo | Ship to location |
| referred_name | str | yes | referredName | Referral name |
| customer_comments | str | yes | customerComments | Customer comments |
| current_book_price | float | no | currentBookPrice | Current booked price |
| current_book_profit | float | no | currentBookProfit | Current booked profit |
| referred_by_category | str | yes | referredByCategory | Referral category |
| total_records | int | yes | totalRecords | Total record count |

## Lookup Response Models (fix from C# ground truth)

### LookupValue (rewrite)

Source: `MasterData.cs` — GET /lookup/{masterConstantKey}

| Field | Type | Nullable | Alias | Description |
|-------|------|----------|-------|-------------|
| key | str | yes | key | Master constant key |
| name | str | yes | name | Display name |
| value | str | yes | value | Value (Guid as string) |

**Note**: Verify against live fixture. Controller may transform shape.

### AccessKey (rewrite)

Source: `APIAccessKey.cs` — GET /lookup/accessKeys

| Field | Type | Nullable | Alias | Description |
|-------|------|----------|-------|-------------|
| access_key | str | yes | accessKey | API access key |
| friendly_name | str | yes | friendlyName | Human-readable name |

### AccessKeySetup (new)

Source: `APIAccessKeySetup.cs` — GET /lookup/accessKey/{accessKey}

| Field | Type | Nullable | Alias | Description |
|-------|------|----------|-------|-------------|
| user_id | str | yes | userId | User UUID |
| user_identifier | int | yes | userIdentifier | User numeric ID |
| referred_by_id | str | yes | referredById | Referred-by UUID |
| referred_by | str | yes | referredBy | Referred-by name |
| use_agent_search | bool | yes | useAgentSearch | Agent search enabled |
| allow_job_info_update | bool | yes | allowJobInfoUpdate | Job info update allowed |
| allow_job_info_update_without_booking_key | bool | yes | allowJobInfoUpdateWithoutBookingKey | Update without booking key |
| ip_protections | list | yes | ipProtections | IP protection rules |
| parcel_transportation_multiplier | float | yes | parcelTransportationMultiplier | Parcel transport multiplier |
| parcel_accessorial_multiplier | float | yes | parcelAccessorialMultiplier | Parcel accessorial multiplier |
| items_combine_max_inches | int | yes | itemsCombineMaxInches | Max combine inches |
| use_pack_labor_calculation | bool | yes | usePackLaborCalculation | Pack labor calculation enabled |
| use_base_pickup_fee_calculation | bool | yes | useBasePickupFeeCalculation | Base pickup fee calculation |
| force_agent_pickup | bool | yes | forceAgentPickup | Force agent pickup |

### DocumentTypeBySource (new)

Source: `DocumentTypeBySource.cs` — GET /lookup/documentTypes

| Field | Type | Nullable | Alias | Description |
|-------|------|----------|-------|-------------|
| name | str | yes | name | Document type name |
| value | int | yes | value | Document type ID |
| document_source | int | yes | documentSource | Document source code |

### PPCCampaign (new)

Source: `PPCCampaign.cs` — GET /lookup/PPCCampaigns

| Field | Type | Nullable | Alias | Description |
|-------|------|----------|-------|-------------|
| id | int | yes | id | Campaign ID |
| name | str | yes | name | Campaign name |

## Models Unchanged

- **ContactTypeEntity**: C# has id/value only but live fixture validates current model (id/name/description/value). Verify and keep if passing.
- **CountryCodeDto**: Controller transforms shape. Verify against live fixture.
- **JobStatus**: No C# class found. Verify against live fixture.
- **LookupItem**: Matches C# (id/name). Already passes all gates.
- **ParcelPackageType**: No C# class found. Verify against live fixture.
- **DensityClassEntry**: Swagger says GuidSequentialRangeValue (rangeEnd/value). Verify against live fixture — may need complete rewrite.
