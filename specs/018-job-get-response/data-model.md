# Data Model: Complete Job Get Response

**Feature**: 018-job-get-response
**Date**: 2026-02-23
**Source**: Server source (Tier 1) + Job.json fixture (Tier 2)

## Entity Hierarchy

```text
Job (ResponseModel, FullAuditModel)                    ← existing, extend with 27 fields
├── customer_contact: JobContactDetails                 ← new sub-model
│   ├── contact: ContactDetails                         ← new sub-model
│   │   ├── company: Optional[dict]                     ← keep as dict (no dedicated fixture)
│   │   ├── emails_list: List[dict]
│   │   ├── phones_list: List[dict]
│   │   └── addresses_list: List[dict]
│   ├── email: JobContactEmail                          ← new sub-model
│   ├── phone: JobContactPhone                          ← new sub-model
│   └── address: CompanyAddress                         ← REUSE from common.py
│       └── coordinates: Coordinates                    ← REUSE from common.py
├── pickup_contact: JobContactDetails                   ← same type as customer_contact
├── delivery_contact: JobContactDetails                 ← same type as customer_contact
├── items: List[JobItem]                                ← new sub-model (replace List[dict])
│   └── materials: List[JobItemMaterial]                ← new sub-model
├── freight_items: List[JobFreightItem]                 ← new sub-model
├── job_summary_snapshot: JobSummarySnapshot             ← new sub-model
├── notes: List[dict]                                   ← keep as dict (empty in fixture)
├── active_on_hold_info: ActiveOnHoldInfo               ← new sub-model
├── documents: List[JobDocument]                        ← new sub-model
├── freight_providers: List[dict]                       ← keep as dict (empty in fixture)
├── freight_info: JobFreightInfo                        ← new sub-model
├── payment_info: JobPaymentInfo                        ← new sub-model
├── agent_payment_info: JobAgentPaymentInfo             ← new sub-model
├── sla_info: JobSlaInfo                                ← new sub-model
├── prices: List[dict]                                  ← keep as dict (empty in fixture)
└── (scalar fields: bookedDate, ownerCompanyId, totalSellPrice, writeAccess,
     accessLevel, statusId, jobMgmtSubId, isCancelled, expectedPickupDate,
     expectedDeliveryDate, labelRequestSentDate, jobType)
```

## Entities

### Job (extend existing)

Server source: `JobPortalInfo` → `AB.ABCEntities.JobEntities.JobPortalInfo`

Add these 27 fields to the existing `Job` model (which already has `job_display_id`, `status`, `customer`, `pickup`, `delivery`, `items`):

