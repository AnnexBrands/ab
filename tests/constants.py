"""Reusable test identifiers — single source of truth for all tests, examples, and docs.

All test/example code should import identifiers from this module rather than
defining local copies.  Values are populated from staging fixtures.

Baseline gate status (026-cli-gate-sweep):
  G1=2/231, G2=2/231, G3=6/231, G4=5/231, G5=216/231, G6=21/231, All=0/231
"""

# UUIDs (staging — sourced from CompanyDetails fixture)
TEST_COMPANY_UUID = "93179b52-3da9-e311-b6f8-000c298b59ee"

# Integer IDs (staging — sourced from ContactSimple fixture)
TEST_CONTACT_ID = 30760
TEST_USER_CONTACT_ID = 1271

# Display IDs (staging — used across job-related examples and tests)
TEST_JOB_DISPLAY_ID = 2000000

# Seller / Catalog IDs (staging — sourced from Catalog fixtures)
TEST_SELLER_ID = 2
TEST_CATALOG_ID = 1

# Company code (staging — sourced from CompanySimple fixture)
TEST_COMPANY_CODE = "TRAINING"

TEST_ITEM_ID = "26611EB7-0B0B-403C-3685-08DE5FE859C2"
TEST_ITEM_ID_2 = "22CF95FA-1D12-41FB-3685-08DE5FE859C2"

TEST_LOOKUP_KEY_SUB_MGMT = "Job Management Status"

# Tracking parameters (staging — educated defaults)
TEST_HISTORY_AMOUNT = 3  # tracking v3 — recent event count

# Alias: companyId in routes uses same UUID as company endpoints
TEST_COMPANY_ID = TEST_COMPANY_UUID

# Chain discovery IDs (staging — discovered from listing endpoints)
TEST_TIMELINE_TASK_ID = 429012  # first timeline task for TEST_JOB_DISPLAY_ID
TEST_TIMELINE_TASK_CODE = "PK"  # packing task code
TEST_ON_HOLD_ID = 2945  # on-hold record for TEST_JOB_DISPLAY_ID
TEST_SMS_TEMPLATE_ID = 7  # SMS template for TEST_JOB_DISPLAY_ID
TEST_RFQ_SERVICE_TYPE = "3"  # RFQ type from list_rfqs
TEST_RFQ_COMPANY_ID = "ec2f2bec-f256-4182-bcd7-6b915b398e52"  # RFQ company from list_rfqs
TEST_NOTE_ID = 6362886  # first note for TEST_JOB_DISPLAY_ID
