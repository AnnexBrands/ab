# Quickstart: Update Constitution — Sources of Truth Hierarchy

**Branch**: `010-update-constitution`

## What This Feature Does

Adds a formal "Sources of Truth" hierarchy to the project constitution and updates existing principles and the DISCOVER workflow to reference it. This is a documentation-only change — no code is modified.

## Files to Modify

1. **`.specify/memory/constitution.md`** — Add Sources of Truth section, update Principles II and IV, bump version to 2.3.0 with Sync Impact Report
2. **`.claude/workflows/DISCOVER.md`** — Add server source research to Phase D, add server source path reference table

## Implementation Steps

1. Add the Sync Impact Report comment at the top of `constitution.md`
2. Add the "Sources of Truth" section between Core Principles and API Coverage & Scope
3. Update Principle II to add server source as research step 0
4. Update Principle IV to cross-reference the hierarchy
5. Update the version line at the bottom
6. Update DISCOVER.md Phase D to include server source research
7. Add server source path reference table to DISCOVER.md
8. Run the agent context update script

## Verification

After implementation, verify:
- Constitution version reads 2.3.0
- Sync Impact Report is complete and accurate
- Principles II and IV reference the hierarchy
- DISCOVER Phase D includes server source step
- No contradictions between the new section and existing principles
