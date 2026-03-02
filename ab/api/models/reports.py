"""Report models for the ACPortal API."""

from __future__ import annotations

from typing import Optional

from pydantic import Field

from ab.api.models.base import ResponseModel
from ab.api.models.mixins import DateRangeRequestMixin


class InsuranceReportRequest(DateRangeRequestMixin):
    """Filter for POST /reports/insurance."""

    page_no: Optional[int] = Field(None, alias="pageNo", description="Page number")
    page_size: Optional[int] = Field(None, alias="pageSize", description="Items per page")
    sort_by: Optional[dict] = Field(None, alias="sortBy", description="Sort config {sortByField: int, sortDir: bool}")


class InsuranceReport(ResponseModel):
    """Insurance report row — POST /reports/insurance.

    Source: InsuranceReportModel.cs + swagger InsuranceReport.
    """

    job_number: Optional[str] = Field(None, alias="jobNumber", description="Job display number")
    franchisee: Optional[str] = Field(None, description="Franchisee code")
    insurance_type: Optional[str] = Field(None, alias="insuranceType", description="Insurance type")
    no_of_piece: Optional[int] = Field(None, alias="noOfPiece", description="Number of pieces")
    total_cost: Optional[float] = Field(None, alias="totalCost", description="Total declared value")
    job_date: Optional[str] = Field(None, alias="jobDate", description="Job date")
    insurance_cost: Optional[float] = Field(None, alias="insuranceCost", description="Insurance cost")
    carrier: Optional[str] = Field(None, description="Carrier name")
    intacct_date: Optional[str] = Field(None, alias="intacctDate", description="Intacct sync date")
    total_records: Optional[int] = Field(None, alias="totalRecords", description="Total record count")


class SalesForecastReportRequest(DateRangeRequestMixin):
    """Filter for POST /reports/sales."""

    agent_code: Optional[str] = Field(None, alias="agentCode", description="Agent code filter")
    page_no: Optional[int] = Field(None, alias="pageNo", description="Page number")
    page_size: Optional[int] = Field(None, alias="pageSize", description="Items per page")
    sort_by: Optional[dict] = Field(None, alias="sortBy", description="Sort config {sortByField: int, sortDir: bool}")


class SalesForecastReport(ResponseModel):
    """Sales forecast row — POST /reports/sales.

    Source: Salesforecast.cs + swagger SalesForecastReport.
    """

    franchisee: Optional[str] = Field(None, description="Franchisee code")
    company: Optional[str] = Field(None, description="Company name")
    job_id: Optional[str] = Field(None, alias="jobID", description="Job display ID")
    job_type: Optional[str] = Field(None, alias="jobType", description="Job type")
    quote_date: Optional[str] = Field(None, alias="quoteDate", description="Quote date")
    booked_date: Optional[str] = Field(None, alias="bookedDate", description="Booked date")
    revenue: Optional[float] = Field(None, description="Revenue amount")
    profit: Optional[float] = Field(None, description="Profit amount")
    gross_margin: Optional[float] = Field(None, alias="grossMargin", description="Gross margin percentage")
    status: Optional[str] = Field(None, description="Job status")
    industry: Optional[str] = Field(None, description="Industry type")
    customer_zip_code: Optional[str] = Field(None, alias="customerZipCode", description="Customer zip code")
    intacct_date: Optional[str] = Field(None, alias="intacctDate", description="Intacct sync date")
    total_records: Optional[int] = Field(None, alias="totalRecords", description="Total record count")


class SalesForecastSummaryRequest(DateRangeRequestMixin):
    """Filter for POST /reports/sales/summary."""


class SalesForecastSummary(ResponseModel):
    """Sales summary — POST /reports/sales/summary.

    Source: swagger SalesForecastSummary (subset of Salesforecast.cs).
    """

    revenue: Optional[float] = Field(None, description="Total revenue")
    profit: Optional[float] = Field(None, description="Total profit")
    gross_margin: Optional[float] = Field(None, alias="grossMargin", description="Gross margin percentage")
    close_ratio: Optional[float] = Field(None, alias="closeRatio", description="Close ratio")


class Web2LeadRevenueFilter(DateRangeRequestMixin):
    """Filter for POST /reports/salesDrilldown, topRevenueCustomers, topRevenueSalesReps."""

    user_id: Optional[str] = Field(None, alias="userID", description="User/franchisee ID")


