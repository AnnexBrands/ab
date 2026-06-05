"""Jobs API endpoints — ACPortal (55 routes) + ABC (1 route).

This file handles two API surfaces. ACPortal routes use the default
``api_surface="acportal"``; the ABC job update route explicitly sets
``api_surface="abc"``.
"""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

from ab.api.base import BaseEndpoint
from ab.api.endpoints.jobs.email import JobEmailEndpoint
from ab.api.endpoints.jobs.form import JobFormEndpoint
from ab.api.endpoints.jobs.freight_providers import JobFreightProvidersEndpoint
from ab.api.endpoints.jobs.note import JobNoteEndpoint
from ab.api.endpoints.jobs.on_hold import JobOnHoldEndpoint
from ab.api.endpoints.jobs.parcel_items import JobParcelItemsEndpoint
from ab.api.endpoints.jobs.payment import JobPaymentEndpoint
from ab.api.endpoints.jobs.rfq import JobRfqEndpoint
from ab.api.endpoints.jobs.shipment import JobShipmentEndpoint
from ab.api.endpoints.jobs.sms import JobSmsEndpoint
from ab.api.endpoints.jobs.status import JobStatusEndpoint
from ab.api.endpoints.jobs.timeline import JobTimelineEndpoint
from ab.api.endpoints.jobs.tracking import JobTrackingEndpoint
from ab.api.route import Route
from ab.cache import CodeResolver
from ab.http import HttpClient


def _deprecated(old: str, new: str) -> None:
    """Emit a DeprecationWarning telling the caller to switch to *new*."""
    warnings.warn(
        f"{old}() is deprecated; use {new}() instead.",
        DeprecationWarning,
        stacklevel=3,
    )

if TYPE_CHECKING:
    from ab.api.helpers.agent import AgentHelpers
    from ab.api.helpers.timeline import TimelineHelpers
    from ab.api.models.jobs import (
        BaseTimelineTaskRequest,
        CalendarItem,
        ChangeJobAgentRequest,
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
        TimelineAgent,
        TimelineResponse,
        TimelineSaveResponse,
        TimelineTask,
        TimelineTaskUpdateRequest,
        TrackingInfo,
        TrackingInfoV3,
    )
    from ab.api.models.rfq import QuoteRequestDisplayInfo
    from ab.api.models.shared import ServiceBaseResponse

# ACPortal routes
_CREATE = Route("POST", "/job", request_model="JobCreateRequest")
_SAVE = Route("PUT", "/job/save", request_model="JobSaveRequest")
_GET = Route("GET", "/job/{jobDisplayId}", response_model="Job")
_SEARCH = Route("GET", "/job/search", params_model="JobSearchParams", response_model="JobSearchResult")
_SEARCH_BY_DETAILS = Route(
    "POST",
    "/job/searchByDetails",
    request_model="JobSearchRequest",
    response_model="List[JobSearchResult]",
)
_GET_PRICE = Route("GET", "/job/{jobDisplayId}/price", response_model="JobPrice")
_GET_CALENDAR = Route("GET", "/job/{jobDisplayId}/calendaritems", response_model="List[CalendarItem]")
_GET_CONFIG = Route("GET", "/job/{jobDisplayId}/updatePageConfig", response_model="JobUpdatePageConfig")

# Transfer route
_TRANSFER = Route("POST", "/job/transfer/{jobDisplayId}", request_model="TransferModel")

# ABC route (different API surface)
_ABC_UPDATE = Route("POST", "/job/update", request_model="JobUpdateRequest", api_surface="abc")

# Timeline routes -> ab.api.endpoints.jobs.timeline   (api.jobs.timeline)
# Status routes   -> ab.api.endpoints.jobs.status     (api.jobs.status)
# Tracking routes -> ab.api.endpoints.jobs.tracking   (api.jobs.tracking)

# Note routes -> moved to ab.api.endpoints.jobs.note (exposed as api.jobs.note)

# JobParcelItems routes -> ab.api.endpoints.jobs.parcel_items (api.jobs.parcel_items)
# /packagingcontainers stays here (tagged Job in swagger, not JobParcelItems).
_GET_PACKAGING_CONTAINERS = Route(
    "GET",
    "/job/{jobDisplayId}/packagingcontainers",
    response_model="List[PackagingContainer]",
)
_PUT_ITEM = Route(
    "PUT",
    "/job/{jobDisplayId}/item/{itemId}",
    request_model="ItemUpdateRequest",
    response_model="ServiceBaseResponse",
)
_POST_ITEM_NOTES = Route(
    "POST",
    "/job/{jobDisplayId}/item/notes",
    request_model="ItemNotesRequest",
    response_model="ServiceBaseResponse",
)


