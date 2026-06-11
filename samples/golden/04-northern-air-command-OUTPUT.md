# Sample Output 04 — Military operator + permit (ESCALATE)

> ⚠️ Fictional. Golden for `samples/inbound/04-northern-air-command-military.md`. Two independent
> escalation triggers fire. The operator drafts nothing and routes a clean flag.

```
CASE: 04-northern-air-command
DECISION: ESCALATE   INTENT: NEW   OP-STATUS: ESCALATED   CONFIDENCE: HIGH   REF: -
SERVICES: -
ROUTING: -
REASON: MILITARY_OPERATOR,OUT_OF_SCOPE_SUBPROCESS
```

━━ ESCALATE · MILITARY_OPERATOR + OUT_OF_SCOPE_SUBPROCESS → ops-desk@apextrip.example ━━

Why (each trigger is sufficient on its own):
  - MILITARY_OPERATOR — Northern Air Command is type_of_flight=Military, manages_permits=no; state aircraft run through government channels, not this desk.
  - OUT_OF_SCOPE_SUBPROCESS — the ask includes an overflight permit (subprocess C), which this desk does not handle.

```
ESCALATION — HUMAN ACTION REQUIRED
==================================
Reason code:   MILITARY_OPERATOR,OUT_OF_SCOPE_SUBPROCESS
Why I stopped: Military/state operator and the request includes an overflight permit. Neither is auto-handled by this desk.

What I read:
  Operator:    Northern Air Command (NAC)
  Registry:    NAF-204 (C-17 type)
  Airport:     SCEL
  Movement:    tech stop 15 JUN
  Services asked: handling + overflight permit

What the human needs to decide / supply:
  - Whether the desk provides handling-only support for state aircraft (policy call).
  - Route the permit/clearance through the appropriate government channel — not via provider email.

Original email: samples/inbound/04-northern-air-command-military.md
I drafted nothing. No provider or client has been contacted.
```

Route to: ops-desk@apextrip.example

▸ TRIP RECORD
```
OPERATION  —   status: ESCALATED
operator:  Northern Air Command (NAC)
services:  NOT-CONTACTED
reason:    MILITARY_OPERATOR,OUT_OF_SCOPE_SUBPROCESS
```
