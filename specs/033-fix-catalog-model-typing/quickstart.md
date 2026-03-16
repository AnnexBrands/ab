# Quickstart: Fix Catalog Model Typing

**Feature**: 033-fix-catalog-model-typing

## What This Changes

Replaces generic `List[dict]` and untyped `list` annotations on catalog/seller/lot response models with proper nested Pydantic model types. After this change, all nested objects in catalog API responses are fully typed and validated.

## Before / After

```python
# BEFORE — no IDE support, no validation
class CatalogExpandedDto(ResponseModel):
    sellers: Optional[List[dict]] = None  # what fields does a seller have?
    lots: Optional[List[dict]] = None     # unknown structure

# AFTER — full IDE autocomplete and Pydantic validation
class CatalogExpandedDto(ResponseModel):
    sellers: Optional[List[SellerDto]] = None      # .name, .id, .display_id
    lots: Optional[List[LotCatalogInformationDto]] = None  # .id, .lot_number
```

## New Models

| Model | File | Fields | Used By |
|-------|------|--------|---------|
| CatalogDto | catalog.py | id, customer_catalog_id, agent, title, start_date, end_date, is_completed | SellerExpandedDto.catalogs |
| LotCatalogInformationDto | lots.py | id, lot_number | CatalogExpandedDto.lots, CatalogWithSellersDto.lots |
| LotCatalogDto | lots.py | catalog_id, lot_number | LotDto.catalogs |
| ImageLinkDto | lots.py | id, link | LotDto.image_links |

## How to Verify

```bash
# Run all tests
cd /usr/src/pkgs/AB && python -m pytest tests/ -v

# Check specific catalog model tests
python -m pytest tests/models/test_catalog_models.py -v
```

## Key Design Decisions

- **D5**: SellerExpandedDto.catalogs → CatalogDto (not CatalogExpandedDto) — avoids circular refs
- **D9**: Cross-file imports use TYPE_CHECKING guards — no circular imports at runtime
- **D10**: SellerDto field alignment with swagger is out of scope — only nested type annotations change
