# Contract — `ab_migrate.md` Outline

**Location**: `/opt/pack/ab/ab_migrate.md` (repo root, alongside `FIXTURES.md`).
**Audience**: Lotsdb engineers (and any future consumer of `ABConnectTools`) planning a cutover to `ab`.
**Style**: Reference manual, not a tutorial. Anchors are stable and linkable.

## Required sections (in order)

1. **`# Migrating from ABConnectTools to `ab`** — H1 title.
2. **`## TL;DR`** — 5-line summary: package rename, exception cleanup, constructor narrowing, model relocations, helpers removed.
3. **`## Version and dependency`**
   - Minimum `ab` version Lotsdb should pin.
   - Replacement `pyproject.toml` / `requirements.txt` line.
   - Note on uninstalling `ABConnectTools` after cutover.
4. **`## Package rename`** (anchor `#package-rename`)
   - `from ABConnect …` → `from ab …` table.
   - Note that `ABConnect.models` / `ABConnect.routes` aliases are gone.
5. **`## Removed helpers`** (anchor `#removed-helpers`)
   - One subsection each for `FileLoader`, `APIRequestBuilder`, `Quoter`, with the recommended replacement or explicit "no replacement — rewrite caller".
6. **`## Exceptions`** (anchor `#exceptions`)
   - Table: ABConnectTools class → `ab` class (or "removed").
   - Subsection `#exceptions-removed` for `NotLoggedInError`, `LoginFailedError` (catch `AuthenticationError`).
   - Subsection `#exceptions-shape` explaining that `ABConnectError` in `ab` no longer carries `.code`, `.details`, `.to_dict()`, `.no_traceback()`. Lists the "silently wrong" access patterns Lotsdb must rewrite.
   - Subsection `#exceptions-requesterror` covering the signature change.
7. **`## `ABConnectAPI` constructor`** (anchor `#constructor`)
   - Old signature vs new.
   - Authentication flow replacement for `username=`/`password=` call sites.
   - Django-request flow (`request=`) still supported — no change.
8. **`## Model relocations`** (anchor `#models`)
   - Table mapping every `ABConnect.api.models.catalog.*` symbol used by Lotsdb to its new `ab.api.models.*` location.
   - Explicit entry for `LotCatalogDto` — whether it moved, was renamed, or remains unported.
9. **`## Endpoint parity`** (anchor `#endpoints`)
   - For each Lotsdb-touched endpoint, either "drop-in" or "behavior change — see note".
   - Table of endpoints present in `ABConnectTools` but not yet in `ab`, with recommended action.
10. **`## Tiebreaker log`** (anchor `#tiebreakers`)
    - Table of every discrepancy found during the audit, with the tiebreaker used (server / fixture / swagger / ABConnectTools) and the decision taken.
11. **`## Cutover checklist`** (anchor `#cutover`)
    - Ordered list a Lotsdb engineer ticks off during the cutover PR.
12. **`## Known gaps`** (anchor `#gaps`)
    - Bullet list of issues the guide cannot yet resolve (maps to `InventoryRow.action == "block"`).

## Style rules

- Every break has a "before" and (where possible) "after" code block.
- Use fenced Python blocks with explicit language tag.
- Anchors MUST be stable; rename-with-redirect is not supported.
- No emojis.
- No links out to external URLs that may rot — link to files in this repo or to `/src/ABConnect/` paths instead.
