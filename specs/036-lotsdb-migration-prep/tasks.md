---

description: "Task list for 036-lotsdb-migration-prep — prepare `ab` for Lotsdb cutover by closing or recommending closures for every gap Lotsdb will hit"
---

# Tasks: Lotsdb Migration Prep

**Input**: Design documents in `/opt/pack/ab/specs/036-lotsdb-migration-prep/`
**Prerequisites**: spec.md, plan.md, research.md, gap-recommendations.md

**Scope correction (2026-04-04)**: the original plan leaned on an audit
script that verified the existing `ab` endpoint surface. That was
tooling, not the goal. The real purpose of this spec is to **prepare
`ab` itself** for the Lotsdb cutover — find functional gaps and either
close them or produce concrete, implementable recommendations so a
follow-up PR can close them.

This rewrite drops the audit tasks. The work is:

1. Research what Lotsdb actually needs from `ab`. *(done)*
2. Identify the gaps (correctness bugs, missing models, missing helpers). *(done)*
3. Write the migration guide. *(done)*
4. Write the Lotsdb call-site inventory. *(done)*
5. Write implementable gap recommendations for each gap found. *(done)*
6. Decide per-gap whether to close in this PR, defer to a follow-up, or push to the Lotsdb side. *(done: Gaps 1–5 closed in this branch; Gap 6 deferred to a follow-up; Gap 7 pushed to the Lotsdb side)*
7. **Execute Gap 1–5 closure** — rewrite `ab/api/models/{catalog,lots,sellers}.py` against swagger; fix broken fixtures; update endpoint docstrings. *(done)*

## Format: `[ID] [P?] [Story] Description`

- **[P]**: parallelizable
- **[Story]**: US1 guide, US2 inventory, US3 gap recommendations
- File paths absolute where appropriate

## Path Conventions

- Feature docs: `/opt/pack/ab/specs/036-lotsdb-migration-prep/`
- Migration guide: `/opt/pack/ab/ab_migrate.md` (repo root)
- Gap recommendations: `/opt/pack/ab/specs/036-lotsdb-migration-prep/gap-recommendations.md`
- Lotsdb inventory: `/opt/pack/ab/specs/036-lotsdb-migration-prep/lotsdb-inventory.md`
- `ab` models under review: `/opt/pack/ab/ab/api/models/{catalog,lots}.py`
- Swagger source of truth: `/opt/pack/ab/ab/api/schemas/catalog.json`
- Reference implementation: `/opt/pack/ABConnectTools/ABConnect/api/models/catalog.py`
- Consumer site (read-only): `/src/lotsdb/`

---

## Phase 1: Research (blocking)

Purpose: collect ground-truth facts about the `ab` ↔ `ABConnectTools`
surface delta and Lotsdb's real call sites, so every later claim in the
guide and recommendations can cite a specific line of code.

- [x] T001 Verify prerequisite paths exist and capture a frozen snapshot of `ABConnectTools`'s public surface (`__init__.py`, `exceptions.py`, model module list, endpoint module list).
- [x] T002 Enumerate every Lotsdb file that imports from `ABConnect` via `grep -rn "ABConnect" /src/lotsdb/src /src/lotsdb/pyproject.toml`. Record the raw output.
- [x] T003 For each Lotsdb import, record exactly which symbol(s) are used, which file(s) use them, and the line numbers.
- [x] T004 Compare `ab.api.models.{catalog,lots}` against `ab/api/schemas/catalog.json` for every class Lotsdb uses. Identify drift (wrong field names, missing fields, wrong types, missing classes). Use `python -c "import json; ..."` to enumerate swagger property sets and diff against `cls.model_fields`.
- [x] T005 Inspect `ab/client.py` and `ab/http.py` to confirm whether `ABConnectAPI` supports any credential-based login path. Document the current signature and the identity-server call path.
- [x] T006 Inspect `ABConnectTools/Loader.py` (`FileLoader`) to understand how narrow the Lotsdb usage is. Decide whether `ab` should ship a replacement or Lotsdb should rewrite the single call site.

**Checkpoint**: research notes exist in `research.md` and every gap claim has a line-number citation.

---

## Phase 2: Migration Guide (US1)

