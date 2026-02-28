"""Company models for the ACPortal API."""

from __future__ import annotations

from typing import List, Optional, Union

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel
from ab.api.models.common import CompanyAddress
from ab.api.models.mixins import PaginatedRequestMixin, SearchableRequestMixin


class CarrierAccountSearchParams(RequestModel):
    """Query parameters for GET /companies/search/carrier-accounts."""

    current_company_id: Optional[str] = Field(
        None, alias="currentCompanyId", description="Current company UUID"
    )
    query: Optional[str] = Field(None, description="Search query string")


class SuggestCarriersParams(RequestModel):
    """Query parameters for GET /companies/suggest-carriers."""

    tracking_number: Optional[str] = Field(None, alias="trackingNumber", description="Tracking number (min 5 chars)")


class GeoSettingsParams(RequestModel):
    """Query parameters for GET /companies/geosettings."""

    latitude: Optional[float] = Field(None, alias="Latitude", description="Latitude coordinate")
    longitude: Optional[float] = Field(None, alias="Longitude", description="Longitude coordinate")
    miles_radius: Optional[float] = Field(None, alias="milesRadius", description="Search radius in miles")


class InheritFromParams(RequestModel):
    """Query parameters for inherited packaging endpoints."""

    inherit_from: Optional[str] = Field(None, alias="inheritFrom", description="Company ID to inherit from")


class CompanySimple(ResponseModel):
    """Lightweight company record — GET /companies/{id}."""

    id: Optional[str] = Field(None, description="Company UUID")
    name: Optional[str] = Field(None, description="Company name")
    code: Optional[str] = Field(None, description="Short company code")
    company_type: Optional[str] = Field(None, alias="companyType", description="Company type")
    parent_company_id: Optional[str] = Field(None, alias="parentCompanyId", description="Parent company UUID")
    company_name: Optional[str] = Field(None, alias="companyName", description="Full company name")
    type_id: Optional[str] = Field(None, alias="typeId", description="Company type UUID")


# ---- CompanyDetails sub-models -------------------------------------------


class CompanyDetailsInfo(ResponseModel):
    """Nested details object within CompanyDetails."""

    display_id: Optional[str] = Field(None, alias="displayId", description="Company display ID")
    name: Optional[str] = Field(None, description="Company name")
    tax_id: Optional[str] = Field(None, alias="taxId", description="Tax ID")
    code: Optional[str] = Field(None, description="Company code")
    parent_id: Optional[str] = Field(None, alias="parentId", description="Parent company UUID")
    franchisee_id: Optional[str] = Field(None, alias="franchiseeId", description="Franchisee UUID")
    company_type_id: Optional[str] = Field(None, alias="companyTypeId", description="Company type UUID")
    industry_type_id: Optional[str] = Field(None, alias="industryTypeId", description="Industry type UUID")
    cell_phone: Optional[str] = Field(None, alias="cellPhone", description="Cell phone")
    phone: Optional[str] = Field(None, description="Phone")
    fax: Optional[str] = Field(None, description="Fax")
    email: Optional[str] = Field(None, description="Email")
    website: Optional[str] = Field(None, description="Website URL")
    is_active: Optional[bool] = Field(None, alias="isActive", description="Active flag")
    is_hidden: Optional[bool] = Field(None, alias="isHidden", description="Hidden flag")
    is_global: Optional[bool] = Field(None, alias="isGlobal", description="Global company flag")
    is_not_used: Optional[bool] = Field(None, alias="isNotUsed", description="Not used flag")
    is_preferred: Optional[bool] = Field(None, alias="isPreferred", description="Preferred flag")
    payer_contact_id: Optional[int] = Field(None, alias="payerContactId", description="Payer contact ID")
    payer_contact_name: Optional[str] = Field(None, alias="payerContactName", description="Payer contact name")


class FileInfo(ResponseModel):
    """File reference for logos and images."""

    file_path: Optional[str] = Field(None, alias="filePath", description="File path")
    new_file: Optional[str] = Field(None, alias="newFile", description="New file data")


class CompanyPreferences(ResponseModel):
    """Company preferences and logo settings."""

    company_header_logo: Optional[FileInfo] = Field(
        None, alias="companyHeaderLogo", description="Header logo"
    )
    thumbnail_logo: Optional[FileInfo] = Field(None, alias="thumbnailLogo", description="Thumbnail logo")
    letter_head_logo: Optional[FileInfo] = Field(None, alias="letterHeadLogo", description="Letterhead logo")
    maps_marker: Optional[FileInfo] = Field(None, alias="mapsMarker", description="Maps marker image")
    is_qb_user: Optional[bool] = Field(None, alias="isQbUser", description="QuickBooks user flag")
    skip_intacct: Optional[bool] = Field(None, alias="skipIntacct", description="Skip Intacct flag")
    pricing_to_use: Optional[str] = Field(None, alias="pricingToUse", description="Pricing UUID")
    pz_code: Optional[str] = Field(None, alias="pzCode", description="PZ code")
    insurance_type_id: Optional[str] = Field(None, alias="insuranceTypeId", description="Insurance type UUID")
    franchisee_maturity_type_id: Optional[str] = Field(
        None, alias="franchiseeMaturityTypeId", description="Franchisee maturity type"
    )
    is_company_used_as_carrier_source: Optional[bool] = Field(
        None, alias="isCompanyUsedAsCarrierSource", description="Carrier source flag"
    )
    carrier_accounts_source_company_id: Optional[str] = Field(
        None, alias="carrierAccountsSourceCompanyId", description="Carrier source company UUID"
    )
    carrier_accounts_source_company_name: Optional[str] = Field(
        None, alias="carrierAccountsSourceCompanyName", description="Carrier source company name"
    )
    account_manager_franchisee_id: Optional[str] = Field(
        None, alias="accountManagerFranchiseeId", description="Account manager franchisee UUID"
    )
    account_manager_franchisee_name: Optional[str] = Field(
        None, alias="accountManagerFranchiseeName", description="Account manager franchisee name"
    )
    auto_price_api_enable_emails: Optional[bool] = Field(
        None, alias="autoPriceAPIEnableEmails", description="AutoPrice email notifications"
    )
    auto_price_api_enable_smss: Optional[bool] = Field(
        None, alias="autoPriceAPIEnableSMSs", description="AutoPrice SMS notifications"
    )
    copy_materials: Optional[int] = Field(None, alias="copyMaterials", description="Copy materials setting")


