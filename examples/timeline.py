"""Timeline API examples.

These snippets are intended to be copied into Sphinx docs. They use real
request JSON fixtures where a request body is required and show the response
model shape returned by each call.

Importing this module is side-effect free: the API client is constructed and
the live calls run only when the module is executed (``python -m
examples.timeline``) or when a function below is called explicitly.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ab import ABConnectAPI
from examples.constants import TEST_JOB_DISPLAY_ID, TEST_TIMELINE_TASK_CODE, TEST_TIMELINE_TASK_ID


REQUESTS_DIR = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "requests"


def load_request_json(filename: str) -> dict[str, Any]:
    """Load a captured request body from tests/fixtures/requests."""
    return json.loads((REQUESTS_DIR / filename).read_text())


def read_examples(api: ABConnectAPI) -> None:
    # GET /job/{jobDisplayId}/timeline
    # Returns list[TimelineTask]. Use timeline.response() for the full wrapper.
    tasks = api.jobs.timeline.list(TEST_JOB_DISPLAY_ID)

    # GET /job/{jobDisplayId}/timeline
    # Returns TimelineResponse with tasks, onHolds, SLA metadata, and job status.
    timeline_response = api.jobs.timeline.response(TEST_JOB_DISPLAY_ID)

    # GET /job/{jobDisplayId}/timeline/{timelineTaskIdentifier}
    # Returns a single TimelineTask.
    task = api.jobs.timeline.get_task(TEST_JOB_DISPLAY_ID, str(TEST_TIMELINE_TASK_ID))

    # GET /job/{jobDisplayId}/timeline/{taskCode}/agent
    # Returns TimelineAgent, or None when no agent is assigned for the task code.
    agent = api.jobs.timeline.get_agent(TEST_JOB_DISPLAY_ID, TEST_TIMELINE_TASK_CODE)

    print(tasks)
    print(timeline_response)
    print(task)
    print(agent)


def create_timeline_task_example(api: ABConnectAPI) -> None:
    # POST /job/{jobDisplayId}/timeline?createEmail=false
    # Request body is a SimpleTaskRequest captured in tests/fixtures/requests.
    # Returns TimelineSaveResponse with success, taskExists, and task.
    request_body = load_request_json("SimpleTaskRequest.json")

    save_response = api.jobs.timeline.create_task(
        TEST_JOB_DISPLAY_ID,
        data=request_body,
        create_email=False,
    )

    print(save_response)


def update_timeline_task_example(api: ABConnectAPI) -> None:
    # PATCH /job/{jobDisplayId}/timeline/{timelineTaskId}
    # Request body is TimelineTaskUpdateRequest.
    # Returns the updated TimelineTask.
    request_body = load_request_json("TimelineTaskUpdateRequest.json")

    updated_task = api.jobs.timeline.update_task(
        TEST_JOB_DISPLAY_ID,
        str(TEST_TIMELINE_TASK_ID),
        data=request_body,
    )

    print(updated_task)


def delete_timeline_task_example(api: ABConnectAPI) -> None:
    # DELETE /job/{jobDisplayId}/timeline/{timelineTaskId}
    # Returns ServiceBaseResponse.
    response = api.jobs.timeline.delete_task(TEST_JOB_DISPLAY_ID, str(TEST_TIMELINE_TASK_ID))

    print(response)


if __name__ == "__main__":
    # Safe read examples run by default. Mutating examples are defined above
    # for documentation copy-paste, but are not executed automatically.
    api = ABConnectAPI(env="staging")
    read_examples(api)
