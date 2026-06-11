# Sample Output 07 — Multi-leg trip, two airports (HANDLE)

> ⚠️ Fictional. Golden for `samples/inbound/07-solaris-multileg-handling.md`. One reference,
> two handling stations — a separate lookup and draft per station.

```
CASE: 07-solaris-multileg
DECISION: HANDLE   INTENT: NEW   OP-STATUS: OPEN   CONFIDENCE: HIGH   REF: PN2606031
SERVICES: handling=REQUESTED ground_transport=REQUESTED
ROUTING: ground_transport=procurement
REASON: -
```

━━ HANDLE · NEW · OPEN · PN2606031 ━━
Solaris Jet Group · M-SJGX (Falcon 8X) · 2 stops: LFPB → EGGW · POB 4/2

DOING → 3 provider emails + 1 client ack staged:
  1. LFPB · handling    → Le Bourget Executive Handling   (ops@lbehandling.example)
  2. LFPB · transport   → Velvet Drive Paris   cc procurement@   (paris@velvetdrive.example)
  3. EGGW · handling    → Albion Ground Services   (ops@albionground.example)
  → ack                 → Solaris Jet Group   (ops@solarisjet.example)

⛑ FLAGS
  - one REF spans 2 airports — do not split the trip
  - confirm LFPB pickup local time once the handler posts on-blocks

▸ DRAFTS — the part a human sends

*LFPB handling* → `ops@lbehandling.example`
```
Subject: M-SJGX | LFPB | HANDLING REQUEST | PN2606031
ARR LFPB 18JUN 1000Z FROM KMIA; DEP LFPB 20JUN 0900Z TO EGGW. 4 PAX / 2 CREW. STANDARD HANDLING.
```
*LFPB ground transport* → `paris@velvetdrive.example`, CC procurement@
```
Subject: M-SJGX | LFPB | GROUND TRANSPORT REQUEST | PN2606031
18JUN on arrival (ETA 1000Z): FBO → city hotel, 2 crew, 1 vehicle. Card attached.
```
*EGGW handling* → `ops@albionground.example`
```
Subject: M-SJGX | EGGW | HANDLING REQUEST | PN2606031
ARR EGGW 20JUN 0945Z FROM LFPB. 4 PAX / 2 CREW. STANDARD HANDLING.
```
*Client ack* → `ops@solarisjet.example`
```
Subject: Re: M-SJGX | LFPB + EGGW | HANDLING — 2 STOPS | 18–20 JUN
Hi team, we have M-SJGX as one trip under PN2606031:
  • LFPB — handling (18 JUN arr / 20 JUN dep) + crew transport on arrival
  • EGGW — handling (20 JUN arr)
We'll revert with both stations' confirmations.
```

▸ TRIP RECORD
```
OPERATION  PN2606031   status: OPEN
operator:  Solaris Jet Group (SJG) · T2 · Part 91 · credit OK
aircraft:  M-SJGX · Falcon 8X · SJG12
itinerary:
  - ARRIVAL    LFPB  18JUN 1000Z ← KMIA   POB 4/2
  - DEPARTURE  LFPB  20JUN 0900Z → EGGW
  - ARRIVAL    EGGW  20JUN 0945Z ← LFPB
services:
  - handling (LFPB)          · Le Bourget Executive Handling  · REQUESTED · cc —
  - ground_transport (LFPB)  · Velvet Drive Paris             · REQUESTED · cc procurement
  - handling (EGGW)          · Albion Ground Services         · REQUESTED · cc —
LEDGER  += sequences."2606"=31 · trips."SJG|M-SJGX|18JUN26|LFPB"="PN2606031"
```
