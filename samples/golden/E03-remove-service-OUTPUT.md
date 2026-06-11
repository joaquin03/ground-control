# Edge Output E03 — Remove / cancel a booked service (ESCALATE)

> ⚠️ Fictional. Golden for `samples/inbound/E03-remove-service.md`. Same rule as a whole-trip
> cancellation: cancelling confirmed work escalates — even partial cancellations.

```
CASE: E03-remove-service
DECISION: ESCALATE   INTENT: AMENDMENT   OP-STATUS: ESCALATED   CONFIDENCE: HIGH   REF: -
SERVICES: -
ROUTING: -
REASON: CANCELLATION
```

━━ ESCALATE · CANCELLATION → ops-desk@apextrip.example ━━

Why (each trigger is sufficient on its own):
  - CANCELLATION (partial) — the 4 hotel rooms on PN2606031 were a confirmed booking under a corporate card; cancelling may incur a hotel fee and needs a human to action with the property. Adding work auto-handles; cancelling confirmed work does not.

```
ESCALATION — HUMAN ACTION REQUIRED
==================================
Reason code:   CANCELLATION
Why I stopped: Operator asked to cancel 4 confirmed hotel rooms. Possible cancellation fee and the property must be contacted by a human.

What I read:
  Operator:    Adriatic Wings (ADW) — T2, credit OK
  Registry:    9H-ADW
  Airport:     LEMD
  Movement:    departure 14 JUN — PN2606031 live
  Services asked: cancel 4 rooms at Hotel Borealis Madrid (partial — handling/transport/catering stand)

What the human needs to decide / supply:
  - Contact Hotel Borealis Madrid to release the 4 rooms; capture any fee.
  - Confirm back to the operator. Leave handling / transport / catering untouched.

Original email: samples/inbound/E03-remove-service.md
I cancelled nothing. The hotel has not been contacted.
```

Route to: ops-desk@apextrip.example

▸ TRIP RECORD
```
OPERATION  —   status: ESCALATED
operator:  Adriatic Wings (ADW)
services:  NOT-CONTACTED
reason:    CANCELLATION
```
