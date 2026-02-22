# Data Model: Deep Pydantic Models for Company Response

## New Models (add to `ab/api/models/companies.py`)

### OverridableField

Models C# `Overridable<T>` — a field wrapper with default/override/forceEmpty semantics.

| Field | Type | Alias | Source |
|-------|------|-------|--------|
| `default_value` | `Optional[str]` | `defaultValue` | C# `Overridable<T>.DefaultValue` |
| `override_value` | `Optional[str]` | `overrideValue` | C# `Overridable<T>.OverrideValue` |
| `force_empty` | `bool` | `forceEmpty` | C# `Overridable<T>.ForceEmpty` |
| `value` | `Optional[str]` | `value` | C# `Overridable<T>.Value` (computed, serialized) |

Inherits: `ResponseModel`

### CompanyInfo

Models C# `AB.ABCEntities.CompanyEntities.CompanyInfo`.

| Field | Type | Alias | Source |
|-------|------|-------|--------|
| `company_id` | `Optional[str]` | `companyId` | C# `Guid CompanyId` |
| `company_type_id` | `Optional[str]` | `companyTypeId` | C# `Guid CompanyTypeId` |
| `company_display_id` | `Optional[str]` | `companyDisplayId` | Fixture (not in C# class) |
| `company_name` | `Optional[str]` | `companyName` | C# `string CompanyName` |
| `company_code` | `Optional[str]` | `companyCode` | C# `string CompanyCode` |
| `company_email` | `Optional[str]` | `companyEmail` | C# `string CompanyEmail` |
| `company_phone` | `Optional[str]` | `companyPhone` | C# `string CompanyPhone` |
| `thumbnail_logo` | `Optional[str]` | `thumbnailLogo` | C# `string ThumbnailLogo` |
| `company_logo` | `Optional[str]` | `companyLogo` | C# `string CompanyLogo` |
| `maps_marker_image` | `Optional[str]` | `mapsMarkerImage` | C# `string MapsMarkerImage` |
| `main_address` | `Optional[CompanyAddress]` | `mainAddress` | C# `AddressDetails MainAddress` |

Inherits: `ResponseModel`

### AddressData

Models C# `AB.ABCEntities.ReportEntities.Common.AddressData`.

| Field | Type | Alias | Source |
|-------|------|-------|--------|
| `company` | `Optional[str]` | `company` | C# `string Company` |
| `first_last_name` | `Optional[str]` | `firstLastName` | C# `string FirstLastName` |
| `address_line1` | `Optional[str]` | `addressLine1` | C# `string AddressLine1` |
| `address_line2` | `Optional[str]` | `addressLine2` | C# `string AddressLine2` |
| `contact_bol_note` | `Optional[str]` | `contactBOLNote` | C# `string ContactBOLNote` |
| `city` | `Optional[str]` | `city` | C# `string City` |
| `state` | `Optional[str]` | `state` | C# `string State` |
| `state_code` | `Optional[str]` | `stateCode` | C# `string StateCode` |
| `zip_code` | `Optional[str]` | `zipCode` | C# `string ZipCode` |
| `country_name` | `Optional[str]` | `countryName` | C# `string CountryName` |
| `property_type` | `Optional[str]` | `propertyType` | C# `string PropertyType` |
| `full_city_line` | `Optional[str]` | `fullCityLine` | C# `string FullCityLine` (computed) |
| `phone` | `Optional[str]` | `phone` | C# `string Phone` |
| `cell_phone` | `Optional[str]` | `cellPhone` | C# `string CellPhone` |
| `fax` | `Optional[str]` | `fax` | C# `string Fax` |
| `email` | `Optional[str]` | `email` | C# `string Email` |
| `country_id` | `Optional[str]` | `countryId` | C# `Guid? CountryId` |
| `address_line2_visible` | `Optional[bool]` | `addressLine2Visible` | C# computed |
| `company_visible` | `Optional[bool]` | `companyVisible` | C# computed |
| `country_name_visible` | `Optional[bool]` | `countryNameVisible` | C# computed |
| `phone_visible` | `Optional[bool]` | `phoneVisible` | C# computed |
| `email_visible` | `Optional[bool]` | `emailVisible` | C# computed |
| `full_address_line` | `Optional[str]` | `fullAddressLine` | C# computed |
| `full_address` | `Optional[str]` | `fullAddress` | C# computed |

Inherits: `ResponseModel`

### OverridableAddressData

Models C# `AB.ABCEntities.ReportEntities.Common.OverridableAddressData`.

| Field | Type | Alias | Source |
|-------|------|-------|--------|
| `company` | `Optional[OverridableField]` | `company` | C# `Overridable<string>` |
| `first_last_name` | `Optional[OverridableField]` | `firstLastName` | C# `Overridable<string>` |
| `address_line1` | `Optional[OverridableField]` | `addressLine1` | C# `Overridable<string>` |
| `address_line2` | `Optional[OverridableField]` | `addressLine2` | C# `Overridable<string>` |
| `city` | `Optional[OverridableField]` | `city` | C# `Overridable<string>` |
| `state` | `Optional[OverridableField]` | `state` | C# `Overridable<string>` |
| `zip_code` | `Optional[OverridableField]` | `zipCode` | C# `Overridable<string>` |
| `phone` | `Optional[OverridableField]` | `phone` | C# `Overridable<string>` |
| `email` | `Optional[OverridableField]` | `email` | C# `Overridable<string>` |
| `full_address_line` | `Optional[str]` | `fullAddressLine` | Plain string (not wrapped) |
| `full_address` | `Optional[OverridableField]` | `fullAddress` | C# `Overridable<string>` (computed) |
| `full_city_line` | `Optional[OverridableField]` | `fullCityLine` | C# `Overridable<string>` (computed) |

Inherits: `ResponseModel`

### CompanyInsurancePricing

Models C# `AB.ABCEntities.CompanyInsurancePricing`.

| Field | Type | Alias | Source |
|-------|------|-------|--------|
| `insurance_slab_id` | `Optional[str]` | `insuranceSlabID` | C# `Guid InsuranceSlabID` |
| `deductible_amount` | `Optional[float]` | `deductibleAmount` | C# `decimal? DeductibleAmount` |
| `rate` | `Optional[float]` | `rate` | C# `decimal? Rate` |
| `company_id` | `Optional[str]` | `companyId` | C# `Guid? CompanyId` |
| `is_active` | `Optional[bool]` | `isActive` | C# `bool? IsActive` |
| `transp_type_id` | `Optional[str]` | `transpTypeID` | C# `Guid? TranspTypeID` |
| `company_name` | `Optional[str]` | `companyName` | C# `string CompanyName` |
| `created_by` | `Optional[str]` | `createdby` | C# `Guid Createdby` |
| `modified_by` | `Optional[str]` | `modifiedby` | C# `Guid Modifiedby` |
| `revision` | `Optional[int]` | `revision` | C# `int? Revision` |
| `insurance_type` | `Optional[str]` | `insuranceType` | C# `Guid? InsuranceType` |
| `whole_sale_markup` | `Optional[float]` | `wholeSaleMarkup` | C# `decimal? WholeSaleMarkup` |
| `base_markup` | `Optional[float]` | `baseMarkup` | C# `decimal? BaseMarkup` |
| `medium_markup` | `Optional[float]` | `mediumMarkup` | C# `decimal? MediumMarkup` |
| `high_markup` | `Optional[float]` | `highMarkup` | C# `decimal? HighMarkup` |

Inherits: `ResponseModel`

### CompanyServicePricing

Models C# `AB.ABCEntities.CompanyServicePricing`.

| Field | Type | Alias | Source |
|-------|------|-------|--------|
| `service_pricing_id` | `Optional[str]` | `servicePricingId` | C# `Guid ServicePricingId` |
| `user_id` | `Optional[str]` | `userID` | C# `Guid UserID` |
| `company_id` | `Optional[str]` | `companyID` | C# `Guid? CompanyID` |
| `service_category_id` | `Optional[str]` | `serviceCategoryID` | C# `Guid? ServiceCategoryID` |
| `category_value` | `Optional[float]` | `categoryValue` | C# `decimal? CategoryValue` |
| `whole_sale_markup` | `Optional[float]` | `wholeSaleMarkup` | C# `decimal? WholeSaleMarkup` |
| `base_markup` | `Optional[float]` | `baseMarkup` | C# `decimal? BaseMarkup` |
| `medium_markup` | `Optional[float]` | `mediumMarkup` | C# `decimal? MediumMarkup` |
| `high_markup` | `Optional[float]` | `highMarkup` | C# `decimal? HighMarkup` |
| `is_active` | `Optional[bool]` | `isActive` | C# `bool? IsActive` |
| `is_taxable` | `Optional[bool]` | `isTaxable` | C# `bool? IsTaxable` |
| `tax_percent` | `Optional[float]` | `taxPercent` | C# `decimal? TaxPercent` |
| `created_by` | `Optional[str]` | `createdBy` | C# `Guid? CreatedBy` |
| `modified_by` | `Optional[str]` | `modifiedBy` | C# `Guid? ModifiedBy` |
| `created_date` | `Optional[str]` | `createdDate` | C# `DateTime? CreatedDate` |
| `modified_date` | `Optional[str]` | `modifiedDate` | C# `DateTime? ModifiedDate` |
| `company_code` | `Optional[str]` | `companyCode` | C# `string CompanyCode` |
| `service_category_name` | `Optional[str]` | `serviceCategoryName` | C# `string ServiceCategoryName` |
| `company_name` | `Optional[str]` | `companyName` | C# `string CompanyName` |
| `company_type_id` | `Optional[str]` | `companyTypeId` | C# `Guid CompanyTypeId` |
| `parent_category_id` | `Optional[str]` | `parentCategoryID` | C# `Guid? ParentCategoryID` |
| `zip_code` | `Optional[str]` | `zipCode` | C# `string ZipCode` |

Inherits: `ResponseModel`

### CompanyTaxPricing

Models C# `AB.ABCEntities.CompanyTaxPricing`.

| Field | Type | Alias | Source |
|-------|------|-------|--------|
| `job_id` | `Optional[str]` | `jobID` | C# `Guid? JobID` |
| `service_category_id` | `Optional[str]` | `serviceCategoryID` | C# `Guid? ServiceCategoryID` |
| `tax_slab_id` | `Optional[str]` | `taxSlabID` | C# `Guid? TaxSlabID` |
| `is_taxable` | `Optional[bool]` | `isTaxable` | C# `bool? IsTaxable` |
| `tax_percent` | `Optional[float]` | `taxPercent` | C# `decimal? TaxPercent` |
| `company_id` | `Optional[str]` | `companyID` | C# `Guid? CompanyID` |
| `service_category_name` | `Optional[str]` | `serviceCategotyName` | C# `string ServiceCategotyName` (typo preserved) |
| `company_name` | `Optional[str]` | `companyName` | C# `string CompanyName` |
| `is_active` | `Optional[bool]` | `isActive` | C# `bool? IsActive` |

Inherits: `ResponseModel`

## Updated Fields in CompanyDetails

These existing `dict`-typed fields in `CompanyDetails` change to their typed models:

| Field | Old type | New type |
|-------|----------|----------|
| `company_info` | `Optional[dict]` | `Optional[CompanyInfo]` |
| `address_data` | `Optional[dict]` | `Optional[AddressData]` |
| `overridable_address_data` | `Optional[dict]` | `Optional[OverridableAddressData]` |
| `contact_info` | `Optional[dict]` | `Optional[CompanyInfo]` |
| `company_insurance_pricing` | `Optional[dict]` | `Optional[CompanyInsurancePricing]` |
| `company_service_pricing` | `Optional[dict]` | `Optional[CompanyServicePricing]` |
| `company_tax_pricing` | `Optional[dict]` | `Optional[CompanyTaxPricing]` |

Note: `contact_info` in the fixture is `null` for the test company. The C# source shows it's typed as `Contact` (a large entity inheriting from `Address`). Since we don't have fixture data to validate against, model it as `Optional[dict]` for now and type it when a non-null fixture is captured. Update: if we can determine a minimal subset of Contact fields that appear here, create a `ContactInfo` model instead.

## Fields Remaining as dict (deferred)

| Field | Type | Reason |
|-------|------|--------|
| `settings` | `Optional[dict]` | Unknown shape — no C# type identified for this context |
| `addresses` | `Optional[List[dict]]` | Dynamic subset of Address fields — needs fixture with data |
| `contacts` | `Optional[List[dict]]` | Dynamic subset of Contact fields — needs fixture with data |
