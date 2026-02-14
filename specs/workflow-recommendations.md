# Workflow & Artifact Recommendations

**Date**: 2026-02-14
**Scope**: DISCOVER.md restructure, ABConnectTools reference integration, artifact improvements

---

## 1. DISCOVER.md: Restructure Around a Single Source of Truth

### Problem

The current DISCOVER.md re-runs discovery every batch cycle. Phase D ("Discover")
asks the agent to compare swagger endpoints vs implemented endpoints and produce a
gap list, but this work is repeated each time a new batch starts. The endpoint
surface is static — swagger specs don't change between batches.

### Recommendation

Split DISCOVER.md into two concerns:

**A. API Surface Reference** (new file, written once, maintained incrementally)
**B. Implementation Workflow** (DISCOVER.md, simplified — drops Phase D)

#### A. New File: `specs/api-surface.md`

A single canonical listing of the full API surface. Structure:

```
## API Surfaces

### ACPortal
- Base URL: `https://portal.{env}.abconnect.co/api/api`
- Auth: Bearer JWT via /token endpoint
- Swagger: `ab/api/schemas/acportal.json` (unreliable — treat as hint)

### Catalog
- Base URL: `https://catalog-api.{env}.abconnect.co/api`
- Auth: Same JWT
- Swagger: `ab/api/schemas/catalog.json` (reliable)

### ABC
- Base URL: `https://api.{env}.abconnect.co/api`
- Auth: Same JWT
- Swagger: `ab/api/schemas/abc.json` (mostly reliable)

## Endpoint Groups

| Group | API | Endpoints | AB Status | ABConnectTools Status | Notes |
|-------|-----|-----------|-----------|----------------------|-------|
| Account | ACPortal | 10 | — | Full | Low priority (auth flows) |
| Address | ACPortal | 4 | 2 done | Full | Staging returns 204 |
| Admin | ACPortal | 12 | — | Full | Internal admin only |
| Commodity | ACPortal | 5 | — | Full | |
| CommodityMap | ACPortal | 5 | — | Full | |
| Companies | ACPortal | 30 | 8 done | Full (30) | Extend with brands, settings, hierarchy |
| Contacts | ACPortal | 14 | 7 done | Full (14) | Extend with merge, history |
| Dashboard | ACPortal | 10 | — | Full | Has working fixtures |
| Documents | ACPortal | 7 | 4 done | Full | |
| E-Sign | ACPortal | 3 | — | Partial | |
| Email | ACPortal | 2 | — | Partial | Job-scoped |
| Jobs (core) | ACPortal | ~99 | 26 done | Full (99) | Split into sub-groups below |
| ├─ Timeline | ACPortal | 9 | 9 (002) | Full | |
| ├─ Shipments | ACPortal | 14 | 14 (002) | Full | |
| ├─ Payments | ACPortal | 10 | 10 (002) | Full | |
| ├─ Forms | ACPortal | 15 | 15 (002) | Full (15 PDF fixtures!) |
| ├─ Notes | ACPortal | 4 | 4 (002) | Full | |
| ├─ Parcels | ACPortal | 7 | 7 (002) | Full | |
| ├─ Tracking | ACPortal | 2 | 2 (002) | Full | |
| ├─ OnHold | ACPortal | 8 | — | Full | |
| ├─ RFQ | ACPortal | 7 | — | Full | |
| ├─ SMS | ACPortal | 4 | — | Full | |
| ├─ FreightProviders | ACPortal | 3 | — | Full | |
| ├─ Email (job) | ACPortal | 5 | — | Full | |
| ├─ IntAcct | ACPortal | 5 | — | Full | |
| JobIntAcct | ACPortal | 5 | — | Full | |
| Lookup | ACPortal | 15 | 4 done | Full | Many staging gaps |
| Note (top-level) | ACPortal | 4 | — | Full | Separate from job notes |
| Notifications | ACPortal | 1 | — | Full | Has fixture |
| Partner | ACPortal | 2 | — | Full | Has fixture |
| Reports | ACPortal | 8 | — | Full | |
| RFQ | ACPortal | 7 | — | Full | |
| Shipment (global) | ACPortal | 3 | — | Full | Has fixture (accessorials) |
| SmsTemplate | ACPortal | 6 | — | Full | Has 3 fixtures |
| Users | ACPortal | 5 | 4 done | Full | |
| V2 (tracking) | ACPortal | 1 | — | Full | Superseded by v3 |
| V3 (tracking) | ACPortal | 1 | — | Full | |
| Values | ACPortal | 1 | — | Full | Has fixture |
| Views | ACPortal | 8 | — | Full | Has 3 fixtures |
| Webhooks | ACPortal | 5 | — | Full | Inbound hooks |
| Catalog (all) | Catalog | 17 | 17 done | — | 100% complete |
| ABC (partial) | ABC | 12 | 7 done | Partial | |
```

Each row has a definitive count. No re-discovery needed — just pick the next
group and start at Phase I.

#### B. Simplified DISCOVER.md

Remove Phase D. The workflow becomes **I-S-C-O-V-E-R** (7 phases). Phase D is
replaced by a simple lookup: "check `specs/api-surface.md` for the target group,
read the ABConnectTools reference column, then start implementing."

Add a new **Phase R** (Reference Scan) before Phase I:

```
### R — Reference Scan (replaces D)

