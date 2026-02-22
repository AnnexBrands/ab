"""Reusable test identifiers — single source of truth for all tests, examples, and docs.

All test/example code should import identifiers from this module rather than
defining local copies.  Values are populated from live staging fixtures.
"""

# UUIDs (live staging — sourced from CompanyDetails fixture)
LIVE_COMPANY_UUID = "93179b52-3da9-e311-b6f8-000c298b59ee"

# Integer IDs (live staging — sourced from ContactSimple fixture)
LIVE_CONTACT_ID = 30760
LIVE_USER_CONTACT_ID = 1271

# Display IDs (live staging — used across job-related examples and tests)
LIVE_JOB_DISPLAY_ID = 2000000

# Seller / Catalog IDs (live staging — sourced from Catalog fixtures)
LIVE_SELLER_ID = 1
LIVE_CATALOG_ID = 1

# Company code (live staging — sourced from CompanySimple fixture)
LIVE_COMPANY_CODE = "14004OH"