class FedExAccount(ResponseModel):
    """FedEx carrier account settings."""

    rest_api_accounts: Optional[list] = Field(None, alias="restApiAccounts", description="REST API accounts")


class UPSAccount(ResponseModel):
    """UPS carrier account settings."""

    shipper_number: Optional[str] = Field(None, alias="shipperNumber", description="Shipper number")
    client_id: Optional[str] = Field(None, alias="clientId", description="Client ID")
    client_secret: Optional[str] = Field(None, alias="clientSecret", description="Client secret")


class RoadRunnerAccount(ResponseModel):
    """RoadRunner carrier account settings."""

    user_name: Optional[str] = Field(None, alias="userName", description="Username")
    password: Optional[str] = Field(None, description="Password")
    app_id: Optional[str] = Field(None, alias="appId", description="App ID")
    api_key: Optional[str] = Field(None, alias="apiKey", description="API key")


class MaerskAccount(ResponseModel):
    """Maersk carrier account settings."""

    location_id: Optional[int] = Field(None, alias="locationId", description="Location ID")
    tariff_header_id: Optional[int] = Field(None, alias="tariffHeaderId", description="Tariff header ID")
    user_name: Optional[str] = Field(None, alias="userName", description="Username")
    password: Optional[str] = Field(None, description="Password")
    address_id: Optional[int] = Field(None, alias="addressId", description="Address ID")
    control_station: Optional[str] = Field(None, alias="controlStation", description="Control station")


class TeamWWAccount(ResponseModel):
    """TeamWW carrier account settings."""

    api_key: Optional[str] = Field(None, alias="apiKey", description="API key")


class EstesAccount(ResponseModel):
    """Estes carrier account settings."""

    user_name: Optional[str] = Field(None, alias="userName", description="Username")
    password: Optional[str] = Field(None, description="Password")
    account: Optional[str] = Field(None, description="Account number")


class ForwardAirAccount(ResponseModel):
    """Forward Air carrier account settings."""

    user_name: Optional[str] = Field(None, alias="userName", description="Username")
    password: Optional[str] = Field(None, description="Password")
    customer_id: Optional[str] = Field(None, alias="customerId", description="Customer ID")
    bill_to: Optional[str] = Field(None, alias="billTo", description="Bill to number")
    shipper_number: Optional[str] = Field(None, alias="shipperNumber", description="Shipper number")


class BTXAccount(ResponseModel):
    """BTX carrier account settings."""

    api_key: Optional[str] = Field(None, alias="apiKey", description="API key")


class GlobalTranzAccount(ResponseModel):
    """GlobalTranz carrier account settings."""

    access_key: Optional[str] = Field(None, alias="accessKey", description="Access key")
    user_name: Optional[str] = Field(None, alias="userName", description="Username")
    password: Optional[str] = Field(None, description="Password")


class USPSAccount(ResponseModel):
    """USPS carrier account settings."""

    account_number: Optional[str] = Field(None, alias="accountNumber", description="Account number")
    customer_registration_id: Optional[str] = Field(
        None, alias="customerRegistrationId", description="Registration ID"
    )
    mailer_id: Optional[str] = Field(None, alias="mailerId", description="Mailer ID")
    mailer_id_code: Optional[str] = Field(None, alias="mailerIdCode", description="Mailer ID code")
    client_id: Optional[str] = Field(None, alias="clientId", description="Client ID")
    client_secret: Optional[str] = Field(None, alias="clientSecret", description="Client secret")


class AccountInformation(ResponseModel):
    """Company account information for all carriers."""

    lmi_user_name: Optional[str] = Field(None, alias="lmiUserName", description="LMI username")
    lmi_client_code: Optional[str] = Field(None, alias="lmiClientCode", description="LMI client code")
    use_flat_rates: Optional[bool] = Field(None, alias="useFlatRates", description="Use flat rates flag")
    fed_ex: Optional[FedExAccount] = Field(None, alias="fedEx", description="FedEx settings")
    ups: Optional[UPSAccount] = Field(None, description="UPS settings")
    road_runner: Optional[RoadRunnerAccount] = Field(None, alias="roadRunner", description="RoadRunner settings")
    maersk: Optional[MaerskAccount] = Field(None, description="Maersk settings")
    team_ww: Optional[TeamWWAccount] = Field(None, alias="teamWW", description="TeamWW settings")
    estes: Optional[EstesAccount] = Field(None, description="Estes settings")
    forward_air: Optional[ForwardAirAccount] = Field(None, alias="forwardAir", description="Forward Air settings")
    btx: Optional[BTXAccount] = Field(None, description="BTX settings")
    global_tranz: Optional[GlobalTranzAccount] = Field(None, alias="globalTranz", description="GlobalTranz settings")
    usps: Optional[USPSAccount] = Field(None, description="USPS settings")


