"""Example: Notes operations (4 methods, via api.jobs.*)."""

from examples._runner import ExampleRunner
from tests.constants import LIVE_JOB_DISPLAY_ID

runner = ExampleRunner("Notes", env="staging")

# ── Uses request fixtures ────────────────────────────────────────────

runner.add(
    "get_notes",
    lambda api: api.jobs.get_notes(LIVE_JOB_DISPLAY_ID),
    response_model="List[JobNote]",
)

runner.add(
    "create_note",
    lambda api, data=None: api.jobs.create_note(LIVE_JOB_DISPLAY_ID, data or {}),
    request_model="JobNoteCreateRequest",
    request_fixture_file="JobNoteCreateRequest.json",
    response_model="JobNote",
)

runner.add(
    "get_note",
    lambda api: api.jobs.get_note(LIVE_JOB_DISPLAY_ID, "note-id-placeholder"),
    response_model="JobNote",
)

runner.add(
    "update_note",
    lambda api, data=None: api.jobs.update_note(LIVE_JOB_DISPLAY_ID, "note-id-placeholder", data or {}),
    request_model="JobNoteUpdateRequest",
    request_fixture_file="JobNoteUpdateRequest.json",
    response_model="JobNote",
)

if __name__ == "__main__":
    runner.run()
