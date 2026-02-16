# Implementation Plan: Remaining API Endpoints

**Branch**: `009-remaining-endpoints` | **Date**: 2026-02-14 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/009-remaining-endpoints/spec.md`

## Summary

Implement the remaining 102 API endpoints (95 ACPortal + 7 ABC) to achieve 100% SDK coverage across all three API surfaces. The work follows established patterns from Features 001, 007, and 008 — Route definitions, `**kwargs` signatures, Pydantic models, fixture validation tests, examples, and Sphinx docs. Delivered in 4 phases to keep PR scope manageable.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: pydantic>=2.0, pydantic-settings, requests, python-dotenv (unchanged)
**Storage**: N/A (SDK — no local storage)
**Testing**: pytest (fixture validation, swagger compliance, example params)
**Target Platform**: pip-installable Python package
**Project Type**: Single project (Python SDK)
**Performance Goals**: N/A (thin HTTP wrapper — no performance-critical paths)
**Constraints**: Backward compatibility with all existing imports and method signatures
**Scale/Scope**: 102 new endpoints, ~10 new endpoint files, ~15-20 new model files, ~30-50 new models

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | PASS | All new models will use mixin-based inheritance, `ResponseModel` (extra=allow), `RequestModel` (extra=forbid) |
| II. Example-Driven Fixture Capture | PASS | Examples will be written for each group; fixtures captured when run against staging |
| III. Four-Way Harmony | PASS | Each endpoint gets: implementation, example, fixture test (skip), Sphinx docs |
| IV. Swagger-Informed, Reality-Validated | PASS | Routes reference swagger operation IDs; models validated against fixtures |
| V. Endpoint Status Tracking | PASS | FIXTURES.md updated for all new endpoints in 4D format |
| VI. Documentation Completeness | PASS | Sphinx pages for each new endpoint group |
| VII. Flywheel Evolution | PASS | Completing 100% coverage is an engineering theme deliverable |
| VIII. Phase-Based Context Recovery | PASS | 4-phase delivery with checkpoint commits per DISCOVER phase |
| IX. Endpoint Input Validation | PASS | POST/PUT endpoints get RequestModels; param names match swagger |

**Post-design re-check**: No violations. All principles satisfied by design.

## Project Structure

### Documentation (this feature)

```text
specs/009-remaining-endpoints/
├── plan.md              # This file
├── research.md          # Phase 0 — gap analysis, ABConnectTools research, design decisions
├── data-model.md        # Phase 1 — new endpoint files and model catalog
├── quickstart.md        # Phase 1 — developer quick reference
├── contracts/           # Phase 1 — endpoint contracts by group
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
ab/api/endpoints/
├── account.py           # NEW — 10 endpoints (/api/account/*)
├── admin.py             # NEW — 13 endpoints (/api/admin/*)
├── company_setup.py     # NEW — 26 endpoints (/api/company/{companyId}/*)
├── intacct.py           # NEW — 5 endpoints (/api/jobintacct/*)
├── esign.py             # NEW — 2 endpoints (/api/e-sign/*)
├── webhooks.py          # NEW — 6 endpoints (/api/webhooks/*)
├── sms_templates.py     # NEW — 5 endpoints (/api/SmsTemplate/*)
├── notifications.py     # NEW — 1 endpoint (/api/notifications)
├── values.py            # NEW — 1 endpoint (/api/Values)
├── abc_test.py          # NEW — 3 endpoints (/api/Test/* on ABC)
├── abc_reports.py       # NEW — 1 endpoint (/api/report/* on ABC)
├── address.py           # EXTEND +2 endpoints
├── companies.py         # EXTEND +7 endpoints
├── contacts.py          # EXTEND +2 endpoints
├── documents.py         # EXTEND +2 endpoints
├── jobs.py              # EXTEND +12 endpoints (→ 67 total)
├── users.py             # EXTEND +1 endpoint
├── autoprice.py         # EXTEND +1 endpoint (v1 quoterequest)
└── web2lead.py          # EXTEND +1 endpoint (postv2)

ab/api/models/
├── account.py           # NEW — Account, Profile, PaymentSource models
├── admin.py             # NEW — AdvancedSetting, CarrierErrorMessage, GlobalSettings, etc.
├── company_setup.py     # NEW — Calendar, DocumentTemplate, GridSettings, Material, Truck, etc.
├── intacct.py           # NEW — JobIntacct models
├── esign.py             # NEW — ESign result model
├── sms_templates.py     # NEW — SmsTemplate models
├── webhooks.py          # NEW — Webhook models (if applicable)
└── [existing files]     # May need extension for new response shapes

examples/
├── account.py           # NEW
├── admin.py             # NEW
├── company_setup.py     # NEW
├── intacct.py           # NEW
├── esign.py             # NEW
├── webhooks.py          # NEW
├── sms_templates.py     # NEW
├── notifications.py     # NEW
├── abc_test.py          # NEW
├── abc_reports.py       # NEW
└── [existing files]     # May extend with new endpoint calls

