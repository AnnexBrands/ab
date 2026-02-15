# Feature Specification: Extended Operations Endpoints

**Feature Branch**: `008-extended-operations`
**Created**: 2026-02-14
**Status**: Draft
**Input**: User description: "Implement the next group of SDK endpoints covering medium-priority operational workflows: RFQ lifecycle, job on-hold management, job email and SMS, reports and dashboards, extended company and contact operations, commodity management, extended lookups, global notes, partners, freight providers, and views/grids."

## Clarifications

### Session 2026-02-14

- Q: How many endpoints should this round target? → A: Focus on MEDIUM-priority operational endpoints (~106) that extend the SDK beyond the core job lifecycle covered by features 001 and 002.
- Q: Should this feature cover all three API surfaces? → A: ACPortal only. Catalog is 100% complete. ABC remaining endpoints are test utilities and deprecated versions — not worth a feature spec.
- Q: Should communication endpoints (email/SMS) return delivery status or fire-and-forget? → A: Fire-and-forget is assumed. These POST to ABConnect's API which queues delivery; the SDK does not poll for delivery status.
- Q: Should report endpoints support streaming or pagination for large result sets? → A: Standard JSON responses. Reports are business-level summaries, not raw data exports. ABConnect handles any internal pagination.
- Q: Should extended lookups expose the generic `/{masterConstantKey}` pattern or individual named methods? → A: Both. A generic `get_by_key(key)` method for flexibility, plus named convenience methods for the most common lookups (parcel package types, document types, density class map, etc.).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Manage RFQ Lifecycle for Competitive Bidding (Priority: P1)

A developer building a procurement integration needs to send jobs out for competitive quotes from freight providers, review incoming bids, accept or decline quotes, and select a winner. The SDK provides typed methods for the full RFQ (Request for Quote) lifecycle so the developer can automate competitive bidding workflows without manual portal interaction.

**Why this priority**: RFQ is the primary mechanism for obtaining competitive pricing on freight jobs. It directly impacts the revenue margin on every shipment. Automating this workflow is the highest-value operational extension for customers who process high volumes of jobs.

**Independent Test**: Can be fully tested by listing RFQs for a job, checking RFQ status, and calling accept/decline/cancel actions, verifying each response is a validated Pydantic model.

**Acceptance Scenarios**:

1. **Given** a valid job display ID, **When** a developer calls `api.jobs.list_rfqs(job_display_id)`, **Then** the SDK returns a list of typed RFQ display info models with provider, price, and status.
2. **Given** a job and a service type/company combination, **When** a developer calls `api.jobs.get_rfq_status(job_display_id, service_type, company_id)`, **Then** the SDK returns a typed RFQ status model.
3. **Given** an RFQ ID, **When** a developer calls `api.rfq.get(rfq_id)`, **Then** the SDK returns the full RFQ detail model.
4. **Given** an RFQ with quotes received, **When** a developer calls `api.rfq.accept(rfq_id, accept_model)`, **Then** the SDK accepts the quote and returns confirmation.
5. **Given** an RFQ that should be rejected, **When** a developer calls `api.rfq.decline(rfq_id)`, **Then** the SDK declines the quote.
6. **Given** an RFQ that is no longer needed, **When** a developer calls `api.rfq.cancel(rfq_id)`, **Then** the SDK cancels the RFQ.
7. **Given** an RFQ with a winning bid selected, **When** a developer calls `api.rfq.accept_winner(rfq_id)`, **Then** the SDK confirms the winner selection.

---

### User Story 2 - Handle Job Exceptions with On-Hold Management (Priority: P2)

A developer building an operations integration needs to place jobs on hold when issues arise (damaged goods, missing paperwork, customer disputes), track follow-up responsibilities, add comments, update dates, and resolve holds to resume the job lifecycle. The SDK provides typed methods for the complete on-hold workflow so the developer can manage exceptions programmatically.

