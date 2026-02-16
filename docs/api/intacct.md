# Intacct

```{eval-rst}
.. autoclass:: ab.api.endpoints.intacct.IntacctEndpoint
   :members:
   :undoc-members:
```

## Methods

### get

`GET /jobintacct/{jobDisplayId}` — Get Intacct data for a job.

**Returns:** {class}`~ab.api.models.intacct.JobIntacctData`

### save / save_draft

`POST /jobintacct/{jobDisplayId}[/draft]` — Save or draft Intacct data.

### apply_rebate

`POST /jobintacct/{jobDisplayId}/applyRebate` — Apply rebate to job.

### delete_franchisee

`DELETE /jobintacct/{jobDisplayId}/{franchiseeId}` — Remove franchisee Intacct entry.
