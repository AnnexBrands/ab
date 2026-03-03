# CLI Interfaces: 028 Quality Infrastructure Sprint

This feature introduces 4 new CLI scripts. No REST API contracts — this is internal tooling.

## 1. Gate Baseline Update

**Script**: `scripts/update_gate_baseline.py`

**Usage**:
```bash
python scripts/update_gate_baseline.py
```

**Behavior**:
1. Calls `evaluate_all_gates()` from `ab.progress.gates`
2. Builds per-endpoint-per-gate mapping
3. Writes `tests/gate_baseline.json` (sorted, indented)
4. Prints diff summary (gates added, gates removed vs previous baseline)

**Exit codes**:
- 0: Baseline updated successfully
- 1: Error evaluating gates

**Output format**:
```
Gate baseline updated: tests/gate_baseline.json
  Endpoints: 231
  Total gate passes: 814
  New passes since last baseline: +23
  Removed passes since last baseline: -0
```

---

## 2. Gate Regression Test

**Test**: `tests/test_gate_regression.py`

**Usage** (via pytest):
```bash
pytest tests/test_gate_regression.py -v
```

**Behavior**:
1. Loads `tests/gate_baseline.json`
2. If file doesn't exist: auto-generates from current state, writes file, passes
3. Calls `evaluate_all_gates()`
4. For each endpoint in baseline, asserts all previously-passing gates still pass
5. New passes (not in baseline) are allowed (one-directional)
6. Reports regressions with endpoint path, method, and gate ID

**Failure output**:
```
FAILED test_gate_regression.py::test_no_gate_regressions
  Gate regressions detected (2):
    /companies/{_} GET: G1 regressed (was PASS, now FAIL: 3 undeclared extra fields)
    /reports/sales POST: G2 regressed (was PASS, now FAIL: fixture file missing)

  Run `python scripts/update_gate_baseline.py` to update after intentional changes.
```

---

## 3. Batch Fixture Capture

**Script**: `scripts/capture_missing.py`

**Usage**:
```bash
python scripts/capture_missing.py [--dry-run]
```

**Options**:
- `--dry-run`: List what would be captured without running examples

**Behavior**:
1. Parses FIXTURES.md for G2=FAIL endpoints
2. Filters: excludes `response_model=None`, `bytes`, primitives
3. For each endpoint, locates matching example file in `examples/`
4. Without `--dry-run`: runs example, checks for captured fixture
5. Prints per-endpoint result and summary

**Output format**:
```
Processing 87 endpoints with G2=FAIL...

  [CAPTURED] POST /reports/sales → SalesForecastReport.json
  [FAILED]   POST /reports/insurance → HTTP 500 (staging server error)
  [NO-EXAMPLE] DELETE /companies/{id}/archive → No example in examples/companies.py

Summary:
  Captured: 34
  Failed: 12
  No example: 41
  Total processed: 87
```

---

## 4. Model Test Stub Generator

**Script**: `scripts/generate_model_tests.py`

**Usage**:
```bash
python scripts/generate_model_tests.py [--dry-run]
```

**Options**:
- `--dry-run`: Show what would be generated without writing files

**Behavior**:
1. Reads all Route definitions via `route_index`
2. Filters to routes with a `response_model` that is a Pydantic model name
3. Checks existing test files for coverage (`def test_{model_snake}`)
4. Generates missing test methods grouped by endpoint module
5. Writes to `tests/models/test_{module}_models.py` (create or append)

**Output format**:
```
Scanning 231 routes...
  Already covered: 135
  No response model: 48
  Generating stubs: 48

Generated tests:
  tests/models/test_commodity_models.py: +3 methods (CommodityModel, CommodityMapEntry, CommodityCategory)
  tests/models/test_dashboard_models.py: +5 methods (DashboardStats, ...)
  tests/models/test_partner_models.py: +2 methods (Partner, PartnerSimple)

Total: 48 test stubs generated across 12 files
```

---

## 5. Return Type Audit

**Script**: `scripts/audit_return_types.py`

**Usage**:
```bash
python scripts/audit_return_types.py
```

**Behavior**:
1. Reads all Route definitions
2. For each route with `response_model`, finds the endpoint method
3. Compares method return type annotation against expected type from Route
4. Reports mismatches

**Output format**:
```
Return type mismatches (46):

  ab/api/endpoints/jobs.py:
    create() → Any (should be → Job)
    save() → Any (should be → Job)
    ...

  ab/api/endpoints/rfq.py:
    accept() → Any (should be → ServiceBaseResponse)
    decline() → Any (should be → ServiceBaseResponse)
    ...

Summary: 46 mismatches across 11 files
```