**Why this priority**: On-hold management is the exception-handling mechanism for the job lifecycle. Jobs frequently encounter issues that pause their progress. Without programmatic on-hold management, integrations cannot handle the most common operational exception — requiring manual portal intervention for every hold/unhold action.

**Independent Test**: Can be fully tested by creating an on-hold record on a job, listing holds, adding a comment, and resolving the hold, verifying each response is a validated Pydantic model.

**Acceptance Scenarios**:

1. **Given** a valid job display ID, **When** a developer calls `api.jobs.list_on_hold(job_display_id)`, **Then** the SDK returns a list of typed on-hold info models.
2. **Given** a job and an on-hold request, **When** a developer calls `api.jobs.create_on_hold(job_display_id, **kwargs)`, **Then** the SDK creates the hold and returns a response model with the hold ID.
3. **Given** an existing on-hold ID, **When** a developer calls `api.jobs.get_on_hold(job_display_id, on_hold_id)`, **Then** the SDK returns the full on-hold detail model.
4. **Given** an on-hold record, **When** a developer calls `api.jobs.update_on_hold(job_display_id, on_hold_id, **kwargs)`, **Then** the SDK updates the hold and returns the updated model.
5. **Given** an on-hold record, **When** a developer calls `api.jobs.add_on_hold_comment(job_display_id, on_hold_id)`, **Then** the SDK adds the comment and returns a note detail model.
6. **Given** an on-hold record ready to resolve, **When** a developer calls `api.jobs.resolve_on_hold(job_display_id, on_hold_id, **kwargs)`, **Then** the SDK resolves the hold and the job resumes its lifecycle.
7. **Given** a job with a hold, **When** a developer calls `api.jobs.delete_on_hold(job_display_id)`, **Then** the SDK removes the hold record.
8. **Given** a contact ID, **When** a developer calls `api.jobs.get_on_hold_followup_user(job_display_id, contact_id)`, **Then** the SDK returns the follow-up user model.

---

### User Story 3 - Generate Business Reports and Analytics (Priority: P3)

A developer building a reporting integration needs to generate insurance reports, sales forecasts, revenue breakdowns by customer/sales rep, referral tracking, and web lead analytics. The SDK provides typed methods for all report endpoints so the developer can pull business intelligence data programmatically for dashboards, executive summaries, or downstream analytics systems.

**Why this priority**: Reports provide the business intelligence layer that operations and management teams rely on for decision-making. Sales forecasts, revenue attribution, and insurance tracking are high-frequency requests from customers building custom reporting workflows.

**Independent Test**: Can be fully tested by generating a sales report with a date range filter and verifying the response is a validated Pydantic model with expected summary fields.

**Acceptance Scenarios**:

1. **Given** a date range filter, **When** a developer calls `api.reports.insurance(**kwargs)`, **Then** the SDK returns a typed insurance report model.
2. **Given** a sales forecast request, **When** a developer calls `api.reports.sales(**kwargs)`, **Then** the SDK returns a typed sales forecast model.
3. **Given** a sales summary request, **When** a developer calls `api.reports.sales_summary(**kwargs)`, **Then** the SDK returns a typed sales summary model.
4. **Given** a revenue filter, **When** a developer calls `api.reports.top_revenue_customers(**kwargs)`, **Then** the SDK returns a list of typed revenue customer models.
5. **Given** a revenue filter, **When** a developer calls `api.reports.top_revenue_sales_reps(**kwargs)`, **Then** the SDK returns a list of typed revenue models by sales rep.
6. **Given** a referral filter, **When** a developer calls `api.reports.referred_by(**kwargs)`, **Then** the SDK returns a typed referral report model.
7. **Given** a web lead filter, **When** a developer calls `api.reports.web2lead(**kwargs)`, **Then** the SDK returns a typed web lead report model.

---

### User Story 4 - Send Job Communications via Email and SMS (Priority: P4)

A developer building a communication workflow needs to send documents via email, trigger transactional emails from templates, send SMS messages to contacts, and mark SMS messages as read. The SDK provides typed methods for all job-level communication endpoints so the developer can automate customer outreach as part of their job management workflow.

