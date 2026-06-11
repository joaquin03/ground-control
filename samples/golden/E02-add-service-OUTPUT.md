# Edge Output E02 — Add a service to a live trip (HANDLE)

> ⚠️ Fictional. Golden for `samples/inbound/E02-add-service.md`. Adding work is in scope: one
> lookup, one new draft, attached to the existing reference PN2606014.

```
CASE: E02-add-service
DECISION: HANDLE   INTENT: AMENDMENT   OP-STATUS: AMENDED   CONFIDENCE: HIGH   REF: PN2606014
SERVICES: catering=REQUESTED
ROUTING: -
REASON: -
```

━━ HANDLE · AMENDMENT · AMENDED · PN2606014 ━━
Falcon Crest Executive · T7-FCX (Global 7500) · ARR SUMU 12JUN 1400Z ← SCEL · POB 4/3

DOING → 1 new service email + 1 client ack (Variant B):
  1. SUMU · catering    → Plata Handling Services   (ops@platahandling.example)
  → ack                 → Falcon Crest Executive   Variant B   (ops@falconcrest-exec.example)

⛑ FLAGS
  - no new reference created — catering addition to PN2606014
  - handling and ground transport on PN2606014 unchanged

▸ DRAFTS — the part a human sends

*SUMU catering* → `ops@platahandling.example`
```
Subject: T7-FCX | SUMU | CATERING ORDER | PN2606014
ATTN: Plata Handling Services
REF: PN2606014 (ADDITION TO EXISTING TRIP)

CATERING ORDER FOR:
OPERATOR:  Falcon Crest Executive   FLIGHT: FCX441 / T7-FCX
AIRPORT:   SUMU (Carrasco Intl)
DELIVERY:  12JUN on arrival (ETA 1400Z) — to aircraft on stand
FOR:       4 PAX
ORDER:     Light lunch x4
DIETARY:   1 vegetarian
PLEASE CONFIRM AND SEND QUOTE.
```
*Client ack (Variant B)* → `ops@falconcrest-exec.example`
```
Subject: Re: T7-FCX | SUMU | ARRIVAL HANDLING REQUEST | PN2606014
Hi Lucia, noted on PN2606014 — we've added VIP catering at SUMU for 4 pax on arrival
(light lunch, 1 vegetarian). We're arranging it with Plata Handling. Everything else stands.
```

▸ TRIP RECORD
```
OPERATION  PN2606014   status: AMENDED
operator:  Falcon Crest Executive (FCX) · T1 · Part 135 · credit OK
aircraft:  T7-FCX · Global 7500 · FCX441
itinerary:
  - ARRIVAL  SUMU  12JUN 1400Z ← SCEL   POB 4/3
services:
  - catering  · Plata Handling Services  · REQUESTED · cc —
```
