# Template — Handling Request (outbound to provider)

> ⚠️ Demo template. Fill `{{TOKENS}}` from the inbound email + provider lookup. Fictional data only.

**Send from:** `info@apextrip.example`
**To:** `{{HANDLING_PROVIDER_EMAIL}}`
**CC:** see `steps/email-categories.md` → routing (procurement@ if new provider / credit-card; accounting@ if US Aircard)
**BCC:** `info@apextrip.example`
**Subject:** `{{REGISTRY}} | {{ICAO}} | HANDLING REQUEST | {{REF}}`

---

```
ATTN: {{HANDLING_PROVIDER_NAME}}
FROM: APEX TRIP SUPPORT - OPS
DATE: {{TODAY_DDMMMYYYY}}
REF:  {{REF}}

WE REQUEST AIRCRAFT GROUND HANDLING FOR THE FOLLOWING FLIGHT:

A. OPERATOR:      {{OPERATOR_NAME}}
B. REGISTRY:      {{REGISTRY}}   ACFT TYPE: {{AIRCRAFT_TYPE}}
C. TYPE OF FLIGHT:{{TYPE_OF_FLIGHT}}   CALL SIGN: {{FLIGHT_NUMBER}}
D. MOVEMENT:      {{ARRIVAL_OR_DEPARTURE}}
   {{#ARRIVAL}}ETA {{ICAO}} {{DATE_DDMMM}} {{TIME}}Z FROM {{FROM_ICAO}}{{/ARRIVAL}}
   {{#DEPARTURE}}ETD {{ICAO}} {{DATE_DDMMM}} {{TIME}}Z TO {{TO_ICAO}}{{/DEPARTURE}}
E. PERSONS ON BOARD: {{PAX}} PAX / {{CREW}} CREW
F. SERVICES REQUESTED:
   - STANDARD GROUND HANDLING
   {{EXTRA_HANDLING_LINES}}
G. REMARKS: {{REMARKS}}

PLEASE CONFIRM RECEIPT, AVAILABILITY AND CHARGES.

KIND REGARDS,
APEX TRIP SUPPORT - OPERATIONS
info@apextrip.example
```
