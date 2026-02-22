"""Fixture validation tests for On-Hold models."""

from ab.api.models.jobs import (
    ExtendedOnHoldInfo,
    OnHoldDetails,
    OnHoldNoteDetails,
    OnHoldUser,
    ResolveJobOnHoldResponse,
    SaveOnHoldResponse,
)
from tests.conftest import assert_no_extra_fields, require_fixture


class TestOnHoldModels:
    def test_extended_on_hold_info(self):
        data = require_fixture("ExtendedOnHoldInfo", "GET", "/job/{id}/onhold")
        model = ExtendedOnHoldInfo.model_validate(data)
        assert isinstance(model, ExtendedOnHoldInfo)
        assert_no_extra_fields(model)

    def test_on_hold_details(self):
        data = require_fixture("OnHoldDetails", "GET", "/job/{id}/onhold/{id}")
        model = OnHoldDetails.model_validate(data)
        assert isinstance(model, OnHoldDetails)
        assert_no_extra_fields(model)

    def test_save_on_hold_response(self):
        data = require_fixture("SaveOnHoldResponse", "POST", "/job/{id}/onhold")
        model = SaveOnHoldResponse.model_validate(data)
        assert isinstance(model, SaveOnHoldResponse)
        assert_no_extra_fields(model)

    def test_resolve_job_on_hold_response(self):
        data = require_fixture("ResolveJobOnHoldResponse", "PUT", "/job/{id}/onhold/{id}/resolve")
        model = ResolveJobOnHoldResponse.model_validate(data)
        assert isinstance(model, ResolveJobOnHoldResponse)
        assert_no_extra_fields(model)

    def test_on_hold_user(self):
        data = require_fixture("OnHoldUser", "GET", "/job/{id}/onhold/followupuser/{id}")
        model = OnHoldUser.model_validate(data)
        assert isinstance(model, OnHoldUser)
        assert_no_extra_fields(model)

    def test_on_hold_note_details(self):
        data = require_fixture("OnHoldNoteDetails", "POST", "/job/{id}/onhold/{id}/comment")
        model = OnHoldNoteDetails.model_validate(data)
        assert isinstance(model, OnHoldNoteDetails)
        assert_no_extra_fields(model)
