"""Timeline helpers — high-level upsert operations with optimistic concurrency.

Provides get-then-set helpers for advancing job status through the timeline
workflow (schedule -> received -> pack -> storage -> carrier).  When a task
already exists the helper deep-merges its new fields onto the full server task
dict, preserving all prior data (notes, preferred dates, work time logs, etc.)
while updating only the fields the helper touches.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from ab.api.models.jobs import (
    BaseTimelineTaskRequest,
    CarrierTaskRequest,
    InTheFieldTaskRequest,
    SimpleTaskRequest,
    TimelineSaveResponse,
    TimeLogRequest,
)
from ab.api.models.notes import NoteRequest

JOB_HISTORY_CATEGORY_KEY = "JobNoteCategory"
JOB_HISTORY_CATEGORY_NAME = "Job History"
JOB_HISTORY_CATEGORY_ID = "10593366-BEA1-427A-A56E-E5AA0C977184"

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


def _parse_datetime(value: str | None) -> datetime | None:
    """Best-effort ISO datetime parser for note text formatting."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _format_datetime(value: str | None) -> str | None:
    parsed = _parse_datetime(value)
    if parsed is None:
        return value
    return parsed.strftime("%Y-%m-%d %H:%M")


def _format_date_range(start: str | None, end: str | None) -> str:
    """Format the best available task date range for an audit note."""
    if start and end:
        parsed_start = _parse_datetime(start)
        parsed_end = _parse_datetime(end)
        if parsed_start and parsed_end and parsed_start.date() == parsed_end.date():
            return f"{parsed_start:%Y-%m-%d} {parsed_start:%H:%M}-{parsed_end:%H:%M}"
        return f"{_format_datetime(start)} - {_format_datetime(end)}"
    if start:
        return _format_datetime(start) or start
    if end:
        return _format_datetime(end) or end
    return "unknown date"


def _task_date_range(data: dict, method_name: str) -> str:
    """Extract a human-readable date or date range from timeline task data."""
    time_log = data.get("timeLog") or {}
    on_site_time_log = data.get("onSiteTimeLog") or {}

    if method_name == "schedule":
        return _format_date_range(data.get("plannedStartDate"), data.get("plannedEndDate"))
    if method_name == "received":
        if on_site_time_log:
            return _format_date_range(on_site_time_log.get("start"), on_site_time_log.get("end"))
        return _format_date_range(None, data.get("completedDate"))
    if method_name in {"pack_start", "pack_finish", "storage_begin", "storage_end"}:
        return _format_date_range(time_log.get("start"), time_log.get("end"))
    if method_name == "carrier_schedule":
        return _format_date_range(data.get("scheduledDate"), None)
    if method_name == "carrier_pickup":
        return _format_date_range(data.get("pickupCompletedDate"), None)
    if method_name == "carrier_delivery":
        return _format_date_range(None, data.get("deliveryCompletedDate"))

    candidates = [
        (data.get("plannedStartDate"), data.get("plannedEndDate")),
        (on_site_time_log.get("start"), on_site_time_log.get("end")),
        (time_log.get("start"), time_log.get("end")),
        (data.get("scheduledDate"), None),
        (data.get("pickupCompletedDate"), None),
        (None, data.get("deliveryCompletedDate")),
        (None, data.get("completedDate")),
        (data.get("targetStartDate"), data.get("actualEndDate")),
    ]
    for start, end in candidates:
        if start or end:
            return _format_date_range(start, end)
    return "unknown date"


