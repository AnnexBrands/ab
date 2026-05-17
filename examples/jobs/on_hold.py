"""Example: ``api.jobs.on_hold`` -- create / assign / email / resolve.

Live SDK example. Run with valid staging credentials in ``.env.staging``::

    python -m examples.jobs.on_hold

The script performs the full on-hold lifecycle on
``TEST_JOB_DISPLAY_ID``, escalating the hold to ``TEST_USER_ID``:

1. Discovery: list any existing holds on the job, then look up
   ``TEST_USER_ID`` as a follow-up user to confirm the contact has an
   email.
2. Discovery: source ``reasonId`` and ``responsiblePartyTypeId`` from
   ``api.lookup.get_by_key(...)`` -- both are required by swagger.
3. Create: ``api.jobs.on_hold.create(...)`` with
   ``assignedToId=TEST_USER_ID``.
4. Notify: build a ``SendEmailRequest`` and call
   ``api.jobs.email.send(...)`` so the assignee learns about the hold
   out-of-band. (Whether the on-hold POST itself triggers a
   notification is server-side configuration; this example sends one
   explicitly.)
5. Resolve: ``api.jobs.on_hold.resolve(...)`` -- swagger uses the same
   ``SaveOnHoldRequest`` schema as create, so ``reasonId`` and
   ``responsiblePartyTypeId`` are still required (carry them forward).

Forward references
------------------

* :meth:`api.lookup.get_by_key("OnHoldReason") <ab.api.endpoints.lookup.LookupEndpoint.get_by_key>`
  -> ``LookupValue.id`` -> :attr:`SaveOnHoldRequest.reason_id`.
* :meth:`api.lookup.get_by_key("ResponsibleParty") <ab.api.endpoints.lookup.LookupEndpoint.get_by_key>`
  -> ``LookupValue.id`` -> :attr:`SaveOnHoldRequest.responsible_party_type_id`.
* ``OnHoldUser.contact_id`` (output of
  :meth:`api.jobs.on_hold.get_followup_user <ab.api.endpoints.jobs.on_hold.JobOnHoldEndpoint.get_followup_user>`)
  -> :attr:`SaveOnHoldRequest.assigned_to_id` (**int**, not UUID).
* ``OnHoldUser.email`` -> :attr:`SendEmailRequest.to`.
* :attr:`SaveOnHoldResponse.on_hold_id` -> path param for
  :meth:`api.jobs.on_hold.resolve <ab.api.endpoints.jobs.on_hold.JobOnHoldEndpoint.resolve>`.

Swagger vs. live behaviour
--------------------------

* The pre-realignment SDK ``SaveOnHoldRequest`` had hand-authored fields
  (``reason``, ``description``, ``followUpContactId: str``,
  ``followUpDate: str``) that did not match the swagger ``SaveOnHoldRequest``
  shape. The model was realigned to swagger -- required fields are now
  ``reasonId`` (UUID) and ``responsiblePartyTypeId`` (UUID), and the
  assignee field is ``assignedToId`` (int).
* Swagger uses the **same** ``SaveOnHoldRequest`` schema for create,
  update, and resolve. The legacy ``ResolveOnHoldRequest`` is now an
  alias of :class:`SaveOnHoldRequest`.

See also: https://ab-sdk.readthedocs.io/en/latest/api/jobs.html#api-jobs-on-hold
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from ab import ABConnectAPI
from ab.api.models.jobs import SaveOnHoldRequest, SendEmailRequest
from ab.cli.formatter import format_result

from examples.constants import TEST_JOB_DISPLAY_ID, TEST_USER_ID

FIXTURES_DIR = Path(__file__).resolve().parents[2] / "tests" / "fixtures"


def _save(name: str, payload) -> None:
    """Serialise *payload* to ``tests/fixtures/{name}`` (no-op on empty lists)."""
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
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"  saved -> {out}")


def _pick_lookup_uuid(api, key: str) -> str:
    """Resolve a master-constant key to its first ``LookupValue.id``.

    ``api.lookup.get_by_key()`` returns ``List[LookupValue]`` whose ``.id``
    is the UUID feeding the on-hold request. Mirrors the
    ``examples/notes.py`` pattern -- ``.value`` is null on referCategory
    and on most master-constant lookups; the UUID lives in ``.id``.
    """
    values = api.lookup.get_by_key(key)
    if not values:
        raise SystemExit(f"No values returned for lookup key {key!r}; cannot continue.")
    print(f"  {key}: chose id={values[0].id!r} name={values[0].name!r}  (of {len(values)} options)")
    return values[0].id


def main() -> None:
    api = ABConnectAPI(env="staging")

    # --- Step 1: list existing on-holds on the job ---------------------
    print(f"\n# api.jobs.on_hold.list({TEST_JOB_DISPLAY_ID})")
    existing = api.jobs.on_hold.list(TEST_JOB_DISPLAY_ID)
    print(format_result(existing))
    _save("ExtendedOnHoldInfo.json", existing)

    # --- Step 2a: confirm TEST_USER_ID has an email --------------------
    print(f"\n# api.jobs.on_hold.get_followup_user({TEST_JOB_DISPLAY_ID}, {TEST_USER_ID})")
    follow_up = api.jobs.on_hold.get_followup_user(TEST_JOB_DISPLAY_ID, str(TEST_USER_ID))
    print(format_result(follow_up))
    _save("OnHoldUser.json", [follow_up])
    if not follow_up.email:
        print(
            "  WARNING: follow-up user has no email on file. The hold is created "
            "but the notification email step will be skipped.",
        )

    # --- Step 2b: discover the required lookup UUIDs -------------------
    # Swagger requires reasonId + responsiblePartyTypeId. The keys below
    # are the master-constant keys used elsewhere in the platform; adjust
    # the chosen value if a more specific reason is desired.
    print("\n# api.lookup.get_by_key('OnHoldReason') / 'ResponsibleParty'")
    reason_id = _pick_lookup_uuid(api, "OnHoldReason")
    responsible_party_type_id = _pick_lookup_uuid(api, "ResponsibleParty")

    # --- Step 3: create the hold, assigned to TEST_USER_ID -------------
    now = datetime.now(timezone.utc).replace(microsecond=0)
    body = SaveOnHoldRequest(
        reasonId=reason_id,
        responsiblePartyTypeId=responsible_party_type_id,
        comment=f"Hold created by examples/jobs/on_hold.py at {now.isoformat()}; assigned to user {TEST_USER_ID}.",
        assignedToId=TEST_USER_ID,
        dueDate=now + timedelta(days=2),
        startDate=now,
    )

    print(
        f"\n# api.jobs.on_hold.create({TEST_JOB_DISPLAY_ID}, data=SaveOnHoldRequest(..., assignedToId={TEST_USER_ID}))",
    )
    print("  payload:")
    print(json.dumps(body.model_dump(by_alias=True, exclude_none=True, mode="json"), indent=2))

    created = api.jobs.on_hold.create(TEST_JOB_DISPLAY_ID, data=body)
    print(format_result(created))
    on_hold_id = created.on_hold_id
    if not on_hold_id:
        raise SystemExit("Create did not return on_hold_id; cannot continue.")

    # --- Step 4: email the assignee ------------------------------------
    if follow_up.email:
        email_body = SendEmailRequest(
            to=[follow_up.email],
            subject=f"Job {TEST_JOB_DISPLAY_ID}: on-hold escalated to you",
            body=(
                f"Hi {follow_up.full_name or 'there'},\n\n"
                f"On-hold record #{on_hold_id} on job {TEST_JOB_DISPLAY_ID} has been assigned to you. "
                "Please review and resolve when ready.\n"
            ),
        )
        print(f"\n# api.jobs.email.send({TEST_JOB_DISPLAY_ID}, data=SendEmailRequest(to={follow_up.email!r}, ...))")
        api.jobs.email.send(TEST_JOB_DISPLAY_ID, data=email_body)
        print("  (sent)")

    # --- Step 5: resolve the hold --------------------------------------
    # The resolve route shares SaveOnHoldRequest with create -- reasonId and
    # responsiblePartyTypeId have to be carried forward.
    resolved_at = datetime.now(timezone.utc).replace(microsecond=0)
    resolve_body = SaveOnHoldRequest(
        reasonId=reason_id,
        responsiblePartyTypeId=responsible_party_type_id,
        comment="Resolved by examples/jobs/on_hold.py walkthrough.",
        resolvedDate=resolved_at,
    )
    print(f"\n# api.jobs.on_hold.resolve({TEST_JOB_DISPLAY_ID}, {on_hold_id!r}, data=SaveOnHoldRequest(..., resolvedDate=...))")
    resolution = api.jobs.on_hold.resolve(TEST_JOB_DISPLAY_ID, on_hold_id, data=resolve_body)
    print(format_result(resolution))


if __name__ == "__main__":
    main()
