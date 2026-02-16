# Data Model: Remaining API Endpoints (009)

**Date**: 2026-02-14

## New Endpoint Files & Route Definitions

### `company_setup.py` — 26 Routes

| Route Constant | Method | Path | Response Model | Request Model |
|----------------|--------|------|----------------|---------------|
| _GET_CALENDAR | GET | /company/{companyId}/calendar/{date} | CalendarDay | — |
| _GET_CALENDAR_BASEINFO | GET | /company/{companyId}/calendar/{date}/baseinfo | CalendarBaseInfo | — |
| _GET_CALENDAR_STARTOFDAY | GET | /company/{companyId}/calendar/{date}/startofday | CalendarTimeInfo | — |
| _GET_CALENDAR_ENDOFDAY | GET | /company/{companyId}/calendar/{date}/endofday | CalendarTimeInfo | — |
| _GET_STRIPE_CONNECT_URL | GET | /company/{companyId}/accounts/stripe/connecturl | StripeConnectUrl | — |
| _POST_STRIPE_COMPLETE | POST | /company/{companyId}/accounts/stripe/completeconnection | StripeConnection | StripeCompleteRequest |
| _DELETE_STRIPE | DELETE | /company/{companyId}/accounts/stripe | — | — |
| _GET_DOC_TEMPLATES | GET | /company/{companyId}/document-templates | List[DocumentTemplate] | — |
| _POST_DOC_TEMPLATE | POST | /company/{companyId}/document-templates | DocumentTemplate | DocumentTemplateRequest |
| _PUT_DOC_TEMPLATE | PUT | /company/{companyId}/document-templates/{documentId} | DocumentTemplate | DocumentTemplateRequest |
| _DELETE_DOC_TEMPLATE | DELETE | /company/{companyId}/document-templates/{documentId} | — | — |
| _GET_GRID_SETTINGS | GET | /company/{companyId}/gridsettings | GridSettings | — |
| _POST_GRID_SETTINGS | POST | /company/{companyId}/gridsettings | GridSettings | GridSettingsRequest |
| _GET_SETUP_DATA | GET | /company/{companyId}/setupdata | CompanySetupData | — |
| _GET_CONTAINER_THICKNESS | GET | /company/{companyId}/containerthicknessinches | List[ContainerThickness] | — |
| _POST_CONTAINER_THICKNESS | POST | /company/{companyId}/containerthicknessinches | ContainerThickness | ContainerThicknessRequest |
| _DELETE_CONTAINER_THICKNESS | DELETE | /company/{companyId}/containerthicknessinches | — | — |
| _GET_MATERIALS | GET | /company/{companyId}/material | List[Material] | — |
| _POST_MATERIAL | POST | /company/{companyId}/material | Material | MaterialRequest |
| _PUT_MATERIAL | PUT | /company/{companyId}/material/{materialId} | Material | MaterialRequest |
| _DELETE_MATERIAL | DELETE | /company/{companyId}/material/{materialId} | — | — |
| _GET_TRUCKS | GET | /company/{companyId}/truck | List[Truck] | — |
| _POST_TRUCK | POST | /company/{companyId}/truck | Truck | TruckRequest |
| _PUT_TRUCK | PUT | /company/{companyId}/truck/{truckId} | Truck | TruckRequest |
| _DELETE_TRUCK | DELETE | /company/{companyId}/truck/{truckId} | — | — |
| _GET_PLANNER | GET | /company/{companyId}/planner | List[PlannerEntry] | — |

### `admin.py` — 13 Routes

