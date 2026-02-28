"""Report models for the ACPortal API."""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ab.api.models.base import ResponseModel
from ab.api.models.mixins import DateRangeRequestMixin


class InsuranceReportRequest(DateRangeRequestMixin):
    """Filter for POST /reports/insurance."""


class InsuranceReport(ResponseModel):
    """Insurance report result — POST /reports/insurance."""

    claims: Optional[List[dict]] = Field(None, description="Insurance claims")
    total_amount: Optional[float] = Field(None, alias="totalAmount", description="Total amount")
    by_status: Optional[List[dict]] = Field(None, alias="byStatus", description="Breakdown by status")


class SalesForecastReportRequest(DateRangeRequestMixin):
    """Filter for POST /reports/sales."""

    agent_code: Optional[str] = Field(None, alias="agentCode", description="Agent code filter")


class SalesForecastReport(ResponseModel):
    """Sales forecast result — POST /reports/sales."""

    projected_revenue: Optional[float] = Field(None, alias="projectedRevenue", description="Projected revenue")
    actual_revenue: Optional[float] = Field(None, alias="actualRevenue", description="Actual revenue")
    by_rep: Optional[List[dict]] = Field(None, alias="byRep", description="Breakdown by sales rep")


class SalesForecastSummaryRequest(DateRangeRequestMixin):
    """Filter for POST /reports/sales/summary."""


class SalesForecastSummary(ResponseModel):
    """Sales summary result — POST /reports/sales/summary."""

    total_revenue: Optional[float] = Field(None, alias="totalRevenue", description="Total revenue")
    count: Optional[int] = Field(None, description="Record count")


class Web2LeadRevenueFilter(DateRangeRequestMixin):
    """Filter for POST /reports/salesDrilldown, topRevenueCustomers, topRevenueSalesReps."""


class RevenueCustomer(ResponseModel):
    """Revenue by customer or sales rep — POST /reports/topRevenueCustomers etc."""

    name: Optional[str] = Field(None, description="Customer or rep name")
    total_revenue: Optional[float] = Field(None, alias="totalRevenue", description="Total revenue")
    job_count: Optional[int] = Field(None, alias="jobCount", description="Number of jobs")
    average_value: Optional[float] = Field(None, alias="averageValue", description="Average job value")


class ReferredByReportRequest(DateRangeRequestMixin):
    """Filter for POST /reports/referredBy."""


class ReferredByReport(ResponseModel):
    """Referral report result — POST /reports/referredBy."""

    referrals: Optional[List[dict]] = Field(None, description="Referral entries")
    by_source: Optional[List[dict]] = Field(None, alias="bySource", description="Breakdown by source")


class Web2LeadV2RequestModel(DateRangeRequestMixin):
    """Filter for POST /reports/web2Lead."""


class Web2LeadReport(ResponseModel):
    """Web lead report result — POST /reports/web2Lead."""

    leads: Optional[List[dict]] = Field(None, description="Lead entries")
    by_campaign: Optional[List[dict]] = Field(None, alias="byCampaign", description="Breakdown by campaign")
