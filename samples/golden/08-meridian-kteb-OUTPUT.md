# Sample Output 08 — KTEB departure, inbound-only transport (HANDLE)

> ⚠️ Fictional. Golden for `samples/inbound/08-meridian-kteb-inbound-only.md`. Handling resolves;
> ground transport is inbound-only at KTEB → service becomes INBOUND-PENDING, no draft sent.

```
CASE: 08-meridian-kteb
DECISION: HANDLE   INTENT: NEW   OP-STATUS: OPEN   CONFIDENCE: HIGH   REF: PN2606033
SERVICES: handling=REQUESTED ground_transport=INBOUND-PENDING
ROUTING: -
REASON: -
```

━━ HANDLE · NEW · OPEN · PN2606033 ━━
Meridian Air Charter · N512MC (Challenger 350) · DEP KTEB 17JUN 1300Z → KMIA · POB 3/2

DOING → 1 provider email + 1 client ack staged:
  1. KTEB · handling    → Summit Jet Center   (ops@summitjetcenter.example)
  2. KTEB · transport   → Drivex Chauffeur (INBOUND — via provider channel, no draft)
  → ack                 → Meridian Air Charter   (ops@meridian-charter.example)

⛑ FLAGS
  - ground_transport @ KTEB = Drivex (inbound_only) → human books via Drivex's own channel; no outbound request generated

▸ DRAFTS — the part a human sends

*KTEB handling* → `ops@summitjetcenter.example`
```
Subject: N512MC | KTEB | HANDLING REQUEST | PN2606033
DEPARTURE — ETD KTEB 17JUN 1300Z TO KMIA. 3 PAX / 2 CREW. STANDARD GROUND HANDLING.
```
*Client ack* → `ops@meridian-charter.example`
```
Subject: Re: N512MC | KTEB | DEPARTURE HANDLING + CREW CAR | 17 JUN
Hi Dana, we have N512MC ex KTEB (17 JUN) under PN2606033. Handling is arranged with Summit
Jet Center. The KTEB crew car is being set up through our local channel — a colleague will
confirm the 0800 LT pickup directly.
```

▸ TRIP RECORD
```
OPERATION  PN2606033   status: OPEN
operator:  Meridian Air Charter (MAC) · T2 · Part 135 · credit OK
aircraft:  N512MC · Challenger 350 · MAC512
itinerary:
  - DEPARTURE  KTEB  17JUN 1300Z → KMIA   POB 3/2
services:
  - handling          · Summit Jet Center   · REQUESTED       · cc —
  - ground_transport  · Drivex Chauffeur    · INBOUND-PENDING  · cc —
LEDGER  += sequences."2606"=33 · trips."MAC|N512MC|17JUN26|KTEB"="PN2606033"
```
