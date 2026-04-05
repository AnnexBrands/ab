# Implementation Plan: Lotsdb Migration Prep — Replace ABConnectTools with `ab`

**Branch**: `036-lotsdb-migration-prep` | **Date**: 2026-04-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/opt/pack/ab/specs/036-lotsdb-migration-prep/spec.md`

## Summary

Produce the artifacts a Lotsdb engineer needs to replace `ABConnectTools` (the `ABConnect` package at `/opt/pack/ABConnectTools`) with the new `ab` SDK in `/src/lotsdb`. Three deliverables, all inside the `ab` repo:

1. **`ab_migrate.md`** (repo root) — an authoritative migration guide that enumerates every backward-incompatible change (package rename, exception shape, constructor, model relocations, removed helpers) with before/after snippets.
2. **Endpoint fixture & real-API audit** (`specs/036-lotsdb-migration-prep/audit.md`) — per-endpoint-method record of path/query/body fixture coverage and HTTP-call reality, with gaps closed (missing fixtures added, stubs upgraded).
3. **Lotsdb call-site inventory** (`specs/036-lotsdb-migration-prep/lotsdb-inventory.md`) — every `ABConnect`-referencing line in `/src/lotsdb` mapped to its `ab` replacement (or explicit "remove caller" / "blocks cutover").

Tiebreaker order when `ab` and `ABConnectTools` disagree: (1) `/src/ABConnect/` server source, (2) captured fixtures, (3) swagger snapshots at `/opt/pack/ABConnectTools/ABConnect/base/*.json`, (4) `ABConnectTools` source — per constitution Sources of Truth.

## Technical Context

**Language/Version**: Python 3.11+ (matches existing SDK).
**Primary Dependencies**: pydantic>=2.0, requests (existing `ab` deps — no new runtime deps). Audit tooling uses stdlib only (`ast`, `json`, `pathlib`).
**Storage**: Filesystem — fixture JSON under `tests/fixtures/` and `tests/fixtures/requests/`; audit/inventory/guide as Markdown under the repo.
**Testing**: pytest (existing). New: a reproducible audit script driven by `ast` that enumerates endpoint methods and cross-checks fixtures; fails in CI when gaps regress.
**Target Platform**: Linux developer workstation + CI.
**Project Type**: Single Python library (`ab/`) with tests/ alongside. No new projects.
**Performance Goals**: Audit must complete under 10s on the full endpoint surface (≈25 modules, ≈200 methods).
**Constraints**: No modifications inside `/src/lotsdb`. No network calls during audit (swagger snapshots are on disk). Documentation must render clean in existing Sphinx build (no warnings).
**Scale/Scope**: 25 endpoint modules in `ab/api/endpoints/`, 118 existing request fixtures, 63+ response fixtures, ~7 known Lotsdb call-site files. `ABConnectTools` exports to enumerate: ~5 top-level, ~6 exception classes, ~25 endpoint modules, model aliases.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Evaluated against `/opt/pack/ab/.specify/memory/constitution.md` v2.3.0.

| Principle | Relevance | Assessment |
|-----------|-----------|------------|
| I. Pydantic Model Fidelity | Indirect — audit verifies body fixtures match current request models (`extra="forbid"`); no model changes. | PASS — audit asserts existing models; any gap found is closed by re-capturing, not by fabricating. |
| II. Example-Driven Fixture Capture | Direct — any missing fixture surfaced by the audit is captured via an existing or new example, never fabricated. | PASS — the remediation path for gaps is "run example, capture fixture", not "write JSON by hand". |
| III. Four-Way Harmony | Direct — audit formalizes the check that Implementation + Example + Fixture/Test + Docs exist per endpoint. | PASS — audit is essentially a Four-Way Harmony report scoped to the migration. |
| IV. Swagger-Informed, Reality-Validated | Direct — swagger snapshots in `ABConnectTools/ABConnect/base/*.json` are Tier 3 tiebreaker; server source at `/src/ABConnect/` is Tier 1. | PASS — guide records tiebreaker used per discrepancy. |
| V. Endpoint Status Tracking | Indirect — audit output must be reconcilable with `FIXTURES.md`; any new gap surfaced updates `FIXTURES.md`. | PASS — plan writes deltas back to `FIXTURES.md`. |
| VI. Documentation Completeness | Direct — `ab_migrate.md` is a new doc; must not introduce Sphinx warnings if linked from docs tree. | PASS — guide lives at repo root, not under `docs/`, matching `FIXTURES.md` precedent. |
| VII. Flywheel Evolution | N/A — migration prep, not a flywheel rotation. | PASS — no conflict. |
| VIII. Phase-Based Context Recovery | Direct — this feature has explicit phases (audit → guide → inventory) with committed checkpoints. | PASS — see Phases in this plan. |
| IX. Endpoint Input Validation | Direct — audit enforces that every endpoint method declares its body `RequestModel` and validates inputs before call; "no stub" rule overlaps with "no silent 400". | PASS — audit blocks merge if any endpoint bypasses `RequestModel`. |

**Sources of Truth alignment**: Tiebreaker order documented above matches constitution §Sources of Truth (server source → fixtures → swagger). `ABConnectTools` source appears only as a Tier-4 fallback because it is not listed in the constitution but is called out by the user.

**Verdict**: PASS. No violations. No entries in Complexity Tracking.

## Project Structure

### Documentation (this feature)

```text
specs/036-lotsdb-migration-prep/
├── plan.md                      # This file (/speckit.plan output)
├── spec.md                      # Feature spec
├── research.md                  # Phase 0 output
├── data-model.md                # Phase 1 output — audit record / inventory entry shapes
├── quickstart.md                # Phase 1 output — how to run the audit + consume the guide
├── contracts/
│   ├── audit-report.schema.md   # Shape of the fixture/real-API audit output
│   ├── ab-migrate.outline.md    # Required section outline for ab_migrate.md
│   └── lotsdb-inventory.schema.md  # Shape of each inventory row
├── checklists/
│   └── requirements.md          # Spec quality checklist (already created by /speckit.specify)
└── tasks.md                     # Phase 2 output (/speckit.tasks — NOT created by /speckit.plan)
```

### Source Code (repository root)

This feature produces documentation and one audit tool. No new Python packages, no new `ab/` modules. Only these files change:

```text
/opt/pack/ab/
├── ab_migrate.md                # NEW — migration guide (repo root, alongside FIXTURES.md)
├── scripts/
│   └── audit_lotsdb_migration.py  # NEW — reproducible audit driven by ast over ab/api/endpoints
├── specs/036-lotsdb-migration-prep/
│   ├── audit.md                 # NEW — audit output (checked in so reviewers see current state)
│   └── lotsdb-inventory.md      # NEW — Lotsdb call-site inventory
├── tests/
│   ├── fixtures/requests/       # EXISTING — add fixtures for any audit gaps
│   └── test_migration_audit.py  # NEW — invokes the audit script, fails on regressions
└── FIXTURES.md                  # MODIFIED — if audit surfaces gaps not already tracked
```

**Structure Decision**: Single-project layout; artifacts live under the feature spec directory except for `ab_migrate.md` (user-facing, repo root) and the audit script (shared tooling under `scripts/`). This mirrors existing precedent: `FIXTURES.md` at repo root, feature-specific analysis under `specs/`, tooling under `scripts/`.

## Phases

1. **Phase 0 — Research** (this command, below) → `research.md`: resolve tiebreaker sourcing, freeze `ABConnectTools` surface snapshot, confirm Lotsdb reference set.
2. **Phase 1 — Design & Contracts** (this command, below) → `data-model.md`, `contracts/`, `quickstart.md`, `update-agent-context.sh`: define the shape of the audit record, the migration guide outline, and the inventory row.
3. **Phase 2 — Task breakdown** (`/speckit.tasks`, later) → `tasks.md`: enumerated tasks for writing the guide, running the audit, closing gaps, and producing the inventory.
4. **Phase 3 — Execution** (`/speckit.implement` or manual): run the audit, add missing fixtures via examples, upgrade any stubs, write the guide, produce the inventory, commit.
5. **Phase 4 — Verification**: reviewer dry-runs the migration against the guide + inventory; Lotsdb cutover PR prepared (out of scope for this feature).

## Complexity Tracking

> No Constitution Check violations. Table intentionally empty.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| _(none)_  | _(none)_   | _(none)_                             |
