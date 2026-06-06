"""Example: get and make job notes by category.

Live SDK example. Run with valid staging credentials::

    python -m examples.jobs.notes
    ex jobs.notes

Job History notes are top-level notes attached to a job UUID, not task notes
attached to a pickup/packing task. The category comes from
``api.lookup.get_by_key("JobNoteCategory")``.
"""

from __future__ import annotations

import json

from ab import ABConnectAPI
from ab.api.helpers.timeline import (
    JOB_HISTORY_CATEGORY_ID,
    JOB_HISTORY_CATEGORY_KEY,
    JOB_HISTORY_CATEGORY_NAME,
)
from ab.api.models.notes import NoteRequest
from ab.cli.formatter import format_result
from examples._capture import capture_dir, load_request, mutations_enabled
from examples.constants import TEST_JOB_DISPLAY_ID, TEST_NOTE_ID

# Honors AB_EXAMPLE_CAPTURE_DIR (feature 037) — verify harness writes to temp.
FIXTURES_DIR = capture_dir()
JOB_ID = "35e2ed80-d477-ee11-ac1c-0a15ce13c9bf"


def _save(name: str, payload) -> None:
    """Serialise *payload* (Pydantic model or non-empty list) to a fixture."""
    from pydantic import BaseModel

    if isinstance(payload, list):
        if not payload:
            print(f"  (skipped -> {FIXTURES_DIR / name}: live result is empty)")
            return
        data = [
            item.model_dump(by_alias=True, mode="json") if isinstance(item, BaseModel) else item
            for item in payload
        ]
    elif isinstance(payload, BaseModel):
        data = payload.model_dump(by_alias=True, mode="json")
    else:
        data = payload

    out = FIXTURES_DIR / name
    out.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n")
    print(f"  saved -> {out}")


def _job_history_category_id(api: ABConnectAPI) -> str:
    print(f"\n# api.lookup.get_by_key({JOB_HISTORY_CATEGORY_KEY!r})")
    categories = api.lookup.get_by_key(JOB_HISTORY_CATEGORY_KEY)
    for category in categories:
        print(f"  id={category.id!r:<40} name={category.name!r}")
        if (category.name or "").casefold() == JOB_HISTORY_CATEGORY_NAME.casefold():
            return category.id or category.value or JOB_HISTORY_CATEGORY_ID

    print(f"  {JOB_HISTORY_CATEGORY_NAME!r} was not returned; using known id {JOB_HISTORY_CATEGORY_ID}")
    return JOB_HISTORY_CATEGORY_ID


def main() -> None:
    api = ABConnectAPI()

    category_id = _job_history_category_id(api)

    print(f"\n# api.notes.list(category=[{category_id!r}], job_id={JOB_ID!r})")
    notes = api.notes.list(category=[category_id], job_id=JOB_ID)
    print(format_result(notes))
    _save("GlobalNote.json", notes)

    body = NoteRequest(
        comments="Example Job History note from examples/jobs/notes.py. Safe to delete if posted.",
        category=category_id,
        job_id=JOB_ID,
        is_important=False,
        send_notification=False,
    )
    print("\n# NoteRequest payload for api.notes.create(data=body) (validated, not sent):")
    print(json.dumps(body.model_dump(by_alias=True, exclude_none=True, mode="json"), indent=2))

    print("\n# To create that Job History note, opt in to this call:")
    print("# created = api.notes.create(data=body)")
    print("# print(format_result(created))")

    # ------------------------------------------------------------------
    # api.jobs.note.* — job-scoped note subgroup (swagger tag JobNote).
    # Renamed from the former top-level api.jobs.get_notes/get_note/
    # create_note/update_note. Each method takes job_display_id first.
    # ------------------------------------------------------------------

    # GET /job/{jobDisplayId}/note — list notes on the job (read-only).
    print(f"\n# api.jobs.note.list({TEST_JOB_DISPLAY_ID})")
    job_notes = api.jobs.note.list(TEST_JOB_DISPLAY_ID)
    print(format_result(job_notes))
    _save("JobNote.json", job_notes)

    # Prefer a discovered note id from the list above; fall back to the
    # known staging TEST_NOTE_ID so the GET runs even on an empty job.
    note_id = str(job_notes[0].id) if job_notes and job_notes[0].id else str(TEST_NOTE_ID)

    # GET /job/{jobDisplayId}/note/{id} — fetch a single note (read-only).
    print(f"\n# api.jobs.note.get({TEST_JOB_DISPLAY_ID}, {note_id!r})")
    job_note = api.jobs.note.get(TEST_JOB_DISPLAY_ID, note_id)
    print(format_result(job_note))
    _save("JobNote.json", job_note)

    # POST /job/{jobDisplayId}/note — create a note (mutates staging; guarded).
    if mutations_enabled():
        print(f"\n# api.jobs.note.create({TEST_JOB_DISPLAY_ID}, data=load_request('JobNoteCreateRequest.json'))")
        created_note = api.jobs.note.create(
            TEST_JOB_DISPLAY_ID, data=load_request("JobNoteCreateRequest.json"),
        )
        print(format_result(created_note))
        _save("JobNote.json", [created_note])

        # PUT /job/{jobDisplayId}/note/{id} — update the note just created.
        update_id = str(created_note.id) if created_note.id else note_id
        print(
            f"\n# api.jobs.note.update({TEST_JOB_DISPLAY_ID}, {update_id!r}, "
            "data=load_request('JobNoteUpdateRequest.json'))"
        )
        updated_note = api.jobs.note.update(
            TEST_JOB_DISPLAY_ID, update_id, data=load_request("JobNoteUpdateRequest.json"),
        )
        print(format_result(updated_note))
        _save("JobNote.json", updated_note)
    else:
        print("# api.jobs.note.create/update skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")


if __name__ == "__main__":
    main()
