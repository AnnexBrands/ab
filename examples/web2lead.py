"""Example: Web2Lead operations (requires ABC API access_key)."""

from ab import ABConnectAPI

api = ABConnectAPI(env="staging")

# Get Web2Lead configuration
config = api.web2lead.get()
print(f"Web2Lead config: {config}")

# Submit a lead (uncomment to run)
# result = api.web2lead.post({
#     "companyCode": "14004OH",
#     "firstName": "John",
#     "lastName": "Doe",
#     "email": "john@example.com",
# })
# print(f"Lead submitted: {result}")
