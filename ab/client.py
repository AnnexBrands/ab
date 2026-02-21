"""ABConnectAPI — top-level orchestrator for the SDK."""

from __future__ import annotations

import logging
from typing import Any, Optional

from ab.auth.base import TokenStorage
from ab.auth.file import FileTokenStorage
from ab.auth.session import SessionTokenStorage
from ab.cache import CodeResolver
from ab.config import load_settings
from ab.http import HttpClient

logger = logging.getLogger(__name__)


class ABConnectAPI:
    """Main SDK entry point.

    Initialises configuration, authentication, and HTTP clients for all
    three API surfaces.  Endpoint groups are available as attributes::

        api = ABConnectAPI(env="staging")
        catalog = api.catalog.get(1)

    Args:
        env: ``"staging"`` or ``"production"``.
        env_file: Explicit path to an env file (overrides *env*).
        request: Django ``HttpRequest`` — if provided, tokens are stored
            in the Django session via :class:`SessionTokenStorage`.
    """

    def __init__(
        self,
        *,
        env: Optional[str] = None,
        env_file: Optional[str] = None,
        request: Any = None,
    ) -> None:
        self._settings = load_settings(env=env, env_file=env_file)

        # Token storage
        if request is not None:
            self._token_storage: TokenStorage = SessionTokenStorage(request)
        else:
            self._token_storage = FileTokenStorage(environment=self._settings.environment)

        # HTTP clients — one per API surface
        self._acportal = HttpClient(self._settings.acportal_base_url, self._settings, self._token_storage)
        self._catalog = HttpClient(self._settings.catalog_base_url, self._settings, self._token_storage)
        self._abc = HttpClient(self._settings.abc_base_url, self._settings, self._token_storage)

        # Code resolver (uses cache service for code→UUID)
        self._resolver = CodeResolver(self._acportal, self._settings.client_secret)

        # Endpoint groups — populated in T048 after all endpoints exist
        self._init_endpoints()

    def _client_for(self, surface: str) -> HttpClient:
        """Return the HttpClient for the given API surface name."""
        return {"acportal": self._acportal, "catalog": self._catalog, "abc": self._abc}[surface]

    def _init_endpoints(self) -> None:
        """Instantiate all endpoint groups as attributes."""
        from ab.api.endpoints import (
            AddressEndpoint,
            AutoPriceEndpoint,
            CatalogEndpoint,
            CommoditiesEndpoint,
            CommodityMapsEndpoint,
            CompaniesEndpoint,
            ContactsEndpoint,
            DashboardEndpoint,
            DocumentsEndpoint,
            FormsEndpoint,
            JobsEndpoint,
            LookupEndpoint,
            LotsEndpoint,
            NotesEndpoint,
            PartnersEndpoint,
            PaymentsEndpoint,
            ReportsEndpoint,
            RFQEndpoint,
            SellersEndpoint,
            ShipmentsEndpoint,
            UsersEndpoint,
            ViewsEndpoint,
            Web2LeadEndpoint,
        )

        # ACPortal endpoints
        self.companies = CompaniesEndpoint(self._acportal, self._resolver)
        self.contacts = ContactsEndpoint(self._acportal)
        self.jobs = JobsEndpoint(self._acportal, self._abc)
        self.documents = DocumentsEndpoint(self._acportal)
        self.address = AddressEndpoint(self._acportal)
        self.lookup = LookupEndpoint(self._acportal)
        self.users = UsersEndpoint(self._acportal)
        self.forms = FormsEndpoint(self._acportal)
        self.shipments = ShipmentsEndpoint(self._acportal)
        self.payments = PaymentsEndpoint(self._acportal)
        self.rfq = RFQEndpoint(self._acportal)
        self.reports = ReportsEndpoint(self._acportal)
        self.dashboard = DashboardEndpoint(self._acportal)
        self.views = ViewsEndpoint(self._acportal)
        self.commodities = CommoditiesEndpoint(self._acportal)
        self.commodity_maps = CommodityMapsEndpoint(self._acportal)
        self.notes = NotesEndpoint(self._acportal)
        self.partners = PartnersEndpoint(self._acportal)

        # Catalog endpoints
        self.catalog = CatalogEndpoint(self._catalog)
        self.lots = LotsEndpoint(self._catalog)
        self.sellers = SellersEndpoint(self._catalog)

        # ABC endpoints
        self.autoprice = AutoPriceEndpoint(self._abc)
        self.web2lead = Web2LeadEndpoint(self._abc)
