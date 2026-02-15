# RFQ

```{eval-rst}
.. autoclass:: ab.api.endpoints.rfq.RFQEndpoint
   :members:
   :undoc-members:
```

## Methods

### get

`GET /rfq/{rfqId}` — Retrieve a single RFQ by ID.

**Returns:** {class}`~ab.api.models.rfq.QuoteRequestDisplayInfo`

```python
rfq = api.rfq.get("rfq-uuid-here")
print(rfq.status, rfq.quoted_price)
```

### get_for_job

`GET /rfq/forjob/{jobId}` — List all RFQs for a job.

**Returns:** `list[`{class}`~ab.api.models.rfq.QuoteRequestDisplayInfo`]`

```python
rfqs = api.rfq.get_for_job("job-uuid")
```

### accept

`POST /rfq/{rfqId}/accept` — Accept an RFQ quote.

```python
api.rfq.accept("rfq-uuid", notes="Accepted")
```

### decline

`POST /rfq/{rfqId}/decline` — Decline an RFQ quote.

```python
api.rfq.decline("rfq-uuid")
```

### cancel

`POST /rfq/{rfqId}/cancel` — Cancel an RFQ.

```python
api.rfq.cancel("rfq-uuid")
```

### accept_winner

`POST /rfq/{rfqId}/acceptwinner` — Accept the winning quote.

```python
api.rfq.accept_winner("rfq-uuid")
```

### add_comment

`POST /rfq/{rfqId}/comment` — Add a comment to an RFQ.

```python
api.rfq.add_comment("rfq-uuid", notes="Follow-up comment")
```

## Job-Scoped RFQ Methods

These methods are on {class}`~ab.api.endpoints.jobs.JobsEndpoint`:

- `api.jobs.list_rfqs(job_display_id)` — `GET /job/{id}/rfq`
- `api.jobs.get_rfq_status(job_display_id, service_type, company_id)` — `GET /job/{id}/rfq/statusof/{type}/forcompany/{id}`