**Entry**: Target group selected from api-surface.md.
**Action**:
1. Read ABConnectTools routes for the group:
   `/usr/src/pkgs/ABConnectTools/ABConnect/api/routes.py` (SCHEMA["{GROUP}"])
2. Read ABConnectTools models:
   `/usr/src/pkgs/ABConnectTools/ABConnect/api/models/{service}.py`
3. Read ABConnectTools endpoint implementation:
   `/usr/src/pkgs/ABConnectTools/ABConnect/api/endpoints/{service}.py`
4. Read ABConnectTools fixtures (if any):
   `/usr/src/pkgs/ABConnectTools/tests/fixtures/{Name}.json|pdf`
5. Read ABConnectTools examples (if any):
   `/usr/src/pkgs/ABConnectTools/examples/api/{service}.py`
6. Note field patterns, model names, edge cases, known API quirks.
**Exit**: Understanding of legacy patterns. No code written — reference only.
**Artifact**: None required (mental model). Optionally note deviations in
  the feature's research.md.
```

---

## 2. ABConnectTools Reference Inventory

### What It Has That We Should Look At (Not Copy)

ABConnectTools at `/usr/src/pkgs/ABConnectTools/` is a mature implementation
covering the same API surface. It provides:

#### 2a. Complete Route Map (399 lines)

**File**: `ABConnect/api/routes.py`

30 route groups with every endpoint defined as a `Route(method, path,
request_model, response_model)` dataclass. This is the single best
reference for "what endpoints exist" — more reliable than swagger for
ACPortal.

**Groups** (with route counts):

| Group | Routes | Our AB Equivalent | Gap |
|-------|--------|-------------------|-----|
| ACCOUNT | 10 | — | 10 |
| ADDRESS | 4 | address.py (2) | 2 |
| ADMIN | 12 | — | 12 |
| COMMODITY | 5 | — | 5 |
| COMMODITY_MAP | 5 | — | 5 |
| COMPANIES | 30 | companies.py (8) | 22 |
| COMPANY | 22 | (merged into companies) | 22 |
| CONTACTS | 14 | contacts.py (7) | 7 |
| DASHBOARD | 10 | — | 10 |
| DOCUMENTS | 7 | documents.py (4) | 3 |
| E_SIGN | 3 | — | 3 |
| EMAIL | 2 | — | 2 |
| JOB | 99 | jobs.py (26) | 73 |
| JOBINTACCT | 5 | — | 5 |
| LOOKUP | 15 | lookup.py (4) | 11 |
| NOTE | 4 | — | 4 |
| NOTIFICATIONS | 1 | — | 1 |
| PARTNER | 2 | — | 2 |
| REPORTS | 8 | — | 8 |
| RFQ | 7 | — | 7 |
| SHIPMENT | 3 | — | 3 |
| SMSTEMPLATE | 6 | — | 6 |
| USERS | 5 | users.py (4) | 1 |
| V2 | 1 | — | 1 |
| V3 | 1 | — | 1 |
| VALUES | 1 | — | 1 |
| VIEWS | 8 | — | 8 |
| WEBHOOKS | 5 | — | 5 |

**Recommendation**: Use `routes.py` as the authoritative source for
`specs/api-surface.md`. It's been validated against the real API, unlike
swagger.

#### 2b. Fixtures: 30 JSON + 15 PDF

**Path**: `ABConnectTools/tests/fixtures/`

**JSON fixtures we don't have** (and should reference for field patterns):

| Fixture | Group | Use Case |
|---------|-------|----------|
| `AccountProfile.json` | Account | Profile response shape |
| `ChangeAgent_OA.json` | Jobs | Agent change response |
| `CompanyBrands.json` | Companies | Brand tree structure |
| `CompanyBrandsTree.json` | Companies | Nested brand hierarchy |
| `CompanyGeoAreaCompanies.json` | Companies | Geo-area filtering |
| `CompanySearch_Training.json` | Companies | Search result shape |
| `Dashboard.json` | Dashboard | Dashboard response |
| `DashboardData.json` | Dashboard | Dashboard data payload |
| `DashboardGridViews.json` | Dashboard | Grid view config |
| `LookupAccessKeys.json` | Lookup | Access key structure |
| `LookupDensityClassMap.json` | Lookup | Density class map |
| `LookupDocumentTypes.json` | Lookup | Document type enum |
| `LookupParcelPackageTypes.json` | Lookup | Package type enum |
| `Notifications.json` | Notifications | Notification response |
| `PartnerList.json` | Partner | Partner list shape |
| `ShipmentAccessorials.json` | Shipment | Global accessorial list |
| `SmsTemplateJobStatuses.json` | SmsTemplate | Job status list |
| `SmsTemplateList.json` | SmsTemplate | Template list shape |
| `SmsTemplateNotificationTokens.json` | SmsTemplate | Token groups |
| `UsersPocUsers.json` | Users | POC user list |
| `Values.json` | Values | Values response |
| `ViewsAll.json` | Views | All grid views |
| `ViewsDatasetSps.json` | Views | Stored proc columns |

**PDF fixtures** (all forms — proves correct binary endpoints):

```
AddressLabel.pdf    BOL_Delivery.pdf     BOL_House.pdf
BOL_LTL.pdf         BOL_PickUp.pdf       CreditCardAuth.pdf
CustomerQuote.pdf    Invoice.pdf          ItemLabels.pdf
Operations_type0.pdf Operations_type1.pdf PackagingSpec.pdf
PackingSlip.pdf      QuickSale.pdf        USAR.pdf
```

**Recommendation**: During Phase C (Capture Fixtures), when staging data is
unavailable, reference ABConnectTools fixtures to understand response shapes.
Do NOT copy the files — capture fresh from staging. But use them to:
- Validate our Pydantic model field names and types
- Understand nested object structures
- Identify fields swagger omits
- Confirm binary response content types

#### 2c. Models: 51 Files

**Path**: `ABConnect/api/models/`

Key model files we should reference when implementing new groups:

| ABConnectTools Model | AB Equivalent | Reference Value |
|---------------------|---------------|-----------------|
| `jobtimeline.py` | `jobs.py` (partial) | TimelineTask, CarrierTask, TimelineResponse field shapes |
| `jobshipment.py` | `shipments.py` | ShipmentOriginDestination, JobCarrierRatesModel nesting |
| `jobpayment.py` | `payments.py` | PaymentSourceDetails, ACH flow models |
| `jobform.py` | `forms.py` | FormsShipmentPlan, USAREditableFormResponseModel |
| `jobnote.py` | `jobs.py` (partial) | JobTaskNote field names, alias patterns |
| `jobparcelitems.py` | `jobs.py` (partial) | ParcelItemWithPackage, Packaging |
| `jobtracking.py` | `shipments.py` (partial) | ShipmentTrackingDetails |
| `jobtrackingv3.py` | `shipments.py` (partial) | JobTrackingResponseV3 |
| `jobonhold.py` | — | OnHoldDetails, SaveOnHoldRequest (future) |
| `jobemail.py` | — | SendDocumentEmailModel (future) |
| `jobfreightproviders.py` | — | PricedFreightProvider (future) |
| `jobintacct.py` | — | CreateJobIntacctModel (future) |
| `jobsms.py` | — | SendSMSModel (future) |
| `jobsmstemplate.py` | — | SmsTemplateModel (future) |
| `dashboard.py` | — | Dashboard response models (future) |
| `reports.py` | — | Report request/response models (future) |
| `rfq.py` | — | QuoteRequestDisplayInfo (future) |
| `shipment.py` | — | ShipmentDetails, ParcelAddOn (future) |
| `enums.py` | `enums.py` | Comprehensive enum definitions |
| `shared.py` | `shared.py` | ServiceBaseResponse, ServiceWarningResponse |
| `planner.py` | — | Planner models (future) |

**Recommendation**: Before writing any new model file, read the ABConnectTools
equivalent. Note:
- Field names and aliases (ABConnectTools has been validated against real data)
- Optional vs required fields (ABConnectTools has real-world experience here)
- Nested model relationships
- Enum values used in practice

Then implement clean-room in AB with our stricter standards:
- `RequestModel(extra="forbid")` / `ResponseModel(extra="allow")`
- Mixin-based inheritance
- Drift logging for unexpected fields

#### 2d. Endpoint Implementations: 31 Files

**Path**: `ABConnect/api/endpoints/`

Notable structural difference: ABConnectTools splits `jobs/` into 22 sub-files:

```
jobs/
├── job.py              # Core CRUD
├── timeline.py         # Timeline endpoints
├── timeline_helpers.py # Business logic helpers
├── tracking.py         # Tracking endpoints
├── shipment.py         # Shipment endpoints
├── ship_helpers.py     # Shipping business logic
├── payment.py          # Payment endpoints
├── form.py             # Form endpoints
├── form_helpers.py     # Form business logic
├── note.py             # Note endpoints
├── parcelitems.py      # Parcel item endpoints
├── items_helpers.py    # Item business logic
├── onhold.py           # On-hold endpoints
├── rfq.py              # RFQ endpoints
├── sms.py              # SMS endpoints
├── email.py            # Email endpoints
├── freightproviders.py # Freight provider endpoints
├── intacct.py          # IntAcct endpoints
├── status.py           # Status management
└── agent_helpers.py    # Agent assignment helpers
```

**Our AB approach**: We keep a single `jobs.py` with methods grouped by concern,
plus separate files when a group exceeds ~10 methods (forms.py, shipments.py,
payments.py). This is cleaner but we should watch the file size of `jobs.py` as
more sub-groups are added.

**Recommendation**: When `jobs.py` exceeds ~300 lines or ~30 methods, consider
splitting. Current state: 205 lines / 26 methods. The ABConnectTools split
pattern is a reasonable guide for where the seams are, but we should not adopt
the `_helpers.py` pattern — those contain business logic that belongs in
consuming applications, not the SDK.

#### 2e. Examples: 22 Files

**Path**: `ABConnect/examples/api/`

```
accounts.py     agent.py        catalog_api.py   companies.py
contacts.py     dashboard.py    documents.py     forms.py
items.py        items_helper.py lookup.py        misc_endpoints.py
note.py         notes.py        ship.py          smstemplate.py
SmsTemplate.py  tasks.py        views.py
_base.py        _constants.py   _helpers.py
```

**Recommendation**: Reference these for realistic usage patterns when writing
our `examples/*.py` files. Their examples show real parameter values, typical
call sequences, and error handling patterns that are hard to derive from
swagger alone.

---

## 3. Proposed DISCOVER.md Structure (v2)

```
# DISCOVER Workflow v2

## API Surface Reference
→ See specs/api-surface.md for the complete endpoint inventory.
  Pick the next group from there. Do not re-derive from swagger.

## Phases: R-I-S-C-O-V-E-R

### R — Reference Scan (NEW)
Read ABConnectTools for the target group. Note patterns, do not copy.

### I — Implement Models
Create Pydantic models. Cross-reference ABConnectTools model file.

### S — Scaffold Endpoints
Write endpoint methods. Cross-reference ABConnectTools endpoint file.

### C — Capture Fixtures (Human Required)
Capture real data from staging. Reference ABConnectTools fixtures for
expected shapes if staging data is scarce.

### O — Observe Tests
Run tests, check harmony.

### V — Verify & Commit
Checkpoint commit.

### E — Examples & Docs
Reference ABConnectTools examples for realistic usage patterns.

### R — Release
PR ready.
```

Key changes:
- **Phase D removed** — replaced by static `api-surface.md`
- **Phase R (Reference) added** — structured ABConnectTools scan
- **ABConnectTools paths documented** in each phase where relevant
- **Batch planning** draws from `api-surface.md` table, not swagger parsing

---

## 4. Specific ABConnectTools Cross-Reference Opportunities

### 4a. Fixtures We Can Validate Against (Not Copy)

Our 27 pending fixtures overlap with ABConnectTools captured data. For each,
we should reference the ABConnectTools fixture to understand the expected
response shape, then capture fresh from staging:

| Our Pending Fixture | ABConnectTools Has | Reference Path |
|--------------------|--------------------|---------------|
| Timeline models | No JSON (but working code) | `models/jobtimeline.py` |
| Shipment accessorials | `ShipmentAccessorials.json` | `tests/fixtures/ShipmentAccessorials.json` |
| Payment models | No JSON (but working code) | `models/jobpayment.py` |
| Form PDFs | All 15 PDFs captured | `tests/fixtures/*.pdf` |
| Tracking models | No JSON (but working code) | `models/jobtracking.py`, `jobtrackingv3.py` |

### 4b. New Endpoint Groups to Prioritize (ABConnectTools Has Fixtures)

These groups have working fixtures in ABConnectTools, making them faster
to implement in AB because we can validate model shapes immediately:

| Group | ABConnectTools Fixtures | Est. Effort |
|-------|------------------------|-------------|
| Dashboard | 3 JSON | Medium (10 endpoints) |
| SmsTemplate | 3 JSON | Low (6 endpoints) |
| Views | 3 JSON | Medium (8 endpoints) |
| Partner | 1 JSON | Low (2 endpoints) |
| Notifications | 1 JSON | Low (1 endpoint) |
| Values | 1 JSON | Low (1 endpoint) |
| Shipment (global) | 1 JSON | Low (3 endpoints) |
| Lookup (extended) | 4 more JSON | Low (11 more endpoints) |

### 4c. Model Patterns Worth Studying

ABConnectTools has solved several patterns we'll need:

1. **`ServiceWarningResponse`** — extends `ServiceBaseResponse` with warning
   field. We have `ServiceBaseResponse` but not the warning variant.

2. **`USAREditableFormResponseModel`** — ABConnectTools has a JSON model for
   editable form endpoints (`/form/invoice/editable`, `/form/usar/editable`).
   We treat all forms as binary. Should we add these two JSON variants?

3. **Route-level `response_model` as string** — ABConnectTools uses string
   references (`"List[CompanySimple]"`) rather than actual types. Our AB
   project uses actual model classes. Both work, but theirs allows lazy
   resolution while ours catches import errors early.

4. **`COMPANY` vs `COMPANIES`** — ABConnectTools has both as separate route
   groups (COMPANIES = list/search, COMPANY = single-entity CRUD). We merged
   them. Their split may be worth understanding for the 22 COMPANY routes
   we haven't implemented.

---

## 5. Artifact Improvement Summary

| Current | Recommendation | Why |
|---------|---------------|-----|
| DISCOVER.md Phase D rediscovers each batch | Create `specs/api-surface.md` once, remove Phase D | Eliminates redundant swagger parsing |
| No structured ABConnectTools reference step | Add Phase R (Reference Scan) with specific file paths | Ensures we learn from legacy before implementing |
| Batch order guessed from swagger | Batch order driven by `api-surface.md` + ABConnectTools fixture availability | Prioritize groups where validation is easiest |
| FIXTURES.md lists only our captures | Add column for ABConnectTools reference fixture | Quick lookup for shape validation |
| research.md per feature | Add ABConnectTools cross-reference section to research template | Systematic pattern comparison |
| `jobs.py` growing unbounded | Monitor line count; split at ~300 lines following ABConnectTools seams | Prevent unwieldy files |
| Forms treated as all-binary | Investigate `/form/invoice/editable` and `/form/usar/editable` (JSON) | ABConnectTools has distinct model for these |

---

## 6. Files to Create/Modify

### Create
- `specs/api-surface.md` — master endpoint inventory (build from ABConnectTools `routes.py` + our swagger specs)

### Modify
- `.claude/workflows/DISCOVER.md` — remove Phase D, add Phase R, reference `api-surface.md`
- `FIXTURES.md` — add ABConnectTools reference column
- `.specify/templates/` — add ABConnectTools cross-reference section to research template

### No Changes Needed
- Constitution — principles are sound, workflow change is operational not philosophical
- AGENTS.md — already correct
- CLAUDE.md — auto-generated, will update when plan changes
