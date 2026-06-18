"""Regression: ShipmentBookRequest must serialize to the portal's
``BookShipmentRequest`` aliases.

The ACPortal ``BookShipmentRequest`` schema binds ``quoteOptionIndex`` (the
chosen rate option) and ``shipOutDate`` (required for non-UPS carriers). The
model used to send ``providerOptionIndex``/``shipDate``, so the portal defaulted
the option to 0 and rejected every book with "Specified provider was not set or
it is not active". These tests pin the wire shape so the bug cannot return.
"""

from __future__ import annotations

from ab.api.models.shipments import ShipmentBookRequest


def test_book_request_serializes_to_quote_option_index_and_ship_out_date():
    req = ShipmentBookRequest(quote_option_index=4, ship_out_date="2026-06-18T00:00:00")
    wire = req.model_dump(by_alias=True, exclude_none=True)
    assert wire == {"quoteOptionIndex": 4, "shipOutDate": "2026-06-18T00:00:00"}
    # The broken aliases must never reappear on this body.
    assert "providerOptionIndex" not in wire
    assert "shipDate" not in wire


def test_book_request_check_matches_confirmed_live_payload():
    # Byte-for-byte the raw dict IQ Tools confirmed live (FedEx 7094963, UPS 7040955).
    payload = ShipmentBookRequest.check({"quoteOptionIndex": 4, "shipOutDate": "2026-06-18"})
    assert payload == {"quoteOptionIndex": 4, "shipOutDate": "2026-06-18"}


def test_book_request_accepts_construction_by_alias_and_by_name():
    by_alias = ShipmentBookRequest.model_validate(
        {"quoteOptionIndex": 7, "shipOutDate": "2026-07-01T00:00:00"}
    )
    by_name = ShipmentBookRequest(quote_option_index=7, ship_out_date="2026-07-01T00:00:00")
    assert by_alias.quote_option_index == by_name.quote_option_index == 7
    assert by_alias.ship_out_date == by_name.ship_out_date == "2026-07-01T00:00:00"


def test_book_request_check_accepts_model_instance():
    # The endpoint forwards either a ShipmentBookRequest or a raw dict; both must
    # reach the wire as the corrected aliases (check() runs model_validate).
    inst = ShipmentBookRequest(quote_option_index=2, ship_out_date="2026-06-18T00:00:00")
    assert ShipmentBookRequest.check(inst) == {
        "quoteOptionIndex": 2,
        "shipOutDate": "2026-06-18T00:00:00",
    }
