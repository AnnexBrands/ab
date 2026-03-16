# Sellers

```{eval-rst}
.. autoclass:: ab.api.endpoints.sellers.SellersEndpoint
   :members:
   :undoc-members:
```

## Methods

### create

`POST /Seller` — Create a new seller.

```python
from ab import ABConnectAPI

api = ABConnectAPI(env="staging")
api.sellers.create({"name": "New Seller"})
```

### list

`GET /Seller` — List sellers with optional filters (paginated).

**Returns:** {class}`~ab.api.models.shared.PaginatedList`\[{class}`~ab.api.models.sellers.SellerExpandedDto`\]

```python
# List all sellers
sellers = api.sellers.list(page_number=1, page_size=25)

# Filter by active status
sellers = api.sellers.list(is_active=True)
```

### get

`GET /Seller/{id}` — Get a seller by ID.

**Returns:** {class}`~ab.api.models.sellers.SellerExpandedDto`

```python
seller = api.sellers.get(1)
print(seller.name)
```

### update

`PUT /Seller/{id}` — Update a seller.

```python
api.sellers.update(1, {"name": "Updated Seller"})
```

### delete

`DELETE /Seller/{id}` — Delete a seller.

```python
api.sellers.delete(1)
```
