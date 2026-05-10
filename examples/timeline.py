"""Timeline API examples.

These snippets are intended to be copied into Sphinx docs. They use real
request JSON fixtures where a request body is required and show the response
model shape returned by each call.
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


api = ABConnectAPI(env="staging")


# GET /job/{jobDisplayId}/timeline
# Returns list[TimelineTask]. Use get_timeline_response() for the full wrapper.
tasks = api.jobs.get_timeline(TEST_JOB_DISPLAY_ID)


# GET /job/{jobDisplayId}/timeline
# Returns TimelineResponse with tasks, onHolds, SLA metadata, and job status.
timeline_response = api.jobs.get_timeline_response(TEST_JOB_DISPLAY_ID)


# GET /job/{jobDisplayId}/timeline/{timelineTaskIdentifier}
# Returns a single TimelineTask.
task = api.jobs.get_timeline_task(TEST_JOB_DISPLAY_ID, str(TEST_TIMELINE_TASK_ID))


# GET /job/{jobDisplayId}/timeline/{taskCode}/agent
# Returns TimelineAgent, or None when no agent is assigned for the task code.
agent = api.jobs.get_timeline_agent(TEST_JOB_DISPLAY_ID, TEST_TIMELINE_TASK_CODE)


def create_timeline_task_example() -> None:
    # POST /job/{jobDisplayId}/timeline?createEmail=false
    # Request body is a SimpleTaskRequest captured in tests/fixtures/requests.
    # Returns TimelineSaveResponse with success, taskExists, and task.
    request_body = load_request_json("SimpleTaskRequest.json")

    save_response = api.jobs.create_timeline_task(
        TEST_JOB_DISPLAY_ID,
        data=request_body,
        create_email=False,
    )

    print(save_response)


def update_timeline_task_example() -> None:
    # PATCH /job/{jobDisplayId}/timeline/{timelineTaskId}
    # Request body is TimelineTaskUpdateRequest.
    # Returns the updated TimelineTask.
    request_body = load_request_json("TimelineTaskUpdateRequest.json")

    updated_task = api.jobs.update_timeline_task(
        TEST_JOB_DISPLAY_ID,
        str(TEST_TIMELINE_TASK_ID),
        data=request_body,
    )

    print(updated_task)


def delete_timeline_task_example() -> None:
    # DELETE /job/{jobDisplayId}/timeline/{timelineTaskId}
    # Returns ServiceBaseResponse.
    response = api.jobs.delete_timeline_task(TEST_JOB_DISPLAY_ID, str(TEST_TIMELINE_TASK_ID))

    print(response)


if __name__ == "__main__":
    # Safe read examples run by default. Mutating examples are defined above
    # for documentation copy-paste, but are not executed automatically.
    print(tasks)
    print(timeline_response)
    print(task)
    print(agent)
