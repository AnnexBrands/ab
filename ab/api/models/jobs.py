"""Job models for ACPortal and ABC APIs."""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel
from ab.api.models.common import CompanyAddress
from ab.api.models.mixins import FullAuditModel, IdentifiedModel


# ---- Job GET response sub-models (018) ------------------------------------


class JobContactEmail(ResponseModel):
    """Email entry nested in JobContactDetails."""

    id: Optional[int] = Field(None, description="Email mapping ID")
    email: Optional[str] = Field(None, description="Email address")
    invalid: Optional[bool] = Field(None, description="Email invalid flag")
    dont_spam: Optional[bool] = Field(None, alias="dontSpam", description="Do-not-spam flag")


class JobContactPhone(ResponseModel):
    """Phone entry nested in JobContactDetails."""

    id: Optional[int] = Field(None, description="Phone mapping ID")
    phone: Optional[str] = Field(None, description="Phone number")


class ContactDetails(ResponseModel):
    """Full contact person — nested in JobContactDetails.contact.

    Maps to C# ContactDetails entity.
    """

    id: Optional[int] = Field(None, description="Contact integer ID")
    contact_display_id: Optional[str] = Field(None, alias="contactDisplayId", description="Display ID")
    full_name: Optional[str] = Field(None, alias="fullName", description="Full name")
    contact_type_id: Optional[int] = Field(None, alias="contactTypeId", description="Contact type")
    editable: Optional[bool] = Field(None, description="Whether contact is editable")
    is_empty: Optional[bool] = Field(None, alias="isEmpty", description="Empty contact flag")
    full_name_update_required: Optional[bool] = Field(
        None, alias="fullNameUpdateRequired", description="Full name update required"
    )
    emails_list: Optional[List[dict]] = Field(None, alias="emailsList", description="Email entries")
    phones_list: Optional[List[dict]] = Field(None, alias="phonesList", description="Phone entries")
    addresses_list: Optional[List[dict]] = Field(None, alias="addressesList", description="Address entries")
    fax: Optional[str] = Field(None, description="Fax number")
    primary_phone: Optional[str] = Field(None, alias="primaryPhone", description="Primary phone")
    primary_email: Optional[str] = Field(None, alias="primaryEmail", description="Primary email")
    care_of: Optional[str] = Field(None, alias="careOf", description="Care of")
    bol_notes: Optional[str] = Field(None, alias="bolNotes", description="BOL notes")
    tax_id: Optional[str] = Field(None, alias="taxId", description="Tax ID")
    is_business: Optional[bool] = Field(None, alias="isBusiness", description="Business contact flag")
    is_payer: Optional[bool] = Field(None, alias="isPayer", description="Payer flag")
    is_prefered: Optional[bool] = Field(None, alias="isPrefered", description="Preferred flag (API typo preserved)")
    is_private: Optional[bool] = Field(None, alias="isPrivate", description="Private contact flag")
    is_active: Optional[bool] = Field(None, alias="isActive", description="Active flag")
    company_id: Optional[str] = Field(None, alias="companyId", description="Company UUID")
    root_contact_id: Optional[str] = Field(None, alias="rootContactId", description="Root contact ID")
    owner_franchisee_id: Optional[str] = Field(None, alias="ownerFranchiseeId", description="Owner franchisee UUID")
    company: Optional[dict] = Field(None, description="Lightweight company summary")
    legacy_guid: Optional[str] = Field(None, alias="legacyGuid", description="Legacy GUID")
    is_primary: Optional[bool] = Field(None, alias="isPrimary", description="Primary contact flag")
    assistant: Optional[str] = Field(None, description="Assistant name")
    department: Optional[str] = Field(None, description="Department")
    web_site: Optional[str] = Field(None, alias="webSite", description="Website URL")
    birth_date: Optional[str] = Field(None, alias="birthDate", description="Birth date")
    job_title_id: Optional[str] = Field(None, alias="jobTitleId", description="Job title ID")
    job_title: Optional[str] = Field(None, alias="jobTitle", description="Job title")


class JobContactDetails(ResponseModel):
    """Contact wrapper — nested in Job as customerContact, pickupContact, deliveryContact.

    Maps to C# JobContactDetails entity. Reuses CompanyAddress from common.py.
    """

    id: Optional[int] = Field(None, description="Contact ID")
    contact: Optional[ContactDetails] = Field(None, description="Full contact person details")
    email: Optional[JobContactEmail] = Field(None, description="Primary email")
    phone: Optional[JobContactPhone] = Field(None, description="Primary phone")
    address: Optional[CompanyAddress] = Field(None, description="Physical address")
    care_of: Optional[str] = Field(None, alias="careOf", description="Care of")
    legacy_guid: Optional[str] = Field(None, alias="legacyGuid", description="Legacy GUID")
    contact_email_mapping_id: Optional[int] = Field(
        None, alias="contactEmailMappingId", description="Email mapping ID"
    )
    contact_phone_mapping_id: Optional[int] = Field(
        None, alias="contactPhoneMappingId", description="Phone mapping ID"
    )
    contact_address_mapping_id: Optional[int] = Field(
        None, alias="contactAddressMappingId", description="Address mapping ID"
    )
    dragged_from: Optional[str] = Field(None, alias="draggedFrom", description="Dragged from contact type")
    job_contact_type: Optional[str] = Field(None, alias="jobContactType", description="Job contact type")
    property_type: Optional[int] = Field(None, alias="propertyType", description="Property type classification")