| Route Constant | Method | Path | Response Model | Request Model |
|----------------|--------|------|----------------|---------------|
| _GET_ADVANCED_SETTINGS_ALL | GET | /admin/advancedsettings/all | List[AdvancedSetting] | — |
| _GET_ADVANCED_SETTING | GET | /admin/advancedsettings/{id} | AdvancedSetting | — |
| _POST_ADVANCED_SETTING | POST | /admin/advancedsettings | AdvancedSetting | AdvancedSettingRequest |
| _DELETE_ADVANCED_SETTING | DELETE | /admin/advancedsettings/{id} | — | — |
| _GET_CARRIER_ERRORS_ALL | GET | /admin/carriererrormessage/all | List[CarrierErrorMessage] | — |
| _POST_CARRIER_ERROR | POST | /admin/carriererrormessage | CarrierErrorMessage | CarrierErrorMessageRequest |
| _GET_COMPANY_HIERARCHY | GET | /admin/globalsettings/companyhierarchy | CompanyHierarchy | — |
| _GET_COMPANY_HIERARCHY_BY_ID | GET | /admin/globalsettings/companyhierarchy/company/{companyId} | CompanyHierarchy | — |
| _POST_INSURANCE_EXCEPTIONS | POST | /admin/globalsettings/getinsuranceexceptions | List[InsuranceException] | InsuranceExceptionFilter |
| _POST_APPROVE_INSURANCE | POST | /admin/globalsettings/approveinsuranceexception | — | — |
| _POST_INTACCT_SETTINGS | POST | /admin/globalsettings/intacct | IntacctSettings | IntacctSettingsRequest |
| _POST_LOG_FLUSH | POST | /admin/logbuffer/flush | — | LogFlushRequest |
| _POST_LOG_FLUSH_ALL | POST | /admin/logbuffer/flushAll | — | — |

### `account.py` — 10 Routes

| Route Constant | Method | Path | Response Model | Request Model |
|----------------|--------|------|----------------|---------------|
| _POST_REGISTER | POST | /account/register | AccountResponse | RegisterRequest |
| _POST_SEND_CONFIRMATION | POST | /account/sendConfirmation | — | SendConfirmationRequest |
| _POST_CONFIRM | POST | /account/confirm | — | ConfirmRequest |
| _POST_FORGOT | POST | /account/forgot | — | ForgotRequest |
| _GET_VERIFY_RESET_TOKEN | GET | /account/verifyresettoken | TokenVerification | — |
| _POST_RESET_PASSWORD | POST | /account/resetpassword | — | ResetPasswordRequest |
| _POST_SET_PASSWORD | POST | /account/setpassword | — | SetPasswordRequest |
| _GET_PROFILE | GET | /account/profile | UserProfile | — |
| _PUT_PAYMENT_SOURCE | PUT | /account/paymentsource/{sourceId} | PaymentSource | PaymentSourceRequest |
| _DELETE_PAYMENT_SOURCE | DELETE | /account/paymentsource/{sourceId} | — | — |

### `intacct.py` — 5 Routes

| Route Constant | Method | Path | Response Model | Request Model |
|----------------|--------|------|----------------|---------------|
| _GET_JOB_INTACCT | GET | /jobintacct/{jobDisplayId} | JobIntacctData | — |
| _POST_JOB_INTACCT | POST | /jobintacct/{jobDisplayId} | JobIntacctData | JobIntacctRequest |
| _POST_DRAFT | POST | /jobintacct/{jobDisplayId}/draft | JobIntacctData | JobIntacctDraftRequest |
| _POST_APPLY_REBATE | POST | /jobintacct/{jobDisplayId}/applyRebate | — | ApplyRebateRequest |
| _DELETE_FRANCHISEE | DELETE | /jobintacct/{jobDisplayId}/{franchiseeId} | — | — |

### `esign.py` — 2 Routes

| Route Constant | Method | Path | Response Model |
|----------------|--------|------|----------------|
| _GET_RESULT | GET | /e-sign/result | ESignResult |
| _GET_ESIGN | GET | /e-sign/{jobDisplayId}/{bookingKey} | ESignData |

### `webhooks.py` — 6 Routes

