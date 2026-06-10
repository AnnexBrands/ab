"""Fixture validation tests for Catalog API models."""


from ab.api.models.catalog import BulkInsertRequest, CatalogDto, CatalogExpandedDto, CatalogWithSellersDto
from ab.api.models.lots import LotCatalogInformationDto, LotDataDto, LotDto, LotOverrideDto
from ab.api.models.sellers import SellerDto, SellerExpandedDto
from tests.conftest import assert_no_extra_fields, require_fixture


class TestCatalogModels:
    def test_catalog_with_sellers_dto(self):
        data = require_fixture("CatalogWithSellersDto", "GET", "/Catalog")
        model = CatalogWithSellersDto.model_validate(data)
        assert isinstance(model, CatalogWithSellersDto)
        assert_no_extra_fields(model)

    def test_catalog_expanded_dto(self):
        data = require_fixture("CatalogExpandedDto", "GET", "/Catalog/{id}")
        model = CatalogExpandedDto.model_validate(data)
        assert isinstance(model, CatalogExpandedDto)
        assert_no_extra_fields(model)
        if model.sellers:
            assert isinstance(model.sellers[0], SellerDto)
        if model.lots:
            assert isinstance(model.lots[0], LotCatalogInformationDto)

    def test_lot_dto(self):
        data = require_fixture("LotDto", "GET", "/Lot")
        model = LotDto.model_validate(data)
        assert isinstance(model, LotDto)
        assert_no_extra_fields(model)

    def test_lot_data_dto(self):
        data = require_fixture("LotDataDto", "GET", "/Lot/{id}")
        model = LotDataDto.model_validate(data)
        assert isinstance(model, LotDataDto)
        assert_no_extra_fields(model)

    def test_lot_data_dto_uses_db_dimension_field_names(self):
        model = LotDataDto(l=10, w=5, h=3, wgt=2)

        assert model.l == 10
        assert model.w == 5
        assert model.h == 3
        assert model.wgt == 2
        assert not hasattr(model, "length")
        assert not hasattr(model, "width")
        assert not hasattr(model, "height")
        assert not hasattr(model, "weight")
        assert model.model_dump(by_alias=False, exclude_none=True) == {
            "l": 10,
            "w": 5,
            "h": 3,
            "wgt": 2,
        }
        assert model.model_dump(by_alias=True, exclude_none=True) == {
            "L": 10,
            "W": 5,
            "H": 3,
            "Wgt": 2,
        }

    def test_lot_data_dto_hydrates_wire_dimension_names_to_db_field_names(self):
        model = LotDataDto.model_validate({"L": 10, "W": 5, "H": 3, "Wgt": 2})

        assert model.l == 10
        assert model.w == 5
        assert model.h == 3
        assert model.wgt == 2
        assert model.model_dump(by_alias=False, exclude_none=True) == {
            "l": 10,
            "w": 5,
            "h": 3,
            "wgt": 2,
        }

    def test_lot_data_dto_ignores_long_dimension_names(self):
        model = LotDataDto(length=10, width=5, height=3, weight=2)

        assert model.l is None
        assert model.w is None
        assert model.h is None
        assert model.wgt is None
        assert model.model_dump(by_alias=False, exclude_none=True) == {}

    def test_lot_override_dto(self):
        data = require_fixture("LotOverrideDto", "POST", "/Lot/overrides")
        model = LotOverrideDto.model_validate(data)
        assert isinstance(model, LotOverrideDto)
        assert_no_extra_fields(model)

    def test_bulk_insert_omits_override_data_when_not_explicitly_provided(self):
        data = {
            "catalogs": [
                {
                    "customerCatalogId": "CAT-001",
                    "agent": "Live",
                    "title": "Auction",
                    "startDate": "2026-05-19T00:00:00Z",
                    "endDate": "2026-05-20T00:00:00Z",
                    "lots": [
                        {
                            "customerItemId": "ITEM-001",
                            "lotNumber": "1",
                            "initialData": {
                                "Qty": 1,
                                "Description": "Initial dimensions only",
                            },
                        },
                    ],
                    "sellers": [
                        {
                            "name": "Seller",
                            "customerDisplayId": 123,
                            "isActive": True,
                        },
                    ],
                },
            ],
        }

        payload = BulkInsertRequest.check(data)

        lot_payload = payload["catalogs"][0]["lots"][0]
        assert lot_payload["initialData"] == {
            "Qty": 1,
            "description": "Initial dimensions only",
        }
        assert "overridenData" not in lot_payload

    def test_bulk_insert_sends_override_data_when_explicitly_provided(self):
        data = {
            "catalogs": [
                {
                    "startDate": "2026-05-19T00:00:00Z",
                    "endDate": "2026-05-20T00:00:00Z",
                    "lots": [
                        {
                            "customerItemId": "ITEM-001",
                            "initialData": {"Qty": 1},
                            "overridenData": [
                                {
                                    "Qty": 1,
                                    "Description": "Explicit override",
                                },
                            ],
                        },
                    ],
                },
            ],
        }

        payload = BulkInsertRequest.check(data)

        lot_payload = payload["catalogs"][0]["lots"][0]
        assert lot_payload["overridenData"] == [
            {
                "Qty": 1,
                "description": "Explicit override",
            },
        ]

    def test_seller_dto(self):
        data = require_fixture("SellerDto", "GET", "/Seller/{id}", required=True)
        model = SellerDto.model_validate(data)
        assert isinstance(model, SellerDto)
        assert_no_extra_fields(model)

    def test_seller_expanded_dto(self):
        data = require_fixture("SellerExpandedDto", "GET", "/Seller/{id}", required=True)
        # Fixture may be a paginated wrapper {items, pageNumber, ...}
        if isinstance(data, dict) and "items" in data:
            items = data["items"]
            assert len(items) > 0, "SellerExpandedDto fixture has empty items array"
            data = items[0]
        model = SellerExpandedDto.model_validate(data)
        assert isinstance(model, SellerExpandedDto)
        assert_no_extra_fields(model)
        if model.catalogs:
            assert isinstance(model.catalogs[0], CatalogDto)
