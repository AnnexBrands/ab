# PR Analysis: 035 — Catalog Endpoint Params & Pagination

**PR**: (pending) — `feat(sdk): add typed filter params, paginate helper, and docstrings to catalog/seller/lot endpoints (#035)`
**Branch**: `035-catalog-endpoint-params`
**Reviewed**: 2026-03-16
**Reviewer level**: Senior — with endpoint design, Pydantic validation flow, and static analysis considerations

---

## Summary

This PR wires all swagger-defined query parameters into the `catalog.list()`, `sellers.list()`, and `lots.list()` method signatures as explicit typed keyword arguments with Pydantic validation. It adds a standalone `paginate()` generator for automatic page iteration, updates all examples/tests to use named constants, and adds docstrings to all 17 catalog/seller/lot endpoint methods.

**Scope**: 1 new file, 19 modified files, +241/-57 lines.

**Tests**: 570 passed, 56 skipped, 5 xfailed, 0 failures. Zero regressions.

---

## Verdict

Clean, well-scoped enhancement that directly advances Constitution Principles VI (Documentation Completeness) and IX (Endpoint Input Validation). The key design insight — validating params in `_paginated_request()` via the existing `model_cls.check()` pattern, then building explicit kwargs that filter `None` values — gives both IDE discoverability and runtime validation without introducing any new abstractions or dependencies.

**Breaking change**: `page` parameter renamed to `page_number` on all three list methods. All callers in examples, tests, and docs updated.

Ship-ready (pending fixture capture from staging — T014 deferred).

---

## Issues

### 1. POSITIVE — Params validation gap closed in `_paginated_request()`

`_request()` (line 110-114 of base.py) already validated query params against `route.params_model`, but `_paginated_request()` bypassed this entirely — it called `self._client.request()` directly. This PR mirrors the validation:

```python
# base.py:157-162
if "params" in kwargs and route.params_model:
    model_cls = self._resolve_model(route.params_model)
    params = kwargs["params"]
    if hasattr(model_cls, "check"):
        kwargs["params"] = model_cls.check(params)
```

`check()` validates via `model_validate()` (catches typos/wrong types via `extra="forbid"`) and returns `model_dump(by_alias=True, exclude_none=True)` — so snake_case Python field names are automatically converted to PascalCase API parameter names.

### 2. POSITIVE — Explicit kwargs over `**kwargs` (Plan D1)

Each list method enumerates all params model fields as explicit keyword arguments:

| Endpoint | Filter Params | Total Params |
|----------|--------------|--------------|
| `catalog.list()` | id, customer_catalog_id, agent, title, start_date, end_date, is_completed, seller_ids | 10 |
| `sellers.list()` | id, name, customer_display_id, is_active | 6 |
| `lots.list()` | id, customer_item_id, lot_number | 5 |

This gives full IDE autocomplete. The `None` filtering (`{k: v for k, v in params.items() if v is not None}`) ensures only caller-specified params reach the API.

### 3. POSITIVE — `paginate()` is minimal and composable

The standalone generator in `ab/api/pagination.py` (45 lines) has no dependencies beyond `PaginatedList`. It accepts any callable with a `page_number` kwarg and filter kwargs:

```python
for page in paginate(api.catalog.list, agent="Smith", page_size=10):
    for item in page.items:
        process(item)
```

PaginatedList remains data-only (FR-008). No HTTP client references leak into the model.

### 4. POSITIVE — Static analysis test adapted for snake_case params

`test_example_params.py` does source-level regex extraction of param dict keys and compares against swagger names. The comparison was case-insensitive but didn't handle underscores:

```python
# Before: "page_number".lower() != "PageNumber".lower()
# After:  "page_number".replace("_","").lower() == "PageNumber".replace("_","").lower()
def _norm(s: str) -> str:
    return s.replace("_", "").lower()
```

This correctly bridges the snake_case → PascalCase gap that `check()` handles at runtime.

### 5. POSITIVE — Bug fix in test_lots.py

`test_lots.py:22` was using `TEST_CATALOG_ID` instead of `TEST_LOT_ID` for `api.lots.get()`. Both happened to equal `1` in the old constants, masking the bug. Now fixed with the dedicated `TEST_LOT_ID` constant.

### 6. POSITIVE — Gate infrastructure fix

`ab/progress/gates.py` `_infer_endpoint_module()` maps path prefixes to module names. It had `"catalog"` (lowercase) but the Catalog API paths are `/Catalog` (PascalCase). Added `"Catalog"` and `"Seller"` entries so G6 (Request Quality) evaluates correctly for these endpoints.

### 7. OBSERVATION — `page` → `page_number` is a breaking change

All three list methods rename `page` to `page_number` (Plan D4). While all in-repo callers are updated, external consumers using `page=` will get `TypeError: unexpected keyword argument`. This is intentional — aligns the kwarg name with the underlying params model field name and the API's `PageNumber` parameter.

### 8. OBSERVATION — `ck.py` remains a stray scratch file

