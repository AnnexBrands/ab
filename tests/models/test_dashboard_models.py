"""Fixture validation tests for Dashboard models."""

from ab.api.models.dashboard import DashboardSummary, GridViewInfo, GridViewState
from tests.conftest import require_fixture


class TestDashboardModels:
    def test_dashboard_summary(self):
        data = require_fixture("DashboardSummary", "GET", "/dashboard")
        DashboardSummary.model_validate(data)

    def test_grid_view_info(self):
        data = require_fixture("GridViewInfo", "GET", "/dashboard/gridviews")
        GridViewInfo.model_validate(data)

    def test_grid_view_state(self):
        data = require_fixture("GridViewState", "GET", "/dashboard/gridviewstate/{id}")
        GridViewState.model_validate(data)
