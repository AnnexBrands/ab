# Feature Specification: Extended API Endpoints

**Feature Branch**: `002-extended-endpoints`
**Created**: 2026-02-13
**Status**: Draft
**Input**: User description: "Next round of not implemented services — extend the SDK with additional API endpoint coverage beyond the initial 59 core endpoints"

## Clarifications

### Session 2026-02-13

- Q: How many endpoints should this round target? → A: Focus on HIGH-priority job workflow endpoints (~60) that developers building integrations need most. MEDIUM and LOW priority groups are deferred to future features.
- Q: Should this feature cover all three API surfaces? → A: ACPortal is the primary focus (vast majority of gaps). ABC has only 5 remaining minor endpoints (test/debug utilities). Catalog is 100% complete.
- Q: Should the feature include a design decisions artifact? → A: Yes. A research/design-decisions document MUST reference ABConnectTools patterns where the new endpoints diverge or make different choices.
- Q: Should form endpoints return raw bytes or a typed wrapper with content-type metadata? → A: Raw bytes, consistent with the existing `documents.get()` pattern. No wrapper object needed.
- Q: Should the SDK expose all three tracking API versions (v1, v2, v3) or only the latest? → A: Expose only v3 (latest). Skip v1 and v2 as deprecated API cruft.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Manage Job Lifecycle Through Timeline and Status (Priority: P1)

A developer building a job management integration needs to advance jobs through their lifecycle — viewing timeline tasks, creating new tasks, incrementing or undoing job status, and setting jobs to quote status. The SDK provides typed methods for all timeline and status operations so the developer can orchestrate job workflows programmatically without manually constructing API calls.

**Why this priority**: Job lifecycle management is the operational backbone of ABConnect. Without timeline and status control, integrations cannot move jobs through the core business workflow (quote → booked → in-transit → delivered → invoiced). Every other job operation (payments, shipments, forms) depends on the job being in the correct status.

**Independent Test**: Can be fully tested by retrieving a job's timeline, creating a timeline task, and advancing the job status, then verifying each response is a validated Pydantic model with correct fields.

**Acceptance Scenarios**:

1. **Given** a valid job display ID, **When** a developer calls `api.jobs.get_timeline(job_display_id)`, **Then** the SDK returns a list of typed timeline task models with status, dates, and agent information.
2. **Given** a job in "quote" status, **When** a developer calls `api.jobs.increment_status(job_display_id)`, **Then** the job advances to the next status in the lifecycle and the SDK returns a confirmation model.
3. **Given** a job whose status was just incremented, **When** a developer calls `api.jobs.undo_increment_status(job_display_id)`, **Then** the job reverts to its previous status.
4. **Given** a timeline task identifier, **When** a developer calls `api.jobs.get_timeline_task(job_display_id, task_id)`, **Then** the SDK returns a single timeline task model with full detail.
5. **Given** a new timeline task payload, **When** a developer calls `api.jobs.create_timeline_task(job_display_id, task)`, **Then** the SDK posts the task and returns the created model.

---

### User Story 2 - Book and Track Shipments with Rate Quotes (Priority: P2)

A developer building a shipping integration needs to request rate quotes from carriers, review accessorials, book a shipment, and track its progress. The SDK provides typed methods for the complete shipment lifecycle — from rate shopping through booking to tracking — so the developer can build end-to-end logistics workflows.

**Why this priority**: Shipment operations are the core revenue-generating activity. Rate quoting and booking are the most common integration points for customers automating their shipping workflows. Tracking provides customer-facing visibility that reduces support inquiries.

**Independent Test**: Can be fully tested by requesting rate quotes for a job, listing available accessorials, and retrieving tracking information, verifying each response is a validated Pydantic model.

**Acceptance Scenarios**:

