# steps/ — What Each Step Reads

> Each file owns the data and criteria for one step of `rules.md` (the spine sequences them). `airports.csv`
> is a **shared lookup** (used inside the extract/lookup steps), not its own step.

| File | Owns (the "one job") | rules.md step |
|------|----------------------|---------------|
| `email-categories.md` | operational? · new/amendment/FYI | 0–1 |
| `operator-registry.csv` | who the sender is: tier · credit · flight type · permits · payment_profile | 2 |
| `airports.csv` | ICAO reference + UTC offset (shared lookup) | 3, 5 |
| `required-fields.md` | the minimum-complete skeleton per service (drives INCOMPLETE_SKELETON) | 3, 6 |
| `service-catalog.md` | in-scope vs out-of-scope service categories | 4 |
| `provider-database.csv` | ICAO × service → provider/email/payment/inbound_only | 5 |
| `routing-cc-matrix.md` | who sends / who is CC'd + escalation queue mapping | 7 |
| `reference-scheme.md` | how to mint/reuse the PN reference | 8 |
| `status-vocabulary.md` | the legal operation + service statuses | 8 |

Addresses are **not** here — they live in `../desk-config.md` (the retargeting knob).

## How to add or edit a step

The spine (`rules.md`) is a fixed sequence; each step delegates its data + criteria to one file here.

**To edit a step**, change only its owning file (the table above says which) — e.g. add an operator to
`operator-registry.csv`, a provider to `provider-database.csv`, a status to `status-vocabulary.md`,
an airport to `airports.csv`. Don't touch `rules.md` for a data change. Then re-run the harness from
the project root:

```sh
python3 eval/run_eval.py --check samples/golden   # all 29 cases must still PASS
python3 eval/check_consistency.py                 # exit 0
```

**To add a new step:**
1. Create `steps/<name>.md` (or `.csv`) that owns **exactly one job** — the data + criteria for one
   decision. One file = one job; if it's doing two things, split it.
2. Add a row to the table above (file · the "one job" · which `rules.md` step it serves).
3. Wire it into `rules.md`: insert the step in the sequence and point it at the new file. Keep the
   **escalation-first** order — the first gate that fires a route wins.
4. If it changes the output, update `reference/decision-card.md` (the contract); if it adds a service
   status, update `steps/status-vocabulary.md`; if it adds an audited action, update
   `reference/logging.md`.
5. Add or refresh a golden in `samples/golden/` **and** a case row in `eval/cases.jsonl` so the harness
   covers the new behaviour. Re-run the two commands above until green.

> Never hard-code an address in a step file — addresses resolve only from `../desk-config.md`.
