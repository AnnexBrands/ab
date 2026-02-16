# Company Setup

```{eval-rst}
.. autoclass:: ab.api.endpoints.company_setup.CompanySetupEndpoint
   :members:
   :undoc-members:
```

## Methods

### Calendar

#### get_calendar

`GET /company/{companyId}/calendar/{date}` — Get calendar day.

**Returns:** {class}`~ab.api.models.company_setup.CalendarDay`

```python
day = api.company_setup.get_calendar("company-uuid", "2026-01-15")
```

#### get_calendar_base_info / get_start_of_day / get_end_of_day

`GET /company/{companyId}/calendar/{date}/baseinfo|startofday|endofday`

**Returns:** {class}`~ab.api.models.company_setup.CalendarBaseInfo` or {class}`~ab.api.models.company_setup.CalendarTimeInfo`

### Stripe External Accounts

#### get_stripe_connect_url

`GET /company/{companyId}/accounts/stripe/connecturl` — Get Stripe connect URL.

**Returns:** {class}`~ab.api.models.company_setup.StripeConnectUrl`

#### complete_stripe_connection / delete_stripe

`POST/DELETE /company/{companyId}/accounts/stripe/completeconnection|stripe`

### Document Templates

#### get_document_templates

`GET /company/{companyId}/document-templates` — List templates.

**Returns:** `list[`{class}`~ab.api.models.company_setup.DocumentTemplate`]`

#### create_document_template / update_document_template / delete_document_template

`POST/PUT/DELETE /company/{companyId}/document-templates[/{documentId}]`

### Settings

#### get_settings / save_settings / get_company_setup_data

`GET/POST /company/{companyId}/settings|gridsettings|companysetupdata`

### Container Thickness

#### get_container_thicknesses / create_container_thickness / delete_container_thickness

`GET/POST/DELETE /company/{companyId}/containerthickness`

### Planner

#### get_planner

`GET /company/{companyId}/planner` — Get planner entries.

**Returns:** `list[`{class}`~ab.api.models.company_setup.PlannerEntry`]`

### Materials

#### get_materials / create_material / update_material / delete_material

`GET/POST/PUT/DELETE /company/{companyId}/material[/{materialId}]`

**Returns:** {class}`~ab.api.models.company_setup.Material`

### Trucks

#### get_trucks / create_truck / update_truck / delete_truck

`GET/POST/PUT/DELETE /company/{companyId}/truck[/{truckId}]`

**Returns:** {class}`~ab.api.models.company_setup.Truck`
