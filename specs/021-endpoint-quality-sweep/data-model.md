# Data Model: ContactDetailedInfo

## Nested Sub-Models (new)

### EmailDetails

Maps to C# `EmailDetails` — inner email object within `ContactEmailEditDetails`.

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| `id` | `Optional[int]` | — | Email row ID |
| `email` | `Optional[str]` | — | Email address |
| `invalid` | `Optional[bool]` | — | Whether email is invalid |
| `dont_spam` | `Optional[bool]` | `dontSpam` | Do-not-spam flag |

### PhoneDetails

Maps to C# `PhoneDetails` — inner phone object.

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| `id` | `Optional[int]` | — | Phone row ID |
| `phone` | `Optional[str]` | — | Phone number |

### ContactEmailEntry

Maps to C# `ContactEmailEditDetails` — extends `DetailBindingBase`.

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| `id` | `Optional[int]` | — | Mapping row ID |
| `is_active` | `Optional[bool]` | `isActive` | Active flag |
| `deactivated_reason` | `Optional[str]` | `deactivatedReason` | Deactivation reason |
| `meta_data` | `Optional[str]` | `metaData` | Type label (e.g. "Primary", "Fax") |
| `editable` | `Optional[bool]` | — | Edit permission |
| `email` | `Optional[EmailDetails]` | — | Nested email details |

### ContactPhoneEntry

Maps to C# `ContactPhoneEditDetails`.

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| `id` | `Optional[int]` | — | Mapping row ID |
| `is_active` | `Optional[bool]` | `isActive` | Active flag |
| `deactivated_reason` | `Optional[str]` | `deactivatedReason` | Deactivation reason |
| `meta_data` | `Optional[str]` | `metaData` | Type label |
| `editable` | `Optional[bool]` | — | Edit permission |
| `phone` | `Optional[PhoneDetails]` | — | Nested phone details |

### ContactAddressEntry

Maps to C# `ContactAddressEditDetails`. Reuses existing `CompanyAddress` from `ab.api.models.common`.

| Field | Type | Alias | Description |
|-------|------|-------|-------------|
| `id` | `Optional[int]` | — | Mapping row ID |
| `is_active` | `Optional[bool]` | `isActive` | Active flag |
| `deactivated_reason` | `Optional[str]` | `deactivatedReason` | Deactivation reason |
| `meta_data` | `Optional[str]` | `metaData` | Type label |
| `editable` | `Optional[bool]` | — | Edit permission |
| `address` | `Optional[CompanyAddress]` | — | Nested address (reuses existing model) |

## Updated ContactDetailedInfo

Inherits from `ResponseModel, FullAuditModel` (provides `id`, `is_active`, `created_date`, `modified_date`, `created_by`, `modified_by`).

### Existing fields (keep)

| Field | Type | Alias |
|-------|------|-------|
| `first_name` | `Optional[str]` | `firstName` |
| `last_name` | `Optional[str]` | `lastName` |
| `email` | `Optional[str]` | — |
| `phone` | `Optional[str]` | — |

### Fields to add (from C# ContactBaseDetails)

