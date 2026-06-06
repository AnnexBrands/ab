"""Views API endpoints (8 routes)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ab.api.models.shared import ServiceBaseResponse
    from ab.api.models.views import GridViewAccess, GridViewCreateRequest, GridViewDetails, StoredProcedureColumn

from ab.api.base import BaseEndpoint
from ab.api.route import Route

_LIST = Route("GET", "/views/all", response_model="List[GridViewDetails]")
_GET = Route("GET", "/views/{viewId}", response_model="GridViewDetails")
_CREATE = Route("POST", "/views", request_model="GridViewCreateRequest", response_model="GridViewDetails")
_DELETE = Route("DELETE", "/views/{viewId}", response_model="ServiceBaseResponse")
_GET_ACCESS_INFO = Route("GET", "/views/{viewId}/accessinfo", response_model="GridViewAccess")
_UPDATE_ACCESS = Route("PUT", "/views/{viewId}/access", request_model="GridViewAccess")
_GET_DATASET_SPS = Route("GET", "/views/datasetsps", response_model="List[StoredProcedureColumn]")
_GET_DATASET_SP = Route("GET", "/views/datasetsp/{spName}", response_model="List[StoredProcedureColumn]")


class ViewsEndpoint(BaseEndpoint):
    """Saved view management (ACPortal API)."""

    def list(self) -> list[GridViewDetails]:
        """GET /views/all

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/views/list.html
        Response model: List[GridViewDetails]
        """
        return self._request(_LIST)

    def get(self, view_id: str) -> GridViewDetails:
        """GET /views/{viewId}

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/views/get.html
        Response model: GridViewDetails
        """
        return self._request(_GET.bind(viewId=view_id))

    def create(self, *, data: GridViewCreateRequest | dict) -> GridViewDetails:
        """POST /views.

        Args:
            data: View creation payload with name, dataset_sp, and columns.
                Accepts a :class:`GridViewCreateRequest` instance or a dict.

        Request model: :class:`GridViewCreateRequest`

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/views/create.html
        Request model: GridViewCreateRequest
        Response model: GridViewDetails
        """
        return self._request(_CREATE, json=data)

    def delete(self, view_id: str) -> ServiceBaseResponse:
        """DELETE /views/{viewId}

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/views/delete.html
        Response model: ServiceBaseResponse
        """
        return self._request(_DELETE.bind(viewId=view_id))

    def get_access_info(self, view_id: str) -> GridViewAccess:
        """GET /views/{viewId}/accessinfo

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/views/get_access_info.html
        Response model: GridViewAccess
        """
        return self._request(_GET_ACCESS_INFO.bind(viewId=view_id))

    def update_access(self, view_id: str, *, data: GridViewAccess | dict) -> None:
        """PUT /views/{viewId}/access.

        Args:
            view_id: View identifier.
            data: Access control payload with users and roles.
                Accepts a :class:`GridViewAccess` instance or a dict.

        Request model: :class:`GridViewAccess`

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/views/update_access.html
        Request model: GridViewAccess
        """
        return self._request(_UPDATE_ACCESS.bind(viewId=view_id), json=data)

    def get_dataset_sps(self) -> list[StoredProcedureColumn]:
        """GET /views/datasetsps

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/views/get_dataset_sps.html
        Response model: List[StoredProcedureColumn]
        """
        return self._request(_GET_DATASET_SPS)

    def get_dataset_sp(self, sp_name: str) -> list[StoredProcedureColumn]:
        """GET /views/datasetsp/{spName}

        Docs: https://ab-sdk.readthedocs.io/en/latest/api/views/get_dataset_sp.html
        Response model: List[StoredProcedureColumn]
        """
        return self._request(_GET_DATASET_SP.bind(spName=sp_name))
