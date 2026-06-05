"""Job-scoped on-hold operations — swagger tag ``JobOnHold`` (10 routes).

Exposed as ``api.jobs.on_hold``. Old method names on
:class:`~ab.api.endpoints.jobs.JobsEndpoint` (``list_on_hold``,
``create_on_hold``, etc.) remain as deprecation shims.

Method renames (suffix ``_on_hold`` dropped; ``followup`` collapsed):

* :meth:`list`                 (was ``list_on_hold``)
* :meth:`get`                  (was ``get_on_hold``)
* :meth:`create`               (was ``create_on_hold``)
* :meth:`delete`               (was ``delete_on_hold``)
* :meth:`update`               (was ``update_on_hold``)
* :meth:`update_dates`         (was ``update_on_hold_dates``)
* :meth:`resolve`              (was ``resolve_on_hold``)
* :meth:`add_comment`          (was ``add_on_hold_comment``)
* :meth:`get_followup_user`    (was ``get_on_hold_followup_user``)
* :meth:`list_followup_users`  (was ``list_on_hold_followup_users``)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab.api.models.jobs import (
        ExtendedOnHoldInfo,
        OnHoldCommentRequest,
        OnHoldDetails,
        OnHoldNoteDetails,
        OnHoldUser,
        ResolveJobOnHoldResponse,
        SaveOnHoldDatesModel,
        SaveOnHoldRequest,
        SaveOnHoldResponse,
    )

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_LIST = Route("GET", "/job/{jobDisplayId}/onhold", response_model="List[ExtendedOnHoldInfo]")
_CREATE = Route(
    "POST",
    "/job/{jobDisplayId}/onhold",
    request_model="SaveOnHoldRequest",
    response_model="SaveOnHoldResponse",
)
_DELETE = Route("DELETE", "/job/{jobDisplayId}/onhold")
_GET = Route("GET", "/job/{jobDisplayId}/onhold/{id}", response_model="OnHoldDetails")
_UPDATE = Route(
    "PUT",
    "/job/{jobDisplayId}/onhold/{onHoldId}",
    request_model="SaveOnHoldRequest",
    response_model="SaveOnHoldResponse",
)
_GET_FOLLOWUP_USER = Route(
    "GET",
    "/job/{jobDisplayId}/onhold/followupuser/{contactId}",
    response_model="OnHoldUser",
)
_LIST_FOLLOWUP_USERS = Route(
    "GET",
    "/job/{jobDisplayId}/onhold/followupusers",
    response_model="List[OnHoldUser]",
)
_ADD_COMMENT = Route(
    "POST",
    "/job/{jobDisplayId}/onhold/{onHoldId}/comment",
    request_model="OnHoldCommentRequest",
    response_model="OnHoldNoteDetails",
)
_UPDATE_DATES = Route(
    "PUT",
    "/job/{jobDisplayId}/onhold/{onHoldId}/dates",
    request_model="SaveOnHoldDatesModel",
)
_RESOLVE = Route(
    "PUT",
    "/job/{jobDisplayId}/onhold/{onHoldId}/resolve",
    # Swagger uses SaveOnHoldRequest for create/update/resolve; resolve is
    # not a distinct schema. ResolveOnHoldRequest is kept as an alias.
    request_model="SaveOnHoldRequest",
    response_model="ResolveJobOnHoldResponse",
)


class JobOnHoldEndpoint(BaseEndpoint):
    """Job-scoped on-hold operations (ACPortal API)."""

    def list(self, job_display_id: int) -> list[ExtendedOnHoldInfo]:
        """List on-hold records for *job_display_id*.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/on_hold.list.html
        Response model: List[ExtendedOnHoldInfo]
        """
        return self._request(_LIST.bind(jobDisplayId=job_display_id))

    def get(self, job_display_id: int, on_hold_id: str) -> OnHoldDetails:
        """Fetch one on-hold record.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/on_hold.get.html
        Response model: OnHoldDetails
        """
        return self._request(_GET.bind(jobDisplayId=job_display_id, id=on_hold_id))

    def create(
        self,
        job_display_id: int,
        *,
        data: SaveOnHoldRequest | dict,
    ) -> SaveOnHoldResponse:
        """Place a job on hold.

        Request model: :class:`SaveOnHoldRequest`.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/on_hold.create.html
        Request model: SaveOnHoldRequest
        Response model: SaveOnHoldResponse
        """
        return self._request(_CREATE.bind(jobDisplayId=job_display_id), json=data)

    def delete(self, job_display_id: int) -> None:
        """Remove the active on-hold record for *job_display_id*.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/on_hold.delete.html
        """
        return self._request(_DELETE.bind(jobDisplayId=job_display_id))

    def update(
        self,
        job_display_id: int,
        on_hold_id: str,
        *,
        data: SaveOnHoldRequest | dict,
    ) -> SaveOnHoldResponse:
        """Update an existing on-hold record.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/on_hold.update.html
        Request model: SaveOnHoldRequest
        Response model: SaveOnHoldResponse
        """
        return self._request(
            _UPDATE.bind(jobDisplayId=job_display_id, onHoldId=on_hold_id),
            json=data,
        )

    def get_followup_user(self, job_display_id: int, contact_id: str) -> OnHoldUser:
        """Resolve one follow-up user by contact ID.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/on_hold.get_followup_user.html
        Response model: OnHoldUser
        """
        return self._request(
            _GET_FOLLOWUP_USER.bind(jobDisplayId=job_display_id, contactId=contact_id),
        )

    def list_followup_users(self, job_display_id: int) -> list[OnHoldUser]:
        """List all follow-up users available for the job.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/on_hold.list_followup_users.html
        Response model: List[OnHoldUser]
        """
        return self._request(_LIST_FOLLOWUP_USERS.bind(jobDisplayId=job_display_id))

    def add_comment(
        self,
        job_display_id: int,
        on_hold_id: str,
        *,
        data: OnHoldCommentRequest | dict,
    ) -> OnHoldNoteDetails:
        """Append a comment to an on-hold record.

        Request model: :class:`OnHoldCommentRequest`.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/on_hold.add_comment.html
        Request model: OnHoldCommentRequest
        Response model: OnHoldNoteDetails
        """
        return self._request(
            _ADD_COMMENT.bind(jobDisplayId=job_display_id, onHoldId=on_hold_id),
            json=data,
        )

    def update_dates(
        self,
        job_display_id: int,
        on_hold_id: str,
        *,
        data: SaveOnHoldDatesModel | dict,
    ) -> None:
        """Update follow-up / due dates on an on-hold record.

        Request model: :class:`SaveOnHoldDatesModel`.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/on_hold.update_dates.html
        Request model: SaveOnHoldDatesModel
        """
        return self._request(
            _UPDATE_DATES.bind(jobDisplayId=job_display_id, onHoldId=on_hold_id),
            json=data,
        )

    def resolve(
        self,
        job_display_id: int,
        on_hold_id: str,
        *,
        data: SaveOnHoldRequest | dict,
    ) -> ResolveJobOnHoldResponse:
        """Resolve an on-hold record.

        Request model: :class:`SaveOnHoldRequest` (resolve shares the
        same swagger schema as create/update; populate ``resolved_code_id``
        and/or ``resolved_date`` to record the outcome).

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/on_hold.resolve.html
        Request model: SaveOnHoldRequest
        Response model: ResolveJobOnHoldResponse
        """
        return self._request(
            _RESOLVE.bind(jobDisplayId=job_display_id, onHoldId=on_hold_id),
            json=data,
        )