class JobItemMaterial(ResponseModel):
    """Material used in a job item — nested in JobItem.materials.

    Maps to C# MasterMaterials entity.
    """

    job_id: Optional[str] = Field(None, alias="jobID", description="Job UUID")
    job_pack_material_id: Optional[str] = Field(None, alias="jobPackMaterialID", description="Pack material UUID")
    material_id: Optional[int] = Field(None, alias="materialID", description="Material integer ID")
    mateial_master_id: Optional[str] = Field(
        None, alias="mateialMasterID", description="Material master UUID (API typo preserved)"
    )
    material_quantity: Optional[float] = Field(None, alias="materialQuantity", description="Quantity")
    material_name: Optional[str] = Field(None, alias="materialName", description="Material name")
    material_description: Optional[str] = Field(None, alias="materialDescription", description="Material description")
    material_code: Optional[str] = Field(None, alias="materialCode", description="Material code")
    material_type: Optional[str] = Field(None, alias="materialType", description="Material type")
    material_unit: Optional[str] = Field(None, alias="materialUnit", description="Unit of measure")
    material_weight: Optional[float] = Field(None, alias="materialWeight", description="Weight per unit")
    material_length: Optional[float] = Field(None, alias="materialLength", description="Length")
    material_width: Optional[float] = Field(None, alias="materialWidth", description="Width")
    material_height: Optional[float] = Field(None, alias="materialHeight", description="Height")
    material_cost: Optional[float] = Field(None, alias="materialCost", description="Cost per unit")
    material_price: Optional[float] = Field(None, alias="materialPrice", description="Price per unit")
    material_waste_factor: Optional[float] = Field(None, alias="materialWasteFactor", description="Waste factor")
    material_total_cost: Optional[float] = Field(None, alias="materialTotalCost", description="Total cost")
    material_total_weight: Optional[float] = Field(None, alias="materialTotalWeight", description="Total weight")
    created_by: Optional[str] = Field(None, alias="createdBy", description="Created by UUID")
    modified_by: Optional[str] = Field(None, alias="modifiedBy", description="Modified by UUID")
    created_date: Optional[str] = Field(None, alias="createdDate", description="Created date")
    modified_date: Optional[str] = Field(None, alias="modifiedDate", description="Modified date")
    item_id: Optional[str] = Field(None, alias="itemID", description="Item UUID")
    quantity_actual: Optional[float] = Field(None, alias="quantityActual", description="Actual quantity used")
    is_automatic: Optional[bool] = Field(None, alias="isAutomatic", description="Auto-generated material")
    waste: Optional[float] = Field(None, description="Waste amount")
    price: Optional[float] = Field(None, description="Price")
    is_edited: Optional[bool] = Field(None, alias="isEdited", description="Manually edited flag")
    item_name: Optional[str] = Field(None, alias="itemName", description="Parent item name")
    item_description: Optional[str] = Field(None, alias="itemDescription", description="Parent item description")
    item_notes: Optional[str] = Field(None, alias="itemNotes", description="Parent item notes")
    job_item_id: Optional[str] = Field(None, alias="jobItemId", description="Job item UUID")
    company_id: Optional[str] = Field(None, alias="companyId", description="Company UUID")
    is_active: Optional[bool] = Field(None, alias="isActive", description="Active flag")


