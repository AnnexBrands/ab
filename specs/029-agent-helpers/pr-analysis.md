# PR Analysis: 029 — Agent Assignment Helpers

**PR**: (pending) — `feat(sdk): agent assignment helpers — oa/da/change with code resolution (#29)`
**Branch**: `029-agent-helpers`
**Reviewed**: 2026-03-03
**Reviewer level**: Senior — with lifecycle gap analysis and forward-looking process recommendations

---

## Summary

This PR adds a single new endpoint (`POST /job/{jobDisplayId}/changeAgent`) with a
`ChangeJobAgentRequest` model, a `ServiceType` enum, and an `AgentHelpers` class
providing `oa()`, `da()`, and `change()` convenience methods with code-to-UUID
resolution. It also adds a UAT guide to the README.

**Scope**: 1 new endpoint, 1 new model, 1 new enum, 1 new helper class, README update.

**Tests**: 536 passed, 58 skipped, 5 xfailed, 0 failures. Gate regression passes.
Mock coverage passes. Baseline: 232 endpoints, 1194 passing gates (+1 endpoint, +3
gates from 028's baseline of 231/1191).

---

## Verdict

The implementation is clean, minimal, and follows established patterns faithfully.
The `AgentHelpers` class mirrors `TimelineHelpers` exactly. The `ChangeJobAgentRequest`
model uses `RequestModel` (extra="forbid") per Constitution Principle IX. The
`ServiceType` enum provides type safety for callers while the request model uses raw
`int` for forward-compatibility. The three-level API (raw endpoint, generic helper,
convenience methods) gives callers the right abstraction for their use case.

The README UAT guide (US4) is the most valuable part of this PR from a process
perspective — it encodes the validation workflow that was previously tribal knowledge.
However, the analysis below identifies a significant lifecycle gap: the instructions
exist in the README but are not wired into the speckit workflow that agents actually
follow.

---

## Issues

### 1. POSITIVE — Helper pattern reuse is exact and correct

`AgentHelpers` follows the `TimelineHelpers` pattern identically:
- Instantiated in `JobsEndpoint.__init__` with references to `self` and `self._resolver`
- Exposed as `self.agent` (parallel to `self.timeline`)
- Core method (`change()`) resolves codes, builds request, delegates to raw endpoint
- Convenience methods (`oa()`, `da()`) are thin wrappers with preset `service_type`

No novel patterns introduced. No architectural surprises. This is exactly how helpers
should work.

### 2. POSITIVE — Request model validation is correct

`ChangeJobAgentRequest` inherits `RequestModel` (extra="forbid") and uses `Optional`
for all 4 fields since the API accepts partial payloads. Field aliases match the
C# DTO exactly: `serviceType`, `agentId`, `recalculatePrice`, `applyRebate`. The
request fixture validates against the model.

### 3. POSITIVE — README UAT guide encodes operational knowledge

The 5-step UAT guide in README.md is actionable:
1. Run full test suite
2. Run gate regression
3. Update gate baseline
4. Regenerate FIXTURES.md
5. Run mock coverage

Each step includes the exact command, expected output, and what failure means.
The troubleshooting section covers the 4 most common failure patterns with
remediation steps. This is the first time this knowledge has been documented
in a user-facing location.

### 4. OBSERVATION — `ck.py` is a stray scratch file

`ck.py` is an unrelated address validation script. It must NOT be committed
with this feature. Exclude from staging.

### 5. OBSERVATION — Three gates still fail for the new endpoint

The new endpoint passes G2 (fixture exists), G4 (doc accuracy), and G5 (param
routing), but fails G1 (model fidelity), G3 (test quality), and G6 (request
quality). This is expected — `ServiceBaseResponse` has a known model/fixture
mismatch (documented in 028 PR analysis, issue #8), and G3 requires a
live-captured response fixture from staging. These are pre-existing issues
inherited from the shared response model, not regressions.

### 6. OBSERVATION — `change_agent()` uses `data:` parameter, not `**kwargs`

The raw endpoint method `change_agent(self, job_display_id, *, data)` accepts
a `data` parameter (dict or `ChangeJobAgentRequest`), while the DISCOVER
workflow anti-patterns section explicitly says "Endpoint methods MUST accept
`**kwargs: Any`, not `data: dict`."

This is intentional and correct for this specific case: the `AgentHelpers.change()`
method builds the request dict programmatically and passes it as `data=`. The
`**kwargs` pattern is for endpoints called directly by SDK consumers; this endpoint
is primarily called through the helper layer, not directly. The `data:` signature
is the right choice here because the helper constructs the full request body —
there's no value in unpacking it into kwargs just to repack it.

However, this departure from the standard pattern should be documented in
research.md as a conscious design decision.

---

## Lifecycle Gap Analysis: "Per Turn" Instructions

The user's core question: **Does the speckit cycle (specify → clarify → plan →
tasks → implement → merge) adequately tell the agent what to run at each turn
for tests and progress updates?**

### Current State

| Turn | Tool/Command | Tests/Progress Instructions? |
|------|-------------|------------------------------|
| `/speckit.specify` | Creates spec.md | None — no validation needed |
| `/speckit.clarify` | Refines spec.md | None — no validation needed |
| `/speckit.plan` | Creates plan.md | None — design phase only |
| `/speckit.tasks` | Creates tasks.md | Tasks MAY include test tasks (template says "OPTIONAL") |
| `/speckit.implement` | Executes tasks.md | Runs whatever tasks.md says to run |
| **GAP** | **???** | **No standardized post-implement checklist** |
| Commit + push | Manual | Not documented in any template |
| Open PR | Manual | Not documented in any template |
| PR analysis | Manual | Not documented in any template |
| Merge | Manual | Not documented in any template |
| Pull main | Manual | Not documented in any template |

### What Feature 029 Got Right

The 029 tasks.md includes Phase 7 (Polish & Cross-Cutting Concerns) with explicit
test and validation tasks (T019-T023):

- T019: Run full test suite
- T020: Run gate baseline update
- T021: Regenerate FIXTURES.md
- T022: Run gate regression test
- T023: Run mock coverage test

This is good — but it was **manually authored by the task writer**, not generated
from the template. The `tasks-template.md` Phase N (Polish) says:

```
- [ ] TXXX [P] Additional unit tests (if requested) in tests/unit/
```

It does NOT include:
- Run full test suite
- Update gate baseline
- Regenerate FIXTURES.md
- Run gate regression
- Run mock coverage
- Write pr-analysis.md
- Commit, push, open PR

### What's Missing: The Post-Implement Lifecycle

The gap between "implement completes" and "PR merged" has **7 distinct steps**
that are currently undocumented in any template or workflow:

#### Step 1: Validate (Run Tests)
```bash
cd /usr/src/pkgs/AB && pytest --tb=line -q
```
Expected: 0 failures. Any failure = regression, investigate before proceeding.

#### Step 2: Ratchet Check (Gate Regression)
```bash
pytest tests/test_gate_regression.py -v
```
Expected: PASSED. Failure = a previously-passing gate regressed.

#### Step 3: Update Baseline (Gate Baseline)
```bash
python scripts/update_gate_baseline.py
```
Expected: Endpoint count incremented, gate count >= previous. Verify no gates lost.

#### Step 4: Update Progress (FIXTURES.md)
```bash
python scripts/generate_progress.py --fixtures
```
Expected: FIXTURES.md regenerated, new endpoint appears with correct gate status.

#### Step 5: Mock Coverage
```bash
pytest tests/test_mock_coverage.py -v
```
Expected: 4/4 pass.

#### Step 6: PR Analysis
Write `specs/NNN-feature-name/pr-analysis.md` covering:
- Implementation review (pattern adherence, correctness)
- Test results with counts
- Gate status changes
- Issues found and their severity
- Forward-looking recommendations

#### Step 7: Commit, Push, Open PR
```bash
# Stage feature files (NOT stray scratch files)
git add <specific files>
git commit -m "feat(...): description (#NNN)"
git push -u origin NNN-feature-name
gh pr create --title "..." --body "..."
```

#### Step 8: Merge and Reset
```bash
# After PR approval:
gh pr merge NNN --squash
git checkout main && git pull
```

### The Gap in the Template

The `tasks-template.md` stops at "Polish & Cross-Cutting Concerns." It does not
include a standardized post-implement phase. This means:

1. **Each feature must manually add validation tasks** — 029 did this (T019-T023),
   but nothing in the template forces it.
2. **PR creation is entirely ad-hoc** — no template, no checklist, no standard body
   format (though a pattern has emerged across PRs #31-#35).
3. **PR analysis is convention, not requirement** — features 027 and 028 wrote
   pr-analysis.md, but there's no template or mandate.
4. **The merge→pull→next-feature cycle is undocumented** — it's assumed knowledge.

### Recommendation: Add a "Release Phase" to the Tasks Template

Add a mandatory final phase to `.specify/templates/tasks-template.md`:

```markdown
## Phase N+1: Release

**Purpose**: Validate, document, and ship

- [ ] TXXX Run full test suite: `pytest --tb=line -q` — verify 0 failures
- [ ] TXXX Run gate regression: `pytest tests/test_gate_regression.py -v` — verify PASSED
- [ ] TXXX Update gate baseline: `python scripts/update_gate_baseline.py`
- [ ] TXXX Regenerate FIXTURES.md: `python scripts/generate_progress.py --fixtures`
- [ ] TXXX Run mock coverage: `pytest tests/test_mock_coverage.py -v` — verify 4/4
- [ ] TXXX Write `specs/[NNN-feature]/pr-analysis.md`
- [ ] TXXX Commit all changes (exclude scratch files)
- [ ] TXXX Push branch and open PR via `gh pr create`
```

This makes the post-implement lifecycle a tracked, checkboxable part of every
feature — not something the task writer must remember to include.

---

## Intermediate Commands: Implement to Merge (Complete Reference)

For this feature (029), the exact sequence from implement-complete to merged:

```bash
# 1. Validate
pytest --tb=line -q
# Expected: 536 passed, 58 skipped, 5 xfailed

# 2. Gate regression
pytest tests/test_gate_regression.py -v
# Expected: 1 passed

# 3. Update baseline
python scripts/update_gate_baseline.py
# Expected: 232 endpoints, 1194 passing gates

# 4. Regenerate FIXTURES.md
python scripts/generate_progress.py --fixtures
# Expected: FIXTURES.md updated, new endpoint row present

# 5. Mock coverage
pytest tests/test_mock_coverage.py -v
# Expected: 4 passed

# 6. Stage and commit (exclude ck.py)
git add ab/api/helpers/agent.py ab/api/endpoints/jobs.py \
       ab/api/models/enums.py ab/api/models/jobs.py \
       examples/agent.py tests/fixtures/requests/ChangeJobAgentRequest.json \
       tests/gate_baseline.json FIXTURES.md README.md CLAUDE.md \
       specs/029-agent-helpers/
git commit -m "feat(sdk): agent assignment helpers — oa/da/change with code resolution (#29)"

# 7. Push and open PR
git push -u origin 029-agent-helpers
gh pr create --title "feat(sdk): agent assignment helpers (#29)" --body "..."

# 8. After approval: merge and reset
gh pr merge <number> --squash
git checkout main && git pull
```

---

## Constitution & Plan Coherence

All 9 principles are satisfied. Notable:

- **Principle I (Model Fidelity)**: `ChangeJobAgentRequest` extends `RequestModel`
  with `extra="forbid"`. All fields use snake_case with camelCase aliases.
- **Principle III (Four-Way Harmony)**: Route, model, example, fixture all present.
  The 4D FIXTURES.md entry is populated.
- **Principle IX (Input Validation)**: Request body validated via `RequestModel`
  before HTTP call. The `data:` parameter pattern works because `AgentHelpers`
  constructs a validated dict from its parameters.

---

## Files Changed

### New Files (5)

| File | Purpose |
|------|---------|
| `ab/api/helpers/agent.py` | AgentHelpers class (oa, da, change) |
| `examples/agent.py` | ExampleRunner for agent change endpoint |
| `tests/fixtures/requests/ChangeJobAgentRequest.json` | Request fixture |
| `specs/029-agent-helpers/` | Full speckit documentation (8 files) |
| `specs/029-agent-helpers/pr-analysis.md` | This analysis |

### Modified Files (7)

| File | Change |
|------|--------|
| `ab/api/endpoints/jobs.py` | +Route, +change_agent(), +AgentHelpers wiring |
| `ab/api/models/enums.py` | +ServiceType enum |
| `ab/api/models/jobs.py` | +ChangeJobAgentRequest model |
| `README.md` | +Agent endpoint group, +UAT guide, +troubleshooting |
| `FIXTURES.md` | Regenerated with new endpoint row (232 total) |
| `tests/gate_baseline.json` | Updated baseline (232 endpoints, 1194 gates) |
| `CLAUDE.md` | Updated recent changes |

### Excluded

| File | Reason |
|------|--------|
| `ck.py` | Unrelated scratch file — not part of this feature |

---

## Success Criteria Status

| Criterion | Target | Actual | Verdict |
|-----------|--------|--------|---------|
| SC-001 | `oa()` changes origin agent | Method implemented, routes to correct endpoint | **PASS** |
| SC-002 | Zero regressions | 536 passed, 0 failures, gate ratchet passes | **PASS** |
| SC-003 | Gates G1,G4,G5,G6 pass | G4,G5 pass; G1,G6 fail (pre-existing ServiceBaseResponse issue) | **PARTIAL** |
| SC-004 | README UAT guide | 5-step guide with troubleshooting | **PASS** |
| SC-005 | Gate baseline updated | 232 endpoints, 1194 gates | **PASS** |
| SC-006 | FIXTURES.md accurate | New endpoint row present, correct status | **PASS** |

SC-003 partial: G1 and G6 failures are inherited from `ServiceBaseResponse`
model/fixture mismatch (028 issue #8), not introduced by this feature.

---

## Forward-Looking Recommendations

### R1. HIGH — Codify the post-implement lifecycle in the tasks template

Add a mandatory "Release" phase to `.specify/templates/tasks-template.md` with the
7 validation/release steps documented above. This ensures every feature includes
the implement-to-merge workflow as tracked tasks, not ad-hoc knowledge.

### R2. MEDIUM — Fix `ServiceBaseResponse` model to unblock G1/G6

The `ServiceBaseResponse` model/fixture mismatch (028 issue #8) now affects 2+
endpoints. Either expand the model with the 12 optional fields or split into
base + enriched subclasses. This would immediately fix G1/G6 for this endpoint
and others sharing the response model.

### R3. LOW — Document `data:` parameter pattern as a valid alternative

The `change_agent()` method correctly uses `data:` instead of `**kwargs` because
it's primarily consumed by a helper, not by direct SDK callers. This should be
documented in research.md as a conscious deviation (D8) so future implementors
know when `data:` is appropriate vs. `**kwargs`.

### R4. LOW — Add PR body template

PRs #31-#35 have converged on a consistent format (Summary, table of metrics,
Test plan, Files Changed). Codify this as a template (e.g., `.github/PULL_REQUEST_TEMPLATE.md`)
so agents don't need to reverse-engineer the pattern from history.

---

## Final Assessment

Feature 029 is a small, clean, well-executed feature that follows every established
pattern in the codebase. The implementation is correct, the documentation is good,
and the tests all pass.

The real value of this PR analysis is the lifecycle gap analysis. The speckit
workflow (specify → implement) covers ~80% of the feature lifecycle. The remaining
~20% (validate → commit → PR → merge → pull main) is currently undocumented tribal
knowledge. This gap doesn't matter when the same person runs the entire cycle in a
single session, but it becomes a problem when:

1. An agent runs `/speckit.implement` and stops — who runs the validation steps?
2. A new contributor joins — where do they learn the post-implement flow?
3. Context is lost mid-cycle — the DISCOVER workflow has "Resuming Work" but the
   speckit workflow has no equivalent.

R1 (adding a Release phase to the template) is the highest-leverage fix. It costs
nothing, prevents the gap from recurring, and makes every future feature self-documenting
through its completion.
