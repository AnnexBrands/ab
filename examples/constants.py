"""Reusable staging identifiers for examples and documentation snippets."""

# UUIDs (staging - sourced from CompanyDetails fixture)
TEST_COMPANY_UUID = "93179b52-3da9-e311-b6f8-000c298b59ee"

# Integer IDs (staging - sourced from ContactSimple fixture)
TEST_CONTACT_ID = 30760
TEST_USER_CONTACT_ID = 1271

# Display IDs (staging - used across examples and tests)
TEST_CONTACT_DID = 22
TEST_JOB_DISPLAY_ID = 2000000
TEST_JOB_DISPLAY_ID2 = 4000000

# Seller / Catalog / Lot IDs (staging - sourced from Catalog fixtures)
TEST_SELLER_ID = 2
TEST_CATALOG_ID = 1
TEST_LOT_ID = 1
CATALOG_CUSTOMER_SELLER_ID = 1103
CATALOG_CUSTOMER_CATALOG_ID = 398425
TEST_LOT_NUMBER = "1"

# Company code (staging - sourced from CompanySimple fixture)
TEST_COMPANY_CODE = "TRAINING"

TEST_ITEM_ID = "26611EB7-0B0B-403C-3685-08DE5FE859C2"
TEST_ITEM_ID_2 = "22CF95FA-1D12-41FB-3685-08DE5FE859C2"
TEST_PU_START_DATE = "2024-06-01T11:00:00Z"
TEST_PU_END_DATE = "2024-06-01T11:59:59Z"
TEST_PU_COMPLETED_DATE = "2024-06-01T12:00:00Z"
TEST_PK_START_DATE = "2024-06-02T10:00:00Z"
TEST_PK_END_DATE = "2024-06-02T10:59:59Z"
TEST_ST_START_DATE = "2024-06-03T10:00:00Z"
TEST_ST_END_DATE = "2024-06-03T10:59:59Z"
TEST_TR_SCHEDULED_DATE = "2024-06-04T10:00:00Z"
TEST_TR_PICKUP_COMPLETED_DATE = "2024-06-04T10:59:59Z"
TEST_TR_DELIVERY_COMPLETED_DATE = "2024-06-05T11:00:00Z"

TEST_LOOKUP_KEY_SUB_MGMT = "Job Management Status"

# Tracking parameters (staging - educated defaults)
TEST_HISTORY_AMOUNT = 3

# Alias: companyId in routes uses same UUID as company endpoints
TEST_COMPANY_ID = TEST_COMPANY_UUID

# Chain discovery IDs (staging - discovered from listing endpoints)
TEST_TIMELINE_TASK_ID = 429012
TEST_TIMELINE_TASK_CODE = "PK"
TEST_ON_HOLD_ID = 2945
TEST_SMS_TEMPLATE_ID = 7
TEST_RFQ_SERVICE_TYPE = "3"
TEST_RFQ_COMPANY_ID = "ec2f2bec-f256-4182-bcd7-6b915b398e52"
TEST_NOTE_ID = 6362886

TEST_USER_LEGACY_ID = "E8E9B469-3D67-44DB-8F78-D768433CD498"
TEST_USER_ID = 206

# Dashboard view ID (staging - sourced from GridViewInfo fixture).
# Discovery sequence: GET /dashboard/gridviews returns a list of GridViewInfo;
# pick `.id` of the desired view, then pass it as `view_id` to GET /dashboard.
TEST_VIEW_ID = 1
