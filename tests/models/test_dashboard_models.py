"""Fixture validation tests for Dashboard models."""

from ab.api.models.dashboard import DashboardSummary, GridViewInfo, GridViewState
from tests.conftest import assert_no_extra_fields, first_or_skip, require_fixture


class TestDashboardModels:
    def test_dashboard_summary(self):
        data = require_fixture("DashboardSummary", "GET", "/dashboard")
        model = DashboardSummary.model_validate(data)
        assert isinstance(model, DashboardSummary)
        assert_no_extra_fields(model)

    def test_grid_view_info_validates_all_rows(self):
        data = require_fixture("GridViewInfo", "GET", "/dashboard/gridviews")
        assert isinstance(data, list) and data, "fixture must be a non-empty list"
        for row in data:
            model = GridViewInfo.model_validate(row)
            assert_no_extra_fields(model)

    def test_grid_view_info_swagger_shape(self):
        # Swagger GridViewDetails: id (int), name, dataKey, isActive (+ optional sp fields).
        data = require_fixture("GridViewInfo", "GET", "/dashboard/gridviews")
        model = GridViewInfo.model_validate(first_or_skip(data))
        assert isinstance(model.id, int)
        assert model.name is not None
        assert model.data_key is not None
        assert model.is_active is not None

    def test_grid_view_info_id_feeds_dashboard_view_id(self):
        # Forward reference: GridViewInfo.id (output of /dashboard/gridviews) is the
        # value passed as DashboardParams.view_id on GET /dashboard.
        from ab.api.models.dashboard import DashboardParams

        data = require_fixture("GridViewInfo", "GET", "/dashboard/gridviews")
        view = GridViewInfo.model_validate(first_or_skip(data))
        params = DashboardParams(view_id=view.id)
        assert params.view_id == view.id

    def test_grid_view_state(self):
        data = require_fixture("GridViewState", "GET", "/dashboard/gridviewstate/{id}")
        model = GridViewState.model_validate(data)
        assert isinstance(model, GridViewState)
        assert_no_extra_fields(model)
