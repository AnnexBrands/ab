# Data Model: Extended API Endpoints

**Branch**: `002-extended-endpoints` | **Date**: 2026-02-13

## Model Hierarchy

All new models inherit from the existing base classes established in feature 001:

```
ABConnectBaseModel
├── RequestModel   (extra="forbid")
└── ResponseModel  (extra="allow" + drift warning)
```

Existing mixins reused where applicable:
- `IdentifiedModel` — `id: Optional[str]`
- `TimestampedModel` — `created_date`, `modified_date`, `created_by`, `modified_by`
- `FullAuditModel` — `IdentifiedModel + TimestampedModel + ActiveModel`

## New Models by Group

### Timeline & Status (in `ab/api/models/jobs.py`)

#### TimelineTask (ResponseModel, IdentifiedModel)

Represents a single task in a job's lifecycle timeline.

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| id | Optional[str] | id | Timeline task ID |
| task_code | Optional[str] | taskCode | Task type code (e.g., "SCH", "RCV", "PKS") |
| status | Optional[int] | status | Status code (numeric) |
| status_name | Optional[str] | statusName | Human-readable status |
| agent_contact_id | Optional[str] | agentContactId | Assigned agent |
| scheduled_date | Optional[str] | scheduledDate | When task is scheduled |
| completed_date | Optional[str] | completedDate | When task was completed |
| comments | Optional[str] | comments | Task notes |
| is_completed | Optional[bool] | isCompleted | Completion flag |
| sort_order | Optional[int] | sortOrder | Display order |

#### TimelineTaskCreateRequest (RequestModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| task_code | str | taskCode | Task type code (required) |
| scheduled_date | Optional[str] | scheduledDate | Scheduled date |
| comments | Optional[str] | comments | Notes |
| agent_contact_id | Optional[str] | agentContactId | Assigned agent |

#### TimelineTaskUpdateRequest (RequestModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| status | Optional[int] | status | New status code |
| scheduled_date | Optional[str] | scheduledDate | Updated schedule |
| completed_date | Optional[str] | completedDate | Completion date |
| comments | Optional[str] | comments | Updated notes |

#### TimelineAgent (ResponseModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| contact_id | Optional[str] | contactId | Agent contact ID |
| name | Optional[str] | name | Agent name |
| company_name | Optional[str] | companyName | Agent's company |

#### IncrementStatusRequest (RequestModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| create_email | Optional[bool] | createEmail | Send status notification email |

---

### Shipments (in `ab/api/models/shipments.py`)

#### RateQuote (ResponseModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| carrier_name | Optional[str] | carrierName | Carrier company name |
| service_type | Optional[str] | serviceType | Service level |
| total_charge | Optional[float] | totalCharge | Total quoted price |
| transit_days | Optional[int] | transitDays | Estimated transit time |
| accessorial_charges | Optional[List[dict]] | accessorialCharges | Itemized extras |
| provider_option_index | Optional[int] | providerOptionIndex | Index for booking selection |

#### ShipmentBookRequest (RequestModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| provider_option_index | Optional[int] | providerOptionIndex | Selected rate quote index |
| ship_date | Optional[str] | shipDate | Requested ship date |

#### ShipmentOriginDestination (ResponseModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| origin | Optional[dict] | origin | Origin address details |
| destination | Optional[dict] | destination | Destination address details |

#### Accessorial (ResponseModel, IdentifiedModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| id | Optional[str] | id | Add-on ID |
| name | Optional[str] | name | Accessorial name |
| description | Optional[str] | description | Description |
| price | Optional[float] | price | Additional cost |
| is_selected | Optional[bool] | isSelected | Whether currently applied |

#### AccessorialAddRequest (RequestModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| add_on_id | str | addOnId | Accessorial ID to add |

#### ShipmentExportData (ResponseModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| export_data | Optional[dict] | exportData | Shipment export payload |

#### RatesState (ResponseModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| state | Optional[str] | state | Current rates state |
| rates | Optional[List[dict]] | rates | Available rates |

#### ShipmentInfo (ResponseModel)