| Python field | Alias | Type | Server C# type | Notes |
|-------------|-------|------|-----------------|-------|
| booked_date | bookedDate | Optional[str] | DateTime? | ISO datetime string |
| owner_company_id | ownerCompanyId | Optional[str] | Guid | Company UUID |
| customer_contact | customerContact | Optional[JobContactDetails] | JobContactDetails | Deep sub-model |
| pickup_contact | pickupContact | Optional[JobContactDetails] | JobContactDetails | Deep sub-model |
| delivery_contact | deliveryContact | Optional[JobContactDetails] | JobContactDetails | Deep sub-model |
| total_sell_price | totalSellPrice | Optional[float] | decimal | Price total |
| freight_items | freightItems | Optional[List[JobFreightItem]] | List\<FreightShimpment\> | May be empty |
| job_summary_snapshot | jobSummarySnapshot | Optional[JobSummarySnapshot] | JobSummary | Financial rollup |
| notes | notes | Optional[List[dict]] | List\<Notes\> | Empty in fixture, keep dict |
| active_on_hold_info | activeOnHoldInfo | Optional[ActiveOnHoldInfo] | OnHoldInfo | Hold details |
| write_access | writeAccess | Optional[bool] | bool | User can modify |
| access_level | accessLevel | Optional[int] | JobAccessLevel | Flags enum as int |
| status_id | statusId | Optional[str] | Guid? | Status UUID |
| job_mgmt_sub_id | jobMgmtSubId | Optional[str] | Guid? | Mgmt subscription UUID |
| is_cancelled | isCancelled | Optional[bool] | bool | Cancellation flag |
| freight_info | freightInfo | Optional[JobFreightInfo] | FreightTrackingLastDetails | Null in fixture |
| freight_providers | freightProviders | Optional[List[dict]] | List\<ShipmentPlanProvider\> | Empty in fixture, keep dict |
| expected_pickup_date | expectedPickupDate | Optional[str] | DateTime? | ISO datetime |
| expected_delivery_date | expectedDeliveryDate | Optional[str] | DateTime? | ISO datetime |
| timeline_tasks | timelineTasks | Optional[List[dict]] | List\<Task\> | Empty in fixture, keep dict |
| documents | documents | Optional[List[JobDocument]] | List\<DocumentDetails\> | 11 docs in fixture |
| label_request_sent_date | labelRequestSentDate | Optional[str] | DateTime? | ISO datetime |
| payment_info | paymentInfo | Optional[JobPaymentInfo] | PaymentInfo | Null in fixture |
| agent_payment_info | agentPaymentInfo | Optional[JobAgentPaymentInfo] | AgentPaymentInfo | Null in fixture |
| sla_info | slaInfo | Optional[JobSlaInfo] | SlaInfo | Has data in fixture |
| job_type | jobType | Optional[str] | ? | Null in fixture |
| prices | prices | Optional[List[dict]] | ? | Empty in fixture, keep dict |

Also retype existing field: `items: Optional[List[dict]]` → `Optional[List[JobItem]]`

### JobContactDetails (new)

Server source: `JobContactDetails` → `AB.ABCEntities.JobEntities.JobContactDetails`

Shared by `customerContact`, `pickupContact`, `deliveryContact`.

| Python field | Alias | Type | Notes |
|-------------|-------|------|-------|
| id | id | Optional[int] | Contact ID |
| contact | contact | Optional[ContactDetails] | Full contact person |
| email | email | Optional[JobContactEmail] | Primary email |
| phone | phone | Optional[JobContactPhone] | Primary phone |
| address | address | Optional[CompanyAddress] | REUSE from common.py |
| care_of | careOf | Optional[str] | Care of |
| legacy_guid | legacyGuid | Optional[str] | Legacy GUID |
| contact_email_mapping_id | contactEmailMappingId | Optional[int] | |
| contact_phone_mapping_id | contactPhoneMappingId | Optional[int] | |
| contact_address_mapping_id | contactAddressMappingId | Optional[int] | |
| dragged_from | draggedFrom | Optional[str] | JobContactType enum |
| job_contact_type | jobContactType | Optional[str] | JobContactType enum |
| property_type | propertyType | Optional[int] | Property classification |

### ContactDetails (new)

Server source: `ContactDetails` (nested in JobContactDetails.contact)

| Python field | Alias | Type | Notes |
|-------------|-------|------|-------|
| id | id | Optional[int] | Contact int ID |
| contact_display_id | contactDisplayId | Optional[str] | Display ID |
| full_name | fullName | Optional[str] | |
| contact_type_id | contactTypeId | Optional[int] | |
| editable | editable | Optional[bool] | |
| is_empty | isEmpty | Optional[bool] | |
| full_name_update_required | fullNameUpdateRequired | Optional[bool] | |
| emails_list | emailsList | Optional[List[dict]] | List of email wrappers |
| phones_list | phonesList | Optional[List[dict]] | List of phone wrappers |
| addresses_list | addressesList | Optional[List[dict]] | List of address wrappers |
| fax | fax | Optional[str] | |
| primary_phone | primaryPhone | Optional[str] | |
| primary_email | primaryEmail | Optional[str] | |
| care_of | careOf | Optional[str] | |
| bol_notes | bolNotes | Optional[str] | |
| tax_id | taxId | Optional[str] | |
| is_business | isBusiness | Optional[bool] | |
| is_payer | isPayer | Optional[bool] | |
| is_prefered | isPrefered | Optional[bool] | Note: API typo preserved |
| is_private | isPrivate | Optional[bool] | |
| is_active | isActive | Optional[bool] | |
| company_id | companyId | Optional[str] | |
| root_contact_id | rootContactId | Optional[str] | |
| owner_franchisee_id | ownerFranchiseeId | Optional[str] | |
| company | company | Optional[dict] | Lightweight company summary |
| legacy_guid | legacyGuid | Optional[str] | |
| is_primary | isPrimary | Optional[bool] | |
| assistant | assistant | Optional[str] | |
| department | department | Optional[str] | |
| web_site | webSite | Optional[str] | |
| birth_date | birthDate | Optional[str] | |
| job_title_id | jobTitleId | Optional[str] | |
| job_title | jobTitle | Optional[str] | |

