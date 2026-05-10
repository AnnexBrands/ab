"""ABConnectAPI — top-level orchestrator for the SDK."""

from __future__ import annotations

import logging
from typing import Any, Optional

from ab.auth.base import Token, TokenStorage
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
        token_storage: Optional[TokenStorage] = None,
        allow_password_fallback: Optional[bool] = None,
    ) -> None:
        external_storage = token_storage is not None or request is not None
        self._settings = load_settings(
            env=env,
            env_file=env_file,
            require_credentials=not external_storage,
        )
        self._allow_password_fallback = (
            True if allow_password_fallback is None else allow_password_fallback
        )

        # Token storage: explicit > Django request > file
        if token_storage is not None:
            self._token_storage: TokenStorage = token_storage
        elif request is not None:
            self._token_storage = SessionTokenStorage(request)
        else:
            self._token_storage = FileTokenStorage(
                environment=self._settings.environment,
                username=self._settings.username,
                client_id=self._settings.client_id,
            )

        # HTTP clients — one per API surface
        self._acportal = HttpClient(
            self._settings.acportal_base_url,
            self._settings,
            self._token_storage,
            allow_password_fallback=self._allow_password_fallback,
        )
        self._catalog = HttpClient(
            self._settings.catalog_base_url,
            self._settings,
            self._token_storage,
            allow_password_fallback=self._allow_password_fallback,
        )
        self._abc = HttpClient(
            self._settings.abc_base_url,
            self._settings,
            self._token_storage,
            allow_password_fallback=self._allow_password_fallback,
        )

        # Code resolver (uses cache service for code→UUID)
        self._resolver = CodeResolver(self._acportal, self._settings.client_secret)

        # Endpoint groups — populated in T048 after all endpoints exist
        self._init_endpoints()

    def _client_for(self, surface: str) -> HttpClient:
        """Return the HttpClient for the given API surface name."""
        return {"acportal": self._acportal, "catalog": self._catalog, "abc": self._abc}[surface]

    def login(self, username: str, password: str) -> Token:
        """Authenticate with explicit credentials and prime token storage.

        This is the supported per-request login path for Django or custom
        session storage. The token is persisted through the storage backend
        selected at construction time.
        """
        return self._acportal._password_grant_with(username=username, password=password)

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
        self.companies: CompaniesEndpoint = CompaniesEndpoint(self._acportal, self._resolver)
        self.contacts: ContactsEndpoint = ContactsEndpoint(self._acportal)
        self.jobs: JobsEndpoint = JobsEndpoint(self._acportal, self._abc, self._resolver)
        self.documents: DocumentsEndpoint = DocumentsEndpoint(self._acportal)
        self.address: AddressEndpoint = AddressEndpoint(self._acportal)
        self.lookup: LookupEndpoint = LookupEndpoint(self._acportal)
        self.users: UsersEndpoint = UsersEndpoint(self._acportal)
        self.forms: FormsEndpoint = FormsEndpoint(self._acportal)
        self.shipments: ShipmentsEndpoint = ShipmentsEndpoint(self._acportal)
        self.payments: PaymentsEndpoint = PaymentsEndpoint(self._acportal)
        self.rfq: RFQEndpoint = RFQEndpoint(self._acportal)
        self.reports: ReportsEndpoint = ReportsEndpoint(self._acportal)
        self.dashboard: DashboardEndpoint = DashboardEndpoint(self._acportal)
        self.views: ViewsEndpoint = ViewsEndpoint(self._acportal)
        self.commodities: CommoditiesEndpoint = CommoditiesEndpoint(self._acportal)
        self.commodity_maps: CommodityMapsEndpoint = CommodityMapsEndpoint(self._acportal)
        self.notes: NotesEndpoint = NotesEndpoint(self._acportal)
        self.partners: PartnersEndpoint = PartnersEndpoint(self._acportal)

        # Catalog endpoints
        self.catalog: CatalogEndpoint = CatalogEndpoint(self._catalog)
        self.lots: LotsEndpoint = LotsEndpoint(self._catalog)
        self.sellers: SellersEndpoint = SellersEndpoint(self._catalog)

        # ABC endpoints
        self.autoprice: AutoPriceEndpoint = AutoPriceEndpoint(self._abc)
        self.web2lead: Web2LeadEndpoint = Web2LeadEndpoint(self._abc)

        # ---- Backwards Compatibility Aliases --------------------------------

        self.docs: DocumentsEndpoint = self.documents
        self.cmaps: CommodityMapsEndpoint = self.commodity_maps
