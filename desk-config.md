# Desk Config

> ⚠️ Demo data. Fictional "Apex Trip Support" desk. **Edit this one file to retarget the whole
> operator** to a different desk — name, domain, and every mailbox the templates and escalation
> rules reference. Nothing else should hard-code an address.

```yaml
desk:
  name: "Apex Trip Support"
  domain: "apextrip.example"
  signature: "APEX TRIP SUPPORT - OPERATIONS"

mailboxes:
  send_from:    "info@apextrip.example"     # all in-scope outbound (handling/ground/hotel/catering)
  archive_bcc:  "info@apextrip.example"     # BCC on every outbound, for the trip record

  cc_procurement: "procurement@apextrip.example"  # CC when the desk's corporate card is used
  cc_accounting:  "accounting@apextrip.example"   # CC for US-Aircard-paid operators

escalation_queues:
  ops_desk:  "ops-desk@apextrip.example"    # default human queue (cancellations, military/state, authority)
  sales:     "sales@apextrip.example"       # unknown / new operators → onboarding
  finance:   "finance@apextrip.example"     # credit HOLD → clear before contacting providers
  permits:   "permits@apextrip.example"     # permit subprocess (out of scope here) → escalate
  fuel_desk: "fuel-desk@apextrip.example"   # fuel subprocess (out of scope here) → escalate
```

## Retargeting checklist

To point this operator at a different desk, change the values above and confirm:
1. `desk.name` / `desk.signature` — appears in every template's `FROM:` and sign-off.
2. `desk.domain` — every mailbox derives from it.
3. `mailboxes.*` and `escalation_queues.*` — referenced by `templates/` and
   `steps/routing-cc-matrix.md`. The templates and matrix should read these keys, not literal
   addresses.

> The templates in this demo show literal `@apextrip.example` addresses for readability. When wiring
> the operator, treat this file as the source of truth and substitute these keys.
