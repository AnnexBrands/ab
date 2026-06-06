# Quickstart: Example Coverage & Run-and-Verify

**Feature**: 037-example-coverage · **Date**: 2026-06-05

Two audiences: the **maintainer** (runs gates, regenerates the report, ingests captures)
and the **operator** (has staging creds; runs read-only examples and pastes responses for
the rest).

---

## Maintainer — daily loop

```bash
# 0. activate the canonical venv
source .venv/bin/activate

# 1. coverage gate + no-drift gates (NON-live — same as CI certification)
pytest -m "not live"
#   - tests/test_example_coverage.py        -> every routed endpoint has a canonical example
#   - tests/test_example_run_results_drift.py -> results artifact shape/sorted/no-drift
#   - existing progress no-drift tests still pass

# 2. regenerate the report (deterministic, no network)
python scripts/generate_progress.py          # writes html/progress.html
#   open html/progress.html -> per-endpoint Run column + paste-capture section
```

A red coverage gate prints the exact `api.<group>.<method>` endpoints missing a canonical
example — create one with the generator shape (see contracts/example-contract.md §1).

---

## Operator — verify read-only examples (live, needs .env.staging)

```bash
source .venv/bin/activate

# run every read-only (GET) example against staging, compare to fixtures,
# and write tests/example_run_results.json
python scripts/run_examples.py

# scope to one group while iterating
python scripts/run_examples.py --group jobs.timeline

# refresh fixtures from live (keeps example <-> fixture in lock-step)
python scripts/run_examples.py --capture
```

Output is a per-endpoint table: `passing` / `failing` (with a short diff) / `awaiting-data`.
Mutating endpoints are listed as `awaiting-paste` and are never executed.

---

## Operator — paste responses for endpoints that can't auto-run

1. Open `html/progress.html`. The capture section lists every `awaiting-paste` /
   `awaiting-data` endpoint with an editable textarea (response, plus a request textarea
   where the endpoint takes a body). A counter shows how many remain.
2. Paste the **real** JSON response (and request body) from a live call.
3. Click **Download captures.json**. The browser downloads a single `captures.json`
   (no server involved).
4. Hand `captures.json` back to the maintainer (or drop it at the repo root).

---

## Maintainer — ingest pastes into fixtures + examples

```bash
python scripts/ingest_captures.py captures.json
#   for each entry: validate paste against the response model (rejects malformed),
#   write tests/fixtures/<Model>.json (+ requests/<ReqModel>.json),
#   generate/update the plain-script example, and mark the endpoint passing(source=paste)
#   in tests/example_run_results.json

# confirm the gate is now green and regenerate the report
pytest -m "not live" && python scripts/generate_progress.py
```

A malformed paste is reported with an actionable message and **no fixture is written**
(Constitution II: no fabricated fixtures).

---

## Migrating a deprecated (`_`-prefixed) example

```bash
# 1. write examples/<group>.py (plain main() form) calling the same endpoints
#    -> import from examples._capture, print via format_result, save(<Model>.json, result)
# 2. DO NOT delete examples/_<group>.py (no-deletion policy) — it just stops being canonical
# 3. update html/rm_runner.html to mark the file migrated
# 4. verify coverage no longer reports the endpoint as legacy-only:
pytest -m "not live" -k example_coverage
```

---

## Interactive app — harmony, workbench, sign-off (US5)

```bash
python scripts/serve_progress.py          # http://localhost:8765+ (auto-skips busy ports)
#   binds 0.0.0.0 → reachable from a Windows browser over WSL2 (localhost or the WSL IP)
# refresh coverage first so the harmony "Test" column is current:
coverage run --source=ab -m pytest -m "not live" -q && coverage json -o coverage.json
```

In the app: left nav drills `path › tag › endpoint`. Selecting an endpoint opens the
**workbench**:

- **LHS request** — the real `import` + `api.<group>.<method>(...)` call (read live from
  the example file), editable, plus a JSON request-body field. **▶ Run** executes the
  edited code against staging (mutations need the *confirm* checkbox) and shows the
  produced response + a `matches fixture` / `DIFF` badge.
- **RHS response** — swagger response codes + the latest fixture JSON, with a
  **JSON | Pydantic** toggle. Save buttons write the request fixture, the response
  fixture, and an "improvement" record (`tests/example_edits.json`).
- **Harmony pillars** are popovers (implementation source, Sphinx link, example, fixture,
  coverage). **Sign-off** checkboxes (example/tests/Sphinx) persist to `progress.db` and
  export to `tests/example_signoffs.json`.

### Interactive enrichment flow

Get a call working in the workbench (or tell the agent "make `examples/_X.py` pass with
this input"). The agent then promotes the legacy `_X.py` to the canonical
`examples/X.py` (mutation-guarded, real input), captures its fixture, and wires the test
— reading your saved `tests/example_edits.json` where relevant. `_X.py` is retained
(no-deletion); `X.py` becomes canonical.

## Definition of done (maps to Success Criteria)

- `pytest -m "not live"` green, incl. coverage gate → SC-001, SC-005.
- `python scripts/run_examples.py` shows all read-only endpoints `passing` → SC-002.
- Every non-runnable endpoint has a paste slot; ingested pastes produce fixture+example
  → SC-003.
- `html/progress.html` shows a Run status for every endpoint and regenerates with no diff
  → SC-004.
- `rm_runner.html` shows zero remaining `_`-prefixed canonical examples → SC-006.
- `ab` public imports unchanged; pre-existing non-live tests still pass → SC-007.
