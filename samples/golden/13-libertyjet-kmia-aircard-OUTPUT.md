# Sample Output 13 — Liberty Jet arrival KMIA (HANDLE; CC rule 2)

> ⚠️ Fictional. Golden for `samples/inbound/13-libertyjet-kmia-aircard.md`. Proves matrix rule 2:
> US station + payment_profile=AIRCARD → CC accounting@.

```
CASE: 13-libertyjet-kmia-aircard
DECISION: HANDLE   INTENT: NEW   OP-STATUS: OPEN   CONFIDENCE: HIGH   REF: PN2606037
SERVICES: handling=REQUESTED
ROUTING: handling=accounting
REASON: -
```

━━ HANDLE · NEW · OPEN · PN2606037 ━━
Liberty Jet Partners · N455LJ (Bombardier Global 6000) · ARR KMIA 16JUN 1830Z ← KTEB · POB 4/3

DOING → 1 provider email + 1 client ack staged:
  1. KMIA · handling    → Anchor Aviation Services   cc accounting@   (dispatch@anchoraviation.example)
  → ack                 → Liberty Jet Partners   (ops@libertyjet.example)

⛑ FLAGS
  - operator pays via US Aircard → CC accounting@ (matrix rule 2: US station + AIRCARD)

▸ DRAFTS — the part a human sends

*KMIA handling* → `dispatch@anchoraviation.example`, CC accounting@
```
Subject: N455LJ | KMIA | HANDLING REQUEST | PN2606037
ARR KMIA 16JUN 1830Z FROM KTEB. 4 PAX / 3 CREW. STANDARD ARRIVAL HANDLING.
```
*Client ack* → `ops@libertyjet.example`
```
Subject: Re: N455LJ | KMIA | ARRIVAL 16 JUN — HANDLING
Hi Dana, we have N455LJ at KMIA (16 JUN) under PN2606037. Handling arranged with Anchor
Aviation Services. We'll revert with confirmation.
```

▸ TRIP RECORD
```
OPERATION  PN2606037   status: OPEN
operator:  Liberty Jet Partners (LJP) · T2 · Part 135 · credit OK
aircraft:  N455LJ · Bombardier Global 6000 · LJP455
itinerary:
  - ARRIVAL  KMIA  16JUN 1830Z ← KTEB   POB 4/3
services:
  - handling  · Anchor Aviation Services  · REQUESTED · cc accounting
LEDGER  += sequences."2606"=37 · trips."LJP|N455LJ|16JUN26|KMIA"="PN2606037"
```
