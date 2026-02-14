"""Lookup API endpoints (4 routes)."""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_CONTACT_TYPES = Route("GET", "/lookup/contactTypes", response_model="List[ContactTypeEntity]")
_COUNTRIES = Route("GET", "/lookup/countries", response_model="List[CountryCodeDto]")
_JOB_STATUSES = Route("GET", "/lookup/jobStatuses", response_model="List[JobStatus]")
_ITEMS = Route("GET", "/lookup/items", response_model="List[LookupItem]")


class LookupEndpoint(BaseEndpoint):
    """Reference/lookup data (ACPortal API)."""

    def get_contact_types(self) -> Any:
        """GET /lookup/contactTypes"""
        return self._request(_CONTACT_TYPES)

    def get_countries(self) -> Any:
        """GET /lookup/countries"""
        return self._request(_COUNTRIES)

    def get_job_statuses(self) -> Any:
        """GET /lookup/jobStatuses"""
        return self._request(_JOB_STATUSES)

    def get_items(self) -> Any:
        """GET /lookup/items"""
        return self._request(_ITEMS)
