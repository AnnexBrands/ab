"""Lookup API endpoints (16 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ab.api.models.lookup import (
        AccessKey,
        AccessKeySetup,
        CommonInsuranceSlab,
        ContactTypeEntity,
        CountryCodeDto,
        DensityClassEntry,
        DocumentTypeBySource,
        JobStatus,
        LookupItem,
        LookupValue,
        ParcelPackageType,
        PPCCampaign,
    )

from ab.api.base import BaseEndpoint
from ab.api.models.enums import MasterConstantKey
from ab.api.route import Route

_CONTACT_TYPES = Route("GET", "/lookup/contactTypes", response_model="List[ContactTypeEntity]")
_COUNTRIES = Route("GET", "/lookup/countries", response_model="List[CountryCodeDto]")
_JOB_STATUSES = Route("GET", "/lookup/jobStatuses", response_model="List[JobStatus]")
_ITEMS = Route("GET", "/lookup/items", params_model="LookupItemsParams", response_model="List[LookupItem]")

# Extended lookup routes (008)
_GET_BY_KEY = Route("GET", "/lookup/{masterConstantKey}", response_model="List[LookupValue]")
_GET_BY_KEY_AND_ID = Route("GET", "/lookup/{masterConstantKey}/{valueId}", response_model="LookupValue")
_ACCESS_KEYS = Route("GET", "/lookup/accessKeys", response_model="List[AccessKey]")
_ACCESS_KEY = Route("GET", "/lookup/accessKey/{accessKey}", response_model="AccessKeySetup")
_PPC_CAMPAIGNS = Route("GET", "/lookup/PPCCampaigns", response_model="List[PPCCampaign]")
_PARCEL_PACKAGE_TYPES = Route("GET", "/lookup/parcelPackageTypes", response_model="List[ParcelPackageType]")
_DOCUMENT_TYPES = Route(
    "GET", "/lookup/documentTypes",
    params_model="LookupDocumentTypesParams", response_model="List[DocumentTypeBySource]",
)
_COMMON_INSURANCE = Route("GET", "/lookup/comonInsurance", response_model="List[CommonInsuranceSlab]")
_DENSITY_CLASS_MAP = Route(
    "GET", "/lookup/densityClassMap",
    params_model="LookupDensityClassMapParams",
    response_model="List[DensityClassEntry]",
)
_REFER_CATEGORIES = Route("GET", "/lookup/referCategory", response_model="List[LookupValue]")
_REFER_CATEGORY_HIERARCHY = Route("GET", "/lookup/referCategoryHeirachy", response_model="List[LookupValue]")
_RESET_CACHE = Route("GET", "/lookup/resetMasterConstantCache")


class LookupEndpoint(BaseEndpoint):
    """Reference/lookup data (ACPortal API)."""

    def get_contact_types(self) -> list[ContactTypeEntity]:
        """GET /lookup/contactTypes

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/lookup/get_contact_types.html
        Response model: List[ContactTypeEntity]
        """
        return self._request(_CONTACT_TYPES)

    def get_countries(self) -> list[CountryCodeDto]:
        """GET /lookup/countries

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/lookup/get_countries.html
        Response model: List[CountryCodeDto]
        """
        return self._request(_COUNTRIES)

    def get_job_statuses(self) -> list[JobStatus]:
        """GET /lookup/jobStatuses

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/lookup/get_job_statuses.html
        Response model: List[JobStatus]
        """
        return self._request(_JOB_STATUSES)

    def get_items(
        self,
        *,
        job_display_id: Optional[int] = None,
        job_item_id: Optional[str] = None,
    ) -> list[LookupItem]:
        """GET /lookup/items

        Args:
            job_display_id: Optional job display ID filter.
            job_item_id: Optional job item ID filter.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/lookup/get_items.html
        Query params: LookupItemsParams
        Response model: List[LookupItem]
        """
        return self._request(
            _ITEMS,
            params=dict(job_display_id=job_display_id, job_item_id=job_item_id),
        )

    # ---- Generic lookup (008) ---------------------------------------------

    def get_by_key(self, key: str | MasterConstantKey) -> list[LookupValue]:
        """GET /lookup/{masterConstantKey}

        Args:
            key: A master-constant GROUP key (e.g. ``"OnHoldReason"``,
                ``"Job Management Status"``), NOT one of its values — see
                :class:`~ab.api.models.enums.MasterConstantKey` for every
                known key. The API returns ``[]`` (not 404) for an unknown
                key, so a misspelt key looks like an empty group.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/lookup/get_by_key.html
        Response model: List[LookupValue]
        """
        key = key.value if isinstance(key, MasterConstantKey) else key
        return self._request(_GET_BY_KEY.bind(masterConstantKey=key))

    def get_by_key_and_id(self, key: str | MasterConstantKey, value_id: str) -> LookupValue:
        """GET /lookup/{masterConstantKey}/{valueId}

        Args:
            key: A master-constant GROUP key — see
                :class:`~ab.api.models.enums.MasterConstantKey`.
            value_id: The ``LookupValue.id`` (MasterConstantValueID) to fetch.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/lookup/get_by_key_and_id.html
        Response model: LookupValue
        """
        key = key.value if isinstance(key, MasterConstantKey) else key
        return self._request(_GET_BY_KEY_AND_ID.bind(masterConstantKey=key, valueId=value_id))

    # ---- Named convenience methods (008) ----------------------------------

    def get_access_keys(self) -> list[AccessKey]:
        """GET /lookup/accessKeys

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/lookup/get_access_keys.html
        Response model: List[AccessKey]
        """
        return self._request(_ACCESS_KEYS)

    def get_access_key(self, access_key: str) -> AccessKeySetup:
        """GET /lookup/accessKey/{accessKey}

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/lookup/get_access_key.html
        Response model: AccessKeySetup
        """
        return self._request(_ACCESS_KEY.bind(accessKey=access_key))

    def get_ppc_campaigns(self) -> list[PPCCampaign]:
        """GET /lookup/PPCCampaigns

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/lookup/get_ppc_campaigns.html
        Response model: List[PPCCampaign]
        """
        return self._request(_PPC_CAMPAIGNS)

    def get_parcel_package_types(self) -> list[ParcelPackageType]:
        """GET /lookup/parcelPackageTypes

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/lookup/get_parcel_package_types.html
        Response model: List[ParcelPackageType]
        """
        return self._request(_PARCEL_PACKAGE_TYPES)

    def get_document_types(self, *, document_source: Optional[str] = None) -> list[DocumentTypeBySource]:
        """GET /lookup/documentTypes

        Args:
            document_source: Optional document source filter.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/lookup/get_document_types.html
        Query params: LookupDocumentTypesParams
        Response model: List[DocumentTypeBySource]
        """
        return self._request(
            _DOCUMENT_TYPES,
            params=dict(document_source=document_source),
        )

    def get_common_insurance(self) -> list[CommonInsuranceSlab]:
        """GET /lookup/comonInsurance

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/lookup/get_common_insurance.html
        Response model: List[CommonInsuranceSlab]
        """
        return self._request(_COMMON_INSURANCE)

    def get_density_class_map(self, *, carrier_api: Optional[str] = None) -> list[DensityClassEntry]:
        """GET /lookup/densityClassMap

        Args:
            carrier_api: Optional carrier API filter.

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/lookup/get_density_class_map.html
        Query params: LookupDensityClassMapParams
        Response model: List[DensityClassEntry]
        """
        return self._request(
            _DENSITY_CLASS_MAP,
            params=dict(carrier_api=carrier_api),
        )

    def get_refer_categories(self) -> list[LookupValue]:
        """GET /lookup/referCategory

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/lookup/get_refer_categories.html
        Response model: List[LookupValue]
        """
        return self._request(_REFER_CATEGORIES)

    def get_refer_category_hierarchy(self) -> list[LookupValue]:
        """GET /lookup/referCategoryHeirachy

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/lookup/get_refer_category_hierarchy.html
        Response model: List[LookupValue]
        """
        return self._request(_REFER_CATEGORY_HIERARCHY)

    def reset_cache(self) -> None:
        """GET /lookup/resetMasterConstantCache

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/lookup/reset_cache.html
        """
        return self._request(_RESET_CACHE)
