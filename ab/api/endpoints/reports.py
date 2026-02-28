"""Reports API endpoints (8 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab.api.models.reports import (
        InsuranceReport,
        InsuranceReportRequest,
        ReferredByReport,
        ReferredByReportRequest,
        RevenueCustomer,
        SalesForecastReport,
        SalesForecastReportRequest,
        SalesForecastSummary,
        SalesForecastSummaryRequest,
        Web2LeadReport,
        Web2LeadRevenueFilter,
        Web2LeadV2RequestModel,
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

    def insurance(self, *, data: InsuranceReportRequest | dict) -> InsuranceReport:
        """POST /reports/insurance.

        Args:
            data: Insurance report payload with date range filters.
                Accepts an :class:`InsuranceReportRequest` instance or a dict.

        Request model: :class:`InsuranceReportRequest`
        """
        return self._request(_INSURANCE, json=data)

    def sales(self, *, data: SalesForecastReportRequest | dict) -> SalesForecastReport:
        """POST /reports/sales.

        Args:
            data: Sales forecast payload with date range and agent code
                filters. Accepts a :class:`SalesForecastReportRequest`
                instance or a dict.

        Request model: :class:`SalesForecastReportRequest`
        """
        return self._request(_SALES, json=data)

    def sales_summary(self, *, data: SalesForecastSummaryRequest | dict) -> SalesForecastSummary:
        """POST /reports/sales/summary.

        Args:
            data: Sales forecast summary payload with date range filters.
                Accepts a :class:`SalesForecastSummaryRequest` instance
                or a dict.

        Request model: :class:`SalesForecastSummaryRequest`
        """
        return self._request(_SALES_SUMMARY, json=data)

    def sales_drilldown(self, *, data: Web2LeadRevenueFilter | dict) -> list[RevenueCustomer]:
        """POST /reports/salesDrilldown.

        Args:
            data: Revenue filter payload with date range filters.
                Accepts a :class:`Web2LeadRevenueFilter` instance or a dict.

        Request model: :class:`Web2LeadRevenueFilter`
        """
        return self._request(_SALES_DRILLDOWN, json=data)

    def top_revenue_customers(self, *, data: Web2LeadRevenueFilter | dict) -> list[RevenueCustomer]:
        """POST /reports/topRevenueCustomers.

        Args:
            data: Revenue filter payload with date range filters.
                Accepts a :class:`Web2LeadRevenueFilter` instance or a dict.

        Request model: :class:`Web2LeadRevenueFilter`
        """
        return self._request(_TOP_REVENUE_CUSTOMERS, json=data)

    def top_revenue_sales_reps(self, *, data: Web2LeadRevenueFilter | dict) -> list[RevenueCustomer]:
        """POST /reports/topRevenueSalesReps.

        Args:
            data: Revenue filter payload with date range filters.
                Accepts a :class:`Web2LeadRevenueFilter` instance or a dict.

        Request model: :class:`Web2LeadRevenueFilter`
        """
        return self._request(_TOP_REVENUE_SALES_REPS, json=data)

    def referred_by(self, *, data: ReferredByReportRequest | dict) -> ReferredByReport:
        """POST /reports/referredBy.

        Args:
            data: Referred-by report payload with date range filters.
                Accepts a :class:`ReferredByReportRequest` instance or a dict.

        Request model: :class:`ReferredByReportRequest`
        """
        return self._request(_REFERRED_BY, json=data)

    def web2lead(self, *, data: Web2LeadV2RequestModel | dict) -> Web2LeadReport:
        """POST /reports/web2Lead.

        Args:
            data: Web2Lead report payload with date range filters.
                Accepts a :class:`Web2LeadV2RequestModel` instance or a dict.

        Request model: :class:`Web2LeadV2RequestModel`
        """
        return self._request(_WEB2LEAD, json=data)
