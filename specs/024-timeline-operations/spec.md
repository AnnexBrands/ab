# Feature Specification: Timeline Operations

**Feature Branch**: `024-timeline-operations`
**Created**: 2026-02-28
**Status**: Draft
**Input**: User description: "lets get timeline working. this needs a heavy amount of research from both ground truth C# and from /opt/pack/ABConnectTools/ABConnect/api/endpoints/jobs/timeline_helpers.py. there are 10 job.jobs.jobmgmtsubid in the db (1-10 plus 2.1,2.2,etc.) - currently _scratch.py has a response model error, but it would otherwise list the statuses. we need methods to get and post all statuses. I have get timeline for test_job_display_id giving each type of response model possible. note that we must get the timeline with the modified date to ensure we are not encountering a race. interrogate the get timeline for each taskcode, ensure we have each type saved. ensure we can delete and post back each task from a fixture. provide a substantially improved set of timeline_helpers so we can pass any value whether or not the task already existed and properly set the value to the api"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Retrieve Timeline with Correct Models (Priority: P1)

A developer calls the SDK to retrieve a job's timeline and receives properly typed task objects — each task code (PU, PK, ST, CP) returns a model with the correct fields for that task type, including modified dates for collision detection.

**Why this priority**: Without correct response models, no other timeline operation can be verified or trusted. This is the foundation for all timeline work.

**Independent Test**: Can be fully tested by calling `get_timeline(TEST_JOB_DISPLAY_ID)` and validating that each returned task is an instance of the correct model with zero extra fields. Delivers accurate, typed timeline data.

**Acceptance Scenarios**:

1. **Given** a job with active timeline tasks, **When** `get_timeline()` is called, **Then** each task is returned as a properly typed model matching its task code (PU, PK, ST, CP) with zero `__pydantic_extra__` fields
2. **Given** a job with a PU (pickup) task, **When** the timeline is retrieved, **Then** the PU task includes `plannedStartDate`, `plannedEndDate`, `completedDate`, `onSiteTimeLog`, `tripTimeLog`, and `modifiedDate`
3. **Given** a job with a PK (packaging) task, **When** the timeline is retrieved, **Then** the PK task includes `timeLog` (with start/end) and `workTimeLogs`
4. **Given** a job with a CP (carrier) task, **When** the timeline is retrieved, **Then** the CP task includes `scheduledDate`, `pickupCompletedDate`, `deliveryCompletedDate`, `expectedDeliveryDate`
5. **Given** any timeline task, **When** retrieved, **Then** it includes `modifiedDate` and `createdDate` for race condition detection

---

### User Story 2 - Capture Fixtures for Every Task Code (Priority: P1)

A developer can run the test suite and have live-captured fixture JSON files for each timeline task type (PU, PK, ST, CP), the timeline agent response, and the full timeline response — enabling offline model validation and quality gate compliance.

**Why this priority**: Fixtures are required for G1/G2 quality gates to pass and for offline testing. Without them, models cannot be verified.

**Independent Test**: Can be fully tested by checking that fixture files exist on disk for each task type, and that each fixture validates against its model with zero extra fields.

**Acceptance Scenarios**:

1. **Given** the test job has timeline tasks for each code, **When** fixtures are captured from live API, **Then** each task type (PU, PK, ST, CP) has a fixture file saved
2. **Given** a captured fixture, **When** validated against its model, **Then** zero `__pydantic_extra__` fields remain
3. **Given** the timeline agent endpoint, **When** called for each task code, **Then** a TimelineAgent fixture is captured and validates cleanly

---

### User Story 3 - Set Any Status Value Idempotently (Priority: P1)

A developer can call a helper method for any job status (2 through 10) and the SDK will correctly create or update the appropriate timeline task — regardless of whether the task already exists — using the get-then-set pattern to prevent race conditions.

**Why this priority**: This is the core operational value of the timeline helpers. Without upsert logic, developers must manually check task existence and handle create-vs-update themselves.

**Independent Test**: Can be tested by calling each status helper (schedule, received, pack_start, pack_finish, storage_begin, carrier_schedule, carrier_pickup, carrier_delivery) and verifying the job status advances correctly.

**Acceptance Scenarios**:

1. **Given** a job at status 1 (new), **When** `schedule()` is called with a start date, **Then** a PU task is created and job advances to status 2
2. **Given** a job at status 2 with an existing PU task, **When** `received()` is called, **Then** the existing PU task is updated (not duplicated) and job advances to status 3
3. **Given** a job at status 3, **When** `pack_start()` is called, **Then** a PK task is created/updated and job advances to status 4
4. **Given** any status transition, **When** the helper is called, **Then** the current task state is fetched first (including `modifiedDate`) before posting the update
5. **Given** a job already past the target status, **When** a lower-status helper is called, **Then** the helper returns None and does not downgrade the job

---

### User Story 4 - Delete and Restore Timeline Tasks (Priority: P2)

A developer can delete individual timeline tasks or all tasks (resetting to status 1), and can recreate tasks from fixture data — enabling test isolation and job state management.

**Why this priority**: Required for test isolation (delete tasks before/after tests) and for operational scenarios like job reset.

**Independent Test**: Can be tested by deleting a task, verifying it's gone, then posting it back from a fixture and verifying it's restored.

**Acceptance Scenarios**:

