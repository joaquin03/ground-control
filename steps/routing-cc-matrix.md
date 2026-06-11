# Routing & CC Matrix

> ⚠️ Demo data. Fictional "Apex Trip Support" desk. Addresses resolve from `desk-config.md`.

The deterministic answer to "where does this go and who is copied?" One source of truth for both the
outbound requests and the escalation hand-offs.

## Every in-scope outbound

- **From** = `desk.send_from` (info@)
- **BCC** = `desk.archive_bcc` (info@) — always, for the trip record

## CC rules (evaluate all — a request can carry more than one CC)

| # | condition | CC | reads from |
|---|---|---|---|
| 1 | provider `payment_type = CREDIT_CARD` (desk's corporate card is used) | `cc_procurement` (procurement@) + attach card | `provider-database.csv` |
| 2 | airport `country = United States` **and** operator `payment_profile = AIRCARD` | `cc_accounting` (accounting@) | `airports.csv` + `operator-registry.csv` |
| 3 | airport `country = United States` **and** operator `payment_profile = UNKNOWN` | `cc_accounting` **marked TBC — verify before sending** | same |
| 4 | provider is new / first contact (optional) | `cc_procurement` | — |

> Rule 2 is the fix for the old terrain crack: whether an operator pays via US Aircard is now a
> column (`payment_profile`), not a free-text provider note. Rule 3 is the safety net — when it's
> unknown, the operator does **not** guess; it marks the accounting@ CC as TBC.

### Worked checks against the samples
- **01** ground transport (Costa Chauffeur, `CREDIT_CARD`) → CC procurement@ (rule 1). SUMU is not
  US → no accounting@ CC.
- **08** KTEB handling (US station) + Meridian `payment_profile = CREDIT` → rule 2 **not** triggered
  → no accounting@ CC. Deterministic, no guess.
- *Hypothetical* US-Aircard operator at KMIA → CC accounting@ (rule 2).
- *Hypothetical* operator with `payment_profile = UNKNOWN` at KTEB → CC accounting@ **TBC** (rule 3).

## Escalation routing (no provider contacted)

Map the escalation reason code → queue (`desk-config.md` → `escalation_queues`).

| reason code | queue |
|---|---|
| `CANCELLATION` | ops_desk |
| `MILITARY_OPERATOR` / `DIPLOMATIC_OPERATOR` | ops_desk |
| `UNVERIFIED_AUTHORITY` | ops_desk |
| `UNVERIFIED_SENDER` / `SUSPECTED_INJECTION` | ops_desk (trust boundary — `reference/trust-boundary.md`) |
| `UNKNOWN_OPERATOR` | sales |
| `NO_CREDIT` | finance (cc ops_desk) |
| `OUT_OF_SCOPE_SUBPROCESS` = permit | permits |
| `OUT_OF_SCOPE_SUBPROCESS` = fuel | fuel_desk |
| `NO_ANCHOR_SERVICE` | ops_desk |
| `INCOMPLETE_SKELETON` | ops_desk — or reply to the operator for the missing field |
| billing / not-operations (DROP → route-out) | accounting |
