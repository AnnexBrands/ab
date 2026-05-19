"""AutoPrice models for the ABC API."""

from __future__ import annotations

from typing import List, Optional

from pydantic import AliasChoices, Field

from ab.api.models.base import RequestModel, ResponseModel


def _api_field(default: object, *aliases: str, description: str):
    """Create a field that accepts swagger casing and emits API casing."""
    return Field(
        default,
        validation_alias=AliasChoices(*aliases),
        serialization_alias=aliases[0],
        description=description,
    )


class QuickQuotePriceBreakdown(ResponseModel):
    """Price breakdown within a quick quote result."""

    pickup: Optional[float] = Field(None, alias="Pickup")
    packaging: Optional[float] = Field(None, alias="Packaging")
    transportation: Optional[float] = Field(None, alias="Transportation")
    insurance: Optional[float] = Field(None, alias="Insurance")
    delivery: Optional[float] = Field(None, alias="Delivery")
    miscellaneous: Optional[float] = Field(None, alias="Miscellaneous")


class QuickQuoteResult(ResponseModel):
    """Inner result from POST /autoprice/quickquote."""

    quote_certified: Optional[bool] = Field(None, alias="QuoteCertified")
    total_amount: Optional[float] = Field(None, alias="TotalAmount")
    warnings: Optional[List[str]] = Field(None, alias="Warnings")
    price_breakdown: Optional[QuickQuotePriceBreakdown] = Field(None, alias="PriceBreakdown")
    request_errors: Optional[List[str]] = Field(None, alias="RequestErrors")


class QuickQuoteResponse(ResponseModel):
    """Response from POST /autoprice/quickquote.

    Live API wraps the result under ``SubmitQuickQuoteRequestPOSTResult``.
    """

    result: Optional[QuickQuoteResult] = Field(
        None, alias="SubmitQuickQuoteRequestPOSTResult", description="Quote result"
    )


class QuoteRequestResponse(ResponseModel):
    """Response from POST /autoprice/v2/quoterequest."""

    quote_id: Optional[str] = Field(None, alias="quoteId", description="Quote request ID")
    status: Optional[str] = Field(None, description="Request status")
    results: Optional[List[dict]] = Field(None, description="Quote results")


class QuoteRequestJobInfo(RequestModel):
    """Job metadata for AutoPrice quote requests."""

    company_code: Optional[str] = _api_field(
        None, "CompanyCode", "companyCode", description="Company code for the quote"
    )
    owner_code: Optional[str] = _api_field(None, "OwnerCode", "ownerCode", description="Owner code")
    job_sell_price: Optional[str] = _api_field(
        None, "JobSellPrice", "jobSellPrice", description="Existing job sell price"
    )
    customer_comments: Optional[str] = _api_field(
        None, "CustomerComments", "customerComments", description="Customer-facing job comments"
    )
    job_type: Optional[str] = _api_field(None, "JobType", "jobType", description="Quote job type")
    ship_out_date: Optional[str] = _api_field(
        None, "ShipOutDate", "shipOutDate", description="Requested ship-out date"
    )
    residence_delivery: Optional[bool] = _api_field(
        None, "ResidenceDelivery", "residenceDelivery", description="Whether delivery is residential"
    )
    pack_agent: Optional[str] = _api_field(None, "PackAgent", "packAgent", description="Packing agent code")
    other_ref_no: Optional[str] = _api_field(
        None, "OtherRefNo", "otherRefNo", description="External reference number"
    )
    is_expedited: Optional[bool] = _api_field(
        None, "IsExpedited", "isExpedited", description="Whether the job is expedited"
    )
    use_only_owner_tariffs: Optional[bool] = _api_field(
        None, "UseOnlyOwnerTariffs", "useOnlyOwnerTariffs", description="Limit pricing to owner tariffs"
    )
    settings_key: Optional[str] = _api_field(
        None, "SettingsKey", "settingsKey", description="AutoPrice settings key"
    )
    do_not_tip: Optional[bool] = _api_field(None, "DoNotTip", "doNotTip", description="Do-not-tip flag")


class QuoteRequestReferrerInfo(RequestModel):
    """Referrer metadata for AutoPrice quote requests."""

    referrer_page: Optional[str] = _api_field(
        None, "ReferrerPage", "referrerPage", description="Referring page"
    )
    entry_url: Optional[str] = _api_field(None, "EntryUrl", "entryUrl", description="Entry URL")
    submission_page: Optional[str] = _api_field(
        None, "SubmissionPage", "submissionPage", description="Submission page"
    )
    how_heard: Optional[str] = _api_field(None, "HowHeard", "howHeard", description="How the customer heard")


