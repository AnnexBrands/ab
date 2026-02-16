# ABC Reports

```{eval-rst}
.. autoclass:: ab.api.endpoints.abc_reports.ABCReportsEndpoint
   :members:
   :undoc-members:
```

## Methods

Reporting and log endpoints on the ABC API surface.

### get_web_revenue

`GET /Report/webrevenue` — Get web revenue report.

```python
revenue = api.abc_reports.get_web_revenue(
    accessKey="key", startDate="2026-01-01", endDate="2026-02-01"
)
```

### flush_log_buffer

`POST /logbuffer/flush` — Flush the ABC log buffer.
