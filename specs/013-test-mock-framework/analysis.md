# PR Analysis: Unified Test Mock Framework (#13)

**Branch**: `013-test-mock-framework` | **Date**: 2026-02-22
**Reviewer**: Claude Opus 4.6 (automated analysis)
**Diff**: 72 files changed, +1,854 / -180

---

## Code Quality Grade: **B+**

A solid infrastructure PR that cleans up significant technical debt (13 failures, 32 xfails, duplicated constants) while introducing a well-scoped mock fixture fallback. The work is methodical, follows existing patterns, and leaves the test suite green. Docked from A for a few design concerns noted below.

---

## Spec Adherence

| Success Criterion | Target | Actual | Verdict |
|---|---|---|---|
| SC-001: Zero model test skips (offline) | 0 skips | 73 skips remain | PARTIAL — mock fixtures (T024) not yet authored |
| SC-002: 13 failures resolved | 0 failures | 0 failures | PASS |
| SC-002: 32 xfails triaged | 0 xfails | 0 xfails | PASS |
| SC-003: No duplicate constants | 0 duplicates | 0 duplicates | PASS |
| SC-004: Sphinx builds offline | Builds clean | Builds clean | PASS |
| SC-005: Mock authoring pattern clear | Documented | Pattern in place, dir exists | PASS |
| SC-006: G2 coverage >= 50% | 50% | 18.6% | NOT MET — requires T024 |

**Assessment**: 4/6 criteria fully met. SC-001 and SC-006 depend on T024 (manual mock fixture authoring), which is explicitly deferred to the user. The infrastructure to satisfy both is in place and verified. This is acceptable per the spec clarification that mock fixtures are "manually authored by me."

---

## Constitution Compliance

| Principle | Status | Notes |
|---|---|---|
| I. Pydantic Model Fidelity | PASS | 139 new model fields across 6 models, all `Optional` with proper aliases. `extra="allow"` on ResponseModel preserved. |
| II. Example-Driven Fixture Capture | JUSTIFIED DEVIATION | Mock fixtures stored in separate `mocks/` subdirectory. Live always takes precedence. Provenance is machine-readable by directory. Spirit preserved. |
| III. Four-Way Harmony | PASS | Model fixes (impl) + example imports (example) + test fixes (test) + Sphinx build verified (docs). All four artifacts touched. |
| IV. Swagger-Informed, Reality-Validated | PASS | params_model classes derived from swagger. Model fields derived from live fixtures. PropertyType and UserRole corrected to match reality over swagger. |
| V. Endpoint Status Tracking | JUSTIFIED DEVIATION | G2 gate now reports "live fixture" vs "mock fixture" provenance. FIXTURES.md regenerated. Mock-backed tests execute instead of skipping — acceptable per complexity tracking. |
| VI. Documentation Completeness | PASS | Sphinx builds clean. `docs/api/users.md` updated for UserRole type change. |
| VIII. Phase-Based Context Recovery | PASS | Work organized into 7 phases. tasks.md uses checkbox tasks. 28/29 tasks checked off. |
| IX. Endpoint Input Validation | PASS | 32 new `RequestModel` subclasses with `extra="forbid"` for query param validation across 13 endpoint files. |

**Verdict**: Constitution is coherent with the plan. The two deviations (Principles II and V) are documented in the plan's Complexity Tracking table with clear rationale. Neither violates the spirit of the principles.

---

## Balls and Strikes

### Hits

1. **Mock fallback is clean and minimal** (`conftest.py`). The `_resolve_fixture_path()` helper is 8 lines, handles both live and mock with no overengineering. The existing `load_fixture` and `require_fixture` APIs are preserved — zero breaking changes to existing tests.

2. **G2 gate provenance reporting** (`gates.py`). Adding "live fixture" vs "mock fixture" to the GateResult reason is thoughtful. Downstream tooling can distinguish fixture sources without inspecting the filesystem.

3. **CompanyDetails +97 fields** is the right approach. Accepting both the flat `/details` and nested `/fulldetails` response shapes in one model with `extra="allow"` is pragmatic. The `_flat` suffix for alias conflicts (`companyID` vs `companyId`) is a clean solution to the snake_case collision.

4. **Constants consolidation** across 15 example files. Simple, boring, correct. Every example now imports from `tests/constants.py`. No more drift.

5. **PropertyType and UserRole fixes** demonstrate "reality over swagger" (Principle IV). Changing `response_model` to `"int"` and `"List[str]"` respectively, then leveraging the existing primitive-type shortcut in `base.py`, is the right fix.

6. **test_search_by_details resilience**. Wrapping the server error in `pytest.skip()` for HTTP 500s is correct — staging instability shouldn't fail the test suite.

### Misses

1. **test_search returns a dict, not List[JobSearchResult]**. The `GET /job/search?jobDisplayId=X` route has `response_model="List[JobSearchResult]"` but the API returns a single object. The test now accepts both shapes, which is defensive, but the Route's `response_model` is arguably wrong. The `base.py` line 94-97 silently returns raw dicts when `is_list=True` but the response isn't a list — this is a silent fallthrough, not an explicit design decision. **Suggestion**: Either change the Route to `response_model="JobSearchResult"` or document the polymorphic behavior.

