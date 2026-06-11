# reference/logging.md — Activity Log & Results CSV

> ⚠️ Demo. Two append-only records Ground Control keeps in the working directory so every decision is
> auditable. Like the PN ledger, Ground Control **emits** the append lines; the runtime applies them.
> It never writes to a live system itself.

## state/results.csv — one row per ACTION (not per email)

An email can carry several actions (case 07: 3 provider drafts + 1 ack across 2 airports). Each
action is its own row, tied to the trip by `ref`. Fixed column order:

```
timestamp,ref,from,subject,leg,action,provider,to,cc,status,decision,note
```

| column | value |
|---|---|
| timestamp | processing date, `DDMMMYYYY` (from the email date) |
| ref | the PN, or `-` for ESCALATE/DROP with no REF |
| from | sender domain |
| subject | inbound subject (quote the field if it contains a comma) |
| leg | ICAO the action is at, or `-` (ack / escalation / drop) |
| action | `handling` / `ground_transport` / `hotel` / `catering` / `client_ack` / `escalation` / `drop` |
| provider | provider name, operator name (on a `client_ack`), `UNKNOWN`, or `-` |
| to | recipient email, or `-` |
| cc | `procurement` / `accounting` / `accounting-TBC` / `-` |
| status | service status from `steps/status-vocabulary.md` (REQUESTED / CONFIRMED / TBC / INBOUND-PENDING / FLAGGED / NOT-CONTACTED); `DRAFTED` for a `client_ack`; `DROPPED` for a `drop` row |
| decision | `HANDLE` / `ESCALATE` / `DROP` |
| note | short free text (e.g. `card attached`, a reason code, a flag); quote the field if it contains a comma |

Rows per route:
- **HANDLE / FYI** → one row per in-scope service + one `client_ack` row (FYI has no ack row).
- **ESCALATE** → one `escalation` row, status `NOT-CONTACTED`, note = reason code(s).
- **DROP** → one `drop` row, status `DROPPED`, note = the route note or `not-operational`.

## state/activity-log.md — one entry per EMAIL (the step trail)

Lets you validate the operator followed the spine. One entry per inbound, newest appended at the end:

```
## <DDMMMYYYY> · <REF|—> · <registry|—> · <operator|UNKNOWN>
inbound: "<subject>"
spine:  S0 <operator/credit> · S1 <scope> · S2 <intent> · S3 <skeleton>
        S4 <services> · S5 <providers> · S6 <validate> · S7 <drafts> · S8 <decision>
actions: <N>  (→ results.csv rows for <REF>)
flags:  <flags, or none>
```

For ESCALATE/DROP the trail stops at the gate that fired (e.g. `S0 operator: MILITARY → ESCALATE`)
and `actions: 0`.

## How Ground Control emits them (Step 8)

At Step 8, after the operation artifact, Ground Control emits — for the runtime, **not** inside the
human card — one `RESULTS +=` line per action and one `LOG +=` step-trail entry:

```
RESULTS += <one csv row per action>
LOG += <the activity-log entry above>
```

The runtime appends the `RESULTS +=` rows to `state/results.csv` and the `LOG +=` block to
`state/activity-log.md` — the same propose-then-apply pattern as `LEDGER +=`, but kept **out of the
card**: the card already shows provider/to/cc once (in `DOING`) and the trip once (in `TRIP RECORD`),
so repeating them there as CSV would break "each fact, one place". The expected state after the sample
corpus is committed at `state/results.csv` + `state/activity-log.md`. The `ref` column joins a trip's
action rows to its log entry.