class JobItem(ResponseModel):
    """Job line item — nested in Job.items.

    Maps to C# Items entity (inherits MasterItems, ItemFeature).
    """

    job_display_id: Optional[int] = Field(None, alias="jobDisplayId", description="Job display ID")
    job_item_id: Optional[str] = Field(None, alias="jobItemID", description="Job item UUID")
    original_job_item_id: Optional[str] = Field(None, alias="originalJobItemId", description="Original job item UUID")
    job_id: Optional[str] = Field(None, alias="jobID", description="Job UUID")
    quantity: Optional[int] = Field(None, description="Quantity")
    original_qty: Optional[int] = Field(None, alias="originalQty", description="Original quantity")
    job_freight_id: Optional[str] = Field(None, alias="jobFreightID", description="Freight UUID")
    nmfc_item: Optional[str] = Field(None, alias="nmfcItem", description="NMFC item code")
    nmfc_sub: Optional[str] = Field(None, alias="nmfcSub", description="NMFC sub code")
    nmfc_sub_class: Optional[str] = Field(None, alias="nmfcSubClass", description="NMFC sub class")
    job_item_pkd_length: Optional[float] = Field(None, alias="jobItemPkdLength", description="Packed length")
    job_item_pkd_width: Optional[float] = Field(None, alias="jobItemPkdWidth", description="Packed width")
    job_item_pkd_height: Optional[float] = Field(None, alias="jobItemPkdHeight", description="Packed height")
    job_item_pkd_weight: Optional[float] = Field(None, alias="jobItemPkdWeight", description="Packed weight")
    is_fill_percent_changed: Optional[bool] = Field(
        None, alias="isFillPercentChanged", description="Fill percent changed flag"
    )
    c_fill_id: Optional[int] = Field(None, alias="cFillId", description="Fill type ID")
    container_id: Optional[int] = Field(None, alias="containerId", description="Container type ID")
    labor_hrs: Optional[float] = Field(None, alias="laborHrs", description="Labor hours")
    labor_charge: Optional[float] = Field(None, alias="laborCharge", description="Labor charge")
    user_id: Optional[str] = Field(None, alias="userId", description="User UUID")
    is_fill_changed: Optional[bool] = Field(None, alias="isFillChanged", description="Fill changed flag")
    is_container_changed: Optional[bool] = Field(
        None, alias="isContainerChanged", description="Container changed flag"
    )
    is_valid_container: Optional[bool] = Field(None, alias="isValidContainer", description="Valid container flag")
    is_valid_fill: Optional[bool] = Field(None, alias="isValidFill", description="Valid fill flag")
    inches_to_add: Optional[float] = Field(None, alias="inchesToAdd", description="Inches to add for packing")
    container_thickness: Optional[float] = Field(None, alias="containerThickness", description="Container thickness")
    is_inch_to_add_changed: Optional[bool] = Field(
        None, alias="isInchToAddChanged", description="Inches-to-add changed flag"
    )
    total_pcs: Optional[int] = Field(None, alias="totalPcs", description="Total pieces")
    description_of_products: Optional[str] = Field(
        None, alias="descriptionOfProducts", description="Product description"
    )
    total_items: Optional[int] = Field(None, alias="totalItems", description="Total items")
    auto_pack_off: Optional[bool] = Field(None, alias="autoPackOff", description="Auto-pack disabled flag")
    c_pack_value: Optional[str] = Field(None, alias="cPackValue", description="Pack type value")
    c_fill_value: Optional[str] = Field(None, alias="cFillValue", description="Fill type value")
    container_type: Optional[str] = Field(None, alias="containerType", description="Container type code")
    job_item_fill_percent: Optional[float] = Field(
        None, alias="jobItemFillPercent", description="Fill percentage"
    )
    container_weight: Optional[float] = Field(None, alias="containerWeight", description="Container weight")
    fill_weight: Optional[float] = Field(None, alias="fillWeight", description="Fill weight")
    material_weight: Optional[float] = Field(None, alias="materialWeight", description="Material weight")
    job_item_pkd_value: Optional[float] = Field(None, alias="jobItemPkdValue", description="Packed value")
    total_packed_value: Optional[float] = Field(None, alias="totalPackedValue", description="Total packed value")
    total_weight: Optional[float] = Field(None, alias="totalWeight", description="Total weight")
    stc: Optional[str] = Field(None, description="Said to contain")
    materials: Optional[List[JobItemMaterial]] = Field(None, description="Packing materials")
    material_total_cost: Optional[float] = Field(None, alias="materialTotalCost", description="Total material cost")
    is_access: Optional[bool] = Field(None, alias="isAccess", description="Access flag")
    job_item_parcel_value: Optional[float] = Field(
        None, alias="jobItemParcelValue", description="Parcel declared value"
    )
    total_labor_charge: Optional[float] = Field(None, alias="totalLaborCharge", description="Total labor charge")
    gross_cubic_feet: Optional[float] = Field(None, alias="grossCubicFeet", description="Gross cubic feet")
    row_number: Optional[int] = Field(None, alias="rowNumber", description="Row number")
    noted_conditions: Optional[str] = Field(None, alias="notedConditions", description="Noted conditions")
    job_item_notes: Optional[str] = Field(None, alias="jobItemNotes", description="Item notes")
    customer_item_id: Optional[str] = Field(None, alias="customerItemId", description="Customer item reference")
    document_exists: Optional[bool] = Field(None, alias="documentExists", description="Has attached documents")
    force_crate: Optional[bool] = Field(None, alias="forceCrate", description="Force crate flag")
    auto_pack_failed: Optional[bool] = Field(None, alias="autoPackFailed", description="Auto-pack failed flag")
    do_not_tip: Optional[bool] = Field(None, alias="doNotTip", description="Do not tip flag")
    commodity_id: Optional[int] = Field(None, alias="commodityId", description="Commodity ID")
    longest_dimension: Optional[float] = Field(None, alias="longestDimension", description="Longest dimension")
    second_dimension: Optional[float] = Field(None, alias="secondDimension", description="Second longest dimension")
    pkd_length_plus_girth: Optional[float] = Field(
        None, alias="pkdLengthPlusGirth", description="Packed length + girth"
    )
    requested_parcel_packagings: Optional[str] = Field(
        None, alias="requestedParcelPackagings", description="Requested parcel packagings"
    )
    parcel_package_type_id: Optional[int] = Field(
        None, alias="parcelPackageTypeId", description="Parcel package type ID"
    )
    transportation_length: Optional[int] = Field(
        None, alias="transportationLength", description="Transportation length"
    )
    transportation_width: Optional[int] = Field(None, alias="transportationWidth", description="Transportation width")
    transportation_height: Optional[int] = Field(
        None, alias="transportationHeight", description="Transportation height"
    )
    transportation_weight: Optional[float] = Field(
        None, alias="transportationWeight", description="Transportation weight"
    )
    ceiling_transportation_weight: Optional[int] = Field(
        None, alias="ceilingTransportationWeight", description="Ceiling transportation weight"
    )
    company_id: Optional[str] = Field(None, alias="companyID", description="Company UUID")
    company_name: Optional[str] = Field(None, alias="companyName", description="Company name")
    item_sequence_no: Optional[int] = Field(None, alias="itemSequenceNo", description="Item sequence number")
    item_name: Optional[str] = Field(None, alias="itemName", description="Item name")
    item_description: Optional[str] = Field(None, alias="itemDescription", description="Item description")
    schedule_b: Optional[str] = Field(None, alias="scheduleB", description="Schedule B export code")
    eccn: Optional[str] = Field(None, description="Export control classification number")
    item_notes: Optional[str] = Field(None, alias="itemNotes", description="Item notes")
    is_prepacked: Optional[bool] = Field(None, alias="isPrepacked", description="Pre-packed flag")
    item_active: Optional[bool] = Field(None, alias="itemActive", description="Item active flag")
    item_public: Optional[bool] = Field(None, alias="itemPublic", description="Item public flag")
    c_pack_id: Optional[str] = Field(None, alias="cPackId", description="Pack type UUID")
    item_id: Optional[str] = Field(None, alias="itemID", description="Item UUID")
    item_value: Optional[float] = Field(None, alias="itemValue", description="Declared value")
    modified_by: Optional[str] = Field(None, alias="modifiedBy", description="Modified by UUID")
    created_by: Optional[str] = Field(None, alias="createdBy", description="Created by UUID")
    created_date: Optional[str] = Field(None, alias="createdDate", description="Created date")
    modified_date: Optional[str] = Field(None, alias="modifiedDate", description="Modified date")
    item_length: Optional[float] = Field(None, alias="itemLength", description="Item length")
    item_width: Optional[float] = Field(None, alias="itemWidth", description="Item width")
    item_height: Optional[float] = Field(None, alias="itemHeight", description="Item height")
    item_weight: Optional[float] = Field(None, alias="itemWeight", description="Item weight")
    net_cubic_feet: Optional[float] = Field(None, alias="netCubicFeet", description="Net cubic feet")