1. **Given** a job with items ready to ship, **When** a developer calls `api.shipments.get_rate_quotes(job_display_id)`, **Then** the SDK returns a list of rate quote models with carrier, price, and transit time.
2. **Given** a selected rate quote, **When** a developer calls `api.shipments.book(job_display_id)`, **Then** the shipment is booked and the SDK returns a booking confirmation model.
3. **Given** a booked shipment, **When** a developer calls `api.jobs.get_tracking(job_display_id)`, **Then** the SDK returns tracking information with status, location, and history.
4. **Given** a job display ID, **When** a developer calls `api.shipments.get_accessorials(job_display_id)`, **Then** the SDK returns a list of available accessorial models.
5. **Given** a shipment with a PRO number, **When** a developer calls `api.jobs.get_tracking_by_pro(job_display_id, pro_number)`, **Then** the SDK returns carrier-specific tracking details.

---

### User Story 3 - Process Payments and Manage Payment Sources (Priority: P3)

A developer building a billing integration needs to retrieve payment information, list payment sources, and process payments via ACH or stored payment methods. The SDK provides typed methods for payment operations so the developer can automate invoicing and collection workflows.

**Why this priority**: Payment processing is essential for closing the job lifecycle. Without payment endpoints, integrations cannot automate the billing step, requiring manual intervention in the ABConnect portal for every transaction.

**Independent Test**: Can be fully tested by retrieving payment information for a job and listing available payment sources, verifying each response is a validated Pydantic model.

**Acceptance Scenarios**:

1. **Given** a completed job, **When** a developer calls `api.payments.get(job_display_id)`, **Then** the SDK returns a payment information model with balance, status, and history.
2. **Given** a job with payment sources configured, **When** a developer calls `api.payments.get_sources(job_display_id)`, **Then** the SDK returns a list of payment source models (cards, bank accounts).
3. **Given** a valid payment source, **When** a developer calls `api.payments.pay_by_source(job_display_id, source_id)`, **Then** the SDK processes the payment and returns a confirmation model.
4. **Given** a job requiring ACH payment, **When** a developer calls `api.payments.create_ach_session(job_display_id)`, **Then** the SDK initiates an ACH payment session and returns session details.

---

### User Story 4 - Generate Job Forms and Documents (Priority: P4)

A developer needs to programmatically generate printable business documents — invoices, bills of lading, packing slips, customer quotes, and shipping labels. The SDK provides typed methods for all 15 form types so the developer can integrate document generation into their workflows without screen-scraping or manual export.

**Why this priority**: Form generation is a high-frequency integration need. Customers regularly need to pull invoices, BOLs, and quotes into their own systems. These are all simple GET endpoints returning document content, making them low-risk to implement but high-value for integrators.

**Independent Test**: Can be fully tested by requesting an invoice form for a valid job and verifying the SDK returns the document content in the expected format.

**Acceptance Scenarios**:

1. **Given** a valid job display ID, **When** a developer calls `api.forms.get_invoice(job_display_id)`, **Then** the SDK returns the invoice document content.
2. **Given** a valid job display ID, **When** a developer calls `api.forms.get_bill_of_lading(job_display_id)`, **Then** the SDK returns the BOL document content.
3. **Given** a valid job display ID, **When** a developer calls `api.forms.get_packing_slip(job_display_id)`, **Then** the SDK returns the packing slip document content.
4. **Given** a valid job display ID, **When** a developer calls `api.forms.get_customer_quote(job_display_id)`, **Then** the SDK returns the customer quote document content.
5. **Given** the full set of 15 form types, **When** a developer calls each form method, **Then** every method returns content without error for a job that has the relevant data.

---

### User Story 5 - Manage Job Notes, Items, and Parcels (Priority: P5)

A developer building a warehouse or operations integration needs to add notes to jobs, manage line items, and handle parcel/packaging data. The SDK provides typed CRUD methods for notes, item updates, and parcel item management so the developer can keep job details synchronized between systems.

**Why this priority**: Notes, items, and parcels are the operational detail layer that sits on top of the job lifecycle. While not as critical as timeline or shipments, they are frequently needed for warehouse management and operational reporting integrations.

**Independent Test**: Can be fully tested by creating a note on a job, listing parcel items, and updating an item, verifying each response is a validated Pydantic model.

**Acceptance Scenarios**:

