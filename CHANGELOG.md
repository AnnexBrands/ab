# Changelog

All notable changes to `annex-abconnect` are documented here. This project
adheres to [Semantic Versioning](https://semver.org/) (pre-1.0: minor/patch
per 0.x pragmatics). The package is imported as `ab`.

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
