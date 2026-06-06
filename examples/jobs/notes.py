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
from examples._capture import capture_dir

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


if __name__ == "__main__":
    main()
