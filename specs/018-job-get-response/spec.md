# Feature Specification: Complete Job Get Response Model

**Feature Branch**: `018-job-get-response`
**Created**: 2026-02-22
**Status**: Draft
**Input**: User description: "run python -m examples jobs get 2000000, note this output is already saved in fixtures. confirm that adequate tests are present to cast a job response to a model without error. research a correct implementation of `jobs get` using the proper sources."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Cast Job API Response Without Extra-Field Warnings (Priority: P1)

As an SDK consumer, when I call `jobs.get(2000000)`, the returned Job model should capture all fields from the API response as typed attributes with zero "unexpected field" warnings. Currently the Job model only defines 6 domain fields (jobDisplayId, status, customer, pickup, delivery, items), leaving 27 additional fields to spill into `model_extra`, each triggering a warning log line.

**Why this priority**: The Job entity is the central domain object in the system. Every downstream consumer (reporting, automation, integrations) depends on reliably accessing job fields by name and type. Unmodeled fields are invisible to IDE autocompletion, static analysis, and test coverage — making the SDK unreliable for its core use case.

**Independent Test**: Can be fully tested by loading the existing `Job.json` fixture, calling `Job.model_validate(data)`, and asserting `assert_no_extra_fields(model)` passes with no warnings logged.

**Acceptance Scenarios**:

1. **Given** the existing `Job.json` fixture (captured from job 2000000), **When** `Job.model_validate(fixture_data)` is called, **Then** the model instance has zero entries in `model_extra` and `assert_no_extra_fields` passes.
2. **Given** the Job model is updated with all 27 missing top-level fields, **When** `python -m examples jobs get 2000000` is run, **Then** zero "unexpected field" warnings appear in the output.
3. **Given** the updated Job model, **When** the existing `test_job` test in `test_job_models.py` runs, **Then** the previously-commented-out `assert_no_extra_fields(model)` call is uncommented and passes.

---

### User Story 2 - Deep Typing for Nested Job Structures (Priority: P2)

As an SDK consumer, when I access nested fields on a Job (e.g., `job.customer_contact.address.city`, `job.job_summary_snapshot.job_total_amount`, `job.sla_info.days`), these should be strongly-typed sub-models rather than opaque `dict` objects. This follows the pattern established by the Companies endpoint in feature 016 (deep pydantic models).

**Why this priority**: Without deep typing, consumers must use dictionary key access for nested data, losing IDE support, type safety, and validation. The companies endpoint already solved this problem — jobs should follow the same pattern.

**Independent Test**: Can be tested by loading the `Job.json` fixture, validating it against the Job model, and asserting that nested objects (customerContact, jobSummarySnapshot, slaInfo, activeOnHoldInfo, documents) are instances of their respective sub-model classes rather than raw dicts.

**Acceptance Scenarios**:

1. **Given** the Job fixture with nested `customerContact` data, **When** the Job model is validated, **Then** `job.customer_contact` is an instance of a typed contact sub-model (not `dict`), and its nested `address`, `email`, and `phone` fields are also typed sub-models.
2. **Given** the Job fixture with nested `jobSummarySnapshot`, **When** the Job model is validated, **Then** `job.job_summary_snapshot` is a typed sub-model with all 24 fields explicitly defined.
3. **Given** the Job fixture with `items` containing nested `materials`, **When** the Job model is validated, **Then** each item in `job.items` is a typed sub-model and `item.materials` is a list of typed material sub-models.

---

### User Story 3 - Adequate Test Coverage for Job Model Casting (Priority: P3)

As a maintainer, I need confidence that the Job model correctly casts the full API response. The existing `test_job` test in `test_job_models.py` has `assert_no_extra_fields` commented out, and the integration test in `test_jobs.py` explicitly notes "Job not yet fully typed — skip extra_fields check." These must be enabled and passing.

**Why this priority**: Tests that skip validation provide a false sense of coverage. Enabling the extra-fields assertion catches API drift immediately and prevents regression.

**Independent Test**: Can be tested by running `pytest tests/models/test_job_models.py -v` and verifying all assertions pass without skips or commented-out checks.

**Acceptance Scenarios**:

