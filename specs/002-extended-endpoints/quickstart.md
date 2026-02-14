# Quickstart: Extended API Endpoints

**Branch**: `002-extended-endpoints` | **Date**: 2026-02-13

## Prerequisites

The `ab` SDK must be installed and configured per the feature 001 quickstart. These examples assume a working `ABConnectAPI` client.

```python
from ab.client import ABConnectAPI

api = ABConnectAPI()
```

## Job Timeline & Status

### View timeline tasks

```python
tasks = api.jobs.get_timeline("12345")
for task in tasks:
    print(f"{task.task_code}: {task.status_name} (scheduled: {task.scheduled_date})")
```

### Advance job status

```python
result = api.jobs.increment_status("12345")
result.raise_for_error()
print("Job status advanced")
```

### Undo last status change

```python
result = api.jobs.undo_increment_status("12345")
result.raise_for_error()
print("Status reverted")
```

### Create a timeline task

```python
task = api.jobs.create_timeline_task("12345", {
    "taskCode": "SCH",
    "scheduledDate": "2026-03-01T09:00:00",
    "comments": "Scheduled for pickup",
})
print(f"Created task: {task.id}")
```

## Shipments

### Get rate quotes

```python
quotes = api.shipments.get_rate_quotes("12345")
for quote in quotes:
    print(f"{quote.carrier_name}: ${quote.total_charge} ({quote.transit_days} days)")
```

### Book a shipment

```python
result = api.shipments.book("12345", {
    "providerOptionIndex": 0,
    "shipDate": "2026-03-01",
})
result.raise_for_error()
print("Shipment booked")
```

### List accessorials

```python
accessorials = api.shipments.get_accessorials("12345")
for acc in accessorials:
    print(f"{acc.name}: ${acc.price}")
```

### Get origin/destination

```python
od = api.shipments.get_origin_destination("12345")
print(f"From: {od.origin}")
print(f"To: {od.destination}")
```

## Tracking

### Get tracking info

```python
tracking = api.jobs.get_tracking("12345")
print(f"Status: {tracking.status}")
print(f"Location: {tracking.location}")
print(f"ETA: {tracking.estimated_delivery}")
```

### Get tracking with history (v3)

```python
tracking = api.jobs.get_tracking_v3("12345", history_amount=10)
for detail in tracking.tracking_details:
    print(detail)
```

## Payments

### Get payment info

```python
payment = api.payments.get("12345")
print(f"Total: ${payment.total_amount}")
print(f"Balance due: ${payment.balance_due}")
print(f"Status: {payment.payment_status}")
```

### List payment sources

```python
sources = api.payments.get_sources("12345")
for src in sources:
    print(f"{src.type}: ****{src.last_four} {'(default)' if src.is_default else ''}")
```

### Pay by stored source

```python
result = api.payments.pay_by_source("12345", {"sourceId": "src_abc123"})
result.raise_for_error()
print("Payment processed")
```

## Forms

### Generate an invoice

```python
pdf_bytes = api.forms.get_invoice("12345")
with open("invoice_12345.pdf", "wb") as f:
    f.write(pdf_bytes)
print(f"Invoice saved ({len(pdf_bytes)} bytes)")
```

### Generate a bill of lading

```python
pdf_bytes = api.forms.get_bill_of_lading("12345")
with open("bol_12345.pdf", "wb") as f:
    f.write(pdf_bytes)
```

### Generate a packing slip

```python
pdf_bytes = api.forms.get_packing_slip("12345")
with open("packing_slip_12345.pdf", "wb") as f:
    f.write(pdf_bytes)
```

### List shipment plans (for BOL selection)

```python
plans = api.forms.get_shipments("12345")
for plan in plans:
    print(f"Plan {plan.shipment_plan_id}: {plan.carrier_name} ({plan.service_type})")

# Use a specific plan for BOL
pdf_bytes = api.forms.get_bill_of_lading("12345",
    shipment_plan_id=plans[0].shipment_plan_id,
    provider_option_index=plans[0].provider_option_index)
```

## Notes

### List job notes

```python
notes = api.jobs.list_notes("12345")
for note in notes:
    print(f"[{note.author}] {note.comment}")
```

### Create a note

```python
note = api.jobs.create_note("12345", {
    "comments": "Customer called about delivery window",
    "taskCode": "SCH",
    "isImportant": True,
    "sendNotification": True,
})
print(f"Note created: {note.id}")
```

## Parcel Items

### List parcel items

```python
parcels = api.jobs.list_parcel_items("12345")
for p in parcels:
    print(f"{p.description}: {p.length}x{p.width}x{p.height} ({p.weight} lbs)")
```

### Create a parcel item

```python
parcel = api.jobs.create_parcel_item("12345", {
    "description": "Antique dresser",
    "length": 48,
    "width": 24,
    "height": 36,
    "weight": 150,
    "quantity": 1,
})
print(f"Parcel created: {parcel.parcel_item_id}")
```

### Get parcel items with materials

```python
items = api.jobs.get_parcel_items_with_materials("12345")
for item in items:
    print(f"{item.description}: {len(item.materials or [])} materials")
```
