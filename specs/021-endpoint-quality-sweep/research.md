# Research: ContactDetailedInfo C# Source Analysis

## Decision: Use C# DTO hierarchy as field source

**Rationale**: The constitution (Sources of Truth) ranks API server source as Tier 1. The C# class hierarchy for the editdetails endpoint is:

```
ContactEditDetails                    # top-level — adds: Editable
  └── ContactExtendedDetails<T>       # adds: EmailsList, PhonesList, AddressesList, Fax, PrimaryPhone, PrimaryEmail
        └── ContactBaseDetails        # adds: Id, ContactDisplayId, FullName, ContactTypeId, CareOf, BolNotes,
                                      #        TaxId, IsPayer, IsPrefered, IsPrivate, CompanyId, RootContactId,
                                      #        OwnerFranchiseeId, Company, LegacyGuid, IsPrimary, Assistant,
                                      #        Department, WebSite, BirthDate, JobTitleId, JobTitle, IsBusiness
```

**Alternatives considered**: Swagger (Tier 3) — rejected because ACPortal swagger is known to omit fields.

## Decision: Reuse `CompanyAddress` for nested address objects

**Rationale**: The C# `AddressDetails` class maps exactly to the existing `CompanyAddress` ResponseModel in `ab/api/models/common.py`. The fixture confirms identical fields. No duplication needed.

## Decision: Create typed nested models for contact detail wrappers

**Rationale**: The fixture shows structured nested objects for `emailsList`, `phonesList`, `addressesList`. The C# source defines `ContactEmailEditDetails`, `ContactPhoneEditDetails`, `ContactAddressEditDetails` — each wrapping a primitive detail type with an `Editable` flag and inheriting `DetailBindingBase` (id, isActive, deactivatedReason, metaData).

Creating typed Pydantic models for these wrappers gives IDE users autocomplete on nested fields. Using `List[dict]` (current state) loses all type information.

## Decision: Share base fields via a mixin rather than duplicating ContactSimple

**Rationale**: `ContactSimple` already declares 31 "extended fields" that overlap with `ContactBaseDetails`. However, `ContactSimple` also includes fields not in `ContactBaseDetails` (e.g., `first_name`, `last_name`, `company_name`). Rather than making `ContactDetailedInfo` inherit from `ContactSimple` (which would pull in `company_name` and other fields not in the DTO), we add the fields directly to `ContactDetailedInfo`. This matches the C# hierarchy where `ContactBaseDetails` is the shared base, not `SelectContactInfo`/`ContactSimple`.

The fields are identical in type and alias, so the code is DRY at the JSON level — just not at the Python inheritance level. This is intentional: the C# classes have different inheritance chains, and our Python models should reflect that.

## Decision: Add `contactDetailsCompanyInfo` as typed dict

**Rationale**: The fixture shows `contactDetailsCompanyInfo` as a rich nested object with company details, address, and branding. This field is unique to `ContactEditDetails` (not in `ContactBaseDetails`). The C# source doesn't show a dedicated DTO for this — it's likely serialized from the `Company` entity with additional fields. We type it as `Optional[dict]` for now, matching the existing pattern for complex company objects. A future sweep can extract a typed model if needed.

## Fixture cross-reference

All 31 undeclared fields from the fixture map directly to C# `ContactBaseDetails` + `ContactExtendedDetails` + `ContactEditDetails` properties:

| Fixture key | C# property | C# type | Python type |
|---|---|---|---|
| `contactDisplayId` | `ContactDisplayId` | `string` | `Optional[str]` |
| `fullName` | `FullName` | `string` | `Optional[str]` |
| `contactTypeId` | `ContactTypeId` | `int` | `Optional[int]` |
| `careOf` | `CareOf` | `string` | `Optional[str]` |
| `bolNotes` | `BolNotes` | `string` | `Optional[str]` |
| `taxId` | `TaxId` | `string` | `Optional[str]` |
| `isBusiness` | `IsBusiness` | `bool` (computed) | `Optional[bool]` |
| `isPayer` | `IsPayer` | `bool` | `Optional[bool]` |
| `isPrefered` | `IsPrefered` | `bool` | `Optional[bool]` |
| `isPrivate` | `IsPrivate` | `bool` | `Optional[bool]` |
| `isPrimary` | `IsPrimary` | `bool` | `Optional[bool]` |
| `companyId` | `CompanyId` | `Guid?` | `Optional[str]` |
| `rootContactId` | `RootContactId` | `int?` | `Optional[int]` |
| `ownerFranchiseeId` | `OwnerFranchiseeId` | `Guid?` | `Optional[str]` |
| `company` | `Company` | `Company` | `Optional[dict]` |
| `legacyGuid` | `LegacyGuid` | `Guid` | `Optional[str]` |
| `assistant` | `Assistant` | `string` | `Optional[str]` |
| `department` | `Department` | `string` | `Optional[str]` |
| `webSite` | `WebSite` | `string` | `Optional[str]` |
| `birthDate` | `BirthDate` | `DateTime?` | `Optional[str]` |
| `jobTitleId` | `JobTitleId` | `int?` | `Optional[int]` |
| `jobTitle` | `JobTitle` | `string` | `Optional[str]` |
| `editable` | `Editable` | `bool` | `Optional[bool]` |
| `emailsList` | `EmailsList` | `List<ContactEmailEditDetails>` | `Optional[List[ContactEmailEntry]]` |
| `phonesList` | `PhonesList` | `List<ContactPhoneEditDetails>` | `Optional[List[ContactPhoneEntry]]` |
| `addressesList` | `AddressesList` | `List<ContactAddressEditDetails>` | `Optional[List[ContactAddressEntry]]` |
| `fax` | `Fax` | `string` (computed) | `Optional[str]` |
| `primaryPhone` | `PrimaryPhone` | `string` (computed) | `Optional[str]` |
| `primaryEmail` | `PrimaryEmail` | `string` (computed) | `Optional[str]` |
| `contactDetailsCompanyInfo` | (serialized Company) | `object` | `Optional[dict]` |
| `fullNameUpdateRequired` | `FullNameUpdateRequired` | `bool?` | `Optional[bool]` |
| `isEmpty` | `IsEmpty` | `bool` (computed) | `Optional[bool]` |
