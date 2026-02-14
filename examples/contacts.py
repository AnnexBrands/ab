"""Example: Contact operations."""

from ab import ABConnectAPI

api = ABConnectAPI(env="staging")

# Get current user's contact info
me = api.contacts.get_current_user()
print(f"Current user: {me.full_name}")

# Get a specific contact
contact = api.contacts.get("30760")
print(f"Contact: {contact}")

# Get contact details (editable form)
details = api.contacts.get_details("30760")
print(f"Details: {details}")

# Get primary details
primary = api.contacts.get_primary_details("30760")
print(f"Primary: {primary.full_name} - {primary.email}")

# Search contacts
results = api.contacts.search({"searchText": "Justine"})
print(f"Search results: {results}")
