"""Unit tests for the dashboard endpoint group.

These tests document the **expected wire-level behaviour** of the
dashboard methods using a mocked :class:`~ab.http.HttpClient`. They lock
in:

* the routes hit by each method,
* the ``params``/``json`` payloads sent (alias keys, exclude_none),
* the swagger-vs-actual divergence for ``GET /dashboard``.

Live behaviour is exercised by ``tests/integration/test_dashboard.py``.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from ab.api.endpoints.dashboard import DashboardEndpoint
from ab.api.models.dashboard import (
    DashboardCompanyRequest,
    DashboardSummary,
    GridViewInfo,
    GridViewState,
)


@pytest.fixture
def client():
    """Mocked HttpClient -- ``request()`` is the only attr exercised."""
    return MagicMock(name="HttpClient")


@pytest.fixture
def dashboard(client):
    return DashboardEndpoint(client)


# ---------------------------------------------------------------------------
# GET /dashboard -- documented behaviour
# ---------------------------------------------------------------------------


class TestDashboardGet:
    """Documented behaviour of ``api.dashboard.get(...)``.

    Swagger (``/api/dashboard``) declares two query parameters --
    ``viewId`` and ``companyId`` -- and marks **both as not required**.
    The live API additionally **defaults ``companyId`` to the active
    user's primary company** when omitted, so calling ``get()`` with no
    arguments must not raise.
    """

    def test_no_params_does_not_fail_and_sends_empty_query(self, dashboard, client):
        client.request.return_value = {}
        dashboard.get()
        args, kwargs = client.request.call_args
        assert args == ("GET", "/dashboard")
        # exclude_none + DashboardParams check() drops both Nones -> {}
        assert kwargs["params"] == {}

    def test_view_id_serialises_as_camel_case_alias(self, dashboard, client):
        client.request.return_value = {}
        dashboard.get(view_id=42)
        kwargs = client.request.call_args.kwargs
        assert kwargs["params"] == {"viewId": 42}

    def test_company_id_serialises_as_camel_case_alias(self, dashboard, client):
        client.request.return_value = {}
        dashboard.get(company_id="93179b52-3da9-e311-b6f8-000c298b59ee")
        kwargs = client.request.call_args.kwargs
        assert kwargs["params"] == {"companyId": "93179b52-3da9-e311-b6f8-000c298b59ee"}

    def test_both_params_round_trip(self, dashboard, client):
        client.request.return_value = {}
        dashboard.get(view_id=1, company_id="abc")
        kwargs = client.request.call_args.kwargs
        assert kwargs["params"] == {"viewId": 1, "companyId": "abc"}

    def test_response_is_cast_to_dashboard_summary(self, dashboard, client):
        client.request.return_value = {
            "inboundCount": 3,
            "outboundCount": 7,
            "inHouseCount": 2,
            "data": [],
        }
        result = dashboard.get()
        assert isinstance(result, DashboardSummary)
        assert result.inbound_count == 3
        assert result.outbound_count == 7


# ---------------------------------------------------------------------------
# GET /dashboard/gridviews -- discovery chain entry point
# ---------------------------------------------------------------------------


class TestDashboardGetGridViews:
    """``api.dashboard.get_grid_views()`` returns ``List[GridViewInfo]``.

    Forward reference: the ``id`` of each :class:`GridViewInfo` is the
    value an operator passes as ``view_id`` to ``api.dashboard.get(...)``.
    """

    def test_route_is_gridviews(self, dashboard, client):
        client.request.return_value = []
        dashboard.get_grid_views()
        args, _ = client.request.call_args
        assert args == ("GET", "/dashboard/gridviews")

    def test_response_is_cast_to_list_of_gridviewinfo(self, dashboard, client):
        client.request.return_value = [
            {"id": 1, "name": "Inbound", "dataKey": "inbound", "isActive": True},
            {"id": 2, "name": "Archived", "dataKey": "archived", "isActive": False},
        ]
        result = dashboard.get_grid_views()
        assert len(result) == 2
        assert all(isinstance(v, GridViewInfo) for v in result)
        # Forward reference in action: feed first id into DashboardParams.
        first = result[0]
        assert first.id == 1
        assert first.data_key == "inbound"
        assert first.is_active is True


# ---------------------------------------------------------------------------
# GET / POST /dashboard/gridviewstate/{id}
# ---------------------------------------------------------------------------


class TestDashboardGridViewState:
    def test_get_grid_view_state_binds_id(self, dashboard, client):
        client.request.return_value = {"id": "abc", "columns": [], "filters": []}
        result = dashboard.get_grid_view_state("abc")
        args, _ = client.request.call_args
        assert args == ("GET", "/dashboard/gridviewstate/abc")
        assert isinstance(result, GridViewState)

    def test_save_grid_view_state_posts_body(self, dashboard, client):
        client.request.return_value = None
        dashboard.save_grid_view_state("abc", data={"columns": [{"k": "v"}], "filters": []})
        args, kwargs = client.request.call_args
        assert args == ("POST", "/dashboard/gridviewstate/abc")
        assert kwargs["json"] == {"columns": [{"k": "v"}], "filters": []}


# ---------------------------------------------------------------------------
# POST /dashboard/{inbound,inhouse,outbound,local-deliveries,recentestimates}
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("method", "path"),
    [
        ("inbound", "/dashboard/inbound"),
        ("in_house", "/dashboard/inhouse"),
        ("outbound", "/dashboard/outbound"),
        ("local_deliveries", "/dashboard/local-deliveries"),
        ("recent_estimates", "/dashboard/recentestimates"),
    ],
)
def test_dashboard_panel_posts_company_request(method, path, dashboard, client):
    client.request.return_value = None
    payload = DashboardCompanyRequest(company_id="93179b52-3da9-e311-b6f8-000c298b59ee")
    getattr(dashboard, method)(data=payload)
    args, kwargs = client.request.call_args
    assert args == ("POST", path)
    assert kwargs["json"] == {"companyId": "93179b52-3da9-e311-b6f8-000c298b59ee"}


def test_dashboard_panel_accepts_dict(dashboard, client):
    client.request.return_value = None
    dashboard.inbound(data={"companyId": "abc"})
    args, kwargs = client.request.call_args
    assert args == ("POST", "/dashboard/inbound")
    assert kwargs["json"] == {"companyId": "abc"}
