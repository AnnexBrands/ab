"""Reusable test identifiers — single source of truth for all tests, examples, and docs.

All test/example code should import identifiers from this module rather than
defining local copies.  Values are populated from staging fixtures.
"""

# UUIDs (staging — sourced from CompanyDetails fixture)
TEST_COMPANY_UUID = "93179b52-3da9-e311-b6f8-000c298b59ee"

# Integer IDs (staging — sourced from ContactSimple fixture)
TEST_CONTACT_ID = 30760
TEST_USER_CONTACT_ID = 1271

# Display IDs (staging — used across job-related examples and tests)
TEST_JOB_DISPLAY_ID = 2000000

# Seller / Catalog IDs (staging — sourced from Catalog fixtures)
TEST_SELLER_ID = 1
TEST_CATALOG_ID = 1

# Company code (staging — sourced from CompanySimple fixture)
TEST_COMPANY_CODE = "TRAINING"
