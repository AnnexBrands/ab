"""Example: api.jobs.shipment — job-scoped shipment lifecycle.

Live SDK example — real call, real printed pydantic response. Authored for
feature 037 (endpoint previously had no example).

Covers the 11 job-scoped shipment routes (swagger tag ``JobShipment``): rate
quotes (read + request), booking, accessorials (read / add / remove),
origin-destination, export data (read + post), rates state, and shipment
delete. These methods moved here from the legacy ``api.shipments`` top-level
endpoint (see ``examples/_shipments.py``); the renames are
``delete_shipment`` -> ``delete``, everything else unchanged.

Read-only GETs run unguarded and capture fixtures. State-changing calls
(request_rate_quotes, book, add_accessorial, post_export_data, delete,
remove_accessorial) mutate staging and are guarded behind
``mutations_enabled()`` — set ``AB_RUN_MUTATIONS=1`` to run them.

See also: https://ab-sdk.readthedocs.io/en/latest/api/jobs/shipment.get_rate_quotes.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, mutations_enabled, save
from examples.constants import TEST_JOB_DISPLAY_ID


def main() -> None:
    api = ABConnectAPI(env="staging")

    # --- Read-only shipment data (safe to run by default) --------------

    print(f"\n# api.jobs.shipment.get_rate_quotes({TEST_JOB_DISPLAY_ID})")
    rate_quotes = api.jobs.shipment.get_rate_quotes(TEST_JOB_DISPLAY_ID)
    print(format_result(rate_quotes))
    save("RateQuote.json", rate_quotes)

    print(f"\n# api.jobs.shipment.get_accessorials({TEST_JOB_DISPLAY_ID})")
    accessorials = api.jobs.shipment.get_accessorials(TEST_JOB_DISPLAY_ID)
    print(format_result(accessorials))
    save("Accessorial.json", accessorials)

    print(f"\n# api.jobs.shipment.get_origin_destination({TEST_JOB_DISPLAY_ID})")
    origin_dest = api.jobs.shipment.get_origin_destination(TEST_JOB_DISPLAY_ID)
    print(format_result(origin_dest))
    save("ShipmentOriginDestination.json", origin_dest)

    print(f"\n# api.jobs.shipment.get_export_data({TEST_JOB_DISPLAY_ID})")
    export_data = api.jobs.shipment.get_export_data(TEST_JOB_DISPLAY_ID)
    print(format_result(export_data))
    save("ShipmentExportData.json", export_data)

    print(f"\n# api.jobs.shipment.get_rates_state({TEST_JOB_DISPLAY_ID})")
    rates_state = api.jobs.shipment.get_rates_state(TEST_JOB_DISPLAY_ID)
    print(format_result(rates_state))
    save("RatesState.json", rates_state)

    # --- State-changing calls (mutate staging — guarded) ---------------
    if not mutations_enabled():
        print(
            "\n# mutating shipment calls skipped (request_rate_quotes / book / "
            "add_accessorial / post_export_data / delete / remove_accessorial) — "
            "set AB_RUN_MUTATIONS=1 to run (mutates staging)",
        )
        return

    print(f"\n# api.jobs.shipment.request_rate_quotes({TEST_JOB_DISPLAY_ID}, data=...)")
    requested = api.jobs.shipment.request_rate_quotes(
        TEST_JOB_DISPLAY_ID, data=load_request("ShipmentRateQuoteRequest.json"),
    )
    print(format_result(requested))
    save("RateQuote.json", requested)

    print(f"\n# api.jobs.shipment.book({TEST_JOB_DISPLAY_ID}, data=...)")
    booked = api.jobs.shipment.book(TEST_JOB_DISPLAY_ID, data=load_request("ShipmentBookRequest.json"))
    print(format_result(booked))
    save("ServiceBaseResponse.json", booked)

    print(f"\n# api.jobs.shipment.add_accessorial({TEST_JOB_DISPLAY_ID}, data=...)")
    added = api.jobs.shipment.add_accessorial(
        TEST_JOB_DISPLAY_ID, data=load_request("AccessorialAddRequest.json"),
    )
    print(format_result(added))
    save("ServiceBaseResponse.json", added)

    print(f"\n# api.jobs.shipment.post_export_data({TEST_JOB_DISPLAY_ID}, data=...)")
    exported = api.jobs.shipment.post_export_data(
        TEST_JOB_DISPLAY_ID, data=load_request("ShipmentExportRequest.json"),
    )
    print(format_result(exported))
    save("ServiceBaseResponse.json", exported)

    # remove_accessorial needs an addOnId. Discover one from the live
    # accessorials list (Accessorial.id); fall back to a placeholder the
    # operator must replace with a real add-on id for a live run.
    add_on_id = str(accessorials[0].id) if accessorials and accessorials[0].id else "REPLACE_WITH_REAL_ADD_ON_ID"
    print(f"\n# api.jobs.shipment.remove_accessorial({TEST_JOB_DISPLAY_ID}, {add_on_id!r})")
    removed = api.jobs.shipment.remove_accessorial(TEST_JOB_DISPLAY_ID, add_on_id)
    print(format_result(removed))
    save("ServiceBaseResponse.json", removed)

    # delete tears down the shipment — run last.
    print(f"\n# api.jobs.shipment.delete({TEST_JOB_DISPLAY_ID})")
    deleted = api.jobs.shipment.delete(TEST_JOB_DISPLAY_ID)
    print(format_result(deleted))
    save("ServiceBaseResponse.json", deleted)


if __name__ == "__main__":
    main()
