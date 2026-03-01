"""Timeline helpers — high-level status transition operations.

Provides idempotent get-then-set helpers for advancing job status
through the timeline workflow (schedule → received → pack → storage → carrier).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

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

# New task templates — used when a task doesn't exist yet
_NEW_FIELD_TASK_SCH = {"taskCode": PU, "completedDate": None}
_NEW_FIELD_TASK = {"taskCode": PU, "onSiteTimeLog": {}, "completedDate": None}
_NEW_PACK_TASK = {"taskCode": PK, "timeLog": {}, "workTimeLogs": []}
_NEW_STORE_TASK = {"taskCode": ST, "timeLog": {}, "workTimeLogs": []}
_NEW_CARRIER_TASK = {
    "taskCode": CP,
    "scheduledDate": None,
    "pickupCompletedDate": None,
    "deliveryCompletedDate": None,
}


class TimelineHelpers:
    """High-level timeline operations with get-then-set collision prevention.

    Usage::

        api = ABConnectAPI()
        api.jobs.timeline.schedule(job_id, start="2026-03-01")
        api.jobs.timeline.received(job_id, end="2026-03-02")
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
        task: dict,
        create_email: bool = False,
    ) -> Any:
        """Create or update a task via POST /timeline.

        The API automatically handles create vs update based on
        whether the task already exists.
        """
        return self._jobs.create_timeline_task(
            job_id, data=task, create_email=create_email,
        )

    # ---- Status helpers (PU) ------------------------------------------------

    def schedule(
        self,
        job_id: int,
        start: str,
        end: str | None = None,
    ) -> Any | None:
        """Status 2 — Set planned pickup dates on PU task.

        Returns None if job is already at or past status 2.
        """
        status_info, task = self.get_task(job_id, PU)
        curr = _status_code(status_info)
        if curr >= 2:
            return None

        if task is None:
            task = _NEW_FIELD_TASK_SCH.copy()
        task["plannedStartDate"] = start
        if end is not None:
            task["plannedEndDate"] = end
        return self.set_task(job_id, PU, task)

    _2 = schedule

    def received(
        self,
        job_id: int,
        end: str | None = None,
        start: str | None = None,
    ) -> Any | None:
        """Status 3 — Mark pickup completed on PU task.

        Args:
            end: Completed date. Uses current time if not provided.
            start: On-site start time. If provided with end, sets onSiteTimeLog.

        Returns None if job is already at or past status 3.
        """
        status_info, task = self.get_task(job_id, PU)
        curr = _status_code(status_info)
        if curr >= 3:
            return None

        if task is None:
            task = _NEW_FIELD_TASK.copy()

        if end:
            task["completedDate"] = end
        if start and end:
            task["onSiteTimeLog"] = {"start": start, "end": end}
        elif start:
            task["onSiteTimeLog"] = {"start": start, "end": start}
        else:
            task.pop("onSiteTimeLog", None)

        return self.set_task(job_id, PU, task)

    _3 = received

    # ---- Status helpers (PK) ------------------------------------------------

    def pack_start(self, job_id: int, start: str) -> Any | None:
        """Status 4 — Set packaging start time on PK task.

        Returns None if job is already at or past status 4.
        """
        status_info, task = self.get_task(job_id, PK)
        curr = _status_code(status_info)
        if curr >= 4:
            return None

        if task is None:
            task = _NEW_PACK_TASK.copy()
        task["timeLog"] = {"start": start}
        return self.set_task(job_id, PK, task)

    _4 = pack_start

    def pack_finish(self, job_id: int, end: str) -> Any | None:
        """Status 5 — Set packaging end time on PK task.

        Returns None if job is already at or past status 5.
        """
        status_info, task = self.get_task(job_id, PK)
        curr = _status_code(status_info)
        if curr >= 5:
            return None

        if task is None:
            task = _NEW_PACK_TASK.copy()
            task["timeLog"] = {}
        if "timeLog" not in task or task["timeLog"] is None:
            task["timeLog"] = {}
        task["timeLog"]["end"] = end
        return self.set_task(job_id, PK, task)

    _5 = pack_finish

    # ---- Status helpers (ST) ------------------------------------------------

    def storage_begin(self, job_id: int, start: str) -> Any:
        """Status 6 — Set storage start time on ST task.

        Always allows update (no status downgrade prevention).
        """
        status_info, task = self.get_task(job_id, ST)

        if task is None:
            task = _NEW_STORE_TASK.copy()
        if "timeLog" not in task or task["timeLog"] is None:
            task["timeLog"] = {}
        task["timeLog"]["start"] = start
        return self.set_task(job_id, ST, task)

    _6 = storage_begin

    def storage_end(self, job_id: int, end: str) -> Any:
        """Status 6 — Set storage end time on ST task.

        Always allows update (no status downgrade prevention).
        """
        status_info, task = self.get_task(job_id, ST)

        if task is None:
            task = _NEW_STORE_TASK.copy()
        if "timeLog" not in task or task["timeLog"] is None:
            task["timeLog"] = {}
        task["timeLog"]["end"] = end
        return self.set_task(job_id, ST, task)

    # ---- Status helpers (CP) ------------------------------------------------

    def carrier_schedule(self, job_id: int, start: str) -> Any | None:
        """Status 7 — Set carrier scheduled date on CP task.

        Returns None if job is already at or past status 7.
        """
        status_info, task = self.get_task(job_id, CP)
        curr = _status_code(status_info)
        if curr >= 7:
            return None

        if task is None:
            task = _NEW_CARRIER_TASK.copy()
        task["scheduledDate"] = start
        return self.set_task(job_id, CP, task)

    _7 = carrier_schedule

    def carrier_pickup(self, job_id: int, start: str) -> Any | None:
        """Status 8 — Set carrier pickup completed date on CP task.

        Returns None if job is already at or past status 8.
        """
        status_info, task = self.get_task(job_id, CP)
        curr = _status_code(status_info)
        if curr >= 8:
            return None

        if task is None:
            task = _NEW_CARRIER_TASK.copy()
        task["pickupCompletedDate"] = start
        return self.set_task(job_id, CP, task)

    _8 = carrier_pickup

    def carrier_delivery(self, job_id: int, end: str) -> Any:
        """Status 10 — Set carrier delivery completed date on CP task.

        Always allows update (no status downgrade prevention).
        """
        status_info, task = self.get_task(job_id, CP)

        if task is None:
            task = _NEW_CARRIER_TASK.copy()
        task["deliveryCompletedDate"] = end
        return self.set_task(job_id, CP, task)

    _10 = carrier_delivery

    # ---- Delete operations --------------------------------------------------

    def delete(self, job_id: int, taskcode: str) -> Any | None:
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
        """Delete all timeline tasks in reverse order (CP → ST → PK → PU).

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