1. **Given** a job with a PU task, **When** `delete(taskcode="PU")` is called, **Then** the PU task is removed and the response confirms success
2. **Given** a job with multiple tasks, **When** `delete_all()` is called, **Then** all tasks are removed and the job resets to status 1
3. **Given** a deleted task, **When** `set_task()` is called with the fixture data for that task code, **Then** the task is recreated and the job status updates accordingly

---

### User Story 5 - Timeline Quality Gates Pass (Priority: P2)

All timeline-related endpoints pass all 6 quality gates (G1-G6) in the progress report, with correct response models, fixtures, tests, documentation, and parameter routing.

**Why this priority**: Quality gates ensure long-term maintainability and correctness of the SDK. Builds on the fixture and model work from P1 stories.

**Independent Test**: Can be tested by running the progress report generator and verifying all timeline endpoints show PASS for all gates.

**Acceptance Scenarios**:

1. **Given** updated timeline models and fixtures, **When** quality gates are evaluated, **Then** G1 (Model Fidelity) passes for TimelineTask and TimelineAgent
2. **Given** captured fixtures on disk, **When** G2 is evaluated, **Then** G2 (Fixture Status) passes for all timeline endpoints
3. **Given** integration tests with `isinstance` and `assert_no_extra_fields`, **When** G3 is evaluated, **Then** G3 (Test Quality) passes

---

### Edge Cases

- What happens when the API returns an empty timeline (no tasks) for a job at status 1?
- How does the system handle a timeline task with null `modifiedDate` (newly created)?
- What happens when two users simultaneously update the same task (race condition)?
- How does the system handle task codes not in the known set (PU, PK, ST, CP)?
- What happens when `delete_all()` is called on a job that already has no tasks?
- How does the system handle sub-statuses (2.1, 2.2, 9.1-9.4)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST type timeline tasks according to their task code — PU tasks include pickup-specific fields (onSiteTimeLog, tripTimeLog, completedDate), PK tasks include packaging fields (timeLog), ST tasks include storage fields (timeLog), CP tasks include carrier fields (scheduledDate, pickupCompletedDate, deliveryCompletedDate, expectedDeliveryDate)
- **FR-002**: System MUST include `modifiedDate` and `createdDate` on all timeline task models for optimistic concurrency control
- **FR-003**: System MUST provide a `get_task(jobid, taskcode)` method that fetches the current timeline state and returns the specific task with its status info, or None if the task doesn't exist
- **FR-004**: System MUST provide a `set_task(jobid, taskcode, task, createEmail)` method that creates or updates a task using POST, handling both new and existing tasks transparently
- **FR-005**: System MUST provide named helper methods for each status transition: `schedule()` (status 2), `received()` (status 3), `pack_start()` (status 4), `pack_finish()` (status 5), `storage_begin()` (status 6), `carrier_schedule()` (status 7), `carrier_pickup()` (status 8), `carrier_delivery()` (status 10)
- **FR-006**: System MUST fetch current task state (including modifiedDate) before any update to prevent race conditions
- **FR-007**: System MUST prevent status downgrades — if a job is already past the target status, the helper returns None
- **FR-008**: System MUST provide `delete(jobid, taskcode)` and `delete_all(jobid)` methods for removing timeline tasks
- **FR-009**: System MUST capture and store fixture JSON files for each timeline task type from the live API
- **FR-010**: All timeline response models MUST validate against their fixtures with zero `__pydantic_extra__` fields

### Key Entities

- **TimelineTask**: A task on a job's timeline, discriminated by task code (PU, PK, ST, CP), each with code-specific fields plus common fields (id, jobId, modifiedDate, createdDate, notes)
- **TimeLog**: Start/end timestamps with optional pauses, used by PK and ST tasks to track work duration
- **TimelineResponse**: The envelope returned by GET /timeline, containing the task list plus job status metadata (jobSubManagementStatus, daysPerSla)
- **TimelineSaveResponse**: The envelope returned by POST /timeline, containing the created/updated task plus a taskExists flag indicating create vs update
- **Job Status**: An integer (1-10, with sub-statuses like 2.1, 2.2) representing the job's position in the operational workflow, automatically advanced by timeline task changes

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All timeline task types (PU, PK, ST, CP) have response fixtures that validate with zero extra fields
- **SC-002**: Timeline endpoints pass all 6 quality gates in the progress report
- **SC-003**: Each status helper (schedule through carrier_delivery) can advance a job from its prerequisite status to the target status in a single call
- **SC-004**: Delete-and-restore round-trip succeeds — deleting a task and recreating it from fixture data produces an equivalent task
- **SC-005**: The get-then-set pattern is enforced for all update operations — no update is issued without first fetching current state

## Assumptions

- The test job (`TEST_JOB_DISPLAY_ID`) has or can have timeline tasks for all four task codes (PU, PK, ST, CP) on the staging environment
- The API's POST /timeline endpoint handles upsert semantics (create if task doesn't exist, update if it does) as documented in the C# reference
- Sub-statuses (2.1, 2.2, 9.1-9.4) are set automatically by the API based on task field values and do not need explicit SDK support
- The `modifiedDate` field is maintained server-side and does not need to be set by the SDK on outbound requests
- The C# reference implementation in ABConnectTools is the authoritative source of truth for field names, task code behavior, and status transition rules
