"""Re-export all model classes for lazy resolution by Route."""

from ab.api.models.base import ABConnectBaseModel, RequestModel, ResponseModel
from ab.api.models.enums import CarrierAPI, DocumentType
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
from ab.api.models.shared import (
    ListRequest,
    PaginatedList,
    ServiceBaseResponse,
    ServiceWarningResponse,
)

# Domain models
from ab.api.models.catalog import (
    AddCatalogRequest,
    BulkInsertRequest,
    CatalogExpandedDto,
    CatalogWithSellersDto,
    UpdateCatalogRequest,
)
from ab.api.models.lots import (
    AddLotRequest,
    LotDataDto,
    LotDto,
    LotOverrideDto,
    UpdateLotRequest,
)
from ab.api.models.sellers import (
    AddSellerRequest,
    SellerDto,
    SellerExpandedDto,
    UpdateSellerRequest,
)
from ab.api.models.companies import (
    CompanyDetails,
    CompanySearchRequest,
    CompanySimple,
    SearchCompanyResponse,
)
from ab.api.models.contacts import (
    ContactDetailedInfo,
    ContactEditRequest,
    ContactPrimaryDetails,
    ContactSearchRequest,
    ContactSimple,
    SearchContactEntityResult,
)
from ab.api.models.jobs import (
    CalendarItem,
    Job,
    JobCreateRequest,
    JobPrice,
    JobSaveRequest,
    JobSearchRequest,
    JobSearchResult,
    JobUpdatePageConfig,
    JobUpdateRequest,
)
from ab.api.models.documents import Document, DocumentUpdateRequest
from ab.api.models.address import AddressIsValidResult, PropertyType
from ab.api.models.lookup import ContactTypeEntity, CountryCodeDto, JobStatus, LookupItem
from ab.api.models.users import User, UserCreateRequest, UserRole, UserUpdateRequest
from ab.api.models.autoprice import (
    QuickQuotePriceBreakdown,
    QuickQuoteResponse,
    QuickQuoteResult,
    QuoteRequestModel,
    QuoteRequestResponse,
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
    # Contacts
    "ContactSimple", "ContactDetailedInfo", "ContactPrimaryDetails",
    "SearchContactEntityResult", "ContactEditRequest", "ContactSearchRequest",
    # Jobs
    "Job", "JobSearchResult", "JobPrice", "CalendarItem", "JobUpdatePageConfig",
    "JobCreateRequest", "JobSaveRequest", "JobSearchRequest", "JobUpdateRequest",
    # Documents
    "Document", "DocumentUpdateRequest",
    # Address
    "AddressIsValidResult", "PropertyType",
    # Lookup
    "ContactTypeEntity", "CountryCodeDto", "JobStatus", "LookupItem",
    # Users
    "User", "UserRole", "UserCreateRequest", "UserUpdateRequest",
    # AutoPrice
    "QuickQuoteResponse", "QuickQuoteResult", "QuickQuotePriceBreakdown",
    "QuoteRequestResponse", "QuoteRequestModel",
    # Web2Lead
    "Web2LeadResponse", "Web2LeadGETResult", "Web2LeadRequest",
]
