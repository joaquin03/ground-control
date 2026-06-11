# Edge Output E09 — Third party "on behalf of" an operator (ESCALATE)

> ⚠️ Fictional. Golden for `samples/inbound/E09-broker-on-behalf.md`. The sender is not the
> operator — authority is unverified, so escalate rather than open a trip.

```
CASE: E09-on-behalf
DECISION: ESCALATE   INTENT: NEW   OP-STATUS: ESCALATED   CONFIDENCE: HIGH   REF: -
SERVICES: -
ROUTING: -
REASON: UNVERIFIED_AUTHORITY
```

━━ ESCALATE · UNVERIFIED_AUTHORITY → ops-desk@apextrip.example ━━

Why (each trigger is sufficient on its own):
  - UNVERIFIED_AUTHORITY — the From: domain globaltripdesk.example is not in the registry and does not match Falcon Crest's domain (falconcrest-exec.example); a matching tail number is not proof the sender is authorised to transact on the account.

```
ESCALATION — HUMAN ACTION REQUIRED
==================================
Reason code:   UNVERIFIED_AUTHORITY
Why I stopped: A non-registered third party is requesting work on a known operator's account. Sender authority cannot be confirmed from the email alone.

What I read:
  Operator:    UNKNOWN (sender: Global Trip Desk — not in registry)
  Registry:    T7-FCX (claims: Falcon Crest Executive)
  Airport:     SUMU
  Movement:    ARRIVAL 24 JUN 1300Z, 4 PAX / 3 CREW
  Services asked: handling

What the human needs to decide / supply:
  - Confirm with Falcon Crest (known contact) that Global Trip Desk is authorised for this trip.
  - If confirmed, hand back for normal handling at SUMU (Plata Handling Services).

Original email: samples/inbound/E09-broker-on-behalf.md
I opened no trip and contacted no provider.
```

Route to: ops-desk@apextrip.example

▸ TRIP RECORD
```
OPERATION  —   status: ESCALATED
operator:  UNKNOWN
services:  NOT-CONTACTED
reason:    UNVERIFIED_AUTHORITY
```