tests/models/
├── test_account_fixtures.py      # NEW
├── test_admin_fixtures.py        # NEW
├── test_company_setup_fixtures.py # NEW
├── test_intacct_fixtures.py      # NEW
├── test_esign_fixtures.py        # NEW
├── test_sms_template_fixtures.py # NEW
└── [existing files]              # May extend

docs/
├── account.rst          # NEW
├── admin.rst            # NEW
├── company_setup.rst    # NEW
├── intacct.rst          # NEW
├── esign.rst            # NEW
├── webhooks.rst         # NEW
├── sms_templates.rst    # NEW
└── [existing files]     # May extend
```

**Structure Decision**: Follows existing single-project layout. New endpoint files for new API path prefixes; extend existing files for additional routes under existing prefixes. Model files mirror endpoint files 1:1.

## Phasing Strategy

### Phase 1: Company Setup + Admin (39 endpoints)

**Scope**: All `/api/company/{companyId}/*` (26) and `/api/admin/*` (13) endpoints.

**New files**: `company_setup.py` (endpoints + models), `admin.py` (endpoints + models)

**Endpoint groups**:
- Calendar (4): GET calendar, baseinfo, startofday, endofday
- Company External Accounts (3): Stripe connect URL, complete connection, delete
- CompanyDocumentTemplates (4): CRUD
- CompanySettings (3): Grid settings GET/POST, setup data GET
- ContainerThicknessInches (3): CRUD
- Material (4): CRUD
- Truck (4): CRUD
- Planner (1): GET
- AdvancedSettings (4): CRUD
- CarrierErrorMessage (2): GET all, POST
- GlobalSettings (5): Company hierarchy, insurance exceptions, Intacct
- LogBuffer (2): flush, flushAll

### Phase 2: Account + Extended Jobs (22 endpoints)

**Scope**: All `/api/account/*` (10) and remaining `/api/job/*` (12) endpoints.

**New files**: `account.py` (endpoints + models)
**Extended files**: `jobs.py` (+12 routes)

**Endpoint groups**:
- Account (10): register, confirm, forgot, resetpassword, setpassword, sendConfirmation, verifyresettoken, profile, paymentsource PUT/DELETE
- Job misc (8): documentConfig, feedback GET/POST, jobAccessLevel, transfer, changeAgent, copy, submanagementstatus
- JobBooking (1): book
- JobTracking (1): tracking/shipment/{proNumber}
- JobTrackingV2 (1): v2 tracking
- Email (1): labelrequest

### Phase 3: Integrations + Communication (21 endpoints)

**Scope**: Intacct, E-Sign, Webhooks, SMS Templates, Notifications, Values.

**New files**: `intacct.py`, `esign.py`, `webhooks.py`, `sms_templates.py`, `notifications.py`, `values.py`

**Endpoint groups**:
- JobIntacct (5): GET, POST, draft, applyRebate, DELETE
- JobSign (2): e-sign result, e-sign by job/booking
- StripeWebhook (3): 3 Stripe handlers
- TwilioWebhook (3): 3 Twilio handlers
- JobSmsTemplate (5): list, notificationTokens, save, GET by id, DELETE
- Notifications (1): GET
- Values (1): GET health check
- Users ext (1): pocusers (extend `users.py`)

### Phase 4: Extended Entities + ABC (20 endpoints)

**Scope**: Extend existing entity files (13 ACPortal) + all ABC gaps (7).

**Extended files**: `companies.py` (+7), `contacts.py` (+2), `address.py` (+2), `documents.py` (+2), `web2lead.py` (+1), `autoprice.py` (+1)
**New files**: `abc_test.py` (3), `abc_reports.py` (1), + ABC logbuffer

**Endpoint groups**:
- Companies ext (7): filteredCustomers, infoFromKey, search GET, simplelist, capabilities GET/POST, franchiseeAddresses
- Contacts ext (2): customers, search POST
- Address ext (2): avoidValidation, validated
- Documents ext (2): thumbnail, hide
- Web2Lead ext (1): postv2
- AutoPrice ext (1): quoterequest v1
- ABC Test (3): contact, recentestimates, renderedtemplate
- ABC Report (1): webrevenue
- ABC LogBuffer (1): flush

## DISCOVER Workflow Per Phase

Each phase follows the established DISCOVER workflow:

1. **D — Determine**: Research ABConnectTools + swagger for each endpoint group
2. **I — Implement models**: Create Pydantic response/request models from swagger schemas
3. **S — Scaffold endpoints**: Write Route definitions and endpoint methods; register in client.py
4. **C — Call & Capture**: Write examples; run against staging for fixtures
5. **O — Observe tests**: Run pytest; confirm Four-Way Harmony
6. **V — Verify & commit**: Checkpoint commit
7. **E — Enrich documentation**: Sphinx docs
8. **R — Release**: PR

**Batching within phases**: Within each phase, work by endpoint group (5-15 endpoints) using batch-by-type strategy (all models → all endpoints → all examples for a group).

## Complexity Tracking

No constitution violations. No complexity tracking needed.
