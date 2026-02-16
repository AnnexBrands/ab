# Endpoint Contracts: 009-remaining-endpoints

## ACPortal Endpoints (95)

### Company Setup (26) — `/api/company/{companyId}/`
```
GET  /api/company/{companyId}/calendar/{date}
GET  /api/company/{companyId}/calendar/{date}/baseinfo
GET  /api/company/{companyId}/calendar/{date}/startofday
GET  /api/company/{companyId}/calendar/{date}/endofday
GET  /api/company/{companyId}/accounts/stripe/connecturl?returnUri={uri}
POST /api/company/{companyId}/accounts/stripe/completeconnection  [json body]
DEL  /api/company/{companyId}/accounts/stripe
GET  /api/company/{companyId}/document-templates
POST /api/company/{companyId}/document-templates  [json body]
PUT  /api/company/{companyId}/document-templates/{documentId}  [json body]
DEL  /api/company/{companyId}/document-templates/{documentId}
GET  /api/company/{companyId}/gridsettings
POST /api/company/{companyId}/gridsettings  [json body]
GET  /api/company/{companyId}/setupdata
GET  /api/company/{companyId}/containerthicknessinches
POST /api/company/{companyId}/containerthicknessinches  [json body]
DEL  /api/company/{companyId}/containerthicknessinches?containerId={id}
GET  /api/company/{companyId}/material
POST /api/company/{companyId}/material  [json body]
PUT  /api/company/{companyId}/material/{materialId}  [json body]
DEL  /api/company/{companyId}/material/{materialId}
GET  /api/company/{companyId}/truck?onlyOwnTrucks={bool}
POST /api/company/{companyId}/truck  [json body]
PUT  /api/company/{companyId}/truck/{truckId}  [json body]
DEL  /api/company/{companyId}/truck/{truckId}
GET  /api/company/{companyId}/planner
```

### Admin (13) — `/api/admin/`
```
GET  /api/admin/advancedsettings/all
GET  /api/admin/advancedsettings/{id}
POST /api/admin/advancedsettings  [json body]
DEL  /api/admin/advancedsettings/{id}
GET  /api/admin/carriererrormessage/all
POST /api/admin/carriererrormessage  [json body]
GET  /api/admin/globalsettings/companyhierarchy
GET  /api/admin/globalsettings/companyhierarchy/company/{companyId}
POST /api/admin/globalsettings/getinsuranceexceptions  [json body]
POST /api/admin/globalsettings/approveinsuranceexception?JobId={id}
POST /api/admin/globalsettings/intacct  [json body]
POST /api/admin/logbuffer/flush  [json body optional]
POST /api/admin/logbuffer/flushAll
```

### Account (10) — `/api/account/`
```
POST /api/account/register  [json body]
POST /api/account/sendConfirmation  [json body]
POST /api/account/confirm  [json body]
POST /api/account/forgot  [json body]
GET  /api/account/verifyresettoken?username={u}&token={t}
POST /api/account/resetpassword  [json body]
POST /api/account/setpassword  [json body]
GET  /api/account/profile
PUT  /api/account/paymentsource/{sourceId}  [json body]
DEL  /api/account/paymentsource/{sourceId}
```

### Job Extensions (12) — `/api/job/`
```
GET  /api/job/documentConfig
GET  /api/job/feedback/{jobDisplayId}
POST /api/job/feedback/{jobDisplayId}  [json body]
GET  /api/job/jobAccessLevel
POST /api/job/transfer/{jobDisplayId}  [json body]
POST /api/job/{jobDisplayId}/changeAgent  [json body]
POST /api/job/{jobDisplayId}/copy/{documentId}
GET  /api/job/{jobDisplayId}/submanagementstatus
POST /api/job/{jobDisplayId}/book  [json body]
GET  /api/job/{jobDisplayId}/tracking/shipment/{proNumber}
GET  /api/v2/job/{jobDisplayId}/tracking/{historyAmount}
POST /api/email/{jobDisplayId}/labelrequest  [json body]
```

### Intacct (5) — `/api/jobintacct/`
```
GET  /api/jobintacct/{jobDisplayId}
POST /api/jobintacct/{jobDisplayId}  [json body]
POST /api/jobintacct/{jobDisplayId}/draft  [json body]
POST /api/jobintacct/{jobDisplayId}/applyRebate  [json body]
DEL  /api/jobintacct/{jobDisplayId}/{franchiseeId}
```

### E-Sign (2) — `/api/e-sign/`
```
GET  /api/e-sign/result?envelope={env}&event={evt}
GET  /api/e-sign/{jobDisplayId}/{bookingKey}
```

### Webhooks (6) — `/api/webhooks/`
```
POST /api/webhooks/stripe/handle
POST /api/webhooks/stripe/connect/handle
POST /api/webhooks/stripe/checkout.session.completed
POST /api/webhooks/twilio/body-sms-inbound
POST /api/webhooks/twilio/form-sms-inbound
POST /api/webhooks/twilio/smsStatusCallback
```

### SMS Templates (5) — `/api/SmsTemplate/`
```
GET  /api/SmsTemplate/list?companyId={id}
GET  /api/SmsTemplate/notificationTokens
POST /api/SmsTemplate/save  [json body]
GET  /api/SmsTemplate/{templateId}
DEL  /api/SmsTemplate/{templateId}
```

### Notifications (1)
```
GET  /api/notifications
```

### Values (1)
```
GET  /api/Values
```

### Companies Extensions (7)
```
POST /api/companies/filteredCustomers  [json body]
GET  /api/companies/infoFromKey
GET  /api/companies/search
POST /api/companies/simplelist  [json body]
GET  /api/companies/{companyId}/capabilities
POST /api/companies/{companyId}/capabilities  [json body]
GET  /api/companies/{companyId}/franchiseeAddresses
```

### Contacts Extensions (2)
```
POST /api/contacts/customers  [json body]
POST /api/contacts/search  [json body]
```

### Address Extensions (2)
```
POST /api/address/{addressId}/avoidValidation
POST /api/address/{addressId}/validated
```

### Documents Extensions (2)
```
GET  /api/documents/get/thumbnail/{docPath}
PUT  /api/documents/hide/{docId}
```

### Users Extension (1)
```
GET  /api/users/pocusers
```

## ABC Endpoints (7)

```
GET  /api/Test/contact                    [abc surface]
GET  /api/Test/recentestimates            [abc surface]
GET  /api/Test/renderedtemplate            [abc surface]
POST /api/Web2Lead/postv2  [json body]    [abc surface]
POST /api/autoprice/quoterequest  [json]  [abc surface]
POST /api/logbuffer/flush                 [abc surface]
GET  /api/report/webrevenue               [abc surface]
```
