# Sample Output 02 — Adriatic Wings departure, full service (HANDLE)

> ⚠️ Fictional. Golden for `samples/inbound/02-adriaticwings-departure-full.md`.
> 3-zone action-board contract (`reference/decision-card.md`): machine header → Glance → Drafts → Trip record.

```
CASE: 02-adriatic-departure
DECISION: HANDLE   INTENT: NEW   OP-STATUS: OPEN   CONFIDENCE: HIGH   REF: PN2606032
SERVICES: handling=REQUESTED ground_transport=REQUESTED catering=REQUESTED hotel=TBC
ROUTING: ground_transport=procurement hotel=procurement
REASON: -
```

━━ HANDLE · NEW · OPEN · PN2606032 ━━
Adriatic Wings · 9H-ADW (G650) · DEP LEMD 14JUN 0930Z → LFPB · POB 6/4

DOING → 4 provider emails + 1 client ack staged:
  1. LEMD · handling          → Iberus Ramp Partners   (handling@iberusramp.example)
  2. LEMD · ground_transport  → Velvet Drive Madrid   cc procurement@   (madrid@velvetdrive.example)
  3. LEMD · catering          → Air Gourmet Iberia   (madrid@airgourmet.example)
  4. LEMD · hotel (named)     → Hotel Borealis Madrid   cc procurement@   (TBC — reservations email unknown)
  → ack                       → Adriatic Wings   (ops@adriaticwings.example)

⛑ FLAGS
  - hotel reservations email unknown → hotel line TBC; confirm the address before sending
  - de-ice standby — handler advises if WX triggers
  - do not split the trip — all four services move together under PN2606032

▸ DRAFTS — the part a human sends

— handling → Iberus Ramp Partners —
```
ATTN: Iberus Ramp Partners
FROM: APEX TRIP SUPPORT - OPS
DATE: 09JUN2026
REF:  PN2606032

WE REQUEST AIRCRAFT GROUND HANDLING FOR THE FOLLOWING FLIGHT:

A. OPERATOR:      Adriatic Wings
B. REGISTRY:      9H-ADW   ACFT TYPE: Gulfstream G650
C. TYPE OF FLIGHT:Commercial Non-Sched (Part 135)   CALL SIGN: ADW88
D. MOVEMENT:      DEPARTURE
   ETD LEMD 14JUN 0930Z TO LFPB
E. PERSONS ON BOARD: 6 PAX / 4 CREW
F. SERVICES REQUESTED:
   - STANDARD GROUND HANDLING
   - DE-ICE ON STANDBY
G. REMARKS: De-ice on standby — confirm if WX triggers.

PLEASE CONFIRM RECEIPT, AVAILABILITY AND CHARGES.

KIND REGARDS,
APEX TRIP SUPPORT - OPERATIONS
info@apextrip.example
```

— ground_transport → Velvet Drive Madrid —
```
ATTN: Velvet Drive Madrid
FROM: APEX TRIP SUPPORT - OPS
DATE: 09JUN2026
REF:  PN2606032

WE REQUEST CHAUFFEUR / GROUND TRANSPORT FOR THE FOLLOWING:

OPERATOR:   Adriatic Wings   FLIGHT: ADW88 / 9H-ADW
AIRPORT:    LEMD (Adolfo Suarez Madrid-Barajas)
DATE/TIME:  14JUN 0700 LT  (0500Z)
PASSENGERS: 4  (PICKUP: Hotel Borealis Madrid)  DROP-OFF: LEMD
VEHICLE:    1 van (seats 4)
REMARKS:    Crew transfer hotel → airport.

PAYMENT: corporate card attached.
PLEASE CONFIRM AVAILABILITY AND RATE.

KIND REGARDS,
APEX TRIP SUPPORT - OPERATIONS
info@apextrip.example
```

— catering → Air Gourmet Iberia —
```
ATTN: Air Gourmet Iberia
FROM: APEX TRIP SUPPORT - OPS
DATE: 09JUN2026
REF:  PN2606032

CATERING ORDER FOR:

OPERATOR:   Adriatic Wings   FLIGHT: ADW88 / 9H-ADW
AIRPORT:    LEMD (Adolfo Suarez Madrid-Barajas)
DELIVERY:   14JUN 0800 LT — TO AIRCRAFT ON STAND / VIA HANDLER Iberus Ramp Partners
FOR:        6 PAX / 4 CREW

ORDER:
  - VIP breakfast service for 6 pax

DIETARY / REMARKS: 2 vegetarian, no shellfish.

PLEASE CONFIRM AND SEND QUOTE.

KIND REGARDS,
APEX TRIP SUPPORT - OPERATIONS
```

— hotel → Hotel Borealis Madrid (Variant A — operator-named; reservations email TBC) —
```
ATTN: RESERVATIONS - Hotel Borealis Madrid
FROM: APEX TRIP SUPPORT - OPS
REF:  PN2606032

PLEASE BOOK THE FOLLOWING ON BEHALF OF OUR CREW:

GUEST(S):   4 (CREW)
ROOMS:      4 x standard
CHECK-IN:   13JUN2026    CHECK-OUT: 14JUN2026
REMARKS:    Crew rest; quiet rooms if available.

PAYMENT: corporate card attached.
PLEASE CONFIRM AND SEND BOOKING REFERENCE.

APEX TRIP SUPPORT - OPERATIONS
```
> ⓘ To-address TBC — Hotel Borealis reservations email not on file. Do not send until confirmed.

— ack → Adriatic Wings (Variant A, new) —
```
HI Marko,

Thank you — we have your request for 9H-ADW at LEMD (14JUN) under reference PN2606032.

We are arranging:
  - Ground handling at LEMD + de-ice on standby
  - Crew transport: Hotel Borealis Madrid → LEMD, 14JUN 0700 LT
  - VIP catering for 6, delivered 14JUN 0800 LT
  - Hotel: 4 crew rooms at Hotel Borealis Madrid, 13–14 JUN

We will revert with provider confirmations shortly. Please send any pending details:
  - Hotel Borealis reservations email (so we can confirm the booking)

KIND REGARDS,
APEX TRIP SUPPORT - OPERATIONS
info@apextrip.example
```

▸ TRIP RECORD
```
OPERATION  PN2606032   status: OPEN
operator:  Adriatic Wings (ADW) · T2 · Part 135 · credit OK
aircraft:  9H-ADW · Gulfstream G650 · ADW88
itinerary:
  - DEPARTURE  LEMD  14JUN 0930Z → LFPB   POB 6/4
services:
  - handling          · Iberus Ramp Partners   · REQUESTED · cc —
  - ground_transport  · Velvet Drive Madrid     · REQUESTED · cc procurement
  - catering          · Air Gourmet Iberia      · REQUESTED · cc —
  - hotel (named)     · Hotel Borealis Madrid   · TBC       · cc procurement
LEDGER  += sequences."2606"=32 · trips."ADW|9H-ADW|14JUN26|LEMD"="PN2606032"
```
