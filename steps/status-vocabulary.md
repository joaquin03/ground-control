# Status Vocabulary

> ⚠️ Demo data. Fictional "Apex Trip Support" desk.

The one-shot output card is a *snapshot*; a real operation has a **lifecycle**. This file defines
the only legal statuses, so "what's the state of this trip / this service?" has a deterministic
answer the operator can report and a harness can assert against.

## Operation status (one per reference / PN)

| status | meaning | set when |
|---|---|---|
| `OPEN` | A trip exists and is being worked: services requested, awaiting confirmations | a HANDLE outcome on a new request |
| `AMENDED` | An OPEN trip changed (time/detail/added service); deltas pushed to affected providers | a HANDLE outcome on an amendment |
| `ESCALATED` | Handed to a human; the operator took no provider action | any ESCALATE outcome |
| `DROPPED` | Not operational (noise) or routed out (e.g. billing); no trip opened | any DROP outcome |
| `CLOSED` | terminal — all services confirmed and the movement is complete; charges reconciled | set by a **human**, post-movement — closing a trip is outside this operator's loop by design (it never closes its own work) |

> An operation is never two of these at once. `AMENDED` returns to effectively-OPEN behaviour; it is
> a marker that a change was processed, not a parallel state.

## Service status (one per service line within a trip)

| status | meaning |
|---|---|
| `REQUESTED` | An outbound request was drafted/sent to the provider; awaiting their confirmation |
| `CONFIRMED` | The provider confirmed (e.g. an inbound confirmation like Edge E06) |
| `TBC` | A required detail is missing before the request can go out (e.g. hotel reservations email unknown) |
| `INBOUND-PENDING` | Provider is `inbound_only` (e.g. Drivex) → booked via their own channel; the desk did not send a request and is waiting on their confirmation |
| `FLAGGED` | Needs a human — no provider on file for this ICAO+service, or a rule blocks an automatic request |
| `NOT-CONTACTED` | No action taken — the trip was escalated/dropped, so providers were never engaged |

## How the sample outputs map to these statuses

| sample | operation | service statuses |
|---|---|---|
| 01 falconcrest | OPEN | handling `REQUESTED`, transport `REQUESTED` |
| 02 adriatic full | OPEN | handling/ground/catering `REQUESTED`, hotel `TBC` (reservations email unknown) |
| 03 eta amendment | AMENDED | handling `REQUESTED` (re-confirm), transport `REQUESTED` (re-time) |
| 07 multi-leg | OPEN | LFPB handling/ground `REQUESTED`, EGGW handling `REQUESTED` |
| 08 kteb | OPEN | handling `REQUESTED`, transport `INBOUND-PENDING` (Drivex) |
| 12 eggw | OPEN | handling `REQUESTED`, catering `FLAGGED` (no provider on file) |
| 04 / 05 / E01 / E03 / E05 / E07 / E08 / E09 | ESCALATED | all services `NOT-CONTACTED` |
| E06 provider confirm | OPEN | handling `CONFIRMED` |
| 06 noise / E04 billing | DROPPED | — |

This is what lets the operator answer "schedule the services" with a real per-line state instead of
a flat list.
