# Base Models & Mixins

## Base Models

```{eval-rst}
.. autoclass:: ab.api.models.base.ABConnectBaseModel
   :members:

.. autoclass:: ab.api.models.base.RequestModel
   :members:
   :show-inheritance:

.. autoclass:: ab.api.models.base.ResponseModel
   :members:
   :show-inheritance:
```

### Design Notes

- **RequestModel** uses `extra="forbid"` — unknown fields cause a validation error
- **ResponseModel** uses `extra="allow"` — unknown fields are stored in `model_extra` and logged as warnings (drift detection)
- All models use `populate_by_name=True` and `alias_generator=to_camel` for camelCase JSON interop

## Mixins

```{eval-rst}
.. autoclass:: ab.api.models.mixins.IdentifiedModel
   :members:

.. autoclass:: ab.api.models.mixins.TimestampedModel
   :members:

.. autoclass:: ab.api.models.mixins.ActiveModel
   :members:

.. autoclass:: ab.api.models.mixins.CompanyRelatedModel
   :members:

.. autoclass:: ab.api.models.mixins.JobRelatedModel
   :members:

.. autoclass:: ab.api.models.mixins.FullAuditModel
   :members:
   :show-inheritance:

.. autoclass:: ab.api.models.mixins.CompanyAuditModel
   :members:
   :show-inheritance:

.. autoclass:: ab.api.models.mixins.JobAuditModel
   :members:
   :show-inheritance:
```

## Shared Models

```{eval-rst}
.. autoclass:: ab.api.models.shared.ServiceBaseResponse
   :members:

.. autoclass:: ab.api.models.shared.PaginatedList
   :members:

.. autoclass:: ab.api.models.shared.ListRequest
   :members:
```
