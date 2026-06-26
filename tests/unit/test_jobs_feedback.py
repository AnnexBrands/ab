"""Wire-level tests for job feedback endpoints."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from ab.api.endpoints.jobs import JobsEndpoint
from ab.api.models.shared import ServiceBaseResponse


@pytest.fixture
def acportal():
    return MagicMock(name="acportal")


@pytest.fixture
def abc():
    return MagicMock(name="abc")


@pytest.fixture
def resolver():
    return MagicMock(name="resolver")


@pytest.fixture
def jobs(acportal, abc, resolver):
    return JobsEndpoint(acportal, abc, resolver)


def test_get_feedback_route(jobs, acportal):
    acportal.request.return_value = {
        "feedbackId": "12345678-1234-1234-1234-123456789abc",
        "cancelJob": False,
    }

    feedback = jobs.get_feedback(42)

    args, _ = acportal.request.call_args
    assert args == ("GET", "/job/feedback/42")
    assert feedback.feedback_id == "12345678-1234-1234-1234-123456789abc"
    assert feedback.cancel_job is False


def test_save_feedback_builds_body_from_feedback_id_and_cancel_flag(jobs, acportal):
    acportal.request.return_value = {"success": True}

    response = jobs.save_feedback(
        42,
        "12345678-1234-1234-1234-123456789abc",
        True,
    )

    args, kwargs = acportal.request.call_args
    assert args == ("POST", "/job/feedback/42")
    assert kwargs["json"] == {
        "feedbackId": "12345678-1234-1234-1234-123456789abc",
        "cancelJob": True,
    }
    assert isinstance(response, ServiceBaseResponse)
    assert response.success is True


def test_save_feedback_accepts_explicit_data_payload(jobs, acportal):
    acportal.request.return_value = {"success": True}

    jobs.save_feedback(
        42,
        data={
            "feedbackId": "12345678-1234-1234-1234-123456789abc",
            "cancelJob": False,
        },
    )

    _, kwargs = acportal.request.call_args
    assert kwargs["json"] == {
        "feedbackId": "12345678-1234-1234-1234-123456789abc",
        "cancelJob": False,
    }
