# Research: Remaining API Endpoints (009)

**Date**: 2026-02-14
**Branch**: `009-remaining-endpoints`

## Corrected Coverage Numbers

The original project-state.md estimated ~149 ACPortal + ~5 ABC remaining. Precise swagger-vs-implementation analysis yields:

| API | Swagger Total | Implemented | Remaining |
|-----|--------------|-------------|-----------|
| ACPortal | 299 | 204 | **95** |
| ABC | 12 | 5 | **7** |
| Catalog | 17 | 17 | 0 |
| **Total** | **328** | **226** | **102** |

The discrepancy (149 → 95 ACPortal) is because the project-state.md counted some groups twice and included estimated counts from a preliminary scan rather than a precise swagger diff.

## ACPortal Gap Analysis (95 endpoints, 30 swagger tags)

### Group 1: Company Operations (26 endpoints — `/api/company/{companyId}/*`)

These all share the `/api/company/{companyId}/` prefix (note: singular, vs the existing `/api/companies/` plural). ABConnectTools implements all in a single `company.py` file.

| Tag | Count | Endpoints |
|-----|-------|-----------|
| Calendar | 4 | calendar/{date}, calendar/{date}/baseinfo, startofday, endofday |
| Company External Accounts | 3 | accounts/stripe/connecturl (GET), completeconnection (POST), stripe (DELETE) |
| CompanyDocumentTemplates | 4 | document-templates CRUD |
| CompanySettings | 3 | gridsettings GET/POST, setupdata GET |
| ContainerThicknessInches | 3 | CRUD (GET list, POST create, DELETE) |
| Material | 4 | CRUD (GET list, POST, PUT, DELETE) |
| Truck | 4 | CRUD (GET list, POST, PUT, DELETE) |
| Planner | 1 | planner GET |

**ABConnectTools reference**: `company.py` — 22 methods covering all of these. Simple REST patterns, no special headers or pagination. Delete endpoints use query params for IDs in some cases (e.g., `containerId` on delete containerThicknessInches). Truck GET accepts `onlyOwnTrucks` query param. Calendar endpoints take `{date}` as URL param (format: YYYY-MM-DD). Stripe connecturl takes `returnUri` query param.

**SDK file**: New `company.py` (or `company_setup.py` to avoid confusion with `companies.py`)

### Group 2: Admin & Settings (13 endpoints — `/api/admin/*`)

| Tag | Count | Endpoints |
|-----|-------|-----------|
| AdvancedSettings | 4 | CRUD (GET all, GET by id, POST, DELETE) |
| CarrierErrorMessage | 2 | GET all, POST |
| GlobalSettings | 5 | companyhierarchy, companyhierarchy/company/{id}, getinsuranceexceptions, approveinsuranceexception, intacct |
| LogBuffer | 2 | flush, flushAll |

**ABConnectTools reference**: `admin.py` — 13 methods. All simple REST. `approveinsuranceexception` takes `JobId` query param on POST. `getinsuranceexceptions` and `intacct` accept JSON body on POST. `logbuffer/flush` accepts optional JSON body; `flushAll` takes no args.

**SDK file**: New `admin.py`

### Group 3: Account (10 endpoints — `/api/account/*`)

| Endpoint | Method |
|----------|--------|
| register | POST (json body) |
| sendConfirmation | POST (json body) |
| confirm | POST (json body) |
| forgot | POST (json body) |
| verifyresettoken | GET (query: username, token) |
| resetpassword | POST (json body) |
| setpassword | POST (json body) |
| profile | GET (no params) |
| paymentsource/{sourceId} | PUT (json body), DELETE |

**ABConnectTools reference**: `account.py` — 10 methods. Standard REST patterns. `verifyresettoken` uses query params `username` and `token`. Payment source methods take `sourceId` as URL path param.

**SDK file**: New `account.py`

### Group 4: Extended Jobs (12 endpoints — `/api/job/*`)

