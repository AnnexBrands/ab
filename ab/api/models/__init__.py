"""Re-export all model classes for lazy resolution by Route."""

from ab.api.models.address import (
    AddressIsValidResult,
    AddressPropertyTypeParams,
    AddressValidateParams,
    PropertyType,
)
from ab.api.models.autoprice import (
    QuickQuotePriceBreakdown,
    QuickQuoteResponse,
    QuickQuoteResult,
    QuoteRequestModel,
    QuoteRequestResponse,
)
from ab.api.models.base import ABConnectBaseModel, RequestModel, ResponseModel

# Domain models
from ab.api.models.catalog import (
    AddCatalogRequest,
    BulkInsertRequest,
    CatalogExpandedDto,
    CatalogListParams,
    CatalogWithSellersDto,
    UpdateCatalogRequest,
)
from ab.api.models.commodities import (
    Commodity,
    CommodityCreateRequest,
    CommodityMap,
    CommodityMapCreateRequest,
    CommodityMapSearchRequest,
    CommodityMapUpdateRequest,
    CommoditySearchRequest,
    CommoditySuggestionRequest,
    CommodityUpdateRequest,
)
from ab.api.models.common import CompanyAddress, Coordinates
from ab.api.models.companies import (
    AccessorialCharge,
    AccountInformation,
    AddressData,
    BrandTree,
    BTXAccount,
    CarrierAccount,
    CarrierAccountSaveRequest,
    CarrierAccountSearchParams,
    CompanyBrand,
    CompanyDetails,
    CompanyDetailsInfo,
    CompanyInfo,
    CompanyInsurance,
    CompanyInsurancePricing,
    CompanyPreferences,
    CompanyPricing,
    CompanySearchRequest,
    CompanyServicePricing,
    CompanySimple,
    CompanyTaxes,
    CompanyTaxPricing,
    EstesAccount,
    FedExAccount,
    FileInfo,
    ForwardAirAccount,
    GeoSettings,
    GeoSettingsParams,
    GeoSettingsSaveRequest,
    GlobalTranzAccount,
    InheritFromParams,
    InsuranceOption,
    LaborCharge,
    MaerskAccount,
    MarkupTier,
    OverridableAddressData,
    OverridableField,
    PackagingLabor,
    PackagingSettings,
    PackagingTariff,
    PaymentSettings,
    RoadRunnerAccount,
    Royalties,
    SearchCompanyResponse,
    SuggestCarriersParams,
    TariffGroup,
    TaxCategory,
    TeamWWAccount,
    TransportationCharge,
    UPSAccount,
    USPSAccount,
)
from ab.api.models.contacts import (
    ContactDetailedInfo,
    ContactEditParams,
    ContactEditRequest,
    ContactGraphData,
    ContactHistory,
    ContactHistoryAggregated,
    ContactHistoryParams,
    ContactMergePreview,
    ContactPrimaryDetails,
    ContactSearchRequest,
    ContactSimple,
    SearchContactEntityResult,
)
from ab.api.models.dashboard import DashboardCompanyParams, DashboardParams, DashboardSummary, GridViewInfo, GridViewState
from ab.api.models.documents import Document, DocumentListParams, DocumentUpdateRequest
from ab.api.models.enums import CarrierAPI, DocumentType
from ab.api.models.forms import (
    BillOfLadingParams,
    FormTypeParams,
    FormsShipmentPlan,
    OperationsFormParams,
    PackagingLabelsParams,
)
from ab.api.models.jobs import (
    CalendarItem,
    ExtendedOnHoldInfo,
    FreightProvidersParams,
    IncrementStatusRequest,
    ItemNotesRequest,
    ItemUpdateRequest,
    Job,
    JobCreateRequest,
    JobNote,
    JobNoteCreateRequest,
    JobNoteListParams,
    JobNoteUpdateRequest,
    JobPrice,
    JobRfqListParams,
    JobSaveRequest,
    JobSearchParams,
    JobSearchRequest,
    JobSearchResult,
    JobUpdatePageConfig,
    JobUpdateRequest,
    MarkSmsAsReadModel,
    OnHoldDetails,
    OnHoldNoteDetails,
    OnHoldUser,
    JobParcelItemMaterial,
    PackagingContainer,
    ParcelItem,
    ParcelItemCreateRequest,
    ParcelItemWithMaterials,
    PricedFreightProvider,
    ResolveJobOnHoldResponse,
    SaveOnHoldDatesModel,
    SaveOnHoldRequest,
    SaveOnHoldResponse,
    SendDocumentEmailModel,
    SortByModel,
    SendSMSModel,
    ShipmentPlanProvider,
    TimelineAgent,
    TimelineCreateParams,
    TimelineTask,
    TimelineTaskCreateRequest,
    TimelineTaskUpdateRequest,
    TrackingInfo,
    TrackingInfoV3,
    TrackingV3Params,
    TransferModel,
)
from ab.api.models.lookup import (
    AccessKey,
    ContactTypeEntity,
    CountryCodeDto,
    DensityClassEntry,
    JobStatus,
    LookupDensityClassMapParams,
    LookupDocumentTypesParams,
    LookupItem,
    LookupItemsParams,
    LookupValue,
    ParcelPackageType,
)
from ab.api.models.lots import (
    AddLotRequest,
    LotDataDto,
    LotDto,
    LotListParams,
    LotOverrideDto,
    UpdateLotRequest,
)
from ab.api.models.mixins import (
    ActiveModel,
    CompanyAuditModel,
    CompanyRelatedModel,
    DateRangeRequestMixin,
    FullAuditModel,
    IdentifiedModel,
    JobAuditModel,
    JobRelatedModel,
    PaginatedRequestMixin,
    SearchableRequestMixin,
    SortableRequestMixin,
    TimestampedModel,
)
from ab.api.models.notes import (
    GlobalNote,
    GlobalNoteCreateRequest,
    GlobalNoteUpdateRequest,
    NotesListParams,
    NotesSuggestUsersParams,
    SuggestedUser,
)
from ab.api.models.partners import Partner, PartnerListParams, PartnerSearchRequest
from ab.api.models.payments import (
    ACHCreditTransferRequest,
    ACHSessionRequest,
    ACHSessionResponse,
    AttachBankRequest,
    BankSourceRequest,
    PayBySourceRequest,
    PaymentInfo,
    PaymentParams,
    PaymentSource,
    VerifyACHRequest,
)
from ab.api.models.reports import (
    InsuranceReport,
    InsuranceReportRequest,
    ReferredByReport,
    ReferredByReportRequest,
    RevenueCustomer,
    SalesForecastReport,
    SalesForecastReportRequest,
    SalesForecastSummary,
    SalesForecastSummaryRequest,
    Web2LeadReport,
    Web2LeadRevenueFilter,
    Web2LeadV2RequestModel,
)
from ab.api.models.rfq import AcceptModel, QuoteRequestDisplayInfo, QuoteRequestStatus, RfqAcceptWinnerParams, RfqForJobParams
from ab.api.models.sellers import (
    AddSellerRequest,
    SellerDto,
    SellerExpandedDto,
    SellerListParams,
    UpdateSellerRequest,
)
from ab.api.models.shared import (
    ListRequest,
    PaginatedList,
    ServiceBaseResponse,
    ServiceWarningResponse,
)
from ab.api.models.shipments import (
    Accessorial,
    AccessorialAddRequest,
    AccessorialOption,
    GlobalAccessorial,
    RadioButtonOption,
    RateQuote,
    RateQuotesParams,
    RatesState,
    ShipmentBookRequest,
    ShipmentDocumentParams,
    ShipmentExportData,
    ShipmentInfo,
    ShipmentOriginDestination,
    ShipmentParams,
    ShipmentWeight,
)
from ab.api.models.users import User, UserCreateRequest, UserRole, UserUpdateRequest
from ab.api.models.views import (
    GridViewAccess,
    GridViewCreateRequest,
    GridViewDetails,
    StoredProcedureColumn,
)
from ab.api.models.web2lead import Web2LeadGetParams, Web2LeadGETResult, Web2LeadRequest, Web2LeadResponse

