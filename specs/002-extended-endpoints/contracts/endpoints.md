# API Contracts: Extended Endpoints

**Branch**: `002-extended-endpoints` | **Date**: 2026-02-13
**Total**: 62 new endpoints (all ACPortal)

## ACPortal API

Base URL: `https://portal.{env}.abconnect.co/api/api`
Auth: Bearer JWT

### Timeline & Status (9)

| Method | Path | Request Model | Response Model | Schema Reliable |
|--------|------|---------------|----------------|-----------------|
| GET | `/job/{jobDisplayId}/timeline` | — | List[TimelineTask] | No |
| POST | `/job/{jobDisplayId}/timeline` | TimelineTaskCreateRequest | TimelineTask | No |
| GET | `/job/{jobDisplayId}/timeline/{timelineTaskIdentifier}` | — | TimelineTask | No |
| PATCH | `/job/{jobDisplayId}/timeline/{timelineTaskId}` | TimelineTaskUpdateRequest | TimelineTask | No |
| DELETE | `/job/{jobDisplayId}/timeline/{timelineTaskId}` | — | ServiceBaseResponse | No |
| GET | `/job/{jobDisplayId}/timeline/{taskCode}/agent` | — | TimelineAgent | No |
| POST | `/job/{jobDisplayId}/timeline/incrementjobstatus` | IncrementStatusRequest | ServiceBaseResponse | No |
| POST | `/job/{jobDisplayId}/timeline/undoincrementjobstatus` | IncrementStatusRequest | ServiceBaseResponse | No |
| POST | `/job/{jobDisplayId}/status/quote` | — | ServiceBaseResponse | No |

### Shipments — Job-Scoped (11)

| Method | Path | Request Model | Response Model | Schema Reliable |
|--------|------|---------------|----------------|-----------------|
| GET | `/job/{jobDisplayId}/shipment/ratequotes` | — | List[RateQuote] | No |
| POST | `/job/{jobDisplayId}/shipment/ratequotes` | — (query params) | List[RateQuote] | No |
| POST | `/job/{jobDisplayId}/shipment/book` | ShipmentBookRequest | ServiceBaseResponse | No |
| DELETE | `/job/{jobDisplayId}/shipment` | — | ServiceBaseResponse | No |
| GET | `/job/{jobDisplayId}/shipment/accessorials` | — | List[Accessorial] | No |
| POST | `/job/{jobDisplayId}/shipment/accessorial` | AccessorialAddRequest | ServiceBaseResponse | No |
| DELETE | `/job/{jobDisplayId}/shipment/accessorial/{addOnId}` | — | ServiceBaseResponse | No |
| GET | `/job/{jobDisplayId}/shipment/origindestination` | — | ShipmentOriginDestination | No |
| GET | `/job/{jobDisplayId}/shipment/exportdata` | — | ShipmentExportData | No |
| POST | `/job/{jobDisplayId}/shipment/exportdata` | — (body) | ServiceBaseResponse | No |
| GET | `/job/{jobDisplayId}/shipment/ratesstate` | — | RatesState | No |

### Shipments — Global (3)

| Method | Path | Request Model | Response Model | Schema Reliable |
|--------|------|---------------|----------------|-----------------|
| GET | `/shipment` | — (query params) | ShipmentInfo | No |
| GET | `/shipment/accessorials` | — | List[GlobalAccessorial] | No |
| GET | `/shipment/document/{docId}` | — | bytes | No |

### Tracking (2)

| Method | Path | Request Model | Response Model | Schema Reliable |
|--------|------|---------------|----------------|-----------------|
| GET | `/job/{jobDisplayId}/tracking` | — | TrackingInfo | No |
| GET | `/v3/job/{jobDisplayId}/tracking/{historyAmount}` | — | TrackingInfoV3 | No |

### Payments (10)

| Method | Path | Request Model | Response Model | Schema Reliable |
|--------|------|---------------|----------------|-----------------|
| GET | `/job/{jobDisplayId}/payment` | — | PaymentInfo | No |
| GET | `/job/{jobDisplayId}/payment/create` | — | PaymentInfo | No |
| GET | `/job/{jobDisplayId}/payment/sources` | — | List[PaymentSource] | No |
| POST | `/job/{jobDisplayId}/payment/bysource` | PayBySourceRequest | ServiceBaseResponse | No |
| POST | `/job/{jobDisplayId}/payment/ACHPaymentSession` | ACHSessionRequest | ACHSessionResponse | No |
| POST | `/job/{jobDisplayId}/payment/ACHCreditTransfer` | ACHCreditTransferRequest | ServiceBaseResponse | No |
| POST | `/job/{jobDisplayId}/payment/attachCustomerBank` | AttachBankRequest | ServiceBaseResponse | No |
| POST | `/job/{jobDisplayId}/payment/verifyJobACHSource` | VerifyACHRequest | ServiceBaseResponse | No |
| POST | `/job/{jobDisplayId}/payment/cancelJobACHVerification` | — | ServiceBaseResponse | No |
| POST | `/job/{jobDisplayId}/payment/banksource` | BankSourceRequest | ServiceBaseResponse | No |