class JobSummarySnapshot(ResponseModel):
    """Financial/weight rollup — nested in Job.job_summary_snapshot.

    Maps to C# JobSummary entity.
    """

    job_snapshot_id: Optional[int] = Field(None, alias="jobSnapshotID", description="Snapshot ID")
    job_id: Optional[str] = Field(None, alias="jobID", description="Job UUID")
    job_status_id: Optional[str] = Field(None, alias="jobStatusID", description="Status UUID")
    job_total_amount: Optional[float] = Field(None, alias="jobTotalAmount", description="Total amount")
    job_total_weight: Optional[float] = Field(None, alias="jobTotalWeight", description="Total weight")
    job_total_qty: Optional[int] = Field(None, alias="jobTotalQty", description="Total quantity")
    job_total_value: Optional[float] = Field(None, alias="jobTotalValue", description="Total value")
    is_current: Optional[bool] = Field(None, alias="isCurrent", description="Current snapshot flag")
    total_unpacked_weight: Optional[float] = Field(
        None, alias="totalUnpackedWeight", description="Total unpacked weight"
    )
    job_items_total_container_lbs: Optional[float] = Field(
        None, alias="jobItemsTotalContainerLbs", description="Total container weight (lbs)"
    )
    job_items_total_fill_lbs: Optional[float] = Field(
        None, alias="jobItemsTotalFillLbs", description="Total fill weight (lbs)"
    )
    job_items_total_materials: Optional[float] = Field(
        None, alias="jobItemsTotalMaterials", description="Total materials cost"
    )
    job_items_total_labor_hrs: Optional[float] = Field(
        None, alias="jobItemsTotalLaborHrs", description="Total labor hours"
    )
    job_items_total_gross_cubes: Optional[float] = Field(
        None, alias="jobItemsTotalGrossCubes", description="Total gross cubic feet"
    )
    job_items_total_net_cubes: Optional[float] = Field(
        None, alias="jobItemsTotalNetCubes", description="Total net cubic feet"
    )
    job_items_total_materials_lbs: Optional[float] = Field(
        None, alias="jobItemsTotalMaterialsLbs", description="Total materials weight (lbs)"
    )
    job_items_total_labor_cost: Optional[float] = Field(
        None, alias="jobItemsTotalLaborCost", description="Total labor cost"
    )
    job_tax_total_amount: Optional[float] = Field(
        None, alias="jobTaxTotalAmount", description="Total tax amount"
    )
    job_total_cost: Optional[float] = Field(None, alias="jobTotalCost", description="Total cost")
    job_net_profit: Optional[float] = Field(None, alias="jobNetProfit", description="Net profit")
    created_date: Optional[str] = Field(None, alias="createdDate", description="Created date")
    created_by: Optional[str] = Field(None, alias="createdBy", description="Created by UUID")
    sub_total: Optional[float] = Field(None, alias="subTotal", description="Sub total")
    sum_total: Optional[float] = Field(None, alias="sumTotal", description="Sum total")


class ActiveOnHoldInfo(ResponseModel):
    """Active on-hold info — nested in Job.active_on_hold_info.

    Maps to C# OnHoldInfo entity.
    """

    id: Optional[int] = Field(None, description="On-hold record ID")
    responsible_party_type_id: Optional[str] = Field(
        None, alias="responsiblePartyTypeId", description="Responsible party type UUID"
    )
    reason_id: Optional[str] = Field(None, alias="reasonId", description="Reason UUID")
    responsible_party: Optional[str] = Field(None, alias="responsibleParty", description="Responsible party name")
    reason: Optional[str] = Field(None, description="Hold reason")
    comment: Optional[str] = Field(None, description="Hold comment")
    start_date: Optional[str] = Field(None, alias="startDate", description="Hold start date")
    created_by: Optional[str] = Field(None, alias="createdBy", description="Creator name")


class JobDocument(ResponseModel):
    """Document attachment — nested in Job.documents.

    Maps to C# DocumentDetails entity.
    """

    id: Optional[int] = Field(None, description="Document ID")
    path: Optional[str] = Field(None, description="Document URL path")
    thumbnail_path: Optional[str] = Field(None, alias="thumbnailPath", description="Thumbnail URL path")
    description: Optional[str] = Field(None, description="Document description")
    type_name: Optional[str] = Field(None, alias="typeName", description="Document type name")
    type_id: Optional[int] = Field(None, alias="typeId", description="Document type ID")
    file_name: Optional[str] = Field(None, alias="fileName", description="File name")
    shared: Optional[int] = Field(None, description="Shared flag")
    tags: Optional[List[dict]] = Field(None, description="Document tags")
    job_items: Optional[List[str]] = Field(None, alias="jobItems", description="Associated job item UUIDs")


class JobSlaInfo(ResponseModel):
    """SLA tracking — nested in Job.sla_info.

    Maps to C# SlaInfo entity.
    """

    days: Optional[int] = Field(None, description="SLA days")
    expedited: Optional[bool] = Field(None, description="Expedited flag")
    start_date: Optional[str] = Field(None, alias="startDate", description="SLA start date")
    finish_date: Optional[str] = Field(None, alias="finishDate", description="SLA finish date")
    total_on_hold_days: Optional[int] = Field(None, alias="totalOnHoldDays", description="Total on-hold days")


class JobFreightInfo(ResponseModel):
    """Freight tracking summary — nested in Job.freight_info.

    Maps to C# FreightTrackingLastDetails entity.
    """

    provider_company_code: Optional[str] = Field(
        None, alias="providerCompanyCode", description="Provider company code"
    )
    provider_company_name: Optional[str] = Field(
        None, alias="providerCompanyName", description="Provider company name"
    )
    pro_num: Optional[str] = Field(None, alias="proNum", description="PRO number")
    transportation_state: Optional[int] = Field(
        None, alias="transportationState", description="State enum: 0=Unknown, 1=Ok, 2=Warning, 3=Error"
    )
    transportation_state_description: Optional[str] = Field(
        None, alias="transportationStateDescription", description="State description"
    )


class JobPaymentInfo(ResponseModel):
    """Payment status — nested in Job.payment_info.

    Maps to C# PaymentInfo entity.
    """

    status_id: Optional[str] = Field(None, alias="statusId", description="Payment status UUID")
    status: Optional[str] = Field(None, description="Payment status text")
    ready_to_invoice_date: Optional[str] = Field(
        None, alias="readyToInvoiceDate", description="Ready to invoice date"
    )
    invoice_date: Optional[str] = Field(None, alias="invoiceDate", description="Invoice date")
    paid_date: Optional[str] = Field(None, alias="paidDate", description="Paid date")


class JobAgentPaymentInfo(ResponseModel):
    """Agent payment info — nested in Job.agent_payment_info.

    Maps to C# AgentPaymentInfo entity.
    """

    amount: Optional[float] = Field(None, description="Payment amount")
    paid_date: Optional[str] = Field(None, alias="paidDate", description="Paid date")


class JobFreightItem(ResponseModel):
    """Freight shipment item — nested in Job.freight_items.

    Maps to C# FreightShimpment entity (inherits ItemFeature).
    """

    job_id: Optional[str] = Field(None, alias="jobID", description="Job UUID")
    quantity: Optional[int] = Field(None, description="Quantity")
    freight_item_id: Optional[str] = Field(None, alias="freightItemId", description="Freight item UUID")
    freight_item_class_id: Optional[str] = Field(
        None, alias="freightItemClassId", description="Freight item class UUID"
    )
    job_freight_id: Optional[str] = Field(None, alias="jobFreightID", description="Job freight UUID")
    freight_description: Optional[str] = Field(None, alias="freightDescription", description="Freight description")
    freight_item_value: Optional[str] = Field(None, alias="freightItemValue", description="Freight item value")
    freight_item_class: Optional[str] = Field(None, alias="freightItemClass", description="Freight item class")
    job_display_id: Optional[str] = Field(None, alias="jobDisplayId", description="Job display ID")
    nmfc_item: Optional[str] = Field(None, alias="nmfcItem", description="NMFC item code")
    total_weight: Optional[float] = Field(None, alias="totalWeight", description="Total weight")


