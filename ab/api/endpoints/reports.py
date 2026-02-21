"""Reports API endpoints (8 routes)."""

from __future__ import annotations

from typing import Any

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

    def insurance(self, **kwargs: Any) -> Any:
        """POST /reports/insurance"""
        return self._request(_INSURANCE, json=kwargs)

    def sales(self, **kwargs: Any) -> Any:
        """POST /reports/sales"""
        return self._request(_SALES, json=kwargs)

    def sales_summary(self, **kwargs: Any) -> Any:
        """POST /reports/sales/summary"""
        return self._request(_SALES_SUMMARY, json=kwargs)

    def sales_drilldown(self, **kwargs: Any) -> Any:
        """POST /reports/salesDrilldown"""
        return self._request(_SALES_DRILLDOWN, json=kwargs)

    def top_revenue_customers(self, **kwargs: Any) -> Any:
        """POST /reports/topRevenueCustomers"""
        return self._request(_TOP_REVENUE_CUSTOMERS, json=kwargs)

    def top_revenue_sales_reps(self, **kwargs: Any) -> Any:
        """POST /reports/topRevenueSalesReps"""
        return self._request(_TOP_REVENUE_SALES_REPS, json=kwargs)

    def referred_by(self, **kwargs: Any) -> Any:
        """POST /reports/referredBy"""
        return self._request(_REFERRED_BY, json=kwargs)

    def web2lead(self, **kwargs: Any) -> Any:
        """POST /reports/web2Lead"""
        return self._request(_WEB2LEAD, json=kwargs)