1. **Given** a valid job display ID, **When** a developer calls `api.jobs.list_notes(job_display_id)`, **Then** the SDK returns a list of note models with author, timestamp, and content.
2. **Given** a note payload, **When** a developer calls `api.jobs.create_note(job_display_id, note)`, **Then** the SDK creates the note and returns the created model.
3. **Given** a valid job display ID, **When** a developer calls `api.jobs.list_parcel_items(job_display_id)`, **Then** the SDK returns a list of parcel item models with dimensions, weight, and materials.
4. **Given** a parcel item payload, **When** a developer calls `api.jobs.create_parcel_item(job_display_id, parcel_item)`, **Then** the SDK creates the parcel item and returns the created model.
5. **Given** an existing item ID, **When** a developer calls `api.jobs.update_item(job_display_id, item_id, updates)`, **Then** the SDK updates the item and returns the updated model.

---

### Edge Cases

- What happens when a form type is requested for a job that lacks the required data (e.g., invoice for an unpriced job)? The SDK passes through the API error response as a typed exception with the status code and message, allowing the developer to handle it gracefully.
- What happens when a shipment booking fails due to carrier rejection? The SDK returns a typed error model containing the carrier's rejection reason, rather than a generic HTTP error.
- What happens when a payment source is expired or invalid? The SDK surfaces the API's validation error as a typed exception so the developer can prompt the user to update their payment method.
- What happens when timeline status increment is called on a job already at its final status? The SDK returns the API's error response as a typed exception indicating the job cannot be advanced further.
- What happens when rate quotes return no results (no carriers available)? The SDK returns an empty list rather than raising an error, consistent with the existing pattern for list endpoints.
- What happens when tracking information is unavailable (shipment not yet picked up)? The SDK returns a tracking model with empty/null tracking events, not an error.
- What happens when form endpoints return binary content (PDF/HTML) instead of JSON? The SDK returns raw bytes with no wrapper object, consistent with the existing `documents.get()` pattern. Callers who need the content type can inspect the response headers via the underlying HTTP client if needed.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: SDK MUST provide typed client methods for all job timeline and status management endpoints (9 endpoints): get timeline, create/get/update/delete timeline tasks, increment/undo status, get timeline task agent, and set quote status.
- **FR-002**: SDK MUST provide typed client methods for all shipment endpoints (14 endpoints): rate quotes, booking, accessorials, origin/destination, export data, rates state, and global shipment/accessorial/document retrieval.
- **FR-003**: SDK MUST provide typed client methods for all payment endpoints (10 endpoints): get payment info, payment sources, ACH credit transfer, ACH session, bank source attachment, pay-by-source, ACH verification, and payment creation.
- **FR-004**: SDK MUST provide typed client methods for all 15 job form endpoints: invoice, editable invoice, bill-of-lading, packing-slip, customer-quote, quick-sale, operations, shipments, address-label, item-labels, packaging-labels, packaging-specification, credit-card-authorization, USAR, and editable USAR.
- **FR-005**: SDK MUST provide typed client methods for job notes (4 endpoints): list, create, get, and update notes.
- **FR-006**: SDK MUST provide typed client methods for job tracking (3 endpoints): get tracking (v1), track by PRO number, and tracking v3 with history. Tracking v2 is skipped as a deprecated intermediate version.
- **FR-007**: SDK MUST provide typed client methods for job items and parcels (7 endpoints): update item, add item notes, list/create/delete parcel items, get parcel items with materials, and get packaging containers.
- **FR-008**: Every new endpoint MUST follow the same patterns established in feature 001: Route definitions with frozen dataclasses, request models with `extra="forbid"`, response models with `extra="allow"` and drift logging, snake_case fields with camelCase aliases.
- **FR-009**: Every new response model MUST have a corresponding fixture file in `tests/fixtures/` validated against the Pydantic model. Endpoints where live fixtures cannot be captured MUST be tracked in `MOCKS.md`.
- **FR-010**: Every new endpoint group MUST have Sphinx documentation with description, HTTP method/path, Python code example, and cross-reference to the response model class.
- **FR-011**: Every new endpoint group MUST have a runnable example file in `examples/`.
- **FR-012**: New endpoint groups (forms, shipments, payments) MUST be exposed as attributes on the `ABConnectAPI` client (e.g., `api.forms`, `api.shipments`, `api.payments`). Endpoints extending existing groups (timeline on jobs, notes on jobs, parcels on jobs) MUST be added as methods on the existing endpoint class.
- **FR-013**: A design decisions document MUST be created at `specs/002-extended-endpoints/research.md` documenting architectural choices that depart from ABConnectTools patterns, with explicit references to how ABConnectTools handles the same operations.
- **FR-014**: Form endpoints that return binary content (PDF/HTML) MUST use the same binary response pattern established by `documents.get()` in feature 001.
- **FR-015**: Swagger compliance tests MUST be updated to reflect the newly implemented endpoints, reducing the unimplemented count.