# ---- Job primary response model -------------------------------------------


class JobSearchParams(RequestModel):
    """Query parameters for GET /job/search."""

    job_display_id: Optional[int] = Field(None, alias="jobDisplayId", description="Job display ID to search for")


class FreightProvidersParams(RequestModel):
    """Query parameters for GET /job/{jobDisplayId}/freightproviders."""

    provider_indexes: Optional[List[int]] = Field(
        None, alias="ProviderIndexes", description="Filter by provider option indexes"
    )
    shipment_types: Optional[List[str]] = Field(
        None, alias="ShipmentTypes", description="Filter by shipment type UUIDs"
    )
    only_active: Optional[bool] = Field(None, alias="OnlyActive", description="Show only active providers")


class TimelineCreateParams(RequestModel):
    """Query parameters for POST /job/{jobDisplayId}/timeline."""

    create_email: Optional[bool] = Field(None, alias="createEmail")


class TrackingV3Params(RequestModel):
    """Query parameters for GET /v3/job/{jobDisplayId}/tracking."""

    history_amount: Optional[int] = Field(None, alias="historyAmount")


class JobNoteListParams(RequestModel):
    """Query parameters for GET /job/{jobDisplayId}/note."""

    category: Optional[str] = Field(None, alias="category")
    task_code: Optional[str] = Field(None, alias="taskCode")


class JobRfqListParams(RequestModel):
    """Query parameters for GET /job/{jobDisplayId}/rfq."""

    rfq_service_type: Optional[str] = Field(None, alias="rfqServiceType")


class Job(ResponseModel, FullAuditModel):
    """Full job record — GET /job/{jobDisplayId}.

    Maps to C# JobPortalInfo entity. Response shape varies by
    JobAccessLevel (Owner/Customer gets full data, Agent gets filtered).
    """

    job_display_id: Optional[int] = Field(None, alias="jobDisplayId", description="Human-readable job ID")
    status: Optional[str] = Field(None, description="Job status")
    customer: Optional[dict] = Field(None, description="Customer details")
    pickup: Optional[dict] = Field(None, description="Pickup info")
    delivery: Optional[dict] = Field(None, description="Delivery info")
    items: Optional[List[JobItem]] = Field(None, description="Line items")

    # ---- Fields added in 018-job-get-response ----
    booked_date: Optional[str] = Field(None, alias="bookedDate", description="Booking date")
    owner_company_id: Optional[str] = Field(None, alias="ownerCompanyId", description="Owner company UUID")
    customer_contact: Optional[JobContactDetails] = Field(
        None, alias="customerContact", description="Customer contact details"
    )
    pickup_contact: Optional[JobContactDetails] = Field(
        None, alias="pickupContact", description="Pickup contact details"
    )
    delivery_contact: Optional[JobContactDetails] = Field(
        None, alias="deliveryContact", description="Delivery contact details"
    )
    total_sell_price: Optional[float] = Field(None, alias="totalSellPrice", description="Total sell price")
    freight_items: Optional[List[JobFreightItem]] = Field(
        None, alias="freightItems", description="Freight shipment items"
    )
    job_summary_snapshot: Optional[JobSummarySnapshot] = Field(
        None, alias="jobSummarySnapshot", description="Financial/weight summary snapshot"
    )
    notes: Optional[List[dict]] = Field(None, description="Job notes")
    active_on_hold_info: Optional[ActiveOnHoldInfo] = Field(
        None, alias="activeOnHoldInfo", description="Active on-hold details"
    )
    write_access: Optional[bool] = Field(None, alias="writeAccess", description="User write access flag")
    access_level: Optional[int] = Field(None, alias="accessLevel", description="User access level bitmask")
    status_id: Optional[str] = Field(None, alias="statusId", description="Job status UUID")
    job_mgmt_sub_id: Optional[str] = Field(None, alias="jobMgmtSubId", description="Job management sub UUID")
    is_cancelled: Optional[bool] = Field(None, alias="isCancelled", description="Cancelled flag")
    freight_info: Optional[JobFreightInfo] = Field(
        None, alias="freightInfo", description="Freight tracking summary"
    )
    freight_providers: Optional[List[dict]] = Field(
        None, alias="freightProviders", description="Freight provider options"
    )
    expected_pickup_date: Optional[str] = Field(
        None, alias="expectedPickupDate", description="Expected pickup date"
    )
    expected_delivery_date: Optional[str] = Field(
        None, alias="expectedDeliveryDate", description="Expected delivery date"
    )
    timeline_tasks: Optional[List[dict]] = Field(
        None, alias="timelineTasks", description="Timeline task entries"
    )
    documents: Optional[List[JobDocument]] = Field(None, description="Attached documents")
    label_request_sent_date: Optional[str] = Field(
        None, alias="labelRequestSentDate", description="Label request sent date"
    )
    payment_info: Optional[JobPaymentInfo] = Field(
        None, alias="paymentInfo", description="Payment status"
    )
    agent_payment_info: Optional[JobAgentPaymentInfo] = Field(
        None, alias="agentPaymentInfo", description="Agent payment info"
    )
    sla_info: Optional[JobSlaInfo] = Field(None, alias="slaInfo", description="SLA tracking info")
    job_type: Optional[str] = Field(None, alias="jobType", description="Job type")
    prices: Optional[List[dict]] = Field(None, description="Price entries")