- [x] T007 [US1] Create `/opt/pack/ab/ab_migrate.md` at repo root. Required sections: TL;DR, Version and dependency, Package rename, Removed helpers, Exceptions (including silent-regression subsection), `ABConnectAPI` constructor, Model relocations, Endpoint parity, Tiebreaker log, Cutover checklist, Known gaps.
- [x] T008 [US1] Fill the TL;DR with the five top-line breaks: rename, exceptions, constructor, model moves, removed helpers.
- [x] T009 [US1] Fill the Exceptions section documenting `LoginFailedError`/`NotLoggedInError` removal, the attribute loss on `ABConnectError`, and the `RequestError` signature change. Include "silently wrong" examples.
- [x] T010 [US1] Fill the Constructor section documenting the narrowed signature and the Lotsdb-specific implication (user-entered credentials no longer work).
- [x] T011 [US1] Fill the Model relocations section with a table mapping every symbol Lotsdb imports. Explicitly flag `LotCatalogDto`, `BulkInsertCatalogRequest`, `BulkInsertSellerRequest`, `BulkInsertLotRequest` as absent from `ab`.
- [x] T012 [US1] Fill the Endpoint parity section honestly: `ab` has the endpoint surface Lotsdb needs, but several model shapes are currently wrong. Point at the recommendations doc for the complete drift table.
- [x] T013 [US1] Fill the Tiebreaker log with every discrepancy found during Phase 1 research. For each, record which tier (server / fixture / swagger / ABConnectTools) was used and the decision taken.
- [x] T014 [US1] Fill the Cutover checklist — ordered steps the Lotsdb engineer ticks off.
- [x] T015 [US1] Fill the Known gaps section. Each entry points at the matching gap number in `gap-recommendations.md` rather than duplicating content.

**Checkpoint**: `ab_migrate.md` exists, every anchor used by `lotsdb-inventory.md` resolves, no TODOs.

---

## Phase 3: Lotsdb Call-Site Inventory (US2)

- [x] T016 [US2] Create `/opt/pack/ab/specs/036-lotsdb-migration-prep/lotsdb-inventory.md`. Record the exact grep command used to generate the row set at the top of the file for reproducibility.
- [x] T017 [US2] Add one row per `ABConnect`-referencing line in `/src/lotsdb`, with category (import / call / type / string), old text, new text, action (rewrite / remove / block / no_change), guide anchor, and tiebreaker source.
- [x] T018 [US2] Tally totals at the top (rewrite / remove / block / no_change counts) and surface block rows first so reviewers see the blockers before the routine rewrites.
- [x] T019 [US2] Cross-check every row's `guide_anchor` against actual headings in `ab_migrate.md`. No dead anchors.
- [x] T020 [US2] For every row whose rewrite depends on a `ab`-side gap, re-mark it as `block` (not `rewrite`) and link to the relevant section in `gap-recommendations.md`. A row cannot be "mechanically rewritable" if the target symbol has the wrong shape or doesn't exist yet.

**Checkpoint**: inventory is complete, anchors resolve, block rows are honest.

---

## Phase 4: Gap Recommendations (US3 — primary deliverable)

Purpose: produce a document a subsequent implementer can execute without
re-doing the research. Each recommendation names the file to edit, the
target shape with full field lists, the authoritative source for each
claim, and the verification step.

- [x] T021 [US3] Create `/opt/pack/ab/specs/036-lotsdb-migration-prep/gap-recommendations.md`. Summary table at the top: one row per gap with severity + affected Lotsdb files + type (correctness bug / missing model / missing helper / Lotsdb-side rewrite).
- [x] T022 [US3] Write Gap 1–5 (catalog/lot model surface) as a single implementable unit. Include: (a) drift table comparing current `ab` against swagger row-by-row, (b) list of missing classes, (c) full target-state code for `ab/api/models/lots.py` and the delta for `ab/api/models/catalog.py`, (d) fixtures that will need recapture, (e) verification snippet that diffs model field aliases against swagger properties.
- [x] T023 [US3] Write Gap 6 (credential-based login helper). Include: what's broken today (with line citations into `ab/http.py`), target state (`ABConnectAPI.login(username, password)` with both `client.py` and `http.py` snippets), Lotsdb usage pattern after the change, unit-test recipe, and alternatives considered/rejected.
- [x] T024 [US3] Write Gap 7 (FileLoader). Document the narrow Lotsdb surface (one call site, one attribute), recommend solving on the Lotsdb side, include a drop-in pandas/json replacement, and record why porting into `ab` was rejected.
- [x] T025 [US3] Write a "Recommended execution order" section: which PRs go first, which can parallelize, which are Lotsdb-side. Make clear that PR-A (models) and PR-B (login helper) are prerequisites for the Lotsdb cutover PR.
- [x] T026 [US3] Write "What is NOT in scope for this spec" — explicitly note that writing PR-A and PR-B is out of scope for this branch; this feature delivers the recommendations.

**Checkpoint**: `gap-recommendations.md` exists and every gap has enough detail for a focused follow-up PR to implement it without re-research.

---

## Phase 5: Polish & Cross-Cutting

- [x] T027 Verify every anchor used across `ab_migrate.md`, `lotsdb-inventory.md`, and `gap-recommendations.md` resolves.
- [x] T028 Verify the existing `ab` test suite still passes.
- [x] T029 Update `ab_migrate.md` so the Known Gaps section references `gap-recommendations.md` entries by number rather than duplicating content. Single source of truth for each gap.
- [x] T030 Write a one-paragraph handoff note at the top of `spec.md` or in this tasks file noting that the deliverable is docs-only and the follow-up PRs (PR-A models, PR-B login helper) are the next piece of work.