**Why this priority**: Communication is a natural extension of job management. After booking a shipment or generating an invoice, customers commonly need to email the BOL or quote to the shipper/receiver. SMS is used for delivery notifications. These are high-frequency actions in the ABConnect portal that benefit from automation.

**Independent Test**: Can be fully tested by sending a test email with a document attachment for a valid job, verifying the SDK accepts the request without error.

**Acceptance Scenarios**:

1. **Given** a job and email parameters, **When** a developer calls `api.jobs.send_email(job_display_id, **kwargs)`, **Then** the SDK posts the email request to ABConnect's queue.
2. **Given** a job and a document to send, **When** a developer calls `api.jobs.send_document_email(job_display_id, **kwargs)`, **Then** the SDK sends the document via email.
3. **Given** a job, **When** a developer calls `api.jobs.create_transactional_email(job_display_id)`, **Then** the SDK triggers a transactional email.
4. **Given** a job and an email template GUID, **When** a developer calls `api.jobs.send_template_email(job_display_id, template_guid)`, **Then** the SDK sends the templated email.
5. **Given** a job display ID, **When** a developer calls `api.jobs.list_sms(job_display_id)`, **Then** the SDK returns SMS history for the job.
6. **Given** a job and SMS parameters, **When** a developer calls `api.jobs.send_sms(job_display_id, **kwargs)`, **Then** the SDK sends the SMS message.
7. **Given** a job and SMS IDs, **When** a developer calls `api.jobs.mark_sms_read(job_display_id, **kwargs)`, **Then** the SDK marks the specified messages as read.
8. **Given** a template ID, **When** a developer calls `api.jobs.get_sms_template(job_display_id, template_id)`, **Then** the SDK returns the rendered SMS template.

---

### User Story 5 - Access Extended Reference Data and Commodities (Priority: P5)

A developer building a data integration needs access to additional lookup tables (parcel package types, document types, density class maps, referral categories, access keys) and commodity management (CRUD, search, classification mappings). The SDK provides typed methods for all extended lookup and commodity endpoints so the developer can reference and manage the master data that underpins job configuration.

**Why this priority**: Reference data and commodities are foundational data that other operations depend on. Commodity classification drives pricing and compliance. Extended lookups provide the configuration values needed to correctly populate job creation, shipment booking, and form generation requests. Without these, developers must hardcode or externally manage values that the API already provides.

**Independent Test**: Can be fully tested by calling the generic lookup method with a known master constant key and verifying the response, then creating and searching for a commodity.

**Acceptance Scenarios**:

1. **Given** a master constant key, **When** a developer calls `api.lookup.get_by_key(key)`, **Then** the SDK returns a list of typed lookup value models.
2. **Given** a master constant key and value ID, **When** a developer calls `api.lookup.get_by_key_and_id(key, value_id)`, **Then** the SDK returns a single typed lookup value model.
3. **Given** no parameters, **When** a developer calls `api.lookup.get_parcel_package_types()`, **Then** the SDK returns a list of parcel package type models.
4. **Given** no parameters, **When** a developer calls `api.lookup.get_document_types()`, **Then** the SDK returns a list of document type models.
5. **Given** no parameters, **When** a developer calls `api.lookup.get_density_class_map()`, **Then** the SDK returns the density-to-freight-class mapping.
6. **Given** a commodity ID, **When** a developer calls `api.commodities.get(commodity_id)`, **Then** the SDK returns a typed commodity model.
7. **Given** a search request, **When** a developer calls `api.commodities.search(**kwargs)`, **Then** the SDK returns a list of matching commodity models.
8. **Given** commodity data, **When** a developer calls `api.commodities.create(**kwargs)`, **Then** the SDK creates the commodity and returns the created model.
9. **Given** a commodity map search, **When** a developer calls `api.commodity_maps.search(**kwargs)`, **Then** the SDK returns matching commodity-to-standard mapping models.