### Forms (15)

| Method | Path | Request Model | Response Model | Schema Reliable |
|--------|------|---------------|----------------|-----------------|
| GET | `/job/{jobDisplayId}/form/invoice` | — | bytes | No |
| GET | `/job/{jobDisplayId}/form/invoice/editable` | — | bytes | No |
| GET | `/job/{jobDisplayId}/form/bill-of-lading` | — (query params) | bytes | No |
| GET | `/job/{jobDisplayId}/form/packing-slip` | — | bytes | No |
| GET | `/job/{jobDisplayId}/form/customer-quote` | — | bytes | No |
| GET | `/job/{jobDisplayId}/form/quick-sale` | — | bytes | No |
| GET | `/job/{jobDisplayId}/form/operations` | — (query params) | bytes | No |
| GET | `/job/{jobDisplayId}/form/shipments` | — | List[FormsShipmentPlan] | No |
| GET | `/job/{jobDisplayId}/form/address-label` | — | bytes | No |
| GET | `/job/{jobDisplayId}/form/item-labels` | — | bytes | No |
| GET | `/job/{jobDisplayId}/form/packaging-labels` | — | bytes | No |
| GET | `/job/{jobDisplayId}/form/packaging-specification` | — | bytes | No |
| GET | `/job/{jobDisplayId}/form/credit-card-authorization` | — | bytes | No |
| GET | `/job/{jobDisplayId}/form/usar` | — | bytes | No |
| GET | `/job/{jobDisplayId}/form/usar/editable` | — | bytes | No |

### Notes (4)

| Method | Path | Request Model | Response Model | Schema Reliable |
|--------|------|---------------|----------------|-----------------|
| GET | `/job/{jobDisplayId}/note` | — (query params) | List[JobNote] | No |
| POST | `/job/{jobDisplayId}/note` | JobNoteCreateRequest | JobNote | No |
| GET | `/job/{jobDisplayId}/note/{id}` | — | JobNote | No |
| PUT | `/job/{jobDisplayId}/note/{id}` | JobNoteUpdateRequest | JobNote | No |

### Items & Parcels (7)

| Method | Path | Request Model | Response Model | Schema Reliable |
|--------|------|---------------|----------------|-----------------|
| GET | `/job/{jobDisplayId}/parcelitems` | — | List[ParcelItem] | No |
| POST | `/job/{jobDisplayId}/parcelitems` | ParcelItemCreateRequest | ParcelItem | No |
| DELETE | `/job/{jobDisplayId}/parcelitems/{parcelItemId}` | — | ServiceBaseResponse | No |
| GET | `/job/{jobDisplayId}/parcel-items-with-materials` | — | List[ParcelItemWithMaterials] | No |
| GET | `/job/{jobDisplayId}/packagingcontainers` | — | List[PackagingContainer] | No |
| PUT | `/job/{jobDisplayId}/item/{itemId}` | ItemUpdateRequest | ServiceBaseResponse | No |
| POST | `/job/{jobDisplayId}/item/notes` | ItemNotesRequest | ServiceBaseResponse | No |

## Schema Reliability Summary

| Rating | Count | Action |
|--------|-------|--------|
| Reliable | 0 | N/A — all ACPortal endpoints lack reliable schemas |
| Not reliable | 62 | Model from fixture only, document swagger deviation |

All 62 endpoints are on the ACPortal surface, which has the least reliable swagger schemas. Models will be built primarily from captured fixtures, with swagger used only as initial guidance.

## Route Definition Convention

Same as feature 001:

```python
Route(
    method="GET",
    path="/job/{jobDisplayId}/timeline",
    response_model="List[TimelineTask]",
)
```

Route is frozen (immutable). Use `route.bind(jobDisplayId=display_id)` to create a bound copy with params applied.

For binary endpoints:

```python
Route(
    method="GET",
    path="/job/{jobDisplayId}/form/invoice",
    response_model="bytes",
)
```
