# Quickstart: Verify Artifact Integrity

## Prerequisites

- Staging credentials configured (`.env` or environment variables)
- SDK installed in development mode (`pip install -e .`)
- All example modules importable (`python -m examples --list`)

## Step 1: Verify fixture files match FIXTURES.md

Count fixture files on disk and compare against FIXTURES.md:

```bash
# Count fixture files (excluding __pycache__, etc.)
ls tests/fixtures/*.json | wc -l

# Count captured rows in FIXTURES.md
grep -c '|.*| GET\|POST\|PUT\|DELETE' FIXTURES.md
```

Expected: counts match the summary numbers in FIXTURES.md.

## Step 2: Run all examples against staging

```bash
# Run each module individually and check output
for module in address autoprice catalog companies contacts \
              documents forms jobs lookup lots notes parcels \
              payments sellers shipments timeline tracking \
              users web2lead; do
    echo "=== $module ==="
    python -m examples $module 2>&1 | tail -5
done
```

Expected: captured entries succeed, needs-request-data entries
fail with expected errors (not unexpected warnings).

## Step 3: Cross-reference artifacts

```bash
# Check that every fixture file is tracked
for f in tests/fixtures/*.json; do
    name=$(basename "$f" .json)
    grep -q "$name" FIXTURES.md || echo "UNTRACKED: $name"
done

# Check that every captured entry has a fixture file
# (manual: read FIXTURES.md captured table, check each model name)
```

## Step 4: Fix discrepancies and regenerate

1. Move invalid captured entries to needs-request-data
2. Update FIXTURES.md summary counts
3. Update api-surface.md status markers
4. Regenerate progress report:
   ```bash
   python scripts/generate_progress.py
   ```
5. Re-run checks to confirm zero findings
