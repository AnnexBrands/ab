"""Jobs API endpoints — ACPortal (54 routes) + ABC (1 route).

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


# RFQ routes (job-scoped)
_LIST_RFQS = Route("GET", "/job/{jobDisplayId}/rfq", response_model="List[QuoteRequestDisplayInfo]")
_GET_RFQ_STATUS = Route("GET", "/job/{jobDisplayId}/rfq/statusof/{rfqServiceType}/forcompany/{companyId}", response_model="QuoteRequestStatus")

# On-Hold routes
_LIST_ON_HOLD = Route("GET", "/job/{jobDisplayId}/onhold", response_model="List[ExtendedOnHoldInfo]")
_CREATE_ON_HOLD = Route("POST", "/job/{jobDisplayId}/onhold", request_model="SaveOnHoldRequest", response_model="SaveOnHoldResponse")
_DELETE_ON_HOLD = Route("DELETE", "/job/{jobDisplayId}/onhold")
_GET_ON_HOLD = Route("GET", "/job/{jobDisplayId}/onhold/{id}", response_model="OnHoldDetails")
_UPDATE_ON_HOLD = Route("PUT", "/job/{jobDisplayId}/onhold/{onHoldId}", request_model="SaveOnHoldRequest", response_model="SaveOnHoldResponse")
_GET_ON_HOLD_FOLLOWUP_USER = Route("GET", "/job/{jobDisplayId}/onhold/followupuser/{contactId}", response_model="OnHoldUser")
_LIST_ON_HOLD_FOLLOWUP_USERS = Route("GET", "/job/{jobDisplayId}/onhold/followupusers", response_model="List[OnHoldUser]")
_ADD_ON_HOLD_COMMENT = Route("POST", "/job/{jobDisplayId}/onhold/{onHoldId}/comment", response_model="OnHoldNoteDetails")
_UPDATE_ON_HOLD_DATES = Route("PUT", "/job/{jobDisplayId}/onhold/{onHoldId}/dates", request_model="SaveOnHoldDatesModel")
_RESOLVE_ON_HOLD = Route("PUT", "/job/{jobDisplayId}/onhold/{onHoldId}/resolve", response_model="ResolveJobOnHoldResponse")

# Email routes
_SEND_EMAIL = Route("POST", "/job/{jobDisplayId}/email")
_SEND_DOCUMENT_EMAIL = Route("POST", "/job/{jobDisplayId}/email/senddocument", request_model="SendDocumentEmailModel")
_CREATE_TRANSACTIONAL_EMAIL = Route("POST", "/job/{jobDisplayId}/email/createtransactionalemail")
_SEND_TEMPLATE_EMAIL = Route("POST", "/job/{jobDisplayId}/email/{emailTemplateGuid}/send")

# SMS routes
_LIST_SMS = Route("GET", "/job/{jobDisplayId}/sms")
_SEND_SMS = Route("POST", "/job/{jobDisplayId}/sms", request_model="SendSMSModel")
_MARK_SMS_READ = Route("POST", "/job/{jobDisplayId}/sms/read", request_model="MarkSmsAsReadModel")
_GET_SMS_TEMPLATE = Route("GET", "/job/{jobDisplayId}/sms/templatebased/{templateId}")

# Freight routes
_LIST_FREIGHT_PROVIDERS = Route("GET", "/job/{jobDisplayId}/freightproviders", response_model="List[PricedFreightProvider]")
_SAVE_FREIGHT_PROVIDERS = Route("POST", "/job/{jobDisplayId}/freightproviders", request_model="ShipmentPlanProvider")
_GET_FREIGHT_PROVIDER_RATE_QUOTE = Route("POST", "/job/{jobDisplayId}/freightproviders/{optionIndex}/ratequote")
_ADD_FREIGHT_ITEMS = Route("POST", "/job/{jobDisplayId}/freightitems")


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

    # ---- RFQ (job-scoped) -------------------------------------------------

    def list_rfqs(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/rfq (ACPortal)"""
        return self._request(_LIST_RFQS.bind(jobDisplayId=job_display_id))

    def get_rfq_status(self, job_display_id: int, rfq_service_type: str, company_id: str) -> Any:
        """GET /job/{jobDisplayId}/rfq/statusof/{rfqServiceType}/forcompany/{companyId} (ACPortal)"""
        return self._request(_GET_RFQ_STATUS.bind(
            jobDisplayId=job_display_id,
            rfqServiceType=rfq_service_type,
            companyId=company_id,
        ))

    # ---- On-Hold ----------------------------------------------------------

    def list_on_hold(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/onhold (ACPortal)"""
        return self._request(_LIST_ON_HOLD.bind(jobDisplayId=job_display_id))

    def create_on_hold(self, job_display_id: int, **kwargs: Any) -> Any:
        """POST /job/{jobDisplayId}/onhold (ACPortal)"""
        return self._request(_CREATE_ON_HOLD.bind(jobDisplayId=job_display_id), json=kwargs)

    def delete_on_hold(self, job_display_id: int) -> Any:
        """DELETE /job/{jobDisplayId}/onhold (ACPortal)"""
        return self._request(_DELETE_ON_HOLD.bind(jobDisplayId=job_display_id))

    def get_on_hold(self, job_display_id: int, on_hold_id: str) -> Any:
        """GET /job/{jobDisplayId}/onhold/{id} (ACPortal)"""
        return self._request(_GET_ON_HOLD.bind(jobDisplayId=job_display_id, id=on_hold_id))

    def update_on_hold(self, job_display_id: int, on_hold_id: str, **kwargs: Any) -> Any:
        """PUT /job/{jobDisplayId}/onhold/{onHoldId} (ACPortal)"""
        return self._request(_UPDATE_ON_HOLD.bind(jobDisplayId=job_display_id, onHoldId=on_hold_id), json=kwargs)

    def get_on_hold_followup_user(self, job_display_id: int, contact_id: str) -> Any:
        """GET /job/{jobDisplayId}/onhold/followupuser/{contactId} (ACPortal)"""
        return self._request(_GET_ON_HOLD_FOLLOWUP_USER.bind(jobDisplayId=job_display_id, contactId=contact_id))

    def list_on_hold_followup_users(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/onhold/followupusers (ACPortal)"""
        return self._request(_LIST_ON_HOLD_FOLLOWUP_USERS.bind(jobDisplayId=job_display_id))

    def add_on_hold_comment(self, job_display_id: int, on_hold_id: str, **kwargs: Any) -> Any:
        """POST /job/{jobDisplayId}/onhold/{onHoldId}/comment (ACPortal)"""
        return self._request(_ADD_ON_HOLD_COMMENT.bind(jobDisplayId=job_display_id, onHoldId=on_hold_id), json=kwargs)

    def update_on_hold_dates(self, job_display_id: int, on_hold_id: str, **kwargs: Any) -> Any:
        """PUT /job/{jobDisplayId}/onhold/{onHoldId}/dates (ACPortal)"""
        return self._request(_UPDATE_ON_HOLD_DATES.bind(jobDisplayId=job_display_id, onHoldId=on_hold_id), json=kwargs)

    def resolve_on_hold(self, job_display_id: int, on_hold_id: str, **kwargs: Any) -> Any:
        """PUT /job/{jobDisplayId}/onhold/{onHoldId}/resolve (ACPortal)"""
        return self._request(_RESOLVE_ON_HOLD.bind(jobDisplayId=job_display_id, onHoldId=on_hold_id), json=kwargs)

    # ---- Email ------------------------------------------------------------

    def send_email(self, job_display_id: int, **kwargs: Any) -> Any:
        """POST /job/{jobDisplayId}/email (ACPortal)"""
        return self._request(_SEND_EMAIL.bind(jobDisplayId=job_display_id), json=kwargs)

    def send_document_email(self, job_display_id: int, **kwargs: Any) -> Any:
        """POST /job/{jobDisplayId}/email/senddocument (ACPortal)"""
        return self._request(_SEND_DOCUMENT_EMAIL.bind(jobDisplayId=job_display_id), json=kwargs)

    def create_transactional_email(self, job_display_id: int) -> Any:
        """POST /job/{jobDisplayId}/email/createtransactionalemail (ACPortal)"""
        return self._request(_CREATE_TRANSACTIONAL_EMAIL.bind(jobDisplayId=job_display_id))

    def send_template_email(self, job_display_id: int, template_guid: str) -> Any:
        """POST /job/{jobDisplayId}/email/{emailTemplateGuid}/send (ACPortal)"""
        return self._request(_SEND_TEMPLATE_EMAIL.bind(jobDisplayId=job_display_id, emailTemplateGuid=template_guid))

    # ---- SMS --------------------------------------------------------------

    def list_sms(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/sms (ACPortal)"""
        return self._request(_LIST_SMS.bind(jobDisplayId=job_display_id))

    def send_sms(self, job_display_id: int, **kwargs: Any) -> Any:
        """POST /job/{jobDisplayId}/sms (ACPortal)"""
        return self._request(_SEND_SMS.bind(jobDisplayId=job_display_id), json=kwargs)

    def mark_sms_read(self, job_display_id: int, **kwargs: Any) -> Any:
        """POST /job/{jobDisplayId}/sms/read (ACPortal)"""
        return self._request(_MARK_SMS_READ.bind(jobDisplayId=job_display_id), json=kwargs)

    def get_sms_template(self, job_display_id: int, template_id: str) -> Any:
        """GET /job/{jobDisplayId}/sms/templatebased/{templateId} (ACPortal)"""
        return self._request(_GET_SMS_TEMPLATE.bind(jobDisplayId=job_display_id, templateId=template_id))

    # ---- Freight Providers ------------------------------------------------

    def list_freight_providers(self, job_display_id: int, **params: Any) -> Any:
        """GET /job/{jobDisplayId}/freightproviders (ACPortal)"""
        return self._request(_LIST_FREIGHT_PROVIDERS.bind(jobDisplayId=job_display_id), params=params or None)

    def save_freight_providers(self, job_display_id: int, **kwargs: Any) -> Any:
        """POST /job/{jobDisplayId}/freightproviders (ACPortal)"""
        return self._request(_SAVE_FREIGHT_PROVIDERS.bind(jobDisplayId=job_display_id), json=kwargs)

    def get_freight_provider_rate_quote(self, job_display_id: int, option_index: int, **kwargs: Any) -> Any:
        """POST /job/{jobDisplayId}/freightproviders/{optionIndex}/ratequote (ACPortal)"""
        return self._request(_GET_FREIGHT_PROVIDER_RATE_QUOTE.bind(jobDisplayId=job_display_id, optionIndex=option_index), json=kwargs)

    def add_freight_items(self, job_display_id: int, **kwargs: Any) -> Any:
        """POST /job/{jobDisplayId}/freightitems (ACPortal)"""
        return self._request(_ADD_FREIGHT_ITEMS.bind(jobDisplayId=job_display_id), json=kwargs)
