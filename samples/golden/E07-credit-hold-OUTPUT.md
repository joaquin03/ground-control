# Edge Output E07 — Operator with credit on HOLD (ESCALATE)

> ⚠️ Fictional. Golden for `samples/inbound/E07-credit-hold.md`. Known operator, but credit_status
> = HOLD → escalate to Finance before any provider is engaged.

```
CASE: E07-credit-hold
DECISION: ESCALATE   INTENT: NEW   OP-STATUS: ESCALATED   CONFIDENCE: HIGH   REF: -
SERVICES: -
ROUTING: -
REASON: NO_CREDIT
```

━━ ESCALATE · NO_CREDIT → finance@apextrip.example (cc ops-desk@apextrip.example) ━━

Why (each trigger is sufficient on its own):
  - NO_CREDIT — Vega Aviation Services is in the registry with credit_status=HOLD; the desk does not contact providers on a held account, even though SBGR handling resolves (Tropic Wings Handling). The block is the account, not the airport.

```
ESCALATION — HUMAN ACTION REQUIRED
==================================
Reason code:   NO_CREDIT
Why I stopped: Operator account is on credit hold. No provider may be engaged until Finance clears it.

What I read:
  Operator:    Vega Aviation Services (VAS) — T4, Private, credit HOLD
  Registry:    N712VA (Challenger 605)
  Airport:     SBGR
  Movement:    ARRIVAL 18 JUN 1700Z from SCEL, POB 2/2
  Services asked: handling

What the human needs to decide / supply:
  - Finance to clear or decline the account for this trip.
  - If cleared, hand back for normal handling at SBGR (Tropic Wings Handling).

Original email: samples/inbound/E07-credit-hold.md
I contacted no provider.
```

Route to: finance@apextrip.example  (cc ops-desk@apextrip.example)

▸ TRIP RECORD
```
OPERATION  —   status: ESCALATED
operator:  Vega Aviation Services (VAS)
services:  NOT-CONTACTED
reason:    NO_CREDIT
```
