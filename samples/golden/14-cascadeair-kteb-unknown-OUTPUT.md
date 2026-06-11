# Sample Output 14 — Cascade Air arrival KTEB (HANDLE; CC rule 3, TBC)

> ⚠️ Fictional. Golden for `samples/inbound/14-cascadeair-kteb-unknown.md`. Proves matrix rule 3:
> US station + payment_profile=UNKNOWN → CC accounting@ marked TBC (no guess).

```
CASE: 14-cascadeair-kteb-unknown
DECISION: HANDLE   INTENT: NEW   OP-STATUS: OPEN   CONFIDENCE: HIGH   REF: PN2606038
SERVICES: handling=REQUESTED
ROUTING: handling=accounting-TBC
REASON: -
```

━━ HANDLE · NEW · OPEN · PN2606038 ━━
Cascade Air LLC · N72CA (Cessna Citation Longitude) · ARR KTEB 17JUN 1500Z ← KMIA · POB 5/2

DOING → 1 provider email + 1 client ack staged:
  1. KTEB · handling    → Summit Jet Center   cc accounting@ (TBC — verify payer before sending)   (ops@summitjetcenter.example)
  → ack                 → Cascade Air LLC   (flightdept@cascadeair.example)

⛑ FLAGS
  - payment_profile UNKNOWN at a US station → CC accounting@ marked TBC; verify payer before sending (rule 3)

▸ DRAFTS — the part a human sends

*KTEB handling* → `ops@summitjetcenter.example`, CC accounting@ (TBC)
```
Subject: N72CA | KTEB | HANDLING REQUEST | PN2606038
ARR KTEB 17JUN 1500Z FROM KMIA. 5 PAX / 2 CREW. STANDARD ARRIVAL HANDLING.
```
*Client ack* → `flightdept@cascadeair.example`
```
Subject: Re: N72CA | KTEB | ARRIVAL 17 JUN — HANDLING
Hi Sam, we have N72CA at KTEB (17 JUN) under PN2606038. Handling arranged with Summit Jet
Center. We'll revert with confirmation.
```

▸ TRIP RECORD
```
OPERATION  PN2606038   status: OPEN
operator:  Cascade Air LLC (CSA) · T3 · Part 91 · credit OK
aircraft:  N72CA · Cessna Citation Longitude · N72CA
itinerary:
  - ARRIVAL  KTEB  17JUN 1500Z ← KMIA   POB 5/2
services:
  - handling  · Summit Jet Center  · REQUESTED · cc accounting-TBC
LEDGER  += sequences."2606"=38 · trips."CSA|N72CA|17JUN26|KTEB"="PN2606038"
```
