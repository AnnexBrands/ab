"""Timeline helpers — high-level upsert operations with optimistic concurrency.

Provides get-then-set helpers for advancing job status through the timeline
workflow (schedule -> received -> pack -> storage -> carrier).  When a task
already exists the helper deep-merges its new fields onto the full server task
dict, preserving all prior data (notes, preferred dates, work time logs, etc.)
while updating only the fields the helper touches.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional

from ab.api.models.jobs import (
    BaseTimelineTaskRequest,
    CarrierTaskRequest,
    InTheFieldTaskRequest,
    SimpleTaskRequest,
    TimelineSaveResponse,
    TimeLogRequest,
)

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from ab.api.endpoints.jobs import JobsEndpoint

# Task code constants
PU = "PU"  # Pickup / field operations
PK = "PK"  # Packaging
ST = "ST"  # Storage
CP = "CP"  # Carrier pickup/delivery

# Task codes in deletion order (reverse of creation)
ALL_TASK_CODES = [PU, PK, ST, CP]
DELETE_ORDER = [CP, ST, PK, PU]


def _deep_merge(base: dict, overlay: dict) -> dict:
    """Recursively merge *overlay* onto *base*.

    Nested dicts are merged so that keys present in *base* but absent from
    *overlay* are preserved.  All other types (scalars, lists) in *overlay*
    replace the corresponding *base* value.
    """
    result = dict(base)
    for key, value in overlay.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


class TimelineHelpers:
    """High-level timeline operations with upsert and optimistic concurrency.

    Usage::

        api = ABConnectAPI()
        api.jobs.tasks.schedule(job_id, start="2026-03-01")
        api.jobs.tasks.received(job_id, end="2026-03-02")
    """

    def __init__(self, jobs: JobsEndpoint) -> None:
        self._jobs = jobs

    # ---- Core methods -------------------------------------------------------

    def get_task(self, job_id: int, taskcode: str) -> tuple[dict, Optional[dict]]:
        """Fetch timeline and extract a specific task by code.

        Returns:
            Tuple of (status_info_dict, task_dict_or_None).
            status_info contains jobSubManagementStatus from the response.
        """
        resp = self._jobs.get_timeline_response(job_id)
        resp_dict = resp.model_dump(by_alias=True, mode="json")

        status_info = resp_dict.get("jobSubManagementStatus") or {}

        task = None
        for t in resp_dict.get("tasks") or []:
            if t.get("taskCode") == taskcode:
                task = t
                break

        return status_info, task

    def set_task(
        self,
        job_id: int,
        taskcode: str,
        task: BaseTimelineTaskRequest,
        create_email: bool = False,
    ) -> TimelineSaveResponse:
        """Create or update a task via POST /timeline.

        Args:
            job_id: Job display ID.
            taskcode: Task code (PU, PK, ST, CP).
            task: Validated request model instance.
            create_email: Send status notification email.

        Serializes the model to a camelCase dict and sends it as-is.
        Callers that need to preserve existing task data should use
        ``_upsert`` instead.
        """
        data = task.model_dump(by_alias=True, exclude_none=True, exclude_unset=True, mode="json")
        return self._jobs.create_timeline_task(
            job_id, data=data, create_email=create_email,
        )

    def _upsert(
        self,
        job_id: int,
        model: BaseTimelineTaskRequest,
        existing: dict | None,
    ) -> TimelineSaveResponse:
        """Serialize *model* and deep-merge onto *existing* task, then POST.

        When *existing* is ``None`` (new task), the model is sent as-is.
        When *existing* is a task dict from the server, the model's
        explicitly-set fields are overlaid onto the full server dict so
        that all prior data (notes, preferred dates, work-time logs, etc.)
        is preserved.
        """
        data = model.model_dump(
            by_alias=True, exclude_none=True, exclude_unset=True, mode="json",
        )
        if existing is not None:
            data = _deep_merge(existing, data)
        return self._jobs.create_timeline_task(job_id, data=data)

    # ---- Status helpers (PU) ------------------------------------------------

    def schedule(
        self,
        job_id: int,
        start: str,
        end: str | None = None,
    ) -> TimelineSaveResponse:
        """Status 2 — Set planned pickup dates on PU task.

        Logs a warning if job is already at or past status 2.
        """
        status_info, task = self.get_task(job_id, PU)
        curr = _status_code(status_info)
        if curr >= 2:
            logger.warning("schedule() called at status %.1f (>= 2); proceeding", curr)

        model = InTheFieldTaskRequest(
            task_code=PU,
            planned_start_date=start,
            planned_end_date=end,
        )
        return self._upsert(job_id, model, task)

    _2 = schedule

    def received(
        self,
        job_id: int,
        end: str | None = None,
        start: str | None = None,
    ) -> TimelineSaveResponse:
        """Status 3 — Mark pickup completed on PU task.

        Args:
            end: Completed date. Uses current time if not provided.
            start: On-site start time. If provided with end, sets onSiteTimeLog.

        Logs a warning if job is already at or past status 3.
        """
        status_info, task = self.get_task(job_id, PU)
        curr = _status_code(status_info)
        if curr >= 3:
            logger.warning("received() called at status %.1f (>= 3); proceeding", curr)

        on_site_time_log = None
        if start and end:
            on_site_time_log = TimeLogRequest(start=start, end=end)
        elif start:
            on_site_time_log = TimeLogRequest(start=start, end=start)

        model = InTheFieldTaskRequest(
            task_code=PU,
            completed_date=end,
            on_site_time_log=on_site_time_log,
        )
        return self._upsert(job_id, model, task)

    _3 = received

    # ---- Status helpers (PK) ------------------------------------------------

    def pack_start(self, job_id: int, start: str) -> TimelineSaveResponse:
        """Status 4 — Set packaging start time on PK task.

        Logs a warning if job is already at or past status 4.
        """
        status_info, task = self.get_task(job_id, PK)
        curr = _status_code(status_info)
        if curr >= 4:
            logger.warning("pack_start() called at status %.1f (>= 4); proceeding", curr)

        model = SimpleTaskRequest(
            task_code=PK,
            time_log=TimeLogRequest(start=start),
        )
        return self._upsert(job_id, model, task)

    _4 = pack_start

    def pack_finish(self, job_id: int, end: str) -> TimelineSaveResponse:
        """Status 5 — Set packaging end time on PK task.

        Logs a warning if job is already at or past status 5.
        """
        status_info, task = self.get_task(job_id, PK)
        curr = _status_code(status_info)
        if curr >= 5:
            logger.warning("pack_finish() called at status %.1f (>= 5); proceeding", curr)

        model = SimpleTaskRequest(
            task_code=PK,
            time_log=TimeLogRequest(end=end),
        )
        return self._upsert(job_id, model, task)

    _5 = pack_finish

    # ---- Status helpers (ST) ------------------------------------------------

    def storage_begin(self, job_id: int, start: str) -> TimelineSaveResponse:
        """Status 6 — Set storage start time on ST task."""
        status_info, task = self.get_task(job_id, ST)

        model = SimpleTaskRequest(
            task_code=ST,
            time_log=TimeLogRequest(start=start),
        )
        return self._upsert(job_id, model, task)

    _6 = storage_begin

    def storage_end(self, job_id: int, end: str) -> TimelineSaveResponse:
        """Status 6 — Set storage end time on ST task."""
        status_info, task = self.get_task(job_id, ST)

        model = SimpleTaskRequest(
            task_code=ST,
            time_log=TimeLogRequest(end=end),
        )
        return self._upsert(job_id, model, task)

    # ---- Status helpers (CP) ------------------------------------------------

    def carrier_schedule(self, job_id: int, start: str) -> TimelineSaveResponse:
        """Status 7 — Set carrier scheduled date on CP task.

        Logs a warning if job is already at or past status 7.
        """
        status_info, task = self.get_task(job_id, CP)
        curr = _status_code(status_info)
        if curr >= 7:
            logger.warning("carrier_schedule() called at status %.1f (>= 7); proceeding", curr)

        model = CarrierTaskRequest(
            task_code=CP,
            scheduled_date=start,
        )
        return self._upsert(job_id, model, task)

    _7 = carrier_schedule

    def carrier_pickup(self, job_id: int, start: str) -> TimelineSaveResponse:
        """Status 8 — Set carrier pickup completed date on CP task.

        Logs a warning if job is already at or past status 8.
        """
        status_info, task = self.get_task(job_id, CP)
        curr = _status_code(status_info)
        if curr >= 8:
            logger.warning("carrier_pickup() called at status %.1f (>= 8); proceeding", curr)

        model = CarrierTaskRequest(
            task_code=CP,
            pickup_completed_date=start,
        )
        return self._upsert(job_id, model, task)

    _8 = carrier_pickup

    def carrier_delivery(self, job_id: int, end: str) -> TimelineSaveResponse:
        """Status 10 — Set carrier delivery completed date on CP task."""
        status_info, task = self.get_task(job_id, CP)

        model = CarrierTaskRequest(
            task_code=CP,
            delivery_completed_date=end,
        )
        return self._upsert(job_id, model, task)

    _10 = carrier_delivery

    # ---- Delete operations --------------------------------------------------

    def delete(self, job_id: int, taskcode: str) -> object | None:
        """Delete a specific task by code.

        Returns None if task not found.
        """
        _, task = self.get_task(job_id, taskcode)
        if task is None:
            return None

        task_id = task.get("id")
        if task_id is None:
            return None
        return self._jobs.delete_timeline_task(job_id, str(task_id))

    def delete_all(self, job_id: int) -> list:
        """Delete all timeline tasks in reverse order (CP -> ST -> PK -> PU).

        Returns list of successful deletion responses.
        """
        results = []
        for code in DELETE_ORDER:
            resp = self.delete(job_id, code)
            if resp is not None:
                results.append(resp)
        return results


def _status_code(status_info: dict) -> float:
    """Extract numeric status code from jobSubManagementStatus dict.

    The status name format is "N - Description" (e.g. "2 - Scheduled",
    "2.1 - Sub Status"). Returns float to handle sub-statuses.
    """
    name = status_info.get("name") or ""
    parts = name.split(" - ", 1)
    if parts:
        try:
            return float(parts[0])
        except (ValueError, TypeError):
            pass
    return 0
