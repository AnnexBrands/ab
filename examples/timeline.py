"""Example: Timeline operations (8 methods, via api.jobs.*)."""

from examples._runner import ExampleRunner
from tests.constants import LIVE_JOB_DISPLAY_ID

runner = ExampleRunner("Timeline", env="staging")

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "get_timeline",
    lambda api: api.jobs.get_timeline(
        # TODO: capture fixture — needs job ID with active timeline
        LIVE_JOB_DISPLAY_ID,
    ),
    response_model="List[TimelineTask]",
)

runner.add(
    "create_timeline_task",
    lambda api: api.jobs.create_timeline_task(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs valid TimelineTaskCreateRequest body
        {},
    ),
    request_model="TimelineTaskCreateRequest",
    response_model="TimelineTask",
)

runner.add(
    "get_timeline_task",
    lambda api: api.jobs.get_timeline_task(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs valid task ID from get_timeline response
        "task-id-placeholder",
    ),
    response_model="TimelineTask",
)

runner.add(
    "update_timeline_task",
    lambda api: api.jobs.update_timeline_task(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs valid task ID and TimelineTaskUpdateRequest body
        "task-id-placeholder",
        {},
    ),
    request_model="TimelineTaskUpdateRequest",
    response_model="TimelineTask",
)

runner.add(
    "delete_timeline_task",
    lambda api: api.jobs.delete_timeline_task(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — destructive operation, needs valid task ID
        "task-id-placeholder",
    ),
    # no fixture — destructive operation
)

runner.add(
    "get_timeline_agent",
    lambda api: api.jobs.get_timeline_agent(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs valid task code from timeline
        "SCH",
    ),
    response_model="TimelineAgent",
)

runner.add(
    "increment_status",
    lambda api: api.jobs.increment_status(
        # TODO: capture fixture — needs job ID with incrementable status
        LIVE_JOB_DISPLAY_ID,
    ),
    request_model="IncrementStatusRequest",
    response_model="ServiceBaseResponse",
)

runner.add(
    "undo_increment_status",
    lambda api: api.jobs.undo_increment_status(
        # TODO: capture fixture — needs job ID with previously incremented status
        LIVE_JOB_DISPLAY_ID,
    ),
    request_model="IncrementStatusRequest",
    response_model="ServiceBaseResponse",
)

if __name__ == "__main__":
    runner.run()
