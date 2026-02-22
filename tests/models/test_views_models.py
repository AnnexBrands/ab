"""Fixture validation tests for Views models."""

from ab.api.models.views import GridViewAccess, GridViewDetails, StoredProcedureColumn
from tests.conftest import assert_no_extra_fields, require_fixture


class TestViewsModels:
    def test_grid_view_details(self):
        data = require_fixture("GridViewDetails", "GET", "/views/all")
        model = GridViewDetails.model_validate(data)
        assert isinstance(model, GridViewDetails)
        assert_no_extra_fields(model)

    def test_grid_view_access(self):
        data = require_fixture("GridViewAccess", "GET", "/views/{id}/accessinfo")
        model = GridViewAccess.model_validate(data)
        assert isinstance(model, GridViewAccess)
        assert_no_extra_fields(model)

    def test_stored_procedure_column(self):
        data = require_fixture("StoredProcedureColumn", "GET", "/views/datasetsps")
        model = StoredProcedureColumn.model_validate(data)
        assert isinstance(model, StoredProcedureColumn)
        assert_no_extra_fields(model)