| Tag | Count | Endpoints |
|-----|-------|-----------|
| Job | 8 | documentConfig (GET), feedback GET/POST, jobAccessLevel (GET), transfer (POST), changeAgent (POST), copy (POST), submanagementstatus (GET) |
| JobBooking | 1 | book (POST) |
| JobTracking | 1 | tracking/shipment/{proNumber} (GET) |
| JobTrackingV2 | 1 | v2 tracking (GET) |
| Email | 1 | email/{jobDisplayId}/labelrequest (POST) |

**ABConnectTools reference**: Distributed across `jobs/job.py`, `jobs/tracking.py`, `jobs/email.py`. Standard patterns — URL params for `{jobDisplayId}`, JSON bodies for POST.

**SDK file**: Extend existing `jobs.py` (continues D2 decision from 008)

### Group 5: Integration Endpoints (13 endpoints)

| Tag | Count | Endpoints | SDK File |
|-----|-------|-----------|----------|
| JobIntacct | 5 | GET, POST, draft, applyRebate, DELETE (all by jobDisplayId) | New `intacct.py` |
| JobSign | 2 | e-sign/result (GET, query: envelope, event), e-sign/{jobDisplayId}/{bookingKey} (GET) | New `esign.py` |
| StripeWebhook | 3 | stripe/handle, stripe/connect/handle, stripe/checkout.session.completed | New `webhooks.py` |
| TwilioWebhook | 3 | twilio/body-sms-inbound, form-sms-inbound, smsStatusCallback | (in `webhooks.py`) |

**ABConnectTools reference**:
- `jobintacct.py` — 5 methods. `applyRebate` takes JSON body. DELETE uses `{franchiseeId}` path param.
- `e_sign.py` — 2 methods. `result` uses query params `envelope`, `event`.
- `webhooks.py` — 4 methods (3 stripe + 1 twilio). Webhook handlers mostly take no request body (Stripe sends via headers/raw body). `smsStatusCallback` accepts JSON body.

### Group 6: Communication & Misc (8 endpoints)

| Tag | Count | Endpoints | SDK File |
|-----|-------|-----------|----------|
| JobSmsTemplate | 5 | list (GET), notificationTokens (GET), save (POST), GET/{id}, DELETE/{id} | New `sms_templates.py` |
| Notifications | 1 | GET /api/notifications | New `notifications.py` |
| Users | 1 | GET /api/users/pocusers | Extend `users.py` |
| Values | 1 | GET /api/Values (health/test) | New or extend |

**ABConnectTools reference**:
- `SmsTemplate.py` — 7 methods (includes `jobStatuses` which may be unlisted in swagger). `list` accepts optional `companyId` query param.
- `notifications.py` — 1 method, no params.
- `Values.py` — Simple health check endpoint.

### Group 7: Extended Entities (13 endpoints — extend existing files)

| Tag | Count | Endpoints | SDK File |
|-----|-------|-----------|----------|
| Companies | 7 | filteredCustomers (POST), infoFromKey (GET), search (GET), simplelist (POST), capabilities GET/POST, franchiseeAddresses (GET) | Extend `companies.py` |
| Contacts | 2 | customers (POST), search (POST) | Extend `contacts.py` |
| Address | 2 | avoidValidation (POST), validated (POST) | Extend `address.py` |
| Documents | 2 | get/thumbnail/{docPath} (GET), hide/{docId} (PUT) | Extend `documents.py` |

## ABC Gap Analysis (7 endpoints)

| Tag | Method | Path | Notes |
|-----|--------|------|-------|
| Test | GET | /api/Test/contact | Diagnostic — returns test contact |
| Test | GET | /api/Test/recentestimates | Diagnostic — returns recent estimates |
| Test | GET | /api/Test/renderedtemplate | Diagnostic — returns rendered template |
| Web2Lead | POST | /api/Web2Lead/postv2 | V2 of existing Web2Lead post |
| AutoPrice | POST | /api/autoprice/quoterequest | V1 of quote request (SDK has v2) |
| LogBuffer | POST | /api/logbuffer/flush | ABC-side log flush |
| Report | GET | /api/report/webrevenue | Web revenue report |