__all__ = [
    # Base
    "ABConnectBaseModel", "RequestModel", "ResponseModel",
    # Mixins
    "IdentifiedModel", "TimestampedModel", "ActiveModel",
    "CompanyRelatedModel", "JobRelatedModel",
    "FullAuditModel", "CompanyAuditModel", "JobAuditModel",
    # Request mixins
    "PaginatedRequestMixin", "SortableRequestMixin",
    "SearchableRequestMixin", "DateRangeRequestMixin",
    # Common (shared sub-models)
    "Coordinates", "CompanyAddress",
    # Shared
    "ServiceBaseResponse", "ServiceWarningResponse", "PaginatedList", "ListRequest",
    # Enums
    "DocumentType", "CarrierAPI",
    # Catalog
    "CatalogListParams",
    "CatalogWithSellersDto", "CatalogExpandedDto",
    "AddCatalogRequest", "UpdateCatalogRequest", "BulkInsertRequest",
    # Lots
    "LotListParams",
    "LotDto", "LotDataDto", "LotOverrideDto", "AddLotRequest", "UpdateLotRequest",
    # Sellers
    "SellerListParams",
    "SellerDto", "SellerExpandedDto", "AddSellerRequest", "UpdateSellerRequest",
    # Companies
    "CarrierAccountSearchParams", "SuggestCarriersParams", "GeoSettingsParams", "InheritFromParams",
    "CompanySimple", "CompanyDetails", "SearchCompanyResponse", "CompanySearchRequest",
    "CompanyDetailsInfo", "FileInfo", "CompanyPreferences",
    "FedExAccount", "UPSAccount", "RoadRunnerAccount", "MaerskAccount",
    "TeamWWAccount", "EstesAccount", "ForwardAirAccount", "BTXAccount",
    "GlobalTranzAccount", "USPSAccount", "AccountInformation",
    "TransportationCharge", "MarkupTier", "LaborCharge", "AccessorialCharge",
    "Royalties", "PaymentSettings", "CompanyPricing",
    "InsuranceOption", "CompanyInsurance", "TariffGroup",
    "TaxCategory", "CompanyTaxes",
    "OverridableField", "CompanyInfo", "AddressData", "OverridableAddressData",
    "CompanyInsurancePricing", "CompanyServicePricing", "CompanyTaxPricing",
    "CompanyBrand", "BrandTree", "GeoSettings", "GeoSettingsSaveRequest",
    "CarrierAccount", "CarrierAccountSaveRequest",
    "PackagingSettings", "PackagingLabor", "PackagingTariff",
    # Contacts
    "ContactEditParams", "ContactHistoryParams",
    "ContactSimple", "ContactDetailedInfo", "ContactPrimaryDetails",
    "SearchContactEntityResult", "ContactEditRequest", "ContactSearchRequest",
    "ContactHistory", "ContactHistoryAggregated", "ContactGraphData", "ContactMergePreview",
    # Jobs
    "JobSearchParams", "FreightProvidersParams",
    "TimelineCreateParams", "TrackingV3Params", "JobNoteListParams", "JobRfqListParams",
    "Job", "JobSearchResult", "JobPrice", "CalendarItem", "JobUpdatePageConfig",
    "JobCreateRequest", "JobSaveRequest", "JobSearchRequest", "JobUpdateRequest",
    "TimelineTask", "TimelineAgent",
    "TimelineTaskCreateRequest", "TimelineTaskUpdateRequest", "IncrementStatusRequest",
    "TrackingInfo", "TrackingInfoV3",
    "JobNote", "JobNoteCreateRequest", "JobNoteUpdateRequest",
    "ParcelItem", "ParcelItemWithMaterials", "JobParcelItemMaterial", "PackagingContainer",
    "ParcelItemCreateRequest", "ItemNotesRequest", "ItemUpdateRequest",
    "ExtendedOnHoldInfo", "OnHoldDetails", "SaveOnHoldRequest", "SaveOnHoldResponse",
    "ResolveJobOnHoldResponse", "SaveOnHoldDatesModel", "OnHoldUser", "OnHoldNoteDetails",
    "SendDocumentEmailModel", "SendSMSModel", "MarkSmsAsReadModel",
    "PricedFreightProvider", "ShipmentPlanProvider",
    # Shipments
    "ShipmentParams", "RateQuotesParams", "ShipmentDocumentParams",
    "RateQuote", "ShipmentOriginDestination", "Accessorial",
    "ShipmentExportData", "RatesState", "ShipmentInfo", "ShipmentWeight",
    "GlobalAccessorial", "AccessorialOption", "RadioButtonOption",
    "ShipmentBookRequest", "AccessorialAddRequest",
    # Documents
    "Document", "DocumentListParams", "DocumentUpdateRequest",
    # Address
    "AddressValidateParams", "AddressPropertyTypeParams", "AddressIsValidResult", "PropertyType",
    # Lookup
    "LookupItemsParams", "LookupDocumentTypesParams", "LookupDensityClassMapParams",
    "ContactTypeEntity", "CountryCodeDto", "JobStatus", "LookupItem",
    "LookupValue", "AccessKey", "ParcelPackageType", "DensityClassEntry",
    # Users
    "User", "UserRole", "UserCreateRequest", "UserUpdateRequest",
    # AutoPrice
    "QuickQuoteResponse", "QuickQuoteResult", "QuickQuotePriceBreakdown",
    "QuoteRequestResponse", "QuoteRequestModel",
    # Payments
    "PaymentParams",
    "PaymentInfo", "PaymentSource", "ACHSessionResponse",
    "PayBySourceRequest", "ACHSessionRequest", "ACHCreditTransferRequest",
    "AttachBankRequest", "VerifyACHRequest", "BankSourceRequest",
    # Forms
    "BillOfLadingParams", "OperationsFormParams", "FormTypeParams", "PackagingLabelsParams", "FormsShipmentPlan",
    # Web2Lead
    "Web2LeadGetParams", "Web2LeadResponse", "Web2LeadGETResult", "Web2LeadRequest",
    # RFQ
    "RfqForJobParams", "RfqAcceptWinnerParams",
    "QuoteRequestDisplayInfo", "QuoteRequestStatus", "AcceptModel",
    # Reports
    "InsuranceReport", "InsuranceReportRequest",
    "SalesForecastReport", "SalesForecastReportRequest",
    "SalesForecastSummary", "SalesForecastSummaryRequest",
    "Web2LeadRevenueFilter", "RevenueCustomer",
    "ReferredByReport", "ReferredByReportRequest",
    "Web2LeadReport", "Web2LeadV2RequestModel",
    # Dashboard
    "DashboardCompanyParams", "DashboardParams", "DashboardSummary", "GridViewState", "GridViewInfo",
    # Views
    "GridViewDetails", "GridViewAccess", "StoredProcedureColumn", "GridViewCreateRequest",
    # Commodities
    "Commodity", "CommodityCreateRequest", "CommodityUpdateRequest",
    "CommoditySearchRequest", "CommoditySuggestionRequest",
    "CommodityMap", "CommodityMapCreateRequest", "CommodityMapUpdateRequest",
    "CommodityMapSearchRequest",
    # Notes
    "NotesListParams", "NotesSuggestUsersParams",
    "GlobalNote", "GlobalNoteCreateRequest", "GlobalNoteUpdateRequest", "SuggestedUser",
    # Partners
    "PartnerListParams",
    "Partner", "PartnerSearchRequest",
]
