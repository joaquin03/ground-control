# Reference-Number Scheme (PN)

> ⚠️ Demo data. Fictional "Apex Trip Support" desk.

Every trip carries one reference ("PN"). This file defines the format and how the operator mints a
**real, sequential** PN from the working-directory ledger — reproducibly, without a duplicate-trip bug.

## Format

```
PN{YY}{MM}{NNN}
   │   │    └── 3-digit sequence within that month (001–999)
   │   └─────── 2-digit month
   └─────────── 2-digit year
example: PN2606031  →  year 26, month 06, sequence 031
```

## Where the counter lives (working directory)

Ground Control runs **with a working directory** (Claude Code, an agent runtime, or a synced folder).
The counter is `state/pn-ledger.json`:

```json
{ "sequences": { "2606": 30 }, "trips": {} }   // pre-07 state; after minting → 31 + the SJG trip
```

- `sequences` — last `NNN` used per `YYMM` bucket (resets each month).
- `trips` — **fingerprint → PN already assigned** (the idempotency map).

Ground Control **reads** the ledger and **proposes** the increment as a commit line in the operation
artifact; the runtime/human applies it. The operator never writes to a live system itself.

## Trip fingerprint

`fingerprint = <operator_code> | <registry> | <first-leg date DDMMMYY> | <first-leg ICAO>`
e.g. `SJG|M-SJGX|18JUN26|LFPB`. A multi-leg trip uses its **first leg** only → one trip = one PN.

## How the operator obtains the REF (deterministic), in order

1. **REF present in the email / a reply on a live thread → reuse it verbatim.** Never mint on an
   amendment or an FYI confirmation. (Samples 01, 10 carry a PN in the email; 03, E02, E06 reuse a
   thread PN.)
2. **New trip, no REF supplied → mint from the ledger.** Read `state/pn-ledger.json`:
   - fingerprint already in `trips` → **reuse that PN** (no new number).
   - else `YYMM` = the email date's year+month; `next = (sequences[YYMM] or 0) + 1`;
     `PN = "PN" + YYMM + zeropad(next,3)`.
   Then emit the PN **and** the ledger commit line (see `reference/operation-artifact.md`):
   `LEDGER += sequences."2606"=31 · trips."SJG|M-SJGX|18JUN26|LFPB"="PN2606031"`
3. **No ledger file / empty bucket → first trip of the month is `…001`.** Still emit the commit line.

This is idempotent: the same email yields the same PN whether or not the commit was applied yet
(unchanged counter recomputes the same `next`; an applied commit hits the fingerprint and reuses).

## Instruction to any validation / audit harness

When checking REF, **wildcard the sequence**. Treat REF as a match against:

```
PN\d{7}                  (a supplied, reused, or minted PN — YY MM NNN)
{{ASSIGN:PN\d{4}-NNN}}   (legacy placeholder — still accepted for back-compat)
```

Do **not** assert an exact minted sequence (it depends on ledger state). Assert that (a) amendments /
FYI reuse the inbound/thread REF unchanged, and (b) new trips either reuse a supplied REF or mint a
valid `PN\d{7}` from the ledger.