class TimelineHelpers:
    """High-level timeline operations with upsert and optimistic concurrency.

    Usage::

        api = ABConnectAPI()
        api.jobs.tasks.schedule(job_id, start="2026-03-01")
        api.jobs.tasks.received(job_id, end="2026-03-02")
        api.jobs.tasks.received(job_id, "2026-03-02T09:00:00", "2026-03-02T10:00:00")
    """

    def __init__(self, jobs: JobsEndpoint) -> None:
        self._jobs = jobs
        self._job_history_category_id: str | None = None

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
        method_name: str = "set_task",
    ) -> TimelineSaveResponse:
        """Create or update a task via POST /timeline.

        Args:
            job_id: Job display ID.
            taskcode: Task code (PU, PK, ST, CP).
            task: Validated request model instance.
            create_email: Send status notification email.
            method_name: Name to record in the audit note.

        Serializes the model to a camelCase dict and sends it as-is.
        Callers that need to preserve existing task data should use
        ``_upsert`` instead.
        """
        data = task.model_dump(by_alias=True, exclude_none=True, exclude_unset=True, mode="json")
        return self._save_task_with_note(
            job_id,
            data=data,
            create_email=create_email,
            method_name=method_name,
            task_code=taskcode,
        )

    def _upsert(
        self,
        job_id: int,
        model: BaseTimelineTaskRequest,
        existing: dict | None,
        create_email: bool = False,
        method_name: str = "set_task",
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
        return self._save_task_with_note(
            job_id,
            data=data,
            create_email=create_email,
            method_name=method_name,
            task_code=data.get("taskCode"),
        )

    def _save_task_with_note(
        self,
        job_id: int,
        *,
        data: dict,
        create_email: bool,
        method_name: str,
        task_code: str | None,
    ) -> TimelineSaveResponse:
        """POST timeline task data, then add the matching job note."""
        response = self._jobs.create_timeline_task(
            job_id,
            data=data,
            create_email=create_email,
        )
        self._create_job_history_note(
            job_display_id=job_id,
            task_code=task_code,
            data=data,
            response=response,
            comment=f"{self._username()} set {method_name} for {_task_date_range(data, method_name)}",
        )
        return response

    def _create_job_history_note(
        self,
        *,
        job_display_id: int,
        task_code: str | None,
        data: dict,
        response: TimelineSaveResponse,
        comment: str,
    ) -> None:
        """Create a top-level job note in the Job History category."""
        job_uuid = self._job_uuid(job_display_id, task_code, data, response)
        if not job_uuid:
            logger.warning("Could not resolve job UUID for job %s; skipping job history note", job_display_id)
            return

        self._jobs._client.request(
            "POST",
            "/note",
            json=NoteRequest.check(
                NoteRequest(
                    comments=comment,
                    category=self._job_history_category(),
                    job_id=job_uuid,
                    is_important=False,
                    send_notification=False,
                )
            ),
        )

    def _job_history_category(self) -> str:
        """Resolve the Job History note category from lookups, with a known fallback."""
        if self._job_history_category_id:
            return self._job_history_category_id

        try:
            categories = self._jobs._client.request("GET", f"/lookup/{JOB_HISTORY_CATEGORY_KEY}")
        except Exception as exc:  # pragma: no cover - defensive live API fallback
            logger.warning("Could not resolve %s lookup: %s", JOB_HISTORY_CATEGORY_KEY, exc)
            self._job_history_category_id = JOB_HISTORY_CATEGORY_ID
            return self._job_history_category_id

        for category in categories or []:
            if str(category.get("name", "")).casefold() == JOB_HISTORY_CATEGORY_NAME.casefold():
                self._job_history_category_id = category.get("id") or category.get("value") or JOB_HISTORY_CATEGORY_ID
                return self._job_history_category_id

        self._job_history_category_id = JOB_HISTORY_CATEGORY_ID
        return self._job_history_category_id

    def _job_uuid(
        self,
        job_display_id: int,
        task_code: str | None,
        data: dict,
        response: TimelineSaveResponse,
    ) -> str | None:
        """Resolve the job UUID needed by the top-level notes endpoint."""
        task = getattr(response, "task", None)
        if getattr(task, "job_id", None):
            return task.job_id
        if data.get("jobId"):
            return data["jobId"]
        if not task_code:
            return None

        _, current_task = self.get_task(job_display_id, task_code)
        if current_task:
            return current_task.get("jobId")
        return None

    def _username(self) -> str:
        """Return the configured API username for helper audit notes."""
        settings = getattr(getattr(self._jobs, "_client", None), "_settings", None)
        return getattr(settings, "username", None) or "Unknown user"

    # ---- Status helpers (PU) ------------------------------------------------

    def schedule(
        self,
        job_id: int,
        start: str,
        end: str | None = None,
        create_email: bool = False,
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
        return self._upsert(job_id, model, task, create_email=create_email, method_name="schedule")

    _2 = schedule

    def received(
        self,
        job_id: int,
        *args: str | bool,
        start: str | None = None,
        end: str | None = None,
        create_email: bool = False,
    ) -> TimelineSaveResponse:
        """Status 3 — Mark pickup completed on PU task.

        Args:
            Positional date arguments are accepted as ``received(job_id, start, end)``.
            A single positional date is treated as ``end`` for compatibility.
            end: Completed date. Uses current time if not provided.
            start: On-site start time. If provided with end, sets onSiteTimeLog.

        Logs a warning if job is already at or past status 3.
        """
        if args:
            if len(args) == 1:
                if start is not None:
                    raise TypeError("received() positional date cannot be combined with start keyword")
                if end is None:
                    end = args[0]
                else:
                    start = args[0]
            elif len(args) == 2:
                if start is not None or end is not None:
                    raise TypeError("received() positional dates cannot be combined with start/end keywords")
                start, end = args
            elif len(args) == 3:
                if start is not None or end is not None:
                    raise TypeError("received() positional dates cannot be combined with start/end keywords")
                if not isinstance(args[2], bool):
                    raise TypeError("received() create_email positional argument must be a bool")
                start, end = args[:2]
                create_email = args[2]
            else:
                raise TypeError("received() accepts at most 3 positional arguments after job_id")

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
        return self._upsert(job_id, model, task, create_email=create_email, method_name="received")

    _3 = received

    # ---- Status helpers (PK) ------------------------------------------------

    def pack_start(
        self, job_id: int, start: str, create_email: bool = False,
    ) -> TimelineSaveResponse:
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
        return self._upsert(job_id, model, task, create_email=create_email, method_name="pack_start")

    _4 = pack_start

    def pack_finish(
        self, job_id: int, end: str, create_email: bool = False,
    ) -> TimelineSaveResponse:
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
        return self._upsert(job_id, model, task, create_email=create_email, method_name="pack_finish")

    _5 = pack_finish

    # ---- Status helpers (ST) ------------------------------------------------

    def storage_begin(
        self, job_id: int, start: str, create_email: bool = False,
    ) -> TimelineSaveResponse:
        """Status 6 — Set storage start time on ST task."""
        status_info, task = self.get_task(job_id, ST)

        model = SimpleTaskRequest(
            task_code=ST,
            time_log=TimeLogRequest(start=start),
        )
        return self._upsert(job_id, model, task, create_email=create_email, method_name="storage_begin")

    _6 = storage_begin

    def storage_end(
        self, job_id: int, end: str, create_email: bool = False,
    ) -> TimelineSaveResponse:
        """Status 6 — Set storage end time on ST task."""
        status_info, task = self.get_task(job_id, ST)

        model = SimpleTaskRequest(
            task_code=ST,
            time_log=TimeLogRequest(end=end),
        )
        return self._upsert(job_id, model, task, create_email=create_email, method_name="storage_end")

    # ---- Status helpers (CP) ------------------------------------------------

    def carrier_schedule(
        self, job_id: int, start: str, create_email: bool = False,
    ) -> TimelineSaveResponse:
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
        return self._upsert(job_id, model, task, create_email=create_email, method_name="carrier_schedule")

    _7 = carrier_schedule

    def carrier_pickup(
        self, job_id: int, start: str, create_email: bool = False,
    ) -> TimelineSaveResponse:
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
        return self._upsert(job_id, model, task, create_email=create_email, method_name="carrier_pickup")

    _8 = carrier_pickup

    def carrier_delivery(
        self, job_id: int, end: str, create_email: bool = False,
    ) -> TimelineSaveResponse:
        """Status 10 — Set carrier delivery completed date on CP task."""
        status_info, task = self.get_task(job_id, CP)

        model = CarrierTaskRequest(
            task_code=CP,
            delivery_completed_date=end,
        )
        return self._upsert(job_id, model, task, create_email=create_email, method_name="carrier_delivery")

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
