"""Live integration tests for the dashboard endpoint group.

The unit tests in ``tests/unit/test_dashboard.py`` document the contract
shape against a mocked HTTP client. These tests verify that the live
staging API behaves as advertised. Skipped when staging credentials are
not available.

Operator-in-the-loop discovery
------------------------------

``test_grid_views_chain_to_get`` mirrors the example in
``examples/dashboard.py`` -- it pulls the view list, picks the first
``isActive`` view, and uses its ``id`` as ``view_id`` for ``GET /dashboard``.
"""

from __future__ import annotations

import pytest

from ab.api.models.dashboard import DashboardSummary, GridViewInfo

pytestmark = pytest.mark.live


class TestDashboardIntegration:
    def test_get_no_params_defaults_to_user_primary_company(self, api):
        # Swagger marks viewId/companyId optional. The live API additionally
        # defaults companyId to the active user's primary company, so this
        # call must succeed without arguments.
        result = api.dashboard.get()
        assert isinstance(result, DashboardSummary)

    def test_get_grid_views_returns_list_of_gridviewinfo(self, api):
        views = api.dashboard.get_grid_views()
        assert isinstance(views, list)
        assert all(isinstance(v, GridViewInfo) for v in views)
        for v in views:
            assert v.id is not None
            assert v.name is not None

    def test_grid_views_chain_to_get(self, api):
        # Forward reference: GridViewInfo.id -> DashboardParams.view_id
        views = api.dashboard.get_grid_views()
        if not views:
            pytest.skip("staging account has no grid views")
        active = next((v for v in views if v.is_active), views[0])
        result = api.dashboard.get(view_id=active.id)
        assert isinstance(result, DashboardSummary)
