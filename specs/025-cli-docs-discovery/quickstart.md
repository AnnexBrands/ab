# Quickstart: CLI Docs & Discovery Major Release

**Branch**: `025-cli-docs-discovery` | **Date**: 2026-03-01

## Verification Scenarios

### Scenario 1: Rich CLI Help (US1)

**Test command**:
```bash
ab jobs get_timeline --help
```

**Expected output** (structural — exact wording may vary):
```
  get_timeline
  ────────────

  Get the timeline tasks for a job.

  Route   GET /job/{jobDisplayId}/timeline
  Python  api.jobs.get_timeline(job_display_id: int) -> list[TimelineTask]
  CLI     ab jobs get_timeline <job_display_id>

  Returns: list[TimelineTask]

  Positional arguments:
    job_display_id (int)

  Response model: TimelineTask
    taskCode            str          Task code (PU, PK, ST, CP)
    ...
```

**Assertions**:
- Output contains `GET /job/{jobDisplayId}/timeline`
- Output contains `api.jobs.get_timeline`
- Output contains `-> list[TimelineTask]`
- Output contains `ab jobs get_timeline`
- No credentials required (exit 0)

---

### Scenario 2: Implicit Method Listing (US4)

**Test command**:
```bash
ab jobs
```

**Expected output** (structural):
```
  jobs — N methods

  Helpers (no API route):
  ──────────────────────
  ...

  API Methods:
  ────────────
  GET /job/{jobDisplayId}                    get(job_display_id) -> Job
  GET /job/{jobDisplayId}/timeline           get_timeline(job_display_id) -> list[TimelineTask]
  ...
```

**Assertions**:
- Output contains HTTP method and path for each Route-backed method
- Output contains return types
- Helpers section appears before API methods (if any helpers exist)
- No `--list` flag required

---

### Scenario 3: Implicit Top-Level Listing (US4)

**Test command**:
```bash
ab
```

**Expected output** (structural):
```
  Endpoint             Methods   Path Root   Aliases
  ─────────────────    ───────   ─────────   ──────────
  address                    8   /address    addr
  companies                 12   /companies  co
  contacts                  15   /contacts   ct
  jobs                      30   /job        job
  ...

  N endpoints, M methods
```

**Assertions**:
- Output includes Path Root column
- Output includes Aliases column (from shared ALIASES registry)
- No `--list` flag required

---

### Scenario 4: Route-Derived Auto-Discovery (US2)

**Test code** (Python):
```python
from examples._runner import ExampleRunner

runner = ExampleRunner("Jobs", endpoint_attr="jobs", env="staging")
runner.add("get", lambda api: api.jobs.get(12345))
# No response_model or fixture_file specified!

entry = runner.entries[0]
assert entry.response_model == "Job"
assert entry.fixture_file == "Job.json"
```

**Assertions**:
- `response_model` auto-populated from Route
- `fixture_file` auto-populated as `{ModelName}.json`
- Existing explicit overrides still take precedence

---

### Scenario 5: Upgraded Progress Report (US3)

**Test command**:
```bash
python scripts/generate_progress.py
# Open html/progress.html
```

**Assertions** (in HTML output):
- Endpoints grouped by endpoint class (e.g., "jobs", "contacts")
- Sub-sections by path sub-root (e.g., "timeline", "onhold")
- Each row shows:
  - Python dotted path (e.g., `api.jobs.get_timeline`)
  - `Ex` column (yes/no)
  - `CLI` column (yes/no)
- Helpers section at top of each endpoint class group
- Quality gate columns still present

---

### Scenario 6: Generic Constants Discovery (US6)

**Test code** (Python):
```python
from ab.cli.route_resolver import path_param_to_constant

assert path_param_to_constant("jobDisplayId") == "TEST_JOB_DISPLAY_ID"
assert path_param_to_constant("contactId") == "TEST_CONTACT_ID"
assert path_param_to_constant("companyId") == "TEST_COMPANY_ID"
```

**Assertions**:
- camelCase → SCREAMING_SNAKE conversion is correct
- Progress report shows missing constant action items

---

### Scenario 7: No Credentials Needed for Help (US1, US4)

**Test setup**: No `.env` or `.env.staging` file present.

```bash
ab jobs --help          # should NOT fail
ab jobs get --help      # should NOT fail
ab                      # should NOT fail
ab jobs                 # should NOT fail
```

**Assertions**: All four commands succeed with exit code 0, no credential error.

---

## Smoke Test Checklist

After implementation, run these commands to verify the feature works end-to-end:

```bash
# 1. Rich help
ab jobs get --help
ab jobs get_timeline --help
ab contacts get_details --help

# 2. Method listing
ab jobs
ab contacts
ab address

# 3. Top-level listing
ab

# 4. Auto-discovery (run example without explicit models)
python -c "
from examples._runner import ExampleRunner
r = ExampleRunner('Jobs', endpoint_attr='jobs', env='staging')
r.add('get', lambda api: api.jobs.get(12345))
e = r.entries[0]
print(f'response_model: {e.response_model}')
print(f'fixture_file: {e.fixture_file}')
"

# 5. Progress report
python scripts/generate_progress.py
# Open html/progress.html and verify grouping

# 6. Sphinx docs
cd docs && make html
# Open _build/html/index.html
```