| Route Constant | Method | Path | Notes |
|----------------|--------|------|-------|
| _STRIPE_HANDLE | POST | /webhooks/stripe/handle | Server-side callback |
| _STRIPE_CONNECT | POST | /webhooks/stripe/connect/handle | Server-side callback |
| _STRIPE_CHECKOUT | POST | /webhooks/stripe/checkout.session.completed | Server-side callback |
| _TWILIO_BODY_SMS | POST | /webhooks/twilio/body-sms-inbound | Server-side callback |
| _TWILIO_FORM_SMS | POST | /webhooks/twilio/form-sms-inbound | Server-side callback |
| _TWILIO_STATUS | POST | /webhooks/twilio/smsStatusCallback | Server-side callback |

### `sms_templates.py` — 5 Routes

| Route Constant | Method | Path | Response Model | Request Model |
|----------------|--------|------|----------------|---------------|
| _GET_LIST | GET | /SmsTemplate/list | List[SmsTemplate] | — |
| _GET_TOKENS | GET | /SmsTemplate/notificationTokens | NotificationTokens | — |
| _POST_SAVE | POST | /SmsTemplate/save | SmsTemplate | SmsTemplateRequest |
| _GET_TEMPLATE | GET | /SmsTemplate/{templateId} | SmsTemplate | — |
| _DELETE_TEMPLATE | DELETE | /SmsTemplate/{templateId} | — | — |

### `notifications.py` — 1 Route

| Route Constant | Method | Path | Response Model |
|----------------|--------|------|----------------|
| _GET_NOTIFICATIONS | GET | /notifications | List[Notification] |

### `values.py` — 1 Route

| Route Constant | Method | Path | Response Model |
|----------------|--------|------|----------------|
| _GET_VALUES | GET | /Values | List[str] |

### Extended Existing Files — 27 Routes

**`jobs.py` (+12)**:
- _GET_DOC_CONFIG, _GET_FEEDBACK, _POST_FEEDBACK, _GET_ACCESS_LEVEL, _POST_TRANSFER, _POST_CHANGE_AGENT, _POST_COPY, _GET_SUB_MGMT_STATUS, _POST_BOOK, _GET_TRACKING_SHIPMENT, _GET_TRACKING_V2, _POST_LABEL_REQUEST

**`companies.py` (+7)**:
- _POST_FILTERED_CUSTOMERS, _GET_INFO_FROM_KEY, _GET_SEARCH, _POST_SIMPLE_LIST, _GET_CAPABILITIES, _POST_CAPABILITIES, _GET_FRANCHISEE_ADDRESSES

**`contacts.py` (+2)**: _POST_CUSTOMERS, _POST_SEARCH

**`address.py` (+2)**: _POST_AVOID_VALIDATION, _POST_VALIDATED

**`documents.py` (+2)**: _GET_THUMBNAIL, _PUT_HIDE

**`users.py` (+1)**: _GET_POC_USERS

**`autoprice.py` (+1)**: _QUOTE_REQUEST_V1

**`web2lead.py` (+1)**: _POST_V2

### ABC New Files — 4 Routes + 1

**`abc_test.py` (3)**: _GET_CONTACT, _GET_RECENT_ESTIMATES, _GET_RENDERED_TEMPLATE

**`abc_reports.py` (1)**: _GET_WEB_REVENUE

**ABC LogBuffer (1)**: _POST_FLUSH (in abc_reports.py or separate)

## New Pydantic Models Summary

Model details will be derived from swagger `components/schemas` during implementation. The model names above are provisional and will be refined during the DISCOVER D-phase when swagger schemas are analyzed.

**Estimated new models**: ~40-50 response models + ~20-30 request models across all groups.

All models follow established conventions:
- Response models: inherit `ResponseModel` (extra="allow"), snake_case fields with camelCase aliases
- Request models: inherit `RequestModel` (extra="forbid")
- Mixins: `IdentifiedModel`, `TimestampedModel`, `ActiveModel`, `CompanyRelatedModel` as applicable