class JobSearchResult(ResponseModel):
    """Single search hit — GET /job/search and POST /job/searchByDetails.

    The live API returns ``jobDisplayID`` (capital *ID*) as a string,
    not the camelCase ``jobDisplayId`` that swagger shows.
    """

    job_display_id: Optional[str] = Field(None, alias="jobDisplayID", description="Display ID (string)")
    job_id: Optional[str] = Field(None, alias="jobID", description="Job UUID")
    customer_full_name: Optional[str] = Field(None, alias="customerFullName", description="Customer full name")
    customer_phone_number: Optional[str] = Field(None, alias="customerPhoneNumber", description="Customer phone")
    jobstatus: Optional[str] = Field(None, description="Job status text")
    company_name: Optional[str] = Field(None, alias="companyName", description="Company name")
    agent_code: Optional[str] = Field(None, alias="agentCode", description="Agent code")
    job_total_amount: Optional[float] = Field(None, alias="jobTotalAmount", description="Total amount")
    pu_address1: Optional[str] = Field(None, alias="puAddress1", description="Pickup address line 1")
    pu_city: Optional[str] = Field(None, alias="puCity", description="Pickup city")
    pu_state: Optional[str] = Field(None, alias="puState", description="Pickup state")
    del_city: Optional[str] = Field(None, alias="delCity", description="Delivery city")
    del_state: Optional[str] = Field(None, alias="delState", description="Delivery state")
    status_id: Optional[str] = Field(None, alias="statusID", description="Status UUID")


class JobPrice(ResponseModel):
    """Price info — GET /job/{jobDisplayId}/price."""

    job_display_id: Optional[int] = Field(None, alias="jobDisplayId")
    prices: Optional[List[dict]] = Field(None, description="Price breakdowns")
    total: Optional[float] = Field(None, description="Total price")
    total_sell_price: Optional[float] = Field(None, alias="totalSellPrice", description="Total sell price")


class CalendarItem(ResponseModel):
    """Calendar/line item — GET /job/{jobDisplayId}/calendaritems.

    Despite the name, the live API returns job line-item details
    (name, quantity, dimensions, value) rather than calendar events.
    """

    id: Optional[str] = Field(None, description="Item UUID")
    title: Optional[str] = Field(None, description="Item title")
    start: Optional[str] = Field(None, description="Start datetime")
    end: Optional[str] = Field(None, description="End datetime")
    name: Optional[str] = Field(None, description="Item name/description")
    quantity: Optional[int] = Field(None, description="Quantity")
    length: Optional[float] = Field(None, description="Length dimension")
    width: Optional[float] = Field(None, description="Width dimension")
    height: Optional[float] = Field(None, description="Height dimension")
    weight: Optional[float] = Field(None, description="Weight")
    value: Optional[float] = Field(None, description="Declared value")
    notes: Optional[str] = Field(None, description="Item notes")
    customer_item_id: Optional[str] = Field(None, alias="customerItemId", description="Customer item reference")
    noted_conditions: Optional[str] = Field(None, alias="notedConditions", description="Noted conditions for item")


class JobUpdatePageConfig(ResponseModel):
    """Update page config — GET /job/{id}/updatePageConfig."""

    config: Optional[dict] = Field(None, description="Page configuration data")
    page_controls: Optional[int] = Field(None, alias="pageControls", description="Page control bitmask")
    workflow_controls: Optional[int] = Field(None, alias="workflowControls", description="Workflow control bitmask")


class JobCreateRequest(RequestModel):
    """Body for POST /job."""

    customer: Optional[dict] = Field(None, description="Customer details")
    pickup: Optional[dict] = Field(None, description="Pickup info")
    delivery: Optional[dict] = Field(None, description="Delivery info")
    items: Optional[List[dict]] = Field(None, description="Line items")
    services: Optional[List[dict]] = Field(None, description="Requested services")


class JobSaveRequest(RequestModel):
    """Body for PUT /job/save."""

    job_display_id: Optional[int] = Field(None, alias="jobDisplayId")
    # Additional fields from job data
    customer: Optional[dict] = Field(None)
    pickup: Optional[dict] = Field(None)
    delivery: Optional[dict] = Field(None)
    items: Optional[List[dict]] = Field(None)


class SortByModel(RequestModel):
    """Sort configuration for POST /job/searchByDetails."""

    sort_by_field: int = Field(1, alias="sortByField", description="Sort field enum value")
    sort_dir: bool = Field(True, alias="sortDir", description="Sort direction (true=asc)")


class JobSearchRequest(RequestModel):
    """Body for POST /job/searchByDetails."""

    search_text: Optional[str] = Field(None, alias="searchText", description="Search query")
    page_no: int = Field(1, alias="pageNo", description="Page number")
    page_size: int = Field(25, alias="pageSize", description="Results per page")
    sort_by: SortByModel = Field(
        default_factory=lambda: SortByModel(sort_by_field=1, sort_dir=True),
        alias="sortBy",
        description="Sort configuration",
    )


class JobUpdateRequest(RequestModel):
    """Body for POST /job/update (ABC API surface)."""

    job_id: Optional[str] = Field(None, alias="jobId", description="Job UUID")
    # Fields defined by ABC API — details from fixture
    updates: Optional[dict] = Field(None, description="Update payload")


# ---- Timeline / Status models -----------------------------------------


class TimelineTask(ResponseModel, IdentifiedModel):
    """Timeline task — GET /job/{jobDisplayId}/timeline."""

    id: Optional[str] = Field(None, description="Timeline task ID")
    task_code: Optional[str] = Field(None, alias="taskCode", description="Task type code")
    status: Optional[int] = Field(None, description="Status code")
    status_name: Optional[str] = Field(None, alias="statusName", description="Human-readable status")
    agent_contact_id: Optional[str] = Field(None, alias="agentContactId", description="Assigned agent")
    scheduled_date: Optional[str] = Field(None, alias="scheduledDate", description="When task is scheduled")
    completed_date: Optional[str] = Field(None, alias="completedDate", description="When task was completed")
    comments: Optional[str] = Field(None, description="Task notes")
    is_completed: Optional[bool] = Field(None, alias="isCompleted", description="Completion flag")
    sort_order: Optional[int] = Field(None, alias="sortOrder", description="Display order")


class TimelineAgent(ResponseModel):
    """Timeline agent — GET /job/{jobDisplayId}/timeline/{taskCode}/agent."""

    contact_id: Optional[str] = Field(None, alias="contactId", description="Agent contact ID")
    name: Optional[str] = Field(None, description="Agent name")
    company_name: Optional[str] = Field(None, alias="companyName", description="Agent's company")


