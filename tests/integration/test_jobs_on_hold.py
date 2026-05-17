"""Live integration tests for ``api.jobs.on_hold``.

Mirrors ``examples/jobs/on_hold.py``: list -> followup discovery ->
create -> email -> resolve. Skipped when staging credentials are not
available, and individual steps may skip if staging data isn't shaped
right (no follow-up user with an email, no lookup options for
``OnHoldReason``, etc.).
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from ab.api.models.jobs import (
    ExtendedOnHoldInfo,
    OnHoldUser,
    SaveOnHoldRequest,
    SendEmailRequest,
)

pytestmark = pytest.mark.live


class TestJobOnHoldIntegration:
    def test_list_returns_extended_on_hold_info(self, api):
        from examples.constants import TEST_JOB_DISPLAY_ID

        holds = api.jobs.on_hold.list(TEST_JOB_DISPLAY_ID)
        assert isinstance(holds, list)
        for h in holds:
            assert isinstance(h, ExtendedOnHoldInfo)

    def test_followup_user_is_on_hold_user(self, api):
        from examples.constants import TEST_JOB_DISPLAY_ID, TEST_USER_ID

        user = api.jobs.on_hold.get_followup_user(TEST_JOB_DISPLAY_ID, str(TEST_USER_ID))
        assert isinstance(user, OnHoldUser)

    def test_create_assign_email_resolve_chain(self, api):
        """Full create/assign/email/resolve walkthrough -- the example's flow."""
        from examples.constants import TEST_JOB_DISPLAY_ID, TEST_USER_ID

        # Lookup the required UUIDs.
        reasons = api.lookup.get_by_key("OnHoldReason")
        parties = api.lookup.get_by_key("ResponsibleParty")
        if not reasons or not parties:
            pytest.skip("staging lookups missing OnHoldReason or ResponsibleParty")
        reason_id = reasons[0].id
        party_id = parties[0].id

        # Follow-up user has to have an email for the notification step.
        user = api.jobs.on_hold.get_followup_user(TEST_JOB_DISPLAY_ID, str(TEST_USER_ID))
        if not user.email:
            pytest.skip(f"TEST_USER_ID={TEST_USER_ID} has no email on staging")

        now = datetime.now(timezone.utc).replace(microsecond=0)
        body = SaveOnHoldRequest(
            reasonId=reason_id,
            responsiblePartyTypeId=party_id,
            comment="Integration test hold; will be resolved immediately.",
            assignedToId=TEST_USER_ID,
            startDate=now,
            dueDate=now + timedelta(days=1),
        )

        # Create.
        created = api.jobs.on_hold.create(TEST_JOB_DISPLAY_ID, data=body)
        assert created.on_hold_id, "create() must return an on_hold_id"

        try:
            # Notify.
            api.jobs.email.send(
                TEST_JOB_DISPLAY_ID,
                data=SendEmailRequest(
                    to=[user.email],
                    subject=f"Job {TEST_JOB_DISPLAY_ID}: integration-test hold",
                    body="Integration test escalation. Safe to ignore.",
                ),
            )
        finally:
            # Resolve -- swagger requires reasonId + responsiblePartyTypeId
            # on the resolve payload too.
            resolution = api.jobs.on_hold.resolve(
                TEST_JOB_DISPLAY_ID,
                created.on_hold_id,
                data=SaveOnHoldRequest(
                    reasonId=reason_id,
                    responsiblePartyTypeId=party_id,
                    comment="Resolved by integration test.",
                    resolvedDate=datetime.now(timezone.utc).replace(microsecond=0),
                ),
            )
            assert resolution.resolved is not False
