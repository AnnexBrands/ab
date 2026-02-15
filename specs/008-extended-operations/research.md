# Research & Design Decisions: Extended Operations Endpoints

**Feature**: 008-extended-operations
**Date**: 2026-02-14
**Reference**: ABConnectTools at `/usr/src/pkgs/ABConnectTools/`

## Design Decisions

### D1 — Job-scoped vs Standalone RFQ Split

**Decision**: RFQ endpoints are split across two classes: `api.jobs.list_rfqs()` and `api.jobs.get_rfq_status()` (job-scoped, under `/api/job/{jobDisplayId}/rfq/...`) go on `JobsEndpoint`; standalone operations (`api.rfq.get()`, `api.rfq.accept()`, etc., under `/api/rfq/{rfqId}/...`) go on a new `RFQEndpoint`.

**Rationale**: The URL structure naturally separates job-scoped discovery (listing RFQs for a job) from entity-scoped lifecycle actions (accept/decline/cancel an RFQ by ID). This mirrors the existing pattern where `api.jobs.get_tracking()` is job-scoped but shipments have their own `api.shipments` class.

**ABConnectTools pattern**: ABConnectTools has a standalone `rfq.py` endpoint file with all 7 methods. It does not split job-scoped RFQ endpoints onto the jobs class. The AB SDK departs by putting job-scoped RFQ queries on the jobs class for consistency with the SDK's URL-driven class assignment.

**Alternatives rejected**: (A) All RFQ methods on a single class — rejected because the URL prefixes differ (`/job/...` vs `/rfq/...`), which would complicate base URL routing. (B) All on jobs — rejected because standalone RFQ operations don't require a job display ID.

### D2 — On-Hold Methods on Jobs (Not a Submodule)

**Decision**: All 10 on-hold methods are added directly to `JobsEndpoint` as a new section, not split into a separate file or submodule.

**Rationale**: The AB SDK convention is one endpoint file per API base path prefix. On-hold endpoints live under `/api/job/{jobDisplayId}/onhold/...`, making them job-scoped. The `jobs.py` file will grow to ~54 methods, but this is acceptable for a flat namespace that's easy to discover via IDE autocomplete.

**ABConnectTools pattern**: ABConnectTools splits job endpoints into subdirectories (`jobs/onhold.py`, `jobs/email.py`, `jobs/sms.py`). The AB SDK departs by keeping all job methods in a single file. This trades file size for import simplicity — users always know `api.jobs.*`.

**Alternatives rejected**: (A) Submodule directory `endpoints/jobs/` — rejected because it would break the established flat file convention and require restructuring the existing jobs.py. (B) Separate `OnHoldEndpoint` class — rejected because on-hold is scoped to jobs and would require a `job_display_id` parameter on every method, duplicating the job context.

### D3 — Email/SMS as Job Methods (Fire-and-Forget)

**Decision**: Email (4 methods) and SMS (4 methods) are added to `JobsEndpoint`. All are fire-and-forget — the SDK posts the request and returns the API's response without polling for delivery status.

**Rationale**: These endpoints live under `/api/job/{jobDisplayId}/email/...` and `/api/job/{jobDisplayId}/sms/...`. They are job-scoped communication actions, not standalone services.

**ABConnectTools pattern**: ABConnectTools has separate files (`jobs/email.py`, `jobs/sms.py`) with the same fire-and-forget pattern. The AB SDK combines these into `jobs.py` per D2's convention.

**Alternatives rejected**: (A) Separate `EmailEndpoint`/`SMSEndpoint` classes — rejected for the same reasons as D2. (B) Delivery status tracking — rejected; ABConnect's API does not surface delivery status through these endpoints.

### D4 — Reports as a New Endpoint Class

**Decision**: All 8 report endpoints go on a new `ReportsEndpoint` class at `api.reports`, mapped to `/api/reports/...`.

**Rationale**: Reports are a distinct functional group with a dedicated URL prefix. They are not scoped to jobs, companies, or contacts.

**ABConnectTools pattern**: ABConnectTools has `reports.py` with the same 8 endpoints using the simple (non-schema-based) pattern. The AB SDK follows the same class structure but with Route definitions and request model validation (Principle IX).

### D5 — Generic Lookup + Named Convenience Methods

**Decision**: The extended lookup class provides a generic `get_by_key(key)` method for the `/{masterConstantKey}` endpoint plus named convenience methods (`get_parcel_package_types()`, `get_document_types()`, etc.) for the 10 specific lookup types.

**Rationale**: The generic method provides flexibility for any master constant key. Named convenience methods provide discoverability and type safety for the most common lookups. This dual approach serves both power users (who know the key names) and casual users (who benefit from autocomplete).

