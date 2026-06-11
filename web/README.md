# web/ - Ground Control front end

A zero-build static site that **shows the operator method running**. Two pages:

| Page | What it is |
|------|-----------|
| `index.html` | Landing page. Frames the problem (what a trip-support desk is) for a newcomer, explains the operator method (Interpretable Context Methodology), the 9-gate spine, the three routes, and shows the **live regression-harness result** (the real `run_eval.py` output, 29/29 — incl. the S-series adversarial + no-anchor cases). Numbers are read live from the corpus. |
| `console.html` | Operations console. Two views: **Pipeline** (every inbound email, the decision tree it ran with **the actual read at each gate**, the operation opened, the flags raised, and the emails the pipeline staged) and **Status board** (every email processed, escalations by reason, the approval queue, the PN ledger, the audit trail). |

## The human approval gate

Per `reference/trust-boundary.md` (the exfiltration lock + approval gate), **drafts are staged, never sent**. Every HANDLE case
with drafts sits in the console's approval queue as **PENDING APPROVAL** until a human clicks
*Approve & release* (or *Reject & hold*) in the Outbox pane. The ribbon shows the live
awaiting-approval count, the inbox marks each pending case with a gold chip, and the status board
totals pending / released / held. Demo state persists in `localStorage` (clamped to the three known
values before rendering); in a wired desk this gate is where the runtime's send hook lives.

Everything is driven by **real desk data** extracted from `../samples/` and `../state/`.
Nothing is mocked: the inbound emails, decision trees, drafted provider emails, trip
records, and audit rows are the actual artifacts the operator produces.

## Run it

It is fully static. Open `index.html` directly, or serve the folder (recommended, so
relative paths resolve cleanly):

```sh
cd web
python3 -m http.server 8765
# then open http://localhost:8765/index.html
```

`console.html#status` deep-links straight to the status board.

## Regenerate the data

The pages read `data.js` (a `window.GC = {...}` bundle). Rebuild it whenever the
samples, goldens, or state files change:

```sh
python3 web/build_data.py      # writes web/data.js + web/data.json
```

`build_data.py` parses, per case: the inbound email, the golden decision card (machine
header, drafts, trip record, flags), reconstructs the spine path (which gate fired) from
the decision and reason codes, and joins each case to its `state/activity-log.md` entry so
the decision tree can show **what each gate actually read** (`S0 -> ADW (T2, Part 135,
credit OK)`). It also reads `state/results.csv` and `state/pn-ledger.json` for the status
board, and **runs `eval/run_eval.py` live** to capture the real pass result for the landing
page. It only reads the repo files; it never writes to `state/`.

## Files

```
web/
├── index.html        landing page
├── console.html      operations console shell
├── build_data.py     extractor: samples/ + state/  ->  data.js / data.json
├── data.js           generated bundle (window.GC) - committed so the site runs with no build step
├── data.json         same payload, for inspection
└── assets/
    ├── styles.css    design system (dark mission-control; one gold accent; route-state colors)
    ├── landing.js    hero artifact + spine flow + scroll reveals
    └── console.js     inbox, pipeline detail, status board
```

## Notes

- **No build step, no executable third-party scripts.** Only Google Fonts is loaded
  (a stylesheet, with system-font fallbacks in CSS), so the page renders fine offline.
- The em-dashes and middle dots inside the console are **verbatim operator output**
  from the goldens, not page chrome.
- Demo data is fictional; ICAO codes are real public reference data.
