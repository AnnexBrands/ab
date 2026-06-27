"""Timeline helper behaviour after the redundant Job History note was removed.

Regression context: the ABConnect job-management endpoint now writes the Job
History note itself when a timeline task is saved. The SDK used to issue a
*second* ``POST /note`` to mirror the status change into Job History. That
redundant call required top-level note-write permission, which a
pickup-and-pack agent does not have — so advancing the pickup (PU) category as
an agent 403'd even though the pickup status change itself succeeded.

These tests pin the fix: the status helpers save the timeline task and make NO
raw ``/note`` request, and :meth:`TimelineHelpers._create_job_history_note` is a
deprecated no-op.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from ab.api.helpers.timeline import TimelineHelpers
from ab.api.models.jobs import (
    InTheFieldTaskRequest,
    SimpleTaskRequest,
    TimelineResponse,
    TimelineSaveResponse,
    TimelineTask,
    TimeLogRequest,
)
from ab.exceptions import RequestError


def _jobs(username: str = "brett@example.com") -> MagicMock:
    """A jobs mock whose raw HTTP client raises if touched.

    The status helpers must never call ``self._jobs._client.request`` now that
    the redundant ``POST /note`` is gone; wiring the client to raise turns any
    accidental reintroduction into a loud failure.
    """
    jobs = MagicMock()
    jobs._client._settings = SimpleNamespace(username=username)
    jobs._client.request.side_effect = AssertionError(
        "TimelineHelpers must not issue a raw request (the redundant POST /note "
        "was removed; the server records the Job History note)"
    )
    jobs.create_timeline_task.return_value = TimelineSaveResponse(
        success=True,
        task=TimelineTask(jobId="job-uuid"),
    )
    return jobs


def test_set_task_saves_timeline_task_and_makes_no_note_request():
    jobs = _jobs()
    helper = TimelineHelpers(jobs)
    task = InTheFieldTaskRequest(
        task_code="PU",
        planned_start_date="2026-06-01T10:00:00Z",
        planned_end_date="2026-06-01T12:00:00Z",
    )

    result = helper.set_task(4000000, "PU", task, method_name="schedule")

    assert result is jobs.create_timeline_task.return_value
    jobs.create_timeline_task.assert_called_once_with(
        4000000,
        data={
            "taskCode": "PU",
            "plannedStartDate": "2026-06-01T10:00:00Z",
            "plannedEndDate": "2026-06-01T12:00:00Z",
        },
        create_email=False,
    )
    # No redundant Job History note: the raw client is never touched.
    jobs._client.request.assert_not_called()
    jobs.note.create.assert_not_called()


def test_schedule_saves_pu_task_without_note_request():
    jobs = _jobs()
    jobs.get_timeline_response.return_value = TimelineResponse(
        tasks=[],
        jobSubManagementStatus={"name": "1 - Created"},
    )
    helper = TimelineHelpers(jobs)

    helper.schedule(4000000, start="2026-06-01T10:00:00Z", end="2026-06-01T12:00:00Z")

    data = jobs.create_timeline_task.call_args.kwargs["data"]
    assert data["taskCode"] == "PU"
    assert data["plannedStartDate"] == "2026-06-01T10:00:00Z"
    jobs._client.request.assert_not_called()


@pytest.mark.parametrize(
    "call_helper",
    [
        lambda helper: helper.schedule(4000000, start="2026-06-01T10:00:00Z", end="2026-06-01T12:00:00Z"),
        lambda helper: helper.received(4000000, start="2026-06-01T10:15:00Z", end="2026-06-01T12:30:00Z"),
        lambda helper: helper.pack_start(4000000, start="2026-06-02T10:00:00Z"),
        lambda helper: helper.pack_finish(4000000, end="2026-06-02T10:59:59Z"),
        lambda helper: helper.storage_begin(4000000, start="2026-06-03T10:00:00Z"),
        lambda helper: helper.storage_end(4000000, end="2026-06-03T10:59:59Z"),
        lambda helper: helper.carrier_schedule(4000000, start="2026-06-04T10:00:00Z"),
        lambda helper: helper.carrier_pickup(4000000, start="2026-06-04T10:59:59Z"),
        lambda helper: helper.carrier_delivery(4000000, end="2026-06-05T11:00:00Z"),
    ],
)
def test_named_task_helpers_make_no_redundant_note_request(call_helper):
    jobs = _jobs()
    jobs.get_timeline_response.return_value = TimelineResponse(
        tasks=[],
        jobSubManagementStatus={"name": "1 - Created"},
    )
    helper = TimelineHelpers(jobs)

    call_helper(helper)

    jobs.create_timeline_task.assert_called_once()
    jobs._client.request.assert_not_called()
    jobs.note.create.assert_not_called()


def test_received_positional_start_end_maps_on_site_time_log_in_order():
    jobs = _jobs()
    jobs.get_timeline_response.return_value = TimelineResponse(
        tasks=[],
        jobSubManagementStatus={"name": "2 - Scheduled"},
    )
    helper = TimelineHelpers(jobs)

    helper.received(4000000, "2026-06-01T10:15:00Z", "2026-06-01T12:30:00Z")

    data = jobs.create_timeline_task.call_args.kwargs["data"]
    assert data["completedDate"] == "2026-06-01T12:30:00Z"
    assert data["onSiteTimeLog"] == {
        "start": "2026-06-01T10:15:00Z",
        "end": "2026-06-01T12:30:00Z",
    }
    jobs._client.request.assert_not_called()


def test_received_single_positional_date_sets_completed_date_for_compatibility():
    jobs = _jobs()
    jobs.get_timeline_response.return_value = TimelineResponse(
        tasks=[],
        jobSubManagementStatus={"name": "2 - Scheduled"},
    )
    helper = TimelineHelpers(jobs)

    helper.received(4000000, "2026-06-01T12:30:00Z")

    data = jobs.create_timeline_task.call_args.kwargs["data"]
    assert data["completedDate"] == "2026-06-01T12:30:00Z"
    assert "onSiteTimeLog" not in data


def test_upsert_deep_merges_onto_existing_task_without_note_request():
    jobs = _jobs()
    helper = TimelineHelpers(jobs)
    existing = {
        "id": 123,
        "taskCode": "PK",
        "modifiedDate": "2026-06-02T09:00:00Z",
        "timeLog": {"start": "2026-06-02T10:00:00Z"},
    }
    task = SimpleTaskRequest(
        task_code="PK",
        time_log=TimeLogRequest(end="2026-06-02T10:59:59Z"),
    )

    helper._upsert(4000000, task, existing, method_name="pack_finish")

    data = jobs.create_timeline_task.call_args.kwargs["data"]
    # Prior data preserved, only the touched field overlaid.
    assert data["timeLog"] == {
        "start": "2026-06-02T10:00:00Z",
        "end": "2026-06-02T10:59:59Z",
    }
    jobs._client.request.assert_not_called()


def test_clear_pack_finish_noops_below_status_5_without_post():
    jobs = _jobs()
    jobs.get_timeline_response.return_value = TimelineResponse(
        tasks=[
            TimelineTask(
                id=123,
                taskCode="PK",
                modifiedDate="2026-06-02T09:00:00Z",
                timeLog={"id": 456, "start": "2026-06-02T10:00:00Z"},
            )
        ],
        jobSubManagementStatus={"name": "4 - Packaging Started"},
    )
    helper = TimelineHelpers(jobs)

    resp = helper.clear_pack_finish(4000000)

    assert resp.success is True
    assert resp.job_sub_management_status == {"name": "4 - Packaging Started"}
    assert "No-op" in (resp.error_message or "")
    jobs._client.request.assert_not_called()


def test_clear_pack_finish_posts_existing_pk_with_null_end_at_status_5():
    jobs = _jobs()
    jobs._client.request.side_effect = None
    jobs._client.request.return_value = {
        "success": True,
        "taskExists": False,
        "jobSubManagementStatus": {"name": "4 - Packaging Started"},
        "task": {
            "id": 123,
            "taskCode": "PK",
            "modifiedDate": "2026-06-02T09:30:00Z",
            "timeLog": {"id": 456, "start": "2026-06-02T10:00:00Z", "end": None},
        },
    }
    jobs.get_timeline_response.return_value = TimelineResponse(
        tasks=[
            TimelineTask(
                id=123,
                jobId="job-uuid",
                taskCode="PK",
                modifiedDate="2026-06-02T09:00:00Z",
                timeLog={
                    "id": 456,
                    "start": "2026-06-02T10:00:00Z",
                    "end": "2026-06-02T10:59:59Z",
                },
                workTimeLogs=[{"id": 789, "minutes": 12}],
            )
        ],
        jobSubManagementStatus={"name": "5 - Packaging Completed"},
    )
    helper = TimelineHelpers(jobs)

    resp = helper.clear_pack_finish(4000000, create_email=True)

    assert resp.success is True
    jobs._client.request.assert_called_once()
    args, kwargs = jobs._client.request.call_args
    assert args == ("POST", "/job/4000000/timeline")
    assert kwargs["params"] == {"createEmail": True}
    body = kwargs["json"]
    assert body["id"] == 123
    assert body["taskCode"] == "PK"
    assert body["modifiedDate"] == "2026-06-02T09:00:00Z"
    assert body["workTimeLogs"] == [{"id": 789, "minutes": 12}]
    assert body["timeLog"] == {
        "id": 456,
        "start": "2026-06-02T10:00:00Z",
        "end": None,
    }
    assert body["completedDate"] is None


def test_note_is_not_added_when_task_create_fails():
    jobs = _jobs()
    jobs.create_timeline_task.side_effect = RuntimeError("conflict")
    helper = TimelineHelpers(jobs)
    task = SimpleTaskRequest(task_code="PK", time_log=TimeLogRequest(start="2026-06-02T10:00:00Z"))

    with pytest.raises(RuntimeError, match="conflict"):
        helper.set_task(4000000, "PK", task, method_name="pack_start")

    jobs._client.request.assert_not_called()
    jobs.note.create.assert_not_called()


# ---- Regression: pickup-and-pack agent no longer 403s on the note ----------


def test_pickup_agent_status_with_note_does_not_403_on_redundant_note():
    """The exact regression: an agent that lacks note-write permission.

    Before the fix, advancing the pickup (PU) category issued a second
    ``POST /note`` that 403'd for the agent and propagated, masking the
    successful pickup status change. With the redundant call gone, the helper
    succeeds and never touches the raw ``/note`` endpoint.
    """
    jobs = MagicMock()
    jobs._client._settings = SimpleNamespace(username="Acme")
    # A pickup-and-pack agent: the timeline (PU) save succeeds...
    jobs.create_timeline_task.return_value = TimelineSaveResponse(
        success=True, task=TimelineTask(jobId="live-owned-job-uuid")
    )
    jobs.get_timeline_response.return_value = TimelineResponse(
        tasks=[], jobSubManagementStatus={"name": "2 - Scheduled"}
    )
    # ...but the raw note endpoint would 403 for the agent if ever called.
    jobs._client.request.side_effect = RequestError(403, "Forbidden")

    helper = TimelineHelpers(jobs)

    # Must NOT raise — the pickup category status-with-note now succeeds.
    result = helper.received(7009964, end="2026-06-01T12:00:00Z")

    assert result is jobs.create_timeline_task.return_value
    jobs._client.request.assert_not_called()


def test_create_job_history_note_is_deprecated_noop():
    """The retained method warns and performs no request (server owns the note)."""
    jobs = _jobs()
    helper = TimelineHelpers(jobs)

    with pytest.warns(DeprecationWarning, match="no-op"):
        helper._create_job_history_note(
            job_display_id=7009964,
            task_code="PU",
            data={"taskCode": "PU"},
            response=jobs.create_timeline_task.return_value,
            comment="ignored",
        )

    jobs._client.request.assert_not_called()
