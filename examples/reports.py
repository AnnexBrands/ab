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
    lambda api, data=None: api.reports.insurance(data=data or {}),
    request_model="InsuranceReportRequest",
    request_fixture_file="InsuranceReportRequest.json",
    response_model="InsuranceReport",
    fixture_file="InsuranceReport.json",
)

runner.add(
    "sales",
    lambda api, data=None: api.reports.sales(data=data or {}),
    request_model="SalesForecastReportRequest",
    request_fixture_file="SalesForecastReportRequest.json",
    response_model="SalesForecastReport",
    fixture_file="SalesForecastReport.json",
)

runner.add(
    "sales_summary",
    lambda api, data=None: api.reports.sales_summary(data=data or {}),
    request_model="SalesForecastSummaryRequest",
    request_fixture_file="SalesForecastSummaryRequest.json",
    response_model="SalesForecastSummary",
    fixture_file="SalesForecastSummary.json",
)

runner.add(
    "sales_drilldown",
    lambda api, data=None: api.reports.sales_drilldown(data=data or {}),
    request_model="Web2LeadRevenueFilter",
    request_fixture_file="Web2LeadRevenueFilter.json",
    response_model="List[RevenueCustomer]",
    fixture_file="RevenueCustomer.json",
)

runner.add(
    "top_revenue_customers",
    lambda api, data=None: api.reports.top_revenue_customers(data=data or {}),
    request_model="Web2LeadRevenueFilter",
    request_fixture_file="Web2LeadRevenueFilter.json",
    response_model="List[RevenueCustomer]",
    fixture_file="RevenueCustomer.json",
)

runner.add(
    "top_revenue_sales_reps",
    lambda api, data=None: api.reports.top_revenue_sales_reps(data=data or {}),
    request_model="Web2LeadRevenueFilter",
    request_fixture_file="Web2LeadRevenueFilter.json",
    response_model="List[RevenueCustomer]",
    fixture_file="RevenueCustomer.json",
)

runner.add(
    "referred_by",
    lambda api, data=None: api.reports.referred_by(data=data or {}),
    request_model="ReferredByReportRequest",
    request_fixture_file="ReferredByReportRequest.json",
    response_model="ReferredByReport",
    fixture_file="ReferredByReport.json",
)

runner.add(
    "web2lead",
    lambda api, data=None: api.reports.web2lead(data=data or {}),
    request_model="Web2LeadV2RequestModel",
    request_fixture_file="Web2LeadV2RequestModel.json",
    response_model="Web2LeadReport",
    fixture_file="Web2LeadReport.json",
)

if __name__ == "__main__":
    runner.run()
