"""Jobs API endpoints — ACPortal (28 routes) + ABC (1 route).

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

# Timeline routes
_GET_TIMELINE = Route("GET", "/job/{jobDisplayId}/timeline", response_model="List[TimelineTask]")
_POST_TIMELINE = Route("POST", "/job/{jobDisplayId}/timeline", request_model="TimelineTaskCreateRequest", response_model="TimelineTask")
_GET_TIMELINE_TASK = Route("GET", "/job/{jobDisplayId}/timeline/{timelineTaskIdentifier}", response_model="TimelineTask")
_PATCH_TIMELINE_TASK = Route("PATCH", "/job/{jobDisplayId}/timeline/{timelineTaskId}", request_model="TimelineTaskUpdateRequest", response_model="TimelineTask")
_DELETE_TIMELINE_TASK = Route("DELETE", "/job/{jobDisplayId}/timeline/{timelineTaskId}", response_model="ServiceBaseResponse")
_GET_TIMELINE_AGENT = Route("GET", "/job/{jobDisplayId}/timeline/{taskCode}/agent", response_model="TimelineAgent")

# Status routes
_INCREMENT_STATUS = Route("POST", "/job/{jobDisplayId}/timeline/incrementjobstatus", request_model="IncrementStatusRequest", response_model="ServiceBaseResponse")
_UNDO_INCREMENT_STATUS = Route("POST", "/job/{jobDisplayId}/timeline/undoincrementjobstatus", request_model="IncrementStatusRequest", response_model="ServiceBaseResponse")
_SET_QUOTE_STATUS = Route("POST", "/job/{jobDisplayId}/status/quote", response_model="ServiceBaseResponse")

# Tracking routes
_GET_TRACKING = Route("GET", "/job/{jobDisplayId}/tracking", response_model="TrackingInfo")
_GET_TRACKING_V3 = Route("GET", "/v3/job/{jobDisplayId}/tracking/{historyAmount}", response_model="TrackingInfoV3")

# Note routes
_GET_NOTES = Route("GET", "/job/{jobDisplayId}/note", response_model="List[JobNote]")
_POST_NOTE = Route("POST", "/job/{jobDisplayId}/note", request_model="JobNoteCreateRequest", response_model="JobNote")
_GET_NOTE = Route("GET", "/job/{jobDisplayId}/note/{id}", response_model="JobNote")
_PUT_NOTE = Route("PUT", "/job/{jobDisplayId}/note/{id}", request_model="JobNoteUpdateRequest", response_model="JobNote")

# Parcel & Item routes
_GET_PARCEL_ITEMS = Route("GET", "/job/{jobDisplayId}/parcelitems", response_model="List[ParcelItem]")
_POST_PARCEL_ITEM = Route("POST", "/job/{jobDisplayId}/parcelitems", request_model="ParcelItemCreateRequest", response_model="ParcelItem")
_DELETE_PARCEL_ITEM = Route("DELETE", "/job/{jobDisplayId}/parcelitems/{parcelItemId}", response_model="ServiceBaseResponse")
_GET_PARCEL_ITEMS_MATERIALS = Route("GET", "/job/{jobDisplayId}/parcel-items-with-materials", response_model="List[ParcelItemWithMaterials]")
_GET_PACKAGING_CONTAINERS = Route("GET", "/job/{jobDisplayId}/packagingcontainers", response_model="List[PackagingContainer]")
_PUT_ITEM = Route("PUT", "/job/{jobDisplayId}/item/{itemId}", request_model="ItemUpdateRequest", response_model="ServiceBaseResponse")
_POST_ITEM_NOTES = Route("POST", "/job/{jobDisplayId}/item/notes", request_model="ItemNotesRequest", response_model="ServiceBaseResponse")


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
        return self._request(_ABC_UPDATE, client=self._abc_client, json=data)

    # ---- Timeline & Status ------------------------------------------------

    def get_timeline(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/timeline (ACPortal)"""
        return self._request(_GET_TIMELINE.bind(jobDisplayId=job_display_id))

    def create_timeline_task(self, job_display_id: int, data: dict | Any) -> Any:
        """POST /job/{jobDisplayId}/timeline (ACPortal)"""
        return self._request(_POST_TIMELINE.bind(jobDisplayId=job_display_id), json=data)

    def get_timeline_task(self, job_display_id: int, task_id: str) -> Any:
        """GET /job/{jobDisplayId}/timeline/{timelineTaskIdentifier} (ACPortal)"""
        return self._request(_GET_TIMELINE_TASK.bind(jobDisplayId=job_display_id, timelineTaskIdentifier=task_id))

    def update_timeline_task(self, job_display_id: int, task_id: str, data: dict | Any) -> Any:
        """PATCH /job/{jobDisplayId}/timeline/{timelineTaskId} (ACPortal)"""
        return self._request(_PATCH_TIMELINE_TASK.bind(jobDisplayId=job_display_id, timelineTaskId=task_id), json=data)

    def delete_timeline_task(self, job_display_id: int, task_id: str) -> Any:
        """DELETE /job/{jobDisplayId}/timeline/{timelineTaskId} (ACPortal)"""
        return self._request(_DELETE_TIMELINE_TASK.bind(jobDisplayId=job_display_id, timelineTaskId=task_id))

    def get_timeline_agent(self, job_display_id: int, task_code: str) -> Any:
        """GET /job/{jobDisplayId}/timeline/{taskCode}/agent (ACPortal)"""
        return self._request(_GET_TIMELINE_AGENT.bind(jobDisplayId=job_display_id, taskCode=task_code))

    def increment_status(self, job_display_id: int, data: dict | Any | None = None) -> Any:
        """POST /job/{jobDisplayId}/timeline/incrementjobstatus (ACPortal)"""
        kwargs: dict[str, Any] = {}
        if data is not None:
            kwargs["json"] = data
        return self._request(_INCREMENT_STATUS.bind(jobDisplayId=job_display_id), **kwargs)

    def undo_increment_status(self, job_display_id: int, data: dict | Any | None = None) -> Any:
        """POST /job/{jobDisplayId}/timeline/undoincrementjobstatus (ACPortal)"""
        kwargs: dict[str, Any] = {}
        if data is not None:
            kwargs["json"] = data
        return self._request(_UNDO_INCREMENT_STATUS.bind(jobDisplayId=job_display_id), **kwargs)

    def set_quote_status(self, job_display_id: int) -> Any:
        """POST /job/{jobDisplayId}/status/quote (ACPortal)"""
        return self._request(_SET_QUOTE_STATUS.bind(jobDisplayId=job_display_id))

    # ---- Tracking ---------------------------------------------------------

    def get_tracking(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/tracking (ACPortal)"""
        return self._request(_GET_TRACKING.bind(jobDisplayId=job_display_id))

    def get_tracking_v3(self, job_display_id: int, history_amount: int = 10) -> Any:
        """GET /v3/job/{jobDisplayId}/tracking/{historyAmount} (ACPortal)"""
        return self._request(_GET_TRACKING_V3.bind(jobDisplayId=job_display_id, historyAmount=history_amount))

    # ---- Notes ------------------------------------------------------------

    def get_notes(self, job_display_id: int, **params: Any) -> Any:
        """GET /job/{jobDisplayId}/note (ACPortal) — query params."""
        return self._request(_GET_NOTES.bind(jobDisplayId=job_display_id), params=params or None)

    def create_note(self, job_display_id: int, data: dict | Any) -> Any:
        """POST /job/{jobDisplayId}/note (ACPortal)"""
        return self._request(_POST_NOTE.bind(jobDisplayId=job_display_id), json=data)

    def get_note(self, job_display_id: int, note_id: str) -> Any:
        """GET /job/{jobDisplayId}/note/{id} (ACPortal)"""
        return self._request(_GET_NOTE.bind(jobDisplayId=job_display_id, id=note_id))

    def update_note(self, job_display_id: int, note_id: str, data: dict | Any) -> Any:
        """PUT /job/{jobDisplayId}/note/{id} (ACPortal)"""
        return self._request(_PUT_NOTE.bind(jobDisplayId=job_display_id, id=note_id), json=data)

    # ---- Parcels & Items --------------------------------------------------

    def get_parcel_items(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/parcelitems (ACPortal)"""
        return self._request(_GET_PARCEL_ITEMS.bind(jobDisplayId=job_display_id))

    def create_parcel_item(self, job_display_id: int, data: dict | Any) -> Any:
        """POST /job/{jobDisplayId}/parcelitems (ACPortal)"""
        return self._request(_POST_PARCEL_ITEM.bind(jobDisplayId=job_display_id), json=data)

    def delete_parcel_item(self, job_display_id: int, parcel_item_id: str) -> Any:
        """DELETE /job/{jobDisplayId}/parcelitems/{parcelItemId} (ACPortal)"""
        return self._request(_DELETE_PARCEL_ITEM.bind(jobDisplayId=job_display_id, parcelItemId=parcel_item_id))

    def get_parcel_items_with_materials(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/parcel-items-with-materials (ACPortal)"""
        return self._request(_GET_PARCEL_ITEMS_MATERIALS.bind(jobDisplayId=job_display_id))

    def get_packaging_containers(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/packagingcontainers (ACPortal)"""
        return self._request(_GET_PACKAGING_CONTAINERS.bind(jobDisplayId=job_display_id))

    def update_item(self, job_display_id: int, item_id: str, data: dict | Any) -> Any:
        """PUT /job/{jobDisplayId}/item/{itemId} (ACPortal)"""
        return self._request(_PUT_ITEM.bind(jobDisplayId=job_display_id, itemId=item_id), json=data)

    def add_item_notes(self, job_display_id: int, data: dict | Any) -> Any:
        """POST /job/{jobDisplayId}/item/notes (ACPortal)"""
        return self._request(_POST_ITEM_NOTES.bind(jobDisplayId=job_display_id), json=data)
