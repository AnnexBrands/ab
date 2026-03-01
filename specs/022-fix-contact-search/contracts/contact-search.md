# Contract: POST /contacts/v2/search

## Request

Model: `ContactSearchRequest` (extra="forbid")

```json
{
  "mainSearchRequest": {
    "contactDisplayId": 1,
    "fullName": "Training",
    "companyName": "Training",
    "companyCode": "Training",
    "email": "training@annexbrands.com",
    "phone": "+3334445566",
    "companyDisplayId": 694618
  },
  "loadOptions": {
    "pageNumber": 1,
    "pageSize": 10,
    "sortingBy": "fullName",
    "sortingDirection": 0
  }
}
```

### Validation Rules

- `loadOptions` is required (HTTP 400 without it)
- `loadOptions.pageNumber` is required (1-32767)
- `loadOptions.pageSize` is required (1-32767)
- `mainSearchRequest` is optional (omit for unfiltered results)
- All search fields are optional

## Response

Model: `List[SearchContactEntityResult]` (extra="allow")

```json
[
  {
    "contactID": 30760,
    "customerCell": null,
    "contactDisplayId": "1308994",
    "contactFullName": "Justine Yigitbasi",
    "contactPhone": "6147065958",
    "contactHomePhone": null,
    "contactEmail": "oh14004@goNavis.com",
    "masterConstantValue": null,
    "contactDept": null,
    "address1": "5738 Westbourne Ave",
    "address2": null,
    "city": "Columbus",
    "state": "OH",
    "zipCode": "43213",
    "countryName": null,
    "companyCode": "14004OH",
    "companyID": "93179b52-3da9-e311-b6f8-000c298b59ee",
    "companyName": "Navis Pack & Ship #14004OH",
    "companyDisplayId": "852949",
    "isPrefered": true,
    "industryType": null,
    "totalRecords": 1
  }
]
```

## Gate Criteria

| Gate | Criteria |
|------|----------|
| G1 | `SearchContactEntityResult.model_validate(fixture[0]).__pydantic_extra__ == {}` |
| G2 | `tests/fixtures/mocks/SearchContactEntityResult.json` exists |
| G3 | Test has isinstance + assert_no_extra_fields |
| G4 | Return type is `list[SearchContactEntityResult]` (already correct) |
| G5 | No query params — auto-pass |
| G6 | Request model has typed signature, field descriptions, no TODOs |
