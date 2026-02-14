"""Endpoint group classes."""

from ab.api.endpoints.address import AddressEndpoint
from ab.api.endpoints.autoprice import AutoPriceEndpoint
from ab.api.endpoints.catalog import CatalogEndpoint
from ab.api.endpoints.companies import CompaniesEndpoint
from ab.api.endpoints.contacts import ContactsEndpoint
from ab.api.endpoints.documents import DocumentsEndpoint
from ab.api.endpoints.jobs import JobsEndpoint
from ab.api.endpoints.lookup import LookupEndpoint
from ab.api.endpoints.lots import LotsEndpoint
from ab.api.endpoints.sellers import SellersEndpoint
from ab.api.endpoints.users import UsersEndpoint
from ab.api.endpoints.web2lead import Web2LeadEndpoint

__all__ = [
    "AddressEndpoint",
    "AutoPriceEndpoint",
    "CatalogEndpoint",
    "CompaniesEndpoint",
    "ContactsEndpoint",
    "DocumentsEndpoint",
    "JobsEndpoint",
    "LookupEndpoint",
    "LotsEndpoint",
    "SellersEndpoint",
    "UsersEndpoint",
    "Web2LeadEndpoint",
]