---

### User Story 6 - Monitor Operations via Dashboard and Views (Priority: P6)

A developer building an operational monitoring tool needs to access dashboard data — inbound/outbound/in-house job counts, local delivery queues, recent estimates, and saved grid view configurations. The SDK provides typed methods for all dashboard and view endpoints so the developer can build custom operational dashboards that surface the same data available in the ABConnect portal.

**Why this priority**: Dashboards are the primary operational interface for day-to-day job management. While individual job endpoints exist, the dashboard endpoints provide pre-aggregated views that are essential for operations managers monitoring throughput, queue depth, and recent activity. Views/grids provide saved query configurations that power custom reporting.

**Independent Test**: Can be fully tested by calling the dashboard endpoint and verifying it returns aggregated operational data, then listing available grid views.

**Acceptance Scenarios**:

1. **Given** an authenticated session, **When** a developer calls `api.dashboard.get()`, **Then** the SDK returns a typed dashboard summary model.
2. **Given** a filter request, **When** a developer calls `api.dashboard.inbound(**kwargs)`, **Then** the SDK returns inbound job data.
3. **Given** a filter request, **When** a developer calls `api.dashboard.outbound(**kwargs)`, **Then** the SDK returns outbound job data.
4. **Given** a filter request, **When** a developer calls `api.dashboard.in_house(**kwargs)`, **Then** the SDK returns in-house job data.
5. **Given** a filter request, **When** a developer calls `api.dashboard.local_deliveries(**kwargs)`, **Then** the SDK returns local delivery data.
6. **Given** a filter request, **When** a developer calls `api.dashboard.recent_estimates(**kwargs)`, **Then** the SDK returns recent estimate data.
7. **Given** no parameters, **When** a developer calls `api.dashboard.get_grid_views()`, **Then** the SDK returns a list of saved grid view models.
8. **Given** a view ID, **When** a developer calls `api.views.get(view_id)`, **Then** the SDK returns the view configuration model.
9. **Given** view data, **When** a developer calls `api.views.create(**kwargs)`, **Then** the SDK creates a new saved view and returns the created model.
10. **Given** a view ID, **When** a developer calls `api.views.get_access_info(view_id)`, **Then** the SDK returns access control information for the view.

---

### User Story 7 - Manage Extended Company and Contact Data (Priority: P7)

A developer building a CRM integration needs access to extended company data — brand hierarchies, geographic settings, carrier account relationships, and packaging configurations — as well as contact history, graph data, and contact merging capabilities. The SDK provides typed methods for these extended entity management endpoints so the developer can fully manage company and contact records beyond the basic CRUD operations in feature 001.

**Why this priority**: Extended company and contact operations are needed for customers managing multi-brand franchisee networks, regional carrier relationships, and contact deduplication. While less frequent than core job operations, these are essential for enterprise integrations that synchronize ABConnect with external CRM and ERP systems.

**Independent Test**: Can be fully tested by listing company brands, retrieving geographic settings for a company, and previewing a contact merge.

**Acceptance Scenarios**:

1. **Given** no parameters, **When** a developer calls `api.companies.get_brands()`, **Then** the SDK returns a list of brand models.
2. **Given** no parameters, **When** a developer calls `api.companies.get_brands_tree()`, **Then** the SDK returns a hierarchical brand tree model.
3. **Given** a company ID, **When** a developer calls `api.companies.get_geo_settings(company_id)`, **Then** the SDK returns the company's geographic settings model.
4. **Given** a company ID, **When** a developer calls `api.companies.get_carrier_accounts(company_id)`, **Then** the SDK returns a list of carrier account models.
5. **Given** a company ID, **When** a developer calls `api.companies.get_packaging_settings(company_id)`, **Then** the SDK returns the company's packaging configuration model.
6. **Given** a contact ID, **When** a developer calls `api.contacts.get_history(contact_id)`, **Then** the SDK returns the contact's interaction history.
7. **Given** a contact ID, **When** a developer calls `api.contacts.get_history_aggregated(contact_id)`, **Then** the SDK returns aggregated contact history.
8. **Given** two contact IDs, **When** a developer calls `api.contacts.merge_preview(merge_to_id, merge_from_ids)`, **Then** the SDK returns a preview of the merge result without executing it.
9. **Given** a confirmed merge preview, **When** a developer calls `api.contacts.merge(merge_to_id, merge_from_ids)`, **Then** the SDK merges the contacts into the target record.

