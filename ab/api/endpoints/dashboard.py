"""Dashboard API endpoints (9 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ab.api.models.dashboard import DashboardSummary, GridViewInfo, GridViewState

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_GET = Route("GET", "/dashboard", params_model="DashboardParams", response_model="DashboardSummary")
_GET_GRID_VIEWS = Route("GET", "/dashboard/gridviews", response_model="List[GridViewInfo]")
_GET_GRID_VIEW_STATE = Route("GET", "/dashboard/gridviewstate/{id}", response_model="GridViewState")
_SAVE_GRID_VIEW_STATE = Route("POST", "/dashboard/gridviewstate/{id}", request_model="GridViewState")
_INBOUND = Route("POST", "/dashboard/inbound")
_IN_HOUSE = Route("POST", "/dashboard/inhouse")
_OUTBOUND = Route("POST", "/dashboard/outbound")
_LOCAL_DELIVERIES = Route("POST", "/dashboard/local-deliveries")
_RECENT_ESTIMATES = Route("POST", "/dashboard/recentestimates")


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

    def save_grid_view_state(self, view_id: str, **kwargs: Any) -> Any:
        """POST /dashboard/gridviewstate/{id}"""
        return self._request(_SAVE_GRID_VIEW_STATE.bind(id=view_id), json=kwargs)

    def inbound(self, **kwargs: Any) -> Any:
        """POST /dashboard/inbound"""
        return self._request(_INBOUND, json=kwargs)

    def in_house(self, **kwargs: Any) -> Any:
        """POST /dashboard/inhouse"""
        return self._request(_IN_HOUSE, json=kwargs)

    def outbound(self, **kwargs: Any) -> Any:
        """POST /dashboard/outbound"""
        return self._request(_OUTBOUND, json=kwargs)

    def local_deliveries(self, **kwargs: Any) -> Any:
        """POST /dashboard/local-deliveries"""
        return self._request(_LOCAL_DELIVERIES, json=kwargs)

    def recent_estimates(self, **kwargs: Any) -> Any:
        """POST /dashboard/recentestimates"""
        return self._request(_RECENT_ESTIMATES, json=kwargs)
