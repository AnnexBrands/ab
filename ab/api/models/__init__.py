"""Re-export all model classes for lazy resolution by Route."""

from ab.api.models.address import AddressIsValidResult, PropertyType
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
from ab.api.models.companies import (
    BrandTree,
    CarrierAccount,
    CarrierAccountSaveRequest,
    CompanyBrand,
    CompanyDetails,
    CompanySearchRequest,
    CompanySimple,
    GeoSettings,
    GeoSettingsSaveRequest,
    PackagingLabor,
    PackagingSettings,
    PackagingTariff,
    SearchCompanyResponse,
)
from ab.api.models.contacts import (
    ContactDetailedInfo,
    ContactEditRequest,
    ContactGraphData,
    ContactHistory,
    ContactHistoryAggregated,
    ContactMergePreview,
    ContactPrimaryDetails,
    ContactSearchRequest,
    ContactSimple,
    SearchContactEntityResult,
)
from ab.api.models.dashboard import DashboardSummary, GridViewInfo, GridViewState
from ab.api.models.documents import Document, DocumentUpdateRequest
from ab.api.models.enums import CarrierAPI, DocumentType
from ab.api.models.forms import FormsShipmentPlan
from ab.api.models.jobs import (
    CalendarItem,
    ExtendedOnHoldInfo,
    IncrementStatusRequest,
    ItemNotesRequest,
    ItemUpdateRequest,
    Job,
    JobCreateRequest,
    JobNote,
    JobNoteCreateRequest,
    JobNoteUpdateRequest,
    JobPrice,
    JobSaveRequest,
    JobSearchRequest,
    JobSearchResult,
    JobUpdatePageConfig,
    JobUpdateRequest,
    MarkSmsAsReadModel,
    OnHoldDetails,
    OnHoldNoteDetails,
    OnHoldUser,
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
    SendSMSModel,
    ShipmentPlanProvider,
    TimelineAgent,
    TimelineTask,
    TimelineTaskCreateRequest,
    TimelineTaskUpdateRequest,
    TrackingInfo,
    TrackingInfoV3,
)
from ab.api.models.lookup import (
    AccessKey,
    ContactTypeEntity,
    CountryCodeDto,
    DensityClassEntry,
    JobStatus,
    LookupItem,
    LookupValue,
    ParcelPackageType,
)
from ab.api.models.lots import (
    AddLotRequest,
    LotDataDto,
    LotDto,
    LotOverrideDto,
    UpdateLotRequest,
)
from ab.api.models.mixins import (
    ActiveModel,
    CompanyAuditModel,
    CompanyRelatedModel,
    FullAuditModel,
    IdentifiedModel,
    JobAuditModel,
    JobRelatedModel,
    TimestampedModel,
)
from ab.api.models.notes import (
    GlobalNote,
    GlobalNoteCreateRequest,
    GlobalNoteUpdateRequest,
    SuggestedUser,
)
from ab.api.models.partners import Partner, PartnerSearchRequest
from ab.api.models.payments import (
    ACHCreditTransferRequest,
    ACHSessionRequest,
    ACHSessionResponse,
    AttachBankRequest,
    BankSourceRequest,
    PayBySourceRequest,
    PaymentInfo,
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
from ab.api.models.rfq import AcceptModel, QuoteRequestDisplayInfo, QuoteRequestStatus
from ab.api.models.sellers import (
    AddSellerRequest,
    SellerDto,
    SellerExpandedDto,
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
    GlobalAccessorial,
    RateQuote,
    RatesState,
    ShipmentBookRequest,
    ShipmentExportData,
    ShipmentInfo,
    ShipmentOriginDestination,
)
from ab.api.models.users import User, UserCreateRequest, UserRole, UserUpdateRequest
from ab.api.models.views import (
    GridViewAccess,
    GridViewCreateRequest,
    GridViewDetails,
    StoredProcedureColumn,
)
from ab.api.models.web2lead import Web2LeadGETResult, Web2LeadRequest, Web2LeadResponse

__all__ = [
    # Base
    "ABConnectBaseModel", "RequestModel", "ResponseModel",
    # Mixins
    "IdentifiedModel", "TimestampedModel", "ActiveModel",
    "CompanyRelatedModel", "JobRelatedModel",
    "FullAuditModel", "CompanyAuditModel", "JobAuditModel",
    # Shared
    "ServiceBaseResponse", "ServiceWarningResponse", "PaginatedList", "ListRequest",
    # Enums
    "DocumentType", "CarrierAPI",
    # Catalog
    "CatalogWithSellersDto", "CatalogExpandedDto",
    "AddCatalogRequest", "UpdateCatalogRequest", "BulkInsertRequest",
    # Lots
    "LotDto", "LotDataDto", "LotOverrideDto", "AddLotRequest", "UpdateLotRequest",
    # Sellers
    "SellerDto", "SellerExpandedDto", "AddSellerRequest", "UpdateSellerRequest",
    # Companies
    "CompanySimple", "CompanyDetails", "SearchCompanyResponse", "CompanySearchRequest",
    "CompanyBrand", "BrandTree", "GeoSettings", "GeoSettingsSaveRequest",
    "CarrierAccount", "CarrierAccountSaveRequest",
    "PackagingSettings", "PackagingLabor", "PackagingTariff",
    # Contacts
    "ContactSimple", "ContactDetailedInfo", "ContactPrimaryDetails",
    "SearchContactEntityResult", "ContactEditRequest", "ContactSearchRequest",
    "ContactHistory", "ContactHistoryAggregated", "ContactGraphData", "ContactMergePreview",
    # Jobs
    "Job", "JobSearchResult", "JobPrice", "CalendarItem", "JobUpdatePageConfig",
    "JobCreateRequest", "JobSaveRequest", "JobSearchRequest", "JobUpdateRequest",
    "TimelineTask", "TimelineAgent",
    "TimelineTaskCreateRequest", "TimelineTaskUpdateRequest", "IncrementStatusRequest",
    "TrackingInfo", "TrackingInfoV3",
    "JobNote", "JobNoteCreateRequest", "JobNoteUpdateRequest",
    "ParcelItem", "ParcelItemWithMaterials", "PackagingContainer",
    "ParcelItemCreateRequest", "ItemNotesRequest", "ItemUpdateRequest",
    "ExtendedOnHoldInfo", "OnHoldDetails", "SaveOnHoldRequest", "SaveOnHoldResponse",
    "ResolveJobOnHoldResponse", "SaveOnHoldDatesModel", "OnHoldUser", "OnHoldNoteDetails",
    "SendDocumentEmailModel", "SendSMSModel", "MarkSmsAsReadModel",
    "PricedFreightProvider", "ShipmentPlanProvider",
    # Shipments
    "RateQuote", "ShipmentOriginDestination", "Accessorial",
    "ShipmentExportData", "RatesState", "ShipmentInfo", "GlobalAccessorial",
    "ShipmentBookRequest", "AccessorialAddRequest",
    # Documents
    "Document", "DocumentUpdateRequest",
    # Address
    "AddressIsValidResult", "PropertyType",
    # Lookup
    "ContactTypeEntity", "CountryCodeDto", "JobStatus", "LookupItem",
    "LookupValue", "AccessKey", "ParcelPackageType", "DensityClassEntry",
    # Users
    "User", "UserRole", "UserCreateRequest", "UserUpdateRequest",
    # AutoPrice
    "QuickQuoteResponse", "QuickQuoteResult", "QuickQuotePriceBreakdown",
    "QuoteRequestResponse", "QuoteRequestModel",
    # Payments
    "PaymentInfo", "PaymentSource", "ACHSessionResponse",
    "PayBySourceRequest", "ACHSessionRequest", "ACHCreditTransferRequest",
    "AttachBankRequest", "VerifyACHRequest", "BankSourceRequest",
    # Forms
    "FormsShipmentPlan",
    # Web2Lead
    "Web2LeadResponse", "Web2LeadGETResult", "Web2LeadRequest",
    # RFQ
    "QuoteRequestDisplayInfo", "QuoteRequestStatus", "AcceptModel",
    # Reports
    "InsuranceReport", "InsuranceReportRequest",
    "SalesForecastReport", "SalesForecastReportRequest",
    "SalesForecastSummary", "SalesForecastSummaryRequest",
    "Web2LeadRevenueFilter", "RevenueCustomer",
    "ReferredByReport", "ReferredByReportRequest",
    "Web2LeadReport", "Web2LeadV2RequestModel",
    # Dashboard
    "DashboardSummary", "GridViewState", "GridViewInfo",
    # Views
    "GridViewDetails", "GridViewAccess", "StoredProcedureColumn", "GridViewCreateRequest",
    # Commodities
    "Commodity", "CommodityCreateRequest", "CommodityUpdateRequest",
    "CommoditySearchRequest", "CommoditySuggestionRequest",
    "CommodityMap", "CommodityMapCreateRequest", "CommodityMapUpdateRequest",
    "CommodityMapSearchRequest",
    # Notes
    "GlobalNote", "GlobalNoteCreateRequest", "GlobalNoteUpdateRequest", "SuggestedUser",
    # Partners
    "Partner", "PartnerSearchRequest",
]