**SDK files**:
- Extend `web2lead.py` (+1: postv2)
- Extend `autoprice.py` (+1: quoterequest v1)
- New `abc_test.py` (3 test endpoints) or fold into existing
- New `abc_reports.py` (1 report endpoint) or fold into existing
- ABC logbuffer (1) — new file or fold into admin

## Design Decisions

### D1: File naming for `/api/company/` (singular) endpoints

**Decision**: Create `company_setup.py` to distinguish from existing `companies.py` (plural).
**Rationale**: The API uses `/api/company/{companyId}/` (singular) for per-company configuration and `/api/companies/` (plural) for listing/searching. ABConnectTools uses `company.py` (singular) but our SDK already has `companies.py`, so a distinct name prevents confusion.
**Alternatives**: `company.py` (ambiguous with `companies.py`), splitting into multiple files per tag (over-fragmentation for 26 endpoints that share the same base path and companyId pattern).

### D2: Webhook endpoints inclusion

**Decision**: Include all 6 webhook endpoints in `webhooks.py` but document that these are server-side callback receivers, not typical SDK operations.
**Rationale**: Completeness per spec (100% coverage). The webhooks are POST endpoints that Stripe/Twilio call into the ACPortal server — calling them from the SDK would only make sense in testing scenarios.
**Alternatives**: Exclude webhooks as non-SDK-relevant (breaks 100% goal), mark as "server-only" in docs.

### D3: ABC Test endpoints inclusion

**Decision**: Include all 3 Test endpoints in a new `abc_test.py` file.
**Rationale**: Completeness. These diagnostic endpoints are useful for integration testing and SDK verification.
**Alternatives**: Exclude as non-production (breaks 100% goal).

### D4: Extending `jobs.py` (already 55 routes)

**Decision**: Extend `jobs.py` with 12 more routes (→ 67 total), maintaining the D2 flat-file convention from Feature 008.
**Rationale**: Consistency with prior decision. The 12 new routes are all `/api/job/*` paths. Splitting would introduce a new pattern mid-project.
**Alternatives**: Split into `jobs_extended.py` (introduces inconsistency with 008 precedent).

### D5: Phasing strategy (4 phases)

**Decision**: Implement in 4 phases to keep PRs at 20-30 endpoints each:
- Phase 1: Company Setup + Admin (~39 endpoints)
- Phase 2: Account + Extended Jobs (~22 endpoints)
- Phase 3: Integrations + Communication (~21 endpoints)
- Phase 4: Extended Entities + ABC (~20 endpoints)

**Rationale**: PR #8 was 106 endpoints and was large but manageable. Four phases of ~20-40 endpoints each should be comfortable. Grouping keeps related functionality together for coherent review.
**Alternatives**: 2 phases (~50 each, larger PRs), 6+ phases (too fragmented, excessive overhead).

### D6: SMS Template `jobStatuses` endpoint

**Decision**: Check swagger carefully — ABConnectTools has a `jobStatuses` method but it may not appear in current swagger. Only implement what's in swagger.
**Rationale**: Principle IV — swagger-informed, reality-validated. If the endpoint isn't in swagger, it may have been removed or is undocumented.

### D7: Values endpoint handling

**Decision**: Create a minimal `values.py` file (1 endpoint) as a health-check utility.
**Rationale**: It's in the swagger spec. A simple GET with no params. Could be useful for connectivity testing.
**Alternatives**: Fold into admin.py or another catch-all file.

## ABConnectTools Pattern Summary

All remaining groups have ABConnectTools implementations (none are "new API additions without legacy code"). Key patterns observed:

1. **No special headers** — All remaining endpoints use standard Bearer token auth
2. **No file uploads** — None of the remaining endpoints handle file uploads
3. **No unusual pagination** — Standard response structures throughout
4. **URL path params** — `{companyId}`, `{jobDisplayId}`, `{sourceId}`, `{templateId}`, etc. use string replacement
5. **Query params** — Some endpoints use query params on POST (e.g., `approveinsuranceexception` takes `JobId`)
6. **JSON bodies** — All POST/PUT endpoints use `json=data` transport (no `params=` confusion)
7. **Delete with query params** — `containerThicknessInches` DELETE uses `containerId` query param instead of URL param
