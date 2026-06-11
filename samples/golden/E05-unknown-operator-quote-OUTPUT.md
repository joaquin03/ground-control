# Edge Output E05 — Unrecognized off-registry sender, first-time quote (ESCALATE)

> ⚠️ Fictional. Golden for `samples/inbound/E05-unknown-operator-quote.md`. Trust before content: an
> off-registry sender with **no impersonation signal** escalates at Step 1 (identify) — **content-blind**,
> before intent or services are ever analysed. A stranger is a potential client, not noise: sales
> onboards and credit-checks before any provider is contacted.

```
CASE: E05-unknown-operator
DECISION: ESCALATE   INTENT: -   OP-STATUS: ESCALATED   CONFIDENCE: HIGH   REF: -
SERVICES: -
ROUTING: -
REASON: UNKNOWN_OPERATOR
```

━━ ESCALATE · UNKNOWN_OPERATOR → sales@apextrip.example ━━

Why (each trigger is sufficient on its own):
  - UNKNOWN_OPERATOR — sender domain `horizonjets.example` is not in `operator-registry.csv`: no tier, credit, or account on file, and no impersonation signal (the display name claims no one else). The desk transacts only with onboarded operators — escalated content-blind, before any intent or service analysis.

```
ESCALATION — HUMAN ACTION REQUIRED
==================================
Reason code:   UNKNOWN_OPERATOR
Why I stopped: Off-registry sender — no account, tier, or credit standing on file. I do not analyse
               or act on email from operators we don't transact with; onboarding is a sales decision,
               not an ops one.

What I read (envelope only — content not analysed):
  Sender domain:   horizonjets.example (NOT in operator-registry.csv; no impersonation signal)
  Subject line:    Handling feasibility — EGGW 20 JUN — Falcon 7X
  Original email:  quoted below for sales, unparsed

What the human needs to decide / supply:
  - Whether to onboard Horizon Jets: registry entry, tier, credit check, payment profile.
  - Until onboarded, no feasibility answer or pricing leaves the desk.
  - I built no skeleton, contacted no provider, and quoted no price.

Original email: samples/inbound/E05-unknown-operator-quote.md
I drafted nothing. EGGW has a handling provider on file, but the block is on the sender.
```

Route to: sales@apextrip.example

▸ TRIP RECORD
```
OPERATION  —   status: ESCALATED
operator:  UNKNOWN (off-registry: horizonjets.example)
services:  NOT-CONTACTED
reason:    UNKNOWN_OPERATOR
```
