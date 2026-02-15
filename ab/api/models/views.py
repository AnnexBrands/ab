"""Views/Grids models for the ACPortal API."""

from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from ab.api.models.base import RequestModel, ResponseModel


class GridViewDetails(ResponseModel):
    """Full view configuration — GET /views/{viewId} and GET /views/all."""

    view_id: Optional[str] = Field(None, alias="viewId", description="View ID")
    name: Optional[str] = Field(None, description="View name")
    dataset_sp: Optional[str] = Field(None, alias="datasetSp", description="Dataset stored procedure")
    columns: Optional[List[dict]] = Field(None, description="Column definitions")
    filters: Optional[List[dict]] = Field(None, description="Filter configurations")
    access: Optional[dict] = Field(None, description="Access control settings")


class GridViewAccess(ResponseModel):
    """View access control — GET /views/{viewId}/accessinfo."""

    view_id: Optional[str] = Field(None, alias="viewId", description="View ID")
    users: Optional[List[dict]] = Field(None, description="User access list")
    roles: Optional[List[dict]] = Field(None, description="Role access list")


class StoredProcedureColumn(ResponseModel):
    """Dataset stored procedure column — GET /views/datasetsps and /views/datasetsp/{spName}."""

    name: Optional[str] = Field(None, description="Column name")
    data_type: Optional[str] = Field(None, alias="dataType", description="Column data type")
    is_sortable: Optional[bool] = Field(None, alias="isSortable", description="Whether column is sortable")


class GridViewCreateRequest(RequestModel):
    """Body for POST /views."""

    name: str = Field(..., description="View name")
    dataset_sp: Optional[str] = Field(None, alias="datasetSp", description="Dataset stored procedure")
    columns: Optional[List[dict]] = Field(None, description="Column definitions")
