# Sample Output 03 — ETA amendment (HANDLE as AMENDMENT)

> ⚠️ Fictional. Golden for `samples/inbound/03-eta-amendment.md`. Reuses existing reference
> PN2606014; op-status becomes AMENDED. Propagates time change to affected providers only.

```
CASE: 03-eta-amendment
DECISION: HANDLE   INTENT: AMENDMENT   OP-STATUS: AMENDED   CONFIDENCE: HIGH   REF: PN2606014
SERVICES: handling=REQUESTED ground_transport=REQUESTED
ROUTING: ground_transport=procurement
REASON: -
```

━━ HANDLE · AMENDMENT · AMENDED · PN2606014 ━━
Falcon Crest Executive · T7-FCX (Global 7500) · ARR SUMU 12JUN 1630Z ← SCEL (was 1400Z) · POB 4/3

DOING → delta notices to 2 affected providers + 1 client ack (Variant B):
  1. SUMU · handling    → Plata Handling Services   re-time   (ops@platahandling.example)
  2. SUMU · transport   → Costa Chauffeur   re-confirm   cc procurement@   (reservations@costachauffeur.example)
  → ack                 → Falcon Crest Executive   Variant B   (ops@falconcrest-exec.example)

⛑ FLAGS
  - no new reference created — amendment to PN2606014
  - confirm both providers re-acknowledge the new time before treating change as settled

▸ DRAFTS — the part a human sends

*SUMU handling amendment* → `ops@platahandling.example`
```
Subject: Re: T7-FCX | SUMU | HANDLING REQUEST | PN2606014
ATTN: Plata Handling Services — AMENDMENT to PN2606014.
Revised ETA SUMU: 12JUN 1630Z (was 1400Z). All else unchanged. Please re-confirm.
```
*SUMU ground transport amendment* → `reservations@costachauffeur.example`, CC procurement@
```
Subject: Re: T7-FCX | SUMU | GROUND TRANSPORT REQUEST | PN2606014
ATTN: Costa Chauffeur — AMENDMENT to PN2606014.
Arrival now 12JUN 1630Z; please move crew pickup to follow the new arrival. Re-confirm timing.
```
*Client ack (Variant B)* → `ops@falconcrest-exec.example`
```
Subject: Re: T7-FCX | SUMU | ARRIVAL HANDLING REQUEST | PN2606014
Hi Lucia, noted on PN2606014. We have updated the ETA to 12 JUN 1630Z and shifted crew
transport to follow the new arrival. We are notifying Plata Handling and Costa Chauffeur.
Everything else stays unchanged.
```

▸ TRIP RECORD
```
OPERATION  PN2606014   status: AMENDED
operator:  Falcon Crest Executive (FCX) · T1 · Part 135 · credit OK
aircraft:  T7-FCX · Global 7500 · FCX441
itinerary:
  - ARRIVAL  SUMU  12JUN 1630Z ← SCEL   POB 4/3   [amended: was 1400Z]
services:
  - handling          · Plata Handling Services  · REQUESTED · cc —
  - ground_transport  · Costa Chauffeur          · REQUESTED · cc procurement
```
