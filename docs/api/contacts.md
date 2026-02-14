# Contacts

```{eval-rst}
.. autoclass:: ab.api.endpoints.contacts.ContactsEndpoint
   :members:
   :undoc-members:
```

## Methods

### get

`GET /contacts/{id}` — Get a contact by ID.

**Returns:** {class}`~ab.api.models.contacts.ContactSimple`

```python
from ab import ABConnectAPI

api = ABConnectAPI(env="staging")
contact = api.contacts.get("30760")
print(contact.first_name, contact.last_name)
```

### get_details

`GET /contacts/{contactId}/editdetails` — Full editable contact details.

**Returns:** {class}`~ab.api.models.contacts.ContactDetailedInfo`

```python
details = api.contacts.get_details("30760")
print(details.emails)
```

### update_details

`PUT /contacts/{contactId}/editdetails` — Update contact details.

```python
api.contacts.update_details("30760", {"firstName": "Jane", "lastName": "Doe"})
```

### create

`POST /contacts/editdetails` — Create a new contact.

```python
api.contacts.create({"firstName": "New", "lastName": "Contact", "email": "new@example.com"})
```

### search

`POST /contacts/v2/search` — Search contacts.

**Returns:** `list[`{class}`~ab.api.models.contacts.SearchContactEntityResult`]`

```python
results = api.contacts.search({"searchText": "Justine"})
```

### get_primary_details

`GET /contacts/{contactId}/primarydetails` — Primary contact info.

**Returns:** {class}`~ab.api.models.contacts.ContactPrimaryDetails`

```python
primary = api.contacts.get_primary_details("30760")
print(primary.full_name, primary.email)
```

### get_current_user

`GET /contacts/user` — Current authenticated user's contact info.

**Returns:** {class}`~ab.api.models.contacts.ContactSimple`

```python
me = api.contacts.get_current_user()
print(me.full_name)
```
