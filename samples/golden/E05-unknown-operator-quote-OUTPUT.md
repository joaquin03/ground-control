# Edge Output E05 — Unrecognized off-registry sender, first-time quote (DROP)

> ⚠️ Fictional. Golden for `samples/inbound/E05-unknown-operator-quote.md`. v1 trust-first: an
> off-registry sender with **no impersonation signal** is dropped at Step 1 (identify) — before intent
> or services are ever analysed. Logged for sales triage; the desk transacts only with onboarded operators.

```
CASE: E05-unknown-operator
DECISION: DROP   INTENT: -   OP-STATUS: DROPPED   CONFIDENCE: HIGH   REF: -
SERVICES: -
ROUTING: -
REASON: UNKNOWN_OPERATOR
```

━━ DROP · UNKNOWN_OPERATOR ━━
Off-registry sender `ops@horizonjets.example` — not in `operator-registry.csv`, no tier / credit /
account on file, and no impersonation signal (the display name claims to be no one else). Dropped at
Step 1, before any intent or service analysis: no skeleton built, no provider contacted, no price
quoted. Logged for sales triage (→ sales: unrecognized sender). The desk transacts only with onboarded
operators; a genuine prospect is recoverable from the drop log, not handled on an unverified first email.
