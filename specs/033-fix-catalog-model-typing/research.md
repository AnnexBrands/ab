# Research: Fix Catalog Model Typing

**Feature**: 033-fix-catalog-model-typing
**Date**: 2026-03-16

## Design Decisions

### D1: CatalogExpandedDto.lots nested type

**Decision**: Type as `Optional[List[LotCatalogInformationDto]]`
**Rationale**: Swagger schema explicitly references `#/components/schemas/LotCatalogInformationDto` for the `lots` array items in CatalogExpandedDto. LotCatalogInformationDto is a lightweight model with only `id` (int) and `lot_number` (str|null) — it is NOT the full LotDto.
**Alternatives considered**: Using full LotDto was considered but rejected — swagger is clear that catalogs embed a summary, not the full lot.

### D2: CatalogExpandedDto.sellers nested type

**Decision**: Type as `Optional[List[SellerDto]]`
**Rationale**: Swagger references `#/components/schemas/SellerDto` for the sellers array. SellerDto already exists in `ab/api/models/sellers.py` with fields: id, name, display_id. Swagger SellerDto has: id, name, customerDisplayId, isActive. The existing model is missing `customer_display_id` and `is_active` fields — these should be added to SellerDto (or verified against fixtures).
**Alternatives considered**: Creating a separate CatalogSellerDto — rejected per clarification Q1 (use existing SellerDto).

### D3: CatalogWithSellersDto.sellers nested type

**Decision**: Type as `Optional[List[SellerDto]]`
**Rationale**: Same swagger reference as CatalogExpandedDto.sellers.

### D4: CatalogWithSellersDto.lots nested type

**Decision**: Type as `Optional[List[LotCatalogInformationDto]]` (if field is kept)
**Rationale**: Swagger CatalogWithSellersDto does NOT include a `lots` field — only `sellers`. However, the existing Python model has `lots: Optional[List[dict]]`, suggesting the real API may return it. Per constitution (Tier 2: fixtures > Tier 3: swagger), keep the field but type it consistently with CatalogExpandedDto.lots. No fixture exists to confirm.

### D5: SellerExpandedDto.catalogs nested type

**Decision**: Type as `Optional[List[CatalogDto]]`
**Rationale**: Swagger references `#/components/schemas/CatalogDto` (NOT CatalogExpandedDto). CatalogDto is a simpler model: id, customerCatalogId, agent, title, startDate, endDate, isCompleted. This eliminates any circular reference risk — SellerExpandedDto references CatalogDto, not CatalogExpandedDto (which references SellerDto).
**Alternatives considered**: Using CatalogExpandedDto — rejected because swagger clearly uses CatalogDto and it would create unnecessary circular references.

### D6: LotDto.catalogs nested type

**Decision**: Type as `Optional[List[LotCatalogDto]]`
**Rationale**: Swagger references `#/components/schemas/LotCatalogDto` for the catalogs array. LotCatalogDto has: catalogId (int), lotNumber (str|null).

### D7: LotDto.image_links nested type

**Decision**: Type as `Optional[List[ImageLinkDto]]`
**Rationale**: Swagger references `#/components/schemas/ImageLinkDto`. ImageLinkDto has: id (int), link (str|null).

### D8: New models required

**Decision**: Create four new response models:
1. **LotCatalogInformationDto** — `id: int`, `lot_number: Optional[str]`
2. **LotCatalogDto** — `catalog_id: int`, `lot_number: Optional[str]`
3. **ImageLinkDto** — `id: int`, `link: Optional[str]`
4. **CatalogDto** — `id: int`, `customer_catalog_id: Optional[str]`, `agent: Optional[str]`, `title: Optional[str]`, `start_date: datetime`, `end_date: datetime`, `is_completed: bool`

**Rationale**: These DTOs are defined in swagger and referenced by in-scope models but do not yet exist in the Python codebase. All inherit from ResponseModel (extra="allow") per constitution Principle I.
**Placement**: LotCatalogInformationDto, LotCatalogDto, and ImageLinkDto in `lots.py`. CatalogDto in `catalog.py`.

### D9: No circular import risk

**Decision**: No forward references needed.
**Rationale**: The reference graph is acyclic:
- CatalogExpandedDto → SellerDto (sellers.py) + LotCatalogInformationDto (lots.py)
- CatalogWithSellersDto → SellerDto (sellers.py) + LotCatalogInformationDto (lots.py)
- SellerExpandedDto → CatalogDto (catalog.py)
- LotDto → LotCatalogDto (same file) + ImageLinkDto (same file) + LotDataDto (same file)

catalog.py imports from sellers.py and lots.py. sellers.py imports from catalog.py. This creates a circular import at module level. **Resolution**: Use `TYPE_CHECKING` imports with string annotations for cross-file references, consistent with existing endpoint patterns.

### D10: SellerDto field alignment with swagger

**Decision**: Out of scope for this feature — note only.
**Rationale**: Current SellerDto has `display_id` but swagger has `customerDisplayId` and `isActive`. The existing model may reflect reality (Tier 2 fixtures show `displayId` key). Field additions/corrections are a separate concern from typing nested lists. The existing SellerDto will be used as-is for nested typing.