class TransportationCharge(ResponseModel):
    """Transportation charge settings."""

    base_trip_fee: Optional[float] = Field(None, alias="baseTripFee", description="Base trip fee")
    base_trip_mile: Optional[float] = Field(None, alias="baseTripMile", description="Base trip mile rate")
    extra_fee: Optional[float] = Field(None, alias="extraFee", description="Extra fee")
    fuel_surcharge: Optional[float] = Field(None, alias="fuelSurcharge", description="Fuel surcharge rate")


class MarkupTier(ResponseModel):
    """Markup tier with wholesale/base/medium/high levels."""

    whole_sale: Optional[float] = Field(None, alias="wholeSale", description="Wholesale markup")
    base: Optional[float] = Field(None, description="Base markup")
    medium: Optional[float] = Field(None, description="Medium markup")
    high: Optional[float] = Field(None, description="High markup")


class LaborCharge(ResponseModel):
    """Labor charge cost/charge settings."""

    cost: Optional[float] = Field(None, description="Labor cost")
    charge: Optional[float] = Field(None, description="Labor charge to customer")


class AccessorialCharge(ResponseModel):
    """Accessorial charge settings."""

    stairs: Optional[float] = Field(None, description="Stairs charge")
    elevator: Optional[float] = Field(None, description="Elevator charge")
    long_carry: Optional[float] = Field(None, alias="longCarry", description="Long carry charge")
    certificate_of_insurance: Optional[float] = Field(
        None, alias="certificateOfInsurance", description="COI charge"
    )
    de_installation: Optional[float] = Field(None, alias="deInstallation", description="De-installation charge")
    disassembly: Optional[float] = Field(None, description="Disassembly charge")
    time_specific: Optional[float] = Field(None, alias="timeSpecific", description="Time-specific charge")
    saturday: Optional[float] = Field(None, description="Saturday delivery charge")


class Royalties(ResponseModel):
    """Royalty percentage settings."""

    franchisee: Optional[float] = Field(None, description="Franchisee royalty percentage")
    national: Optional[float] = Field(None, description="National royalty percentage")
    local: Optional[float] = Field(None, description="Local royalty percentage")


class PaymentSettings(ResponseModel):
    """Payment settings."""

    credit_card_surcharge: Optional[float] = Field(
        None, alias="creditCardSurcharge", description="Credit card surcharge"
    )
    stripe_connected: Optional[bool] = Field(None, alias="stripeConnected", description="Stripe connected flag")


class CompanyPricing(ResponseModel):
    """Company pricing configuration."""

    transportation_charge: Optional[TransportationCharge] = Field(
        None, alias="transportationCharge", description="Transportation charges"
    )
    transportation_markups: Optional[MarkupTier] = Field(
        None, alias="transportationMarkups", description="Transportation markups"
    )
    carrier_freight_markups: Optional[MarkupTier] = Field(
        None, alias="carrierFreightMarkups", description="Carrier freight markups"
    )
    carrier_other_markups: Optional[MarkupTier] = Field(
        None, alias="carrierOtherMarkups", description="Carrier other markups"
    )
    material_markups: Optional[MarkupTier] = Field(None, alias="materialMarkups", description="Material markups")
    labor_charge: Optional[LaborCharge] = Field(None, alias="laborCharge", description="Labor charges")
    accesorial_charge: Optional[AccessorialCharge] = Field(
        None, alias="accesorialCharge", description="Accessorial charges"
    )
    royalties: Optional[Royalties] = Field(None, description="Royalty settings")
    payment_settings: Optional[PaymentSettings] = Field(
        None, alias="paymentSettings", description="Payment settings"
    )


class InsuranceOption(ResponseModel):
    """Insurance option for a service type."""

    insurance_slab_id: Optional[str] = Field(None, alias="insuranceSlabId", description="Insurance slab UUID")
    option: Optional[int] = Field(None, description="Option number")
    sell_price: Optional[float] = Field(None, alias="sellPrice", description="Sell price")


class CompanyInsurance(ResponseModel):
    """Company insurance configuration."""

    isp: Optional[InsuranceOption] = Field(None, description="ISP insurance")
    nsp: Optional[InsuranceOption] = Field(None, description="NSP insurance")
    ltl: Optional[InsuranceOption] = Field(None, description="LTL insurance")


class TariffGroup(ResponseModel):
    """Final mile tariff group."""

    group_id: Optional[str] = Field(None, alias="groupId", description="Group UUID")
    from_value: Optional[float] = Field(None, alias="from", description="Weight range start")
    to: Optional[float] = Field(None, description="Weight range end")
    to_curb: Optional[float] = Field(None, alias="toCurb", description="To curb rate")
    into_garage: Optional[float] = Field(None, alias="intoGarage", description="Into garage rate")
    room_of_choice: Optional[float] = Field(None, alias="roomOfChoice", description="Room of choice rate")
    white_glove: Optional[float] = Field(None, alias="whiteGlove", description="White glove rate")
    delete_group: Optional[bool] = Field(None, alias="deleteGroup", description="Delete flag")


