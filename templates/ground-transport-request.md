# Template — Ground Transport Request (outbound to provider)

> ⚠️ Demo template. Fictional data only. Credit-card payment type → CC procurement@ and attach the card.

**Send from:** `info@apextrip.example`
**To:** `{{GROUND_PROVIDER_EMAIL}}`
**CC:** `procurement@apextrip.example` (ground transport providers are CREDIT_CARD — card attached)
**BCC:** `info@apextrip.example`
**Subject:** `{{REGISTRY}} | {{ICAO}} | GROUND TRANSPORT REQUEST | {{REF}}`

> ⛔ Do not use this template for a provider marked `inbound_only=yes` (e.g. Drivex Chauffeur).
> Those bookings are made through their own channel — flag for a human instead.

---

```
ATTN: {{GROUND_PROVIDER_NAME}}
FROM: APEX TRIP SUPPORT - OPS
DATE: {{TODAY_DDMMMYYYY}}
REF:  {{REF}}

WE REQUEST CHAUFFEUR / GROUND TRANSPORT FOR THE FOLLOWING:

OPERATOR:   {{OPERATOR_NAME}}   FLIGHT: {{FLIGHT_NUMBER}} / {{REGISTRY}}
AIRPORT:    {{ICAO}} ({{AIRPORT_NAME}})
DATE/TIME:  {{DATE_DDMMM}} {{TIME_LOCAL}} LT  ({{TIME}}Z)
PASSENGERS: {{PAX}}  (PICKUP: {{PICKUP_LOCATION}})  DROP-OFF: {{DROPOFF_LOCATION}}
VEHICLE:    {{VEHICLE_TYPE}}
REMARKS:    {{REMARKS}}

PAYMENT: corporate card attached.
PLEASE CONFIRM AVAILABILITY AND RATE.

KIND REGARDS,
APEX TRIP SUPPORT - OPERATIONS
info@apextrip.example
```
