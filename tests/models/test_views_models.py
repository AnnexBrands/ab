"""Fixture validation tests for Views models."""

from ab.api.models.views import GridViewAccess, GridViewDetails, StoredProcedureColumn
from tests.conftest import require_fixture


class TestViewsModels:
    def test_grid_view_details(self):
        data = require_fixture("GridViewDetails", "GET", "/views/all")
        GridViewDetails.model_validate(data)

    def test_grid_view_access(self):
        data = require_fixture("GridViewAccess", "GET", "/views/{id}/accessinfo")
        GridViewAccess.model_validate(data)

    def test_stored_procedure_column(self):
        data = require_fixture("StoredProcedureColumn", "GET", "/views/datasetsps")
        StoredProcedureColumn.model_validate(data)
