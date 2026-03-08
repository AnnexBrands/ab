# Research: Client Endpoint Type Hints

**Feature**: 032-client-type-hints
**Date**: 2026-03-08

## R1: Can endpoint imports be used at class-attribute level without circular imports?

**Decision**: Yes — use the same imports already present in `_init_endpoints()`, moved to module-level or kept in the method.

**Rationale**: All 23 endpoint classes are already exported from `ab.api.endpoints.__init__` as runtime imports (not behind `TYPE_CHECKING`). The `_init_endpoints()` method in `client.py` already imports them at runtime. Moving these imports to module-level (or keeping them in the method) and adding type annotations to `self.<attr>: <Type>` is safe.

**Alternatives considered**:
- Class-level annotations (outside `__init__`): Would work for type checkers but doesn't match the existing pattern of lazy initialization in `_init_endpoints()`. Rejected to minimize diff.
- `.pyi` stub file: Would work but adds a separate file to maintain. The existing `py.typed` marker means inline annotations are sufficient. Rejected for maintenance burden.
- `TYPE_CHECKING` guard: Not applicable — these are runtime assignments, not forward references. Type checkers need the annotations to be visible at the assignment site.

## R2: What annotation style to use?

**Decision**: Add inline type annotations on the assignment lines in `_init_endpoints()`:
```python
self.dashboard: DashboardEndpoint = DashboardEndpoint(self._acportal)
```

**Rationale**: This is the simplest change — one token added per line (`:<space><Type>`) with zero behavioral impact. Type checkers (mypy, pyright/Pylance) and IDEs resolve these annotations from the assignment context. The imports are already in scope within the method body.

**Alternatives considered**:
- Class-level `dashboard: DashboardEndpoint` declarations: Would also work but creates a separate declaration site from the assignment, increasing the chance of drift. Rejected for DRY.
- `__init__` signature approach: Not applicable — endpoints are initialized after the constructor body.

## R3: Sphinx autodoc impact

**Decision**: No Sphinx changes needed. Verify build only.

**Rationale**: Sphinx `autodoc` uses `inspect` and reads type annotations from `__init__` or instance attributes. Adding `self.dashboard: DashboardEndpoint` makes the type visible to `autodoc` where it previously wasn't. This is a net improvement — the `ABConnectAPI` class documentation will now show typed attributes. No `conf.py` or `.rst`/`.md` doc file changes required.

## R4: CLI discovery impact

**Decision**: No CLI changes needed. Verify output only.

**Rationale**: The CLI discovery module (`ab/cli/discovery.py`) uses `getattr` and introspection on the `ABConnectAPI` instance. Type annotations don't change `getattr` behavior or the endpoint objects themselves. CLI output will be identical.

## R5: Alias attributes

**Decision**: Add type annotations to both aliases:
```python
self.docs: DocumentsEndpoint = self.documents
self.cmaps: CommodityMapsEndpoint = self.commodity_maps
```

**Rationale**: Without annotations, `api.docs.` won't get autocompletion even though `api.documents.` will. Both aliases are documented and used in client code.
