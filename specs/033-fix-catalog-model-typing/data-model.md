# Data Model: Fix Catalog Model Typing

**Feature**: 033-fix-catalog-model-typing
**Date**: 2026-03-16

## New Models (to be created)

### CatalogDto (catalog.py)
Base catalog summary used as nested type in SellerExpandedDto.

| Field | Type | Nullable | Alias |
|-------|------|----------|-------|
| id | int | No | — |
| customer_catalog_id | str | Yes | customerCatalogId |
| agent | str | Yes | — |
| title | str | Yes | — |
| start_date | datetime | No | startDate |
| end_date | datetime | No | endDate |
| is_completed | bool | No | isCompleted |

Inherits: `ResponseModel`

### LotCatalogInformationDto (lots.py)
Lightweight lot summary used as nested type in CatalogExpandedDto/CatalogWithSellersDto.

| Field | Type | Nullable | Alias |
|-------|------|----------|-------|
| id | int | No | — |
| lot_number | str | Yes | lotNumber |

Inherits: `ResponseModel`

### LotCatalogDto (lots.py)
Lot-catalog association used as nested type in LotDto.catalogs.

| Field | Type | Nullable | Alias |
|-------|------|----------|-------|
| catalog_id | int | No | catalogId |
| lot_number | str | Yes | lotNumber |

Inherits: `ResponseModel`

### ImageLinkDto (lots.py)
Image reference used as nested type in LotDto.image_links.

| Field | Type | Nullable | Alias |
|-------|------|----------|-------|
| id | int | No | — |
| link | str | Yes | — |

Inherits: `ResponseModel`

## Modified Models (field type changes only)

### CatalogExpandedDto (catalog.py)

| Field | Current Type | New Type |
|-------|-------------|----------|
| sellers | `Optional[List[dict]]` | `Optional[List[SellerDto]]` |
| lots | `Optional[List[dict]]` | `Optional[List[LotCatalogInformationDto]]` |

### CatalogWithSellersDto (catalog.py)

| Field | Current Type | New Type |
|-------|-------------|----------|
| sellers | `Optional[List[dict]]` | `Optional[List[SellerDto]]` |
| lots | `Optional[List[dict]]` | `Optional[List[LotCatalogInformationDto]]` |

### SellerExpandedDto (sellers.py)

| Field | Current Type | New Type |
|-------|-------------|----------|
| catalogs | `Optional[List[dict]]` | `Optional[List[CatalogDto]]` |

### LotDto (lots.py)

| Field | Current Type | New Type |
|-------|-------------|----------|
| catalogs | `Optional[list]` | `Optional[List[LotCatalogDto]]` |
| image_links | `Optional[list]` | `Optional[List[ImageLinkDto]]` |

## Import Dependencies

```
catalog.py imports:
  - SellerDto from sellers.py (TYPE_CHECKING)
  - LotCatalogInformationDto from lots.py (TYPE_CHECKING)

sellers.py imports:
  - CatalogDto from catalog.py (TYPE_CHECKING)

lots.py imports:
  - (no cross-file imports — all new lot models in same file)
```

Note: Cross-file imports use `TYPE_CHECKING` guard with string annotations to avoid circular imports at runtime.

## Reference Graph (acyclic)

```
CatalogExpandedDto ──→ SellerDto (sellers.py)
                   ──→ LotCatalogInformationDto (lots.py)

CatalogWithSellersDto ──→ SellerDto (sellers.py)
                      ──→ LotCatalogInformationDto (lots.py)

SellerExpandedDto ──→ CatalogDto (catalog.py)

LotDto ──→ LotCatalogDto (lots.py, same file)
       ──→ ImageLinkDto (lots.py, same file)
       ──→ LotDataDto (lots.py, same file, already typed)
```
