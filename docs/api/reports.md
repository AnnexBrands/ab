# Reports

```{eval-rst}
.. autoclass:: ab.api.endpoints.reports.ReportsEndpoint
   :members:
   :undoc-members:
```

## Methods

### insurance

`POST /reports/insurance` — Generate insurance report.

**Returns:** {class}`~ab.api.models.reports.InsuranceReport`

```python
report = api.reports.insurance(startDate="2025-01-01", endDate="2025-12-31")
```

### sales

`POST /reports/sales` — Generate sales forecast report.

**Returns:** {class}`~ab.api.models.reports.SalesForecastReport`

```python
report = api.reports.sales(startDate="2025-01-01", endDate="2025-12-31")
```

### sales_summary

`POST /reports/sales/summary` — Sales summary.

**Returns:** {class}`~ab.api.models.reports.SalesForecastSummary`

### sales_drilldown

`POST /reports/salesDrilldown` — Sales drilldown by customer/rep.

**Returns:** `list[`{class}`~ab.api.models.reports.RevenueCustomer`]`

### top_revenue_customers

`POST /reports/topRevenueCustomers` — Top revenue customers.

**Returns:** `list[`{class}`~ab.api.models.reports.RevenueCustomer`]`

### top_revenue_sales_reps

`POST /reports/topRevenueSalesReps` — Top revenue sales reps.

**Returns:** `list[`{class}`~ab.api.models.reports.RevenueCustomer`]`

### referred_by

`POST /reports/referredBy` — Referral source report.

**Returns:** {class}`~ab.api.models.reports.ReferredByReport`

### web2lead

`POST /reports/web2Lead` — Web lead report.

**Returns:** {class}`~ab.api.models.reports.Web2LeadReport`
