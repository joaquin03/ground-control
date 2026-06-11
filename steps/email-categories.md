# Email Categories (classification reference)

> ⚠️ Demo data. Fictional contacts.

Reference the operator uses to classify an inbound **after the sender is validated** (Step 0,
`rules.md` — machine mail with bulk/bounce/OOO headers is already dropped there). Two questions,
in order; the noise classes below catch what slips past the header markers.

## Question 1 — Is this an operational email at all?

| class | what it looks like | action |
|---|---|---|
| **Operational** | A real trip request/amendment from a known or plausible operator: registry, ICAO, times, services | continue to Question 2 |
| **Noise — marketing** | Newsletters, event invites, promotions, "this week in business aviation" | **DROP** |
| **Noise — automated** | Delivery-failure bounces, out-of-office, read receipts, "do not reply" system mail | **DROP** |
| **Noise — internal/admin** | Internal chatter, invoices to accounting, HR, unrelated CCs | **DROP** (not this operator's job) |
| **Inbound provider confirmation** | A provider replying with a booking/handling confirmation on a live trip | **FYI** — note it, no new outbound |

## Question 2 — Intent of an operational email

| intent | signals | action |
|---|---|---|
| **NEW** | Fresh subject, no `Re:`/`RE:`, new reference or none yet, full trip details | open a new trip → run the full flow |
| **AMENDMENT** | `Re:`/`RE:` on a live thread, words like *change, update, revised, new ETA, please note, correction*, same reference number | update the existing trip → notify affected providers of the delta, re-acknowledge. **Do not open a new trip.** |
| **FYI / ack-only** | "Thanks", "noted", "received", confirmations with no new action | acknowledge internally, no outbound |

### Amendments split further — add vs cancel
An amendment is not one thing. The direction of the change decides the outcome:

| sub-type | signals | action |
|---|---|---|
| **Add service** | "also arrange…", "please add…", a new service on a live trip | **HANDLE** — look up the provider, draft the new request, attach to the existing reference |
| **Change detail** | new ETA/ETD, revised pax, corrected time — same services | **HANDLE** — notify affected providers of the delta, re-acknowledge |
| **Cancel (whole trip)** | "cancel the trip", "scrubbed", "no longer operating" | **ESCALATE** — confirmed work, possible fees, provider notifications → human |
| **Cancel (one booked service)** | "cancel the hotel/transport/catering", "drop the…" | **ESCALATE** — same rule, even partial; touch only the named service |

> **Rule of thumb:** *adding work auto-handles; cancelling confirmed work escalates.* See
> `samples/` (cases E01–E03) for worked examples.

## Subprocess tags (for operational emails)

Tag every operational email with the subprocess(es) it touches. Only A and B are in scope.

| tag | subprocess | in scope |
|---|---|---|
| A | Handling | ✅ |
| B | Ground transport / Hotel / Catering | ✅ |
| C | Permits | ❌ escalate |
| E | Fuel | ❌ escalate |
| D | Flight plan / weather | ❌ escalate |

A single email can carry several tags (e.g. `A + B`). If it carries any of C/D/E as part of the
ask, the whole email escalates so the trip stays together.
