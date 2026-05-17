"""Wire-level tests for the ``api.jobs.on_hold`` create/assign/email/resolve chain.

Mirrors the workflow in ``examples/jobs/on_hold.py``. Uses a mocked
:class:`~ab.http.HttpClient` to assert:

* the routes hit by each step,
* alias-key serialisation of ``SaveOnHoldRequest`` (swagger camelCase),
* required-field enforcement (``reasonId`` + ``responsiblePartyTypeId``),
* the forward references ``LookupValue.id -> SaveOnHoldRequest.reason_id``
  and ``OnHoldUser.email -> SendEmailRequest.to``,
* the resolve route reuses :class:`SaveOnHoldRequest` (not a separate
  ``ResolveOnHoldRequest`` schema).
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from ab.api.endpoints.jobs import JobsEndpoint
from ab.api.models.jobs import (
    ResolveOnHoldRequest,
    SaveOnHoldRequest,
    SendEmailRequest,
)


@pytest.fixture
def acportal():
    return MagicMock(name="acportal")


@pytest.fixture
def jobs(acportal):
    return JobsEndpoint(acportal, MagicMock(name="abc"), MagicMock(name="resolver"))


# ---------------------------------------------------------------------------
# Model contract
# ---------------------------------------------------------------------------


class TestSaveOnHoldRequestContract:
    def test_required_fields(self):
        with pytest.raises(Exception):
            SaveOnHoldRequest.model_validate({})
        # Both swagger-required fields satisfy validation.
        SaveOnHoldRequest(reasonId="r", responsiblePartyTypeId="p")

    def test_assigned_to_id_is_int(self):
        m = SaveOnHoldRequest(reasonId="r", responsiblePartyTypeId="p", assignedToId=206)
        assert m.assigned_to_id == 206
        with pytest.raises(Exception):
            SaveOnHoldRequest(reasonId="r", responsiblePartyTypeId="p", assignedToId="not-int")

    def test_alias_serialisation(self):
        m = SaveOnHoldRequest(
            reasonId="r", responsiblePartyTypeId="p", comment="x", assignedToId=206,
        )
        out = m.model_dump(by_alias=True, exclude_none=True, mode="json")
        assert out == {
            "reasonId": "r",
            "responsiblePartyTypeId": "p",
            "comment": "x",
            "assignedToId": 206,
        }

    def test_resolve_alias_identity(self):
        assert ResolveOnHoldRequest is SaveOnHoldRequest


# ---------------------------------------------------------------------------
# Wire-level — list + followup discovery
# ---------------------------------------------------------------------------


class TestDiscoverySteps:
    def test_list_hits_job_onhold_route(self, jobs, acportal):
        acportal.request.return_value = []
        jobs.on_hold.list(42)
        args, _ = acportal.request.call_args
        assert args == ("GET", "/job/42/onhold")

    def test_get_followup_user_binds_contact_id(self, jobs, acportal):
        acportal.request.return_value = {"contactId": 206, "fullName": "Brett", "email": "b@x.co"}
        user = jobs.on_hold.get_followup_user(42, "206")
        args, _ = acportal.request.call_args
        assert args == ("GET", "/job/42/onhold/followupuser/206")
        # Forward reference: email feeds SendEmailRequest.to
        msg = SendEmailRequest(to=[user.email], subject="x", body="y")
        assert msg.to == ["b@x.co"]


# ---------------------------------------------------------------------------
# Wire-level — create with assignedToId
# ---------------------------------------------------------------------------


class TestCreateOnHold:
    def test_create_sends_camelcase_body(self, jobs, acportal):
        acportal.request.return_value = {"onHoldId": "5001", "status": "Open"}
        body = SaveOnHoldRequest(
            reasonId="r-uuid",
            responsiblePartyTypeId="p-uuid",
            comment="Awaiting docs",
            assignedToId=206,
        )
        out = jobs.on_hold.create(42, data=body)
        args, kwargs = acportal.request.call_args
        assert args == ("POST", "/job/42/onhold")
        assert kwargs["json"] == {
            "reasonId": "r-uuid",
            "responsiblePartyTypeId": "p-uuid",
            "comment": "Awaiting docs",
            "assignedToId": 206,
        }
        assert out.on_hold_id == "5001"

    def test_create_rejects_missing_required_fields(self, jobs):
        with pytest.raises(Exception):
            jobs.on_hold.create(42, data={"comment": "no required fields"})


# ---------------------------------------------------------------------------
# Wire-level — email the assignee
# ---------------------------------------------------------------------------


class TestEmailAssignee:
    def test_send_posts_camelcase_body(self, jobs, acportal):
        acportal.request.return_value = None
        body = SendEmailRequest(to=["b@x.co"], subject="Hold for you", body="Please review")
        jobs.email.send(42, data=body)
        args, kwargs = acportal.request.call_args
        assert args == ("POST", "/job/42/email")
        assert kwargs["json"] == {"to": ["b@x.co"], "subject": "Hold for you", "body": "Please review"}


# ---------------------------------------------------------------------------
# Wire-level — resolve uses SaveOnHoldRequest, binds onHoldId
# ---------------------------------------------------------------------------


class TestResolveOnHold:
    def test_resolve_route_binds_on_hold_id(self, jobs, acportal):
        acportal.request.return_value = {"resolved": True, "status": "Resolved"}
        body = SaveOnHoldRequest(
            reasonId="r-uuid",
            responsiblePartyTypeId="p-uuid",
            resolvedDate="2026-05-14T15:30:00",
        )
        jobs.on_hold.resolve(42, "5001", data=body)
        args, kwargs = acportal.request.call_args
        assert args == ("PUT", "/job/42/onhold/5001/resolve")
        assert kwargs["json"]["reasonId"] == "r-uuid"
        assert kwargs["json"]["resolvedDate"] == "2026-05-14T15:30:00"

    def test_resolve_route_request_model_is_save_on_hold_request(self):
        from ab.api.endpoints.jobs.on_hold import _RESOLVE

        assert _RESOLVE.request_model == "SaveOnHoldRequest"


# ---------------------------------------------------------------------------
# End-to-end chain (mocked) -- mirrors examples/jobs/on_hold.py
# ---------------------------------------------------------------------------


class TestFullChain:
    """The same chain the example walks, validated against a mocked client."""

    def test_create_assign_email_resolve(self, jobs, acportal):
        responses = iter(
            [
                # 1. list
                [],
                # 2a. get_followup_user
                {"contactId": 206, "fullName": "Brett", "email": "b@x.co", "jobRelation": "Owner"},
                # 3.  create
                {"onHoldId": "5001", "status": "Open"},
                # 4.  email send
                None,
                # 5.  resolve
                {"resolved": True, "status": "Resolved"},
            ]
        )

        def _request(*_args, **_kwargs):
            return next(responses)

        acportal.request.side_effect = _request

        jobs.on_hold.list(42)
        user = jobs.on_hold.get_followup_user(42, "206")
        created = jobs.on_hold.create(
            42,
            data=SaveOnHoldRequest(
                reasonId="r-uuid",
                responsiblePartyTypeId="p-uuid",
                comment="x",
                assignedToId=user.contact_id,
            ),
        )
        jobs.email.send(
            42,
            data=SendEmailRequest(to=[user.email], subject="hold", body="hi"),
        )
        resolution = jobs.on_hold.resolve(
            42,
            created.on_hold_id,
            data=SaveOnHoldRequest(reasonId="r-uuid", responsiblePartyTypeId="p-uuid"),
        )

        assert user.email == "b@x.co"
        assert created.on_hold_id == "5001"
        assert resolution.resolved is True

        # 5 HTTP calls total, in order, hitting the expected routes.
        paths = [call.args for call in acportal.request.call_args_list]
        assert paths == [
            ("GET", "/job/42/onhold"),
            ("GET", "/job/42/onhold/followupuser/206"),
            ("POST", "/job/42/onhold"),
            ("POST", "/job/42/email"),
            ("PUT", "/job/42/onhold/5001/resolve"),
        ]
