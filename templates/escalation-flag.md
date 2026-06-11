# Template — Escalation Flag (internal, for a human)

> ⚠️ Demo template. Fictional data only. This is NOT sent to a provider or client — it is the
> structured hand-off the operator produces instead of acting, when a rule says "do not auto-handle".

**Route to:** `{{ESCALATION_QUEUE}}` (e.g. ops-desk@ / sales@ / permits@ / fuel-desk@ — pick per reason)
**Subject:** `[ESCALATE] {{REGISTRY}} | {{ICAO}} | {{ONE_LINE_REASON}}`

---

```
ESCALATION — HUMAN ACTION REQUIRED
==================================
Reason code:   {{REASON_CODE}}        (e.g. MILITARY_OPERATOR, DIPLOMATIC_OPERATOR,
                                       OUT_OF_SCOPE_SUBPROCESS, NO_CREDIT, UNKNOWN_OPERATOR,
                                       UNVERIFIED_AUTHORITY, UNVERIFIED_SENDER,
                                       SUSPECTED_INJECTION, NO_ANCHOR_SERVICE,
                                       INCOMPLETE_SKELETON, CANCELLATION, LOW_CONFIDENCE)
Why I stopped: {{PLAIN_LANGUAGE_REASON}}

What I read:
  Operator:    {{OPERATOR_NAME_OR_UNKNOWN}}
  Registry:    {{REGISTRY_OR_UNKNOWN}}
  Airport:     {{ICAO_OR_UNKNOWN}}
  Movement:    {{ARR_DEP_OR_UNKNOWN}} {{DATE_TIME_OR_UNKNOWN}}
  Services asked: {{SERVICES_OR_UNKNOWN}}

What the human needs to decide / supply:
  - {{ACTION_1}}
  - {{ACTION_2}}

Original email: {{INBOUND_FILENAME_OR_THREAD_REF}}
I drafted nothing. No provider or client has been contacted.
```