Global shipment details (non-job-scoped).

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| shipment_id | Optional[str] | shipmentId | Shipment identifier |
| status | Optional[str] | status | Current status |
| carrier | Optional[str] | carrier | Carrier name |
| pro_number | Optional[str] | proNumber | PRO tracking number |

#### GlobalAccessorial (ResponseModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| id | Optional[str] | id | Accessorial ID |
| name | Optional[str] | name | Name |
| category | Optional[str] | category | Category grouping |

---

### Tracking (in `ab/api/models/jobs.py`)

#### TrackingInfo (ResponseModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| status | Optional[str] | status | Current tracking status |
| location | Optional[str] | location | Current location |
| estimated_delivery | Optional[str] | estimatedDelivery | ETA |
| events | Optional[List[dict]] | events | Tracking event history |
| carrier_name | Optional[str] | carrierName | Carrier |
| pro_number | Optional[str] | proNumber | PRO number |

#### TrackingInfoV3 (ResponseModel)

Extended tracking with history depth control.

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| tracking_details | Optional[List[dict]] | trackingDetails | Detailed tracking entries |
| carrier_info | Optional[List[dict]] | carrierInfo | Carrier metadata |
| shipment_status | Optional[str] | shipmentStatus | Overall status |

---

### Payments (in `ab/api/models/payments.py`)

#### PaymentInfo (ResponseModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| total_amount | Optional[float] | totalAmount | Job total |
| balance_due | Optional[float] | balanceDue | Remaining balance |
| payment_status | Optional[str] | paymentStatus | Current status |
| payments | Optional[List[dict]] | payments | Payment history |

#### PaymentSource (ResponseModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| source_id | Optional[str] | sourceId | Payment source ID |
| type | Optional[str] | type | "card" or "bank_account" |
| last_four | Optional[str] | lastFour | Last 4 digits |
| brand | Optional[str] | brand | Card brand (Visa, etc.) |
| is_default | Optional[bool] | isDefault | Default source flag |

#### PayBySourceRequest (RequestModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| source_id | str | sourceId | Payment source to charge |
| amount | Optional[float] | amount | Amount (or full balance) |

#### ACHSessionRequest (RequestModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| return_url | Optional[str] | returnUrl | Redirect after session |

#### ACHSessionResponse (ResponseModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| session_id | Optional[str] | sessionId | ACH session identifier |
| client_secret | Optional[str] | clientSecret | Stripe client secret |

#### ACHCreditTransferRequest (RequestModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| amount | float | amount | Transfer amount |

#### AttachBankRequest (RequestModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| token | str | token | Bank account token |

#### VerifyACHRequest (RequestModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| amounts | List[int] | amounts | Micro-deposit verification amounts |

#### BankSourceRequest (RequestModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| source_id | str | sourceId | Bank source ID |

---

### Notes (in `ab/api/models/jobs.py`)

#### JobNote (ResponseModel, IdentifiedModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| id | Optional[str] | id | Note ID |
| comment | Optional[str] | comment | Note content |
| is_important | Optional[bool] | isImportant | Flagged as important |
| is_completed | Optional[bool] | isCompleted | Completion status |
| author | Optional[str] | author | Author name |
| modify_date | Optional[str] | modifiyDate | Last modified (note: API typo "modifiy") |
| task_code | Optional[str] | taskCode | Associated timeline task |

#### JobNoteCreateRequest (RequestModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| comments | str | comments | Note content (max 8000 chars) |
| task_code | str | taskCode | Associated timeline task code |
| is_important | Optional[bool] | isImportant | Flag as important |
| send_notification | Optional[bool] | sendNotification | Notify assigned users |
| due_date | Optional[str] | dueDate | Due date |

#### JobNoteUpdateRequest (RequestModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| comments | Optional[str] | comments | Updated content |
| is_important | Optional[bool] | isImportant | Updated flag |
| is_completed | Optional[bool] | isCompleted | Mark complete |

---

### Parcels & Items (in `ab/api/models/jobs.py`)

