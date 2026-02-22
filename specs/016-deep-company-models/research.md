# Research: Deep Pydantic Models for Company Response

## R1: What do /details and /fulldetails actually return?

**Decision**: Both endpoints use the same `CompanyDetails` response model. The existing fixture (`CompanyDetails.json`) was captured from `fulldetails` and contains BOTH the nested envelope sections (details, preferences, address, pricing, insurance, taxes) AND the flat Company entity fields (companyName, companyCode, companyInfo, addressData, etc.) in a single response.

**Rationale**: The C# source only shows `/details` returning `Company` entity. However, the `/fulldetails` endpoint exists in the live API and returns a superset that includes both the envelope AND the Company fields. The current model already accepts both shapes via Optional fields. Splitting into two models would be premature — the live fixture proves both sets of fields appear in one response.

**Alternatives considered**:
- Split into `CompanyFlat` and `CompanyFull` — rejected because the fixture shows fulldetails returns all Company flat fields too
- Keep dict fields — rejected because it violates Constitution Principle I (Pydantic Model Fidelity)

## R2: Which dict fields can be typed from C# source?

**Decision**: Type the following 7 nested structures based on their C# entity definitions:

| Current field | Current type | New pydantic model | C# source |
|---------------|-------------|-------------------|-----------|
| `company_info` | `dict` | `CompanyInfo` | `AB.ABCEntities.CompanyEntities.CompanyInfo` |
| `address_data` | `dict` | `AddressData` | `AB.ABCEntities.ReportEntities.Common.AddressData` |
| `overridable_address_data` | `dict` | `OverridableAddressData` | `AB.ABCEntities.ReportEntities.Common.OverridableAddressData` |
| `contact_info` | `dict` | `ContactInfo` | `AB.ABCEntities.Contact` (subset) |
| `company_insurance_pricing` | `dict` | `CompanyInsurancePricing` | `AB.ABCEntities.CompanyInsurancePricing` |
| `company_service_pricing` | `dict` | `CompanyServicePricing` | `AB.ABCEntities.CompanyServicePricing` |
| `company_tax_pricing` | `dict` | `CompanyTaxPricing` | `AB.ABCEntities.CompanyTaxPricing` |

**Rationale**: Each has a clearly defined C# entity with known fields. The fixture confirms the JSON shape matches the C# definitions.

## R3: What about `Overridable<T>` pattern?

**Decision**: Model as `OverridableField` — a pydantic model with `default_value: Optional[str]`, `override_value: Optional[str]`, `force_empty: bool`, `value: Optional[str]`. Each field in `OverridableAddressData` uses this type.

**Rationale**: The fixture shows the exact shape: `{"defaultValue": "...", "overrideValue": null, "forceEmpty": false, "value": "..."}`. The `value` is computed server-side but serialized in the response. Note: `fullAddressLine` is a plain string (not wrapped), while `fullAddress` and `fullCityLine` are wrapped in Overridable.

**Alternatives considered**: Generic `Overridable[T]` with TypeVar — rejected because all instances are `Overridable<string>` in practice; no polymorphism needed.

## R4: What about `addresses`, `contacts`, `settings` list/dict fields?

**Decision**: Defer to a follow-up feature. Keep as `Optional[List[dict]]` / `Optional[dict]`.

**Rationale**: These fields don't have clear C# entity types in the response context (they're populated dynamically from various service calls). The user's reported issue is specifically about `companyInfo`, `addressData`, and `overridableAddressData`. Typing `addresses` and `contacts` lists would require additional research into what subset of Address/Contact fields are actually serialized in this context.

## R5: CompanyInfo has a field not in C# source

**Decision**: The fixture shows `companyDisplayId` in `companyInfo` which is NOT in the C# `CompanyInfo` class. Add it as `Optional[str]` in the pydantic model.

**Rationale**: Constitution Principle IV — reality (fixture) trumps source code. The C# `CompanyInfo.CompanyId` computed property may generate this from the `Company` entity's `CompanyDisplayID` field.

## R6: AddressData has computed visibility booleans

**Decision**: Include the visibility booleans (`address_line2_visible`, `company_visible`, `country_name_visible`, `phone_visible`, `email_visible`) and computed address fields (`full_address_line`, `full_address`) in the pydantic model as regular `Optional` fields.

**Rationale**: The fixture includes these server-computed fields in the serialized JSON. They're useful for UI consumers. Model them as Optional response fields (they come from the server, not from user input).
