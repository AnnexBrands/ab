"""Shared module aliases for CLI commands.

Single source of truth for endpoint short names — imported by both
the ``ex`` example runner and the ``ab``/``abs`` endpoint CLIs.
"""

from __future__ import annotations

ALIASES: dict[str, str] = {
    "addr": "address",
    "q": "autoprice",
    "cat": "catalog",
    "co": "companies",
    "ct": "contacts",
    "doc": "documents",
    "form": "forms",
    "job": "jobs",
    "lu": "lookup",
    "lot": "lots",
    "note": "notes",
    "parc": "parcels",
    "pay": "payments",
    "sell": "sellers",
    "ship": "shipments",
    "tk": "timeline",
    "track": "tracking",
    "u": "users",
    "lead": "web2lead",
}
