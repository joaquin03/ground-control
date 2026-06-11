# Template — Client Acknowledgment (reply to the operator)

> ⚠️ Demo template. Fictional data only. Sent back to whoever requested the trip.

**Send from:** `info@apextrip.example`
**To:** `{{OPERATOR_EMAIL}}` (the original sender)
**BCC:** `info@apextrip.example`
**Subject:** `Re: {{ORIGINAL_SUBJECT}}`

---

## Variant A — new request acknowledged
```
HI {{OPERATOR_CONTACT}},

Thank you — we have your request for {{REGISTRY}} at {{ICAO}} ({{DATE_DDMMM}}) under reference {{REF}}.

We are arranging:
{{SERVICES_BULLETS}}

We will revert with provider confirmations shortly. Please send any pending details:
{{PENDING_ITEMS_OR_NONE}}

KIND REGARDS,
APEX TRIP SUPPORT - OPERATIONS
info@apextrip.example
```

## Variant B — amendment acknowledged
```
HI {{OPERATOR_CONTACT}},

Noted on {{REF}} ({{REGISTRY}} / {{ICAO}}). We have updated:
{{CHANGE_SUMMARY}}

We are notifying the affected provider(s): {{AFFECTED_PROVIDERS}}.
Everything else on the trip stays unchanged.

KIND REGARDS,
APEX TRIP SUPPORT - OPERATIONS
```
