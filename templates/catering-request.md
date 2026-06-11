# Template — Catering Request (outbound to provider)

> ⚠️ Demo template. Fictional data only.

**Send from:** `info@apextrip.example`
**To:** `{{CATERING_PROVIDER_EMAIL}}`
**CC:** `procurement@apextrip.example` if provider `payment_type=CREDIT_CARD`
**BCC:** `info@apextrip.example`
**Subject:** `{{REGISTRY}} | {{ICAO}} | CATERING ORDER | {{REF}}`

---

```
ATTN: {{CATERING_PROVIDER_NAME}}
FROM: APEX TRIP SUPPORT - OPS
DATE: {{TODAY_DDMMMYYYY}}
REF:  {{REF}}

CATERING ORDER FOR:

OPERATOR:   {{OPERATOR_NAME}}   FLIGHT: {{FLIGHT_NUMBER}} / {{REGISTRY}}
AIRPORT:    {{ICAO}} ({{AIRPORT_NAME}})
DELIVERY:   {{DATE_DDMMM}} {{DELIVERY_TIME}} LT — TO AIRCRAFT ON STAND / VIA HANDLER {{HANDLER_NAME}}
FOR:        {{PAX}} PAX / {{CREW}} CREW

ORDER:
{{CATERING_ITEMS}}

DIETARY / REMARKS: {{REMARKS}}

PLEASE CONFIRM AND SEND QUOTE.

KIND REGARDS,
APEX TRIP SUPPORT - OPERATIONS
```
