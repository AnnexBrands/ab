# SMS Templates

```{eval-rst}
.. autoclass:: ab.api.endpoints.sms_templates.SmsTemplateEndpoint
   :members:
   :undoc-members:
```

## Methods

### list

`GET /SmsTemplate/list` — List SMS templates (optionally by company).

**Returns:** `list[`{class}`~ab.api.models.sms_templates.SmsTemplate`]`

```python
templates = api.sms_templates.list(companyId="company-uuid")
```

### get_notification_tokens

`GET /SmsTemplate/notificationTokens` — Available notification tokens.

**Returns:** {class}`~ab.api.models.sms_templates.NotificationTokens`

### save / get / delete

`POST /SmsTemplate/save`, `GET/DELETE /SmsTemplate/{templateId}`
