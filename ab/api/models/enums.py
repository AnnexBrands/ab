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


class CarrierAPI(str, Enum):
    """Carrier API identifiers for quoting and shipping."""

    USHIP = "uship"
    ESTES = "estes"
    XPO = "xpo"
    SAIA = "saia"
    ABF = "abf"
    FEDEX = "fedex"
    UPS = "ups"


class ServiceType(int, Enum):
    """Agent service type for POST /job/{jobDisplayId}/changeAgent.

    Maps to C# ``ServiceType`` enum (ABConnectTools).
    """

    UNDEFINED = 0
    PICK = 1
    PACK = 2
    PICKANDPACK = 3
    DELIVERY = 4
