# Notifications

```{eval-rst}
.. autoclass:: ab.api.endpoints.notifications.NotificationsEndpoint
   :members:
   :undoc-members:
```

## Methods

### get_all

`GET /notifications` — Get all notifications.

**Returns:** `list[`{class}`~ab.api.models.notifications.Notification`]`

```python
notifications = api.notifications.get_all()
```
