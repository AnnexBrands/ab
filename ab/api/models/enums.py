"""Shared enumerations referenced across ABConnect models."""

from enum import Enum


class DocumentType(int, Enum):
    """Document type identifiers used by the Documents endpoint."""

    UNKNOWN = 0
    BOL = 1
    INVOICE = 2
    PHOTO = 3
    CLAIM = 4
    POD = 5
    OTHER = 6


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
