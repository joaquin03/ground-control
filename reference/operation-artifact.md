# reference/operation-artifact.md — The Operation Record

> ⚠️ Demo. The "created operation / scheduled services" as a **commit-ready block** — what a human (or
> a future write-tool) applies. Read-only by design: Ground Control drafts this; it never writes to a system.

## Shape (HANDLE)

```
OPERATION  <REF>   status: <OPEN|AMENDED>
operator:  <name> (<code>) · <tier> · <type_of_flight> · credit <OK|HOLD>
aircraft:  <registry> · <type> · <callsign>
itinerary:
  - <ARRIVAL|DEPARTURE>  <ICAO>  <DDMMM> <TIME>Z <→ TO_ICAO | ← FROM_ICAO>   POB <pax>/<crew>
services:
  - <category>  · <provider | operator-named | —>  · <SERVICE-STATUS>  · cc <queue|—>
LEDGER += sequences."<YYMM>"=<n> · trips."<fingerprint>"="<PN>"
flags:
  - <free text, one per line; omit the block if none>
```

## Shape (ESCALATE / DROP — minimal)

```
OPERATION  <REF|—>   status: <ESCALATED|DROPPED>
operator:  <name|UNKNOWN>
services:  NOT-CONTACTED
reason:    <REASON_CODE(s) | not-operational>
```

## Field rules
- `status` and every service `SERVICE-STATUS` are drawn **only** from `steps/status-vocabulary.md`.
- `<REF>` follows `steps/reference-scheme.md` (reuse supplied/thread PN; else mint from `state/pn-ledger.json`).
- `cc <queue>` mirrors the header `ROUTING:` line (`procurement` / `accounting` / `accounting-TBC` / `—`).
- A multi-airport trip lists one `itinerary` line per leg and groups `services` by station in the note.
- `LEDGER +=` is present **only when a new PN was minted** (a NEW trip with no supplied/thread REF).
  Omit it when the REF was reused (amendments, FYI confirmations, emails that carried a PN). Format
  and fingerprint follow `steps/reference-scheme.md`.
- `RESULTS +=` / `LOG +=` are **not** part of this artifact or the card. They are the audit trail,
  emitted separately to `state/results.csv` + `state/activity-log.md` per `reference/logging.md`.
