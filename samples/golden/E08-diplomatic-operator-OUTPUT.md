# Edge Output E08 — Diplomatic / state operator (ESCALATE)

> ⚠️ Fictional. Golden for `samples/inbound/E08-diplomatic-operator.md`. State-operator block
> applies equally to diplomatic and military operators.

```
CASE: E08-diplomatic
DECISION: ESCALATE   INTENT: NEW   OP-STATUS: ESCALATED   CONFIDENCE: HIGH   REF: -
SERVICES: -
ROUTING: -
REASON: DIPLOMATIC_OPERATOR
```

━━ ESCALATE · DIPLOMATIC_OPERATOR → ops-desk@apextrip.example ━━

Why (each trigger is sufficient on its own):
  - DIPLOMATIC_OPERATOR — Republic Air Wing is type_of_flight=Diplomatic/State, manages_permits=no; state flights run through government/protocol channels; the desk never auto-handles them — the same rule that blocks military operators (Sample 04).

```
ESCALATION — HUMAN ACTION REQUIRED
==================================
Reason code:   DIPLOMATIC_OPERATOR
Why I stopped: State/diplomatic flight. Handling support for state aircraft is a policy/protocol decision, not an auto-handled provider request.

What I read:
  Operator:    Republic Air Wing (RAW) — Diplomatic/State
  Registry:    RAW-02 (A319CJ)
  Airport:     LEMD
  Movement:    ARRIVAL 23 JUN 0800Z, POB 12 delegation / 6 CREW
  Services asked: handling

What the human needs to decide / supply:
  - Whether the desk supports this state flight, under what protocol arrangement.
  - Coordinate via the appropriate channel — clearance is already with their foreign ministry.

Original email: samples/inbound/E08-diplomatic-operator.md
I drafted nothing. LEMD has a handling provider on file, but the block is on the operator.
```

Route to: ops-desk@apextrip.example

▸ TRIP RECORD
```
OPERATION  —   status: ESCALATED
operator:  Republic Air Wing (RAW)
services:  NOT-CONTACTED
reason:    DIPLOMATIC_OPERATOR
```