### JobContactEmail (new)

| Python field | Alias | Type | Notes |
|-------------|-------|------|-------|
| id | id | Optional[int] | |
| email | email | Optional[str] | |
| invalid | invalid | Optional[bool] | |
| dont_spam | dontSpam | Optional[bool] | |

### JobContactPhone (new)

| Python field | Alias | Type | Notes |
|-------------|-------|------|-------|
| id | id | Optional[int] | |
| phone | phone | Optional[str] | |

### JobItem (new)

Server source: `Items` inherits `MasterItems` inherits `ItemFeature` → `AB.ABCEntities.Items`

Approximately 75 fields observed in fixture. Full field list:

| Python field | Alias | Type | Notes |
|-------------|-------|------|-------|
| job_display_id | jobDisplayId | Optional[int] | |
| job_item_id | jobItemID | Optional[str] | UUID (note capital ID) |
| original_job_item_id | originalJobItemId | Optional[str] | |
| job_id | jobID | Optional[str] | UUID |
| quantity | quantity | Optional[int] | |
| original_qty | originalQty | Optional[int] | |
| job_freight_id | jobFreightID | Optional[str] | |
| nmfc_item | nmfcItem | Optional[str] | |
| nmfc_sub | nmfcSub | Optional[str] | |
| nmfc_sub_class | nmfcSubClass | Optional[str] | |
| job_item_pkd_length | jobItemPkdLength | Optional[float] | |
| job_item_pkd_width | jobItemPkdWidth | Optional[float] | |
| job_item_pkd_height | jobItemPkdHeight | Optional[float] | |
| job_item_pkd_weight | jobItemPkdWeight | Optional[float] | |
| is_fill_percent_changed | isFillPercentChanged | Optional[bool] | |
| c_fill_id | cFillId | Optional[int] | |
| container_id | containerId | Optional[int] | |
| labor_hrs | laborHrs | Optional[float] | |
| labor_charge | laborCharge | Optional[float] | |
| user_id | userId | Optional[str] | |
| is_fill_changed | isFillChanged | Optional[bool] | |
| is_container_changed | isContainerChanged | Optional[bool] | |
| is_valid_container | isValidContainer | Optional[bool] | |
| is_valid_fill | isValidFill | Optional[bool] | |
| inches_to_add | inchesToAdd | Optional[float] | |
| container_thickness | containerThickness | Optional[float] | |
| is_inch_to_add_changed | isInchToAddChanged | Optional[bool] | |
| total_pcs | totalPcs | Optional[int] | |
| description_of_products | descriptionOfProducts | Optional[str] | |
| total_items | totalItems | Optional[int] | |
| auto_pack_off | autoPackOff | Optional[bool] | |
| c_pack_value | cPackValue | Optional[str] | |
| c_fill_value | cFillValue | Optional[str] | |
| container_type | containerType | Optional[str] | |
| job_item_fill_percent | jobItemFillPercent | Optional[float] | |
| container_weight | containerWeight | Optional[float] | |
| fill_weight | fillWeight | Optional[float] | |
| material_weight | materialWeight | Optional[float] | |
| job_item_pkd_value | jobItemPkdValue | Optional[float] | |
| total_packed_value | totalPackedValue | Optional[float] | |
| total_weight | totalWeight | Optional[float] | |
| stc | stc | Optional[str] | |
| materials | materials | Optional[List[JobItemMaterial]] | Nested materials |
| material_total_cost | materialTotalCost | Optional[float] | |
| is_access | isAccess | Optional[bool] | |
| job_item_parcel_value | jobItemParcelValue | Optional[float] | |
| total_labor_charge | totalLaborCharge | Optional[float] | |
| gross_cubic_feet | grossCubicFeet | Optional[float] | |
| row_number | rowNumber | Optional[int] | |
| noted_conditions | notedConditions | Optional[str] | |
| job_item_notes | jobItemNotes | Optional[str] | |
| customer_item_id | customerItemId | Optional[str] | |
| document_exists | documentExists | Optional[bool] | |
| force_crate | forceCrate | Optional[bool] | |
| auto_pack_failed | autoPackFailed | Optional[bool] | |
| do_not_tip | doNotTip | Optional[bool] | |
| commodity_id | commodityId | Optional[str] | |
| longest_dimension | longestDimension | Optional[float] | |
| second_dimension | secondDimension | Optional[float] | |
| pkd_length_plus_girth | pkdLengthPlusGirth | Optional[float] | |
| requested_parcel_packagings | requestedParcelPackagings | Optional[str] | |
| parcel_package_type_id | parcelPackageTypeId | Optional[int] | |
| transportation_length | transportationLength | Optional[int] | |
| transportation_width | transportationWidth | Optional[int] | |
| transportation_height | transportationHeight | Optional[int] | |
| transportation_weight | transportationWeight | Optional[float] | |
| ceiling_transportation_weight | ceilingTransportationWeight | Optional[int] | |
| company_id | companyID | Optional[str] | Note capital ID |
| company_name | companyName | Optional[str] | |
| item_sequence_no | itemSequenceNo | Optional[int] | |
| item_name | itemName | Optional[str] | |
| item_description | itemDescription | Optional[str] | |
| schedule_b | scheduleB | Optional[str] | |
| eccn | eccn | Optional[str] | |
| item_notes | itemNotes | Optional[str] | |
| is_prepacked | isPrepacked | Optional[bool] | |
| item_active | itemActive | Optional[bool] | |
| item_public | itemPublic | Optional[bool] | |
| c_pack_id | cPackId | Optional[str] | |
| item_id | itemID | Optional[str] | UUID (capital ID) |
| item_value | itemValue | Optional[float] | |
| modified_by | modifiedBy | Optional[str] | |
| created_by | createdBy | Optional[str] | |
| created_date | createdDate | Optional[str] | |
| modified_date | modifiedDate | Optional[str] | |
| item_length | itemLength | Optional[float] | |
| item_width | itemWidth | Optional[float] | |
| item_height | itemHeight | Optional[float] | |
| item_weight | itemWeight | Optional[float] | |
| net_cubic_feet | netCubicFeet | Optional[float] | |

