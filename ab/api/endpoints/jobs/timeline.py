"""Job-scoped timeline operations — swagger tag ``JobTimeline`` (8 routes).

Exposed as ``api.jobs.timeline``. Old names on
:class:`~ab.api.endpoints.jobs.JobsEndpoint` (``get_timeline_response``,
``create_timeline_task`` …) remain as deprecation shims.

Method renames:

* :meth:`response`              (was ``get_timeline_response``)
* :meth:`list`                  (was ``get_timeline``)
* :meth:`get_task`              (was ``get_timeline_task``)
* :meth:`create_task`           (was ``create_timeline_task``)
* :meth:`update_task`           (was ``update_timeline_task``)
* :meth:`delete_task`           (was ``delete_timeline_task``)
* :meth:`get_agent`             (was ``get_timeline_agent``)
* :meth:`increment_status`      (unchanged)
* :meth:`undo_increment_status` (unchanged)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab.api.models.jobs import (
        BaseTimelineTaskRequest,
        IncrementStatusRequest,
        TimelineAgent,
        TimelineResponse,
        TimelineSaveResponse,
        TimelineTask,
        TimelineTaskUpdateRequest,
    )
    from ab.api.models.shared import ServiceBaseResponse

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_TIMELINE = Route("GET", "/job/{jobDisplayId}/timeline", response_model="TimelineResponse")
_POST_TIMELINE = Route(
    "POST",
    "/job/{jobDisplayId}/timeline",
    params_model="TimelineCreateParams",
    response_model="TimelineSaveResponse",
)
_GET_TASK = Route(
    "GET",
    "/job/{jobDisplayId}/timeline/{timelineTaskIdentifier}",
    response_model="TimelineTask",
)
_PATCH_TASK = Route(
    "PATCH",
    "/job/{jobDisplayId}/timeline/{timelineTaskId}",
    request_model="TimelineTaskUpdateRequest",
    response_model="TimelineTask",
)
_DELETE_TASK = Route(
    "DELETE",
    "/job/{jobDisplayId}/timeline/{timelineTaskId}",
    response_model="ServiceBaseResponse",
)
_GET_AGENT = Route(
    "GET",
    "/job/{jobDisplayId}/timeline/{taskCode}/agent",
    response_model="TimelineAgent",
)
_INCREMENT_STATUS = Route(
    "POST",
    "/job/{jobDisplayId}/timeline/incrementjobstatus",
    request_model="IncrementStatusRequest",
    response_model="ServiceBaseResponse",
)
_UNDO_INCREMENT_STATUS = Route(
    "POST",
    "/job/{jobDisplayId}/timeline/undoincrementjobstatus",
    request_model="IncrementStatusRequest",
    response_model="ServiceBaseResponse",
)


class JobTimelineEndpoint(BaseEndpoint):
    """Job-scoped timeline operations (ACPortal API)."""

    def response(self, job_display_id: int) -> TimelineResponse:
        """``GET /job/{jobDisplayId}/timeline`` — full wrapper response.

        Returns :class:`~ab.api.models.jobs.TimelineResponse` with tasks,
        status metadata, SLA info, and on-hold entries.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/timeline.response.html
        Response model: TimelineResponse
        """
        return self._request(_TIMELINE.bind(jobDisplayId=job_display_id))

    def list(self, job_display_id: int) -> list[TimelineTask]:
        """``GET /job/{jobDisplayId}/timeline`` — convenience returning just tasks."""
        resp = self.response(job_display_id)
        return resp.tasks or []

    def create_task(
        self,
        job_display_id: int,
        *,
        data: BaseTimelineTaskRequest | dict,
        create_email: bool | None = None,
    ) -> TimelineSaveResponse:
        """``POST /job/{jobDisplayId}/timeline`` — create or update a task.

        Args:
            job_display_id: Job display ID.
            data: Task request model instance or dict with ``taskCode`` and
                task-code-specific fields.
            create_email: Send status notification email (query param).

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/timeline.create_task.html
        Query params: TimelineCreateParams
        Response model: TimelineSaveResponse
        """
        params = dict(create_email=create_email)
        return self._request(
            _POST_TIMELINE.bind(jobDisplayId=job_display_id),
            json=data,
            params=params,
        )

    def get_task(self, job_display_id: int, task_id: str) -> TimelineTask:
        """``GET /job/{jobDisplayId}/timeline/{timelineTaskIdentifier}``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/timeline.get_task.html
        Response model: TimelineTask
        """
        return self._request(
            _GET_TASK.bind(jobDisplayId=job_display_id, timelineTaskIdentifier=task_id),
        )

    def update_task(
        self,
        job_display_id: int,
        task_id: str,
        *,
        data: TimelineTaskUpdateRequest | dict,
    ) -> TimelineTask:
        """``PATCH /job/{jobDisplayId}/timeline/{timelineTaskId}``

        Request model: :class:`TimelineTaskUpdateRequest`.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/timeline.update_task.html
        Request model: TimelineTaskUpdateRequest
        Response model: TimelineTask
        """
        return self._request(
            _PATCH_TASK.bind(jobDisplayId=job_display_id, timelineTaskId=task_id),
            json=data,
        )

    def delete_task(self, job_display_id: int, task_id: str) -> ServiceBaseResponse:
        """``DELETE /job/{jobDisplayId}/timeline/{timelineTaskId}``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/timeline.delete_task.html
        Response model: ServiceBaseResponse
        """
        return self._request(
            _DELETE_TASK.bind(jobDisplayId=job_display_id, timelineTaskId=task_id),
        )

    def get_agent(self, job_display_id: int, task_code: str) -> TimelineAgent | None:
        """``GET /job/{jobDisplayId}/timeline/{taskCode}/agent``

        Returns ``None`` when no agent is assigned for the given task code.
        """
        resp = self._client.request(
            _GET_AGENT.method,
            _GET_AGENT.bind(jobDisplayId=job_display_id, taskCode=task_code).path,
        )
        if resp is None:
            return None
        from ab.api.models.jobs import TimelineAgent as _TA

        return _TA.model_validate(resp)

    def increment_status(
        self,
        job_display_id: int,
        *,
        data: IncrementStatusRequest | dict,
    ) -> ServiceBaseResponse:
        """``POST /job/{jobDisplayId}/timeline/incrementjobstatus``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/timeline.increment_status.html
        Request model: IncrementStatusRequest
        Response model: ServiceBaseResponse
        """
        return self._request(_INCREMENT_STATUS.bind(jobDisplayId=job_display_id), json=data)

    def undo_increment_status(
        self,
        job_display_id: int,
        *,
        data: IncrementStatusRequest | dict,
    ) -> ServiceBaseResponse:
        """``POST /job/{jobDisplayId}/timeline/undoincrementjobstatus``

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/jobs/timeline.undo_increment_status.html
        Request model: IncrementStatusRequest
        Response model: ServiceBaseResponse
        """
        return self._request(_UNDO_INCREMENT_STATUS.bind(jobDisplayId=job_display_id), json=data)