class TimelineTaskCreateRequest(RequestModel):
    """Body for POST /job/{jobDisplayId}/timeline."""

    task_code: str = Field(..., alias="taskCode", description="Task type code")
    scheduled_date: Optional[str] = Field(None, alias="scheduledDate", description="Scheduled date")
    comments: Optional[str] = Field(None, description="Notes")
    agent_contact_id: Optional[str] = Field(None, alias="agentContactId", description="Assigned agent")


class TimelineTaskUpdateRequest(RequestModel):
    """Body for PATCH /job/{jobDisplayId}/timeline/{timelineTaskId}."""

    status: Optional[int] = Field(None, description="New status code")
    scheduled_date: Optional[str] = Field(None, alias="scheduledDate", description="Updated schedule")
    completed_date: Optional[str] = Field(None, alias="completedDate", description="Completion date")
    comments: Optional[str] = Field(None, description="Updated notes")


class IncrementStatusRequest(RequestModel):
    """Body for POST /job/{jobDisplayId}/timeline/incrementjobstatus."""

    create_email: Optional[bool] = Field(None, alias="createEmail", description="Send status notification email")


# ---- Tracking models --------------------------------------------------


class TrackingInfo(ResponseModel):
    """Tracking info — GET /job/{jobDisplayId}/tracking."""

    status: Optional[str] = Field(None, description="Current tracking status")
    location: Optional[str] = Field(None, description="Current location")
    estimated_delivery: Optional[str] = Field(None, alias="estimatedDelivery", description="ETA")
    events: Optional[List[dict]] = Field(None, description="Tracking event history")
    carrier_name: Optional[str] = Field(None, alias="carrierName", description="Carrier")
    pro_number: Optional[str] = Field(None, alias="proNumber", description="PRO number")


class TrackingInfoV3(ResponseModel):
    """Tracking info v3 — GET /v3/job/{jobDisplayId}/tracking/{historyAmount}."""

    tracking_details: Optional[List[dict]] = Field(
        None, alias="trackingDetails", description="Detailed tracking entries",
    )
    carrier_info: Optional[List[dict]] = Field(None, alias="carrierInfo", description="Carrier metadata")
    shipment_status: Optional[str] = Field(None, alias="shipmentStatus", description="Overall status")


# ---- Notes models -----------------------------------------------------


class JobNote(ResponseModel, IdentifiedModel):
    """Job note — GET /job/{jobDisplayId}/note."""

    id: Optional[str] = Field(None, description="Note ID")
    comment: Optional[str] = Field(None, description="Note content")
    is_important: Optional[bool] = Field(None, alias="isImportant", description="Flagged as important")
    is_completed: Optional[bool] = Field(None, alias="isCompleted", description="Completion status")
    author: Optional[str] = Field(None, description="Author name")
    modify_date: Optional[str] = Field(None, alias="modifiyDate", description="Last modified (API typo preserved)")
    task_code: Optional[str] = Field(None, alias="taskCode", description="Associated timeline task")


class JobNoteCreateRequest(RequestModel):
    """Body for POST /job/{jobDisplayId}/note."""

    comments: str = Field(..., description="Note content (max 8000 chars)")
    task_code: str = Field(..., alias="taskCode", description="Associated timeline task code")
    is_important: Optional[bool] = Field(None, alias="isImportant", description="Flag as important")
    send_notification: Optional[bool] = Field(None, alias="sendNotification", description="Notify assigned users")
    due_date: Optional[str] = Field(None, alias="dueDate", description="Due date")


class JobNoteUpdateRequest(RequestModel):
    """Body for PUT /job/{jobDisplayId}/note/{id}."""

    comments: Optional[str] = Field(None, description="Updated content")
    is_important: Optional[bool] = Field(None, alias="isImportant", description="Updated flag")
    is_completed: Optional[bool] = Field(None, alias="isCompleted", description="Mark complete")


# ---- Parcels & Items models -------------------------------------------


class ParcelItem(ResponseModel):
    """Parcel item — GET /job/{jobDisplayId}/parcelitems.

    Maps to C# ParcelItemWithPackage entity.
    """

    id: Optional[int] = Field(None, description="Parcel item ID")
    job_item_id: Optional[str] = Field(None, alias="jobItemId", description="Job item UUID")
    description: Optional[str] = Field(None, description="Item description")
    quantity: Optional[int] = Field(None, description="Number of pieces")
    job_item_pkd_length: Optional[float] = Field(None, alias="jobItemPkdLength", description="Packed length")
    job_item_pkd_width: Optional[float] = Field(None, alias="jobItemPkdWidth", description="Packed width")
    job_item_pkd_height: Optional[float] = Field(None, alias="jobItemPkdHeight", description="Packed height")
    job_item_pkd_weight: Optional[float] = Field(None, alias="jobItemPkdWeight", description="Packed weight")
    job_item_parcel_value: Optional[float] = Field(None, alias="jobItemParcelValue", description="Declared value")
    parcel_package_type_id: Optional[int] = Field(None, alias="parcelPackageTypeId", description="Package type ID")
    insure_key: Optional[str] = Field(None, alias="insureKey", description="Insurance key")
    package_type_code: Optional[str] = Field(None, alias="packageTypeCode", description="Package type code")


class JobParcelItemMaterial(ResponseModel):
    """Material used in a parcel item — nested in ParcelItemWithMaterials."""

    name: Optional[str] = Field(None, description="Material name")
    description: Optional[str] = Field(None, description="Material description")
    code: Optional[str] = Field(None, description="Material code")
    type: Optional[str] = Field(None, description="Material type")
    weight: Optional[float] = Field(None, description="Weight")
    length: Optional[float] = Field(None, description="Length")
    width: Optional[float] = Field(None, description="Width")
    height: Optional[float] = Field(None, description="Height")
    cost: Optional[float] = Field(None, description="Cost")
    price: Optional[float] = Field(None, description="Price")
    quantity: Optional[float] = Field(None, description="Quantity")


class ParcelItemWithMaterials(ParcelItem):
    """Parcel item with materials — GET /job/{jobDisplayId}/parcel-items-with-materials."""

    materials: Optional[List[JobParcelItemMaterial]] = Field(None, description="Associated materials")


class PackagingContainer(ResponseModel):
    """Packaging container — GET /job/{jobDisplayId}/packagingcontainers.

    Maps to C# Packaging entity.
    """

    name: Optional[str] = Field(None, description="Container name")
    description: Optional[str] = Field(None, description="Container description")
    length: Optional[float] = Field(None, description="Length")
    width: Optional[float] = Field(None, description="Width")
    height: Optional[float] = Field(None, description="Height")
    weight: Optional[float] = Field(None, description="Weight")
    total_cost: Optional[float] = Field(None, alias="totalCost", description="Total cost")


