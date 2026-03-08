# Quickstart: Client Endpoint Type Hints

**Feature**: 032-client-type-hints

## What Changes

One file: `ab/client.py`

Add `: <EndpointType>` annotation to every `self.<endpoint> = ...` line in `_init_endpoints()`, plus the two alias lines at the bottom.

## Before

```python
self.dashboard = DashboardEndpoint(self._acportal)
```

IDE sees `self.dashboard` as `Unknown` — no method completions.

## After

```python
self.dashboard: DashboardEndpoint = DashboardEndpoint(self._acportal)
```

IDE sees `self.dashboard` as `DashboardEndpoint` — full method/signature completions.

## Verification

1. **Tests**: `pytest` — all existing tests pass unchanged
2. **Sphinx**: `sphinx-build docs/ html/` — zero new warnings
3. **CLI**: `ab --list` and `ab dashboard --help` — output identical to before
4. **IDE**: Open a Python file, type `api.dashboard.`, press Ctrl+Space — methods appear

## Scope

- 22 endpoint attributes + 2 aliases = 24 annotation additions
- Zero behavioral changes
- Zero new files
- Zero new dependencies
