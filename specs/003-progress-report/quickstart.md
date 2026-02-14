# Quickstart: Progress Report

**Feature**: 003-progress-report

## Generate the Report

From the repository root:

```bash
python scripts/generate_progress.py
```

This produces `progress.html` in the repository root.

## Open the Report

Open `progress.html` in any browser:

```bash
# Linux
xdg-open progress.html

# macOS
open progress.html

# Windows
start progress.html
```

## What You'll See

1. **Summary** — Coverage counts per API surface (ACPortal, Catalog, ABC) with color-coded status.
2. **Action Required: Tier 1** — Scaffolded endpoints that need fixture capture or constants. Each has step-by-step instructions.
3. **Action Required: Tier 2** — Not-started endpoints that need full implementation first.

## Resolving an Item

Follow the step-by-step instructions in the report for any Tier 1 item. Typical flow:

1. Find the right staging entity (the report tells you what kind)
2. Add any missing constants to `tests/constants.py` (the report lists them)
3. Capture the fixture (the report gives you the SDK method call)
4. Save the response to `tests/fixtures/{ModelName}.json`
5. Run `pytest tests/ -k test_{model}` to verify
6. Regenerate: `python scripts/generate_progress.py`

## Adding to .gitignore

The generated `progress.html` is a build artifact. Consider adding it to `.gitignore`:

```
# Generated reports
progress.html
```
