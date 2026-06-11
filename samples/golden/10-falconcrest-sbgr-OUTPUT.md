# Sample Output 10 — SBGR arrival, handling only (HANDLE)

> ⚠️ Fictional. Golden for `samples/inbound/10-falconcrest-sbgr-handling.md`. Fixed reference
> PN2606053 supplied by operator. Single service, single airport. Terse email parsing.

```
CASE: 10-falconcrest-sbgr
DECISION: HANDLE   INTENT: NEW   OP-STATUS: OPEN   CONFIDENCE: HIGH   REF: PN2606053
SERVICES: handling=REQUESTED
ROUTING: -
REASON: -
```

━━ HANDLE · NEW · OPEN · PN2606053 ━━
Falcon Crest Executive · T7-FCY (Global 7500) · ARR SBGR 19JUN 1500Z ← SUMU · POB 6/3

DOING → 1 provider email + 1 client ack staged:
  1. SBGR · handling    → Tropic Wings Handling   (ops@tropicwings.example)
  → ack                 → Falcon Crest Executive   (ops@falconcrest-exec.example)

⛑ FLAGS
  - none

▸ DRAFTS — the part a human sends

*SBGR handling* → `ops@tropicwings.example`
```
Subject: T7-FCY | SBGR | HANDLING REQUEST | PN2606053
ARR SBGR 19JUN 1500Z FROM SUMU. 6 PAX / 3 CREW. STANDARD GROUND HANDLING.
```
*Client ack* → `ops@falconcrest-exec.example`
```
Subject: Re: T7-FCY | SBGR | ARR 19 JUN 1500Z | HANDLING | PN2606053
Hi Lucia, confirmed receipt of PN2606053 — handling at SBGR for T7-FCY, 19 JUN 1500Z.
Arranging with Tropic Wings Handling; confirmation to follow.
```

▸ TRIP RECORD
```
OPERATION  PN2606053   status: OPEN
operator:  Falcon Crest Executive (FCX) · T1 · Part 135 · credit OK
aircraft:  T7-FCY · Global 7500 · FCX512
itinerary:
  - ARRIVAL  SBGR  19JUN 1500Z ← SUMU   POB 6/3
services:
  - handling  · Tropic Wings Handling  · REQUESTED · cc —
```
