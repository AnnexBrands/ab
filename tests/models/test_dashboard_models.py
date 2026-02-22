"""Fixture validation tests for Dashboard models."""

from ab.api.models.dashboard import DashboardSummary, GridViewInfo, GridViewState
from tests.conftest import assert_no_extra_fields, require_fixture


class TestDashboardModels:
    def test_dashboard_summary(self):
        data = require_fixture("DashboardSummary", "GET", "/dashboard")
        model = DashboardSummary.model_validate(data)
        assert isinstance(model, DashboardSummary)
        assert_no_extra_fields(model)

    def test_grid_view_info(self):
        data = require_fixture("GridViewInfo", "GET", "/dashboard/gridviews")
        model = GridViewInfo.model_validate(data)
        assert isinstance(model, GridViewInfo)
        assert_no_extra_fields(model)

    def test_grid_view_state(self):
        data = require_fixture("GridViewState", "GET", "/dashboard/gridviewstate/{id}")
        model = GridViewState.model_validate(data)
        assert isinstance(model, GridViewState)
        assert_no_extra_fields(model)
