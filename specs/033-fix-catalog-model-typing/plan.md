# Implementation Plan: Fix Catalog Model Typing

**Branch**: `033-fix-catalog-model-typing` | **Date**: 2026-03-16 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/033-fix-catalog-model-typing/spec.md`

## Summary

Replace `List[dict]` and untyped `list` field annotations on catalog, seller, and lot response models with their correct nested Pydantic model types per the Catalog API swagger schema. Four new lightweight models (CatalogDto, LotCatalogInformationDto, LotCatalogDto, ImageLinkDto) must be created. Cross-file imports use `TYPE_CHECKING` guards to avoid circular imports. All existing fixtures and tests must continue to pass.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: pydantic>=2.0, requests (existing SDK deps — no new dependencies)
**Storage**: N/A — SDK, no local storage
**Testing**: pytest
**Target Platform**: Cross-platform Python library
**Project Type**: Library (SDK)
**Performance Goals**: N/A — type annotation change only, no runtime performance impact
**Constraints**: No new dependencies; backward-compatible with existing consumers
**Scale/Scope**: 4 models modified, 4 new models created, ~6 files touched

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pydantic Model Fidelity | **Advancing** | This feature directly advances Principle I by replacing `List[dict]` with proper Pydantic models |
| II. Example-Driven Fixture Capture | **Pass** | No new endpoints; existing fixtures preserved |
| III. Four-Way Harmony | **Pass** | No endpoint changes; model improvements propagate through existing harmony |
| IV. Swagger-Informed, Reality-Validated | **Pass** | Types sourced from swagger schema; existing fixtures validate reality |
| V. Endpoint Status Tracking | **Pass** | No new endpoints to track |
| VI. Documentation Completeness | **Deferred** | Sphinx docs may need model cross-ref updates — low priority |
| VII. Flywheel Evolution | **Pass** | Typing fix improves IDE discoverability per SDK quality goals |
| VIII. Phase-Based Context Recovery | **Pass** | Feature is small enough for single-phase implementation |
| IX. Endpoint Input Validation | **Pass** | No endpoint signature changes |

**Post-Phase 1 re-check**: All gates still pass. New models (CatalogDto, LotCatalogInformationDto, LotCatalogDto, ImageLinkDto) inherit ResponseModel with `extra="allow"` per Principle I. No circular imports; TYPE_CHECKING guards used for cross-file references.

## Project Structure

### Documentation (this feature)

```text
specs/033-fix-catalog-model-typing/
├── plan.md              # This file
├── research.md          # Phase 0 output (10 design decisions)
├── data-model.md        # Phase 1 output (4 new models, 4 modified models)
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
ab/api/models/
├── catalog.py           # MODIFY: add CatalogDto, update CatalogExpandedDto + CatalogWithSellersDto types
├── sellers.py           # MODIFY: update SellerExpandedDto.catalogs type
├── lots.py              # MODIFY: add LotCatalogInformationDto + LotCatalogDto + ImageLinkDto, update LotDto types
└── __init__.py          # MODIFY: export new models

tests/
├── models/
│   └── test_catalog_models.py  # MODIFY: add isinstance checks for nested types
└── fixtures/
    └── (existing fixtures preserved)
```

**Structure Decision**: Standard single-project layout. All changes confined to existing model files and their test file. No new directories needed.
