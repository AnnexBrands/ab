"""Unit tests for contact endpoint helpers and CLI wiring."""

from __future__ import annotations

import json
import sys
from unittest.mock import MagicMock, patch

from ab.api.endpoints.contacts import ContactsEndpoint
from ab.api.models.contacts import ContactSimple
from ab.cli.discovery import discover_endpoints_from_class


def test_get_did_resolves_display_id_then_gets_contact():
    acportal = MagicMock(name="acportal")
    resolver = MagicMock(name="resolver")
    resolved_id = "11111111-1111-1111-1111-111111111111"
    resolver.resolve.return_value = resolved_id
    acportal.request.return_value = {
        "id": resolved_id,
        "contactDisplayId": "1308994",
        "fullName": "Test Contact",
    }

    contacts = ContactsEndpoint(acportal, resolver)
    result = contacts.get_did("1308994")

    resolver.resolve.assert_called_once_with("1308994")
    acportal.request.assert_called_once_with("GET", f"/contacts/{resolved_id}")
    assert isinstance(result, ContactSimple)
    assert result.id == resolved_id


def test_cli_discovery_includes_get_did_helper():
    registry = discover_endpoints_from_class()
    contacts = registry["contacts"]
    method = next((m for m in contacts.methods if m.name == "get_did"), None)

    assert method is not None
    assert [p.name for p in method.positional_params] == ["contact_did"]
    assert method.route is None


def test_cli_dispatch_calls_contacts_get_did(capsys):
    from ab.cli.__main__ import main

    api = MagicMock()
    api.contacts.get_did.return_value = ContactSimple(
        id="11111111-1111-1111-1111-111111111111",
        contactDisplayId="1308994",
        fullName="Test Contact",
    )

    with patch("ab.cli.__main__._create_api", return_value=api):
        with patch.object(sys, "argv", ["ab", "contacts", "get_did", "1308994", "--json"]):
            main()

    api.contacts.get_did.assert_called_once_with("1308994")
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["id"] == "11111111-1111-1111-1111-111111111111"
    assert data["contactDisplayId"] == "1308994"
