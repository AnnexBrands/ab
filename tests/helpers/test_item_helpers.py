"""Tests for ``api.jobs.items`` — lenient parcel/freight item helpers.

Covers the lifecycle the helpers were added for: create-then-delete,
create-then-replace, and that a follow-up GET shows the expected state. Also
pins the "don't squawk" guarantee: loose kwargs the request model doesn't
declare are dropped instead of raising, and a fully-populated freight payload
validates with no ResponseModel drift warning.
"""

from __future__ import annotations

import logging
from types import SimpleNamespace
from unittest.mock import MagicMock

from ab.api.helpers.items import JobItemsHelpers
from ab.api.models.jobs import JobFreightItem, ParcelItem
from ab.api.models.shared import ServiceBaseResponse

JOB = 7009964


# ---- Parcel items ----------------------------------------------------------


def _parcel_jobs() -> MagicMock:
    jobs = MagicMock()
    jobs.parcel_items.create.side_effect = lambda jid, *, data: ParcelItem(
        id=999, description=data["description"], quantity=data.get("quantity")
    )
    jobs.parcel_items.delete.return_value = ServiceBaseResponse(success=True)
    jobs.update_item.return_value = ServiceBaseResponse(success=True)
    return jobs


def test_upsert_parcel_drops_unknown_kwargs_without_squawk():
    jobs = _parcel_jobs()
    items = JobItemsHelpers(jobs)

    created = items.upsert_parcel(JOB, description="Wood crate", weight=120.0, bogus="x", color="red")

    sent = jobs.parcel_items.create.call_args.kwargs["data"]
    assert sent == {"description": "Wood crate", "weight": 120.0}  # unknown keys gone
    assert created.id == 999


def test_create_then_delete_parcel():
    jobs = _parcel_jobs()
    items = JobItemsHelpers(jobs)

    created = items.upsert_parcel(JOB, description="Box")
    resp = items.delete_parcel(JOB, created.id)

    jobs.parcel_items.delete.assert_called_once_with(JOB, "999")
    assert resp.success is True


def test_create_then_replace_parcel_deletes_old_then_creates_new():
    jobs = _parcel_jobs()
    items = JobItemsHelpers(jobs)

    new_item = items.replace_parcel(JOB, "abc-old-id", description="Reinforced crate", weight=200.0)

    jobs.parcel_items.delete.assert_called_once_with(JOB, "abc-old-id")
    sent = jobs.parcel_items.create.call_args.kwargs["data"]
    assert sent == {"description": "Reinforced crate", "weight": 200.0}
    assert new_item.description == "Reinforced crate"


def test_update_parcel_only_sends_allowed_fields():
    jobs = _parcel_jobs()
    items = JobItemsHelpers(jobs)

    items.update_parcel(JOB, "item-id", description="Updated", quantity=3, weight=50.0, nonsense=1)

    sent = jobs.update_item.call_args.kwargs["data"]
    assert sent == {"description": "Updated", "quantity": 3, "weight": 50.0}


# ---- Freight items (stateful fake -> exercises get-merge-write) -------------


class _FakeFreightJobs:
    """Models the server's replace-all freight behaviour for round-trip tests."""

    def __init__(self, items: list[dict] | None = None) -> None:
        self._state: list[dict] = list(items or [])
        self.saved_payloads: list[list[dict]] = []

    def get(self, job_display_id: int):
        freight = [JobFreightItem.model_validate(d) for d in self._state]
        return SimpleNamespace(freight_items=freight)

    def add_freight_items(self, job_display_id: int, *, data: dict) -> None:
        payload = data["freightItems"]
        self.saved_payloads.append(payload)
        self._state = [dict(d) for d in payload]  # server replaces the whole set


def test_upsert_freight_adds_when_absent_and_get_shows_state():
    jobs = _FakeFreightJobs([])
    items = JobItemsHelpers(jobs)

    state = items.upsert_freight(JOB, freight_item_id="F1", weight=120.0, freight_description="Crate")

    assert len(state) == 1
    only = state[0]
    assert only.freight_item_id == "F1"
    assert only.item_weight == 120.0
    assert only.freight_description == "Crate"


def test_upsert_freight_updates_one_and_preserves_others():
    jobs = _FakeFreightJobs(
        [
            {"freightItemId": "F1", "itemWeight": 100.0, "freightDescription": "Crate A"},
            {"freightItemId": "F2", "itemWeight": 50.0, "freightDescription": "Crate B"},
        ]
    )
    items = JobItemsHelpers(jobs)

    state = items.replace_freight(JOB, "F1", weight=130.0)

    by_id = {f.freight_item_id: f for f in state}
    assert by_id["F1"].item_weight == 130.0
    assert by_id["F1"].freight_description == "Crate A"  # untouched field preserved
    assert by_id["F2"].item_weight == 50.0  # other item preserved
    # The save POSTed the FULL set (replace-all), not just the changed item.
    assert len(jobs.saved_payloads[-1]) == 2


def test_create_then_delete_freight_leaves_remaining_item():
    jobs = _FakeFreightJobs(
        [
            {"freightItemId": "F1", "itemWeight": 100.0},
            {"freightItemId": "F2", "itemWeight": 50.0},
        ]
    )
    items = JobItemsHelpers(jobs)

    state = items.delete_freight(JOB, "F1")

    assert [f.freight_item_id for f in state] == ["F2"]


def test_set_freight_replaces_entire_set():
    jobs = _FakeFreightJobs([{"freightItemId": "OLD", "itemWeight": 1.0}])
    items = JobItemsHelpers(jobs)

    replacement = [
        JobFreightItem(freightItemId="N1", itemWeight=10.0),
        {"freightItemId": "N2", "itemWeight": 20.0},
    ]
    state = items.set_freight(JOB, replacement)

    assert sorted(f.freight_item_id for f in state) == ["N1", "N2"]


# ---- "Don't squawk": full payload validates with no drift warning ----------


def test_full_freight_payload_validates_without_drift_warning(caplog):
    payload = {
        "itemID": "i", "jobID": "j", "jobDisplayId": "7009964", "freightItemId": "fi",
        "freightItemClassId": "fc", "jobFreightID": "jf", "quantity": 2,
        "itemLength": 10.0, "itemWidth": 5.0, "itemHeight": 4.0, "itemWeight": 100.0,
        "itemValue": 500.0, "totalWeight": 200.0, "cube": 1.2, "netCubicFeet": 1.2,
        "netCubicInches": 2000, "longestDimension": 10.0, "transportationLength": 10,
        "transportationWidth": 5, "transportationHeight": 4, "ceilingTransportationWeight": 210,
        "freightDescription": "Crate", "freightItemValue": "500", "freightItemClass": "70",
        "nmfcItem": "12345", "bolDescription": "bol", "jobFreightReport": "r",
        "createdBy": "u", "createdDate": "2026-01-01T00:00:00Z", "modifiedBy": "u",
        "modifiedDate": "2026-01-02T00:00:00Z",
    }

    with caplog.at_level(logging.WARNING, logger="ab.api.models.base"):
        model = JobFreightItem.model_validate(payload)

    assert not model.model_extra  # every server field is declared
    assert "consider adding it to the model" not in caplog.text