Must not be committed with this feature.

---

## Constitution & Plan Coherence

All 9 principles satisfied. Notable:

- **Principle I (Model Fidelity)**: Params models (CatalogListParams, SellerListParams, LotListParams) already existed as RequestModel with `extra="forbid"`. This PR wires them into the validation path.
- **Principle III (Four-Way Harmony)**: All four artifacts updated: endpoint implementation, examples (with filter demos), FIXTURES.md status, and Sphinx docs with filter examples.
- **Principle V (Endpoint Status Tracking)**: FIXTURES.md updated for all three list endpoints — method references, params_model columns, and notes reflect feature 035.
- **Principle VI (Documentation Completeness)**: Docstrings added to all 17 endpoint methods across catalog/sellers/lots. Sphinx docs updated with filter param examples.
- **Principle IX (Endpoint Input Validation)**: Core goal of this feature. `_paginated_request()` now validates params before HTTP call, matching `_request()` behavior.

All 5 design decisions (D1-D5) from plan.md implemented as specified.

---

## Files Changed

### New Files (1)

| File | Purpose |
|------|---------|
| `ab/api/pagination.py` | Standalone `paginate()` sync generator (45 lines) |

### Modified Files (19)

| File | Change |
|------|--------|
| `ab/api/base.py` | Add params validation to `_paginated_request()` (6 lines) |
| `ab/api/__init__.py` | Export `paginate` |
| `ab/__init__.py` | Export `paginate` |
| `ab/api/endpoints/catalog.py` | Expand `list()` to 10 kwargs, add docstrings to all 6 methods |
| `ab/api/endpoints/sellers.py` | Expand `list()` to 6 kwargs, add docstrings to all 5 methods, remove unused `Any` import |
| `ab/api/endpoints/lots.py` | Expand `list()` to 5 kwargs, add docstrings to all 6 methods, remove unused `Any` import |
| `ab/api/models/shared.py` | Fix docstring example: `page=` → `page_number=` |
| `ab/progress/gates.py` | Add `Catalog`/`Seller` PascalCase entries to `_infer_endpoint_module()` |
| `tests/constants.py` | Add `TEST_LOT_ID`, `TEST_LOT_NUMBER` |
| `tests/test_example_params.py` | Normalize param comparison to handle snake_case ↔ PascalCase |
| `tests/integration/test_lots.py` | Fix `TEST_CATALOG_ID` → `TEST_LOT_ID` bug |
| `examples/catalog.py` | Use `CATALOG_CUSTOMER_SELLER_ID` filter, `page_number=` |
| `examples/sellers.py` | Use `is_active=True` filter, `page_number=` |
| `examples/lots.py` | Use `TEST_LOT_NUMBER` filter, `TEST_LOT_ID` constants |
| `docs/api/catalog.md` | Add filter param examples, fix return type |
| `docs/api/sellers.md` | Add filter param examples, fix return type |
| `docs/api/lots.md` | Add filter param examples, fix return type |
| `docs/quickstart.md` | Add paginate helper example |
| `FIXTURES.md` | Update catalog/seller/lot list entries with params models and feature 035 notes |

### Excluded

| File | Reason |
|------|--------|
| `ck.py` | Unrelated scratch file |
| `specs/035-catalog-endpoint-params/*` | Spec artifacts (not shipped code) |

---

## Success Criteria Status

| Criterion | Target | Actual | Verdict |
|-----------|--------|--------|---------|
| SC-001 | 100% swagger query params accessible as typed kwargs | 10/10 catalog, 6/6 seller, 5/5 lot | **PASS** |
| SC-002 | All endpoint methods have docstrings | 17/17 methods documented | **PASS** |
| SC-003 | Standalone paginate helper works | `paginate()` exported from `ab`, yields pages | **PASS** |
| SC-004 | Zero magic numbers in examples/tests | All replaced with named constants | **PASS** |
| SC-005 | Invalid params caught before HTTP call | `check()` in `_paginated_request()` validates | **PASS** |
| SC-006 | All existing tests pass | 570 passed, 0 failures | **PASS** |

---

## Forward-Looking Recommendations

### R1. MEDIUM — Fixture capture from staging (T014)

Examples now demonstrate filter params but haven't been run against staging to capture filtered-response fixtures. This should happen before or shortly after merge to close G2 (Fixture Status) for the three list endpoints.

### R2. LOW — Extend paginate() with items-only iteration

A convenience wrapper like `paginate_items(api.catalog.list, ...)` that yields individual items (flattening pages) would simplify the most common use case. Low priority — users can do `for page in paginate(...): for item in page.items:` today.

### R3. LOW — Apply typed list params to ACPortal paginated endpoints

ACPortal has ~15 paginated list endpoints (companies.list, contacts.list, jobs.list, etc.) that use the POST-body `ListRequest` pattern instead of query params. Those use a different pagination mechanism but could benefit from the same explicit-kwargs approach for their filter criteria.