#### ParcelItem (ResponseModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| parcel_item_id | Optional[str] | parcelItemId | Parcel item ID |
| description | Optional[str] | description | Item description |
| length | Optional[float] | length | Length (inches) |
| width | Optional[float] | width | Width (inches) |
| height | Optional[float] | height | Height (inches) |
| weight | Optional[float] | weight | Weight (lbs) |
| quantity | Optional[int] | quantity | Number of pieces |
| packaging_type | Optional[str] | packagingType | Package type |

#### ParcelItemWithMaterials (ResponseModel)

Extends ParcelItem with materials data.

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| parcel_item_id | Optional[str] | parcelItemId | Parcel item ID |
| description | Optional[str] | description | Item description |
| materials | Optional[List[dict]] | materials | Associated materials |
| dimensions | Optional[dict] | dimensions | Packed dimensions |

#### ParcelItemCreateRequest (RequestModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| description | str | description | Item description |
| length | Optional[float] | length | Length |
| width | Optional[float] | width | Width |
| height | Optional[float] | height | Height |
| weight | Optional[float] | weight | Weight |
| quantity | Optional[int] | quantity | Quantity |

#### PackagingContainer (ResponseModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| container_id | Optional[str] | containerId | Container ID |
| name | Optional[str] | name | Container name |
| dimensions | Optional[dict] | dimensions | Container dimensions |

#### ItemNotesRequest (RequestModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| notes | str | notes | Item notes content |

#### ItemUpdateRequest (RequestModel)

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| description | Optional[str] | description | Updated description |
| quantity | Optional[int] | quantity | Updated quantity |
| weight | Optional[float] | weight | Updated weight |

---

### Forms (in `ab/api/models/forms.py`)

#### FormsShipmentPlan (ResponseModel)

The only JSON-returning form endpoint (`get_form_shipments`).

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| shipment_plan_id | Optional[str] | shipmentPlanId | Plan identifier |
| provider_option_index | Optional[int] | providerOptionIndex | Provider index |
| carrier_name | Optional[str] | carrierName | Carrier |
| service_type | Optional[str] | serviceType | Service level |

*All other form endpoints return raw PDF `bytes` — no Pydantic model needed.*

## Model Count Summary

| Group | Response Models | Request Models | Total |
|-------|----------------|----------------|-------|
| Timeline/Status | 3 (TimelineTask, TimelineAgent, +ServiceBaseResponse) | 3 (Create, Update, IncrementStatus) | 6 |
| Shipments | 7 (RateQuote, ShipmentOriginDestination, Accessorial, ShipmentExportData, RatesState, ShipmentInfo, GlobalAccessorial) | 2 (ShipmentBookRequest, AccessorialAddRequest) | 9 |
| Tracking | 2 (TrackingInfo, TrackingInfoV3) | 0 | 2 |
| Payments | 3 (PaymentInfo, PaymentSource, ACHSessionResponse) | 5 (PayBySource, ACHSession, ACHCreditTransfer, AttachBank, VerifyACH, BankSource) | 8 |
| Notes | 1 (JobNote) | 2 (Create, Update) | 3 |
| Parcels/Items | 3 (ParcelItem, ParcelItemWithMaterials, PackagingContainer) | 3 (Create, ItemNotes, ItemUpdate) | 6 |
| Forms | 1 (FormsShipmentPlan) | 0 | 1 |
| **Total** | **20** | **15** | **35** |

## Notes on Model Design

- **All response fields are `Optional`** with `None` default. ACPortal API responses are unpredictable about which fields are present. Making fields required would cause validation failures on partial responses.
- **Complex nested structures use `dict` or `List[dict]`** initially. These will be refined to typed sub-models as fixtures reveal the actual data shapes. This is the same progressive typing approach used in feature 001.
- **API typos are preserved in aliases** (e.g., `modifiyDate` in JobNote). The field name uses correct spelling (`modify_date`) but the alias matches the actual API key.
- **`ServiceBaseResponse`** is reused for status/confirmation endpoints (increment, undo, delete operations) rather than defining new response models.
