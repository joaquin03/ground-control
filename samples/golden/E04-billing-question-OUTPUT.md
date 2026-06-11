# Edge Output E04 — Billing / invoice question (DROP → accounting)

> ⚠️ Fictional. Golden for `samples/inbound/E04-billing-question.md`. Not an operational request —
> a billing/invoice query routes to accounting and drops from the ops queue.

```
CASE: E04-billing
DECISION: DROP   INTENT: -   OP-STATUS: DROPPED   CONFIDENCE: HIGH   REF: -
SERVICES: -
ROUTING: -
REASON: -
```

━━ DROP ━━
Billing query on invoice INV-4471 (SUMU handling line + VAT) from `accounts@adriaticwings.example` —
a finance question, not a trip request or change. → route to accounting@apextrip.example; dropped
from the ops queue. A real counterparty expects an answer, so it is forwarded, not silently dropped.

▸ TRIP RECORD
```
OPERATION  —   status: DROPPED
operator:  UNKNOWN
services:  NOT-CONTACTED
reason:    not-operational
```