### JobItemMaterial (new)

Server source: `MasterMaterials` → `AB.ABCEntities.MasterMaterials`

Fields observed in fixture `items[0].materials[0]`:

| Python field | Alias | Type | Notes |
|-------------|-------|------|-------|
| job_id | jobID | Optional[str] | UUID |
| job_pack_material_id | jobPackMaterialID | Optional[str] | UUID |
| material_id | materialID | Optional[int] | |
| mateial_master_id | mateialMasterID | Optional[str] | API typo preserved |
| material_quantity | materialQuantity | Optional[float] | |
| material_name | materialName | Optional[str] | |
| material_description | materialDescription | Optional[str] | |
| material_code | materialCode | Optional[str] | |
| material_type | materialType | Optional[str] | |
| material_unit | materialUnit | Optional[str] | |
| material_weight | materialWeight | Optional[float] | |
| material_length | materialLength | Optional[float] | |
| material_width | materialWidth | Optional[float] | |
| material_height | materialHeight | Optional[float] | |
| material_cost | materialCost | Optional[float] | |
| material_price | materialPrice | Optional[float] | |
| material_waste_factor | materialWasteFactor | Optional[float] | |
| material_total_cost | materialTotalCost | Optional[float] | |
| material_total_weight | materialTotalWeight | Optional[float] | |
| created_by | createdBy | Optional[str] | |
| modified_by | modifiedBy | Optional[str] | |
| created_date | createdDate | Optional[str] | |
| modified_date | modifiedDate | Optional[str] | |
| item_id | itemID | Optional[str] | UUID |
| quantity_actual | quantityActual | Optional[float] | |
| is_automatic | isAutomatic | Optional[bool] | |
| waste | waste | Optional[float] | |
| price | price | Optional[float] | |
| is_edited | isEdited | Optional[bool] | |
| item_name | itemName | Optional[str] | |
| item_description | itemDescription | Optional[str] | |
| item_notes | itemNotes | Optional[str] | |
| job_item_id | jobItemId | Optional[str] | |
| company_id | companyId | Optional[str] | |
| is_active | isActive | Optional[bool] | |

