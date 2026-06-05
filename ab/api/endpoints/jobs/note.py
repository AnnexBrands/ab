"""Job-scoped note operations — swagger tag ``JobNote`` (4 routes).

Exposed as ``api.jobs.note`` (renamed from the former ``api.jobs.get_notes``,
``create_note``, ``get_note``, ``update_note`` -- those names remain on
:class:`~ab.api.endpoints.jobs.JobsEndpoint` as deprecation shims).

Subgroup method names drop the ``_note`` suffix:

* :meth:`list` (was ``get_notes``)
* :meth:`get` (was ``get_note``)
* :meth:`create` (was ``create_note``)
* :meth:`update` (was ``update_note``)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab.api.models.jobs import (
        JobNote,
        JobNoteCreateRequest,
        JobNoteUpdateRequest,
    )

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_LIST = Route(
    "GET",
    "/job/{jobDisplayId}/note",
    params_model="JobNoteListParams",
    response_model="List[JobNote]",
)
_CREATE = Route(
    "POST",
    "/job/{jobDisplayId}/note",
    request_model="JobNoteCreateRequest",
    response_model="JobNote",
)
_GET = Route("GET", "/job/{jobDisplayId}/note/{id}", response_model="JobNote")
_UPDATE = Route(
    "PUT",
    "/job/{jobDisplayId}/note/{id}",
    request_model="JobNoteUpdateRequest",
    response_model="JobNote",
)


class JobNoteEndpoint(BaseEndpoint):
    """Job-scoped note operations (ACPortal API).

    Reached via ``api.jobs.note``. Each method takes the job's
    ``job_display_id`` as its first positional argument.
    """

    def list(
        self,
        job_display_id: int,
        *,
        category: str | None = None,
        task_code: str | None = None,
    ) -> list[JobNote]:
        """List notes attached to *job_display_id* (``GET /job/{jobDisplayId}/note``).

        Args:
            job_display_id: Job display ID.
            category: Note category filter.
            task_code: Task code filter.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/note.list.html
        Query params: JobNoteListParams
        Response model: List[JobNote]
        """
        params = dict(category=category, task_code=task_code)
        return self._request(_LIST.bind(jobDisplayId=job_display_id), params=params)

    def get(self, job_display_id: int, note_id: str) -> JobNote:
        """Fetch a single note (``GET /job/{jobDisplayId}/note/{id}``).

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/note.get.html
        Response model: JobNote
        """
        return self._request(_GET.bind(jobDisplayId=job_display_id, id=note_id))

    def create(
        self,
        job_display_id: int,
        *,
        data: JobNoteCreateRequest | dict,
    ) -> JobNote:
        """Create a note (``POST /job/{jobDisplayId}/note``).

        Args:
            job_display_id: Job display ID.
            data: :class:`JobNoteCreateRequest` instance or a dict.

        Request model: :class:`JobNoteCreateRequest`.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/note.create.html
        Request model: JobNoteCreateRequest
        Response model: JobNote
        """
        return self._request(_CREATE.bind(jobDisplayId=job_display_id), json=data)

    def update(
        self,
        job_display_id: int,
        note_id: str,
        *,
        data: JobNoteUpdateRequest | dict,
    ) -> JobNote:
        """Update a note (``PUT /job/{jobDisplayId}/note/{id}``).

        Args:
            job_display_id: Job display ID.
            note_id: Note identifier.
            data: :class:`JobNoteUpdateRequest` instance or a dict.

        Request model: :class:`JobNoteUpdateRequest`.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/note.update.html
        Request model: JobNoteUpdateRequest
        Response model: JobNote
        """
        return self._request(
            _UPDATE.bind(jobDisplayId=job_display_id, id=note_id),
            json=data,
        )