class ParcelItemCreateRequest(RequestModel):
    """Body for POST /job/{jobDisplayId}/parcelitems."""

    description: str = Field(..., description="Item description")
    length: Optional[float] = Field(None, description="Length")
    width: Optional[float] = Field(None, description="Width")
    height: Optional[float] = Field(None, description="Height")
    weight: Optional[float] = Field(None, description="Weight")
    quantity: Optional[int] = Field(None, description="Quantity")


class ItemNotesRequest(RequestModel):
    """Body for POST /job/{jobDisplayId}/item/notes."""

    notes: str = Field(..., description="Item notes content")


class ItemUpdateRequest(RequestModel):
    """Body for PUT /job/{jobDisplayId}/item/{itemId}."""

    description: Optional[str] = Field(None, description="Updated description")
    quantity: Optional[int] = Field(None, description="Updated quantity")
    weight: Optional[float] = Field(None, description="Updated weight")


# ---- On-Hold models (008) ------------------------------------------------


class ExtendedOnHoldInfo(ResponseModel):
    """On-hold listing entry — GET /job/{jobDisplayId}/onhold."""

    id: Optional[str] = Field(None, description="On-hold record ID")
    reason: Optional[str] = Field(None, description="Hold reason")
    description: Optional[str] = Field(None, description="Hold description")
    follow_up_user: Optional[str] = Field(None, alias="followUpUser", description="Follow-up user name")
    follow_up_date: Optional[str] = Field(None, alias="followUpDate", description="Follow-up date")
    status: Optional[str] = Field(None, description="Hold status")
    created_date: Optional[str] = Field(None, alias="createdDate", description="Created date")


class OnHoldDetails(ResponseModel):
    """Full on-hold detail — GET /job/{jobDisplayId}/onhold/{id}."""

    id: Optional[str] = Field(None, description="On-hold record ID")
    reason: Optional[str] = Field(None, description="Hold reason")
    description: Optional[str] = Field(None, description="Hold description")
    comments: Optional[List[dict]] = Field(None, description="Associated comments")
    dates: Optional[dict] = Field(None, description="Date information")
    follow_up_user: Optional[dict] = Field(None, alias="followUpUser", description="Follow-up user details")
    status: Optional[str] = Field(None, description="Hold status")


class SaveOnHoldRequest(RequestModel):
    """Body for POST/PUT /job/{jobDisplayId}/onhold."""

    reason: Optional[str] = Field(None, description="Hold reason")
    description: Optional[str] = Field(None, description="Hold description")
    follow_up_contact_id: Optional[str] = Field(None, alias="followUpContactId", description="Follow-up contact ID")
    follow_up_date: Optional[str] = Field(None, alias="followUpDate", description="Follow-up date")


class SaveOnHoldResponse(ResponseModel):
    """On-hold create/update response."""

    on_hold_id: Optional[str] = Field(None, alias="onHoldId", description="On-hold record ID")
    status: Optional[str] = Field(None, description="Operation status")


class ResolveJobOnHoldResponse(ResponseModel):
    """On-hold resolution response."""

    resolved: Optional[bool] = Field(None, description="Whether resolved successfully")
    status: Optional[str] = Field(None, description="Resolution status")


class SaveOnHoldDatesModel(RequestModel):
    """Body for PUT /job/{jobDisplayId}/onhold/{onHoldId}/dates."""

    follow_up_date: Optional[str] = Field(None, alias="followUpDate", description="Follow-up date")
    due_date: Optional[str] = Field(None, alias="dueDate", description="Due date")


class OnHoldUser(ResponseModel):
    """Follow-up user info — GET /job/{jobDisplayId}/onhold/followupuser/{contactId}."""

    contact_id: Optional[str] = Field(None, alias="contactId", description="Contact ID")
    name: Optional[str] = Field(None, description="User name")
    email: Optional[str] = Field(None, description="User email")


class OnHoldNoteDetails(ResponseModel):
    """On-hold comment — POST /job/{jobDisplayId}/onhold/{onHoldId}/comment."""

    id: Optional[str] = Field(None, description="Comment ID")
    comment: Optional[str] = Field(None, description="Comment text")
    author: Optional[str] = Field(None, description="Author name")
    date: Optional[str] = Field(None, description="Comment date")


# ---- Email/SMS models (008) -----------------------------------------------


class SendDocumentEmailModel(RequestModel):
    """Body for POST /job/{jobDisplayId}/email/senddocument."""

    to: Optional[List[str]] = Field(None, description="Recipient emails")
    cc: Optional[List[str]] = Field(None, description="CC emails")
    bcc: Optional[List[str]] = Field(None, description="BCC emails")
    subject: Optional[str] = Field(None, description="Email subject")
    body: Optional[str] = Field(None, description="Email body")
    document_type: Optional[str] = Field(None, alias="documentType", description="Document type")


class SendSMSModel(RequestModel):
    """Body for POST /job/{jobDisplayId}/sms."""

    phone_number: Optional[str] = Field(None, alias="phoneNumber", description="Phone number")
    message: Optional[str] = Field(None, description="SMS message body")
    template_id: Optional[str] = Field(None, alias="templateId", description="SMS template ID")


class MarkSmsAsReadModel(RequestModel):
    """Body for POST /job/{jobDisplayId}/sms/read."""

    sms_ids: Optional[List[str]] = Field(None, alias="smsIds", description="SMS IDs to mark read")


# ---- Freight provider models (008) ----------------------------------------


class PricedFreightProvider(ResponseModel):
    """Freight provider with pricing — GET /job/{jobDisplayId}/freightproviders."""

    provider_name: Optional[str] = Field(None, alias="providerName", description="Provider name")
    service_types: Optional[List[dict]] = Field(None, alias="serviceTypes", description="Available service types")
    rate_available: Optional[bool] = Field(None, alias="rateAvailable", description="Whether rate is available")


class ShipmentPlanProvider(RequestModel):
    """Save freight provider selection — POST /job/{jobDisplayId}/freightproviders."""

    provider_data: Optional[dict] = Field(None, alias="providerData", description="Provider selection data")
