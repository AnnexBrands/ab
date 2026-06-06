# Changelog

All notable changes to `annex-abconnect` are documented here. This project
adheres to [Semantic Versioning](https://semver.org/) (pre-1.0: minor/patch
per 0.x pragmatics). The package is imported as `ab`.

## [Unreleased] - 0.1.5

An example-coverage release (feature 037). Every previously deprecated
`ExampleRunner` (`examples/_X.py`) example is replaced by a canonical
plain-script `examples/X.py`, so no routed endpoint is backed only by the
deprecated runner anymore. This is additive and docs/examples-only — the
client-construction, auth, config, exceptions, endpoint, and model surface
relied on by downstream consumers is unchanged from `0.1.4`.

> Not yet published — publish once the remaining author-new examples
> (the `jobs.*` subgroups) are mostly done.

### Changed

- **All 114 legacy-only endpoints migrated to canonical examples** — the
  deprecated `examples/_X.py` runner files are superseded by plain-`main()`
  scripts (`catalog`, `commodities`, `commodity_maps`, `companies`(+`_extended`),
  `contacts`(+`_extended`), `documents`, `jobs/core`, `lookup`, `lots`, `notes`,
  `reports`, `rfq`, `shipments`, `views`). Each call binds to the real endpoint
  signature, guards state-changing calls behind `mutations_enabled()`, and saves
  the matching response fixture. Canonical example coverage rises from 34 to 148
  of 209 routed endpoints; `legacy_only_endpoints()` is now empty and the
  `STRICT_NO_LEGACY` coverage gate is hardened to `True`.

## [0.1.4] - 2026-06-05

A documents + discoverability release. The `help()` → Read the Docs rollout now
covers every route-backed group, and the Documents endpoint gains a
swagger-faithful item-photo upload. The client-construction, auth, config,
exceptions, and model-import surface relied on by downstream consumers is
unchanged from `0.1.3`.

### Added

- **Item-photo upload for the Documents endpoint** — `documents.upload` is now a
  typed, route-backed `POST /documents` multipart primitive
  (`DocumentUploadRequest` / `DocumentUploadResponse`), with
  `documents.upload_item_photo` and `documents.upload_item_photos` (batch;
  always returns a list) convenience wrappers.
- **`help()` → Read the Docs for every group** — the per-endpoint page + `Docs:`
  footer mechanism (jobs-only in `0.1.3`) now covers all 21 route-backed groups,
  each with generated per-endpoint pages and a `:glob:` toctree.

### Changed

- **`DocumentType` enum corrected to swagger-truth** — values now mirror the live
  `GET /lookup/documentTypes` lookup (e.g. `BOL = 4`, `ITEM_PHOTO = 6`,
  `OTHER = 7`); the previous values were incorrect. Code referencing the old
  members (`UNKNOWN`, `INVOICE`, `PHOTO`, `CLAIM`, `POD`) or their old integer
  values must update.

### Fixed

- Generated per-endpoint pages now escape pipes in the parameter *type* column,
  so Union types (`DocumentType | int`, `str | None`) no longer break the
  Markdown tables under MyST.
- `jobs.tracking.v3` documents `historyAmount` as a **path** parameter (not a
  query parameter) in both its page heading and its docstring footer.

### CI

- Hardened the PyPI publish job: a tag↔`pyproject` version guard, token-based
  auth, and `skip-existing: true`.

[0.1.4]: https://github.com/AnnexBrands/ab/compare/v0.1.3...v0.1.4

## [0.1.3] - 2026-06-05

A quality & discoverability release. No breaking changes — the public API
surface (client construction, auth, config, exceptions, and models) is
backward compatible with `0.1.2`.

### Added

- **Statically discoverable endpoint groups** — `ABConnectAPI` now carries
  class-level annotations for every endpoint group, so `api.<TAB>` completion
  works in editors and REPLs. Adds public `ABConnectAPI.groups()` and
  `__repr__()`.
- **`help()` → Read the Docs links** — route-backed jobs-group methods now
  carry a `Docs:` footer linking to a rich per-endpoint documentation page,
  plus generated per-endpoint pages for the jobs group.
- **`contacts.get_did` accepts integer display IDs** — the parameter is
  widened from `str` to `str | int` (backward compatible; existing string
  callers are unaffected).

### Changed

- Internal quality gates are now enforced in CI: zero `ruff` violations, a
  green deterministic test suite (`pytest -m "not live"`), and no-drift gates
  for the progress report and generated endpoint docs.

[0.1.3]: https://github.com/AnnexBrands/ab/compare/v0.1.2...v0.1.3
