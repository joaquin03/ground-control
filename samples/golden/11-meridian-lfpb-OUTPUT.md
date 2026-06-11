# Sample Output 11 — LFPB departure, handling + catering (HANDLE)

> ⚠️ Fictional. Golden for `samples/inbound/11-meridian-lfpb-handling-catering.md`. Two in-scope
> services both resolve at LFPB. No CC routing (both CREDIT payment).

```
CASE: 11-meridian-lfpb
DECISION: HANDLE   INTENT: NEW   OP-STATUS: OPEN   CONFIDENCE: HIGH   REF: PN2606035
SERVICES: handling=REQUESTED catering=REQUESTED
ROUTING: -
REASON: -
```

━━ HANDLE · NEW · OPEN · PN2606035 ━━
Meridian Air Charter · N728MC (Gulfstream G450) · DEP LFPB 21JUN 1100Z → LEMD · POB 4/3

DOING → 2 provider emails + 1 client ack staged:
  1. LFPB · handling    → Le Bourget Executive Handling   (ops@lbehandling.example)
  2. LFPB · catering    → Air Gourmet Paris   (paris@airgourmet.example)
  → ack                 → Meridian Air Charter   (ops@meridian-charter.example)

⛑ FLAGS
  - none

▸ DRAFTS — the part a human sends

*LFPB handling* → `ops@lbehandling.example`
```
Subject: N728MC | LFPB | HANDLING REQUEST | PN2606035
DEP LFPB 21JUN 1100Z TO LEMD. 4 PAX / 3 CREW. STANDARD HANDLING.
```
*LFPB catering* → `paris@airgourmet.example`
```
Subject: N728MC | LFPB | CATERING ORDER | PN2606035
Deliver 21JUN 1000 LT to aircraft on stand. Lunch x4. No special diets.
```
*Client ack* → `ops@meridian-charter.example`
```
Subject: Re: N728MC | LFPB | DEPARTURE 21 JUN — HANDLING + CATERING
Hi Dana, we have N728MC ex LFPB (21 JUN) under PN2606035. Arranging:
  • handling (Le Bourget Executive Handling)
  • lunch catering for 4 to aircraft at 1000 LT
We'll revert with confirmations.
```

▸ TRIP RECORD
```
OPERATION  PN2606035   status: OPEN
operator:  Meridian Air Charter (MAC) · T2 · Part 135 · credit OK
aircraft:  N728MC · Gulfstream G450 · MAC728
itinerary:
  - DEPARTURE  LFPB  21JUN 1100Z → LEMD   POB 4/3
services:
  - handling  · Le Bourget Executive Handling  · REQUESTED · cc —
  - catering  · Air Gourmet Paris              · REQUESTED · cc —
LEDGER  += sequences."2606"=35 · trips."MAC|N728MC|21JUN26|LFPB"="PN2606035"
```