class RevenueCustomer(ResponseModel):
    """Revenue by customer or sales rep — POST /reports/topRevenueCustomers etc.

    Source: RevenueCustomer.cs — simple 2-field model.
    """

    id: Optional[str] = Field(None, description="Customer or rep ID")
    name: Optional[str] = Field(None, description="Customer or rep name")


class ReferredByReportRequest(DateRangeRequestMixin):
    """Filter for POST /reports/referredBy."""

    page_no: Optional[int] = Field(None, alias="pageNo", description="Page number")
    page_size: Optional[int] = Field(None, alias="pageSize", description="Items per page")
    sort_by: Optional[dict] = Field(None, alias="sortBy", description="Sort config {sortByField: int, sortDir: bool}")


class ReferredByReport(ResponseModel):
    """Referral report row — POST /reports/referredBy.

    Source: ReferedData.cs + swagger ReferredByReport.
    """

    referred_by: Optional[str] = Field(None, alias="referredBy", description="Referral source")
    referred_name: Optional[str] = Field(None, alias="referredName", description="Referral contact name")
    referred_by_category: Optional[str] = Field(None, alias="referredByCategory", description="Referral category")
    quote_date: Optional[str] = Field(None, alias="quoteDate", description="Quote date")
    booked_date: Optional[str] = Field(None, alias="bookedDate", description="Booked date")
    revenue: Optional[float] = Field(None, description="Revenue amount")
    profit: Optional[float] = Field(None, description="Profit amount")
    customer: Optional[str] = Field(None, description="Customer name")
    job_display_id: Optional[int] = Field(None, alias="jobDisplayID", description="Job display ID")
    industry: Optional[str] = Field(None, description="Industry type")
    customer_zip_code: Optional[str] = Field(None, alias="customerZipCode", description="Customer zip code")
    intacct_date: Optional[str] = Field(None, alias="intacctDate", description="Intacct sync date")
    total_records: Optional[int] = Field(None, alias="totalRecords", description="Total record count")


class Web2LeadV2RequestModel(DateRangeRequestMixin):
    """Filter for POST /reports/web2Lead."""

    page_no: Optional[int] = Field(None, alias="pageNo", description="Page number")
    page_size: Optional[int] = Field(None, alias="pageSize", description="Items per page")
    sort_by: Optional[dict] = Field(None, alias="sortBy", description="Sort config {sortByField: int, sortDir: bool}")


class Web2LeadReport(ResponseModel):
    """Web lead report row — POST /reports/web2Lead.

    Source: Web2Lead.cs + swagger Web2LeadReport.
    """

    franchisee_id: Optional[str] = Field(None, alias="franchiseeID", description="Franchisee ID")
    type: Optional[str] = Field(None, description="Lead type")
    job_display_id: Optional[str] = Field(None, alias="jobDisplayID", description="Job display ID")
    intacct_status: Optional[str] = Field(None, alias="intacctStatus", description="Intacct status")
    lead_date: Optional[str] = Field(None, alias="leadDate", description="Lead creation date")
    company_name: Optional[str] = Field(None, alias="companyName", description="Company name")
    refer_page: Optional[str] = Field(None, alias="referPage", description="Referring page URL")
    entry_url: Optional[str] = Field(None, alias="entryURL", description="Entry URL")
    submission_page: Optional[str] = Field(None, alias="submissionPage", description="Submission page URL")
    how_heard: Optional[str] = Field(None, alias="howHeard", description="How customer heard of us")
    email: Optional[str] = Field(None, description="Contact email")
    phone: Optional[str] = Field(None, description="Contact phone")
    ship_from: Optional[str] = Field(None, alias="shipFrom", description="Ship from location")
    ship_to: Optional[str] = Field(None, alias="shipTo", description="Ship to location")
    referred_name: Optional[str] = Field(None, alias="referredName", description="Referral name")
    customer_comments: Optional[str] = Field(None, alias="customerComments", description="Customer comments")
    current_book_price: Optional[float] = Field(None, alias="currentBookPrice", description="Current booked price")
    current_book_profit: Optional[float] = Field(None, alias="currentBookProfit", description="Current booked profit")
    referred_by_category: Optional[str] = Field(None, alias="referredByCategory", description="Referral category")
    total_records: Optional[int] = Field(None, alias="totalRecords", description="Total record count")