class TaxCategory(ResponseModel):
    """Tax category settings."""

    is_taxable: Optional[bool] = Field(None, alias="isTaxable", description="Whether taxable")
    tax_percent: Optional[float] = Field(None, alias="taxPercent", description="Tax percentage")


class CompanyTaxes(ResponseModel):
    """Company tax configuration."""

    delivery_service: Optional[TaxCategory] = Field(
        None, alias="deliveryService", description="Delivery service tax"
    )
    insurance: Optional[TaxCategory] = Field(None, description="Insurance tax")
    pickup_service: Optional[TaxCategory] = Field(None, alias="pickupService", description="Pickup service tax")
    services: Optional[TaxCategory] = Field(None, description="Services tax")
    transportation_service: Optional[TaxCategory] = Field(
        None, alias="transportationService", description="Transportation service tax"
    )
    packaging_material: Optional[TaxCategory] = Field(
        None, alias="packagingMaterial", description="Packaging material tax"
    )
    packaging_labor: Optional[TaxCategory] = Field(None, alias="packagingLabor", description="Packaging labor tax")


# ---- Deep nested models (016) --------------------------------------------


class OverridableField(ResponseModel):
    """Overridable field wrapper — models C# Overridable<T>."""

    default_value: Optional[str] = Field(None, alias="defaultValue", description="Default value")
    override_value: Optional[str] = Field(None, alias="overrideValue", description="Override value")
    force_empty: Optional[bool] = Field(None, alias="forceEmpty", description="Force empty flag")
    value: Optional[str] = Field(None, description="Computed value")


class CompanyInfo(ResponseModel):
    """Company info summary — nested in CompanyDetails.companyInfo."""

    company_id: Optional[str] = Field(None, alias="companyId", description="Company UUID")
    company_type_id: Optional[str] = Field(None, alias="companyTypeId", description="Company type UUID")
    company_display_id: Optional[str] = Field(None, alias="companyDisplayId", description="Display ID")
    company_name: Optional[str] = Field(None, alias="companyName", description="Company name")
    company_code: Optional[str] = Field(None, alias="companyCode", description="Company code")
    company_email: Optional[str] = Field(None, alias="companyEmail", description="Company email")
    company_phone: Optional[str] = Field(None, alias="companyPhone", description="Company phone")
    thumbnail_logo: Optional[str] = Field(None, alias="thumbnailLogo", description="Thumbnail logo")
    company_logo: Optional[str] = Field(None, alias="companyLogo", description="Company logo")
    maps_marker_image: Optional[str] = Field(None, alias="mapsMarkerImage", description="Maps marker image")
    main_address: Optional[CompanyAddress] = Field(None, alias="mainAddress", description="Main address")
    is_third_party: Optional[bool] = Field(None, alias="isThirdParty", description="Third-party flag")
    is_active: Optional[bool] = Field(None, alias="isActive", description="Active flag")
    is_hidden: Optional[bool] = Field(None, alias="isHidden", description="Hidden flag")


class AddressData(ResponseModel):
    """Flat address data — nested in CompanyDetails.addressData."""

    company: Optional[str] = Field(None, description="Company name")
    first_last_name: Optional[str] = Field(None, alias="firstLastName", description="Contact name")
    address_line1: Optional[str] = Field(None, alias="addressLine1", description="Address line 1")
    address_line2: Optional[str] = Field(None, alias="addressLine2", description="Address line 2")
    contact_bol_note: Optional[str] = Field(None, alias="contactBOLNote", description="Contact BOL note")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State")
    state_code: Optional[str] = Field(None, alias="stateCode", description="State code")
    zip_code: Optional[str] = Field(None, alias="zipCode", description="ZIP code")
    country_name: Optional[str] = Field(None, alias="countryName", description="Country name")
    property_type: Optional[str] = Field(None, alias="propertyType", description="Property type")
    full_city_line: Optional[str] = Field(None, alias="fullCityLine", description="Full city line")
    phone: Optional[str] = Field(None, description="Phone")
    cell_phone: Optional[str] = Field(None, alias="cellPhone", description="Cell phone")
    fax: Optional[str] = Field(None, description="Fax")
    email: Optional[str] = Field(None, description="Email")
    address_line2_visible: Optional[bool] = Field(
        None, alias="addressLine2Visible", description="Address line 2 visible"
    )
    company_visible: Optional[bool] = Field(None, alias="companyVisible", description="Company visible")
    country_name_visible: Optional[bool] = Field(
        None, alias="countryNameVisible", description="Country name visible"
    )
    phone_visible: Optional[bool] = Field(None, alias="phoneVisible", description="Phone visible")
    email_visible: Optional[bool] = Field(None, alias="emailVisible", description="Email visible")
    full_address_line: Optional[str] = Field(None, alias="fullAddressLine", description="Full address line")
    full_address: Optional[str] = Field(None, alias="fullAddress", description="Full address")
    country_id: Optional[str] = Field(None, alias="countryId", description="Country UUID")


