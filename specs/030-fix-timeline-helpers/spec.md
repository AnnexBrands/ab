# Feature Specification: Fix Timeline Helpers

**Feature Branch**: `030-fix-timeline-helpers`
**Created**: 2026-03-03
**Status**: Draft
**Input**: User description: "using api.jobs.tasks fails to load methods and func signatures in an IDE importing the library. Running pack_start(job, start) gave pydantic error Extra inputs are not permitted. We should not be building a dict here, we should be casting an object."

## Clarifications

### Session 2026-03-03

- Q: What does the API actually accept for POST /timeline? → A: The C# server uses polymorphic deserialization via `TaskModelDataBinder`. Three concrete models: `InTheFieldTaskModel` (PU/DE), `SimpleTaskModel` (PK/ST default), `CarrierTaskModel` (CP). Each has different fields. The existing `TimelineTaskCreateRequest` (4 fields) is wrong — it was a stub, not the real schema.
- Q: Should we keep raw dict templates? → A: No. The `_NEW_*_TASK` dicts were copied from ABConnectTools which itself uses untyped dicts. This SDK must use proper Pydantic request models per task type, matching the C# ground truth.

## User Scenarios & Testing

### User Story 1 — Proper Request Models Per Task Type (Priority: P1)

The API's POST `/job/{jobDisplayId}/timeline` endpoint uses polymorphic deserialization: the server reads `taskCode` from the JSON body and deserializes to one of three C# DTOs. The SDK must mirror this with three distinct Pydantic request models, each declaring exactly the fields that task type accepts. The current `TimelineTaskCreateRequest` (4 generic fields) must be replaced with task-type-specific models.

