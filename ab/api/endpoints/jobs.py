"""Jobs API endpoints — ACPortal (8 routes) + ABC (1 route).

This file handles two API surfaces. ACPortal routes use the default
``api_surface="acportal"``; the ABC job update route explicitly sets
``api_surface="abc"``.
"""

from __future__ import annotations

from typing import Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route
from ab.http import HttpClient

# ACPortal routes
_CREATE = Route("POST", "/job", request_model="JobCreateRequest")
_SAVE = Route("PUT", "/job/save", request_model="JobSaveRequest")
_GET = Route("GET", "/job/{jobDisplayId}", response_model="Job")
_SEARCH = Route("GET", "/job/search", response_model="List[JobSearchResult]")
_SEARCH_BY_DETAILS = Route("POST", "/job/searchByDetails", request_model="JobSearchRequest", response_model="List[JobSearchResult]")
_GET_PRICE = Route("GET", "/job/{jobDisplayId}/price", response_model="JobPrice")
_GET_CALENDAR = Route("GET", "/job/{jobDisplayId}/calendaritems", response_model="List[CalendarItem]")
_GET_CONFIG = Route("GET", "/job/{jobDisplayId}/updatePageConfig", response_model="JobUpdatePageConfig")

# ABC route (different API surface)
_ABC_UPDATE = Route("POST", "/job/update", request_model="JobUpdateRequest", api_surface="abc")


class JobsEndpoint(BaseEndpoint):
    """Operations on jobs (ACPortal + ABC APIs)."""

    def __init__(self, acportal_client: HttpClient, abc_client: HttpClient) -> None:
        super().__init__(acportal_client)
        self._abc_client = abc_client

    def create(self, data: dict | Any) -> Any:
        """POST /job (ACPortal)"""
        return self._request(_CREATE, json=data)

    def save(self, data: dict | Any) -> Any:
        """PUT /job/save (ACPortal)"""
        return self._request(_SAVE, json=data)

    def get(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId} (ACPortal)"""
        return self._request(_GET.bind(jobDisplayId=job_display_id))

    def search(self, **params: Any) -> Any:
        """GET /job/search (ACPortal) — query params."""
        return self._request(_SEARCH, params=params)

    def search_by_details(self, data: dict | Any) -> Any:
        """POST /job/searchByDetails (ACPortal)"""
        return self._request(_SEARCH_BY_DETAILS, json=data)

    def get_price(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/price (ACPortal)"""
        return self._request(_GET_PRICE.bind(jobDisplayId=job_display_id))

    def get_calendar_items(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/calendaritems (ACPortal)"""
        return self._request(_GET_CALENDAR.bind(jobDisplayId=job_display_id))

    def get_update_page_config(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/updatePageConfig (ACPortal)"""
        return self._request(_GET_CONFIG.bind(jobDisplayId=job_display_id))

    def update(self, data: dict | Any) -> Any:
        """POST /job/update (ABC API surface)"""
        from ab.api.base import BaseEndpoint

        # Use ABC client for this route
        old_client = self._client
        self._client = self._abc_client
        try:
            return self._request(_ABC_UPDATE, json=data)
        finally:
            self._client = old_client
