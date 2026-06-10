"""MasterConstantKey enum + lookup.get_by_key key normalization."""

from __future__ import annotations

from unittest.mock import MagicMock

from ab.api.endpoints.lookup import LookupEndpoint
from ab.api.models.enums import MasterConstantKey


def test_known_wire_values():
    assert MasterConstantKey.ON_HOLD_REASON.value == "OnHoldReason"
    # The DB typo is the real wire value — must never be "corrected".
    assert MasterConstantKey.ON_HOLD_RESOLVED_CODE.value == "OnHoldRecolvedCode"
    # Space-containing key.
    assert MasterConstantKey.JOB_MANAGEMENT_STATUS.value == "Job Management Status"


def test_get_by_key_accepts_enum_and_str():
    client = MagicMock()
    client.request.return_value = []
    ep = LookupEndpoint(client)

    ep.get_by_key(MasterConstantKey.ON_HOLD_RESOLVED_CODE)
    path_enum = client.request.call_args.args[1]
    ep.get_by_key("OnHoldRecolvedCode")
    path_str = client.request.call_args.args[1]

    assert path_enum == path_str == "/lookup/OnHoldRecolvedCode"