class QuoteRequestContactInfo(RequestModel):
    """Contact/address section for AutoPrice quote requests."""

    company: Optional[str] = _api_field(None, "Company", "company", description="Company name")
    company_display_id: Optional[str] = _api_field(
        None, "CompanyDisplayId", "companyDisplayId", description="Company display identifier"
    )
    full_name: Optional[str] = _api_field(None, "FullName", "fullName", description="Contact full name")
    contact_display_id: Optional[str] = _api_field(
        None, "ContactDisplayId", "contactDisplayId", description="Contact display identifier"
    )
    phone: Optional[str] = _api_field(None, "Phone", "phone", description="Contact phone number")
    email: Optional[str] = _api_field(None, "Email", "email", description="Contact email address")
    address1: Optional[str] = _api_field(None, "Address1", "address1", description="Primary address line")
    address2: Optional[str] = _api_field(None, "Address2", "address2", description="Secondary address line")
    property_type_param: Optional[str] = _api_field(
        None, "PropertyTypeParam", "propertyTypeParam", description="Property type text parameter"
    )
    property_type: Optional[int] = _api_field(
        None, "PropertyType", "propertyType", description="Property type enum value"
    )
    city: Optional[str] = _api_field(None, "City", "city", description="City")
    state: Optional[str] = _api_field(None, "State", "state", description="State or province")
    zip_code: Optional[str] = _api_field(None, "ZipCode", "zipCode", description="Postal code")
    country_code: Optional[str] = _api_field(None, "CountryCode", "countryCode", description="Country code")
    contact_details: Optional[dict] = _api_field(
        None, "ContactDetails", "contactDetails", description="Expanded contact details"
    )


class QuoteRequestLaborInfo(RequestModel):
    """Labor options for legacy AutoPrice service requests."""

    type: Optional[str] = _api_field(None, "Type", "type", description="Labor type")
    hours: Optional[str] = _api_field(None, "Hours", "hours", description="Labor hours")
    parsed_hours: Optional[float] = _api_field(
        None, "ParsedHours", "parsedHours", description="Parsed labor hours"
    )
    parsed_type: Optional[int] = _api_field(
        None, "ParsedType", "parsedType", description="Parsed labor type enum value"
    )


class QuoteRequestServiceInfo(RequestModel):
    """Pickup or delivery service options for AutoPrice quote requests."""

    agent_code: Optional[str] = _api_field(None, "AgentCode", "agentCode", description="Agent code")
    date: Optional[str] = _api_field(None, "Date", "date", description="Requested service date")
    fee_override_amount: Optional[str] = _api_field(
        None, "FeeOverrideAmount", "feeOverrideAmount", description="Service fee override amount"
    )
    accessorials: Optional[List[str]] = _api_field(
        None, "Accessorials", "accessorials", description="Requested accessorial service codes"
    )
    labor: Optional[QuoteRequestLaborInfo] = _api_field(None, "Labor", "labor", description="Labor settings")
    done_by: Optional[str] = _api_field(None, "DoneBy", "doneBy", description="Service provider code")


class QuoteRequestContainerInfo(RequestModel):
    """Extra package/container details for AutoPrice quote requests."""

    code: Optional[str] = _api_field(None, "Code", "code", description="Container code")
    description: Optional[str] = _api_field(None, "Description", "description", description="Container description")
    length: Optional[float] = _api_field(None, "Length", "length", description="Container length")
    width: Optional[float] = _api_field(None, "Width", "width", description="Container width")
    height: Optional[float] = _api_field(None, "Height", "height", description="Container height")
    weight: Optional[float] = _api_field(None, "Weight", "weight", description="Container weight")
    cost: Optional[float] = _api_field(None, "Cost", "cost", description="Container cost")
    sell: Optional[float] = _api_field(None, "Sell", "sell", description="Container sell price")


class QuoteRequestPackServiceInfo(RequestModel):
    """Packaging service options for AutoPrice quote requests."""

    extra_containers: Optional[List[QuoteRequestContainerInfo]] = _api_field(
        None, "ExtraContainers", "extraContainers", description="Additional containers to include"
    )


class QuoteRequestLimitCarrierToSetting(RequestModel):
    """Carrier limiting settings for AutoPrice quote requests."""

    carrier_codes: Optional[List[str]] = _api_field(
        None, "CarrierCodes", "carrierCodes", description="Carrier codes to include or exclude"
    )
    carrier_apis: Optional[List[int]] = _api_field(
        None, "CarrierAPIs", "carrierAPIs", description="Carrier API enum values"
    )
    is_empty: Optional[bool] = _api_field(None, "IsEmpty", "isEmpty", description="Whether the setting is empty")
    is_excluded: Optional[bool] = _api_field(
        None, "IsExcluded", "isExcluded", description="Whether the carriers are excluded"
    )
    used_for: Optional[str] = _api_field(None, "UsedFor", "usedFor", description="Setting usage scope")


