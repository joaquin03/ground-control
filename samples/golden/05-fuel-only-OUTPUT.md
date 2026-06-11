# Sample Output 05 — Fuel-only request (ESCALATE)

> ⚠️ Fictional. Golden for `samples/inbound/05-fuel-only-request.md`. A known, good-standing
> operator triggers escalation on the subprocess, not the operator. Fuel is out of scope.

```
CASE: 05-fuel-only
DECISION: ESCALATE   INTENT: NEW   OP-STATUS: ESCALATED   CONFIDENCE: HIGH   REF: -
SERVICES: -
ROUTING: -
REASON: OUT_OF_SCOPE_SUBPROCESS
```

━━ ESCALATE · OUT_OF_SCOPE_SUBPROCESS → fuel-desk@apextrip.example ━━

Why (each trigger is sufficient on its own):
  - OUT_OF_SCOPE_SUBPROCESS — the only ask is fuel uplift (subprocess E), which uses a multi-broker comparative-quote process, not a single-provider email; not handled here.

```
ESCALATION — HUMAN ACTION REQUIRED
==================================
Reason code:   OUT_OF_SCOPE_SUBPROCESS
Why I stopped: The only service requested is fuel, which goes through the comparative-quote process, not this desk's single-provider handling flow.

What I read:
  Operator:    Meridian Air Charter (MAC) — T2, credit OK
  Registry:    N512MC (Challenger 350)
  Airport:     KMIA
  Movement:    16 JUN
  Services asked: fuel uplift ~1,800 USG JET A1

What the human needs to decide / supply:
  - Run the fuel comparative (multi-broker) for KMIA, 16 JUN, ~1,800 USG.
  - Confirm whether any handling is needed (operator says handling is arranged direct).

Original email: samples/inbound/05-fuel-only-request.md
I drafted nothing.
```

Route to: fuel-desk@apextrip.example

▸ TRIP RECORD
```
OPERATION  —   status: ESCALATED
operator:  Meridian Air Charter (MAC)
services:  NOT-CONTACTED
reason:    OUT_OF_SCOPE_SUBPROCESS
```
