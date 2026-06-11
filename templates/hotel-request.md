# Template — Hotel Request (outbound)

> ⚠️ Demo template. Fictional data only. Hotel has **no ICAO provider lookup**.

There are two variants. Pick based on whether the operator named a hotel.

**Send from:** `info@apextrip.example`
**CC:** `procurement@apextrip.example` (credit card attached for the booking)
**BCC:** `info@apextrip.example`
**Subject:** `{{REGISTRY}} | {{ICAO}} | HOTEL REQUEST | {{REF}}`

---

## Variant A — operator named a specific hotel → book it directly
**To:** `{{NAMED_HOTEL_RESERVATIONS_EMAIL_OR_TBC}}`

```
ATTN: RESERVATIONS - {{HOTEL_NAME}}
FROM: APEX TRIP SUPPORT - OPS
REF:  {{REF}}

PLEASE BOOK THE FOLLOWING ON BEHALF OF OUR CREW/PASSENGERS:

GUEST(S):   {{GUEST_COUNT}} ({{CREW_OR_PAX}})
ROOMS:      {{ROOM_COUNT}} x {{ROOM_TYPE}}
CHECK-IN:   {{CHECKIN_DATE}}    CHECK-OUT: {{CHECKOUT_DATE}}
REMARKS:    {{REMARKS}}

PAYMENT: corporate card attached.
PLEASE CONFIRM AND SEND BOOKING REFERENCE.

APEX TRIP SUPPORT - OPERATIONS
```

## Variant B — no hotel named → request 3 options
**To:** operator (`{{OPERATOR_EMAIL}}`) — we propose, operator chooses.

```
HI {{OPERATOR_CONTACT}},

FOR {{REGISTRY}} AT ({{CITY}}), {{CHECKIN_DATE}}–{{CHECKOUT_DATE}}, we suggest the
following 4–5 star hotels close to the airport for {{GUEST_COUNT}} guest(s), {{ROOM_COUNT}} room(s):

  1. {{OPTION_1}}
  2. {{OPTION_2}}
  3. {{OPTION_3}}

Please confirm your preference and we will book.

KIND REGARDS,
APEX TRIP SUPPORT - OPERATIONS
```
