# Data Model: G1 Model Fidelity Sweep

**Feature**: 034-g1-model-fidelity-sweep
**Date**: 2026-03-15

## Entity: ServiceBaseResponse (expansion)

**Location**: `ab/api/models/shared.py`
**Base class**: `ResponseModel`
**Used by**: 21 endpoints across payments, shipments, timeline, jobs, commodity-maps, views

### Current Fields (3)

| Python Name | Alias | Type | Description |
|-------------|-------|------|-------------|
| `success` | — | `Optional[bool]` | Whether operation succeeded |
| `error_message` | `errorMessage` | `Optional[str]` | Error detail |
| `job_sub_management_status` | `jobSubManagementStatus` | `Optional[dict]` | Job sub-management status |

### New Fields (13)

| Python Name | Alias | Type | Description | Fixture Evidence |
|-------------|-------|------|-------------|------------------|
| `documents` | `documents` | `Optional[List[str]]` | Document URLs/refs from operation | `[]` |
| `errors` | `errors` | `Optional[dict]` | Detailed error object | `null` |
| `confirm_required` | `confirmRequired` | `Optional[bool]` | User confirmation needed | `false` |
| `notifications` | `notifications` | `Optional[List[str]]` | Notification messages | `[]` |
| `shipment_id` | `shipmentId` | `Optional[str]` | Shipment UUID | `null` |
| `shipment_accept_identifier` | `shipmentAcceptIdentifier` | `Optional[str]` | Carrier acceptance ref | `null` |
| `weight` | `weight` | `Optional[ShipmentWeight]` | Weight details (nested) | `{pounds: 0.0, ...}` |
| `total_net_charge_amount` | `totalNetChargeAmount` | `Optional[float]` | Total charge amount | `0.0` |
| `currency_code` | `currencyCode` | `Optional[str]` | Currency code (e.g., USD) | `null` |
| `international_info_required` | `internationalInfoRequired` | `Optional[bool]` | Intl info flag | `false` |
| `ship_out_date_required` | `shipOutDateRequired` | `Optional[bool]` | Ship date confirmation flag | `false` |
| `fed_ex_express_freight_detail_required` | `fedExExpressFreightDetailRequired` | `Optional[bool]` | FedEx freight details flag | `false` |
| `carrier_api` | `carrierAPI` | `Optional[int]` | Carrier API type code | `0` |

### Relationships

- `ServiceBaseResponse.weight` → `ShipmentWeight` (existing model in `ab/api/models/shipments.py:116`)
- `ServiceWarningResponse` inherits from `ServiceBaseResponse` — inherits all new fields automatically

### Validation Rules

- All new fields `Optional` with `None` default (backward compatible)
- `weight` uses existing `ShipmentWeight` model (3 fields: pounds, originalWeight, originalWeightMeasureUnit)
- No `extra="forbid"` (ResponseModel uses `extra="allow"` per constitution)

## Entity: ShipmentWeight (existing, no changes)

**Location**: `ab/api/models/shipments.py:116`
**Reused by**: `ServiceBaseResponse.weight`

| Python Name | Alias | Type |
|-------------|-------|------|
| `pounds` | — | `Optional[float]` |
| `original_weight` | `originalWeight` | `Optional[float]` |
| `original_weight_measure_unit` | `originalWeightMeasureUnit` | `Optional[str]` |

## Affected Endpoints (21)

All share `response_model="ServiceBaseResponse"`:

| Group | Endpoint | Method |
|-------|----------|--------|
| Jobs | `/job/{_}/changeAgent` | POST |
| Jobs | `/job/{_}/item/notes` | POST |
| Jobs | `/job/{_}/item/{_}` | PUT |
| Jobs | `/job/{_}/parcelitems/{_}` | DELETE |
| Jobs | `/job/{_}/status/quote` | POST |
| Jobs | `/job/{_}/timeline/incrementjobstatus` | POST |
| Jobs | `/job/{_}/timeline/undoincrementjobstatus` | POST |
| Jobs | `/job/{_}/timeline/{_}` | DELETE |
| Payments | `/job/{_}/payment/ACHCreditTransfer` | POST |
| Payments | `/job/{_}/payment/attachCustomerBank` | POST |
| Payments | `/job/{_}/payment/banksource` | POST |
| Payments | `/job/{_}/payment/bysource` | POST |
| Payments | `/job/{_}/payment/cancelJobACHVerification` | POST |
| Payments | `/job/{_}/payment/verifyJobACHSource` | POST |
| Shipments | `/job/{_}/shipment` | DELETE |
| Shipments | `/job/{_}/shipment/accessorial` | POST |
| Shipments | `/job/{_}/shipment/accessorial/{_}` | DELETE |
| Shipments | `/job/{_}/shipment/book` | POST |
| Shipments | `/job/{_}/shipment/exportdata` | POST |
| Commodity Maps | `/commodity-map/{_}` | DELETE |
| Views | `/views/{_}` | DELETE |

## No New Models Required

The `ShipmentWeight` model already exists and matches the fixture exactly. No new model classes needed beyond expanding `ServiceBaseResponse`.