class OverridableAddressData(ResponseModel):
    """Overridable address data — fields wrapped in OverridableField."""

    company: Optional[OverridableField] = Field(None, description="Company name (overridable)")
    first_last_name: Optional[OverridableField] = Field(
        None, alias="firstLastName", description="Contact name (overridable)"
    )
    address_line1: Optional[OverridableField] = Field(
        None, alias="addressLine1", description="Address line 1 (overridable)"
    )
    address_line2: Optional[OverridableField] = Field(
        None, alias="addressLine2", description="Address line 2 (overridable)"
    )
    city: Optional[OverridableField] = Field(None, description="City (overridable)")
    state: Optional[OverridableField] = Field(None, description="State (overridable)")
    zip_code: Optional[OverridableField] = Field(None, alias="zipCode", description="ZIP code (overridable)")
    phone: Optional[OverridableField] = Field(None, description="Phone (overridable)")
    email: Optional[OverridableField] = Field(None, description="Email (overridable)")
    full_address_line: Optional[str] = Field(None, alias="fullAddressLine", description="Full address line")
    full_address: Optional[OverridableField] = Field(
        None, alias="fullAddress", description="Full address (overridable)"
    )
    full_city_line: Optional[OverridableField] = Field(
        None, alias="fullCityLine", description="Full city line (overridable)"
    )


class CompanyInsurancePricing(ResponseModel):
    """Company insurance pricing — nested in CompanyDetails."""

    insurance_slab_id: Optional[str] = Field(None, alias="insuranceSlabID", description="Insurance slab UUID")
    deductible_amount: Optional[float] = Field(None, alias="deductibleAmount", description="Deductible amount")
    rate: Optional[float] = Field(None, description="Rate")
    company_id: Optional[str] = Field(None, alias="companyId", description="Company UUID")
    is_active: Optional[bool] = Field(None, alias="isActive", description="Active flag")
    transp_type_id: Optional[str] = Field(None, alias="transpTypeID", description="Transportation type UUID")
    company_name: Optional[str] = Field(None, alias="companyName", description="Company name")
    created_by: Optional[str] = Field(None, alias="createdby", description="Created by UUID")
    modified_by: Optional[str] = Field(None, alias="modifiedby", description="Modified by UUID")
    revision: Optional[int] = Field(None, description="Revision number")
    insurance_type: Optional[str] = Field(None, alias="insuranceType", description="Insurance type")
    whole_sale_markup: Optional[float] = Field(None, alias="wholeSaleMarkup", description="Wholesale markup")
    base_markup: Optional[float] = Field(None, alias="baseMarkup", description="Base markup")
    medium_markup: Optional[float] = Field(None, alias="mediumMarkup", description="Medium markup")
    high_markup: Optional[float] = Field(None, alias="highMarkup", description="High markup")


class CompanyServicePricing(ResponseModel):
    """Company service pricing — nested in CompanyDetails."""

    service_pricing_id: Optional[str] = Field(None, alias="servicePricingId", description="Service pricing UUID")
    user_id: Optional[str] = Field(None, alias="userID", description="User UUID")
    company_id: Optional[str] = Field(None, alias="companyID", description="Company UUID")
    service_category_id: Optional[str] = Field(
        None, alias="serviceCategoryID", description="Service category UUID"
    )
    category_value: Optional[float] = Field(None, alias="categoryValue", description="Category value")
    whole_sale_markup: Optional[float] = Field(None, alias="wholeSaleMarkup", description="Wholesale markup")
    base_markup: Optional[float] = Field(None, alias="baseMarkup", description="Base markup")
    medium_markup: Optional[float] = Field(None, alias="mediumMarkup", description="Medium markup")
    high_markup: Optional[float] = Field(None, alias="highMarkup", description="High markup")
    is_active: Optional[bool] = Field(None, alias="isActive", description="Active flag")
    is_taxable: Optional[bool] = Field(None, alias="isTaxable", description="Taxable flag")
    tax_percent: Optional[float] = Field(None, alias="taxPercent", description="Tax percentage")
    created_by: Optional[str] = Field(None, alias="createdBy", description="Created by UUID")
    modified_by: Optional[str] = Field(None, alias="modifiedBy", description="Modified by UUID")
    created_date: Optional[str] = Field(None, alias="createdDate", description="Created date")
    modified_date: Optional[str] = Field(None, alias="modifiedDate", description="Modified date")
    company_code: Optional[str] = Field(None, alias="companyCode", description="Company code")
    service_category_name: Optional[str] = Field(
        None, alias="serviceCategoryName", description="Service category name"
    )
    company_name: Optional[str] = Field(None, alias="companyName", description="Company name")
    company_type_id: Optional[str] = Field(None, alias="companyTypeId", description="Company type UUID")
    parent_category_id: Optional[str] = Field(None, alias="parentCategoryID", description="Parent category UUID")
    zip_code: Optional[str] = Field(None, alias="zipCode", description="ZIP code")


