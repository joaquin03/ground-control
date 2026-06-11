# Edge Output E06 — Provider confirmation reply (FYI)

> ⚠️ Fictional. Golden for `samples/inbound/E06-provider-confirmation-fyi.md`. A provider
> confirmation on a live thread must NOT be read as a new handling request — note it as FYI.

```
CASE: E06-provider-confirm
DECISION: HANDLE   INTENT: FYI   OP-STATUS: OPEN   CONFIDENCE: HIGH   REF: PN2606014
SERVICES: handling=CONFIRMED
ROUTING: -
REASON: -
```

━━ HANDLE · FYI · OPEN · PN2606014 ━━
Falcon Crest Executive · T7-FCX (Global 7500) · ARR SUMU 12JUN 1400Z ← SCEL · POB 4/3

This is a provider (`ops@platahandling.example`) replying Re: our handling request on PN2606014 —
information arriving back, not a new ask. Record it; generate no outbound. Reuse the thread REF; no
new PN is minted.

⛑ FLAGS
  - watch for the post-movement charges email so the trip can be closed

▸ TRIP RECORD
```
OPERATION  PN2606014   status: OPEN
operator:  Falcon Crest Executive (FCX) · T1 · Part 135 · credit OK
aircraft:  T7-FCX · Global 7500 · FCX441
itinerary:
  - ARRIVAL  SUMU  12JUN 1400Z ← SCEL   POB 4/3
services:
  - handling  · Plata Handling Services  · CONFIRMED · cc —
```