### JobSummarySnapshot (new)

Server source: `JobSummary` → `AB.ABCEntities.JobSummary`

| Python field | Alias | Type | Notes |
|-------------|-------|------|-------|
| job_snapshot_id | jobSnapshotID | Optional[int] | |
| job_id | jobID | Optional[str] | |
| job_status_id | jobStatusID | Optional[str] | UUID |
| job_total_amount | jobTotalAmount | Optional[float] | |
| job_total_weight | jobTotalWeight | Optional[float] | |
| job_total_qty | jobTotalQty | Optional[int] | |
| job_total_value | jobTotalValue | Optional[float] | |
| is_current | isCurrent | Optional[bool] | |
| total_unpacked_weight | totalUnpackedWeight | Optional[float] | |
| job_items_total_container_lbs | jobItemsTotalContainerLbs | Optional[float] | |
| job_items_total_fill_lbs | jobItemsTotalFillLbs | Optional[float] | |
| job_items_total_materials | jobItemsTotalMaterials | Optional[float] | |
| job_items_total_labor_hrs | jobItemsTotalLaborHrs | Optional[float] | |
| job_items_total_gross_cubes | jobItemsTotalGrossCubes | Optional[float] | |
| job_items_total_net_cubes | jobItemsTotalNetCubes | Optional[float] | |
| job_items_total_materials_lbs | jobItemsTotalMaterialsLbs | Optional[float] | |
| job_items_total_labor_cost | jobItemsTotalLaborCost | Optional[float] | |
| job_tax_total_amount | jobTaxTotalAmount | Optional[float] | |
| job_total_cost | jobTotalCost | Optional[float] | |
| job_net_profit | jobNetProfit | Optional[float] | |
| created_date | createdDate | Optional[str] | |
| created_by | createdBy | Optional[str] | |
| sub_total | subTotal | Optional[float] | |
| sum_total | sumTotal | Optional[float] | |

### ActiveOnHoldInfo (new)

Server source: `OnHoldInfo` → `AB.ABCEntities.JobEntities.OnHold.OnHoldInfo`

| Python field | Alias | Type | Notes |
|-------------|-------|------|-------|
| id | id | Optional[int] | |
| responsible_party_type_id | responsiblePartyTypeId | Optional[str] | UUID |
| reason_id | reasonId | Optional[str] | UUID |
| responsible_party | responsibleParty | Optional[str] | |
| reason | reason | Optional[str] | |
| comment | comment | Optional[str] | |
| start_date | startDate | Optional[str] | ISO datetime |
| created_by | createdBy | Optional[str] | Creator name |

### JobDocument (new)

Server source: `DocumentDetails` → `AB.ABCEntities.Common.DocumentDetails`

