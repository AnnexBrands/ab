# Research: Harden Example Parameters Against Swagger

**Date**: 2026-02-14
**Branch**: `005-harden-example-params`

## Methodology

Audited all 19 example files against swagger schemas and ABConnectTools implementations. Only flagged mismatches where swagger clearly defines parameter names and types.

## Confirmed Mismatches

### R1. AddressEndpoint.validate() — Wrong Parameter Names

**Swagger** (GET `/api/address/isvalid`): query params `Line1`, `City`, `State`, `Zip` (all optional strings).

**Current SDK** (`ab/api/endpoints/address.py`):
- Python params: `street`, `city`, `state`, `zip_code`, `country`
- Maps to: `street`, `city`, `state`, `zipCode`, `country`

**ABConnectTools** (`ABConnect/api/endpoints/address.py`):
- Python params: `line1`, `city`, `state`, `zip`
- Maps to: `Line1`, `City`, `State`, `Zip` — matches swagger exactly.

**Verdict**: SDK maps to wrong API param names. `country` is fabricated (not in swagger, not in ABConnectTools).

**Fix**: Rename Python params to `line1`, `city`, `state`, `zip`. Map to `Line1`, `City`, `State`, `Zip`. Remove `country`.

---

### R2. AddressEndpoint.get_property_type() — Wrong + Missing Parameters

**Swagger** (GET `/api/address/propertytype`): query params `Address1`, `Address2` (optional), `City`, `State`, `ZipCode` (all optional strings).

**Current SDK**: Only accepts `street`, `zip_code`. Maps to `street`, `zipCode`.

**ABConnectTools**: Accepts `address1`, `address2`, `city`, `state`, `zip_code`. Maps to `Address1`, `Address2`, `City`, `State`, `ZipCode` — matches swagger exactly.

**Verdict**: SDK has 2 of 5 params, both with wrong API names.

**Fix**: Accept `address1`, `address2`, `city`, `state`, `zip_code`. Map to `Address1`, `Address2`, `City`, `State`, `ZipCode`.

---

### R3. FormsEndpoint.get_operations() — Wrong Parameter Name

**Swagger** (GET `/api/job/{jobDisplayId}/form/operations`): query param `type` (optional, schema `OperationsFormType`).

**Current SDK** (`ab/api/endpoints/forms.py`): Python param `ops_type`, maps to `opsType`.

**ABConnectTools** (`ABConnect/api/endpoints/jobs/form.py`): Python param `ops_type`, maps to `type` — matches swagger.

**Verdict**: SDK maps to `opsType` instead of `type`.

**Fix**: Change mapping from `opsType` to `type`. Keep Python param name `ops_type`.

---

### R4. ShipmentsEndpoint.request_rate_quotes() — params vs json

**Swagger** (POST `/api/job/{jobDisplayId}/shipment/ratequotes`): defines `requestBody` with schema `TransportationRatesRequestModel`.

**Current SDK** (`ab/api/endpoints/shipments.py`): Uses `params=params` (query string) instead of `json=data` (request body).

**ABConnectTools**: Uses `json=data` for POST body.

**Verdict**: Endpoint passes request body as query params instead of JSON body. Would fail if any body data is actually passed.

**Fix**: Change method signature to accept a `data` dict and pass via `json=data`.

---

## Not Flagged (swagger lacks clear info or implementation is correct)

- **jobs.search()** — `jobDisplayId` is optional in swagger. SDK uses `**params` which works. Could be more explicit but not wrong.
- **jobs.set_quote_status()** — Swagger shows no request body. SDK correctly omits it. ABConnectTools had an unnecessary optional body param.
- **documents.upload()** — Form-data field naming (PascalCase vs camelCase) may be server-flexible. No clear evidence of failure from swagger alone.
- **Pagination params** (catalog, lots, sellers) — All correctly mapped.
- **All other endpoints** — 14 example files with ~80 method calls verified correct.

## Alternatives Considered

- **Option A**: Fix only examples, leave endpoint methods unchanged.
  - Rejected: The mismatches originate in the endpoint layer. Fixing only examples would mean the SDK methods still send wrong params to the API.

- **Option B**: Fix endpoints + examples, no automated guard.
  - Rejected: Without a guard test, drift will recur as new endpoints are added.

- **Option C (chosen)**: Fix endpoints + examples + add automated validation test.
  - Rationale: Addresses root cause and prevents recurrence. The validation test cross-references endpoint param mappings against swagger.
