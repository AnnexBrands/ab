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

### get_did

Resolve a contact display ID through the cache resolver, then call `GET /contacts/{id}`.

**Returns:** {class}`~ab.api.models.contacts.ContactSimple`

```python
from examples.constants import TEST_CONTACT_DID

contact = api.contacts.get_did(TEST_CONTACT_DID)
print(contact.id, contact.contact_display_id)
```

### get_details

`GET /contacts/{contactId}/editdetails` — Full editable contact details.

**Returns:** {class}`~ab.api.models.contacts.ContactDetailedInfo`

```python
details = api.contacts.get_details("30760")
print(details.full_name, details.contact_display_id)

# Typed nested lists with IDE autocomplete
for entry in details.emails_list or []:
    print(entry.email.email, entry.meta_data)

for entry in details.phones_list or []:
    print(entry.phone.phone, entry.meta_data)

for entry in details.addresses_list or []:
    print(entry.address.city, entry.address.state)
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
from ab.api.models.contacts import ContactSearchRequest, ContactSearchParams, PageOrderedRequest

results = api.contacts.search(data=ContactSearchRequest(
    main_search_request=ContactSearchParams(full_name="Justine"),
    load_options=PageOrderedRequest(page_number=1, page_size=10),
))
for r in results:
    print(r.contact_full_name, r.contact_email, r.company_name)
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