class CompanyTaxPricing(ResponseModel):
    """Company tax pricing — nested in CompanyDetails."""

    job_id: Optional[str] = Field(None, alias="jobID", description="Job UUID")
    service_category_id: Optional[str] = Field(
        None, alias="serviceCategoryID", description="Service category UUID"
    )
    tax_slab_id: Optional[str] = Field(None, alias="taxSlabID", description="Tax slab UUID")
    is_taxable: Optional[bool] = Field(None, alias="isTaxable", description="Taxable flag")
    tax_percent: Optional[float] = Field(None, alias="taxPercent", description="Tax percentage")
    company_id: Optional[str] = Field(None, alias="companyID", description="Company UUID")
    service_category_name: Optional[str] = Field(
        None, alias="serviceCategotyName", description="Service category name"
    )
    company_name: Optional[str] = Field(None, alias="companyName", description="Company name")
    is_active: Optional[bool] = Field(None, alias="isActive", description="Active flag")


class CompanyDetails(ResponseModel):
    """Full company details — GET /companies/{id}/fulldetails and /details.

    The ``fulldetails`` endpoint nests data under ``details`` and ``preferences``;
    the ``details`` endpoint returns a flat structure with all fields at the
    top level.  This model accepts both shapes.

    ``capabilities`` is an integer bitmask (not a dict as swagger implies).
    """

    # --- fulldetails nested fields -------------------------------------------
    id: Optional[str] = Field(None, description="Company UUID")
    details: Optional[CompanyDetailsInfo] = Field(None, description="Nested company detail fields")
    preferences: Optional[CompanyPreferences] = Field(None, description="Company preferences and logos")
    # swagger says dict; reality is an int bitmask
    capabilities: Optional[Union[int, dict]] = Field(None, description="Service capabilities (bitmask or dict)")
    settings: Optional[dict] = Field(None, description="Company settings")
    addresses: Optional[List[dict]] = Field(None, description="Associated addresses")
    contacts: Optional[List[dict]] = Field(None, description="Associated contacts")
    address: Optional[CompanyAddress] = Field(None, description="Primary company address")
    account_information: Optional[AccountInformation] = Field(
        None, alias="accountInformation", description="Carrier account information"
    )
    pricing: Optional[CompanyPricing] = Field(None, description="Pricing configuration")
    insurance: Optional[CompanyInsurance] = Field(None, description="Insurance configuration")
    final_mile_tariff: Optional[List[TariffGroup]] = Field(
        None, alias="finalMileTariff", description="Final mile tariff groups"
    )
    taxes: Optional[CompanyTaxes] = Field(None, description="Tax configuration")
    read_only_access: Optional[bool] = Field(None, alias="readOnlyAccess", description="Read-only access flag")

    # --- details flat fields (GET /companies/{companyId}/details) ------------
    user_id: Optional[str] = Field(None, alias="userId", description="User UUID")
    company_name: Optional[str] = Field(None, alias="companyName", description="Company name")
    contact_name: Optional[str] = Field(None, alias="contactName", description="Contact name")
    contact_phone: Optional[str] = Field(None, alias="contactPhone", description="Contact phone")
    company_type: Optional[str] = Field(None, alias="companyType", description="Company type")
    parcel_only: Optional[bool] = Field(None, alias="parcelOnly", description="Parcel-only flag")
    is_third_party: Optional[bool] = Field(None, alias="isThirdParty", description="Third-party flag")
    company_code: Optional[str] = Field(None, alias="companyCode", description="Company code")
    parent_company_name: Optional[str] = Field(None, alias="parentCompanyName", description="Parent company name")
    company_type_id: Optional[str] = Field(
        None, alias="companyTypeID", description="Company type UUID"
    )
    parent_company_id: Optional[str] = Field(
        None, alias="parentCompanyID", description="Parent company UUID"
    )
    company_phone: Optional[str] = Field(None, alias="companyPhone", description="Company phone")
    company_email: Optional[str] = Field(None, alias="companyEmail", description="Company email")
    company_fax: Optional[str] = Field(None, alias="companyFax", description="Company fax")
    company_web_site: Optional[str] = Field(None, alias="companyWebSite", description="Company website URL")
    industry_type: Optional[str] = Field(None, alias="industryType", description="Industry type UUID")
    industry_type_name: Optional[str] = Field(None, alias="industryTypeName", description="Industry type name")
    tax_id: Optional[str] = Field(None, alias="taxId", description="Tax ID")
    customer_cell: Optional[str] = Field(None, alias="customerCell", description="Customer cell phone")
    company_cell: Optional[str] = Field(None, alias="companyCell", description="Company cell phone")
    pz_code: Optional[str] = Field(None, alias="pzCode", description="PZ code")
    referral_code: Optional[str] = Field(None, alias="referralCode", description="Referral code")
    company_logo: Optional[str] = Field(None, alias="companyLogo", description="Company logo filename")
    letter_head_logo: Optional[str] = Field(None, alias="letterHeadLogo", description="Letterhead logo filename")
    thumbnail_logo: Optional[str] = Field(None, alias="thumbnailLogo", description="Thumbnail logo filename")
    maps_marker_image: Optional[str] = Field(None, alias="mapsMarkerImage", description="Maps marker image filename")
    color_theme: Optional[str] = Field(None, alias="colorTheme", description="Color theme name")
    franchisee_maturity_type: Optional[str] = Field(
        None, alias="franchiseeMaturityType", description="Franchisee maturity type UUID"
    )
    pricing_to_use: Optional[str] = Field(None, alias="pricingToUse", description="Pricing UUID")
    total_rows: Optional[int] = Field(None, alias="totalRows", description="Total rows count")
    company_insurance_pricing: Optional[CompanyInsurancePricing] = Field(
        None, alias="companyInsurancePricing", description="Company insurance pricing data"
    )
    company_service_pricing: Optional[CompanyServicePricing] = Field(
        None, alias="companyServicePricing", description="Company service pricing data"
    )
    company_tax_pricing: Optional[CompanyTaxPricing] = Field(
        None, alias="companyTaxPricing", description="Company tax pricing data"
    )
    whole_sale_markup: Optional[float] = Field(None, alias="wholeSaleMarkup", description="Wholesale markup")
    base_markup: Optional[float] = Field(None, alias="baseMarkup", description="Base markup")
    medium_markup: Optional[float] = Field(None, alias="mediumMarkup", description="Medium markup")
    high_markup: Optional[float] = Field(None, alias="highMarkup", description="High markup")
    miles: Optional[float] = Field(None, description="Miles")
    insurance_type: Optional[str] = Field(None, alias="insuranceType", description="Insurance type UUID")
    is_global: Optional[bool] = Field(None, alias="isGlobal", description="Global company flag")
    is_qb_user: Optional[bool] = Field(None, alias="isQbUser", description="QuickBooks user flag")
    skip_intacct: Optional[bool] = Field(None, alias="skipIntacct", description="Skip Intacct flag")
    is_access: Optional[str] = Field(None, alias="isAccess", description="Access flag")
    company_display_id: Optional[str] = Field(
        None, alias="companyDisplayID", description="Company display ID"
    )
    depth: Optional[int] = Field(None, description="Hierarchy depth")
    franchisee_name: Optional[str] = Field(None, alias="franchiseeName", description="Franchisee name")
    is_prefered: Optional[bool] = Field(None, alias="isPrefered", description="Preferred flag")
    created_user: Optional[str] = Field(None, alias="createdUser", description="Created by user")
    mapping_locations: Optional[str] = Field(None, alias="mappingLocations", description="Mapping locations")
    location_count: Optional[str] = Field(None, alias="locationCount", description="Location count")
    base_parent: Optional[str] = Field(None, alias="baseParent", description="Base parent")
    copy_material_from: Optional[str] = Field(None, alias="copyMaterialFrom", description="Copy material from")
    is_hide: Optional[bool] = Field(None, alias="isHide", description="Hidden flag")
    is_dont_use: Optional[bool] = Field(None, alias="isDontUse", description="Don't use flag")
    main_address: Optional[CompanyAddress] = Field(None, alias="mainAddress", description="Main address")
    account_manager_franchisee_id: Optional[str] = Field(
        None, alias="accountManagerFranchiseeId", description="Account manager franchisee UUID"
    )
    account_manager_franchisee_name: Optional[str] = Field(
        None, alias="accountManagerFranchiseeName", description="Account manager franchisee name"
    )
    carrier_accounts_source_company_id: Optional[str] = Field(
        None, alias="carrierAccountsSourceCompanyId", description="Carrier source company UUID"
    )
    carrier_accounts_source_company_name: Optional[str] = Field(
        None, alias="carrierAccountsSourceCompanyName", description="Carrier source company name"
    )
    auto_price_api_enable_emails: Optional[bool] = Field(
        None, alias="autoPriceAPIEnableEmails", description="AutoPrice email notifications"
    )
    auto_price_api_enable_smss: Optional[bool] = Field(
        None, alias="autoPriceAPIEnableSMSs", description="AutoPrice SMS notifications"
    )
    commercial_capabilities: Optional[int] = Field(
        None, alias="commercialCapabilities", description="Commercial capabilities bitmask"
    )
    primary_contact_id: Optional[int] = Field(
        None, alias="primaryContactId", description="Primary contact ID"
    )
    payer_contact_id: Optional[int] = Field(None, alias="payerContactId", description="Payer contact ID")
    payer_contact_name: Optional[str] = Field(None, alias="payerContactName", description="Payer contact name")
    total_jobs: Optional[int] = Field(None, alias="totalJobs", description="Total jobs count")
    total_jobs_revenue: Optional[float] = Field(
        None, alias="totalJobsRevenue", description="Total jobs revenue"
    )
    total_sales: Optional[int] = Field(None, alias="totalSales", description="Total sales count")
    total_sales_revenue: Optional[float] = Field(
        None, alias="totalSalesRevenue", description="Total sales revenue"
    )
    is_readonly: Optional[bool] = Field(None, alias="isReadonly", description="Read-only flag")
    address_data: Optional[AddressData] = Field(None, alias="addressData", description="Address data")
    overridable_address_data: Optional[OverridableAddressData] = Field(
        None, alias="overridableAddressData", description="Overridable address data"
    )
    company_info: Optional[CompanyInfo] = Field(None, alias="companyInfo", description="Company info summary")
    company_id_flat: Optional[str] = Field(
        None, alias="companyID", description="Company UUID (flat details response)"
    )
    address_id_flat: Optional[str] = Field(
        None, alias="addressID", description="Address UUID (flat details response)"
    )
    address1: Optional[str] = Field(None, description="Address line 1")
    address2: Optional[str] = Field(None, description="Address line 2")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State")
    state_code: Optional[str] = Field(None, alias="stateCode", description="State code")
    country_name: Optional[str] = Field(None, alias="countryName", description="Country name")
    country_code: Optional[str] = Field(None, alias="countryCode", description="Country code")
    country_id_flat: Optional[str] = Field(
        None, alias="countryID", description="Country UUID (flat details response)"
    )
    zip_code: Optional[str] = Field(None, alias="zipCode", description="ZIP code")
    is_active: Optional[bool] = Field(None, alias="isActive", description="Active flag")
    created_date: Optional[str] = Field(None, alias="createdDate", description="Created date")
    created_by: Optional[str] = Field(None, alias="createdBy", description="Created by UUID")
    modified_date: Optional[str] = Field(None, alias="modifiedDate", description="Modified date")
    modified_by: Optional[str] = Field(None, alias="modifiedBy", description="Modified by UUID")
    latitude: Optional[str] = Field(None, description="Latitude")
    longitude: Optional[str] = Field(None, description="Longitude")
    result: Optional[str] = Field(None, description="Result")
    address_mapping_id: Optional[str] = Field(
        None, alias="addressMappingID", description="Address mapping UUID"
    )
    contact_id_flat: Optional[str] = Field(
        None, alias="contactID", description="Contact UUID (flat details response)"
    )
    user_id_flat: Optional[str] = Field(
        None, alias="userID", description="User UUID (flat details response)"
    )
    primary_customer_name: Optional[str] = Field(
        None, alias="primaryCustomerName", description="Primary customer name"
    )
    contact_info: Optional[dict] = Field(None, alias="contactInfo", description="Contact info")


