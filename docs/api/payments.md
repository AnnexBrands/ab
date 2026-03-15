# Payments

```{eval-rst}
.. autoclass:: ab.api.endpoints.payments.PaymentsEndpoint
   :members:
   :undoc-members:
```

## Methods

### get

`GET /job/{jobDisplayId}/payment` — Get payment information for a job.

**Returns:** {class}`~ab.api.models.payments.PaymentInfo`

```python
info = api.payments.get(job_display_id)
```

### get_sources

`GET /job/{jobDisplayId}/payment/sources` — List payment sources.

**Returns:** `list[`{class}`~ab.api.models.payments.PaymentSource`]`

### pay_by_source / set_bank_source

`POST /job/{jobDisplayId}/payment/bysource` and `POST .../banksource` — Execute payment.

**Returns:** {class}`~ab.api.models.shared.ServiceBaseResponse`

### ACH operations

`POST .../ACHCreditTransfer`, `POST .../attachCustomerBank`, `POST .../verifyJobACHSource`, `POST .../cancelJobACHVerification` — ACH payment workflow.

**Returns:** {class}`~ab.api.models.shared.ServiceBaseResponse`
