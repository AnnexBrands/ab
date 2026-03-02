# Quickstart: Reports & Lookups Quality Gates

**Branch**: `027-reports-lookups-gates` | **Date**: 2026-03-01

## Prerequisites

- `.venv` activated or use `PYTHONPATH=/opt/pack/ab .venv/bin/...`
- Staging API accessible (AB_API_KEY set in .env)
- Run from repo root `/opt/pack/ab`

## Verification Scenarios

### Scenario 1: Report Models Validate Against Fixtures

```bash
# After rewriting models and capturing fixtures:
PYTHONPATH=/opt/pack/ab .venv/bin/ex reports insurance
PYTHONPATH=/opt/pack/ab .venv/bin/ex reports sales
PYTHONPATH=/opt/pack/ab .venv/bin/ex reports sales_summary
PYTHONPATH=/opt/pack/ab .venv/bin/ex reports sales_drilldown
PYTHONPATH=/opt/pack/ab .venv/bin/ex reports top_revenue_customers
PYTHONPATH=/opt/pack/ab .venv/bin/ex reports top_revenue_sales_reps
PYTHONPATH=/opt/pack/ab .venv/bin/ex reports referred_by
PYTHONPATH=/opt/pack/ab .venv/bin/ex reports web2lead

# Expected: All succeed with no "received extras" warnings
```

### Scenario 2: Extended Lookup Models Validate Against Fixtures

```bash
PYTHONPATH=/opt/pack/ab .venv/bin/ex lookup get_by_key
PYTHONPATH=/opt/pack/ab .venv/bin/ex lookup get_access_keys
PYTHONPATH=/opt/pack/ab .venv/bin/ex lookup get_access_key
PYTHONPATH=/opt/pack/ab .venv/bin/ex lookup get_ppc_campaigns
PYTHONPATH=/opt/pack/ab .venv/bin/ex lookup get_parcel_package_types
PYTHONPATH=/opt/pack/ab .venv/bin/ex lookup get_document_types
PYTHONPATH=/opt/pack/ab .venv/bin/ex lookup get_common_insurance
PYTHONPATH=/opt/pack/ab .venv/bin/ex lookup get_density_class_map
PYTHONPATH=/opt/pack/ab .venv/bin/ex lookup get_refer_categories
PYTHONPATH=/opt/pack/ab .venv/bin/ex lookup get_refer_category_hierarchy

# Expected: All succeed with no "received extras" warnings
```

### Scenario 3: Basic Lookups Still Pass

```bash
PYTHONPATH=/opt/pack/ab .venv/bin/ex lookup get_contact_types
PYTHONPATH=/opt/pack/ab .venv/bin/ex lookup get_countries
PYTHONPATH=/opt/pack/ab .venv/bin/ex lookup get_job_statuses
PYTHONPATH=/opt/pack/ab .venv/bin/ex lookup get_items

# Expected: All pass, no regressions
```

### Scenario 4: Tests Pass

```bash
source .venv/bin/activate
pytest tests/ -q

# Expected: 520+ passed, 7 or fewer failures (pre-existing)
```

### Scenario 5: Lint Clean

```bash
source .venv/bin/activate
ruff check ab/api/models/reports.py ab/api/models/lookup.py

# Expected: All checks passed
```

### Scenario 6: Progress Report Shows Improvement

```bash
PYTHONPATH=/opt/pack/ab .venv/bin/python scripts/generate_progress.py

# Expected:
#   G1 Model Fidelity:  80+/231 (up from 66)
#   G2 Fixture Status:  100+/231 (up from 87)
#   All gates pass:     65+/231 (up from 50)
```

### Scenario 7: FIXTURES.md Updated

```bash
PYTHONPATH=/opt/pack/ab .venv/bin/python scripts/generate_progress.py --fixtures

# Expected: Report and extended lookup rows show PASS for G1 and G2
```
