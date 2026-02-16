# Account

```{eval-rst}
.. autoclass:: ab.api.endpoints.account.AccountEndpoint
   :members:
   :undoc-members:
```

## Methods

### Registration & Confirmation

#### register

`POST /account/register` — Register a new account.

**Returns:** {class}`~ab.api.models.account.AccountResponse`

#### send_confirmation / confirm

`POST /account/sendConfirmation|confirm` — Email confirmation flow.

### Password Management

#### forgot / verify_reset_token / reset_password / set_password

`POST /account/forgot|resetpassword|setpassword`, `GET /account/verifyresettoken`

**verify_reset_token Returns:** {class}`~ab.api.models.account.TokenVerification`

### Profile

#### get_profile

`GET /account/profile` — Get current user profile.

**Returns:** {class}`~ab.api.models.account.UserProfile`

```python
profile = api.account.get_profile()
print(profile.email)
```

### Payment Sources

#### update_payment_source / delete_payment_source

`PUT/DELETE /account/paymentsource/{sourceId}`

**Returns:** {class}`~ab.api.models.account.AccountPaymentSource`
