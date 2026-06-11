# Sample Output 12 — EGGW arrival, catering has no provider (HANDLE + flag)

> ⚠️ Fictional. Golden for `samples/inbound/12-solaris-eggw-no-catering-provider.md`. Tests a
> lookup miss: EGGW has handling on file but no catering provider → catering=FLAGGED.

```
CASE: 12-solaris-eggw
DECISION: HANDLE   INTENT: NEW   OP-STATUS: OPEN   CONFIDENCE: HIGH   REF: PN2606036
SERVICES: handling=REQUESTED catering=FLAGGED
ROUTING: -
REASON: -
```

━━ HANDLE · NEW · OPEN · PN2606036 ━━
Solaris Jet Group · M-SJGZ (Falcon 8X) · ARR EGGW 22JUN 0930Z ← LEMD · POB 3/2

DOING → 1 provider email + 1 client ack staged:
  1. EGGW · handling    → Albion Ground Services   (ops@albionground.example)
  2. EGGW · catering    → (no provider on file) ⛑ FLAGGED for human
  → ack                 → Solaris Jet Group   (ops@solarisjet.example)

⛑ FLAGS
  - catering @ EGGW: no provider in database → human sources caterer or handler arranges
  - do not send a catering draft until a provider is confirmed

▸ DRAFTS — the part a human sends

*EGGW handling* → `ops@albionground.example`
```
Subject: M-SJGZ | EGGW | HANDLING REQUEST | PN2606036
ARR EGGW 22JUN 0930Z FROM LEMD. 3 PAX / 2 CREW. STANDARD GROUND HANDLING.
```
*Client ack* → `ops@solarisjet.example`
```
Subject: Re: M-SJGZ | EGGW | ARRIVAL 22 JUN — HANDLING + CATERING
Hi Priya, handling at EGGW for M-SJGZ (22 JUN) is arranged with Albion Ground Services
under PN2606036. For catering at EGGW we'll confirm a supplier and revert shortly.
```

▸ TRIP RECORD
```
OPERATION  PN2606036   status: OPEN
operator:  Solaris Jet Group (SJG) · T2 · Part 91 · credit OK
aircraft:  M-SJGZ · Falcon 8X · SJG20
itinerary:
  - ARRIVAL  EGGW  22JUN 0930Z ← LEMD   POB 3/2
services:
  - handling  · Albion Ground Services  · REQUESTED · cc —
  - catering  · —                       · FLAGGED   · cc —
LEDGER  += sequences."2606"=36 · trips."SJG|M-SJGZ|22JUN26|EGGW"="PN2606036"
```
