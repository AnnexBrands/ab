"""Example: api.jobs.form — job-scoped form generation (shipment plans).

Live SDK example — real call, real printed pydantic response. Authored for
feature 037 (endpoint previously had no example).

``api.jobs.form`` exposes 15 routes; all but :meth:`shipments` return PDF bytes
(no JSON fixture). :meth:`shipments` returns ``List[FormsShipmentPlan]`` whose
``job_shipment_id`` drives the BOL routes — so it is the canonical, fixture-backed
read for this group.

See also: https://ab-sdk.readthedocs.io/en/latest/api/jobs.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import save
from examples.constants import TEST_JOB_DISPLAY_ID


def main() -> None:
    api = ABConnectAPI(env="staging")

    # GET /job/{jobDisplayId}/form/shipments — JSON shipment plans (read-only).
    print(f"\n# api.jobs.form.shipments({TEST_JOB_DISPLAY_ID})")
    result = api.jobs.form.shipments(TEST_JOB_DISPLAY_ID)
    print(format_result(result))
    save("FormsShipmentPlan.json", result)


if __name__ == "__main__":
    main()
