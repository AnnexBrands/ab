# Users

```{eval-rst}
.. autoclass:: ab.api.endpoints.users.UsersEndpoint
   :members:
   :undoc-members:
```

## Methods

### list

`POST /users/list` — List users (paginated).

**Returns:** `list[`{class}`~ab.api.models.users.User`]`

```python
from ab import ABConnectAPI

api = ABConnectAPI(env="staging")
users = api.users.list({"page": 1, "pageSize": 10})
```

### get_roles

`GET /users/roles` — List all user roles.

**Returns:** `list[str]`

```python
roles = api.users.get_roles()
for role in roles:
    print(role)
```

### create

`POST /users/user` — Create a new user.

```python
api.users.create({"username": "newuser", "email": "new@example.com", "roles": ["role-id"]})
```

### update

`PUT /users/user` — Update a user.

```python
api.users.update({"id": "user-id", "email": "updated@example.com"})
```