---

## Phase 6: Gap 1–5 Closure (PR-A, executed in-branch)

The original plan deferred model-layer gap closure to a follow-up PR.
That decision was reversed after the recommendations were written —
the rewrite is small enough to execute in this branch, and it removes
the biggest blocker from the Lotsdb cutover.

- [x] T031 Rewrite `ab/api/models/lots.py` with `LotDataDto` (14 fields, mixed-case aliases), `LotCatalogDto`, `LotCatalogInformationDto`, `ImageLinkDto`, `LotDto`, `LotOverrideDto`, correct `AddLotRequest`/`UpdateLotRequest`, preserved `LotListParams`.
- [x] T032 Rewrite `ab/api/models/catalog.py` with `CatalogDto`, `CatalogWithSellersDto`, `CatalogExpandedDto`, correct `AddCatalogRequest`/`UpdateCatalogRequest`, and `BulkInsertRequest` → `BulkInsertCatalogRequest` → `BulkInsertLotRequest`/`BulkInsertSellerRequest` nested shape.
- [x] T033 Fix `ab/api/models/sellers.py::SellerDto` to have the correct `customerDisplayId`/`isActive` fields; absorb the captured-but-not-in-swagger `displayId` field with a docstring note. Keep `SellerExpandedDto.catalogs` as `List[dict]` to avoid the `sellers → catalog` circular import.
- [x] T034 Re-export the new classes from `ab/api/models/__init__.py` so `Route.request_model` resolution and `getattr(models, name)` lookup work.
- [x] T035 Update endpoint docstrings in `ab/api/endpoints/{lots,catalog}.py` that referenced the old (wrong) field names.
- [x] T036 Rewrite the 5 request fixture JSON files (`AddLotRequest.json`, `UpdateLotRequest.json`, `AddCatalogRequest.json`, `UpdateCatalogRequest.json`, `BulkInsertRequest.json`) to match the new model shapes. Use all-null values plus `1970-01-01T00:00:00Z` sentinels for required datetime fields. Note in `gap-recommendations.md` that real capture against staging is still pending.
- [x] T037 Fix the `AddSellerRequest.json` / `UpdateSellerRequest.json` stubs that were broken by the tighter `SellerDto` shape.
- [x] T038 Fix broken response stubs: `SellerDto.json` (missing `customerDisplayId`/`isActive`) and `CatalogExpandedDto.json` (missing required `startDate`/`endDate`/`isCompleted`, had invented `lotCount`/`status`).
- [x] T039 Verify model parity against `ab/api/schemas/catalog.json` for all 16 rewritten/added classes via scripted alias diff.
- [x] T040 Verify a realistic nested `BulkInsertRequest` payload round-trips through the new models with mixed-case `LotDataDto` aliases preserving swagger casing.
- [x] T041 Verify `RequestModel.extra="forbid"` still rejects typos on the new models.
- [x] T042 Run the full pytest suite — 573 passed, 56 skipped, 5 xfailed (same failure count as before Gap 1–5 closure, no regressions).
- [x] T043 Update `ab_migrate.md` Known Gaps section to mark Gaps 1–5 as closed on this branch; update the status table in `gap-recommendations.md`; promote three `block` rows in `lotsdb-inventory.md` to `rewrite` now that their blockers are closed.

**Checkpoint**: PR-A is complete in-branch. PR-B (Gap 6 — `ABConnectAPI.login()` helper) remains open as a follow-up. Lotsdb cutover still blocked on PR-B plus real fixture re-capture against staging.

---

## Dependencies & Execution Order

1. Phase 1 (research) blocks everything else.
2. Phases 2 (guide) and 3 (inventory) can start once research is complete; the inventory depends on the guide only for anchor resolution so the guide skeleton (T007) must land first.
3. Phase 4 (recommendations) can start in parallel with Phases 2–3 as long as Phase 1 is complete.
4. Phase 5 (polish) depends on all earlier phases.

## Dropped tasks from the previous version

The following tasks from the previous version of this file are no
longer part of scope and have been removed:

- Building `scripts/audit_lotsdb_migration.py` (tooling, not deliverable).
- `tests/test_migration_audit.py` + baseline JSON.
- Per-endpoint stub remediation and fixture capture — the existing `ab`
  endpoints are already correct at the HTTP-dispatch level. The real
  gaps are in the **model layer** (see Gap 1–5), not in endpoint
  dispatch.

## Notes

- This spec delivers **documentation and recommendations only**. No
  changes land under `ab/` or `tests/` on this branch.
- Recommendations must be concrete enough that the implementer of
  PR-A or PR-B does not need to re-read `ABConnectTools` or swagger
  from scratch. Every claim cites the specific file and line.
- Tiebreaker order per constitution: server source → captured
  fixtures → swagger → ABConnectTools.
