# Data Model: Endpoint Quality Gates

**Date**: 2026-02-21
**Feature**: 011-endpoint-quality-gates

## Entities

### GateResult

Represents the pass/fail evaluation of a single quality gate for one endpoint.

| Field | Type | Description |
|-------|------|-------------|
| gate | enum(G1,G2,G3,G4) | Gate dimension |
| passed | bool | Whether the gate passes |
| reason | str | Failure reason (empty if passed) |

### EndpointGateStatus

Per-endpoint aggregate of all gate evaluations.

| Field | Type | Description |
|-------|------|-------------|
| endpoint_path | str | API path (e.g., `/companies/{id}/fulldetails`) |
| method | str | HTTP method |
| request_model | str | Request model name (or None) |
| response_model | str | Response model name (or None) |
| api_surface | str | acportal, catalog, abc |
| g1_model_fidelity | GateResult | Does model declare all fixture fields? |
| g2_fixture_status | GateResult | Does fixture file exist and was it captured from API? |
| g3_test_quality | GateResult | Do tests assert isinstance + zero __pydantic_extra__? |
| g4_doc_accuracy | GateResult | Do docs show correct return type? |
| overall_status | str | "complete" only if all applicable gates pass |
| notes | str | Hand-maintained debugging context (preserved from existing FIXTURES.md) |

### ModelWarning

Tracks fields present in fixture but missing from model.

| Field | Type | Description |
|-------|------|-------------|
| model_name | str | Python class name |
| model_file | str | File path |
| missing_fields | list[MissingField] | Fields to add |
| fixture_file | str | Fixture path used for analysis |

### MissingField

| Field | Type | Description |
|-------|------|-------------|
| field_name | str | camelCase API field name |
| python_name | str | snake_case Python field name |
| inferred_type | str | Type inferred from fixture data |
| is_nested | bool | Whether the value is a dict/list-of-dicts requiring a sub-model |
| sub_model_name | str | Proposed sub-model class name (if is_nested) |

## New Sub-Models Required (by parent model)

### CompanyDetails (~20 sub-models)

| Sub-Model | Parent Field | Fields | Depth |
|-----------|-------------|--------|-------|
| CompanyDetailsInfo | details | displayId, name, taxId, code, parentId, franchiseeId, companyTypeId, industryTypeId, cellPhone, phone, fax, email, website, isActive, isHidden, isGlobal, isNotUsed, isPreferred, payerContactId, payerContactName | 1 |
| CompanyPreferences | preferences | companyHeaderLogo, thumbnailLogo, letterHeadLogo, mapsMarker, isQbUser, skipIntacct, pricingToUse, pzCode, insuranceTypeId, +9 more | 1 |
| FileInfo | preferences.*.logo | filePath, newFile | 2 |
| CompanyAddress | address | id, isValid, dontValidate, propertyType, address1Value, address2Value, countryName, countryCode, countryId, +11 more | 1 |
| Coordinates | address.coordinates | latitude, longitude | 2 |
| AccountInformation | accountInformation | lmiUserName, lmiClientCode, useFlatRates, fedEx, ups, roadRunner, maersk, teamWW, estes, forwardAir, btx, globalTranz, usps | 1 |
| FedExAccount | accountInformation.fedEx | restApiAccounts | 2 |
| UPSAccount | accountInformation.ups | shipperNumber, clientId, clientSecret | 2 |
| RoadRunnerAccount | accountInformation.roadRunner | userName, password, appId, apiKey | 2 |
| MaerskAccount | accountInformation.maersk | locationId, tariffHeaderId, userName, password, addressId, controlStation | 2 |
| TeamWWAccount | accountInformation.teamWW | apiKey | 2 |
| EstesAccount | accountInformation.estes | userName, password, account | 2 |
| ForwardAirAccount | accountInformation.forwardAir | userName, password, customerId, billTo, shipperNumber | 2 |
| BTXAccount | accountInformation.btx | apiKey | 2 |
| GlobalTranzAccount | accountInformation.globalTranz | accessKey, userName, password | 2 |
| USPSAccount | accountInformation.usps | accountNumber, customerRegistrationId, mailerId, mailerIdCode, clientId, clientSecret | 2 |
| CompanyPricing | pricing | transportationCharge, transportationMarkups, carrierFreightMarkups, carrierOtherMarkups, materialMarkups, laborCharge, accesorialCharge, royalties, paymentSettings | 1 |
| TransportationCharge | pricing.transportationCharge | baseTripFee, baseTripMile, extraFee, fuelSurcharge | 2 |
| MarkupTier | pricing.*Markups | wholeSale, base, medium, high | 2 |
| LaborCharge | pricing.laborCharge | cost, charge | 2 |
| AccessorialCharge | pricing.accesorialCharge | stairs, elevator, longCarry, certificateOfInsurance, deInstallation, disassembly, timeSpecific, saturday | 2 |
| Royalties | pricing.royalties | franchisee, national, local | 2 |
| PaymentSettings | pricing.paymentSettings | creditCardSurcharge, stripeConnected | 2 |
| CompanyInsurance | insurance | isp, nsp, ltl | 1 |
| InsuranceOption | insurance.* | insuranceSlabId, option, sellPrice | 2 |
| TariffGroup | finalMileTariff[] | groupId, from, to, toCurb, intoGarage, roomOfChoice, whiteGlove, deleteGroup | 1 |
| CompanyTaxes | taxes | deliveryService, insurance, pickupService, services, transportationService, packagingMaterial, packagingLabor | 1 |
| TaxCategory | taxes.* | isTaxable, taxPercent | 2 |

