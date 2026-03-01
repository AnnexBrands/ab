# Research: Timeline Operations

**Feature**: 024-timeline-operations | **Date**: 2026-02-28

## R1: GET /timeline Response Shape

**Decision**: The API returns a `TimelineResponse` wrapper object, not a bare `List[TimelineTask]`.

**Rationale**: The C# server controller (`JobTimelineController.cs`) returns a `TimelineResponse` which extends `ServiceBaseResponse` and includes `tasks`, `onHolds`, `daysPerSla`, `deliveryServiceDoneBy`, `jobSubManagementStatus`, and `jobBookedDate`. The current Python route declares `response_model="List[TimelineTask]"` which is incorrect — the base client tries to unwrap a list from the response dict, losing the wrapper metadata.

**Alternatives considered**:
- Keep `List[TimelineTask]` and rely on `_unwrap_list_from_dict` to extract the `tasks` key — loses job status metadata needed by helpers.
- Return raw dict — loses type safety.

## R2: Task Code Discrimination

**Decision**: Use a single `TimelineTask` model with all fields from all task types (union of fields), rather than Pydantic discriminated unions.

**Rationale**: The C# ABConnectTools uses a discriminated union pattern (`Union[PickupTask, PackagingTask, StorageTask, CarrierTaskModel]` with `Discriminator`), but the Python SDK's `ResponseModel` uses `extra="allow"` which makes this unnecessary — all fields can coexist on one model since unused fields are simply null. A discriminated union would add complexity (4 model classes + discriminator function) with no practical benefit for an SDK consumer who just reads fields. The C# code itself uses untyped dicts in the helpers.

**Alternatives considered**:
- Discriminated union with Literal taskCode — more type-safe but adds 4 classes and complicates serialization for the POST upsert where you pass raw dicts.
- Separate fixture files per task code — fixture per model makes G1 evaluation complex. Instead, capture individual task types in separate fixture files for validation, but use one unified model.

## R3: TimelineResponse vs List Route

**Decision**: Change the GET timeline route from `response_model="List[TimelineTask]"` to `response_model="TimelineResponse"` and create a new `TimelineResponse` model.

**Rationale**: The helpers need `jobSubManagementStatus` from the wrapper to check current job status before deciding whether to allow a status transition. Without the wrapper, this requires a separate API call.

**Alternatives considered**:
- Two methods: `get_timeline()` returning typed list, `get_timeline_raw()` returning wrapper — unnecessary indirection.

## R4: Timeline Helpers Architecture

**Decision**: Create `ab/api/helpers/timeline.py` as a standalone class that takes a `JobsEndpoint` instance, mirroring the ABConnectTools pattern.

**Rationale**: The helpers need access to `get_timeline()`, `create_timeline_task()`, and `delete_timeline_task()` methods. Making them a separate class keeps the endpoint clean (no business logic in the API layer) and allows independent testing.

**Alternatives considered**:
- Methods directly on JobsEndpoint — bloats the endpoint class with business logic.
- Standalone functions — lose the encapsulation of task templates and state.

## R5: POST /timeline Response Shape

**Decision**: Create a `TimelineSaveResponse` model matching the C# `SaveResponseModel`: `success`, `errorMessage`, `taskExists`, `task`, `emailLogId`, `jobSubManagementStatus`.

**Rationale**: The current route says `response_model="TimelineTask"` but the API returns a wrapper. The helpers need `taskExists` to know if they created or updated, and `jobSubManagementStatus` for status tracking.

## R6: DELETE Response Shape

**Decision**: The DELETE endpoint returns `ServiceBaseResponse` (just `success` + `errorMessage`). Keep current route as-is.

**Rationale**: The C# server's delete action returns `ServiceBaseResponse`, not the richer `DeleteTaskResponse` from ABConnectTools models. The ABConnectTools model adds `jobSubManagementStatus` but this appears to be a client-side enrichment, not a server response field. Verify against live API during fixture capture.

## R7: Task Code Constants

**Decision**: Define task code constants as class-level strings in the helpers class: `PU = "PU"`, `PK = "PK"`, `ST = "ST"`, `CP = "CP"`.

**Rationale**: Simple, matches ABConnectTools pattern. No need for a full Enum class — task codes are just strings used in dict keys.

## R8: Status Code Tracking

**Decision**: The job status is tracked via `jobSubManagementStatus` in the `TimelineResponse` wrapper (a `LookupItem` with `id` and `name`). Status codes (1-10 with sub-statuses 2.1, 2.2, 9.1-9.4) are server-side; helpers check current status by reading the timeline response.

**Rationale**: ABConnectTools helpers use `get_task()` which parses the timeline response to extract current status. The status code comes from `jobSubManagementStatus.name` which contains the numeric code as a string.

## R9: Modified Date Handling

**Decision**: Include `modifiedDate` and `createdDate` on `TimelineTask` (inherited from the base task pattern). The get-then-set pattern in helpers naturally preserves the `modifiedDate` by fetching current state before POSTing updates.

**Rationale**: The C# `BaseTask` extends `TimestampedModel` which provides these fields. Server-side optimistic concurrency uses `modifiedDate` to detect conflicts. The SDK does not need to explicitly set it — the server manages it.
