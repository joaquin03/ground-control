# eval/ — Ground Control Regression + Consistency Harness

One harness, two layers. Re-run after **any** edit to `rules.md`, `steps/`, `reference/`, or `templates/`.

## Regression (`run_eval.py`)
Two layers per golden — **both** must pass:
1. **Machine header** — pins each of the 29 cases (`cases.jsonl`, incl. the S-series adversarial /
   prompt-injection + external-sender set per `reference/trust-boundary.md`) to its expected DECISION · INTENT ·
   OP-STATUS · SERVICE-STATUSES · ROUTING (CC) · REASON. REF is wildcarded per `steps/reference-scheme.md`.
2. **Card body** (`cardbody.py`) — the 3-zone action-board contract (`reference/decision-card.md`):
   banner + the per-route zones present, the retired 8-section markers absent, and the audit appends
   (`RESULTS +=` / `LOG +=`) absent from the card (they live in `state/`; only `LEDGER +=` stays).
   This is what stops the body from drifting from the contract while the header still reads green.

- `python3 run_eval.py --list` — list case ids.
- `python3 run_eval.py --check ../samples/golden` — check every golden (exit 1 on any FAIL).
- `python3 run_eval.py <capture.md>` — check one captured run (start the file with `CASE: <id>`).

**Soft assertions** (printed, you eyeball): provider-correct · cc-correct · no-fabrication ·
required-fields · distinct-read · on-voice.

## Consistency (`check_consistency.py`)
Folder invariants: **no real-system refs** (`check_no_pike`), no stale legacy-path refs
(`check_stale_paths`), ICAO coverage (`check_icao_coverage`), and the relocated audit fixture
(`check_results_schema`: `state/results.csv` exists with the `reference/logging.md` column order).
`python3 check_consistency.py` — exits 1 on any problem.

## Unit tests (the harness's own code)
`python3 test_headers.py && python3 test_refmatch.py && python3 test_differ.py && python3 test_cardbody.py && python3 test_consistency.py`

## The discipline
A failing case means **fix the rule, not the test.** Captures in `runs/` are disposable evidence.