1. **Given** the updated Job model with all fields defined, **When** `pytest tests/models/test_job_models.py::TestJobModels::test_job` runs, **Then** `assert_no_extra_fields` is called (not commented out) and passes.
2. **Given** the updated Job model, **When** the integration test `test_get_job` runs, **Then** it includes `assert_no_extra_fields(result)` and passes.
3. **Given** the full test suite, **When** `pytest tests/models/` runs, **Then** no job-related tests contain commented-out assertions or skip markers related to incomplete typing.

---

### Edge Cases

- What happens when the API adds a new field to the Job response that is not yet in the model? The `extra="allow"` base class behavior should continue to work — new fields are captured in `model_extra` and logged as warnings, preserving forward compatibility.
- What happens when a nested object (e.g., `customerContact`) is `null` in the response? All nested sub-model fields must be `Optional` so that null values are handled gracefully.
- What happens when list fields (e.g., `documents`, `items`, `freightProviders`) are empty arrays? The model must accept empty lists without error.
- What happens when nested sub-objects have fields not present in the fixture? Sub-models should also use `extra="allow"` (via `ResponseModel` base class) to remain resilient.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The Job response model MUST define typed fields for all 27 currently-unmodeled top-level fields: `bookedDate`, `ownerCompanyId`, `customerContact`, `pickupContact`, `deliveryContact`, `totalSellPrice`, `freightItems`, `jobSummarySnapshot`, `notes`, `activeOnHoldInfo`, `writeAccess`, `accessLevel`, `statusId`, `jobMgmtSubId`, `isCancelled`, `freightInfo`, `freightProviders`, `expectedPickupDate`, `expectedDeliveryDate`, `timelineTasks`, `documents`, `labelRequestSentDate`, `paymentInfo`, `agentPaymentInfo`, `slaInfo`, `jobType`, `prices`.
- **FR-002**: Nested structures (`customerContact`, `pickupContact`, `deliveryContact`, `jobSummarySnapshot`, `activeOnHoldInfo`, `slaInfo`, and `documents` entries) MUST be represented as dedicated pydantic sub-models rather than `dict` types.
- **FR-003**: The existing `items` field on Job (currently `List[dict]`) MUST be re-typed to use a dedicated `JobItem` sub-model with all fields observed in the fixture (approximately 75 fields per item, including nested `materials`).
- **FR-004**: All model field names MUST use proper aliases matching the API's camelCase keys (e.g., `alias="jobDisplayId"`, `alias="customerContact"`).
- **FR-005**: All previously commented-out `assert_no_extra_fields` calls in job-related tests MUST be enabled and passing.
- **FR-006**: The fixture file `Job.json` (already captured from job 2000000) MUST validate against the updated Job model with zero extra fields.
- **FR-007**: Existing `customer`, `pickup`, and `delivery` fields on Job (currently `Optional[dict]`) SHOULD remain as `Optional[dict]` if they are `null` in the current fixture, unless real data becomes available to type them.

### Key Entities

- **Job**: The central domain entity representing a moving/shipping job. Contains identification (jobDisplayId, statusId), contacts (customerContact, pickupContact, deliveryContact), financial data (totalSellPrice, prices, paymentInfo), logistics (freightItems, freightProviders, freightInfo, timelineTasks), documents, items with materials, on-hold info, and SLA tracking.
- **JobContact**: A nested contact structure with sub-objects for contact details, email, phone, and address. Shared by customerContact, pickupContact, and deliveryContact.
- **JobSummarySnapshot**: Financial and weight rollup summary with 24 fields covering totals, costs, and dimensional data.
- **JobItem**: A line item on a job with packing/crating details, dimensions, materials list, and item metadata (approximately 75 fields).
- **JobDocument**: A document attachment with path, type, tags, and item associations.
- **ActiveOnHoldInfo**: Hold status record with reason, responsible party, and dates.
- **SlaInfo**: Service level agreement tracking with days, dates, and on-hold duration.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Running `python -m examples jobs get 2000000` produces zero "unexpected field" warnings for the Job model.
- **SC-002**: `Job.model_validate(fixture_data)` on the existing `Job.json` fixture results in an empty `model_extra` dictionary.
- **SC-003**: 100% of job model tests pass with `assert_no_extra_fields` assertions enabled (not commented out).
- **SC-004**: All nested sub-models (contact, snapshot, items, documents, on-hold, SLA) are accessible as typed attributes with IDE autocompletion support.
