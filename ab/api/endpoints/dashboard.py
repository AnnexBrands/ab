"""Dashboard API endpoints (9 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ab.api.models.dashboard import DashboardCompanyParams, DashboardSummary, GridViewInfo, GridViewState

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_GET = Route("GET", "/dashboard", params_model="DashboardParams", response_model="DashboardSummary")
_GET_GRID_VIEWS = Route("GET", "/dashboard/gridviews", params_model="DashboardCompanyParams", response_model="List[GridViewInfo]")
_GET_GRID_VIEW_STATE = Route("GET", "/dashboard/gridviewstate/{id}", response_model="GridViewState")
_SAVE_GRID_VIEW_STATE = Route("POST", "/dashboard/gridviewstate/{id}", request_model="GridViewState")
_INBOUND = Route("POST", "/dashboard/inbound", request_model="DashboardCompanyParams")
_IN_HOUSE = Route("POST", "/dashboard/inhouse", request_model="DashboardCompanyParams")
_OUTBOUND = Route("POST", "/dashboard/outbound", request_model="DashboardCompanyParams")
_LOCAL_DELIVERIES = Route("POST", "/dashboard/local-deliveries", request_model="DashboardCompanyParams")
_RECENT_ESTIMATES = Route("POST", "/dashboard/recentestimates", request_model="DashboardCompanyParams")


class DashboardEndpoint(BaseEndpoint):
    """Dashboard operations (ACPortal API)."""

    def get(
        self,
        *,
        view_id: int | None = None,
        company_id: str | None = None,
    ) -> DashboardSummary:
        """GET /dashboard"""
        return self._request(_GET, params=dict(view_id=view_id, company_id=company_id))

    def get_grid_views(self) -> list[GridViewInfo]:
        """GET /dashboard/gridviews"""
        return self._request(_GET_GRID_VIEWS)

    def get_grid_view_state(self, view_id: str) -> GridViewState:
        """GET /dashboard/gridviewstate/{id}"""
        return self._request(_GET_GRID_VIEW_STATE.bind(id=view_id))

    def save_grid_view_state(self, view_id: str, *, data: GridViewState | dict) -> Any:
        """POST /dashboard/gridviewstate/{id}.

        Args:
            view_id: View state identifier.
            data: Grid view state with columns, filters, and sort_order.
                Accepts a :class:`GridViewState` instance or a dict.

        Request model: :class:`GridViewState`
        """
        return self._request(_SAVE_GRID_VIEW_STATE.bind(id=view_id), json=data)

    def inbound(self, *, data: DashboardCompanyParams | dict) -> Any:
        """POST /dashboard/inbound.

        Args:
            data: Dashboard company filter payload.
                Accepts a :class:`DashboardCompanyParams` instance or a dict.

        Request model: :class:`DashboardCompanyParams`
        """
        return self._request(_INBOUND, json=data)

    def in_house(self, *, data: DashboardCompanyParams | dict) -> Any:
        """POST /dashboard/inhouse.

        Args:
            data: Dashboard company filter payload.
                Accepts a :class:`DashboardCompanyParams` instance or a dict.

        Request model: :class:`DashboardCompanyParams`
        """
        return self._request(_IN_HOUSE, json=data)

    def outbound(self, *, data: DashboardCompanyParams | dict) -> Any:
        """POST /dashboard/outbound.

        Args:
            data: Dashboard company filter payload.
                Accepts a :class:`DashboardCompanyParams` instance or a dict.

        Request model: :class:`DashboardCompanyParams`
        """
        return self._request(_OUTBOUND, json=data)

    def local_deliveries(self, *, data: DashboardCompanyParams | dict) -> Any:
        """POST /dashboard/local-deliveries.

        Args:
            data: Dashboard company filter payload.
                Accepts a :class:`DashboardCompanyParams` instance or a dict.

        Request model: :class:`DashboardCompanyParams`
        """
        return self._request(_LOCAL_DELIVERIES, json=data)

    def recent_estimates(self, *, data: DashboardCompanyParams | dict) -> Any:
        """POST /dashboard/recentestimates.

        Args:
            data: Dashboard company filter payload.
                Accepts a :class:`DashboardCompanyParams` instance or a dict.

        Request model: :class:`DashboardCompanyParams`
        """
        return self._request(_RECENT_ESTIMATES, json=data)
