"""Example: Reports & analytics operations (8 methods).

Covers insurance, sales, sales summary, sales drilldown, top revenue
customers/reps, referred by, and web2lead reports.
"""

from examples._runner import ExampleRunner

runner = ExampleRunner("Reports", env="staging")

# ═══════════════════════════════════════════════════════════════════════
# Report Endpoints
# ═══════════════════════════════════════════════════════════════════════

runner.add(
    "insurance",
    lambda api: api.reports.insurance(startDate="2025-01-01", endDate="2025-12-31"),
    request_model="InsuranceReportRequest",
    response_model="InsuranceReport",
    fixture_file="InsuranceReport.json",
)

runner.add(
    "sales",
    lambda api: api.reports.sales(startDate="2025-01-01", endDate="2025-12-31"),
    request_model="SalesForecastReportRequest",
    response_model="SalesForecastReport",
    fixture_file="SalesForecastReport.json",
)

runner.add(
    "sales_summary",
    lambda api: api.reports.sales_summary(startDate="2025-01-01", endDate="2025-12-31"),
    request_model="SalesForecastSummaryRequest",
    response_model="SalesForecastSummary",
    fixture_file="SalesForecastSummary.json",
)

runner.add(
    "sales_drilldown",
    lambda api: api.reports.sales_drilldown(startDate="2025-01-01", endDate="2025-12-31"),
    request_model="Web2LeadRevenueFilter",
    response_model="List[RevenueCustomer]",
    fixture_file="RevenueCustomer.json",
)

runner.add(
    "top_revenue_customers",
    lambda api: api.reports.top_revenue_customers(startDate="2025-01-01", endDate="2025-12-31"),
    request_model="Web2LeadRevenueFilter",
    response_model="List[RevenueCustomer]",
)

runner.add(
    "top_revenue_sales_reps",
    lambda api: api.reports.top_revenue_sales_reps(startDate="2025-01-01", endDate="2025-12-31"),
    request_model="Web2LeadRevenueFilter",
    response_model="List[RevenueCustomer]",
)

runner.add(
    "referred_by",
    lambda api: api.reports.referred_by(startDate="2025-01-01", endDate="2025-12-31"),
    request_model="ReferredByReportRequest",
    response_model="ReferredByReport",
    fixture_file="ReferredByReport.json",
)

runner.add(
    "web2lead",
    lambda api: api.reports.web2lead(startDate="2025-01-01", endDate="2025-12-31"),
    request_model="Web2LeadV2RequestModel",
    response_model="Web2LeadReport",
    fixture_file="Web2LeadReport.json",
)

if __name__ == "__main__":
    runner.run()
