"""Example: Reports & analytics operations.

Live SDK example — real call, real printed pydantic response. Migrated from the
deprecated runner (examples/_reports.py) to the plain-script form.

All report endpoints are POST but READ-ONLY (they only run a query and return
rows), so every call is unguarded. Each takes a request-body model via
``data=...`` — the bodies come from committed request fixtures.

See also: https://ab-sdk.readthedocs.io/en/latest/api/reports.html
"""

from __future__ import annotations

from ab import ABConnectAPI
from ab.cli.formatter import format_result
from examples._capture import load_request, save


def main() -> None:
    api = ABConnectAPI(env="staging")

    # POST /reports/insurance
    print("\n# api.reports.insurance(data=...)")
    result = api.reports.insurance(data=load_request("InsuranceReportRequest.json"))
    print(format_result(result))
    save("InsuranceReport.json", result)

    # POST /reports/sales
    print("\n# api.reports.sales(data=...)")
    result = api.reports.sales(data=load_request("SalesForecastReportRequest.json"))
    print(format_result(result))
    save("SalesForecastReport.json", result)

    # POST /reports/sales/summary
    print("\n# api.reports.sales_summary(data=...)")
    result = api.reports.sales_summary(data=load_request("SalesForecastSummaryRequest.json"))
    print(format_result(result))
    save("SalesForecastSummary.json", result)

    # POST /reports/salesDrilldown
    print("\n# api.reports.sales_drilldown(data=...)")
    result = api.reports.sales_drilldown(data=load_request("Web2LeadRevenueFilter.json"))
    print(format_result(result))
    save("RevenueCustomer.json", result)

    # POST /reports/topRevenueCustomers
    print("\n# api.reports.top_revenue_customers(data=...)")
    result = api.reports.top_revenue_customers(data=load_request("Web2LeadRevenueFilter.json"))
    print(format_result(result))
    save("RevenueCustomer.json", result)

    # POST /reports/topRevenueSalesReps
    print("\n# api.reports.top_revenue_sales_reps(data=...)")
    result = api.reports.top_revenue_sales_reps(data=load_request("Web2LeadRevenueFilter.json"))
    print(format_result(result))
    save("RevenueCustomer.json", result)

    # POST /reports/referredBy
    print("\n# api.reports.referred_by(data=...)")
    result = api.reports.referred_by(data=load_request("ReferredByReportRequest.json"))
    print(format_result(result))
    save("ReferredByReport.json", result)

    # POST /reports/web2Lead
    print("\n# api.reports.web2lead(data=...)")
    result = api.reports.web2lead(data=load_request("Web2LeadV2RequestModel.json"))
    print(format_result(result))
    save("Web2LeadReport.json", result)


if __name__ == "__main__":
    main()
