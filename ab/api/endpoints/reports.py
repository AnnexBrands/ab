"""Reports API endpoints (8 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ab.api.models.reports import (
        InsuranceReport,
        ReferredByReport,
        RevenueCustomer,
        SalesForecastReport,
        SalesForecastSummary,
        Web2LeadReport,
    )

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_INSURANCE = Route(
    "POST", "/reports/insurance",
    request_model="InsuranceReportRequest", response_model="InsuranceReport",
)
_SALES = Route(
    "POST", "/reports/sales",
    request_model="SalesForecastReportRequest", response_model="SalesForecastReport",
)
_SALES_SUMMARY = Route(
    "POST", "/reports/sales/summary",
    request_model="SalesForecastSummaryRequest", response_model="SalesForecastSummary",
)
_SALES_DRILLDOWN = Route(
    "POST", "/reports/salesDrilldown",
    request_model="Web2LeadRevenueFilter", response_model="List[RevenueCustomer]",
)
_TOP_REVENUE_CUSTOMERS = Route(
    "POST", "/reports/topRevenueCustomers",
    request_model="Web2LeadRevenueFilter", response_model="List[RevenueCustomer]",
)
_TOP_REVENUE_SALES_REPS = Route(
    "POST", "/reports/topRevenueSalesReps",
    request_model="Web2LeadRevenueFilter", response_model="List[RevenueCustomer]",
)
_REFERRED_BY = Route(
    "POST", "/reports/referredBy",
    request_model="ReferredByReportRequest", response_model="ReferredByReport",
)
_WEB2LEAD = Route(
    "POST", "/reports/web2Lead",
    request_model="Web2LeadV2RequestModel", response_model="Web2LeadReport",
)


class ReportsEndpoint(BaseEndpoint):
    """Report generation (ACPortal API)."""

    def insurance(
        self,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> InsuranceReport:
        """POST /reports/insurance.

        Args:
            start_date: Report start date (ISO 8601).
            end_date: Report end date (ISO 8601).

        Request model: :class:`InsuranceReportRequest`
        """
        body = dict(start_date=start_date, end_date=end_date)
        return self._request(_INSURANCE, json=body)

    def sales(
        self,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
        agent_code: str | None = None,
    ) -> SalesForecastReport:
        """POST /reports/sales.

        Args:
            start_date: Report start date (ISO 8601).
            end_date: Report end date (ISO 8601).
            agent_code: Agent code filter.

        Request model: :class:`SalesForecastReportRequest`
        """
        body = dict(start_date=start_date, end_date=end_date, agent_code=agent_code)
        return self._request(_SALES, json=body)

    def sales_summary(
        self,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> SalesForecastSummary:
        """POST /reports/sales/summary.

        Args:
            start_date: Report start date (ISO 8601).
            end_date: Report end date (ISO 8601).

        Request model: :class:`SalesForecastSummaryRequest`
        """
        body = dict(start_date=start_date, end_date=end_date)
        return self._request(_SALES_SUMMARY, json=body)

    def sales_drilldown(
        self,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[RevenueCustomer]:
        """POST /reports/salesDrilldown.

        Args:
            start_date: Report start date (ISO 8601).
            end_date: Report end date (ISO 8601).

        Request model: :class:`Web2LeadRevenueFilter`
        """
        body = dict(start_date=start_date, end_date=end_date)
        return self._request(_SALES_DRILLDOWN, json=body)

    def top_revenue_customers(
        self,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[RevenueCustomer]:
        """POST /reports/topRevenueCustomers.

        Args:
            start_date: Report start date (ISO 8601).
            end_date: Report end date (ISO 8601).

        Request model: :class:`Web2LeadRevenueFilter`
        """
        body = dict(start_date=start_date, end_date=end_date)
        return self._request(_TOP_REVENUE_CUSTOMERS, json=body)

    def top_revenue_sales_reps(
        self,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[RevenueCustomer]:
        """POST /reports/topRevenueSalesReps.

        Args:
            start_date: Report start date (ISO 8601).
            end_date: Report end date (ISO 8601).

        Request model: :class:`Web2LeadRevenueFilter`
        """
        body = dict(start_date=start_date, end_date=end_date)
        return self._request(_TOP_REVENUE_SALES_REPS, json=body)

    def referred_by(
        self,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> ReferredByReport:
        """POST /reports/referredBy.

        Args:
            start_date: Report start date (ISO 8601).
            end_date: Report end date (ISO 8601).

        Request model: :class:`ReferredByReportRequest`
        """
        body = dict(start_date=start_date, end_date=end_date)
        return self._request(_REFERRED_BY, json=body)

    def web2lead(
        self,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> Web2LeadReport:
        """POST /reports/web2Lead.

        Args:
            start_date: Report start date (ISO 8601).
            end_date: Report end date (ISO 8601).

        Request model: :class:`Web2LeadV2RequestModel`
        """
        body = dict(start_date=start_date, end_date=end_date)
        return self._request(_WEB2LEAD, json=body)
