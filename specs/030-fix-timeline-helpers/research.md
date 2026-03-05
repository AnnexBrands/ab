# Research: 030 — Fix Timeline Helpers

## D1: Replace Single Request Model with Per-Type Models

**Decision**: Replace `TimelineTaskCreateRequest` (4 fields) with three request models matching the C# ground truth: `InTheFieldTaskRequest` (PU/DE), `SimpleTaskRequest` (PK/ST), `CarrierTaskRequest` (CP), sharing a common `BaseTimelineTaskRequest` base.

**Rationale**: The C# server uses `TaskModelDataBinder` which reads `taskCode` from the JSON body and deserializes to one of three different DTOs. Each DTO has different fields. The current `TimelineTaskCreateRequest` only declared 4 fields — none of which match what the helpers actually send (`timeLog`, `onSiteTimeLog`, `completedDate`, etc.). This caused the `extra_forbidden` crash. Per-type models match the server's polymorphic deserialization exactly.

**Alternatives considered**:
- Single fat model with all fields from all three types: Rejected. This would accept `timeLog` on a CP task and `scheduledDate` on a PK task — the server would silently ignore the wrong fields. Per-type models with `extra="forbid"` catch these errors at construction time.
- Removing `request_model` from the Route to bypass validation: Rejected. This violates Constitution Principle IX (Endpoint Input Validation).

## D2: Nested Request Models for TimeLog, WorkTimeLog, etc.

**Decision**: Create nested `RequestModel` subclasses for `TimeLogRequest` (start, end, pauses), `TimeLogPauseRequest` (start, end), and `WorkTimeLogRequest` (date, start_time, end_time). These are used as field types in the task request models.

**Rationale**: The C# source defines `TimeLogModel`, `TimeLogPauseModel`, and `WorkTimeLogModel` as distinct classes with their own validation rules. Using typed nested models instead of `dict` ensures field names are validated at construction time. The existing `TimelineTask` response model uses `dict` for these nested structures — that's fine for responses (`extra="allow"`), but requests must use `extra="forbid"` per the constitution.

**Alternatives considered**:
- Using `dict` for nested structures: Rejected. This bypasses the entire point of Pydantic validation for request bodies.
- Reusing the response model's nested types: Rejected. Response models use `extra="allow"` while request models must use `extra="forbid"`.

## D3: Route Validation Strategy — Remove request_model from Route

**Decision**: Remove `request_model="TimelineTaskCreateRequest"` from `_POST_TIMELINE` Route. The helpers validate by constructing the correct model type directly. The `create_timeline_task()` endpoint method accepts `data: BaseTimelineTaskRequest | dict` — the helpers always pass a model instance, and the model's `.check()` is called in the helper, not in `_request()`.

**Rationale**: The `_request()` pipeline's `request_model` validation assumes a single model class. The timeline POST endpoint accepts three different model types based on `taskCode`. Rather than adding polymorphic dispatch to `_request()` (which would be a framework-level change affecting all endpoints), validation happens in the helper layer where the task type is already known. This is the same pattern used by `AgentHelpers` (feature 029) — the helper constructs a validated payload and passes it as `data=`.

**Alternatives considered**:
- Adding a discriminated union to Route's `request_model`: Viable but requires framework changes to `_request()` and `Route`. Overkill for a single endpoint.
- Keeping `request_model` and using a single fat model: Rejected per D1.

## D4: Type Annotations for IDE Discoverability

**Decision**: Add type annotations `self.tasks: TimelineHelpers` and `self.agent: AgentHelpers` in `JobsEndpoint.__init__`. Use `TYPE_CHECKING` imports to avoid circular import at runtime.

**Rationale**: IDEs (Pylance, PyCharm) rely on type annotations to resolve attribute types. The helpers are already imported at runtime inside `__init__` to avoid circular imports — adding annotations under `TYPE_CHECKING` gives the IDE what it needs without changing runtime behavior.

**Alternatives considered**:
- Moving helper imports to module level: Rejected. Would create circular imports (`helpers` → `JobsEndpoint` → `helpers`).
- Using string annotations: Viable but `TYPE_CHECKING` is the established Python pattern and is already used in the codebase.

## D5: Helper Construction Pattern — Model Instances, Not Dicts

**Decision**: Replace all `_NEW_*_TASK` dict templates and inline dict construction in helpers with model instantiation. Each helper method creates the correct request model type for its task code.

**Rationale**: The `_NEW_*_TASK` dicts were copied from ABConnectTools which itself uses untyped dicts. This SDK's architecture is Pydantic-first with `extra="forbid"` on request models. Building raw dicts defeats the purpose — typos in field names would only be caught when the server rejects them, not at construction time. Model instantiation catches errors immediately.

**Alternatives considered**:
- Keeping dicts but validating via `.check()` in `set_task()`: Partial improvement but still relies on remembering to call `.check()`. Direct model instantiation is safer.

## D6: Response Model — Keep Unified TimelineTask

**Decision**: Keep the existing unified `TimelineTask` response model (all fields from all task types in one class with `extra="allow"`). Do not split into per-type response models with discriminated union.

**Rationale**: The response model already works — `extra="allow"` means extra fields from any task type are accepted. ABConnectTools uses a discriminated union (`TimelineTask = Annotated[Union[...], Discriminator(...)]`) but that adds complexity without benefit for a response model. The unified model lets consumers access any field without type-checking the task code first. If a consumer needs type-specific behavior, they can check `task_code` themselves.

**Alternatives considered**:
- Discriminated union response model (matching ABConnectTools): Viable but adds complexity. The union requires consumers to type-narrow before accessing task-specific fields. The current unified model is simpler and works because `extra="allow"` handles all task types.

## D7: Request Fixture Strategy — One Per Task Type

**Decision**: Create three request fixtures: `InTheFieldTaskRequest.json` (PU task), `SimpleTaskRequest.json` (PK task), `CarrierTaskRequest.json` (CP task). Remove the old `TimelineTaskCreateRequest.json` fixture.

**Rationale**: Each task type has different fields. A single fixture can't represent all three. The existing auto-discovery in `tests/models/test_request_fixtures.py` will validate each fixture against its model class (name must match).

**Alternatives considered**:
- One fixture with a superset of all fields: Rejected. Would fail `extra="forbid"` on any single model.
