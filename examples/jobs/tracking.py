"""Example: api.jobs.tracking — job-scoped shipment tracking (3 GETs).

Live SDK example — real call, real printed pydantic response. Authored for
feature 037 (endpoint previously had no example).

Both routes are read-only (``GET``) and take explicit positional/keyword args
(Constitution IX), so the calls use real inline values rather than a request
fixture. ``v3`` lives under a separate ``/v3/`` controller and adds a
``historyAmount`` path param (defaults to 10).

See also: https://ab-sdk.readthedocs.io/en/latest/api/jobs.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import save
from examples.constants import TEST_JOB_DISPLAY_ID


def main() -> None:
    api = ABConnectAPI(env="staging")

    # GET /job/{jobDisplayId}/tracking (read-only)
    print(f"\n# api.jobs.tracking.get({TEST_JOB_DISPLAY_ID})")
    tracking_info = api.jobs.tracking.get(TEST_JOB_DISPLAY_ID)
    print(format_result(tracking_info))
    save("TrackingInfo.json", tracking_info)

    # GET /v3/job/{jobDisplayId}/tracking/{historyAmount} (read-only)
    print(f"\n# api.jobs.tracking.v3({TEST_JOB_DISPLAY_ID}, history_amount=10)")
    result = api.jobs.tracking.v3(TEST_JOB_DISPLAY_ID, history_amount=10)
    print(format_result(result))
    save("TrackingInfoV3.json", result)

    # GET /job/{jobDisplayId}/tracking/shipment/{proNumber} (read-only)
    # The PRO number comes from the job's own tracking info above.
    pro_number = tracking_info.pro_number
    if pro_number:
        print(f"\n# api.jobs.tracking.shipment({TEST_JOB_DISPLAY_ID}, {pro_number!r})")
        result = api.jobs.tracking.shipment(TEST_JOB_DISPLAY_ID, pro_number)
        print(format_result(result))
        save("ShipmentTrackingDetails.json", result)
    else:
        print("\n# api.jobs.tracking.shipment skipped — job tracking has no PRO number")


if __name__ == "__main__":
    main()
