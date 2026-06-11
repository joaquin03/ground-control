# Edge Output E01 — Whole-trip cancellation (ESCALATE)

> ⚠️ Fictional. Golden for `samples/inbound/E01-trip-cancellation.md`. Cancelling confirmed work
> always escalates — the operator never silently cancels provider relationships.

```
CASE: E01-cancel-trip
DECISION: ESCALATE   INTENT: AMENDMENT   OP-STATUS: ESCALATED   CONFIDENCE: HIGH   REF: -
SERVICES: -
ROUTING: -
REASON: CANCELLATION
```

━━ ESCALATE · CANCELLATION → ops-desk@apextrip.example ━━

Why (each trigger is sufficient on its own):
  - CANCELLATION — PN2606014 is a confirmed trip with providers already engaged (Plata Handling, Costa Chauffeur); cancelling touches money and provider relationships, and may incur a last-minute fee (<48h out). A human owns this.

```
ESCALATION — HUMAN ACTION REQUIRED
==================================
Reason code:   CANCELLATION
Why I stopped: Operator asked to cancel a confirmed trip <48h out. Provider notifications and any cancellation fees are a human decision.

What I read:
  Operator:    Falcon Crest Executive (FCX) — T1, credit OK
  Registry:    T7-FCX
  Airport:     SUMU
  Movement:    confirmed trip — cancel requested <48h out
  Services asked: cancel PN2606014 in full (providers: Plata Handling, Costa Chauffeur)

What the human needs to decide / supply:
  - Confirm cancellation and notify Plata Handling + Costa Chauffeur.
  - Determine whether a last-minute fee applies and advise the operator ("let us know if owed").

Original email: samples/inbound/E01-trip-cancellation.md
I drafted no cancellations. Providers have not been told yet.
```

Route to: ops-desk@apextrip.example

▸ TRIP RECORD
```
OPERATION  —   status: ESCALATED
operator:  Falcon Crest Executive (FCX)
services:  NOT-CONTACTED
reason:    CANCELLATION
```
