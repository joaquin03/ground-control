# Edge Output E10 — Hotel-only, no handling anchor (ESCALATE)

> ⚠️ Fictional. Golden for `samples/inbound/E10-solaris-hotel-only.md`. Known operator, complete
> hotel fields — but no handling on the email, no live trip thread, and Solaris is not a
> full-service account. The anchor rule (`steps/service-catalog.md`) escalates: there is no
> operation to attach the service to, and opening a serviceless operation invents one.

```
CASE: E10-no-anchor
DECISION: ESCALATE   INTENT: NEW   OP-STATUS: ESCALATED   CONFIDENCE: HIGH   REF: -
SERVICES: -
ROUTING: -
REASON: NO_ANCHOR_SERVICE
```

━━ ESCALATE · NO_ANCHOR_SERVICE → ops-desk@apextrip.example ━━

Why (each trigger is sufficient on its own):
  - NO_ANCHOR_SERVICE — hotel is asked with no handling and no live thread, and Solaris's registry default_services is handling only (not a full-service account). Every hotel hard-field is present; the block is the missing anchor, not missing detail.

```
ESCALATION — HUMAN ACTION REQUIRED
==================================
Reason code:   NO_ANCHOR_SERVICE
Why I stopped: A secondary service (hotel) with no operation to attach it to. Handling is
               the anchor; I don't open a serviceless trip on my own call.

What I read:
  Operator:    Solaris Jet Group (SJG, T2, credit OK)
  Registry:    — (no movement on this request; crew positioning commercially)
  Airport:     LEMD (hotel near Barajas)
  Movement:    — (rooms only, 21–23 JUN)
  Services asked: hotel — 2 rooms, 2 named crew, check-in 21 JUN, check-out 23 JUN, 4–5 star near airport

What the human needs to decide / supply:
  - Open a standalone hotel-only operation for SJG deliberately, or decline/redirect.
  - If the stay belongs to an upcoming SJG trip, attach it when the handling request arrives.
  - All hotel hard-fields are already captured above — nothing further to collect from the operator.

Original email: samples/inbound/E10-solaris-hotel-only.md
I drafted nothing. No provider or client has been contacted.
```

Route to: ops-desk@apextrip.example

▸ TRIP RECORD
```
OPERATION  —   status: ESCALATED
operator:  Solaris Jet Group (SJG)
services:  NOT-CONTACTED
reason:    NO_ANCHOR_SERVICE
```