# JobRfq routes -> ab.api.endpoints.jobs.rfq (api.jobs.rfq)

# On-Hold routes -> moved to ab.api.endpoints.jobs.on_hold (exposed as api.jobs.on_hold)

# Email routes  -> ab.api.endpoints.jobs.email             (api.jobs.email)
# SMS routes    -> ab.api.endpoints.jobs.sms               (api.jobs.sms)
# JobFreightProviders routes -> ab.api.endpoints.jobs.freight_providers
#                                                          (api.jobs.freight_providers)
# /freightitems (tag=Job, not JobFreightProviders) stays here.
_ADD_FREIGHT_ITEMS = Route(
    "POST",
    "/job/{jobDisplayId}/freightitems",
    request_model="FreightItemsRequest",
)

# Agent change route (029)
_POST_CHANGE_AGENT = Route(
    "POST",
    "/job/{jobDisplayId}/changeAgent",
    request_model="ChangeJobAgentRequest",
    response_model="ServiceBaseResponse",
)


class JobsEndpoint(BaseEndpoint):
    """Operations on jobs (ACPortal + ABC APIs).

    Subgroups (each is a :class:`~ab.api.base.BaseEndpoint` instance
    organised by swagger tag):

    * :attr:`note`     — ``JobNote``   (``api.jobs.note``)
    * :attr:`on_hold`  — ``JobOnHold`` (``api.jobs.on_hold``)
    * :attr:`form`     — ``JobForm``   (``api.jobs.form``)

    The legacy flat method names (``get_notes``, ``list_on_hold`` …) remain
    on this class as deprecation shims and forward to the subgroups.
    """

    # Class-level type annotations make CLI discovery introspectable
    # without instantiating the client.
    note: JobNoteEndpoint
    on_hold: JobOnHoldEndpoint
    form: JobFormEndpoint
    timeline: JobTimelineEndpoint
    email: JobEmailEndpoint
    sms: JobSmsEndpoint
    freight_providers: JobFreightProvidersEndpoint
    parcel_items: JobParcelItemsEndpoint
    tracking: JobTrackingEndpoint
    status: JobStatusEndpoint
    payment: JobPaymentEndpoint
    shipment: JobShipmentEndpoint
    rfq: JobRfqEndpoint

    def __init__(self, acportal_client: HttpClient, abc_client: HttpClient, resolver: CodeResolver) -> None:
        super().__init__(acportal_client)
        self._abc_client = abc_client
        self._resolver = resolver

        from ab.api.helpers.agent import AgentHelpers as _AgentHelpers
        from ab.api.helpers.timeline import TimelineHelpers as _TimelineHelpers

        self.agent: AgentHelpers = _AgentHelpers(self, self._resolver)
        self.tasks: TimelineHelpers = _TimelineHelpers(self)

        # Subgroups (instances share the parent's HttpClient).
        self.note = JobNoteEndpoint(acportal_client)
        self.on_hold = JobOnHoldEndpoint(acportal_client)
        self.form = JobFormEndpoint(acportal_client)
        self.timeline = JobTimelineEndpoint(acportal_client)
        self.email = JobEmailEndpoint(acportal_client)
        self.sms = JobSmsEndpoint(acportal_client)
        self.freight_providers = JobFreightProvidersEndpoint(acportal_client)
        self.parcel_items = JobParcelItemsEndpoint(acportal_client)
        self.tracking = JobTrackingEndpoint(acportal_client)
        self.status = JobStatusEndpoint(acportal_client)
        self.payment = JobPaymentEndpoint(acportal_client)
        self.shipment = JobShipmentEndpoint(acportal_client)
        self.rfq = JobRfqEndpoint(acportal_client)

    def create(self, *, data: JobCreateRequest | dict) -> None:
        """POST /job.

        Args:
            data: Job creation payload with customer, pickup, delivery,
                items, and services. Accepts a :class:`JobCreateRequest`
                instance or a dict.

        Request model: :class:`JobCreateRequest`

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/create.html
        Request model: JobCreateRequest
        """
        return self._request(_CREATE, json=data)

    def save(self, *, data: JobSaveRequest | dict) -> None:
        """PUT /job/save.

        Args:
            data: Job save payload with jobDisplayId, customer, pickup,
                delivery, and items. Accepts a :class:`JobSaveRequest`
                instance or a dict.

        Request model: :class:`JobSaveRequest`

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/save.html
        Request model: JobSaveRequest
        """
        return self._request(_SAVE, json=data)

    def get(self, job_display_id: int) -> Job:
        """GET /job/{jobDisplayId} (ACPortal)

        Retrieve a job by its display ID.

        Args:
            job_display_id: The numeric display ID of the job.

        Returns:
            :class:`~ab.api.models.jobs.Job`

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/get.html
        Response model: Job
        """
        return self._request(_GET.bind(jobDisplayId=job_display_id))

    def search(self, *, job_display_id: int | None = None) -> JobSearchResult:
        """GET /job/search (ACPortal) — query params.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/search.html
        Query params: JobSearchParams
        Response model: JobSearchResult
        """
        return self._request(_SEARCH, params=dict(job_display_id=job_display_id))

    def search_by_details(self, *, data: JobSearchRequest | dict) -> list[JobSearchResult]:
        """POST /job/searchByDetails.

        Args:
            data: Search filter with search_text, page, page_size, and
                sort_by. Accepts a :class:`JobSearchRequest` instance
                or a dict.

        Request model: :class:`JobSearchRequest`

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/search_by_details.html
        Request model: JobSearchRequest
        Response model: List[JobSearchResult]
        """
        return self._request(_SEARCH_BY_DETAILS, json=data)

    def get_price(self, job_display_id: int) -> JobPrice:
        """GET /job/{jobDisplayId}/price (ACPortal)

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/get_price.html
        Response model: JobPrice
        """
        return self._request(_GET_PRICE.bind(jobDisplayId=job_display_id))

    def get_calendar_items(self, job_display_id: int) -> list[CalendarItem]:
        """GET /job/{jobDisplayId}/calendaritems (ACPortal)

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/get_calendar_items.html
        Response model: List[CalendarItem]
        """
        return self._request(_GET_CALENDAR.bind(jobDisplayId=job_display_id))

    def get_update_page_config(self, job_display_id: int) -> JobUpdatePageConfig:
        """GET /job/{jobDisplayId}/updatePageConfig (ACPortal)

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/get_update_page_config.html
        Response model: JobUpdatePageConfig
        """
        return self._request(_GET_CONFIG.bind(jobDisplayId=job_display_id))

    def update(self, *, data: JobUpdateRequest | dict) -> None:
        """POST /job/update (ABC API surface).

        Args:
            data: Job update payload with job_id and updates.
                Accepts a :class:`JobUpdateRequest` instance or a dict.

        Request model: :class:`JobUpdateRequest`

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/update.html
        Request model: JobUpdateRequest
        """
        return self._request(_ABC_UPDATE, client=self._abc_client, json=data)

    def transfer(self, job_display_id: int, franchisee_id: str) -> None:
        """POST /job/transfer/{jobDisplayId} (ACPortal)

        Args:
            job_display_id: Job to transfer.
            franchisee_id: Target franchisee — accepts a company code
                (e.g. ``"9999AZ"``) or UUID.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/transfer.html
        Request model: TransferModel
        """
        resolved = self._resolver.resolve(franchisee_id)
        return self._request(
            _TRANSFER.bind(jobDisplayId=job_display_id),
            json={"franchiseeId": resolved},
        )

    # ---- Timeline (deprecated shims; canonical home is api.jobs.timeline) -

    def get_timeline_response(self, job_display_id: int) -> TimelineResponse:
        """Deprecated. Use ``api.jobs.timeline.response(...)``."""
        _deprecated("api.jobs.get_timeline_response", "api.jobs.timeline.response")
        return self.timeline.response(job_display_id)

    def get_timeline(self, job_display_id: int) -> list[TimelineTask]:
        """Deprecated. Use ``api.jobs.timeline.list(...)``."""
        _deprecated("api.jobs.get_timeline", "api.jobs.timeline.list")
        return self.timeline.list(job_display_id)

    def create_timeline_task(
        self,
        job_display_id: int,
        *,
        data: BaseTimelineTaskRequest | dict,
        create_email: bool | None = None,
    ) -> TimelineSaveResponse:
        """Deprecated. Use ``api.jobs.timeline.create_task(...)``."""
        _deprecated("api.jobs.create_timeline_task", "api.jobs.timeline.create_task")
        return self.timeline.create_task(job_display_id, data=data, create_email=create_email)

    def get_timeline_task(self, job_display_id: int, task_id: str) -> TimelineTask:
        """Deprecated. Use ``api.jobs.timeline.get_task(...)``."""
        _deprecated("api.jobs.get_timeline_task", "api.jobs.timeline.get_task")
        return self.timeline.get_task(job_display_id, task_id)

    def update_timeline_task(
        self,
        job_display_id: int,
        task_id: str,
        *,
        data: TimelineTaskUpdateRequest | dict,
    ) -> TimelineTask:
        """Deprecated. Use ``api.jobs.timeline.update_task(...)``."""
        _deprecated("api.jobs.update_timeline_task", "api.jobs.timeline.update_task")
        return self.timeline.update_task(job_display_id, task_id, data=data)

    def delete_timeline_task(self, job_display_id: int, task_id: str) -> ServiceBaseResponse:
        """Deprecated. Use ``api.jobs.timeline.delete_task(...)``."""
        _deprecated("api.jobs.delete_timeline_task", "api.jobs.timeline.delete_task")
        return self.timeline.delete_task(job_display_id, task_id)

    def get_timeline_agent(self, job_display_id: int, task_code: str) -> TimelineAgent | None:
        """Deprecated. Use ``api.jobs.timeline.get_agent(...)``."""
        _deprecated("api.jobs.get_timeline_agent", "api.jobs.timeline.get_agent")
        return self.timeline.get_agent(job_display_id, task_code)

    def increment_status(
        self,
        job_display_id: int,
        *,
        data: IncrementStatusRequest | dict,
    ) -> ServiceBaseResponse:
        """Deprecated. Use ``api.jobs.timeline.increment_status(...)``."""
        _deprecated("api.jobs.increment_status", "api.jobs.timeline.increment_status")
        return self.timeline.increment_status(job_display_id, data=data)

    def undo_increment_status(
        self,
        job_display_id: int,
        *,
        data: IncrementStatusRequest | dict,
    ) -> ServiceBaseResponse:
        """Deprecated. Use ``api.jobs.timeline.undo_increment_status(...)``."""
        _deprecated("api.jobs.undo_increment_status", "api.jobs.timeline.undo_increment_status")
        return self.timeline.undo_increment_status(job_display_id, data=data)

    # ---- Status (deprecated shim; canonical home is api.jobs.status) ------

    def set_quote_status(self, job_display_id: int) -> ServiceBaseResponse:
        """Deprecated. Use ``api.jobs.status.set_quote(...)``."""
        _deprecated("api.jobs.set_quote_status", "api.jobs.status.set_quote")
        return self.status.set_quote(job_display_id)

    # ---- Tracking (deprecated shims; canonical home is api.jobs.tracking) -

    def get_tracking(self, job_display_id: int) -> TrackingInfo:
        """Deprecated. Use ``api.jobs.tracking.get(...)``."""
        _deprecated("api.jobs.get_tracking", "api.jobs.tracking.get")
        return self.tracking.get(job_display_id)

    def get_tracking_v3(self, job_display_id: int, history_amount: int = 10) -> TrackingInfoV3:
        """Deprecated. Use ``api.jobs.tracking.v3(...)``."""
        _deprecated("api.jobs.get_tracking_v3", "api.jobs.tracking.v3")
        return self.tracking.v3(job_display_id, history_amount)

    # ---- Notes (deprecated shims; canonical home is api.jobs.note) -------

    def get_notes(
        self,
        job_display_id: int,
        *,
        category: str | None = None,
        task_code: str | None = None,
    ) -> list[JobNote]:
        """Deprecated. Use ``api.jobs.note.list(...)``."""
        _deprecated("api.jobs.get_notes", "api.jobs.note.list")
        return self.note.list(job_display_id, category=category, task_code=task_code)

    def create_note(
        self,
        job_display_id: int,
        *,
        data: JobNoteCreateRequest | dict,
    ) -> JobNote:
        """Deprecated. Use ``api.jobs.note.create(...)``."""
        _deprecated("api.jobs.create_note", "api.jobs.note.create")
        return self.note.create(job_display_id, data=data)

    def get_note(self, job_display_id: int, note_id: str) -> JobNote:
        """Deprecated. Use ``api.jobs.note.get(...)``."""
        _deprecated("api.jobs.get_note", "api.jobs.note.get")
        return self.note.get(job_display_id, note_id)

    def update_note(
        self,
        job_display_id: int,
        note_id: str,
        *,
        data: JobNoteUpdateRequest | dict,
    ) -> JobNote:
        """Deprecated. Use ``api.jobs.note.update(...)``."""
        _deprecated("api.jobs.update_note", "api.jobs.note.update")
        return self.note.update(job_display_id, note_id, data=data)

    # ---- Parcel Items (deprecated shims; canonical home is api.jobs.parcel_items) ----

    def get_parcel_items(self, job_display_id: int) -> list[ParcelItem]:
        """Deprecated. Use ``api.jobs.parcel_items.list(...)``."""
        _deprecated("api.jobs.get_parcel_items", "api.jobs.parcel_items.list")
        return self.parcel_items.list(job_display_id)

    def create_parcel_item(
        self,
        job_display_id: int,
        *,
        data: ParcelItemCreateRequest | dict,
    ) -> ParcelItem:
        """Deprecated. Use ``api.jobs.parcel_items.create(...)``."""
        _deprecated("api.jobs.create_parcel_item", "api.jobs.parcel_items.create")
        return self.parcel_items.create(job_display_id, data=data)

    def delete_parcel_item(self, job_display_id: int, parcel_item_id: str) -> ServiceBaseResponse:
        """Deprecated. Use ``api.jobs.parcel_items.delete(...)``."""
        _deprecated("api.jobs.delete_parcel_item", "api.jobs.parcel_items.delete")
        return self.parcel_items.delete(job_display_id, parcel_item_id)

    def get_parcel_items_with_materials(self, job_display_id: int) -> list[ParcelItemWithMaterials]:
        """Deprecated. Use ``api.jobs.parcel_items.list_with_materials(...)``."""
        _deprecated("api.jobs.get_parcel_items_with_materials", "api.jobs.parcel_items.list_with_materials")
        return self.parcel_items.list_with_materials(job_display_id)

    # ---- /packagingcontainers (tag=Job, kept here) -----------------------

    def get_packaging_containers(self, job_display_id: int) -> list[PackagingContainer]:
        """GET /job/{jobDisplayId}/packagingcontainers (ACPortal)

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/get_packaging_containers.html
        Response model: List[PackagingContainer]
        """
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

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/update_item.html
        Request model: ItemUpdateRequest
        Response model: ServiceBaseResponse
        """
        return self._request(
            _PUT_ITEM.bind(jobDisplayId=job_display_id, itemId=item_id),
            json=data,
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

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/add_item_notes.html
        Request model: ItemNotesRequest
        Response model: ServiceBaseResponse
        """
        return self._request(_POST_ITEM_NOTES.bind(jobDisplayId=job_display_id), json=data)

    # ---- RFQ (deprecated shims; canonical home is api.jobs.rfq) ----------

    def list_rfqs(self, job_display_id: int) -> list[QuoteRequestDisplayInfo]:
        """Deprecated. Use ``api.jobs.rfq.list(...)``."""
        _deprecated("api.jobs.list_rfqs", "api.jobs.rfq.list")
        return self.rfq.list(job_display_id)

    def get_rfq_status(self, job_display_id: int, rfq_service_type: str, company_id: str) -> int:
        """Deprecated. Use ``api.jobs.rfq.status(...)``."""
        _deprecated("api.jobs.get_rfq_status", "api.jobs.rfq.status")
        return self.rfq.status(job_display_id, rfq_service_type, company_id)

    # ---- On-Hold (deprecated shims; canonical home is api.jobs.on_hold) -

    def list_on_hold(self, job_display_id: int) -> list[ExtendedOnHoldInfo]:
        """Deprecated. Use ``api.jobs.on_hold.list(...)``."""
        _deprecated("api.jobs.list_on_hold", "api.jobs.on_hold.list")
        return self.on_hold.list(job_display_id)

    def create_on_hold(
        self,
        job_display_id: int,
        *,
        data: SaveOnHoldRequest | dict,
    ) -> SaveOnHoldResponse:
        """Deprecated. Use ``api.jobs.on_hold.create(...)``."""
        _deprecated("api.jobs.create_on_hold", "api.jobs.on_hold.create")
        return self.on_hold.create(job_display_id, data=data)

    def delete_on_hold(self, job_display_id: int) -> None:
        """Deprecated. Use ``api.jobs.on_hold.delete(...)``."""
        _deprecated("api.jobs.delete_on_hold", "api.jobs.on_hold.delete")
        return self.on_hold.delete(job_display_id)

    def get_on_hold(self, job_display_id: int, on_hold_id: str) -> OnHoldDetails:
        """Deprecated. Use ``api.jobs.on_hold.get(...)``."""
        _deprecated("api.jobs.get_on_hold", "api.jobs.on_hold.get")
        return self.on_hold.get(job_display_id, on_hold_id)

    def update_on_hold(
        self,
        job_display_id: int,
        on_hold_id: str,
        *,
        data: SaveOnHoldRequest | dict,
    ) -> SaveOnHoldResponse:
        """Deprecated. Use ``api.jobs.on_hold.update(...)``."""
        _deprecated("api.jobs.update_on_hold", "api.jobs.on_hold.update")
        return self.on_hold.update(job_display_id, on_hold_id, data=data)

    def get_on_hold_followup_user(self, job_display_id: int, contact_id: str) -> OnHoldUser:
        """Deprecated. Use ``api.jobs.on_hold.get_followup_user(...)``."""
        _deprecated("api.jobs.get_on_hold_followup_user", "api.jobs.on_hold.get_followup_user")
        return self.on_hold.get_followup_user(job_display_id, contact_id)

    def list_on_hold_followup_users(self, job_display_id: int) -> list[OnHoldUser]:
        """Deprecated. Use ``api.jobs.on_hold.list_followup_users(...)``."""
        _deprecated("api.jobs.list_on_hold_followup_users", "api.jobs.on_hold.list_followup_users")
        return self.on_hold.list_followup_users(job_display_id)

    def add_on_hold_comment(
        self,
        job_display_id: int,
        on_hold_id: str,
        *,
        data: OnHoldCommentRequest | dict,
    ) -> OnHoldNoteDetails:
        """Deprecated. Use ``api.jobs.on_hold.add_comment(...)``."""
        _deprecated("api.jobs.add_on_hold_comment", "api.jobs.on_hold.add_comment")
        return self.on_hold.add_comment(job_display_id, on_hold_id, data=data)

    def update_on_hold_dates(
        self,
        job_display_id: int,
        on_hold_id: str,
        *,
        data: SaveOnHoldDatesModel | dict,
    ) -> None:
        """Deprecated. Use ``api.jobs.on_hold.update_dates(...)``."""
        _deprecated("api.jobs.update_on_hold_dates", "api.jobs.on_hold.update_dates")
        return self.on_hold.update_dates(job_display_id, on_hold_id, data=data)

    def resolve_on_hold(
        self,
        job_display_id: int,
        on_hold_id: str,
        *,
        data: ResolveOnHoldRequest | dict,
    ) -> ResolveJobOnHoldResponse:
        """Deprecated. Use ``api.jobs.on_hold.resolve(...)``."""
        _deprecated("api.jobs.resolve_on_hold", "api.jobs.on_hold.resolve")
        return self.on_hold.resolve(job_display_id, on_hold_id, data=data)

    # ---- Email ------------------------------------------------------------

    # ---- Email (deprecated shims; canonical home is api.jobs.email) -------

    def send_email(self, job_display_id: int, *, data: SendEmailRequest | dict) -> None:
        """Deprecated. Use ``api.jobs.email.send(...)``."""
        _deprecated("api.jobs.send_email", "api.jobs.email.send")
        return self.email.send(job_display_id, data=data)

    def send_document_email(
        self,
        job_display_id: int,
        *,
        data: SendDocumentEmailModel | dict,
    ) -> None:
        """Deprecated. Use ``api.jobs.email.send_document(...)``."""
        _deprecated("api.jobs.send_document_email", "api.jobs.email.send_document")
        return self.email.send_document(job_display_id, data=data)

    def create_transactional_email(self, job_display_id: int) -> None:
        """Deprecated. Use ``api.jobs.email.create_transactional(...)``."""
        _deprecated("api.jobs.create_transactional_email", "api.jobs.email.create_transactional")
        return self.email.create_transactional(job_display_id)

    def send_template_email(self, job_display_id: int, template_guid: str) -> None:
        """Deprecated. Use ``api.jobs.email.send_template(...)``."""
        _deprecated("api.jobs.send_template_email", "api.jobs.email.send_template")
        return self.email.send_template(job_display_id, template_guid)

    # ---- SMS (deprecated shims; canonical home is api.jobs.sms) -----------

    def list_sms(self, job_display_id: int) -> None:
        """Deprecated. Use ``api.jobs.sms.list(...)``."""
        _deprecated("api.jobs.list_sms", "api.jobs.sms.list")
        return self.sms.list(job_display_id)

    def send_sms(self, job_display_id: int, *, data: SendSMSModel | dict) -> None:
        """Deprecated. Use ``api.jobs.sms.send(...)``."""
        _deprecated("api.jobs.send_sms", "api.jobs.sms.send")
        return self.sms.send(job_display_id, data=data)

    def mark_sms_read(self, job_display_id: int, *, data: MarkSmsAsReadModel | dict) -> None:
        """Deprecated. Use ``api.jobs.sms.mark_read(...)``."""
        _deprecated("api.jobs.mark_sms_read", "api.jobs.sms.mark_read")
        return self.sms.mark_read(job_display_id, data=data)

    def get_sms_template(self, job_display_id: int, template_id: str) -> None:
        """Deprecated. Use ``api.jobs.sms.get_template(...)``."""
        _deprecated("api.jobs.get_sms_template", "api.jobs.sms.get_template")
        return self.sms.get_template(job_display_id, template_id)

    # ---- Freight Providers (deprecated shims; canonical home is api.jobs.freight_providers) ----

    def list_freight_providers(
        self,
        job_display_id: int,
        *,
        provider_indexes: list[int] | None = None,
        shipment_types: list[str] | None = None,
        only_active: bool | None = None,
    ) -> list[PricedFreightProvider]:
        """Deprecated. Use ``api.jobs.freight_providers.list(...)``."""
        _deprecated("api.jobs.list_freight_providers", "api.jobs.freight_providers.list")
        return self.freight_providers.list(
            job_display_id,
            provider_indexes=provider_indexes,
            shipment_types=shipment_types,
            only_active=only_active,
        )

    def save_freight_providers(
        self,
        job_display_id: int,
        *,
        data: ShipmentPlanProvider | dict,
    ) -> None:
        """Deprecated. Use ``api.jobs.freight_providers.save(...)``."""
        _deprecated("api.jobs.save_freight_providers", "api.jobs.freight_providers.save")
        return self.freight_providers.save(job_display_id, data=data)

    def get_freight_provider_rate_quote(
        self,
        job_display_id: int,
        option_index: int,
        *,
        data: RateQuoteRequest | dict,
    ) -> None:
        """Deprecated. Use ``api.jobs.freight_providers.rate_quote(...)``."""
        _deprecated("api.jobs.get_freight_provider_rate_quote", "api.jobs.freight_providers.rate_quote")
        return self.freight_providers.rate_quote(job_display_id, option_index, data=data)

    # ---- /freightitems (tag=Job, kept here) ------------------------------

    def add_freight_items(self, job_display_id: int, *, data: FreightItemsRequest | dict) -> None:
        """POST /job/{jobDisplayId}/freightitems.

        Args:
            job_display_id: Job display ID.
            data: Freight items payload. Accepts a :class:`FreightItemsRequest`
                instance or a dict.

        Request model: :class:`FreightItemsRequest`

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/add_freight_items.html
        Request model: FreightItemsRequest
        """
        return self._request(_ADD_FREIGHT_ITEMS.bind(jobDisplayId=job_display_id), json=data)

    # ---- Agent change (029) -----------------------------------------------

    def change_agent(
        self,
        job_display_id: int,
        *,
        data: ChangeJobAgentRequest | dict,
    ) -> ServiceBaseResponse:
        """POST /job/{jobDisplayId}/changeAgent.

        Args:
            job_display_id: Job display ID.
            data: Agent change payload with service type, agent ID, and
                optional price/rebate flags. Accepts a
                :class:`ChangeJobAgentRequest` instance or a dict.

        Returns:
            :class:`~ab.api.models.shared.ServiceBaseResponse`

        Request model: :class:`ChangeJobAgentRequest`

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/change_agent.html
        Request model: ChangeJobAgentRequest
        Response model: ServiceBaseResponse
        """
        return self._request(
            _POST_CHANGE_AGENT.bind(jobDisplayId=job_display_id),
            json=data,
        )