---

### Edge Cases

- What happens when an RFQ is accepted after another provider's quote was already accepted? The SDK surfaces the API's conflict error as a typed exception indicating the RFQ has already been awarded.
- What happens when a job on-hold is resolved but the underlying issue recurs? A new on-hold record can be created — the SDK does not prevent multiple holds on the same job.
- What happens when a report is requested with an empty date range? The SDK passes through the API's validation error as a typed exception.
- What happens when an email is sent to an invalid address? The SDK accepts the request (fire-and-forget to ABConnect's queue). Delivery failures are handled by ABConnect's email infrastructure, not surfaced through the API.
- What happens when SMS is sent to a non-mobile number? The SDK posts to ABConnect's queue which handles delivery. The API does not validate phone number type.
- What happens when a generic lookup key does not exist? The SDK returns an empty list, consistent with the existing pattern for list endpoints.
- What happens when a contact merge preview shows data conflicts? The preview model includes conflict details so the developer can decide whether to proceed with the merge.
- What happens when a dashboard request is made by a user without sufficient permissions? The SDK surfaces the API's 403 error as a typed permission exception.
- What happens when a commodity map references a commodity that has been deleted? The SDK returns the map with the dangling reference; it does not validate referential integrity.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: SDK MUST provide typed client methods for all RFQ lifecycle endpoints (9 endpoints): list RFQs for a job, get RFQ status by service type/company, get RFQ by ID, get RFQs for a job by job ID, accept, decline, cancel, accept winner, and add comment.
- **FR-002**: SDK MUST provide typed client methods for all job on-hold management endpoints (10 endpoints): list, create, delete, get by ID, update, get follow-up user, list follow-up users, add comment, update dates, and resolve.
- **FR-003**: SDK MUST provide typed client methods for all report endpoints (8 endpoints): insurance, sales forecast, sales summary, sales drilldown, top revenue customers, top revenue sales reps, referred by, and web2lead.
- **FR-004**: SDK MUST provide typed client methods for all job email endpoints (4 endpoints): send email, send document email, create transactional email, and send template email.
- **FR-005**: SDK MUST provide typed client methods for all job SMS endpoints (4 endpoints): list SMS, send SMS, mark as read, and get template-based SMS.
- **FR-006**: SDK MUST provide typed client methods for all extended lookup endpoints (12 endpoints): generic get-by-key, get-by-key-and-id, plus named convenience methods for access keys, PPC campaigns, parcel package types, document types, common insurance, density class map, referral categories, referral category hierarchy, and reset cache.
- **FR-007**: SDK MUST provide typed client methods for all commodity endpoints (5 endpoints): get, update, create, search, and suggestions.
- **FR-008**: SDK MUST provide typed client methods for all commodity map endpoints (5 endpoints): get, update, delete, create, and search.
- **FR-009**: SDK MUST provide typed client methods for all dashboard endpoints (9 endpoints): get dashboard, get grid views, get/save grid view state, and filter by inbound, in-house, outbound, local deliveries, and recent estimates.
- **FR-010**: SDK MUST provide typed client methods for all views/grids endpoints (8 endpoints): list all, get by ID, create, delete, get access info, update access, get dataset SPs, and get dataset SP by name.
- **FR-011**: SDK MUST provide typed client methods for all extended company endpoints (16 endpoints): brands, brands tree, geo area companies, geo settings (global and per-company get/save), carrier accounts (search, suggest, per-company get/save), packaging settings (get/save), packaging labor (get/save), and inherited packaging tariffs/labor.
- **FR-012**: SDK MUST provide typed client methods for all extended contact endpoints (5 endpoints): post history, get aggregated history, get graph data, merge preview, and merge.
- **FR-013**: SDK MUST provide typed client methods for freight provider and item endpoints (4 endpoints): list freight providers, add freight provider, get freight provider rate quote, and add freight items.
- **FR-014**: SDK MUST provide typed client methods for global note endpoints (4 endpoints): list, create, update, and suggest users.
- **FR-015**: SDK MUST provide typed client methods for partner endpoints (3 endpoints): list, get by ID, and search.
- **FR-016**: Every new endpoint MUST follow the same patterns established in features 001 and 007: Route definitions with frozen dataclasses, `**kwargs` method signatures, `request_model`/`params_model` on Route, request models with `extra="forbid"`, response models with `extra="allow"` and drift logging, snake_case fields with camelCase aliases.
- **FR-017**: Every new response model MUST have a corresponding fixture file in `tests/fixtures/` validated against the Pydantic model. Endpoints where live fixtures cannot be captured MUST be tracked in `FIXTURES.md` with status and notes.
- **FR-018**: Every new endpoint group MUST have Sphinx documentation with description, HTTP method/path, Python code example, and cross-reference to the response model class.
- **FR-019**: New endpoint groups (rfq, reports, dashboard, views, commodities, commodity_maps, notes, partners) MUST be exposed as attributes on the `ABConnectAPI` client. Endpoints extending existing groups (on-hold, email, SMS on jobs; extended lookups; extended companies; extended contacts; freight providers) MUST be added as methods on the existing endpoint class.
- **FR-020**: A design decisions document MUST be created at `specs/008-extended-operations/research.md` documenting architectural choices that depart from ABConnectTools patterns, with explicit references to how ABConnectTools handles the same operations.
- **FR-021**: Swagger compliance tests MUST be updated to reflect the newly implemented endpoints, further reducing the unimplemented count.
- **FR-022**: `FIXTURES.md` MUST be updated with tracking entries for all new endpoints in the unified 4D format.

### Key Entities

- **QuoteRequestDisplayInfo**: An RFQ listing entry. Key attributes: RFQ ID, provider company, service type, quoted price, transit time, and bid status (pending/accepted/declined/cancelled).
- **ExtendedOnHoldInfo**: A job on-hold record. Key attributes: hold ID, reason category, description, created date, follow-up user, follow-up date, resolution status, and comments list.
- **SaveOnHoldRequest**: Request payload for creating or updating a hold. Key attributes: reason, description, follow-up contact ID, follow-up date.
- **InsuranceReport**: Insurance claims summary. Key attributes: date range, claim count, total amount, claims by status.
- **SalesForecastReport**: Sales projections. Key attributes: date range, projected revenue, actual revenue, sales rep breakdowns.
- **RevenueCustomer**: Revenue attribution by customer or sales rep. Key attributes: entity name, total revenue, job count, average job value.
- **SendDocumentEmailModel**: Email request payload. Key attributes: recipient addresses, subject, body, document type to attach.
- **SendSMSModel**: SMS request payload. Key attributes: recipient phone number, message body, template ID (optional).
- **Commodity**: A product classification entry. Key attributes: commodity ID, description, freight class, NMFC code, weight range.
- **CommodityMap**: A mapping between custom commodity names and standard classifications. Key attributes: map ID, custom name, standard commodity ID.
- **DashboardSummary**: Aggregated operational metrics. Key attributes: inbound count, outbound count, in-house count, local deliveries count, recent estimates.
- **ViewConfig**: A saved grid/view configuration. Key attributes: view ID, name, dataset SP reference, column definitions, filter criteria, sort order, access permissions.
- **CompanyBrand**: A brand in the company hierarchy. Key attributes: brand ID, name, parent brand ID, company associations.
- **GeoSettings**: Geographic configuration for a company. Key attributes: service area definitions, geo restrictions, area-based routing rules.
- **CarrierAccount**: A carrier relationship for a company. Key attributes: account number, carrier name, negotiated rates flag, service types.
- **ContactHistory**: Interaction history for a contact. Key attributes: event type, timestamp, related job, description, agent.
- **GlobalNote**: A note not tied to a specific job. Key attributes: note ID, author, content, created date, mentioned users.
- **Partner**: A business partner entity. Key attributes: partner ID, name, type, contact information.
- **FreightProvider**: A carrier option for a job. Key attributes: provider name, service types, rate quote availability.

### Assumptions

- All new endpoints use the same authentication mechanism (Bearer JWT via the existing `HttpClient`) and the same ACPortal base URL pattern (`portal.{env}.abconnect.co/api/api`).
- Email and SMS endpoints are fire-and-forget: the SDK posts the request to ABConnect's queue and does not poll for delivery status. Success means the API accepted the request, not that the message was delivered.
- Report endpoints return complete result sets in a single JSON response. No streaming or cursor-based pagination is needed for these summary-level reports.
- The generic lookup endpoint (`/{masterConstantKey}`) returns different shapes depending on the key. The SDK will use a generic model with `extra="allow"` for the base case and typed convenience methods for known keys where the response shape is stable.
- Commodity and commodity-map endpoints are CRUD + search operations following standard REST patterns. The search endpoints accept POST with filter criteria in the body.
- Dashboard filter endpoints (inbound, outbound, etc.) accept POST with filter criteria in the body and return lists of job summary records.
- Views/grids endpoints manage saved UI configurations. The `datasetsp` and `datasetsps` endpoints reference stored procedures that power custom data views.
- Contact merge is a destructive operation — once executed, the merged-from contacts are permanently consolidated into the merge-to contact. The preview endpoint exists to allow review before committing.
- Extended company endpoints (brands, geo, carriers, packaging) follow the same URL pattern as the existing company endpoints and are added as methods on the existing `Companies` endpoint class.
- ABConnectTools at `/usr/src/pkgs/ABConnectTools/` will be referenced during planning to document design departures, but no code will be copied.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All ~106 new endpoints return validated Pydantic models, with zero raw-dict responses in the public API.
- **SC-002**: 100% of new endpoints have a fixture file (live or mock) tracked in `FIXTURES.md` with the unified 4D format.
- **SC-003**: Sphinx documentation builds with zero warnings and every new endpoint group page includes a code example and model cross-reference.
- **SC-004**: Swagger compliance tests show a measurable reduction in unimplemented endpoint count (from ~145 to ~39).
- **SC-005**: A `research.md` design decisions document exists with at least one documented departure from ABConnectTools patterns per new endpoint group.
- **SC-006**: All new endpoint methods are accessible through the `ABConnectAPI` client object without requiring manual instantiation of endpoint classes.
- **SC-007**: Existing tests continue to pass — zero regressions in feature 001 and 002 functionality.
- **SC-008**: New endpoint groups (rfq, reports, dashboard, views, commodities, commodity_maps, notes, partners) are registered as client attributes in `ab/client.py`.

## Scope Boundaries

### In Scope

- All 14 MEDIUM-priority endpoint groups from the project gap analysis
- ACPortal endpoints only
- New endpoint classes for: rfq, reports, dashboard, views, commodities, commodity_maps, notes, partners
- Extensions to existing endpoint classes for: jobs (on-hold, email, SMS, freight), lookup (extended), companies (brands, geo, carriers, packaging), contacts (history, merge)

### Out of Scope

- LOW-priority admin/internal endpoints (~110 endpoints): account/auth management, admin settings, SMS templates, company setup, materials/trucks, Intacct integration, e-sign, webhooks, notifications
- ABC API remaining endpoints (test utilities and deprecated versions)
- Catalog API (already 100% complete)
- Webhook receiver/handler endpoints (these are inbound to ABConnect, not outbound API calls)
- Delivery status tracking for email/SMS (fire-and-forget pattern)