**ABConnectTools pattern**: ABConnectTools has individual methods for each lookup type (15 methods total) plus a generic `get_lookup_value()`. The AB SDK follows the same dual pattern.

**Note on `resetMasterConstantCache`**: This is a mutating action (cache invalidation), not a read-only lookup. It is included on the `LookupEndpoint` class as `reset_cache()` with a clear name indicating its side effect. This matches ABConnectTools which places it on the lookup class.

### D6 — Commodities and Commodity Maps as Separate Classes

**Decision**: Two new endpoint classes: `CommoditiesEndpoint` (`api.commodities`) for `/api/commodity/...` and `CommodityMapsEndpoint` (`api.commodity_maps`) for `/api/commodity-map/...`.

**Rationale**: Different URL prefixes = different endpoint classes. Commodity maps are a mapping layer on top of commodities — conceptually related but operationally separate (different CRUD operations, different models).

**ABConnectTools pattern**: ABConnectTools has a single `commodity.py` file covering both commodity and commodity-map endpoints. The AB SDK separates them by URL prefix for consistency with the one-class-per-prefix convention.

### D7 — Dashboard and Views as Separate Classes

**Decision**: Two new endpoint classes: `DashboardEndpoint` (`api.dashboard`) for `/api/dashboard/...` and `ViewsEndpoint` (`api.views`) for `/api/views/...`.

**Rationale**: Different URL prefixes. The dashboard provides operational aggregate views; views/grids manage saved UI configurations. While User Story 6 groups them conceptually, they are distinct API resources.

**ABConnectTools pattern**: ABConnectTools has separate `dashboard.py` and `views.py` files. The AB SDK follows the same separation. ABConnectTools's dashboard has deprecated endpoints with warnings — the AB SDK only implements current, non-deprecated endpoints.

### D8 — Extended Company Methods with CodeResolver

**Decision**: New company methods (brands, geo settings, carrier accounts, packaging) are added to the existing `CompaniesEndpoint` class. Methods that take a `company_id` parameter use the existing `CodeResolver` for UUID/code resolution.

**Rationale**: These endpoints share the `/api/companies/...` URL prefix. The CodeResolver is already wired into `CompaniesEndpoint.__init__()` and handles the code→UUID translation transparently.

**ABConnectTools pattern**: ABConnectTools uses `get_cache()` for the same code/UUID resolution. The AB SDK's `CodeResolver` is functionally equivalent but uses a dedicated cache service rather than an in-memory dict.

### D9 — Contact Merge as Separate Methods (No Guardrail)

**Decision**: Contact merge is exposed as two independent methods: `merge_preview()` (read-only preview) and `merge()` (destructive execution). The SDK does not enforce that `merge_preview()` must be called before `merge()`.

**Rationale**: The SDK's role is to provide typed access to the API, not enforce business workflows. Requiring a preview before merge would add state management to a stateless SDK. Developers who want the safeguard can call preview first at the application layer.

**ABConnectTools pattern**: ABConnectTools exposes `post_merge_preview()` and `put_merge()` independently, with no enforcement. The AB SDK follows the same pattern.

### D10 — Global Notes Naming (api.notes)

**Decision**: Global notes are exposed as `api.notes` (not `api.global_notes` or similar). This is distinct from job-scoped notes at `api.jobs.get_notes()`.

**Rationale**: The URL prefix is `/api/note/...` — the natural SDK attribute is `notes`. Job-scoped notes are accessed via `api.jobs.get_notes(job_display_id)`, which is syntactically unambiguous. The global notes endpoint supports query-param filtering by job_id, contact_id, company_id, and category — making it a cross-cutting search facility, not a duplication of job notes.

**ABConnectTools pattern**: ABConnectTools has `note.py` as a standalone endpoint file with filter parameters. The AB SDK follows the same structure.

### D11 — Freight Provider Methods on Jobs

**Decision**: All 4 freight provider endpoints go on `JobsEndpoint` since they are scoped to `/api/job/{jobDisplayId}/freightproviders/...` and `/api/job/{jobDisplayId}/freightitems`.

**ABConnectTools pattern**: ABConnectTools has a separate `jobs/freightproviders.py` submodule with Pydantic TypeAdapter validation. The AB SDK uses its standard `_request()` method with Route-defined response_model for the same validation, without needing TypeAdapter.

### D12 — Freight Items as Single Endpoint on Jobs

**Decision**: The `POST /job/{jobDisplayId}/freightitems` endpoint for adding freight items is added as a job method (`add_freight_items()`), not on a separate freight-items class.

**Rationale**: Single endpoint under the job URL prefix. Creating a dedicated class for one method would violate simplicity.