2. **test_get_seller now makes 2 API calls**. Fetching the list first then getting by ID is correct for resilience, but it doubles the network calls in an integration test. If the list endpoint is slow or returns many items, this adds latency. Minor, but worth noting — consider caching the seller ID in a session-scoped fixture if this becomes a problem.

3. **`exclude_unset=True` in `check()` caused silent field drops** (the `search_by_details` 400 error). This is a pre-existing design issue, not introduced by this PR, but the PR surfaced it. The `JobSearchRequest` model has default values for `page_no`, `page_size`, and `sort_by`, but `check()` strips them because they're "unset." The test works around it by passing all fields explicitly. **This is a ticking bomb for other POST endpoints** — any RequestModel with defaults for required API fields will silently drop them. Consider whether `exclude_unset=False` should be the default for RequestModel, or at least document the footgun.

4. **CompanyDetails has 111+ fields**. This model is getting unwieldy. Both the nested (`fulldetails`) and flat (`details`) shapes coexist in one class. This works because `extra="allow"` and all fields are Optional, but it makes the model harder to reason about. Not blocking, but a future refactor into `CompanyFullDetails` and `CompanyFlatDetails` with a shared base might be cleaner.

5. **Some params_model classes have debatable field types**. For example, `TrackingV3Params` has `history_amount` as a query param, but the agent noted `{historyAmount}` appears in the URL template — making it a path parameter, not a query param. The params_model was added per task spec, but the Route's `.bind()` already handles it as a path parameter. This is harmless (the param is sent twice: in the path and as a query param) but semantically imprecise.

---

## User Stories Effectiveness

| Story | Priority | Status | Effectiveness |
|---|---|---|---|
| US1: Centralized Constants | P1 | Complete | High. Simple, well-scoped, no ambiguity. 15 files cleaned up. |
| US2: Offline Model Validation | P2 | Infrastructure done, content pending (T024) | Medium. The infrastructure is solid but the value isn't realized until mock fixtures are authored. |
| US3: Sphinx Documentation | P3 | Complete | High. Verified clean build. |
| US4: Resolve Failures | P1 | Complete | High. 13 failures -> 0, 32 xfails -> 0. Largest and most impactful story. |

The priority ordering (P1: US1+US4 as MVP, then P2, then P3) was effective. US4 consumed ~70% of the work but delivered the highest-impact outcome.

---

## Progress Toward Project Goals

The ABConnect SDK project tracks quality across 161 endpoints using five gates (G1-G5). This PR's impact:

| Gate | Before | After | Delta |
|---|---|---|---|
| G1 (Model Fidelity) | Multiple failures | PropertyType, UserRole, CompanyDetails, ContactSimple, CatalogExpandedDto, LotDto all fixed | +6 models corrected |
| G2 (Fixture Status) | 22% (35/161) | 18.6% (30/161)* | Slight regression in % due to fixture tracking recalculation; mock infra in place |
| G3 (Test Quality) | 13 failures, 32 xfails | 0 failures, 0 xfails | Clean suite |
| G4 (Doc Accuracy) | Sphinx builds | Sphinx builds, UserRole docs updated | Maintained |
| G5 (Param Routing) | 32 routes missing params_model | 0 routes missing params_model | +32 params_model classes |

*G2 percentage will jump significantly when T024 mock fixtures are authored.

The SDK now has **zero test failures** and **complete G5 param routing coverage** — two significant quality milestones.

---

## Suggested Next Steps

1. **T024: Author mock fixtures** (immediate). This is the one remaining task. Author ~45 mock JSON files in `tests/fixtures/mocks/` to bring G2 coverage above 50%. Prioritize models needed for offline CI. This is the fastest path to satisfying SC-001 and SC-006.

2. **Investigate `check(exclude_unset=True)` default** (near-term). The silent field-drop behavior is a latent bug for any POST endpoint with RequestModel defaults. Consider changing the default to `exclude_unset=False` for `RequestModel` subclasses, or adding a validation step that warns when required API fields would be stripped.

3. **Fix Route response_model for `GET /job/search`** (low priority). The Route says `List[JobSearchResult]` but the API returns a single object. This is a minor correctness issue that doesn't affect runtime but makes the type contract misleading.

4. **Consider CompanyDetails refactor** (future cycle). Splitting into nested vs flat variants would improve readability and make the model contract clearer. Not urgent — the current unified model works.

5. **Next feature cycle candidates**:
   - **Fixture capture sprint**: Run all examples against staging to convert mock fixtures to live fixtures, improving G2 from mock-backed to live-backed.
   - **Request model coverage**: Extend the params_model pattern to request bodies — several POST endpoints still accept raw dicts instead of validated RequestModels.
   - **CI pipeline integration**: Now that the mock infrastructure exists, set up CI to run `pytest tests/models/` without staging credentials as a required check.