class SearchCompanyResponse(ResponseModel):
    """Single result from GET /companies/availableByCurrentUser.

    The live API returns ``companyName`` and ``name`` (both present),
    plus ``typeId`` and ``parentCompanyId``.
    """

    id: Optional[str] = Field(None, description="Company UUID")
    code: Optional[str] = Field(None, description="Company code")
    company_name: Optional[str] = Field(None, alias="companyName", description="Full company name")
    name: Optional[str] = Field(None, description="Company name")
    type_id: Optional[str] = Field(None, alias="typeId", description="Company type UUID")
    parent_company_id: Optional[str] = Field(None, alias="parentCompanyId", description="Parent company UUID")
    company_type: Optional[str] = Field(None, alias="companyType", description="Company type")


class CompanySearchRequest(PaginatedRequestMixin, SearchableRequestMixin):
    """Body for POST /companies/search/v2."""

    filters: Optional[dict] = Field(None, description="Filter criteria")


# ---- Extended company models (008) ----------------------------------------


class CompanyBrand(ResponseModel):
    """Brand record — GET /companies/brands."""

    id: Optional[str] = Field(None, description="Brand ID")
    name: Optional[str] = Field(None, description="Brand name")
    parent_id: Optional[str] = Field(None, alias="parentId", description="Parent brand ID")


