# Data Model: Parameter Mapping Reference

**Feature**: 005-harden-example-params

This feature does not introduce new data entities. It corrects parameter name mappings in existing endpoint methods. This document serves as the authoritative reference for correct mappings.

## Corrected Parameter Mappings

### AddressEndpoint.validate()

| Python Param | API Query Param | Source | Required |
|-------------|-----------------|--------|----------|
| `line1` | `Line1` | Swagger + ABConnectTools | No |
| `city` | `City` | Swagger + ABConnectTools | No |
| `state` | `State` | Swagger + ABConnectTools | No |
| `zip` | `Zip` | Swagger + ABConnectTools | No |
| ~~`country`~~ | ~~removed~~ | Not in swagger or ABConnectTools | — |

**Breaking change**: Python params renamed from `street`→`line1`, `zip_code`→`zip`. `country` removed.

### AddressEndpoint.get_property_type()

| Python Param | API Query Param | Source | Required |
|-------------|-----------------|--------|----------|
| `address1` | `Address1` | Swagger + ABConnectTools | No |
| `address2` | `Address2` | Swagger + ABConnectTools | No |
| `city` | `City` | Swagger + ABConnectTools | No |
| `state` | `State` | Swagger + ABConnectTools | No |
| `zip_code` | `ZipCode` | Swagger + ABConnectTools | No |

**Breaking change**: Python param renamed from `street`→`address1`. Three new params added: `address2`, `city`, `state`.

### FormsEndpoint.get_operations()

| Python Param | API Query Param | Source |
|-------------|-----------------|--------|
| `ops_type` | `type` | Swagger + ABConnectTools |

**Non-breaking**: Python param name unchanged. Only the API-side mapping changes from `opsType`→`type`.

### ShipmentsEndpoint.request_rate_quotes()

| Python Param | Transport | Source |
|-------------|-----------|--------|
| `data` (dict) | JSON request body | Swagger (requestBody: TransportationRatesRequestModel) |

**Breaking change**: Method signature changes from `**params` (query string) to `data` (JSON body).
