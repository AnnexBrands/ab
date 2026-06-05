"""Unit tests for the Stage-2 ``api.jobs.<subgroup>`` additions.

Covers the 10 subgroups added in Stage 2:

* In-jobs: ``timeline``, ``email``, ``sms``, ``freight_providers``,
  ``parcel_items``, ``tracking``, ``status``.
* Cross-endpoint moves: ``payment`` (from ``api.payments``),
  ``shipment`` (from ``api.shipments``), ``rfq`` (job-scoped methods
  that were on ``api.jobs.*``).

For each subgroup we check one representative route + verify the
deprecation shim on the legacy surface still works and emits a warning.
"""

from __future__ import annotations

import warnings
from unittest.mock import MagicMock

import pytest

from ab.api.endpoints.jobs import (
    JobEmailEndpoint,
    JobFreightProvidersEndpoint,
    JobParcelItemsEndpoint,
    JobPaymentEndpoint,
    JobRfqEndpoint,
    JobsEndpoint,
    JobShipmentEndpoint,
    JobSmsEndpoint,
    JobStatusEndpoint,
    JobTimelineEndpoint,
    JobTrackingEndpoint,
)
from ab.api.endpoints.payments import PaymentsEndpoint
from ab.api.endpoints.shipments import ShipmentsEndpoint


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
# Structural — every Stage-2 subgroup is wired and the right type
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("attr", "cls"),
    [
        ("timeline", JobTimelineEndpoint),
        ("email", JobEmailEndpoint),
        ("sms", JobSmsEndpoint),
        ("freight_providers", JobFreightProvidersEndpoint),
        ("parcel_items", JobParcelItemsEndpoint),
        ("tracking", JobTrackingEndpoint),
        ("status", JobStatusEndpoint),
        ("payment", JobPaymentEndpoint),
        ("shipment", JobShipmentEndpoint),
        ("rfq", JobRfqEndpoint),
    ],
)
def test_subgroup_wired(jobs, attr, cls):
    assert isinstance(getattr(jobs, attr), cls), f"api.jobs.{attr} should be a {cls.__name__}"


# ---------------------------------------------------------------------------
# Wire-level — one method per subgroup
# ---------------------------------------------------------------------------


class TestTimelineSubgroup:
    def test_response_route(self, jobs, acportal):
        acportal.request.return_value = {"tasks": []}
        jobs.timeline.response(42)
        args, _ = acportal.request.call_args
        assert args == ("GET", "/job/42/timeline")

    def test_increment_status_route(self, jobs, acportal):
        acportal.request.return_value = {}
        jobs.timeline.increment_status(42, data={})
        args, _ = acportal.request.call_args
        assert args == ("POST", "/job/42/timeline/incrementjobstatus")


class TestEmailSubgroup:
    def test_send_template_binds_guid(self, jobs, acportal):
        acportal.request.return_value = None
        jobs.email.send_template(42, "abc-template")
        args, _ = acportal.request.call_args
        assert args == ("POST", "/job/42/email/abc-template/send")


class TestSmsSubgroup:
    def test_list_route(self, jobs, acportal):
        acportal.request.return_value = []
        jobs.sms.list(42)
        args, _ = acportal.request.call_args
        assert args == ("GET", "/job/42/sms")


class TestFreightProvidersSubgroup:
    def test_rate_quote_binds_option_index(self, jobs, acportal):
        acportal.request.return_value = None
        jobs.freight_providers.rate_quote(42, 3, data={})
        args, _ = acportal.request.call_args
        assert args == ("POST", "/job/42/freightproviders/3/ratequote")


class TestParcelItemsSubgroup:
    def test_list_route(self, jobs, acportal):
        acportal.request.return_value = []
        jobs.parcel_items.list(42)
        args, _ = acportal.request.call_args
        assert args == ("GET", "/job/42/parcelitems")

    def test_delete_binds_id(self, jobs, acportal):
        acportal.request.return_value = {}
        jobs.parcel_items.delete(42, "pi-1")
        args, _ = acportal.request.call_args
        assert args == ("DELETE", "/job/42/parcelitems/pi-1")


class TestTrackingSubgroup:
    def test_get_route(self, jobs, acportal):
        acportal.request.return_value = {}
        jobs.tracking.get(42)
        args, _ = acportal.request.call_args
        assert args == ("GET", "/job/42/tracking")

    def test_v3_route_binds_history_amount(self, jobs, acportal):
        acportal.request.return_value = {}
        jobs.tracking.v3(42, 5)
        args, _ = acportal.request.call_args
        assert args == ("GET", "/v3/job/42/tracking/5")


class TestStatusSubgroup:
    def test_set_quote_route(self, jobs, acportal):
        acportal.request.return_value = {}
        jobs.status.set_quote(42)
        args, _ = acportal.request.call_args
        assert args == ("POST", "/job/42/status/quote")


class TestPaymentSubgroup:
    def test_get_route(self, jobs, acportal):
        acportal.request.return_value = {}
        jobs.payment.get(42)
        args, _ = acportal.request.call_args
        assert args == ("GET", "/job/42/payment")

    def test_pay_by_source_posts_body(self, jobs, acportal):
        acportal.request.return_value = {}
        jobs.payment.pay_by_source(42, data={})
        args, _ = acportal.request.call_args
        assert args == ("POST", "/job/42/payment/bysource")


