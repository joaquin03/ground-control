# Sample Output 09 — SCEL arrival, full service (HANDLE)

> ⚠️ Fictional. Golden for `samples/inbound/09-adriatic-scel-full.md`. Three in-scope services
> resolve at SCEL. Ground transport has CREDIT_CARD → CC procurement.

```
CASE: 09-adriatic-scel
DECISION: HANDLE   INTENT: NEW   OP-STATUS: OPEN   CONFIDENCE: HIGH   REF: PN2606034
SERVICES: handling=REQUESTED ground_transport=REQUESTED catering=REQUESTED
ROUTING: ground_transport=procurement
REASON: -
```

━━ HANDLE · NEW · OPEN · PN2606034 ━━
Adriatic Wings · 9H-ADV (Gulfstream G650) · ARR SCEL 16JUN 1130Z ← SBGR · POB 5/4

DOING → 3 provider emails + 1 client ack staged:
  1. SCEL · handling    → Andes Ramp Services   (ops@andesramp.example)
  2. SCEL · transport   → Cordillera Cars   cc procurement@   (reservas@cordilleracars.example)
  3. SCEL · catering    → Andes Gourmet   (catering@andesgourmet.example)
  → ack                 → Adriatic Wings   (ops@adriaticwings.example)

⛑ FLAGS
  - confirm transport pickup LT once handler posts arrival

▸ DRAFTS — the part a human sends

*SCEL handling* → `ops@andesramp.example`
```
Subject: 9H-ADV | SCEL | HANDLING REQUEST | PN2606034
ARR SCEL 16JUN 1130Z FROM SBGR. 5 PAX / 4 CREW. STANDARD HANDLING.
```
*SCEL ground transport* → `reservas@cordilleracars.example`, CC procurement@
```
Subject: 9H-ADV | SCEL | GROUND TRANSPORT REQUEST | PN2606034
16JUN on arrival (ETA 1130Z): FBO → city hotel, 4 crew, 1 van. Card attached.
```
*SCEL catering* → `catering@andesgourmet.example`
```
Subject: 9H-ADV | SCEL | CATERING ORDER | PN2606034
Deliver 17JUN 0700 LT to aircraft on stand. Breakfast x5, 1 gluten-free.
```
*Client ack* → `ops@adriaticwings.example`
```
Subject: Re: 9H-ADV | SCEL | ARRIVAL 16 JUN — HANDLING + TRANSPORT + CATERING
Hi Marko, we have 9H-ADV into SCEL (16 JUN) under PN2606034. Arranging:
  • handling (Andes Ramp Services)
  • crew transport FBO → city hotel on arrival
  • next-morning breakfast catering for 5 (1 gluten-free)
We'll revert with confirmations.
```

▸ TRIP RECORD
```
OPERATION  PN2606034   status: OPEN
operator:  Adriatic Wings (ADW) · T2 · Part 135 · credit OK
aircraft:  9H-ADV · Gulfstream G650 · ADW91
itinerary:
  - ARRIVAL  SCEL  16JUN 1130Z ← SBGR   POB 5/4
services:
  - handling          · Andes Ramp Services   · REQUESTED · cc —
  - ground_transport  · Cordillera Cars       · REQUESTED · cc procurement
  - catering          · Andes Gourmet         · REQUESTED · cc —
LEDGER  += sequences."2606"=34 · trips."ADW|9H-ADV|16JUN26|SCEL"="PN2606034"
```