| Field | Type | Alias | C# Source |
|-------|------|-------|-----------|
| `contact_display_id` | `Optional[str]` | `contactDisplayId` | `ContactBaseDetails.ContactDisplayId` |
| `full_name` | `Optional[str]` | `fullName` | `ContactBaseDetails.FullName` |
| `contact_type_id` | `Optional[int]` | `contactTypeId` | `ContactBaseDetails.ContactTypeId` |
| `care_of` | `Optional[str]` | `careOf` | `ContactBaseDetails.CareOf` |
| `bol_notes` | `Optional[str]` | `bolNotes` | `ContactBaseDetails.BolNotes` |
| `tax_id` | `Optional[str]` | `taxId` | `ContactBaseDetails.TaxId` |
| `is_business` | `Optional[bool]` | `isBusiness` | `ContactBaseDetails.IsBusiness` (computed) |
| `is_payer` | `Optional[bool]` | `isPayer` | `ContactBaseDetails.IsPayer` |
| `is_prefered` | `Optional[bool]` | `isPrefered` | `ContactBaseDetails.IsPrefered` |
| `is_private` | `Optional[bool]` | `isPrivate` | `ContactBaseDetails.IsPrivate` |
| `is_primary` | `Optional[bool]` | `isPrimary` | `ContactBaseDetails.IsPrimary` |
| `company_id` | `Optional[str]` | `companyId` | `ContactBaseDetails.CompanyId` (Guid) |
| `root_contact_id` | `Optional[int]` | `rootContactId` | `ContactBaseDetails.RootContactId` |
| `owner_franchisee_id` | `Optional[str]` | `ownerFranchiseeId` | `ContactBaseDetails.OwnerFranchiseeId` (Guid) |
| `company` | `Optional[dict]` | — | `ContactBaseDetails.Company` |
| `legacy_guid` | `Optional[str]` | `legacyGuid` | `ContactBaseDetails.LegacyGuid` (Guid) |
| `assistant` | `Optional[str]` | — | `ContactBaseDetails.Assistant` |
| `department` | `Optional[str]` | — | `ContactBaseDetails.Department` |
| `web_site` | `Optional[str]` | `webSite` | `ContactBaseDetails.WebSite` |
| `birth_date` | `Optional[str]` | `birthDate` | `ContactBaseDetails.BirthDate` (DateTime?) |
| `job_title_id` | `Optional[int]` | `jobTitleId` | `ContactBaseDetails.JobTitleId` |
| `job_title` | `Optional[str]` | `jobTitle` | `ContactBaseDetails.JobTitle` |

### Fields to add (from C# ContactExtendedDetails)

| Field | Type | Alias | C# Source |
|-------|------|-------|-----------|
| `emails_list` | `Optional[List[ContactEmailEntry]]` | `emailsList` | `ContactExtendedDetails.EmailsList` |
| `phones_list` | `Optional[List[ContactPhoneEntry]]` | `phonesList` | `ContactExtendedDetails.PhonesList` |
| `addresses_list` | `Optional[List[ContactAddressEntry]]` | `addressesList` | `ContactExtendedDetails.AddressesList` |
| `fax` | `Optional[str]` | — | `ContactExtendedDetails.Fax` (computed) |
| `primary_phone` | `Optional[str]` | `primaryPhone` | `ContactExtendedDetails.PrimaryPhone` (computed) |
| `primary_email` | `Optional[str]` | `primaryEmail` | `ContactExtendedDetails.PrimaryEmail` (computed) |

### Fields to add (from C# ContactEditDetails)

| Field | Type | Alias | C# Source |
|-------|------|-------|-----------|
| `editable` | `Optional[bool]` | — | `ContactEditDetails.Editable` |

### Fields to add (observed in fixture, not in C# base classes)

| Field | Type | Alias | Notes |
|-------|------|-------|-------|
| `contact_details_company_info` | `Optional[dict]` | `contactDetailsCompanyInfo` | Rich company object serialized from service layer |
| `full_name_update_required` | `Optional[bool]` | `fullNameUpdateRequired` | From `ContactDetails.FullNameUpdateRequired` |
| `is_empty` | `Optional[bool]` | `isEmpty` | Computed in C# `ContactDetails.IsEmpty` |

### Fields to change type (from `List[dict]` to typed)

| Field | Old Type | New Type |
|-------|----------|----------|
| `addresses` | `Optional[List[dict]]` | removed — replaced by `addresses_list` |
| `phones` | `Optional[List[dict]]` | removed — replaced by `phones_list` |
| `emails` | `Optional[List[dict]]` | removed — replaced by `emails_list` |
| `company_info` | `Optional[dict]` | keep as `Optional[dict]` (alias `companyInfo`) |
