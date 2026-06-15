#!/usr/bin/env python
"""Live reproduction: Acme pickup-and-pack agent — status-with-note + item helpers.

Part 1 — set status with note (the pickup category must NOT 403)
    Acme advances the pickup (PU) timeline category with a note. The pickup
    status change must succeed. Before the fix the SDK then issued a *redundant*
    ``POST /note`` that the agent lacked permission for, producing a spurious
    403 that masked the otherwise-successful status change. The ABConnect server
    now records the Job History note itself, so the redundant call is gone (see
    ``ab/api/helpers/timeline.py``).

Part 2 — parcel/freight item helpers (ACID, no pydantic squawk)
    Using ``api.jobs.items``: create -> get (shows state) -> replace -> delete
    for parcel items, with the existing items preserved (the parcel endpoint is
    replace-all; the SDK reads-merges-writes the full set).

Job selection
    The regression was originally reported for job 7009964, but on current
    staging that job is OUT OF Acme's scope (every call returns HTTP 400), so the
    live repro defaults to the in-scope Acme job ``ACME_JOB_DISPLAY_ID``
    (6902293). Override with a display id argument::

        python scripts/repro_acme_job_7009964.py            # 6902293 (default)
        python scripts/repro_acme_job_7009964.py 6902293

Uses the gitignored .env.acme and MUTATES the chosen Acme job by design (Acme is
a disposable test account). Each step reports a permission boundary (e.g. 403)
rather than aborting — that is itself the diagnostic.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from ab.cli.formatter import format_result  # noqa: E402
from ab.exceptions import RequestError  # noqa: E402
from examples._acme import acme_api, acme_env_available  # noqa: E402
from examples.constants import ACME_JOB_DISPLAY_ID  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")


def _step(label: str, fn):
    """Run *fn*, printing the result or a clear error (esp. HTTP status)."""
    print(f"\n# {label}")
    try:
        result = fn()
    except RequestError as exc:
        marker = "  <-- 403 (permission boundary)" if exc.status_code == 403 else ""
        print(f"  ERROR: HTTP {exc.status_code}: {exc}{marker}")
        return None
    except Exception as exc:  # noqa: BLE001 - diagnostic script
        print(f"  ERROR: {type(exc).__name__}: {exc}")
        return None
    print(format_result(result))
    return result


def part1_status_with_note(api, job: int) -> None:
    print("\n" + "=" * 72)
    print(f"Part 1: set status with note on the pickup (PU) category — job {job}")
    print("=" * 72)

    _step(f"api.jobs.timeline.response({job})  # current status (read-only)", lambda: api.jobs.timeline.response(job))

    # The pickup category status-with-note. This MUST NOT 403 for the agent.
    # schedule() advances the PU task; the server records the Job History note.
    result = _step(
        f"api.jobs.tasks.schedule({job}, start=..., end=...)  # pickup status + note",
        lambda: api.jobs.tasks.schedule(job, start="2026-06-20T09:00:00Z", end="2026-06-20T12:00:00Z"),
    )
    if result is not None:
        print("\n  RESULT: pickup status-with-note SUCCEEDED — no spurious 403 on the note.")


def part2_item_helpers(api, job: int) -> None:
    print("\n" + "=" * 72)
    print(f"Part 2: parcel/freight item helpers (ACID, no squawk) — job {job}")
    print("=" * 72)

    _step(f"api.jobs.items.list_parcel({job})  # current state", lambda: api.jobs.items.list_parcel(job))

    # Parcel: create -> get (shows state) -> replace -> delete. Existing items
    # are preserved (replace-all get-merge-write). Dimensions are required.
    created = _step(
        f"api.jobs.items.upsert_parcel({job}, description='Acme repro crate', ...)",
        lambda: api.jobs.items.upsert_parcel(
            job, description="Acme repro crate", length=24, width=18, height=12, weight=40,
            not_a_real_field="ignored",  # dropped, not raised
        ),
    )
    _step(f"api.jobs.items.list_parcel({job})  # GET shows the new item", lambda: api.jobs.items.list_parcel(job))

    if created is not None and getattr(created, "id", None) is not None:
        replaced = _step(
            f"api.jobs.items.replace_parcel({job}, {created.id!r}, ...)  # delete + create",
            lambda: api.jobs.items.replace_parcel(
                job, created.id, description="Acme repro crate (reinforced)",
                length=26, width=20, height=14, weight=60,
            ),
        )
        if replaced is not None and getattr(replaced, "id", None) is not None:
            _step(
                f"api.jobs.items.delete_parcel({job}, {replaced.id!r})",
                lambda: api.jobs.items.delete_parcel(job, replaced.id),
            )

    # Freight: get-merge-write replace (preserves the other items)
    freight = _step(f"api.jobs.items.list_freight({job})", lambda: api.jobs.items.list_freight(job))
    if freight:
        target = freight[0]
        _step(
            f"api.jobs.items.replace_freight({job}, {target.freight_item_id!r}, weight=...)",
            lambda: api.jobs.items.replace_freight(
                job, target.freight_item_id, weight=(target.item_weight or 100.0)
            ),
        )
    else:
        print("\n# freight replace skipped — job has no freight items to edit")


def main() -> int:
    if not acme_env_available():
        print(
            "Acme credentials not found. Create .env.acme (gitignored) with the "
            "ABCONNECT_USERNAME/PASSWORD for the Acme staging agent. See "
            "examples/_acme.py.",
            file=sys.stderr,
        )
        return 2

    job = int(sys.argv[1]) if len(sys.argv) > 1 else ACME_JOB_DISPLAY_ID

    try:
        api = acme_api()
    except Exception as exc:  # noqa: BLE001 - surface auth/config errors plainly
        print(f"Could not build Acme client: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    print(f"Authenticated user: {api._settings.username} | env: {api._settings.environment} | job: {job}")
    part1_status_with_note(api, job)
    part2_item_helpers(api, job)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
