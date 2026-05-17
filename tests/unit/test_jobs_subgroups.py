"""Unit tests for the new ``api.jobs.<subgroup>`` layout.

Covers the three Stage-1 subgroups (``note``, ``on_hold``, ``form``):

* wire-level call shape for one representative method per subgroup,
* presence of subgroup attributes on :class:`JobsEndpoint`,
* deprecation shim contract (warning + forwarding) for the old method
  names on :class:`JobsEndpoint` and :class:`FormsEndpoint`.
"""

from __future__ import annotations

import warnings
from unittest.mock import MagicMock

import pytest

from ab.api.endpoints.forms import FormsEndpoint
from ab.api.endpoints.jobs import (
    JobFormEndpoint,
    JobNoteEndpoint,
    JobOnHoldEndpoint,
    JobsEndpoint,
)


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


# ---------------------------------------------------------------------------
# Structural — subgroup attributes exist
# ---------------------------------------------------------------------------


def test_jobs_endpoint_exposes_note_subgroup(jobs):
    assert isinstance(jobs.note, JobNoteEndpoint)


def test_jobs_endpoint_exposes_on_hold_subgroup(jobs):
    assert isinstance(jobs.on_hold, JobOnHoldEndpoint)


def test_jobs_endpoint_exposes_form_subgroup(jobs):
    assert isinstance(jobs.form, JobFormEndpoint)


# ---------------------------------------------------------------------------
# Wire-level — one method per subgroup
# ---------------------------------------------------------------------------


class TestNoteSubgroup:
    def test_list_route(self, jobs, acportal):
        acportal.request.return_value = []
        jobs.note.list(42, category="Op", task_code="PK")
        args, kwargs = acportal.request.call_args
        assert args == ("GET", "/job/42/note")
        # JobNoteListParams.check() converts snake_case -> camelCase alias.
        assert kwargs["params"] == {"category": "Op", "taskCode": "PK"}

    def test_create_route_and_body(self, jobs, acportal):
        acportal.request.return_value = {"id": 1}
        jobs.note.create(42, data={"comments": "hello", "taskCode": "PK"})
        args, kwargs = acportal.request.call_args
        assert args == ("POST", "/job/42/note")
        assert kwargs["json"] == {"comments": "hello", "taskCode": "PK"}


class TestOnHoldSubgroup:
    def test_list_route(self, jobs, acportal):
        acportal.request.return_value = []
        jobs.on_hold.list(42)
        args, _ = acportal.request.call_args
        assert args == ("GET", "/job/42/onhold")

    def test_resolve_route_binds_on_hold_id(self, jobs, acportal):
        acportal.request.return_value = {}
        # Resolve shares the SaveOnHoldRequest schema -- reasonId +
        # responsiblePartyTypeId are required.
        jobs.on_hold.resolve(
            42, "oh-1",
            data={
                "reasonId": "r-uuid",
                "responsiblePartyTypeId": "p-uuid",
                "comment": "fixed",
            },
        )
        args, kwargs = acportal.request.call_args
        assert args == ("PUT", "/job/42/onhold/oh-1/resolve")
        assert kwargs["json"] == {
            "reasonId": "r-uuid",
            "responsiblePartyTypeId": "p-uuid",
            "comment": "fixed",
        }

    def test_add_comment_route_binds_on_hold_id(self, jobs, acportal):
        acportal.request.return_value = {}
        jobs.on_hold.add_comment(42, "oh-1", data={"comment": "hi"})
        args, _ = acportal.request.call_args
        assert args == ("POST", "/job/42/onhold/oh-1/comment")


class TestFormSubgroup:
    def test_shipments_route(self, jobs, acportal):
        acportal.request.return_value = []
        jobs.form.shipments(42)
        args, _ = acportal.request.call_args
        assert args == ("GET", "/job/42/form/shipments")

    def test_invoice_returns_named_pdf_blob(self, jobs, acportal):
        acportal.request.return_value = b"PDF-BYTES"
        out = jobs.form.invoice(42, type="standard")
        assert out == {"invoice_42.pdf": b"PDF-BYTES"}
        args, kwargs = acportal.request.call_args
        assert args == ("GET", "/job/42/form/invoice")
        assert kwargs["params"] == {"type": "standard"}


# ---------------------------------------------------------------------------
# Deprecation shims — old names still work and emit warnings
# ---------------------------------------------------------------------------


class TestJobsDeprecationShims:
    def test_get_notes_forwards_to_note_list(self, jobs, acportal):
        acportal.request.return_value = []
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            jobs.get_notes(42)
        assert any(issubclass(w.category, DeprecationWarning) for w in caught)
        assert "api.jobs.note.list" in str(caught[0].message)
        args, _ = acportal.request.call_args
        assert args == ("GET", "/job/42/note")

    def test_list_on_hold_forwards_to_on_hold_list(self, jobs, acportal):
        acportal.request.return_value = []
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            jobs.list_on_hold(42)
        assert any(issubclass(w.category, DeprecationWarning) for w in caught)
        assert "api.jobs.on_hold.list" in str(caught[0].message)
        args, _ = acportal.request.call_args
        assert args == ("GET", "/job/42/onhold")

    def test_resolve_on_hold_forwards_with_data(self, jobs, acportal):
        acportal.request.return_value = {}
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            jobs.resolve_on_hold(
                42, "oh-1",
                data={
                    "reasonId": "r-uuid",
                    "responsiblePartyTypeId": "p-uuid",
                    "comment": "done",
                },
            )
        assert any(issubclass(w.category, DeprecationWarning) for w in caught)
        args, kwargs = acportal.request.call_args
        assert args == ("PUT", "/job/42/onhold/oh-1/resolve")
        assert kwargs["json"]["reasonId"] == "r-uuid"
        assert kwargs["json"]["comment"] == "done"


class TestFormsEndpointShim:
    def test_get_shipments_forwards_to_jobs_form_shipments(self, acportal):
        acportal.request.return_value = []
        forms = FormsEndpoint(acportal)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            forms.get_shipments(42)
        assert any(
            issubclass(w.category, DeprecationWarning)
            and "api.jobs.form.shipments" in str(w.message)
            for w in caught
        )
        args, _ = acportal.request.call_args
        assert args == ("GET", "/job/42/form/shipments")

    def test_get_invoice_forwards_to_jobs_form_invoice(self, acportal):
        acportal.request.return_value = b""
        forms = FormsEndpoint(acportal)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            forms.get_invoice(42, type="standard")
        assert any(
            issubclass(w.category, DeprecationWarning)
            and "api.jobs.form.invoice" in str(w.message)
            for w in caught
        )


# ---------------------------------------------------------------------------
# CLI discovery — subgroups appear with hierarchical names
# ---------------------------------------------------------------------------


class TestCliDiscovery:
    def test_subgroups_are_discoverable(self):
        from ab.cli.discovery import discover_endpoints_from_class

        reg = discover_endpoints_from_class()
        for name in ("jobs", "jobs.note", "jobs.on_hold", "jobs.form"):
            assert name in reg, f"{name!r} missing from discovery registry"

    def test_subgroup_method_counts(self):
        from ab.cli.discovery import discover_endpoints_from_class

        reg = discover_endpoints_from_class()
        assert len(reg["jobs.note"].methods) == 4
        assert len(reg["jobs.on_hold"].methods) == 10
        # form has 15 swagger routes + 5 convenience helpers (ops/bol/hbl/pbl/dbl)
        assert len(reg["jobs.form"].methods) == 20