The three task model types (from C# ground truth):

- **InTheFieldTaskRequest** (maps to C# `InTheFieldTaskModel`; taskCode=PU or DE): `planned_start_date`, `planned_end_date`, `preferred_start_date`, `preferred_end_date`, `on_site_time_log` (nested TimeLog), `trip_time_log` (nested TimeLog), `completed_date`, `truck` (nested TaskTruckInfo), plus base fields (`task_code`, `work_time_logs`, `initial_note`, `planned_start_date`)
- **SimpleTaskRequest** (maps to C# `SimpleTaskModel`; taskCode=PK or ST): `time_log` (nested TimeLog), plus base fields
- **CarrierTaskRequest** (maps to C# `CarrierTaskModel`; taskCode=CP): `scheduled_date`, `pickup_completed_date`, `delivery_completed_date`, `expected_delivery_date`, plus base fields

Base fields shared by all three: `task_code` (required), `planned_start_date`, `work_time_logs` (list of WorkTimeLog), `initial_note` (nested InitialNote)

Nested models: `TimeLogModel` (start, end, pauses list), `TimeLogPauseModel` (start, end), `WorkTimeLogModel` (date, start_time, end_time), `InitialNoteModel` (comments required, due_date, is_important, is_completed, send_notification), `TaskTruckInfo` (id, name, is_active)

**Why this priority**: This is the root cause of the runtime crash. The current `TimelineTaskCreateRequest` has the wrong fields. Every timeline helper fails because the model doesn't match what the API expects. Replacing it with correct per-type models fixes the crash and enforces type safety.

**Independent Test**: Call `api.jobs.tasks.pack_start(job_id, "2026-03-03T11:00:00")` against staging. The helper constructs a `SimpleTaskRequest` instance with `task_code="PK"` and `time_log=TimeLogRequest(start=...)`, validates it, sends it, and returns a `TimelineSaveResponse`.

**Acceptance Scenarios**:

1. **Given** a valid job and datetime, **When** the user calls `pack_start(job, start)`, **Then** the helper constructs a `SimpleTaskRequest` with `task_code="PK"` and `time_log.start` set, the model passes `extra="forbid"` validation, and the API returns success.
2. **Given** a valid job and datetime, **When** the user calls `schedule(job, start)`, **Then** the helper constructs an `InTheFieldTaskRequest` with `task_code="PU"` and `planned_start_date` set.
3. **Given** a valid job and datetime, **When** the user calls `carrier_schedule(job, start)`, **Then** the helper constructs a `CarrierTaskRequest` with `task_code="CP"` and `scheduled_date` set.
4. **Given** a raw dict passed directly to `create_timeline_task()`, **When** the endpoint receives it, **Then** the dict is passed through without model validation (D3 — callers bypassing helpers accept this trade-off).

---

### User Story 2 — IDE Discovers Timeline Helper Methods and Signatures (Priority: P2)

An SDK consumer types `api.jobs.tasks.` in their IDE and expects autocomplete suggestions for all timeline methods with full parameter signatures. Currently `self.tasks` and `self.agent` in `JobsEndpoint.__init__` lack type annotations, so IDEs cannot resolve the types.

**Why this priority**: Developer experience — the code works at runtime (once P1 is fixed) but the IDE cannot discover the API surface.

**Independent Test**: Type `api.jobs.tasks.` in VS Code with Pylance and verify autocomplete shows all `TimelineHelpers` methods with parameter names and types.

**Acceptance Scenarios**:

1. **Given** a properly configured IDE, **When** the user types `api.jobs.tasks.`, **Then** the IDE shows autocomplete for all `TimelineHelpers` methods.
2. **Given** a properly configured IDE, **When** the user types `api.jobs.agent.`, **Then** the IDE shows autocomplete for all `AgentHelpers` methods.
3. **Given** the type annotations, **When** the IDE inspects a method like `pack_start`, **Then** it shows the full signature with parameter names, types, and return type.

---

### User Story 3 — Timeline Helpers Construct Model Objects (Priority: P3)

The timeline helpers must construct proper Pydantic model instances instead of raw dicts. The `_NEW_*_TASK` dict templates must be replaced with model construction. Each helper method should instantiate the correct task model for its task code, set the relevant fields, and pass the model to `set_task()`.

**Why this priority**: Architectural quality — eliminates the raw dict pattern that caused the original crash and ensures all payloads are validated at construction time.

**Independent Test**: Read the timeline helpers source and verify no raw dict construction (`{"taskCode": ...}`) remains. All payloads are built via model instantiation.

**Acceptance Scenarios**:

1. **Given** a helper method like `pack_start()`, **When** it builds the task payload, **Then** it instantiates `SimpleTaskRequest(task_code="PK", time_log=TimeLogRequest(start=...))` — not a raw dict.
2. **Given** the get-then-set pattern (`get_task` returns a response dict), **When** a helper updates a task, **Then** it constructs a fresh request model from the relevant response fields rather than mutating and passing the response dict back.

---

### User Story 4 — Accurate Response Model for Timeline Tasks (Priority: P4)

The `TimelineSaveResponse` and `TimelineResponse` models must accurately represent the API response, including discriminated task types in the response body. The save response includes `task` (the created/updated task), `task_exists`, `email_log_id`, and `job_sub_management_status`. The list response returns a list of tasks that should be parsed into the correct task type based on `taskCode`.

**Why this priority**: Response model accuracy ensures the SDK consumer gets properly typed task objects back, not unvalidated dicts.

**Independent Test**: Call `api.jobs.get_timeline(job_id)` and verify the response contains properly typed task objects (InTheFieldTask, SimpleTask, CarrierTask) based on each task's `taskCode`.

**Acceptance Scenarios**:

1. **Given** a timeline response containing tasks with different `taskCode` values, **When** the response is parsed, **Then** each task is deserialized into the correct response model type.
2. **Given** a save response after creating a PK task, **When** the response is parsed, **Then** `response.task` is a properly typed task object with `time_log` fields accessible.

---

### Edge Cases

- What happens when a task field is `None`? Optional fields are excluded from the serialized payload via `.check(exclude_none=True)`.
- What happens when `get_task()` returns a response dict with extra fields (`id`, `createdDate`, etc.) not in the request model? The helpers must construct a fresh request model, not pass the response dict back. Only the fields relevant to the update should be set on the new request.
- What happens when an unknown `taskCode` is passed? The validation should reject it — only "PU", "PK", "ST", "CP" (and optionally "DE") are valid.
- What happens when `create_timeline_task()` receives a raw dict? Per D3, raw dicts bypass model validation — the Route has no `request_model`. Callers using helpers get validation via model construction. Direct callers accept the trade-off.

## Requirements

### Functional Requirements

- **FR-001**: The SDK MUST define three distinct request models matching the C# ground truth: `InTheFieldTaskRequest` (PU/DE), `SimpleTaskRequest` (PK/ST), and `CarrierTaskRequest` (CP), all sharing a common base with `task_code`, `planned_start_date`, `work_time_logs`, and `initial_note`. These replace the existing `TimelineTaskCreateRequest`.
- **FR-002**: The SDK MUST define nested request models for `TimeLogModel` (start, end, pauses), `TimeLogPauseModel` (start, end), `WorkTimeLogModel` (date, start_time, end_time), `InitialNoteModel` (comments, due_date, is_important, is_completed, send_notification), and `TaskTruckInfo` (id, name, is_active).
- **FR-003**: All timeline helper methods MUST construct proper Pydantic model instances — no raw dict construction with camelCase keys.
- **FR-004**: The `_NEW_*_TASK` dict templates MUST be removed and replaced with model construction in each helper method.
- **FR-005**: The `self.tasks` and `self.agent` attributes in `JobsEndpoint.__init__` MUST have type annotations for IDE discoverability.
- **FR-006**: Timeline task payloads MUST be validated by constructing the correct per-type model in the helper layer (D3). The `_POST_TIMELINE` Route MUST NOT declare a `request_model` — polymorphic dispatch happens in helpers, not `_request()`. The `create_timeline_task()` endpoint method MUST accept `BaseTimelineTaskRequest | dict` and SHOULD document that callers passing raw dicts bypass model validation.
- **FR-007**: Response models (`TimelineSaveResponse`, `TimelineResponse`) MUST accurately represent the API response, including discriminated task types in the `task`/`tasks` fields.
- **FR-008**: Request fixtures MUST be created for each task model type (one per task code).
- **FR-009**: All existing tests MUST continue to pass with zero regressions.
- **FR-010**: *(Merged into FR-001)* The old `TimelineTaskCreateRequest` model (4 fields) MUST be replaced — not expanded — with the correct per-type models.

### Key Entities

- **BaseTimelineTaskRequest**: Shared base request model with `task_code` (required), `planned_start_date`, `work_time_logs`, `initial_note`.
- **InTheFieldTaskRequest**: Request model for PU/DE tasks — adds `planned_end_date`, `preferred_start_date`, `preferred_end_date`, `on_site_time_log`, `trip_time_log`, `completed_date`, `truck`.
- **SimpleTaskRequest**: Request model for PK/ST tasks — adds `time_log`.
- **CarrierTaskRequest**: Request model for CP tasks — adds `scheduled_date`, `pickup_completed_date`, `delivery_completed_date`, `expected_delivery_date`.
- **TimeLogModel**: Nested model with `start`, `end`, `pauses` (list of TimeLogPauseModel).
- **WorkTimeLogModel**: Nested model with `date`, `start_time`, `end_time`.
- **InitialNoteModel**: Nested model with `comments` (required), `due_date`, `is_important`, `is_completed`, `send_notification`.
- **TaskTruckInfo**: Nested model with `id`, `name`, `is_active`.
- **TimelineSaveResponse**: Response from POST timeline — includes `success`, `task_exists`, `task` (discriminated by taskCode), `email_log_id`, `job_sub_management_status`.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Calling `api.jobs.tasks.pack_start(job, start)` succeeds without Pydantic validation errors when tested against staging.
- **SC-002**: All 9 timeline status helper methods execute without Pydantic errors against staging.
- **SC-003**: Typing `api.jobs.tasks.` in an IDE shows autocomplete for all `TimelineHelpers` methods with parameter names and types.
- **SC-004**: Typing `api.jobs.agent.` in an IDE shows autocomplete for all `AgentHelpers` methods.
- **SC-005**: All existing tests continue to pass (zero regressions).
- **SC-006**: Request fixtures for each task type validate against their respective models.
- **SC-007**: Zero raw dict templates (`_NEW_*_TASK`) remain in the timeline helpers source.
- **SC-008**: *(Deferred — US4, D6)* The `TimelineSaveResponse` model correctly parses the `task` field into the right task type based on `taskCode`. Current release uses unified `TimelineTask` with `extra="allow"`, which works for all task types.

## Assumptions

- The C# `TaskModelDataBinder` routing logic (`PU`/`DE` → InTheFieldTaskModel, `CP` → CarrierTaskModel, default → SimpleTaskModel) is the definitive source of truth for which fields each task type accepts.
- The nested models (`TimeLogModel`, `WorkTimeLogModel`, etc.) use the same camelCase serialization as all other SDK models.
- The `_POST_TIMELINE` Route's `request_model` is removed (D3). Validation happens at model construction in the helper layer, not in `_request()`. Direct callers of `create_timeline_task()` passing raw dicts bypass model validation.
- The `ChangeJobAgentRequest` export fix (already applied to `ab/api/models/__init__.py` in this session) will be included in this branch's commit.
- ABConnectTools' `TimelineHelpers` pattern (get-then-set with status checks) is correct and should be preserved — only the dict-building aspect changes to model construction.