class TestShipmentSubgroup:
    def test_delete_route(self, jobs, acportal):
        acportal.request.return_value = {}
        jobs.shipment.delete(42)
        args, _ = acportal.request.call_args
        assert args == ("DELETE", "/job/42/shipment")

    def test_remove_accessorial_binds_id(self, jobs, acportal):
        acportal.request.return_value = {}
        jobs.shipment.remove_accessorial(42, "add-1")
        args, _ = acportal.request.call_args
        assert args == ("DELETE", "/job/42/shipment/accessorial/add-1")


class TestRfqSubgroup:
    def test_list_route(self, jobs, acportal):
        acportal.request.return_value = []
        jobs.rfq.list(42)
        args, _ = acportal.request.call_args
        assert args == ("GET", "/job/42/rfq")

    def test_status_binds_three_params(self, jobs, acportal):
        acportal.request.return_value = 0
        jobs.rfq.status(42, "3", "company-uuid")
        args, _ = acportal.request.call_args
        assert args == ("GET", "/job/42/rfq/statusof/3/forcompany/company-uuid")


# ---------------------------------------------------------------------------
# Deprecation shims — one per subgroup
# ---------------------------------------------------------------------------


def _expect_deprecation(call, msg_contains: str):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        call()
    matching = [w for w in caught if issubclass(w.category, DeprecationWarning)]
    assert matching, "expected a DeprecationWarning"
    assert any(msg_contains in str(w.message) for w in matching), (
        f"expected a warning containing {msg_contains!r}; got {[str(w.message) for w in matching]}"
    )


class TestJobsLegacyShims:
    """The flat method names on ``JobsEndpoint`` still work and warn."""

    def test_get_timeline_response(self, jobs, acportal):
        acportal.request.return_value = {"tasks": []}
        _expect_deprecation(lambda: jobs.get_timeline_response(42), "api.jobs.timeline.response")

    def test_send_email(self, jobs, acportal):
        acportal.request.return_value = None
        _expect_deprecation(lambda: jobs.send_email(42, data={}), "api.jobs.email.send")

    def test_list_sms(self, jobs, acportal):
        acportal.request.return_value = []
        _expect_deprecation(lambda: jobs.list_sms(42), "api.jobs.sms.list")

    def test_get_tracking(self, jobs, acportal):
        acportal.request.return_value = {}
        _expect_deprecation(lambda: jobs.get_tracking(42), "api.jobs.tracking.get")

    def test_set_quote_status(self, jobs, acportal):
        acportal.request.return_value = {}
        _expect_deprecation(lambda: jobs.set_quote_status(42), "api.jobs.status.set_quote")

    def test_list_rfqs(self, jobs, acportal):
        acportal.request.return_value = []
        _expect_deprecation(lambda: jobs.list_rfqs(42), "api.jobs.rfq.list")


class TestPaymentsStandaloneShim:
    """``api.payments.*`` is now a thin shim forwarding to ``api.jobs.payment``."""

    def test_get_warns_and_forwards(self, acportal):
        acportal.request.return_value = {}
        payments = PaymentsEndpoint(acportal)
        _expect_deprecation(lambda: payments.get(42), "api.jobs.payment.get")
        args, _ = acportal.request.call_args
        assert args == ("GET", "/job/42/payment")

    def test_pay_by_source_warns(self, acportal):
        acportal.request.return_value = {}
        payments = PaymentsEndpoint(acportal)
        _expect_deprecation(
            lambda: payments.pay_by_source(42, data={}),
            "api.jobs.payment.pay_by_source",
        )


class TestShipmentsStandaloneShim:
    """Job-scoped methods on ``api.shipments`` warn and forward.
    Non-job-scoped methods (``get_shipment`` etc.) stay canonical here.
    """

    def test_job_scoped_warns(self, acportal):
        acportal.request.return_value = []
        shipments = ShipmentsEndpoint(acportal)
        _expect_deprecation(
            lambda: shipments.get_rate_quotes(42),
            "api.jobs.shipment.get_rate_quotes",
        )
        args, _ = acportal.request.call_args
        assert args == ("GET", "/job/42/shipment/ratequotes")

    def test_global_get_shipment_does_not_warn(self, acportal):
        acportal.request.return_value = {}
        shipments = ShipmentsEndpoint(acportal)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            shipments.get_shipment(pro_number="1234")
        deprecations = [w for w in caught if issubclass(w.category, DeprecationWarning)]
        assert not deprecations, "non-job-scoped get_shipment should not warn"
        args, _ = acportal.request.call_args
        assert args == ("GET", "/shipment")


# ---------------------------------------------------------------------------
# CLI discovery — all 13 subgroups discoverable
# ---------------------------------------------------------------------------


def test_all_subgroups_discoverable():
    from ab.cli.discovery import discover_endpoints_from_class

    reg = discover_endpoints_from_class()
    expected = {
        "jobs.note", "jobs.on_hold", "jobs.form",
        "jobs.timeline", "jobs.email", "jobs.sms",
        "jobs.freight_providers", "jobs.parcel_items",
        "jobs.tracking", "jobs.status",
        "jobs.payment", "jobs.shipment", "jobs.rfq",
    }
    missing = expected - set(reg)
    assert not missing, f"missing subgroups: {missing}"
