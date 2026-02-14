# Tasks: Harden Example Parameters Against Swagger

**Input**: Design documents from `/specs/005-harden-example-params/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Included — spec FR-006 explicitly requires an automated validation test.

**Organization**: Tasks grouped by user story. US1 fixes the 4 confirmed mismatches. US2 adds the automated guard.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Phase 1: User Story 1 — Fix Parameter Mismatches (Priority: P1) 🎯 MVP

**Goal**: All 4 confirmed endpoint methods map Python params to correct swagger-defined API parameter names. Examples updated to match.

**Independent Test**: Run `python -m examples address.validate`, `python -m examples address.get_property_type`, `python -m examples forms.get_operations` against staging — no 400 errors from wrong parameter names.

### Endpoint Fixes

- [x] T001 [US1] Fix `AddressEndpoint.validate()` param mapping in `ab/api/endpoints/address.py` — rename Python params to `line1`, `city`, `state`, `zip`; map to `Line1`, `City`, `State`, `Zip`; remove fabricated `country` param. See contracts/param-corrections.md Contract 1.
- [x] T002 [US1] Fix `AddressEndpoint.get_property_type()` param mapping in `ab/api/endpoints/address.py` — replace `street`/`zip_code` with `address1`, `address2`, `city`, `state`, `zip_code`; map to `Address1`, `Address2`, `City`, `State`, `ZipCode`. See contracts/param-corrections.md Contract 2.
- [x] T003 [P] [US1] Fix `FormsEndpoint.get_operations()` param mapping in `ab/api/endpoints/forms.py` — change `params["opsType"]` to `params["type"]`. See contracts/param-corrections.md Contract 3.
- [x] T004 [P] [US1] Fix `ShipmentsEndpoint.request_rate_quotes()` in `ab/api/endpoints/shipments.py` — change from `**params` with `params=params` to `data: dict | None = None` with `json=data`. See contracts/param-corrections.md Contract 4.

### Example Updates

- [x] T005 [US1] Update `examples/address.py` lambda calls to use new parameter names — `validate(line1=..., city=..., state=..., zip=...)` and `get_property_type(address1=..., city=..., state=..., zip_code=...)`. Use realistic values from ABConnectTools examples.
- [x] T006 [P] [US1] Update `examples/shipments.py` `request_rate_quotes` lambda call to pass `data={}` dict body instead of keyword params (mark TODO for correct body fields).

### Verification

- [x] T007 [US1] Run corrected address and forms examples against staging (`python -m examples address.validate`, `python -m examples address.get_property_type`, `python -m examples forms.get_operations`) and confirm no parameter-name 400 errors. Run `ruff check` on all changed files.

**Checkpoint**: All 4 endpoint methods now send correct API parameter names. Examples match new signatures.

---

## Phase 2: User Story 2 — Automated Validation Guard (Priority: P2)

**Goal**: A pytest test validates that every example entry's parameters are consistent with the swagger schema, catching future drift automatically.

**Independent Test**: Run `pytest tests/test_example_params.py -v` — all pass. Introduce a deliberate wrong param and confirm it fails.

### Implementation

- [x] T008 [US2] Create `tests/test_example_params.py` — automated test that: (1) loads each swagger spec from `ab/api/schemas/{acportal,catalog,abc}.json`, (2) for each endpoint implementation in `ab/api/endpoints/`, inspects the parameter-to-API mapping, (3) cross-references mapped API param names against swagger query parameters and request body fields, (4) fails with a clear message for any unknown parameter. Must handle edge cases: `**kwargs` endpoints, `additionalProperties: true` bodies, optional params the example omits.
- [x] T009 [US2] Run `pytest tests/test_example_params.py -v` and confirm all pass. Verify test completes in under 10 seconds. Run `ruff check tests/test_example_params.py`.

**Checkpoint**: Validation guard runs in CI. Future param mismatches will be caught before merge.

---

## Phase 3: Polish & Cross-Cutting Concerns

- [x] T010 Run full `pytest` suite to confirm no regressions from endpoint signature changes.
- [x] T011 Run `ruff check .` across entire project.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (US1)**: No prerequisites — can start immediately
- **Phase 2 (US2)**: Can start after T001–T006 are complete (needs correct param mappings to validate against)
- **Phase 3 (Polish)**: After US1 and US2 are complete

### Within Phase 1

- T001 and T002 edit the same file (`ab/api/endpoints/address.py`) — must be sequential
- T003 and T004 edit different files — can run in parallel with T001/T002
- T005 depends on T001+T002 (needs new method signatures)
- T006 depends on T004 (needs new method signature)
- T007 depends on all endpoint + example changes

### Parallel Opportunities

```
T001 → T002 → T005 ─┐
T003 ────────────────┤
T004 → T006 ─────────┼→ T007 → T008 → T009 → T010 → T011
```

## Implementation Strategy

### MVP First (US1 Only)

1. Complete T001–T007 (fix all 4 mismatches + verify)
2. **STOP and VALIDATE**: Run examples against staging
3. This alone delivers the primary value — correct API calls

### Full Delivery

1. Complete US1 (T001–T007)
2. Complete US2 (T008–T009) — adds automated guard
3. Polish (T010–T011) — full suite validation

---

## Notes

- T001+T002 are on the same file — execute sequentially
- T003, T004 are independent files — parallelize with T001/T002
- All contracts are documented in `specs/005-harden-example-params/contracts/param-corrections.md` with exact before/after code
- The validation test (T008) is the most complex task — it needs to parse swagger JSON and introspect endpoint methods
- Commit after each phase checkpoint
