"""Company models for the ACPortal API."""

from __future__ import annotations

from typing import List, Optional, Union

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel
from ab.api.models.common import CompanyAddress


class CarrierAccountSearchParams(RequestModel):
    """Query parameters for GET /companies/search/carrier-accounts."""

    current_company_id: Optional[str] = Field(
        None, alias="currentCompanyId", description="Current company UUID"
    )
    query: Optional[str] = Field(None, description="Search query string")


class SuggestCarriersParams(RequestModel):
    """Query parameters for GET /companies/suggest-carriers."""

    tracking_number: str = Field(..., alias="trackingNumber", description="Tracking number (min 5 chars)")


class CompanySimple(ResponseModel):
    """Lightweight company record — GET /companies/{id}."""

    id: Optional[str] = Field(None, description="Company UUID")
    name: Optional[str] = Field(None, description="Company name")
    code: Optional[str] = Field(None, description="Short company code")
    company_type: Optional[str] = Field(None, alias="companyType", description="Company type")
    parent_company_id: Optional[str] = Field(None, alias="parentCompanyId", description="Parent company UUID")


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


class CompanyDetails(ResponseModel):
    """Full company details — GET /companies/{id}/fulldetails.

    The live API nests most data under ``details`` and ``preferences``;
    ``capabilities`` is an integer bitmask (not a dict as swagger implies).
    """

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


class CompanySearchRequest(RequestModel):
    """Body for POST /companies/search/v2."""

    search_text: Optional[str] = Field(None, alias="searchText", description="Search query")
    page: int = Field(1, description="Page number")
    page_size: int = Field(25, alias="pageSize", description="Results per page")
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
