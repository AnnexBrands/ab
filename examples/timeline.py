"""Example: Timeline operations (8 methods, via api.jobs.*)."""

from examples._runner import ExampleRunner
from tests.constants import LIVE_JOB_DISPLAY_ID

runner = ExampleRunner("Timeline", env="staging")

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "get_timeline",
    lambda api: api.jobs.get_timeline(LIVE_JOB_DISPLAY_ID),
    response_model="List[TimelineTask]",
)

runner.add(
    "create_timeline_task",
    lambda api, data=None: api.jobs.create_timeline_task(LIVE_JOB_DISPLAY_ID, data or {}),
    request_model="TimelineTaskCreateRequest",
    request_fixture_file="TimelineTaskCreateRequest.json",
    response_model="TimelineTask",
)

runner.add(
    "get_timeline_task",
    lambda api: api.jobs.get_timeline_task(LIVE_JOB_DISPLAY_ID, "task-id-placeholder"),
    response_model="TimelineTask",
)

runner.add(
    "update_timeline_task",
    lambda api, data=None: api.jobs.update_timeline_task(LIVE_JOB_DISPLAY_ID, "task-id-placeholder", data or {}),
    request_model="TimelineTaskUpdateRequest",
    request_fixture_file="TimelineTaskUpdateRequest.json",
    response_model="TimelineTask",
)

runner.add(
    "delete_timeline_task",
    lambda api: api.jobs.delete_timeline_task(LIVE_JOB_DISPLAY_ID, "task-id-placeholder"),
)

runner.add(
    "get_timeline_agent",
    lambda api: api.jobs.get_timeline_agent(LIVE_JOB_DISPLAY_ID, "SCH"),
    response_model="TimelineAgent",
)

runner.add(
    "increment_status",
    lambda api: api.jobs.increment_status(LIVE_JOB_DISPLAY_ID),
    request_model="IncrementStatusRequest",
    response_model="ServiceBaseResponse",
)

runner.add(
    "undo_increment_status",
    lambda api: api.jobs.undo_increment_status(LIVE_JOB_DISPLAY_ID),
    request_model="IncrementStatusRequest",
    response_model="ServiceBaseResponse",
)

if __name__ == "__main__":
    runner.run()
