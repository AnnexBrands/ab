# PR Review: 011 — Endpoint Quality Gates

**Branch**: `011-endpoint-quality-gates`
**Date**: 2026-02-21
**Files Changed**: 80 modified, 4 new (+1,667 / -599 lines)

---

## Executive Summary

Feature 011 introduces a four-gate quality system (G1-G4) that enforces honest endpoint status tracking across the SDK. Previously, FIXTURES.md declared endpoints "complete" when they had captured fixtures — regardless of model fidelity, test substance, or documentation accuracy. This feature replaces that binary status with a multi-dimensional evaluation: **an endpoint is "complete" only when all four gates pass**.

The honest baseline now reads **25/161 endpoints truly complete** — a sharp but truthful demotion from the previous inflated count. This is the correct outcome.

---

## Spec & Constitution Coherence — A

The spec, plan, and constitution are tightly aligned. The four gates map directly to Constitution v2.3.0 principles:

| Gate | Constitution Principle | What It Enforces |
|------|----------------------|------------------|
| G1 — Model Fidelity | Principle I (Pydantic Model Fidelity) | Zero `__pydantic_extra__` on fixture validation |
| G2 — Fixture Status | Principle II (Example-Driven Capture) | Fixture file physically exists on disk |
| G3 — Test Quality | Principle III (Four-Way Harmony) | Tests assert `isinstance` + zero extra fields |
| G4 — Doc Accuracy | Principle VI (Documentation Completeness) | Return type is not `Any`, Sphinx picks up correct types |

The Sources of Truth hierarchy (Tier 1: server source, Tier 2: fixtures, Tier 3: swagger) is respected throughout. Models are derived from captured fixtures, not swagger schemas. Swagger deviations are documented inline (e.g., `CompanyDetails.capabilities` is an int bitmask, not a dict).

**One gap**: The spec claims FR-003 requires ~30 fully-typed sub-models with no nested `Optional[dict]`, but `CompanyDetails` still has `settings: Optional[dict]`, `addresses: Optional[List[dict]]`, and `contacts: Optional[List[dict]]`. These are acknowledged but unresolved — likely awaiting fixture data to type correctly. This should be tracked in a follow-up.

---

## Code Quality — A-

### Strengths

1. **Gate evaluators are clean and well-structured** (`ab/progress/gates.py`). Each gate is a pure function returning a `GateResult` dataclass. The orchestrator `evaluate_endpoint_gates()` composes them cleanly. The paginated wrapper handling in G1 (detecting `data: [...]` and `items: [...]` patterns) is correct and handles edge cases.

2. **Shared sub-models are properly extracted** (`ab/api/models/common.py`). `Coordinates` and `CompanyAddress` are reusable across `CompanyDetails` and `ContactPrimaryDetails`. This follows DRY without over-abstracting.

3. **CompanyDetails model tree is thorough** — 334 new lines covering ~25 sub-models (carrier accounts for 10 carriers, pricing with 7 sub-objects, insurance, tariffs, taxes). Every field has a `Field(None, alias=..., description=...)` annotation. This is the largest model in the SDK and it's done right.

4. **Test pattern is consistent and enforced**. Every integration test went from `assert result is not None` to `isinstance(result, Model)` + `assert_no_extra_fields(result)`. The shared `assert_no_extra_fields()` helper in `conftest.py` provides a clean, reusable assertion with a descriptive error message.

5. **Return types properly annotated**. All 25 endpoint files went from `-> Any` to specific model types (e.g., `-> CompanyDetails`, `-> list[RateQuote]`). Imports use `TYPE_CHECKING` blocks to avoid circular imports — correct pattern.

6. **FIXTURES.md regeneration is automated**. `python scripts/generate_progress.py --fixtures` regenerates the file from source artifacts. The parser handles both legacy 8-column format and new 10-column gate format. Notes are preserved.

### Issues

1. **G3 test quality evaluation is a regex heuristic** — it pattern-matches for `isinstance(` and `__pydantic_extra__` in test files. This works today but is fragile. A test that uses a wrapper function or different assertion pattern could pass G3 even if tests are weak, or fail G3 even if tests are strong. Acceptable for now; document the limitation.

2. **G4 doc accuracy only checks return type annotations**, not actual Sphinx build output. The check for `docs/models/` directory existence is a no-op (just `pass`). If Sphinx isn't configured or autodoc fails silently, G4 would still pass. This is an honest trade-off — checking annotation correctness covers 90% of the value.

3. **`logging.disable(logging.WARNING)` / `logging.disable(logging.NOTSET)`** is used in both `fixtures_generator.py` and `generate_progress.py` to suppress pydantic extra-field warnings during gate evaluation. This is a global side-effect that affects all loggers. If the script crashes between disable/enable, warnings stay suppressed. Consider a context manager.

4. **`_scratchpad.py` is in the repo root** — this should not be committed.

---

## User Stories & Plan Effectiveness — A

The 73 tasks across 8 phases are all marked complete. The phased approach was effective:

- **Phase 1-2 (setup + gate infrastructure)** laid the foundation before touching any endpoint code
- **Phase 4 (model updates)** was correctly identified as the largest effort — CompanyDetails alone is 25 sub-models
- **Phase 5 (test hardening)** applied a uniform pattern across all 30+ test files
- **Phase 6 (return types)** was mechanical but essential for G4

The critical path (T001 → T004 → T009 → T010 → T014) produced the first honest FIXTURES.md baseline, which is exactly the right sequencing — you need the gates evaluating before you can see what's broken.

The plan correctly prioritized US1-US3 (P1) over US4-US5 (P2). Documentation and dashboard are nice-to-have; honest status and model fidelity are essential.

---

## Progress Toward Project Goals — B+

**What's been achieved across 11 features**:
- SDK covers 161 endpoints across ACPortal, Catalog, and ABC surfaces
- 25 endpoints pass all four quality gates (true "complete")
- Constitution v2.3.0 is stable with Sources of Truth hierarchy
- Automated progress reporting (HTML + FIXTURES.md) from source artifacts
- Request and response model methodology is established

**What the gate data reveals**:
- G1 (Model Fidelity): 30/161 pass — ~80% of models still have undeclared fields
- G2 (Fixture Status): 35/161 pass — ~78% of endpoints lack captured fixtures
- G3 (Test Quality): 125/161 pass — tests are in good shape (77%)
- G4 (Doc Accuracy): 118/161 pass — return types mostly correct (73%)

**The bottleneck is G1 and G2** — fixture capture and model fidelity. G3 and G4 are ahead. This is expected: capturing fixtures requires live API access and valid test data, and model fidelity requires those fixtures to exist first.

---

## Suggested Next Steps

1. **Fixture capture sprint**: The highest-leverage next feature is systematically capturing fixtures for the ~126 endpoints missing them. G2 is the gate blocking the most endpoints, and G1 requires G2 first.

2. **Resolve remaining `Optional[dict]` in CompanyDetails**: `settings`, `addresses`, and `contacts` fields need fixture data to type correctly. Track these as G1 blockers.

3. **Address G4 failures for shipment/payment endpoints**: 8 job-scoped shipment endpoints (`/job/{id}/shipment/*`) and payment endpoints pass G1-G3 but fail G4 — their return types just need annotation fixes.

4. **Replace `logging.disable` with a context manager** in `fixtures_generator.py` and `generate_progress.py` to prevent leaked global state.

5. **Consider CI integration**: The gate evaluator could run in CI to prevent status regression — reject PRs that demote an endpoint from complete to incomplete without justification.
