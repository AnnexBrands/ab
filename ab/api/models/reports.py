"""Report models for the ACPortal API."""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


class InsuranceReportRequest(RequestModel):
    """Filter for POST /reports/insurance."""

    start_date: Optional[str] = Field(None, alias="startDate", description="Start date")
    end_date: Optional[str] = Field(None, alias="endDate", description="End date")


class InsuranceReport(ResponseModel):
    """Insurance report result — POST /reports/insurance."""

    claims: Optional[List[dict]] = Field(None, description="Insurance claims")
    total_amount: Optional[float] = Field(None, alias="totalAmount", description="Total amount")
    by_status: Optional[List[dict]] = Field(None, alias="byStatus", description="Breakdown by status")


class SalesForecastReportRequest(RequestModel):
    """Filter for POST /reports/sales."""

    start_date: Optional[str] = Field(None, alias="startDate", description="Start date")
    end_date: Optional[str] = Field(None, alias="endDate", description="End date")
    agent_code: Optional[str] = Field(None, alias="agentCode", description="Agent code filter")


class SalesForecastReport(ResponseModel):
    """Sales forecast result — POST /reports/sales."""

    projected_revenue: Optional[float] = Field(None, alias="projectedRevenue", description="Projected revenue")
    actual_revenue: Optional[float] = Field(None, alias="actualRevenue", description="Actual revenue")
    by_rep: Optional[List[dict]] = Field(None, alias="byRep", description="Breakdown by sales rep")


class SalesForecastSummaryRequest(RequestModel):
    """Filter for POST /reports/sales/summary."""

    start_date: Optional[str] = Field(None, alias="startDate", description="Start date")
    end_date: Optional[str] = Field(None, alias="endDate", description="End date")


class SalesForecastSummary(ResponseModel):
    """Sales summary result — POST /reports/sales/summary."""

    total_revenue: Optional[float] = Field(None, alias="totalRevenue", description="Total revenue")
    count: Optional[int] = Field(None, description="Record count")


class Web2LeadRevenueFilter(RequestModel):
    """Filter for POST /reports/salesDrilldown, topRevenueCustomers, topRevenueSalesReps."""

    start_date: Optional[str] = Field(None, alias="startDate", description="Start date")
    end_date: Optional[str] = Field(None, alias="endDate", description="End date")


class RevenueCustomer(ResponseModel):
    """Revenue by customer or sales rep — POST /reports/topRevenueCustomers etc."""

    name: Optional[str] = Field(None, description="Customer or rep name")
    total_revenue: Optional[float] = Field(None, alias="totalRevenue", description="Total revenue")
    job_count: Optional[int] = Field(None, alias="jobCount", description="Number of jobs")
    average_value: Optional[float] = Field(None, alias="averageValue", description="Average job value")


class ReferredByReportRequest(RequestModel):
    """Filter for POST /reports/referredBy."""

    start_date: Optional[str] = Field(None, alias="startDate", description="Start date")
    end_date: Optional[str] = Field(None, alias="endDate", description="End date")


class ReferredByReport(ResponseModel):
    """Referral report result — POST /reports/referredBy."""

    referrals: Optional[List[dict]] = Field(None, description="Referral entries")
    by_source: Optional[List[dict]] = Field(None, alias="bySource", description="Breakdown by source")


class Web2LeadV2RequestModel(RequestModel):
    """Filter for POST /reports/web2Lead."""

    start_date: Optional[str] = Field(None, alias="startDate", description="Start date")
    end_date: Optional[str] = Field(None, alias="endDate", description="End date")


class Web2LeadReport(ResponseModel):
    """Web lead report result — POST /reports/web2Lead."""

    leads: Optional[List[dict]] = Field(None, description="Lead entries")
    by_campaign: Optional[List[dict]] = Field(None, alias="byCampaign", description="Breakdown by campaign")
