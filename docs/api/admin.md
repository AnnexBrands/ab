# Admin

```{eval-rst}
.. autoclass:: ab.api.endpoints.admin.AdminEndpoint
   :members:
   :undoc-members:
```

## Methods

### Advanced Settings

#### get_all_advanced_settings

`GET /admin/advancedsettings/all` — List all advanced settings.

**Returns:** `list[`{class}`~ab.api.models.admin.AdvancedSetting`]`

#### get_advanced_setting / save_advanced_setting / delete_advanced_setting

`GET/POST/DELETE /admin/advancedsettings[/{id}]`

### Carrier Error Messages

#### get_all_carrier_errors / save_carrier_error

`GET/POST /admin/carriererrormessage[/all]`

**Returns:** `list[`{class}`~ab.api.models.admin.CarrierErrorMessage`]`

### Global Settings

#### get_company_hierarchy

`GET /admin/globalsettings/companyhierarchy` — Company hierarchy tree.

**Returns:** {class}`~ab.api.models.admin.CompanyHierarchy`

#### get_insurance_exceptions / approve_insurance_exception

`POST /admin/globalsettings/getinsuranceexceptions|approveinsuranceexception`

#### save_intacct_settings

`POST /admin/globalsettings/intacct`

### Log Buffer

#### flush_log / flush_all_logs

`POST /admin/logbuffer/flush|flushAll`