| Python field | Alias | Type | Notes |
|-------------|-------|------|-------|
| id | id | Optional[int] | |
| path | path | Optional[str] | URL-encoded path |
| thumbnail_path | thumbnailPath | Optional[str] | |
| description | description | Optional[str] | |
| type_name | typeName | Optional[str] | |
| type_id | typeId | Optional[int] | |
| file_name | fileName | Optional[str] | |
| shared | shared | Optional[int] | |
| tags | tags | Optional[List[dict]] | |
| job_items | jobItems | Optional[List[dict]] | |

### JobSlaInfo (new)

Server source: `SlaInfo` → `AB.ABCEntities.JobEntities.SlaInfo`

| Python field | Alias | Type | Notes |
|-------------|-------|------|-------|
| days | days | Optional[int] | short in C# |
| expedited | expedited | Optional[bool] | |
| start_date | startDate | Optional[str] | |
| finish_date | finishDate | Optional[str] | |
| total_on_hold_days | totalOnHoldDays | Optional[int] | |

### JobFreightInfo (new)

Server source: `FreightTrackingLastDetails` → `AB.ABCEntities.JobEntities.FreightTrackingLastDetails`

Null in current fixture but typed from server source:

| Python field | Alias | Type | Notes |
|-------------|-------|------|-------|
| provider_company_code | providerCompanyCode | Optional[str] | |
| provider_company_name | providerCompanyName | Optional[str] | |
| pro_num | proNum | Optional[str] | PRO number |
| transportation_state | transportationState | Optional[int] | Enum: 0=Unknown,1=Ok,2=Warning,3=Error |
| transportation_state_description | transportationStateDescription | Optional[str] | |

### JobPaymentInfo (new)

Server source: `PaymentInfo` → `AB.ABCEntities.JobEntities.Payment.PaymentInfo`

Null in current fixture but typed from server source:

| Python field | Alias | Type | Notes |
|-------------|-------|------|-------|
| status_id | statusId | Optional[str] | UUID |
| status | status | Optional[str] | |
| ready_to_invoice_date | readyToInvoiceDate | Optional[str] | |
| invoice_date | invoiceDate | Optional[str] | |
| paid_date | paidDate | Optional[str] | |

### JobAgentPaymentInfo (new)

Server source: `AgentPaymentInfo` → `AB.ABCEntities.JobEntities.Payment.AgentPaymentInfo`

Null in current fixture but typed from server source:

| Python field | Alias | Type | Notes |
|-------------|-------|------|-------|
| amount | amount | Optional[float] | decimal in C# |
| paid_date | paidDate | Optional[str] | |

### JobFreightItem (new)

Server source: `FreightShimpment` inherits `ItemFeature`

Empty list in current fixture — typed from server source for forward compatibility:

| Python field | Alias | Type | Notes |
|-------------|-------|------|-------|
| job_id | jobID | Optional[str] | UUID |
| quantity | quantity | Optional[int] | |
| freight_item_id | freightItemId | Optional[str] | UUID |
| freight_item_class_id | freightItemClassId | Optional[str] | UUID |
| job_freight_id | jobFreightID | Optional[str] | UUID |
| freight_description | freightDescription | Optional[str] | |
| freight_item_value | freightItemValue | Optional[str] | String in C# |
| freight_item_class | freightItemClass | Optional[str] | |
| job_display_id | jobDisplayId | Optional[str] | |
| nmfc_item | nmfcItem | Optional[str] | |
| total_weight | totalWeight | Optional[float] | |

## Validation Rules

1. All sub-models inherit from `ResponseModel` (extra="allow" for forward compatibility)
2. All fields are `Optional` (response data varies by user access level)
3. Field aliases match exact API camelCase keys from fixture
4. API typos are preserved in aliases (e.g., `mateialMasterID`, `isPrefered`, `ModifiyDate`)
5. UUIDs represented as `Optional[str]` (not UUID type — matches existing SDK convention)
6. Dates represented as `Optional[str]` (not datetime — matches existing SDK convention for most models)

## Reused Models

| Model | Import from | Used by |
|-------|------------|---------|
| CompanyAddress | ab.api.models.common | JobContactDetails.address |
| Coordinates | ab.api.models.common | Nested in CompanyAddress |
