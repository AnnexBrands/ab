"""Example: Company operations."""

from ab import ABConnectAPI

api = ABConnectAPI(env="staging")

# Get a company by UUID
company = api.companies.get_by_id("93179b52-3da9-e311-b6f8-000c298b59ee")
print(f"Company: {company.name}")  # Navis Pack & Ship #14004OH

# Get company details
details = api.companies.get_details("93179b52-3da9-e311-b6f8-000c298b59ee")
print(f"Details: {details}")

# Get full details
full = api.companies.get_fulldetails("93179b52-3da9-e311-b6f8-000c298b59ee")
print(f"Full details: {full}")

# List companies accessible to current user
my_companies = api.companies.available_by_current_user()
print(f"Accessible companies: {len(my_companies) if my_companies else 0}")

# Search companies
results = api.companies.search({"searchText": "Navis"})
print(f"Search results: {results}")
