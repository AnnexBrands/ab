# Implementation Plan: Update Constitution — Sources of Truth Hierarchy

**Branch**: `010-update-constitution` | **Date**: 2026-02-21 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/010-update-constitution/spec.md`

## Summary

Codify a three-tier sources of truth hierarchy in the project constitution: (1) API server source code at `/src/ABConnect/`, (2) captured fixtures from real API responses, (3) swagger specifications. Update existing Principles II and IV to cross-reference the hierarchy, update the DISCOVER workflow's Phase D to include server source research, and bump the constitution version (2.2.0 → 2.3.0) with a Sync Impact Report.

## Technical Context

**Language/Version**: N/A — documentation-only change (Markdown files)
**Primary Dependencies**: N/A — no code dependencies
**Storage**: N/A
**Testing**: Manual review — constitution and workflow are documentation artifacts
**Target Platform**: N/A
**Project Type**: single
**Performance Goals**: N/A
**Constraints**: Must follow constitution amendment procedure (PR with rationale, semantic version bump, Sync Impact Report)
**Scale/Scope**: 3 files modified (constitution, DISCOVER workflow, CLAUDE.md auto-update)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
| --------- | ------ | ----- |
| I. Pydantic Model Fidelity | N/A | No models affected |
| II. Example-Driven Fixture Capture | PASS | Will be updated to reference hierarchy |
| III. Four-Way Harmony | N/A | No endpoint changes |
| IV. Swagger-Informed, Reality-Validated | PASS | Will be updated to reference hierarchy |
| V. Endpoint Status Tracking | N/A | No endpoint changes |
| VI. Documentation Completeness | PASS | Constitution itself is the documentation |
| VII. Flywheel Evolution | PASS | This change is flywheel-driven (stakeholder input → guideline) |
| VIII. Phase-Based Context Recovery | PASS | Workflow will be updated |
| IX. Endpoint Input Validation | N/A | No endpoint changes |
| Governance — Amendment Procedure | PASS | Version bump + Sync Impact Report included |

**Gate result**: PASS — no violations.

## Project Structure

### Documentation (this feature)

```text
specs/010-update-constitution/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (minimal — doc-only feature)
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── constitution-diff.md  # Planned changes to constitution
└── checklists/
    └── requirements.md  # Spec quality checklist
```

### Source Code (repository root)

```text
.specify/memory/
└── constitution.md          # Primary target — add Sources of Truth section

.claude/workflows/
└── DISCOVER.md              # Update Phase D to reference server source
```

**Structure Decision**: No source code changes. This feature modifies two existing documentation files and produces spec artifacts.

## Constitution Check — Post-Design

*Re-evaluated after Phase 1 design. All gates still pass.*

| Principle | Status | Notes |
| --------- | ------ | ----- |
| II. Example-Driven Fixture Capture | PASS | Contract adds server source as research step 0, preserves existing ABConnectTools + swagger steps |
| IV. Swagger-Informed, Reality-Validated | PASS | Contract adds hierarchy cross-reference, preserves swagger's role for discovery |
| VII. Flywheel Evolution | PASS | Stakeholder input (user request) → guideline (hierarchy) → agent guidance (DISCOVER update) |
| Governance — Amendment Procedure | PASS | Sync Impact Report drafted in contracts/constitution-diff.md, version bump planned |

**Gate result**: PASS — ready for `/speckit.tasks`.

## Phase 1 Artifacts

| Artifact | Path | Status |
| -------- | ---- | ------ |
| Research | [research.md](research.md) | Complete — 5 decisions documented |
| Data Model | [data-model.md](data-model.md) | Complete — hierarchy and conflict rules |
| Constitution Diff | [contracts/constitution-diff.md](contracts/constitution-diff.md) | Complete — 4 changes specified |
| Quickstart | [quickstart.md](quickstart.md) | Complete — implementation steps listed |
| Agent Context | `CLAUDE.md` | Updated via script |
