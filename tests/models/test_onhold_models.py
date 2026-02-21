"""Fixture validation tests for On-Hold models."""

from ab.api.models.jobs import (
    ExtendedOnHoldInfo,
    OnHoldDetails,
    OnHoldNoteDetails,
    OnHoldUser,
    ResolveJobOnHoldResponse,
    SaveOnHoldResponse,
)
from tests.conftest import require_fixture


class TestOnHoldModels:
    def test_extended_on_hold_info(self):
        data = require_fixture("ExtendedOnHoldInfo", "GET", "/job/{id}/onhold")
        ExtendedOnHoldInfo.model_validate(data)

    def test_on_hold_details(self):
        data = require_fixture("OnHoldDetails", "GET", "/job/{id}/onhold/{id}")
        OnHoldDetails.model_validate(data)

    def test_save_on_hold_response(self):
        data = require_fixture("SaveOnHoldResponse", "POST", "/job/{id}/onhold")
        SaveOnHoldResponse.model_validate(data)

    def test_resolve_job_on_hold_response(self):
        data = require_fixture("ResolveJobOnHoldResponse", "PUT", "/job/{id}/onhold/{id}/resolve")
        ResolveJobOnHoldResponse.model_validate(data)

    def test_on_hold_user(self):
        data = require_fixture("OnHoldUser", "GET", "/job/{id}/onhold/followupuser/{id}")
        OnHoldUser.model_validate(data)

    def test_on_hold_note_details(self):
        data = require_fixture("OnHoldNoteDetails", "POST", "/job/{id}/onhold/{id}/comment")
        OnHoldNoteDetails.model_validate(data)