### GlobalAccessorial (2 sub-models)

| Sub-Model | Parent Field | Fields | Depth |
|-----------|-------------|--------|-------|
| AccessorialOption | options[] | key, type, radioButtonOptions | 1 |
| RadioButtonOption | options[].radioButtonOptions[] | description, code | 2 |

### ShipmentInfo (1 sub-model)

| Sub-Model | Parent Field | Fields | Depth |
|-----------|-------------|--------|-------|
| ShipmentWeight | weight | pounds, originalWeight, originalWeightMeasureUnit | 1 |

### Shared (reusable across models)

| Sub-Model | Used By | Fields |
|-----------|---------|--------|
| Coordinates | CompanyAddress, ContactAddress | latitude, longitude |
| CompanyAddress | CompanyDetails.address, ContactPrimaryDetails.address | id, isValid, dontValidate, propertyType, address1Value, address2Value, countryName, countryCode, countryId, latitude, longitude, fullCityLine, coordinates, address1, address2, city, state, zipCode |

## Flat Field Additions (no sub-models needed)

| Model | Fields to Add | Types |
|-------|--------------|-------|
| AddressIsValidResult | dontValidate, countryId, countryCode, latitude, longitude, propertyType | bool, str, str, float, float, int |
| CalendarItem | notedConditions | Optional[str] |
| CompanySimple | parentCompanyId, companyName, typeId | Optional[str] x3 |
| ContactSimple | editable, isEmpty, fullNameUpdateRequired, emailsList, phonesList, addressesList, fax, primaryPhone, primaryEmail, +14 more | Mixed (bool, str, list) |
| ContactTypeEntity | value | Optional[str] |
| CountryCodeDto | id, iataCode | Optional[str] x2 |
| FormsShipmentPlan | jobShipmentID, jobID, fromAddressId, toAddressId, providerID, sequenceNo, fromLocationCompanyName, toLocationCompanyName, transportType, providerCompanyName, optionIndex | Mixed (str, int) |
| RatesState | fromZip, toZip, itemWeight, services, parcelItems, parcelServices, shipOutDate | str, str, float, list, list, list, str |
| SellerExpandedDto | customerDisplayId, isActive | Optional[int], Optional[bool] |
| User | login, fullName, contactId, contactDisplayId, contactCompanyName, contactCompanyId, contactCompanyDisplayId, emailConfirmed, contactPhone, contactEmail, password, lockoutDateUtc, lockoutEnabled, role, isActive, legacyId, additionalUserCompanies, additionalUserCompaniesNames, crmContactId | Mixed |
| Web2LeadResponse | SubmitNewLeadPOSTResult | Optional[Web2LeadGETResult] (alias) |

## State Transitions

No state machine — gate status is **derived** from source artifacts on each evaluation. There is no stored state to transition.

## Relationships

```
EndpointGateStatus 1--* GateResult (one per gate dimension)
ModelWarning 1--* MissingField
EndpointGateStatus *--1 ModelWarning (via response_model name)
```
