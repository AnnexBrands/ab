# Data Model: Fix FreightProviders Drift

**Feature**: 033-fix-freightproviders-drift
**Date**: 2026-03-15

## Entities

### CarrierAPI (Enum)

Integer enum representing the carrier API type used for freight quoting.

| Value | Meaning |
|-------|---------|
| 0–4, 6–12, 14, 20 | Carrier API identifiers (specific carrier integrations) |

**Used by**: PricedFreightProvider.providerAPI, ShipmentPlanProvider.usedAPI

### CarrierAccountInfo (Nested Response/Request Model)

Carrier account details embedded within freight provider objects.

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| id | int | No | Carrier account identifier |
| key | str | Yes | Account key |
| friendly_name | str | Yes | Human-readable account name |

**Used by**: PricedFreightProvider.usedCarrierAccountInfo, ShipmentPlanProvider.usedCarrierAccountInfo

### PricedFreightProvider (Response Model) — EXPAND

Current: 3 fields → Target: 15 fields + nested CarrierAccountInfo

| Field | Type | Nullable | Alias | Status |
|-------|------|----------|-------|--------|
| option_index | int | No | optionIndex | NEW |
| shipment_type | str | No | shipmentType | NEW |
| provider_api | CarrierAPI | No | providerAPI | NEW |
| provider_id | str | Yes | providerId | NEW |
| provider_code | str | Yes | providerCode | NEW |
| provider_company_name | str | Yes | providerCompanyName | RENAME (was provider_name) |
| total_sell | float | No | totalSell | NEW |
| transit | int | Yes | transit | NEW |
| quote_no | str | Yes | quoteNo | NEW |
| pro_num | str | Yes | proNum | NEW |
| option_active | bool | No | optionActive | NEW |
| shipment_accepted | bool | No | shipmentAccepted | NEW |
| shipment_accepted_date | str | Yes | shipmentAcceptedDate | NEW |
| obtain_nfm_job_state | str | Yes | obtainNFMJobState | NEW |
| used_carrier_account_info | CarrierAccountInfo | No | usedCarrierAccountInfo | NEW |

**Removed**: `provider_name` (renamed to `provider_company_name`), `service_types` (not in swagger — likely a fabricated field), `rate_available` (not in swagger — likely a fabricated field).

### ShipmentPlanProvider (Request Model) — EXPAND

Current: 1 field (`provider_data: dict`) → Target: 22+ typed fields

| Field | Type | Nullable | Alias | Status |
|-------|------|----------|-------|--------|
| job_id | str | Yes | jobID | NEW |
| freight_quote_options_id | str | Yes | freightQuoteOptionsId | NEW |
| provider_id | str | Yes | providerID | NEW |
| is_primary | bool | No | isPrimary | NEW |
| provider_company_code | str | Yes | providerCompanyCode | NEW |
| provider_company_name | str | Yes | providerCompanyName | NEW |
| original_company_name | str | Yes | originalCompanyName | NEW |
| freight_amount | float | No | freightAmount | NEW |
| accessorial_amount | float | No | accessorialAmount | NEW |
| caf_note | str | Yes | cafNote | NEW |
| quote_no | str | Yes | quoteNo | NEW |
| pro_num | str | Yes | proNum | NEW |
| transit | int | Yes | transit | NEW |
| shipment_type | str | Yes | shipmentType | NEW |
| miles | float | No | miles | NEW |
| logo | str | Yes | logo | NEW |
| option_index | int | No | optionIndex | NEW |
| option_active | bool | No | optionActive | NEW |
| shipment_accepted | bool | No | shipmentAccepted | NEW |
| shipment_accepted_date | str | Yes | shipmentAcceptedDate | NEW |
| used_api | CarrierAPI | No | usedAPI | NEW |
| bill_to_franchisee_id | str | Yes | billToFranchiseeId | NEW |
| bill_to_company_code | str | Yes | billToCompanyCode | NEW |
| obtain_nfm_job_state | str | Yes | obtainNFMJobState | NEW |
| used_carrier_account_info | CarrierAccountInfo | No | usedCarrierAccountInfo | NEW |

**Removed**: `provider_data: dict` (stub field, replaced by typed fields)

### RateQuoteRequest (Request Model) — NEEDS LIVE CAPTURE

Current: 1 field (`options: dict`). Swagger schema to be verified during implementation. Expand based on swagger or live capture findings.

### FreightItemsRequest (Request Model) — NEEDS LIVE CAPTURE

Current: 1 field (`items: List[dict]`). Expand based on swagger schema for the items array element type.

### FreightProvidersParams (Query Params Model) — KEEP

Current 3 fields are consistent with swagger. No changes needed.

| Field | Type | Nullable | Alias |
|-------|------|----------|-------|
| provider_indexes | List[int] | Yes | ProviderIndexes |
| shipment_types | List[str] | Yes | ShipmentTypes |
| only_active | bool | Yes | OnlyActive |

## Relationships

```
PricedFreightProvider
  └── usedCarrierAccountInfo: CarrierAccountInfo
  └── providerAPI: CarrierAPI (enum)

ShipmentPlanProvider
  └── usedCarrierAccountInfo: CarrierAccountInfo
  └── usedAPI: CarrierAPI (enum)
```

## Validation Rules

- **ResponseModel** (`extra="allow"`): PricedFreightProvider, CarrierAccountInfo (response variant) — unknown fields stored in `model_extra`, logged as warnings
- **RequestModel** (`extra="forbid"`): ShipmentPlanProvider, RateQuoteRequest, FreightItemsRequest, FreightProvidersParams — unknown fields raise `ValidationError`
- Non-nullable fields with primitive defaults (int=0, float=0.0, bool=False) should still be `Optional` in the model since real API behavior may differ from swagger declaration
