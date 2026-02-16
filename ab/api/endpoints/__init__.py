"""Endpoint group classes."""

from ab.api.endpoints.abc_reports import ABCReportsEndpoint
from ab.api.endpoints.abc_test import ABCTestEndpoint
from ab.api.endpoints.account import AccountEndpoint
from ab.api.endpoints.address import AddressEndpoint
from ab.api.endpoints.admin import AdminEndpoint
from ab.api.endpoints.autoprice import AutoPriceEndpoint
from ab.api.endpoints.catalog import CatalogEndpoint
from ab.api.endpoints.commodities import CommoditiesEndpoint
from ab.api.endpoints.commodity_maps import CommodityMapsEndpoint
from ab.api.endpoints.companies import CompaniesEndpoint
from ab.api.endpoints.company_setup import CompanySetupEndpoint
from ab.api.endpoints.contacts import ContactsEndpoint
from ab.api.endpoints.dashboard import DashboardEndpoint
from ab.api.endpoints.documents import DocumentsEndpoint
from ab.api.endpoints.esign import ESignEndpoint
from ab.api.endpoints.forms import FormsEndpoint
from ab.api.endpoints.intacct import IntacctEndpoint
from ab.api.endpoints.jobs import JobsEndpoint
from ab.api.endpoints.lookup import LookupEndpoint
from ab.api.endpoints.lots import LotsEndpoint
from ab.api.endpoints.notes import NotesEndpoint
from ab.api.endpoints.notifications import NotificationsEndpoint
from ab.api.endpoints.partners import PartnersEndpoint
from ab.api.endpoints.payments import PaymentsEndpoint
from ab.api.endpoints.reports import ReportsEndpoint
from ab.api.endpoints.rfq import RFQEndpoint
from ab.api.endpoints.sellers import SellersEndpoint
from ab.api.endpoints.shipments import ShipmentsEndpoint
from ab.api.endpoints.sms_templates import SmsTemplateEndpoint
from ab.api.endpoints.users import UsersEndpoint
from ab.api.endpoints.values import ValuesEndpoint
from ab.api.endpoints.views import ViewsEndpoint
from ab.api.endpoints.web2lead import Web2LeadEndpoint
from ab.api.endpoints.webhooks import WebhooksEndpoint

__all__ = [
    "ABCReportsEndpoint",
    "ABCTestEndpoint",
    "AccountEndpoint",
    "AddressEndpoint",
    "AdminEndpoint",
    "AutoPriceEndpoint",
    "CatalogEndpoint",
    "CommoditiesEndpoint",
    "CommodityMapsEndpoint",
    "CompaniesEndpoint",
    "CompanySetupEndpoint",
    "ContactsEndpoint",
    "DashboardEndpoint",
    "DocumentsEndpoint",
    "ESignEndpoint",
    "FormsEndpoint",
    "IntacctEndpoint",
    "JobsEndpoint",
    "LookupEndpoint",
    "LotsEndpoint",
    "NotesEndpoint",
    "NotificationsEndpoint",
    "PartnersEndpoint",
    "PaymentsEndpoint",
    "ReportsEndpoint",
    "RFQEndpoint",
    "SellersEndpoint",
    "ShipmentsEndpoint",
    "SmsTemplateEndpoint",
    "UsersEndpoint",
    "ValuesEndpoint",
    "ViewsEndpoint",
    "Web2LeadEndpoint",
    "WebhooksEndpoint",
]
