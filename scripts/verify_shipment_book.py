#!/usr/bin/env python
"""Live verify for the ShipmentBookRequest alias fix (0.1.6).

Proves the typed ``api.jobs.shipment.book()`` path now serializes to the
portal's ``BookShipmentRequest`` aliases — ``quoteOptionIndex`` /
``shipOutDate`` — exactly mirroring the raw dict IQ Tools confirmed live on
FedEx job 7094963 and UPS job 7040955.

SAFE BY DEFAULT
---------------
Without ``--book`` this only constructs the typed request and prints the wire
payload (``model.check()``) — no network, no auth, no carrier call.

Booking a shipment hits a real carrier API (charges, labels, PRO) and is not
reversible; the two reference jobs were already booked via the workaround, so a
re-book will likely come back ``success=False`` ("already booked") rather than a
fresh PRO. Pass a *fresh, ready-to-ship* job id for a clean positive result.

Usage
-----
    # dry run — print the exact payload the typed call will send (no network)
    python scripts/verify_shipment_book.py

    # live book (requires BOTH the flag and the env guard)
    AB_RUN_MUTATIONS=1 python scripts/verify_shipment_book.py --book \
        --env production --job 7094963 --option 4 --ship-out-date 2026-06-18
"""

from __future__ import annotations

import argparse
import os
from datetime import date

from ab.api.models.shipments import ShipmentBookRequest

# Jobs IQ Tools booked successfully with the raw-dict workaround.
REFERENCE_JOBS = {"fedex": 7094963, "ups": 7040955}


def _payload(option_index: int, ship_out_date: str) -> dict:
    req = ShipmentBookRequest(quote_option_index=option_index, ship_out_date=ship_out_date)
    # .check() is exactly what BaseEndpoint._request() puts on the wire.
    return ShipmentBookRequest.check(req)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--job", type=int, action="append", help="job display id (repeatable)")
    parser.add_argument("--option", type=int, default=4, help="quoteOptionIndex (default 4)")
    parser.add_argument("--ship-out-date", default=date.today().isoformat(), help="ISO ship-out date")
    parser.add_argument("--env", default="production", help="staging | production")
    parser.add_argument("--env-file", default=None, help="explicit env file path")
    parser.add_argument("--book", action="store_true", help="actually POST the book (needs AB_RUN_MUTATIONS=1)")
    args = parser.parse_args()

    jobs = args.job or list(REFERENCE_JOBS.values())
    payload = _payload(args.option, args.ship_out_date)

    print("Typed ShipmentBookRequest wire payload (what hits /shipment/book):")
    print(f"  {payload}")
    print("Confirmed-live raw dict (IQ Tools): {'quoteOptionIndex': 4, 'shipOutDate': '<date>'}")
    assert "providerOptionIndex" not in payload and "shipDate" not in payload
    print("  ✓ uses quoteOptionIndex/shipOutDate; no providerOptionIndex/shipDate\n")

    if not args.book:
        print("Dry run (no --book): not contacting the API. Add --book + AB_RUN_MUTATIONS=1 to book.")
        return

    if os.environ.get("AB_RUN_MUTATIONS") != "1":
        raise SystemExit("Refusing to book: set AB_RUN_MUTATIONS=1 to authorize a real carrier booking.")

    from ab import ABConnectAPI

    api = ABConnectAPI(env=args.env, env_file=args.env_file)
    for job in jobs:
        print(f"\n# POST /job/{job}/shipment/book  data={payload}")
        resp = api.jobs.shipment.book(
            job,
            data=ShipmentBookRequest(quote_option_index=args.option, ship_out_date=args.ship_out_date),
        )
        success = getattr(resp, "success", None)
        pro = getattr(resp, "shipment_id", None) or getattr(resp, "shipment_accept_identifier", None)
        docs = getattr(resp, "documents", None)
        err = getattr(resp, "error_message", None)
        print(f"  success={success!r}  shipment/pro={pro!r}  documents={bool(docs)}  error={err!r}")


if __name__ == "__main__":
    main()
