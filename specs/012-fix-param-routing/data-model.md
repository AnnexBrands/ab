# Data Model: Fix Parameter Routing

**Feature**: 012-fix-param-routing
**Date**: 2026-02-21

## New Entities

### Params Models (Query Parameter Validation)

These models extend `RequestModel` (extra="forbid") and define fields for endpoints that accept query string parameters. The `.check()` method validates input and returns a dict with aliased keys for HTTP transport.

#### AddressValidateParams

For `GET /address/isvalid` — all params are PascalCase in the swagger spec.

| Field | Type | Alias | Required | Description |
| ----- | ---- | ----- | -------- | ----------- |
| line1 | Optional[str] | Line1 | No | Street address line 1 |
| city | Optional[str] | City | No | City name |
| state | Optional[str] | State | No | State abbreviation |
| zip | Optional[str] | Zip | No | ZIP/postal code |

#### AddressPropertyTypeParams

For `GET /address/propertytype` — PascalCase params.

| Field | Type | Alias | Required | Description |
| ----- | ---- | ----- | -------- | ----------- |
| address1 | Optional[str] | Address1 | No | Street address line 1 |
| address2 | Optional[str] | Address2 | No | Street address line 2 |
| city | Optional[str] | City | No | City name |
| state | Optional[str] | State | No | State abbreviation |
| zip_code | Optional[str] | ZipCode | No | ZIP/postal code |

#### BillOfLadingParams

For `GET /job/{jobDisplayId}/form/bill-of-lading` — camelCase params.

| Field | Type | Alias | Required | Description |
| ----- | ---- | ----- | -------- | ----------- |
| shipment_plan_id | Optional[str] | shipmentPlanId | No | Shipment plan UUID |
| provider_option_index | Optional[int] | providerOptionIndex | No | Provider index |

#### OperationsFormParams

For `GET /job/{jobDisplayId}/form/operations` — single param.

| Field | Type | Alias | Required | Description |
| ----- | ---- | ----- | -------- | ----------- |
| ops_type | Optional[str] | type | No | Operations type filter |

#### DocumentListParams

For `GET /documents/list` — camelCase params.

| Field | Type | Alias | Required | Description |
| ----- | ---- | ----- | -------- | ----------- |
| job_display_id | Optional[str] | jobDisplayId | No | Job display ID filter |

### Tier 2: Params Models for Existing kwargs-params Endpoints

These endpoints currently pass `**kwargs` as `params=` without validation. Each needs a params model derived from the swagger spec. Models to be created during implementation based on swagger research for each endpoint:

- `GeoAreaCompaniesParams` — for `GET /companies/geoAreaCompanies`
- `CarrierAccountSearchParams` — for `GET /companies/search/carrier-accounts`
- `SuggestCarriersParams` — for `GET /companies/suggest-carriers`
- `DashboardParams` — for `GET /dashboard`
- `JobSearchParams` — for `GET /job/search` (if different from POST search)
- `JobNotesParams` — for `GET /job/{jobId}/notes`
- `FreightProvidersParams` — for `GET /job/{jobId}/freight-providers`
- `NotesListParams` — for `GET /notes`
- `NotesSuggestUsersParams` — for `GET /notes/suggest-users`
- `ShipmentParams` — for `GET /shipment/{id}`
- `Web2LeadGetParams` — for `GET /web2lead`

## Modified Entities

### Route (dataclass)

No structural changes. The existing `params_model: Optional[str]` field is activated — it transitions from "defined but unused" to "standard practice for query-param endpoints."

### EndpointGateStatus (dataclass)

New field for G5 gate:

| Field | Type | Description |
| ----- | ---- | ----------- |
| g5_param_routing | GateResult \| None | Result of parameter routing evaluation |

The `compute_overall()` method includes G5 in its gate check.

### GateResult (dataclass)

No structural changes. G5 uses the same `GateResult(gate="G5", passed=bool, reason=str)` pattern.

## Relationships

```
Route
├── params_model → ParamsModel class (validates query params)
├── request_model → RequestModel class (validates body params)
├── _path_params → frozenset[str] (extracted from path template)
└── response_model → ResponseModel class (validates response)

BaseEndpoint._request()
├── if route.params_model → check(params) → aliased dict → HttpClient.request(params=...)
├── if route.request_model → check(json) → aliased dict → HttpClient.request(json=...)
└── if route.response_model → model_validate(response) → typed object

EndpointGateStatus
├── g1_model_fidelity → GateResult
├── g2_fixture_status → GateResult
├── g3_test_quality → GateResult
├── g4_doc_accuracy → GateResult
└── g5_param_routing → GateResult (NEW)
```

## Validation Rules

1. **Params models** use `extra="forbid"` — unknown query param names raise ValidationError before HTTP call
2. **alias mapping** uses explicit `Field(alias=...)` for PascalCase params (Line1, City) and auto-generated aliases for standard camelCase (pageSize, jobDisplayId)
3. **exclude_none=True** — None-valued params excluded from query string
4. **exclude_unset=True** — default-valued but unset params excluded from query string
5. **populate_by_name=True** — callers can provide snake_case field names (Python convention)
