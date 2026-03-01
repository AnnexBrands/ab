"""Jobs API endpoints — ACPortal (54 routes) + ABC (1 route).

This file handles two API surfaces. ACPortal routes use the default
``api_surface="acportal"``; the ABC job update route explicitly sets
``api_surface="abc"``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ab.api.base import BaseEndpoint
from ab.api.route import Route
from ab.cache import CodeResolver
from ab.http import HttpClient

if TYPE_CHECKING:
    from ab.api.models.jobs import (
        CalendarItem,
        ExtendedOnHoldInfo,
        FreightItemsRequest,
        IncrementStatusRequest,
        ItemNotesRequest,
        ItemUpdateRequest,
        Job,
        JobCreateRequest,
        JobNote,
        JobNoteCreateRequest,
        JobNoteUpdateRequest,
        JobPrice,
        JobSaveRequest,
        JobSearchRequest,
        JobSearchResult,
        JobUpdatePageConfig,
        JobUpdateRequest,
        MarkSmsAsReadModel,
        OnHoldCommentRequest,
        OnHoldDetails,
        OnHoldNoteDetails,
        OnHoldUser,
        PackagingContainer,
        ParcelItem,
        ParcelItemCreateRequest,
        ParcelItemWithMaterials,
        PricedFreightProvider,
        RateQuoteRequest,
        ResolveJobOnHoldResponse,
        ResolveOnHoldRequest,
        SaveOnHoldDatesModel,
        SaveOnHoldRequest,
        SaveOnHoldResponse,
        SendDocumentEmailModel,
        SendEmailRequest,
        SendSMSModel,
        ShipmentPlanProvider,
        SortByModel,
        TimelineAgent,
        TimelineTask,
        TimelineTaskCreateRequest,
        TimelineTaskUpdateRequest,
        TrackingInfo,
        TrackingInfoV3,
    )
    from ab.api.models.rfq import QuoteRequestDisplayInfo, QuoteRequestStatus
    from ab.api.models.shared import ServiceBaseResponse

# ACPortal routes
_CREATE = Route("POST", "/job", request_model="JobCreateRequest")
_SAVE = Route("PUT", "/job/save", request_model="JobSaveRequest")
_GET = Route("GET", "/job/{jobDisplayId}", response_model="Job")
_SEARCH = Route("GET", "/job/search", params_model="JobSearchParams", response_model="JobSearchResult")
_SEARCH_BY_DETAILS = Route(
    "POST", "/job/searchByDetails",
    request_model="JobSearchRequest", response_model="List[JobSearchResult]",
)
_GET_PRICE = Route("GET", "/job/{jobDisplayId}/price", response_model="JobPrice")
_GET_CALENDAR = Route("GET", "/job/{jobDisplayId}/calendaritems", response_model="List[CalendarItem]")
_GET_CONFIG = Route("GET", "/job/{jobDisplayId}/updatePageConfig", response_model="JobUpdatePageConfig")

# Transfer route
_TRANSFER = Route("POST", "/job/transfer/{jobDisplayId}", request_model="TransferModel")

# ABC route (different API surface)
_ABC_UPDATE = Route("POST", "/job/update", request_model="JobUpdateRequest", api_surface="abc")

# Timeline routes
_GET_TIMELINE = Route("GET", "/job/{jobDisplayId}/timeline", response_model="List[TimelineTask]")
_POST_TIMELINE = Route(
    "POST", "/job/{jobDisplayId}/timeline",
    request_model="TimelineTaskCreateRequest", response_model="TimelineTask",
    params_model="TimelineCreateParams",
)
_GET_TIMELINE_TASK = Route(
    "GET", "/job/{jobDisplayId}/timeline/{timelineTaskIdentifier}", response_model="TimelineTask",
)
_PATCH_TIMELINE_TASK = Route(
    "PATCH", "/job/{jobDisplayId}/timeline/{timelineTaskId}",
    request_model="TimelineTaskUpdateRequest", response_model="TimelineTask",
)
_DELETE_TIMELINE_TASK = Route(
    "DELETE", "/job/{jobDisplayId}/timeline/{timelineTaskId}", response_model="ServiceBaseResponse",
)
_GET_TIMELINE_AGENT = Route(
    "GET", "/job/{jobDisplayId}/timeline/{taskCode}/agent", response_model="TimelineAgent",
)

# Status routes
_INCREMENT_STATUS = Route(
    "POST", "/job/{jobDisplayId}/timeline/incrementjobstatus",
    request_model="IncrementStatusRequest", response_model="ServiceBaseResponse",
)
_UNDO_INCREMENT_STATUS = Route(
    "POST", "/job/{jobDisplayId}/timeline/undoincrementjobstatus",
    request_model="IncrementStatusRequest", response_model="ServiceBaseResponse",
)
_SET_QUOTE_STATUS = Route("POST", "/job/{jobDisplayId}/status/quote", response_model="ServiceBaseResponse")

# Tracking routes
_GET_TRACKING = Route("GET", "/job/{jobDisplayId}/tracking", response_model="TrackingInfo")
_GET_TRACKING_V3 = Route(
    "GET", "/v3/job/{jobDisplayId}/tracking/{historyAmount}", response_model="TrackingInfoV3",
    params_model="TrackingV3Params",
)

# Note routes
_GET_NOTES = Route("GET", "/job/{jobDisplayId}/note", params_model="JobNoteListParams", response_model="List[JobNote]")
_POST_NOTE = Route(
    "POST", "/job/{jobDisplayId}/note",
    request_model="JobNoteCreateRequest", response_model="JobNote",
)
_GET_NOTE = Route("GET", "/job/{jobDisplayId}/note/{id}", response_model="JobNote")
_PUT_NOTE = Route(
    "PUT", "/job/{jobDisplayId}/note/{id}",
    request_model="JobNoteUpdateRequest", response_model="JobNote",
)

# Parcel & Item routes
_GET_PARCEL_ITEMS = Route("GET", "/job/{jobDisplayId}/parcelitems", response_model="List[ParcelItem]")
_POST_PARCEL_ITEM = Route(
    "POST", "/job/{jobDisplayId}/parcelitems",
    request_model="ParcelItemCreateRequest", response_model="ParcelItem",
)
_DELETE_PARCEL_ITEM = Route(
    "DELETE", "/job/{jobDisplayId}/parcelitems/{parcelItemId}", response_model="ServiceBaseResponse",
)
_GET_PARCEL_ITEMS_MATERIALS = Route(
    "GET", "/job/{jobDisplayId}/parcel-items-with-materials",
    response_model="List[ParcelItemWithMaterials]",
)
_GET_PACKAGING_CONTAINERS = Route(
    "GET", "/job/{jobDisplayId}/packagingcontainers", response_model="List[PackagingContainer]",
)
_PUT_ITEM = Route(
    "PUT", "/job/{jobDisplayId}/item/{itemId}",
    request_model="ItemUpdateRequest", response_model="ServiceBaseResponse",
)
_POST_ITEM_NOTES = Route(
    "POST", "/job/{jobDisplayId}/item/notes",
    request_model="ItemNotesRequest", response_model="ServiceBaseResponse",
)


# RFQ routes (job-scoped)
_LIST_RFQS = Route("GET", "/job/{jobDisplayId}/rfq", params_model="JobRfqListParams", response_model="List[QuoteRequestDisplayInfo]")
_GET_RFQ_STATUS = Route(
    "GET", "/job/{jobDisplayId}/rfq/statusof/{rfqServiceType}/forcompany/{companyId}",
    response_model="QuoteRequestStatus",
)

# On-Hold routes
_LIST_ON_HOLD = Route("GET", "/job/{jobDisplayId}/onhold", response_model="List[ExtendedOnHoldInfo]")
_CREATE_ON_HOLD = Route(
    "POST", "/job/{jobDisplayId}/onhold",
    request_model="SaveOnHoldRequest", response_model="SaveOnHoldResponse",
)
_DELETE_ON_HOLD = Route("DELETE", "/job/{jobDisplayId}/onhold")
_GET_ON_HOLD = Route("GET", "/job/{jobDisplayId}/onhold/{id}", response_model="OnHoldDetails")
_UPDATE_ON_HOLD = Route(
    "PUT", "/job/{jobDisplayId}/onhold/{onHoldId}",
    request_model="SaveOnHoldRequest", response_model="SaveOnHoldResponse",
)
_GET_ON_HOLD_FOLLOWUP_USER = Route(
    "GET", "/job/{jobDisplayId}/onhold/followupuser/{contactId}", response_model="OnHoldUser",
)
_LIST_ON_HOLD_FOLLOWUP_USERS = Route(
    "GET", "/job/{jobDisplayId}/onhold/followupusers", response_model="List[OnHoldUser]",
)
_ADD_ON_HOLD_COMMENT = Route(
    "POST", "/job/{jobDisplayId}/onhold/{onHoldId}/comment",
    request_model="OnHoldCommentRequest", response_model="OnHoldNoteDetails",
)
_UPDATE_ON_HOLD_DATES = Route(
    "PUT", "/job/{jobDisplayId}/onhold/{onHoldId}/dates", request_model="SaveOnHoldDatesModel",
)
_RESOLVE_ON_HOLD = Route(
    "PUT", "/job/{jobDisplayId}/onhold/{onHoldId}/resolve",
    request_model="ResolveOnHoldRequest", response_model="ResolveJobOnHoldResponse",
)

# Email routes
_SEND_EMAIL = Route("POST", "/job/{jobDisplayId}/email", request_model="SendEmailRequest")
_SEND_DOCUMENT_EMAIL = Route(
    "POST", "/job/{jobDisplayId}/email/senddocument", request_model="SendDocumentEmailModel",
)
_CREATE_TRANSACTIONAL_EMAIL = Route("POST", "/job/{jobDisplayId}/email/createtransactionalemail")
_SEND_TEMPLATE_EMAIL = Route("POST", "/job/{jobDisplayId}/email/{emailTemplateGuid}/send")

# SMS routes
_LIST_SMS = Route("GET", "/job/{jobDisplayId}/sms")
_SEND_SMS = Route("POST", "/job/{jobDisplayId}/sms", request_model="SendSMSModel")
_MARK_SMS_READ = Route("POST", "/job/{jobDisplayId}/sms/read", request_model="MarkSmsAsReadModel")
_GET_SMS_TEMPLATE = Route("GET", "/job/{jobDisplayId}/sms/templatebased/{templateId}")

# Freight routes
_LIST_FREIGHT_PROVIDERS = Route(
    "GET", "/job/{jobDisplayId}/freightproviders",
    params_model="FreightProvidersParams", response_model="List[PricedFreightProvider]",
)
_SAVE_FREIGHT_PROVIDERS = Route(
    "POST", "/job/{jobDisplayId}/freightproviders", request_model="ShipmentPlanProvider",
)
_GET_FREIGHT_PROVIDER_RATE_QUOTE = Route(
    "POST", "/job/{jobDisplayId}/freightproviders/{optionIndex}/ratequote",
    request_model="RateQuoteRequest",
)
_ADD_FREIGHT_ITEMS = Route(
    "POST", "/job/{jobDisplayId}/freightitems",
    request_model="FreightItemsRequest",
)


class JobsEndpoint(BaseEndpoint):
    """Operations on jobs (ACPortal + ABC APIs)."""

    def __init__(self, acportal_client: HttpClient, abc_client: HttpClient, resolver: CodeResolver) -> None:
        super().__init__(acportal_client)
        self._abc_client = abc_client
        self._resolver = resolver

    def create(self, *, data: JobCreateRequest | dict) -> Any:
        """POST /job.

        Args:
            data: Job creation payload with customer, pickup, delivery,
                items, and services. Accepts a :class:`JobCreateRequest`
                instance or a dict.

        Request model: :class:`JobCreateRequest`
        """
        return self._request(_CREATE, json=data)

    def save(self, *, data: JobSaveRequest | dict) -> Any:
        """PUT /job/save.

        Args:
            data: Job save payload with jobDisplayId, customer, pickup,
                delivery, and items. Accepts a :class:`JobSaveRequest`
                instance or a dict.

        Request model: :class:`JobSaveRequest`
        """
        return self._request(_SAVE, json=data)

    def get(self, job_display_id: int) -> Job:
        """GET /job/{jobDisplayId} (ACPortal)"""
        return self._request(_GET.bind(jobDisplayId=job_display_id))

    def search(self, *, job_display_id: int | None = None) -> JobSearchResult:
        """GET /job/search (ACPortal) — query params."""
        return self._request(_SEARCH, params=dict(job_display_id=job_display_id))

    def search_by_details(self, *, data: JobSearchRequest | dict) -> list[JobSearchResult]:
        """POST /job/searchByDetails.

        Args:
            data: Search filter with search_text, page, page_size, and
                sort_by. Accepts a :class:`JobSearchRequest` instance
                or a dict.

        Request model: :class:`JobSearchRequest`
        """
        return self._request(_SEARCH_BY_DETAILS, json=data)

    def get_price(self, job_display_id: int) -> JobPrice:
        """GET /job/{jobDisplayId}/price (ACPortal)"""
        return self._request(_GET_PRICE.bind(jobDisplayId=job_display_id))

    def get_calendar_items(self, job_display_id: int) -> list[CalendarItem]:
        """GET /job/{jobDisplayId}/calendaritems (ACPortal)"""
        return self._request(_GET_CALENDAR.bind(jobDisplayId=job_display_id))

    def get_update_page_config(self, job_display_id: int) -> JobUpdatePageConfig:
        """GET /job/{jobDisplayId}/updatePageConfig (ACPortal)"""
        return self._request(_GET_CONFIG.bind(jobDisplayId=job_display_id))

    def update(self, *, data: JobUpdateRequest | dict) -> Any:
        """POST /job/update (ABC API surface).

        Args:
            data: Job update payload with job_id and updates.
                Accepts a :class:`JobUpdateRequest` instance or a dict.

        Request model: :class:`JobUpdateRequest`
        """
        return self._request(_ABC_UPDATE, client=self._abc_client, json=data)

    def transfer(self, job_display_id: int, franchisee_id: str) -> Any:
        """POST /job/transfer/{jobDisplayId} (ACPortal)

        Args:
            job_display_id: Job to transfer.
            franchisee_id: Target franchisee — accepts a company code
                (e.g. ``"9999AZ"``) or UUID.
        """
        resolved = self._resolver.resolve(franchisee_id)
        return self._request(
            _TRANSFER.bind(jobDisplayId=job_display_id),
            json={"franchiseeId": resolved},
        )

    # ---- Timeline & Status ------------------------------------------------

    def get_timeline(self, job_display_id: int) -> list[TimelineTask]:
        """GET /job/{jobDisplayId}/timeline (ACPortal)"""
        return self._request(_GET_TIMELINE.bind(jobDisplayId=job_display_id))

    def create_timeline_task(
        self,
        job_display_id: int,
        *,
        data: TimelineTaskCreateRequest | dict,
        create_email: bool | None = None,
    ) -> TimelineTask:
        """POST /job/{jobDisplayId}/timeline.

        Args:
            job_display_id: Job display ID.
            data: Timeline task payload with task_code, scheduled_date,
                comments, and agent_contact_id. Accepts a
                :class:`TimelineTaskCreateRequest` instance or a dict.
            create_email: Send status notification email (query param).

        Request model: :class:`TimelineTaskCreateRequest`
        Params model: :class:`TimelineCreateParams`
        """
        params = dict(create_email=create_email)
        return self._request(
            _POST_TIMELINE.bind(jobDisplayId=job_display_id), json=data, params=params,
        )

    def get_timeline_task(self, job_display_id: int, task_id: str) -> TimelineTask:
        """GET /job/{jobDisplayId}/timeline/{timelineTaskIdentifier} (ACPortal)"""
        return self._request(
            _GET_TIMELINE_TASK.bind(jobDisplayId=job_display_id, timelineTaskIdentifier=task_id),
        )

    def update_timeline_task(
        self,
        job_display_id: int,
        task_id: str,
        *,
        data: TimelineTaskUpdateRequest | dict,
    ) -> TimelineTask:
        """PATCH /job/{jobDisplayId}/timeline/{timelineTaskId}.

        Args:
            job_display_id: Job display ID.
            task_id: Timeline task identifier.
            data: Timeline task update payload with status, scheduled_date,
                completed_date, and comments. Accepts a
                :class:`TimelineTaskUpdateRequest` instance or a dict.

        Request model: :class:`TimelineTaskUpdateRequest`
        """
        return self._request(
            _PATCH_TIMELINE_TASK.bind(jobDisplayId=job_display_id, timelineTaskId=task_id),
            json=data,
        )

    def delete_timeline_task(self, job_display_id: int, task_id: str) -> ServiceBaseResponse:
        """DELETE /job/{jobDisplayId}/timeline/{timelineTaskId} (ACPortal)"""
        return self._request(
            _DELETE_TIMELINE_TASK.bind(jobDisplayId=job_display_id, timelineTaskId=task_id),
        )

    def get_timeline_agent(self, job_display_id: int, task_code: str) -> TimelineAgent:
        """GET /job/{jobDisplayId}/timeline/{taskCode}/agent (ACPortal)"""
        return self._request(
            _GET_TIMELINE_AGENT.bind(jobDisplayId=job_display_id, taskCode=task_code),
        )

    def increment_status(
        self,
        job_display_id: int,
        *,
        data: IncrementStatusRequest | dict,
    ) -> ServiceBaseResponse:
        """POST /job/{jobDisplayId}/timeline/incrementjobstatus.

        Args:
            job_display_id: Job display ID.
            data: Status increment payload with create_email flag.
                Accepts an :class:`IncrementStatusRequest` instance or a dict.

        Request model: :class:`IncrementStatusRequest`
        """
        return self._request(_INCREMENT_STATUS.bind(jobDisplayId=job_display_id), json=data)

    def undo_increment_status(
        self,
        job_display_id: int,
        *,
        data: IncrementStatusRequest | dict,
    ) -> ServiceBaseResponse:
        """POST /job/{jobDisplayId}/timeline/undoincrementjobstatus.

        Args:
            job_display_id: Job display ID.
            data: Status undo payload with create_email flag.
                Accepts an :class:`IncrementStatusRequest` instance or a dict.

        Request model: :class:`IncrementStatusRequest`
        """
        return self._request(
            _UNDO_INCREMENT_STATUS.bind(jobDisplayId=job_display_id), json=data,
        )

    def set_quote_status(self, job_display_id: int) -> ServiceBaseResponse:
        """POST /job/{jobDisplayId}/status/quote (ACPortal)"""
        return self._request(_SET_QUOTE_STATUS.bind(jobDisplayId=job_display_id))

    # ---- Tracking ---------------------------------------------------------

    def get_tracking(self, job_display_id: int) -> TrackingInfo:
        """GET /job/{jobDisplayId}/tracking (ACPortal)"""
        return self._request(_GET_TRACKING.bind(jobDisplayId=job_display_id))

    def get_tracking_v3(self, job_display_id: int, history_amount: int = 10) -> TrackingInfoV3:
        """GET /v3/job/{jobDisplayId}/tracking/{historyAmount} (ACPortal)"""
        return self._request(
            _GET_TRACKING_V3.bind(jobDisplayId=job_display_id, historyAmount=history_amount),
        )

    # ---- Notes ------------------------------------------------------------

    def get_notes(
        self,
        job_display_id: int,
        *,
        category: str | None = None,
        task_code: str | None = None,
    ) -> list[JobNote]:
        """GET /job/{jobDisplayId}/note.

        Args:
            job_display_id: Job display ID.
            category: Note category filter.
            task_code: Task code filter.

        Params model: :class:`JobNoteListParams`
        """
        params = dict(category=category, task_code=task_code)
        return self._request(_GET_NOTES.bind(jobDisplayId=job_display_id), params=params)

    def create_note(
        self,
        job_display_id: int,
        *,
        data: JobNoteCreateRequest | dict,
    ) -> JobNote:
        """POST /job/{jobDisplayId}/note.

        Args:
            job_display_id: Job display ID.
            data: Note creation payload with comments, task_code,
                is_important, send_notification, and due_date. Accepts a
                :class:`JobNoteCreateRequest` instance or a dict.

        Request model: :class:`JobNoteCreateRequest`
        """
        return self._request(_POST_NOTE.bind(jobDisplayId=job_display_id), json=data)

    def get_note(self, job_display_id: int, note_id: str) -> JobNote:
        """GET /job/{jobDisplayId}/note/{id} (ACPortal)"""
        return self._request(_GET_NOTE.bind(jobDisplayId=job_display_id, id=note_id))

    def update_note(
        self,
        job_display_id: int,
        note_id: str,
        *,
        data: JobNoteUpdateRequest | dict,
    ) -> JobNote:
        """PUT /job/{jobDisplayId}/note/{id}.

        Args:
            job_display_id: Job display ID.
            note_id: Note identifier.
            data: Note update payload with comments, is_important,
                and is_completed. Accepts a :class:`JobNoteUpdateRequest`
                instance or a dict.

        Request model: :class:`JobNoteUpdateRequest`
        """
        return self._request(
            _PUT_NOTE.bind(jobDisplayId=job_display_id, id=note_id), json=data,
        )

    # ---- Parcels & Items --------------------------------------------------

    def get_parcel_items(self, job_display_id: int) -> list[ParcelItem]:
        """GET /job/{jobDisplayId}/parcelitems (ACPortal)"""
        return self._request(_GET_PARCEL_ITEMS.bind(jobDisplayId=job_display_id))

    def create_parcel_item(
        self,
        job_display_id: int,
        *,
        data: ParcelItemCreateRequest | dict,
    ) -> ParcelItem:
        """POST /job/{jobDisplayId}/parcelitems.

        Args:
            job_display_id: Job display ID.
            data: Parcel item payload with description, length, width,
                height, weight, and quantity. Accepts a
                :class:`ParcelItemCreateRequest` instance or a dict.

        Request model: :class:`ParcelItemCreateRequest`
        """
        return self._request(_POST_PARCEL_ITEM.bind(jobDisplayId=job_display_id), json=data)

    def delete_parcel_item(self, job_display_id: int, parcel_item_id: str) -> ServiceBaseResponse:
        """DELETE /job/{jobDisplayId}/parcelitems/{parcelItemId} (ACPortal)"""
        return self._request(
            _DELETE_PARCEL_ITEM.bind(jobDisplayId=job_display_id, parcelItemId=parcel_item_id),
        )

    def get_parcel_items_with_materials(self, job_display_id: int) -> list[ParcelItemWithMaterials]:
        """GET /job/{jobDisplayId}/parcel-items-with-materials (ACPortal)"""
        return self._request(_GET_PARCEL_ITEMS_MATERIALS.bind(jobDisplayId=job_display_id))

    def get_packaging_containers(self, job_display_id: int) -> list[PackagingContainer]:
        """GET /job/{jobDisplayId}/packagingcontainers (ACPortal)"""
        return self._request(_GET_PACKAGING_CONTAINERS.bind(jobDisplayId=job_display_id))

    def update_item(
        self,
        job_display_id: int,
        item_id: str,
        *,
        data: ItemUpdateRequest | dict,
    ) -> ServiceBaseResponse:
        """PUT /job/{jobDisplayId}/item/{itemId}.

        Args:
            job_display_id: Job display ID.
            item_id: Item identifier.
            data: Item update payload with description, quantity, and weight.
                Accepts an :class:`ItemUpdateRequest` instance or a dict.

        Request model: :class:`ItemUpdateRequest`
        """
        return self._request(
            _PUT_ITEM.bind(jobDisplayId=job_display_id, itemId=item_id), json=data,
        )

    def add_item_notes(
        self,
        job_display_id: int,
        *,
        data: ItemNotesRequest | dict,
    ) -> ServiceBaseResponse:
        """POST /job/{jobDisplayId}/item/notes.

        Args:
            job_display_id: Job display ID.
            data: Item notes payload. Accepts an :class:`ItemNotesRequest`
                instance or a dict.

        Request model: :class:`ItemNotesRequest`
        """
        return self._request(_POST_ITEM_NOTES.bind(jobDisplayId=job_display_id), json=data)

    # ---- RFQ (job-scoped) -------------------------------------------------

    def list_rfqs(self, job_display_id: int) -> list[QuoteRequestDisplayInfo]:
        """GET /job/{jobDisplayId}/rfq (ACPortal)"""
        return self._request(_LIST_RFQS.bind(jobDisplayId=job_display_id))

    def get_rfq_status(self, job_display_id: int, rfq_service_type: str, company_id: str) -> QuoteRequestStatus:
        """GET /job/{jobDisplayId}/rfq/statusof/{rfqServiceType}/forcompany/{companyId} (ACPortal)"""
        return self._request(_GET_RFQ_STATUS.bind(
            jobDisplayId=job_display_id,
            rfqServiceType=rfq_service_type,
            companyId=company_id,
        ))

    # ---- On-Hold ----------------------------------------------------------

    def list_on_hold(self, job_display_id: int) -> list[ExtendedOnHoldInfo]:
        """GET /job/{jobDisplayId}/onhold (ACPortal)"""
        return self._request(_LIST_ON_HOLD.bind(jobDisplayId=job_display_id))

    def create_on_hold(
        self,
        job_display_id: int,
        *,
        data: SaveOnHoldRequest | dict,
    ) -> SaveOnHoldResponse:
        """POST /job/{jobDisplayId}/onhold.

        Args:
            job_display_id: Job display ID.
            data: On-hold payload with reason, description,
                follow_up_contact_id, and follow_up_date. Accepts a
                :class:`SaveOnHoldRequest` instance or a dict.

        Request model: :class:`SaveOnHoldRequest`
        """
        return self._request(_CREATE_ON_HOLD.bind(jobDisplayId=job_display_id), json=data)

    def delete_on_hold(self, job_display_id: int) -> Any:
        """DELETE /job/{jobDisplayId}/onhold (ACPortal)"""
        return self._request(_DELETE_ON_HOLD.bind(jobDisplayId=job_display_id))

    def get_on_hold(self, job_display_id: int, on_hold_id: str) -> OnHoldDetails:
        """GET /job/{jobDisplayId}/onhold/{id} (ACPortal)"""
        return self._request(_GET_ON_HOLD.bind(jobDisplayId=job_display_id, id=on_hold_id))

    def update_on_hold(
        self,
        job_display_id: int,
        on_hold_id: str,
        *,
        data: SaveOnHoldRequest | dict,
    ) -> SaveOnHoldResponse:
        """PUT /job/{jobDisplayId}/onhold/{onHoldId}.

        Args:
            job_display_id: Job display ID.
            on_hold_id: On-hold record identifier.
            data: On-hold payload with reason, description,
                follow_up_contact_id, and follow_up_date. Accepts a
                :class:`SaveOnHoldRequest` instance or a dict.

        Request model: :class:`SaveOnHoldRequest`
        """
        return self._request(
            _UPDATE_ON_HOLD.bind(jobDisplayId=job_display_id, onHoldId=on_hold_id), json=data,
        )

    def get_on_hold_followup_user(self, job_display_id: int, contact_id: str) -> OnHoldUser:
        """GET /job/{jobDisplayId}/onhold/followupuser/{contactId} (ACPortal)"""
        return self._request(
            _GET_ON_HOLD_FOLLOWUP_USER.bind(jobDisplayId=job_display_id, contactId=contact_id),
        )

    def list_on_hold_followup_users(self, job_display_id: int) -> list[OnHoldUser]:
        """GET /job/{jobDisplayId}/onhold/followupusers (ACPortal)"""
        return self._request(_LIST_ON_HOLD_FOLLOWUP_USERS.bind(jobDisplayId=job_display_id))

    def add_on_hold_comment(
        self, job_display_id: int, on_hold_id: str, *, data: OnHoldCommentRequest | dict,
    ) -> OnHoldNoteDetails:
        """POST /job/{jobDisplayId}/onhold/{onHoldId}/comment.

        Args:
            job_display_id: Job display ID.
            on_hold_id: On-hold record identifier.
            data: Comment payload. Accepts an :class:`OnHoldCommentRequest`
                instance or a dict.

        Request model: :class:`OnHoldCommentRequest`
        """
        return self._request(
            _ADD_ON_HOLD_COMMENT.bind(jobDisplayId=job_display_id, onHoldId=on_hold_id),
            json=data,
        )

    def update_on_hold_dates(
        self,
        job_display_id: int,
        on_hold_id: str,
        *,
        data: SaveOnHoldDatesModel | dict,
    ) -> Any:
        """PUT /job/{jobDisplayId}/onhold/{onHoldId}/dates.

        Args:
            job_display_id: Job display ID.
            on_hold_id: On-hold record identifier.
            data: On-hold dates payload with follow_up_date and due_date.
                Accepts a :class:`SaveOnHoldDatesModel` instance or a dict.

        Request model: :class:`SaveOnHoldDatesModel`
        """
        return self._request(
            _UPDATE_ON_HOLD_DATES.bind(jobDisplayId=job_display_id, onHoldId=on_hold_id),
            json=data,
        )

    def resolve_on_hold(
        self, job_display_id: int, on_hold_id: str, *, data: ResolveOnHoldRequest | dict,
    ) -> ResolveJobOnHoldResponse:
        """PUT /job/{jobDisplayId}/onhold/{onHoldId}/resolve.

        Args:
            job_display_id: Job display ID.
            on_hold_id: On-hold record identifier.
            data: Resolution payload. Accepts a :class:`ResolveOnHoldRequest`
                instance or a dict.

        Request model: :class:`ResolveOnHoldRequest`
        """
        return self._request(
            _RESOLVE_ON_HOLD.bind(jobDisplayId=job_display_id, onHoldId=on_hold_id),
            json=data,
        )

    # ---- Email ------------------------------------------------------------

    def send_email(self, job_display_id: int, *, data: SendEmailRequest | dict) -> Any:
        """POST /job/{jobDisplayId}/email.

        Args:
            job_display_id: Job display ID.
            data: Email payload. Accepts a :class:`SendEmailRequest`
                instance or a dict.

        Request model: :class:`SendEmailRequest`
        """
        return self._request(_SEND_EMAIL.bind(jobDisplayId=job_display_id), json=data)

    def send_document_email(
        self,
        job_display_id: int,
        *,
        data: SendDocumentEmailModel | dict,
    ) -> Any:
        """POST /job/{jobDisplayId}/email/senddocument.

        Args:
            job_display_id: Job display ID.
            data: Document email payload with to, cc, bcc, subject, body,
                and document_type. Accepts a :class:`SendDocumentEmailModel`
                instance or a dict.

        Request model: :class:`SendDocumentEmailModel`
        """
        return self._request(
            _SEND_DOCUMENT_EMAIL.bind(jobDisplayId=job_display_id), json=data,
        )

    def create_transactional_email(self, job_display_id: int) -> Any:
        """POST /job/{jobDisplayId}/email/createtransactionalemail (ACPortal)"""
        return self._request(_CREATE_TRANSACTIONAL_EMAIL.bind(jobDisplayId=job_display_id))

    def send_template_email(self, job_display_id: int, template_guid: str) -> Any:
        """POST /job/{jobDisplayId}/email/{emailTemplateGuid}/send (ACPortal)"""
        return self._request(
            _SEND_TEMPLATE_EMAIL.bind(jobDisplayId=job_display_id, emailTemplateGuid=template_guid),
        )

    # ---- SMS --------------------------------------------------------------

    def list_sms(self, job_display_id: int) -> Any:
        """GET /job/{jobDisplayId}/sms (ACPortal)"""
        return self._request(_LIST_SMS.bind(jobDisplayId=job_display_id))

    def send_sms(
        self,
        job_display_id: int,
        *,
        data: SendSMSModel | dict,
    ) -> Any:
        """POST /job/{jobDisplayId}/sms.

        Args:
            job_display_id: Job display ID.
            data: SMS payload with phone_number, message, and template_id.
                Accepts a :class:`SendSMSModel` instance or a dict.

        Request model: :class:`SendSMSModel`
        """
        return self._request(_SEND_SMS.bind(jobDisplayId=job_display_id), json=data)

    def mark_sms_read(
        self,
        job_display_id: int,
        *,
        data: MarkSmsAsReadModel | dict,
    ) -> Any:
        """POST /job/{jobDisplayId}/sms/read.

        Args:
            job_display_id: Job display ID.
            data: SMS read payload with sms_ids. Accepts a
                :class:`MarkSmsAsReadModel` instance or a dict.

        Request model: :class:`MarkSmsAsReadModel`
        """
        return self._request(_MARK_SMS_READ.bind(jobDisplayId=job_display_id), json=data)

    def get_sms_template(self, job_display_id: int, template_id: str) -> Any:
        """GET /job/{jobDisplayId}/sms/templatebased/{templateId} (ACPortal)"""
        return self._request(
            _GET_SMS_TEMPLATE.bind(jobDisplayId=job_display_id, templateId=template_id),
        )

    # ---- Freight Providers ------------------------------------------------

    def list_freight_providers(
        self,
        job_display_id: int,
        *,
        provider_indexes: list[int] | None = None,
        shipment_types: list[str] | None = None,
        only_active: bool | None = None,
    ) -> list[PricedFreightProvider]:
        """GET /job/{jobDisplayId}/freightproviders (ACPortal)"""
        return self._request(
            _LIST_FREIGHT_PROVIDERS.bind(jobDisplayId=job_display_id),
            params=dict(
                provider_indexes=provider_indexes,
                shipment_types=shipment_types,
                only_active=only_active,
            ),
        )

    def save_freight_providers(
        self, job_display_id: int, *, data: ShipmentPlanProvider | dict,
    ) -> Any:
        """POST /job/{jobDisplayId}/freightproviders.

        Args:
            job_display_id: Job display ID.
            data: Freight provider selection payload.
                Accepts a :class:`ShipmentPlanProvider` instance or a dict.

        Request model: :class:`ShipmentPlanProvider`
        """
        return self._request(
            _SAVE_FREIGHT_PROVIDERS.bind(jobDisplayId=job_display_id), json=data,
        )

    def get_freight_provider_rate_quote(
        self, job_display_id: int, option_index: int, *, data: RateQuoteRequest | dict,
    ) -> Any:
        """POST /job/{jobDisplayId}/freightproviders/{optionIndex}/ratequote.

        Args:
            job_display_id: Job display ID.
            option_index: Provider option index.
            data: Rate quote request payload. Accepts a
                :class:`RateQuoteRequest` instance or a dict.

        Request model: :class:`RateQuoteRequest`
        """
        return self._request(
            _GET_FREIGHT_PROVIDER_RATE_QUOTE.bind(
                jobDisplayId=job_display_id, optionIndex=option_index,
            ),
            json=data,
        )

    def add_freight_items(self, job_display_id: int, *, data: FreightItemsRequest | dict) -> Any:
        """POST /job/{jobDisplayId}/freightitems.

        Args:
            job_display_id: Job display ID.
            data: Freight items payload. Accepts a :class:`FreightItemsRequest`
                instance or a dict.

        Request model: :class:`FreightItemsRequest`
        """
        return self._request(_ADD_FREIGHT_ITEMS.bind(jobDisplayId=job_display_id), json=data)
