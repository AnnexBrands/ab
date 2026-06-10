"""Example: Notes operations.

Live SDK example -- no runner indirection. Run with valid staging
credentials in ``.env.staging`` to hit the real API and (optionally) save
captured responses as fixtures under ``tests/fixtures/``.

Operator-in-the-loop sequence
-----------------------------

Two pieces of information have to be discovered before ``create`` will
work. Follow them in order:

1. **Category UUID** -- ``NoteRequest.category`` is **required** by
   swagger. Call ``api.lookup.get_refer_categories()`` and pick a
   ``LookupValue.id`` whose ``name`` matches the category you want
   (e.g. ``"Internet"``). Note: ``LookupValue.value`` is null for
   ``referCategory`` -- the UUID lives in ``.id``.
2. **Assigned users (optional)** -- call
   ``api.notes.suggest_users(query, company_id=...)`` to find
   ``SuggestedUser`` rows; their ``id`` feeds
   ``NoteRequest.assigned_users[].id``. The ``company_id`` (or
   ``job_franchisee_id``) is required in practice -- without it the API
   returns ``[]``.

Then call ``api.notes.create(data=NoteRequest(...))``.

Forward references
------------------

* ``LookupValue.id`` (output of ``GET /lookup/referCategory``) ->
  ``NoteRequest.category`` (input to ``POST /note``).
* ``SuggestedUser.id`` (output of ``GET /note/suggestUsers``) ->
  ``NoteRequest.assigned_users[].id``.
* ``GlobalNote.note_id`` (output of ``GET /note``) -> path parameter for
  ``PUT /note/{id}``.

Swagger vs. live behaviour
--------------------------

* The swagger contract uses **one** schema (``NoteModel``) for both
  ``POST /note`` and ``PUT /note/{id}``. The SDK reflects this with a
  single :class:`NoteRequest`; the legacy names
  ``GlobalNoteCreateRequest`` / ``GlobalNoteUpdateRequest`` remain as
  aliases. Practical consequence: **partial updates are not supported by
  this endpoint** -- ``PUT`` requires ``comments`` + ``category`` just
  like ``POST``.
* ``GET /note`` requires **at least one filter** (one of ``category``,
  ``jobId``, ``contactId``, ``companyId``) at the live API, even though
  swagger marks them all optional. A bare ``GET /note`` returns HTTP 400.
  This example always passes ``company_id`` to keep the call valid.
* ``GET /note/suggestUsers`` returns ``[]`` without ``CompanyId`` or
  ``JobFranchiseeId``, even though swagger marks both optional. The
  example always passes ``company_id`` so the chain actually produces
  rows.
* The server returns the field as ``modifiyDate`` (sic -- the typo is on
  the server side). The SDK aliases it; the Python attribute is
  ``modified_date``.

See also: https://ab-sdk.readthedocs.io/en/latest/api/notes.html
"""

from __future__ import annotations

import json

from ab import ABConnectAPI
from ab.api.models.notes import NoteRequest, SuggestedUser
from ab.cli.formatter import format_result
from examples._capture import mutations_enabled, save
from examples.constants import TEST_COMPANY_ID, TEST_NOTE_ID


def main() -> None:
    api = ABConnectAPI(env="staging")

    # Output formatting uses ``ab.cli.formatter.format_result`` so this
    # example and ``abs notes …`` produce identical layouts.

    # --- Step 1: list current notes -------------------------------------
    # NB: live API requires at least one filter; bare list() returns 400.
    print(f"\n# api.notes.list(company_id={TEST_COMPANY_ID!r})")
    notes = api.notes.list(company_id=TEST_COMPANY_ID)
    print(format_result(notes))
    save("GlobalNote.json", notes)

    # --- Step 2: discover a category UUID -------------------------------
    # NB: for /lookup/referCategory the UUID lives in `.id` (not `.value`).
    print("\n# api.lookup.get_refer_categories()  (sourcing NoteRequest.category)")
    categories = api.lookup.get_refer_categories()
    for c in categories[:5]:
        print(f"  id={c.id!r:<40} name={c.name!r}")
    save("LookupValue.json", categories)
    if not categories:
        raise SystemExit("No note categories available on staging — cannot continue.")
    category_uuid = categories[0].id

    # --- Step 3: suggest users for mentions -----------------------------
    # NB: live API returns [] without company_id (or job_franchisee_id).
    print(f"\n# api.notes.suggest_users('br', company_id={TEST_COMPANY_ID!r})")
    suggestions = api.notes.suggest_users("br", company_id=TEST_COMPANY_ID)
    print(format_result(suggestions))
    save("SuggestedUser.json", suggestions)

    # --- Step 4: build a NoteRequest (does not POST) --------------------
    # The example file deliberately does not call create() so re-running
    # is idempotent. Uncomment the create() block below to actually post.
    body = NoteRequest(
        comments="Example note from examples/notes.py — safe to delete.",
        category=category_uuid,
        is_important=False,
        is_completed=False,
        company_id=TEST_COMPANY_ID,
        send_notification=False,
        assigned_users=[
            SuggestedUser(id=s.id, fullName=s.full_name) for s in suggestions[:1]
        ] if suggestions else None,
    )
    print("\n# NoteRequest payload (validated, not sent):")
    print(json.dumps(body.model_dump(by_alias=True, exclude_none=True), indent=2))

    # --- Step 5: create the note (mutates staging) ----------------------
    # POST /note. Guarded: set AB_RUN_MUTATIONS=1 to actually run. Capture
    # the response as a single-row GlobalNote fixture.
    if mutations_enabled():
        print("\n# api.notes.create(data=body)")
        created = api.notes.create(data=body)
        print(format_result(created))
        save("GlobalNote.json", [created])  # overwrite with a single-row fixture
    else:
        print("\n# api.notes.create skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")

    # --- Step 6: update the note (mutates staging) ----------------------
    # PUT /note/{id} uses the same NoteRequest schema -- comments + category
    # remain required (partial updates unsupported). The note id is a path
    # param passed positionally as a str.
    if mutations_enabled():
        update_body = NoteRequest(
            comments="Updated: pickup time confirmed at 1700 PST.",
            category=category_uuid,
            is_completed=True,
        )
        print(f"\n# api.notes.update({str(TEST_NOTE_ID)!r}, data=update_body)")
        updated = api.notes.update(str(TEST_NOTE_ID), data=update_body)
        print(format_result(updated))
        save("GlobalNote.json", [updated])
    else:
        print("\n# api.notes.update skipped — set AB_RUN_MUTATIONS=1 to run (mutates staging)")


if __name__ == "__main__":
    main()
