# Sample Output 01 — Falcon Crest arrival SUMU (HANDLE)

> ⚠️ Fictional. Golden for `samples/inbound/01-falconcrest-arrival-handling.md`. Fixed reference
> PN2606014 supplied by operator. Two in-scope services: handling + ground transport.

```
CASE: 01-falconcrest-arrival
DECISION: HANDLE   INTENT: NEW   OP-STATUS: OPEN   CONFIDENCE: HIGH   REF: PN2606014
SERVICES: handling=REQUESTED ground_transport=REQUESTED
ROUTING: ground_transport=procurement
REASON: -
```

━━ HANDLE · NEW · OPEN · PN2606014 ━━
Falcon Crest Executive · T7-FCX (Global 7500) · ARR SUMU 12JUN 1400Z ← SCEL · POB 4/3

DOING → 2 provider emails + 1 client ack staged:
  1. SUMU · handling    → Plata Handling Services   (ops@platahandling.example)
  2. SUMU · transport   → Costa Chauffeur   cc procurement@   (reservations@costachauffeur.example)
  → ack                 → Falcon Crest Executive   (ops@falconcrest-exec.example)

⛑ FLAGS
  - confirm transport local pickup time once handler posts arrival

▸ DRAFTS — the part a human sends

*SUMU handling* → `ops@platahandling.example`
```
Subject: T7-FCX | SUMU | HANDLING REQUEST | PN2606014
ARR SUMU 12JUN 1400Z FROM SCEL. 4 PAX / 3 CREW. STANDARD HANDLING.
```
*SUMU ground transport* → `reservations@costachauffeur.example`, CC procurement@
```
Subject: T7-FCX | SUMU | GROUND TRANSPORT REQUEST | PN2606014
12JUN on arrival (ETA 1400Z): FBO → city hotel, 3 crew, 1 vehicle. Card attached.
```
*Client ack* → `ops@falconcrest-exec.example`
```
Subject: Re: T7-FCX | SUMU | ARRIVAL HANDLING REQUEST | PN2606014
Hi Lucia, we have T7-FCX at SUMU (12 JUN) under PN2606014.
We are arranging:
  • SUMU — ground handling (Plata Handling Services)
  • SUMU — crew transport FBO → city hotel on arrival
We'll revert with confirmations shortly.
```

▸ TRIP RECORD
```
OPERATION  PN2606014   status: OPEN
operator:  Falcon Crest Executive (FCX) · T1 · Part 135 · credit OK
aircraft:  T7-FCX · Global 7500 · FCX441
itinerary:
  - ARRIVAL  SUMU  12JUN 1400Z ← SCEL   POB 4/3
services:
  - handling          · Plata Handling Services  · REQUESTED · cc —
  - ground_transport  · Costa Chauffeur          · REQUESTED · cc procurement
```
