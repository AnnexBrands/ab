"""Dashboard API endpoints (9 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab.api.models.dashboard import DashboardCompanyRequest, DashboardSummary, GridViewInfo, GridViewState

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_GET = Route("GET", "/dashboard", params_model="DashboardParams", response_model="DashboardSummary")
_GET_GRID_VIEWS = Route(
    "GET", "/dashboard/gridviews", params_model="DashboardCompanyParams", response_model="List[GridViewInfo]"
)
_GET_GRID_VIEW_STATE = Route("GET", "/dashboard/gridviewstate/{id}", response_model="GridViewState")
_SAVE_GRID_VIEW_STATE = Route("POST", "/dashboard/gridviewstate/{id}", request_model="GridViewState")
_INBOUND = Route("POST", "/dashboard/inbound", request_model="DashboardCompanyRequest")
_IN_HOUSE = Route("POST", "/dashboard/inhouse", request_model="DashboardCompanyRequest")
_OUTBOUND = Route("POST", "/dashboard/outbound", request_model="DashboardCompanyRequest")
_LOCAL_DELIVERIES = Route("POST", "/dashboard/local-deliveries", request_model="DashboardCompanyRequest")
_RECENT_ESTIMATES = Route("POST", "/dashboard/recentestimates", request_model="DashboardCompanyRequest")


class DashboardEndpoint(BaseEndpoint):
    """Dashboard operations (ACPortal API)."""

    def get(
        self,
        *,
        view_id: int | None = None,
        company_id: str | None = None,
    ) -> DashboardSummary:
        """Aggregated dashboard summary for one grid view.

        Both ``view_id`` and ``company_id`` are optional. When ``company_id``
        is omitted the API defaults to the active user's primary company —
        the call does not 4xx. ``view_id`` is the ``id`` of a row returned
        by :meth:`get_grid_views`.

        Args:
            view_id: Grid view id (forward reference: :class:`GridViewInfo.id`).
            company_id: Company UUID; defaults to the caller's primary company.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/dashboard/get.html
        Query params: DashboardParams
        Response model: DashboardSummary
        """
        return self._request(_GET, params=dict(view_id=view_id, company_id=company_id))

    def get_grid_views(self) -> list[GridViewInfo]:
        """List the grid views available to the caller.

        Each row carries the ``id`` you pass to :meth:`get` as ``view_id``,
        plus ``name``, ``dataKey``, and ``isActive``.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/dashboard/get_grid_views.html
        Query params: DashboardCompanyParams
        Response model: List[GridViewInfo]
        """
        return self._request(_GET_GRID_VIEWS)

    def get_grid_view_state(self, view_id: str) -> GridViewState:
        """Fetch the saved column / filter / sort state for a grid view.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/dashboard/get_grid_view_state.html
        Response model: GridViewState
        """
        return self._request(_GET_GRID_VIEW_STATE.bind(id=view_id))

    def save_grid_view_state(self, view_id: str, *, data: GridViewState | dict) -> None:
        """POST /dashboard/gridviewstate/{id}.

        Args:
            view_id: View state identifier.
            data: Grid view state with columns, filters, and sort_order.
                Accepts a :class:`GridViewState` instance or a dict.

        Request model: :class:`GridViewState`

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/dashboard/save_grid_view_state.html
        Request model: GridViewState
        """
        return self._request(_SAVE_GRID_VIEW_STATE.bind(id=view_id), json=data)

    def inbound(self, *, data: DashboardCompanyRequest | dict) -> None:
        """POST /dashboard/inbound.

        Args:
            data: Dashboard company filter payload.
                Accepts a :class:`DashboardCompanyRequest` instance or a dict.

        Request model: :class:`DashboardCompanyRequest`

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/dashboard/inbound.html
        Request model: DashboardCompanyRequest
        """
        return self._request(_INBOUND, json=data)

    def in_house(self, *, data: DashboardCompanyRequest | dict) -> None:
        """POST /dashboard/inhouse.

        Args:
            data: Dashboard company filter payload.
                Accepts a :class:`DashboardCompanyRequest` instance or a dict.

        Request model: :class:`DashboardCompanyRequest`

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/dashboard/in_house.html
        Request model: DashboardCompanyRequest
        """
        return self._request(_IN_HOUSE, json=data)

    def outbound(self, *, data: DashboardCompanyRequest | dict) -> None:
        """POST /dashboard/outbound.

        Args:
            data: Dashboard company filter payload.
                Accepts a :class:`DashboardCompanyRequest` instance or a dict.

        Request model: :class:`DashboardCompanyRequest`

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/dashboard/outbound.html
        Request model: DashboardCompanyRequest
        """
        return self._request(_OUTBOUND, json=data)

    def local_deliveries(self, *, data: DashboardCompanyRequest | dict) -> None:
        """POST /dashboard/local-deliveries.

        Args:
            data: Dashboard company filter payload.
                Accepts a :class:`DashboardCompanyRequest` instance or a dict.

        Request model: :class:`DashboardCompanyRequest`

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/dashboard/local_deliveries.html
        Request model: DashboardCompanyRequest
        """
        return self._request(_LOCAL_DELIVERIES, json=data)

    def recent_estimates(self, *, data: DashboardCompanyRequest | dict) -> None:
        """POST /dashboard/recentestimates.

        Args:
            data: Dashboard company filter payload.
                Accepts a :class:`DashboardCompanyRequest` instance or a dict.

        Request model: :class:`DashboardCompanyRequest`

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/dashboard/recent_estimates.html
        Request model: DashboardCompanyRequest
        """
        return self._request(_RECENT_ESTIMATES, json=data)
