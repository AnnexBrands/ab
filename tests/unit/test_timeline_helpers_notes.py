"""Unit tests for timeline helper audit-note creation."""

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


def _jobs(username: str = "brett@example.com") -> MagicMock:
    jobs = MagicMock()
    jobs._client._settings = SimpleNamespace(username=username)
    jobs._client.request.side_effect = [
        [{"id": "history-category-id", "name": "Job History"}],
        {
            "noteID": 100,
            "comments": "note",
            "category": "history-category-id",
            "jobId": "job-uuid",
        },
    ]
    jobs.create_timeline_task.return_value = TimelineSaveResponse(
        success=True,
        task=TimelineTask(jobId="job-uuid"),
    )
    return jobs


def _created_note_payload(jobs: MagicMock) -> dict:
    request = jobs._client.request.call_args_list[-1]
    assert request.args == ("POST", "/note")
    return request.kwargs["json"]


def test_set_task_creates_task_then_adds_note():
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
    assert jobs._client.request.call_args_list[0].args == ("GET", "/lookup/JobNoteCategory")
    assert _created_note_payload(jobs) == {
        "comments": "brett@example.com set schedule for 2026-06-01 10:00-12:00",
        "category": "history-category-id",
        "isImportant": False,
        "jobId": "job-uuid",
        "sendNotification": False,
    }
    jobs.note.create.assert_not_called()


def test_schedule_creates_jobhistory_note_with_related_task_code():
    jobs = _jobs()
    jobs.get_timeline_response.return_value = TimelineResponse(
        tasks=[],
        jobSubManagementStatus={"name": "1 - Created"},
    )
    helper = TimelineHelpers(jobs)

    helper.schedule(
        4000000,
        start="2026-06-01T10:00:00Z",
        end="2026-06-01T12:00:00Z",
    )

    assert _created_note_payload(jobs) == {
        "comments": "brett@example.com set schedule for 2026-06-01 10:00-12:00",
        "category": "history-category-id",
        "isImportant": False,
        "jobId": "job-uuid",
        "sendNotification": False,
    }


def test_received_positional_start_end_maps_on_site_time_log_in_order():
    jobs = _jobs()
    jobs.get_timeline_response.return_value = TimelineResponse(
        tasks=[],
        jobSubManagementStatus={"name": "2 - Scheduled"},
    )
    helper = TimelineHelpers(jobs)

    helper.received(
        4000000,
        "2026-06-01T10:15:00Z",
        "2026-06-01T12:30:00Z",
    )

    data = jobs.create_timeline_task.call_args.kwargs["data"]
    assert data["completedDate"] == "2026-06-01T12:30:00Z"
    assert data["onSiteTimeLog"] == {
        "start": "2026-06-01T10:15:00Z",
        "end": "2026-06-01T12:30:00Z",
    }


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


@pytest.mark.parametrize(
    ("call_helper", "expected_comment"),
    [
        (
            lambda helper: helper.schedule(
                4000000,
                start="2026-06-01T10:00:00Z",
                end="2026-06-01T12:00:00Z",
            ),
            "brett@example.com set schedule for 2026-06-01 10:00-12:00",
        ),
        (
            lambda helper: helper.received(
                4000000,
                start="2026-06-01T10:15:00Z",
                end="2026-06-01T12:30:00Z",
            ),
            "brett@example.com set received for 2026-06-01 10:15-12:30",
        ),
        (
            lambda helper: helper.pack_start(4000000, start="2026-06-02T10:00:00Z"),
            "brett@example.com set pack_start for 2026-06-02 10:00",
        ),
        (
            lambda helper: helper.pack_finish(4000000, end="2026-06-02T10:59:59Z"),
            "brett@example.com set pack_finish for 2026-06-02 10:59",
        ),
        (
            lambda helper: helper.storage_begin(4000000, start="2026-06-03T10:00:00Z"),
            "brett@example.com set storage_begin for 2026-06-03 10:00",
        ),
        (
            lambda helper: helper.storage_end(4000000, end="2026-06-03T10:59:59Z"),
            "brett@example.com set storage_end for 2026-06-03 10:59",
        ),
        (
            lambda helper: helper.carrier_schedule(4000000, start="2026-06-04T10:00:00Z"),
            "brett@example.com set carrier_schedule for 2026-06-04 10:00",
        ),
        (
            lambda helper: helper.carrier_pickup(4000000, start="2026-06-04T10:59:59Z"),
            "brett@example.com set carrier_pickup for 2026-06-04 10:59",
        ),
        (
            lambda helper: helper.carrier_delivery(4000000, end="2026-06-05T11:00:00Z"),
            "brett@example.com set carrier_delivery for 2026-06-05 11:00",
        ),
    ],
)
def test_named_task_helpers_create_top_level_job_history_notes(call_helper, expected_comment):
    jobs = _jobs()
    jobs.get_timeline_response.return_value = TimelineResponse(
        tasks=[],
        jobSubManagementStatus={"name": "1 - Created"},
    )
    helper = TimelineHelpers(jobs)

    call_helper(helper)

    assert _created_note_payload(jobs) == {
        "comments": expected_comment,
        "category": "history-category-id",
        "isImportant": False,
        "jobId": "job-uuid",
        "sendNotification": False,
    }
    jobs.note.create.assert_not_called()


def test_upsert_adds_note_from_merged_task_range():
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
    assert data["timeLog"] == {
        "start": "2026-06-02T10:00:00Z",
        "end": "2026-06-02T10:59:59Z",
    }
    assert _created_note_payload(jobs)["comments"] == (
        "brett@example.com set pack_finish for 2026-06-02 10:00-10:59"
    )


def test_received_note_uses_completed_date_over_existing_planned_date():
    jobs = _jobs()
    helper = TimelineHelpers(jobs)
    existing = {
        "id": 456,
        "taskCode": "PU",
        "plannedStartDate": "2026-06-01T10:00:00Z",
        "plannedEndDate": "2026-06-01T12:00:00Z",
    }
    task = InTheFieldTaskRequest(
        task_code="PU",
        completed_date="2026-06-03T15:30:00Z",
    )

    helper._upsert(4000000, task, existing, method_name="received")

    assert _created_note_payload(jobs)["comments"] == "brett@example.com set received for 2026-06-03 15:30"


def test_note_is_not_added_when_task_create_fails():
    jobs = _jobs()
    jobs.create_timeline_task.side_effect = RuntimeError("conflict")
    helper = TimelineHelpers(jobs)
    task = SimpleTaskRequest(task_code="PK", time_log=TimeLogRequest(start="2026-06-02T10:00:00Z"))

    with pytest.raises(RuntimeError, match="conflict"):
        helper.set_task(4000000, "PK", task, method_name="pack_start")

    jobs._client.request.assert_not_called()
    jobs.note.create.assert_not_called()