### Key Entities

- **TimelineTask**: A step in a job's lifecycle workflow. Key attributes: task code, status, assigned agent, scheduled/completed dates, and comments. Represents the state machine transitions a job moves through.
- **ShipmentInfo**: Details of a booked or pending shipment. Key attributes: carrier, service type, PRO number, origin/destination addresses, accessorials, rate quote details, and booking status.
- **RateQuote**: A carrier's quoted price for shipping a job. Key attributes: carrier name, service level, price, transit days, and accessorial charges.
- **Accessorial**: An additional service for a shipment (e.g., liftgate, inside delivery). Key attributes: add-on ID, name, description, and price.
- **TrackingInfo**: Current shipment tracking state. Key attributes: status, location, estimated delivery, and a list of tracking events with timestamps.
- **PaymentInfo**: Payment state for a job. Key attributes: total amount, balance due, payment status, and payment history.
- **PaymentSource**: A stored payment method (card or bank account). Key attributes: source ID, type, last four digits, and expiration.
- **JobNote**: A text note attached to a job. Key attributes: note ID, author, timestamp, content, and visibility.
- **ParcelItem**: A packaged item within a job. Key attributes: parcel item ID, dimensions, weight, description, and associated materials.
- **JobForm**: A generated business document (invoice, BOL, etc.). Returns binary content (PDF/HTML) rather than a JSON model.

### Assumptions

- All new endpoints use the same authentication mechanism (Bearer JWT via the existing `HttpClient`) and the same ACPortal base URL pattern (`portal.{env}.abconnect.co/api/api`).
- The shipment global endpoints (`/api/shipment`, `/api/shipment/accessorials`, `/api/shipment/document/{docId}`) use the same ACPortal base URL as job-scoped shipment endpoints.
- Form endpoints return either HTML or PDF binary content; the response content type determines the format. The SDK does not convert between formats.
- Payment endpoints involving Stripe (ACH, bank sources) interact with Stripe indirectly through ABConnect's API — the SDK does not call Stripe directly.
- Timeline task codes and status values follow a fixed set defined by ABConnect's business logic; the SDK models these as string fields rather than strict enums to avoid breaking on new codes.
- Only tracking v3 is implemented (latest, most complete data). Tracking v1 (basic) and v2 (intermediate) are skipped as deprecated API versions.
- ABConnectTools at `/usr/src/pkgs/ABConnectTools/` will be referenced during planning to document design departures, but no code will be copied.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All ~62 new endpoints return validated Pydantic models (or raw bytes for forms), with zero raw-dict responses in the public API.
- **SC-002**: 100% of new endpoints have a fixture file (live or mock) that validates against the corresponding model without error.
- **SC-003**: Sphinx documentation builds with zero warnings and every new endpoint page includes a code example and model cross-reference.
- **SC-004**: `MOCKS.md` is updated to account for every new endpoint where a live fixture is unavailable.
- **SC-005**: Swagger compliance tests show a measurable reduction in unimplemented endpoint count (from ~269 to ~207).
- **SC-006**: A `research.md` design decisions document exists with at least one documented departure from ABConnectTools patterns per new endpoint group.
- **SC-007**: All new endpoint methods are accessible through the `ABConnectAPI` client object without requiring manual instantiation of endpoint classes.
- **SC-008**: Existing tests continue to pass — zero regressions in feature 001 functionality.
