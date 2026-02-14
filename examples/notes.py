"""Example: Notes operations (4 methods, via api.jobs.*)."""

from examples._runner import ExampleRunner

runner = ExampleRunner("Notes", env="staging")

LIVE_JOB_DISPLAY_ID = 2000000

# ── Needs request data ───────────────────────────────────────────────

runner.add(
    "get_notes",
    lambda api: api.jobs.get_notes(
        # TODO: capture fixture — needs job ID with existing notes
        LIVE_JOB_DISPLAY_ID,
    ),
    response_model="List[JobNote]",
)

runner.add(
    "create_note",
    lambda api: api.jobs.create_note(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs valid JobNoteCreateRequest body
        {},
    ),
    request_model="JobNoteCreateRequest",
    response_model="JobNote",
)

runner.add(
    "get_note",
    lambda api: api.jobs.get_note(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs valid note ID from get_notes response
        "note-id-placeholder",
    ),
    response_model="JobNote",
)

runner.add(
    "update_note",
    lambda api: api.jobs.update_note(
        LIVE_JOB_DISPLAY_ID,
        # TODO: capture fixture — needs valid note ID and JobNoteUpdateRequest body
        "note-id-placeholder",
        {},
    ),
    request_model="JobNoteUpdateRequest",
    response_model="JobNote",
)

if __name__ == "__main__":
    runner.run()