class QuoteRequestCarrierServiceInfo(RequestModel):
    """Carrier service options for AutoPrice quote requests."""

    accessorials: Optional[List[str]] = _api_field(
        None, "Accessorials", "accessorials", description="Carrier accessorial service codes"
    )
    limit_carriers_to: Optional[List[QuoteRequestLimitCarrierToSetting]] = _api_field(
        None, "LimitCarriersTo", "limitCarriersTo", description="Carrier inclusion or exclusion rules"
    )


class QuoteRequestItem(RequestModel):
    """Item line for AutoPrice quote requests."""

    length: Optional[str | float] = _api_field(
        None, "L", "l", "lengthParam", description="Item length parameter"
    )
    width: Optional[str | float] = _api_field(None, "W", "w", "widthParam", description="Item width parameter")
    height: Optional[str | float] = _api_field(
        None, "H", "h", "heightParam", description="Item height parameter"
    )
    weight: Optional[str | float] = _api_field(
        None, "Wgt", "wgt", "weightParam", description="Item weight parameter"
    )
    value: Optional[str | float] = _api_field(
        None, "Value", "value", "valueParam", description="Item declared value"
    )
    labor_hours: Optional[str | float] = _api_field(
        None, "LaborHrs", "laborHrs", "laborHrsParam", description="Item labor hours"
    )
    cpack: Optional[str] = _api_field(None, "Cpack", "cpack", description="Container/package code")
    description: Optional[str] = _api_field(None, "Description", "description", description="Item description")
    item_id: Optional[str] = _api_field(None, "ItemID", "itemID", description="Item identifier")
    noted_conditions: Optional[str] = _api_field(
        None, "NotedConditions", "notedConditions", description="Noted item conditions"
    )
    item_notes: Optional[str] = _api_field(None, "ItemNotes", "itemNotes", description="Item notes")
    customer_item_id: Optional[str] = _api_field(
        None, "CustomerItemId", "customerItemId", description="Customer item identifier"
    )
    force_crate: Optional[bool] = _api_field(
        None, "ForceCrate", "forceCrate", description="Whether to force crating"
    )
    qty: Optional[str] = _api_field(None, "Qty", "qtyParam", description="Item quantity parameter")
    quantity: Optional[int] = _api_field(None, "Quantity", "quantity", description="Parsed item quantity")
    do_not_tip: Optional[bool] = _api_field(None, "DoNotTip", "doNotTip", description="Item do-not-tip flag")
    commodity_id: Optional[str] = _api_field(None, "CommodityId", "commodityId", description="Commodity identifier")


class QuoteRequestModel(RequestModel):
    """Body for POST /autoprice/quickquote and /autoprice/v2/quoterequest."""

    access_key: Optional[str] = _api_field(None, "AccessKey", "accessKey", description="ABC API access key")
    job_info: Optional[QuoteRequestJobInfo] = _api_field(
        None, "JobInfo", "jobInfo", description="Job/shipment details"
    )
    referrer_info: Optional[QuoteRequestReferrerInfo] = _api_field(
        None, "ReferrerInfo", "referrerInfo", description="Referrer details"
    )
    customer: Optional[QuoteRequestContactInfo] = _api_field(
        None, "Customer", "customer", description="Customer contact details"
    )
    pickup: Optional[QuoteRequestContactInfo] = _api_field(
        None, "Pickup", "pickup", description="Pickup contact and address"
    )
    delivery: Optional[QuoteRequestContactInfo] = _api_field(
        None, "Delivery", "delivery", description="Delivery contact and address"
    )
    pickup_service: Optional[QuoteRequestServiceInfo] = _api_field(
        None, "PickupService", "pickupService", description="Pickup service details"
    )
    delivery_service: Optional[QuoteRequestServiceInfo] = _api_field(
        None, "DeliveryService", "deliveryService", description="Delivery service details"
    )
    carrier_services: Optional[List[str]] = _api_field(
        None, "CarrierServices", "carrierServices", description="Legacy carrier service codes"
    )
    pack_service: Optional[QuoteRequestPackServiceInfo] = _api_field(
        None, "PackService", "packService", description="Packaging service details"
    )
    carrier_service: Optional[QuoteRequestCarrierServiceInfo] = _api_field(
        None, "CarrierService", "carrierService", description="Carrier service details"
    )
    items: Optional[List[QuoteRequestItem]] = _api_field(None, "Items", "items", description="Items to quote")
