"""Example: Job operations."""

from ab import ABConnectAPI

api = ABConnectAPI(env="staging")

# Search for jobs
results = api.jobs.search()
print(f"Jobs found: {results}")

# Search by detail criteria
detailed = api.jobs.search_by_details({"searchText": "test"})
print(f"Detailed search: {detailed}")