class BrandTree(ResponseModel):
    """Hierarchical brand tree — GET /companies/brandstree."""

    id: Optional[str] = Field(None, description="Brand ID")
    name: Optional[str] = Field(None, description="Brand name")
    children: Optional[List[dict]] = Field(None, description="Child brands")


class GeoSettings(ResponseModel):
    """Geographic settings — GET /companies/{companyId}/geosettings."""

    company_id: Optional[str] = Field(None, alias="companyId", description="Company UUID")
    service_areas: Optional[List[dict]] = Field(None, alias="serviceAreas", description="Service area definitions")
    restrictions: Optional[List[dict]] = Field(None, description="Geographic restrictions")


class GeoSettingsSaveRequest(RequestModel):
    """Body for POST /companies/{companyId}/geosettings."""

    service_areas: Optional[List[dict]] = Field(None, alias="serviceAreas", description="Service area definitions")
    restrictions: Optional[List[dict]] = Field(None, description="Geographic restrictions")


class CarrierAccount(ResponseModel):
    """Carrier account — GET /companies/{companyId}/carrierAcounts."""

    id: Optional[str] = Field(None, description="Carrier account ID")
    carrier_name: Optional[str] = Field(None, alias="carrierName", description="Carrier name")
    account_number: Optional[str] = Field(None, alias="accountNumber", description="Account number")


class CarrierAccountSaveRequest(RequestModel):
    """Body for POST /companies/{companyId}/carrierAcounts."""

    carrier_name: Optional[str] = Field(None, alias="carrierName", description="Carrier name")
    account_number: Optional[str] = Field(None, alias="accountNumber", description="Account number")


class PackagingSettings(ResponseModel):
    """Packaging config — GET /companies/{companyId}/packagingsettings."""

    company_id: Optional[str] = Field(None, alias="companyId", description="Company UUID")
    settings: Optional[dict] = Field(None, description="Packaging settings data")


class PackagingLabor(ResponseModel):
    """Packaging labor config — GET /companies/{companyId}/packaginglabor."""

    company_id: Optional[str] = Field(None, alias="companyId", description="Company UUID")
    labor_rates: Optional[List[dict]] = Field(None, alias="laborRates", description="Labor rate entries")


class PackagingTariff(ResponseModel):
    """Inherited packaging tariff — GET /companies/{companyId}/inheritedPackagingTariffs."""

    tariff_id: Optional[str] = Field(None, alias="tariffId", description="Tariff ID")
    rates: Optional[List[dict]] = Field(None, description="Tariff rate entries")
