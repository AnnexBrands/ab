"""Timeline API examples.

These snippets are intended to be copied into Sphinx docs. They use real
request JSON fixtures where a request body is required and show the response
model shape returned by each call.

Importing this module is side-effect free: the API client is constructed and
the live calls run only when the module is executed (``python -m
examples.timeline``) or when a function below is called explicitly.
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, mutations_enabled, save
from examples.constants import TEST_JOB_DISPLAY_ID, TEST_TIMELINE_TASK_CODE, TEST_TIMELINE_TASK_ID


def read_examples(api: ABConnectAPI) -> None:
    # GET /job/{jobDisplayId}/timeline
    # Returns list[TimelineTask]. Use timeline.response() for the full wrapper.
    tasks = api.jobs.timeline.list(TEST_JOB_DISPLAY_ID)
    print(format_result(tasks))

    # GET /job/{jobDisplayId}/timeline
    # Returns TimelineResponse with tasks, onHolds, SLA metadata, and job status.
    timeline_response = api.jobs.timeline.response(TEST_JOB_DISPLAY_ID)
    print(format_result(timeline_response))
    save("TimelineResponse.json", timeline_response)

    # GET /job/{jobDisplayId}/timeline/{timelineTaskIdentifier}
    # Returns a single TimelineTask.
    task = api.jobs.timeline.get_task(TEST_JOB_DISPLAY_ID, str(TEST_TIMELINE_TASK_ID))
    print(format_result(task))
    save("TimelineTask.json", task)

    # GET /job/{jobDisplayId}/timeline/{taskCode}/agent
    # Returns TimelineAgent, or None when no agent is assigned for the task code.
    agent = api.jobs.timeline.get_agent(TEST_JOB_DISPLAY_ID, TEST_TIMELINE_TASK_CODE)
    print(format_result(agent))
    if agent is not None:
        save("TimelineAgent.json", agent)


def create_timeline_task_example(api: ABConnectAPI):
    # POST /job/{jobDisplayId}/timeline?createEmail=false
    # Request body is a SimpleTaskRequest captured in tests/fixtures/requests.
    # Returns TimelineSaveResponse with success, taskExists, and task.
    request_body = load_request("SimpleTaskRequest.json")

    save_response = api.jobs.timeline.create_task(
        TEST_JOB_DISPLAY_ID,
        data=request_body,
        create_email=False,
    )

    print(format_result(save_response))
    save("TimelineSaveResponse.json", save_response)
    return save_response


def update_timeline_task_example(api: ABConnectAPI, task_id: str = str(TEST_TIMELINE_TASK_ID)) -> None:
    # PATCH /job/{jobDisplayId}/timeline/{timelineTaskId}
    # Request body is TimelineTaskUpdateRequest.
    # Returns the updated TimelineTask.
    request_body = load_request("TimelineTaskUpdateRequest.json")

    updated_task = api.jobs.timeline.update_task(
        TEST_JOB_DISPLAY_ID,
        task_id,
        data=request_body,
    )

    print(format_result(updated_task))


def delete_timeline_task_example(api: ABConnectAPI, task_id: str = str(TEST_TIMELINE_TASK_ID)) -> None:
    # DELETE /job/{jobDisplayId}/timeline/{timelineTaskId}
    # Returns ServiceBaseResponse.
    response = api.jobs.timeline.delete_task(TEST_JOB_DISPLAY_ID, task_id)

    print(format_result(response))


def increment_status_example(api: ABConnectAPI) -> None:
    # POST /job/{jobDisplayId}/timeline/incrementjobstatus
    # Advances the job to its next timeline status. Request body is an
    # IncrementStatusRequest (createEmail toggles the status notification email).
    # Returns ServiceBaseResponse.
    request_body = load_request("IncrementStatusRequest.json")

    response = api.jobs.timeline.increment_status(TEST_JOB_DISPLAY_ID, data=request_body)

    print(format_result(response))
    save("ServiceBaseResponse.json", response)


def undo_increment_status_example(api: ABConnectAPI) -> None:
    # POST /job/{jobDisplayId}/timeline/undoincrementjobstatus
    # Reverts the most recent timeline status increment. Request body is an
    # IncrementStatusRequest. Returns ServiceBaseResponse.
    request_body = load_request("IncrementStatusRequest.json")

    response = api.jobs.timeline.undo_increment_status(TEST_JOB_DISPLAY_ID, data=request_body)

    print(format_result(response))


if __name__ == "__main__":
    # Safe read examples run by default.
    api = ABConnectAPI(env="staging")
    read_examples(api)

    # State-changing timeline calls are guarded — they only run when
    # AB_RUN_MUTATIONS=1 is set (they mutate staging). create -> update ->
    # delete runs against the captured SimpleTaskRequest task, then the
    # increment/undo pair leaves the job status where it started.
    if mutations_enabled():
        created = create_timeline_task_example(api)
        # Update/delete run against the task just created above — never against
        # the committed TEST_TIMELINE_TASK_ID task the read examples rely on.
        created_id = str(created.task.id) if created and created.task else None
        if created_id:
            update_timeline_task_example(api, created_id)
            delete_timeline_task_example(api, created_id)
        else:
            print("# update_task/delete_task skipped — create returned no task id")
        increment_status_example(api)
        undo_increment_status_example(api)
    else:
        print(
            "# api.jobs.timeline.create_task / update_task / delete_task /"
            " increment_status / undo_increment_status skipped"
            " — set AB_RUN_MUTATIONS=1 to run (mutates staging)"
        )
