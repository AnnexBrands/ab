"""Shared enumerations referenced across ABConnect models."""

from enum import Enum


class DocumentType(int, Enum):
    """Document type identifiers used by the Documents endpoint.

    Values mirror the live ``GET /lookup/documentTypes`` lookup exactly (see
    ``tests/fixtures/DocumentTypeBySource.json``), which is the authoritative
    source. ``ITEM_PHOTO`` (6) is the type used when attaching photos to job
    items via ``POST /documents`` with ``JobItems`` set. The
    ``test_document_type_enum_matches_lookup`` gate keeps this in sync.
    """

    LABEL = 1
    USAR = 2
    CREDIT_CARD_AUTH = 3
    BOL = 4
    ELECTRONIC_INVOICE = 5
    ITEM_PHOTO = 6
    OTHER = 7
    MANIFEST = 8
    COMMERCIAL_INVOICE = 9
    PRO_FORMA_INVOICE = 10
    PACKING_LIST = 11
    INTERNATIONAL_FORMS = 12
    AIR_WAYBILL = 13
    TERMS_AND_CONDITIONS = 14
    CUSTOMER_QUOTE = 15
    PICKUP_RECEIPT = 16
    UPS_CONTROL_LOG = 18
    DELETED_LABEL = 19


class CarrierAPI(int, Enum):
    """Carrier API type identifiers — int32 enum per swagger CarrierAPI schema.

    Values correspond to specific carrier integration APIs used by the
    freight quoting and shipping subsystem.
    """

    API_0 = 0
    API_1 = 1
    API_2 = 2
    API_3 = 3
    API_4 = 4
    API_6 = 6
    API_7 = 7
    API_8 = 8
    API_9 = 9
    API_10 = 10
    API_11 = 11
    API_12 = 12
    API_14 = 14
    API_20 = 20


class ServiceType(int, Enum):
    """Agent service type for POST /job/{jobDisplayId}/changeAgent.

    Maps to C# ``ServiceType`` enum (ABConnectTools).
    """

    UNDEFINED = 0
    PICK = 1
    PACK = 2
    PICKANDPACK = 3
    DELIVERY = 4
