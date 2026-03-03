# Research: 029 — Agent Assignment Helpers

## D1: Agent Helper Architecture Pattern

**Decision**: Create `ab/api/helpers/agent.py` with an `AgentHelpers` class attached to `JobsEndpoint` as `self.agent`, following the same pattern as `TimelineHelpers`.

**Rationale**: The codebase already has exactly one helper pattern — `TimelineHelpers` in `ab/api/helpers/timeline.py`. It is instantiated in `JobsEndpoint.__init__` and exposed as `self.timeline`. Agent helpers follow the identical pattern: the class takes a reference to `JobsEndpoint`, uses `self._jobs` to call the underlying route method, and layers code-to-UUID resolution on top. This keeps the endpoint file focused on routes and the helpers file focused on business logic.

**Alternatives considered**:
- Adding `oa()`/`da()` directly to `JobsEndpoint`: Rejected. This conflates low-level route methods with high-level business helpers. The timeline pattern deliberately separates these concerns.
- Creating a nested `ab/api/endpoints/jobs/` package: Rejected. ABConnectTools uses this pattern but the AB SDK uses single-file endpoints. The helper pattern is the established equivalent.

## D2: Route Definition for POST_CHANGE_AGENT

**Decision**: Add `_POST_CHANGE_AGENT = Route("POST", "/job/{jobDisplayId}/changeAgent", request_model="ChangeJobAgentRequest", response_model="ServiceBaseResponse")` to `ab/api/endpoints/jobs.py` alongside the existing timeline routes. The method `change_agent()` follows the `**kwargs` signature pattern.

**Rationale**: All 55 existing jobs routes are defined as module-level `Route` objects in `jobs.py`. The method signature follows the project convention: `def change_agent(self, *, jobDisplayId: str, **kwargs: Any) -> ServiceBaseResponse:`. The `**kwargs` pattern is universal across all endpoint methods (established in feature 007).

**Alternatives considered**:
- Putting the route in the helpers file: Rejected. Routes belong in endpoint files; helpers consume routes, they don't define them.

## D3: ChangeJobAgentRequest Model

**Decision**: Add `ChangeJobAgentRequest` as a `RequestModel` in `ab/api/models/jobs.py` with 4 fields: `service_type` (int), `agent_id` (str), `recalculate_price` (bool), `apply_rebate` (bool). All Optional since the API accepts partial payloads.

**Rationale**: The C# DTO from ABConnectTools (`ABConnect/api/models/job.py:46-53`) defines exactly these 4 fields with camelCase aliases (`serviceType`, `agentId`, `recalculatePrice`, `applyRebate`). The swagger schema confirms the same 4 fields. Using `RequestModel` (which inherits `extra="forbid"`) catches typos per Constitution Principle IX.

**Alternatives considered**:
- Using `ServiceType` enum for `service_type` field type: Viable but adds coupling. The `change()` helper can accept the enum and pass `.value` to the request. The request model itself uses `int` for maximum API compatibility (in case new service types are added server-side before the enum is updated).

## D4: ServiceType Enum

**Decision**: Add `ServiceType(int, Enum)` to `ab/api/models/enums.py` with values: UNDEFINED=0, PICK=1, PACK=2, PICKANDPACK=3, DELIVERY=4. Import and use in `AgentHelpers` but not in the request model.

**Rationale**: The enum exists in ABConnectTools (`ABConnect/api/models/enums.py:269-277`) with identical values. Using an enum in the helper methods provides IDE autocompletion and type safety for callers. The request model uses `int` directly for forward-compatibility.

**Alternatives considered**:
- No enum (raw ints everywhere): Rejected. Callers shouldn't need to remember that 3 = PICKANDPACK.
- Enum in the request model: Rejected per D3 rationale — pydantic would reject unknown future int values.

## D5: Code-to-UUID Resolution in Helpers

**Decision**: `AgentHelpers.__init__` receives the `CodeResolver` from `JobsEndpoint._resolver`. The `change()` method calls `self._resolver.resolve(agent)` before building the request body.

**Rationale**: The `CodeResolver` in `ab/cache.py` already handles the exact same pattern — it checks if the input is a UUID (36 chars, 4 dashes), returns it unchanged if so, otherwise queries the cache service at `https://tasks.abconnect.co/cache/{KEY}`. The `companies.transfer()` method at line 330 of `jobs.py` already uses this exact pattern: `resolved = self._resolver.resolve(franchisee_id)`.

**Alternatives considered**:
- Separate agent-specific resolver: Rejected. The cache service is generic — all entity types (companies, agents) use the same lookup.
- Direct HTTP call to cache: Rejected. `CodeResolver` already handles caching, UUID detection, and error fallback.

## D6: Example and Fixture Strategy

**Decision**: Create `examples/agent.py` with entries for `oa` and `da` using `ExampleRunner`. Request fixture: `ChangeJobAgentRequest.json` in `tests/fixtures/requests/`. Response fixture: `ServiceBaseResponse.json` already exists (from commodity-map DELETE). If staging is available, capture live fixtures; otherwise create mock fixtures in `tests/fixtures/mocks/`.

**Rationale**: Constitution Principle II requires runnable examples. The `ExampleRunner` pattern with `endpoint_attr` auto-discovers Route metadata. ABConnectTools has `examples/api/agent.py` with the same structure. The response model (`ServiceBaseResponse`) already has a fixture from a prior endpoint — the test stub generator already skips it due to G1 issues (documented in 028 PR analysis).

**Alternatives considered**:
- Adding agent examples to the existing `examples/jobs.py`: Rejected. Agent operations are a distinct sub-group with their own helper class — a separate example file keeps discoverability clean.

## D7: README UAT Guide Structure

**Decision**: Add two new sections to README.md: (1) an updated endpoint groups table row for `api.jobs.agent`, and (2) a comprehensive "Agent Responsibilities & UAT Guide" section covering test execution, progress scripts, troubleshooting, and remediation.

**Rationale**: The user explicitly requested README coverage of agent responsibilities and UAT. The guide should be actionable — specific commands, expected outputs, and decision trees for common failures. This captures the tribal knowledge currently distributed across spec files and PR analyses.

**Sections in the UAT guide**:
1. Running the full test suite (`pytest --tb=line -q`)
2. Expected output (pass/skip/xfail counts, zero failures)
3. Running quality gate checks (`python scripts/update_gate_baseline.py`)
4. Regenerating FIXTURES.md (`python scripts/generate_progress.py --fixtures`)
5. Common failure patterns and remediation:
   - Gate regression: what it means, how to fix, when to update baseline
   - Fixture missing: how to capture via examples
   - Model mismatch: extra fields, how to investigate
   - FIXTURES.md drift: how to regenerate and verify

**Alternatives considered**:
- Separate CONTRIBUTING.md: Viable but the user specifically said "make sure readme.md covers" this content. A future refactor could extract it if the README grows too large.
