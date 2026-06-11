# Ground Control — an AI Operator for an Executive-Aviation Trip Desk

**🌐 Live demo (landing + ops console):** https://joaquin03.github.io/ground-control/

**▶ Watch it work — walkthrough:** https://www.loom.com/share/58958951bb9b43ef8551d3f29c720b8a

**Why I built this.** I ran an operational discovery for a charter flight-support company — the desk
that arranges everything a private flight needs on the ground (handling, fuel, catering, transport,
crew hotels), one inbound email at a time, across every airport it touches. It's a real client: I ran
the discovery process to bring AI into their operation, and we're waiting to close on the
implementation. Ground Control encodes *that desk's real workflow* — every decision rule, escalation
trigger, and edge case here is one the operation actually runs. The data is synthetic, modeled on the
real operation — the logic is real.

## Quick start
1. Create a Claude Project and add this `ground-control/` folder. It's self-contained.
2. Paste an inbound ops email (or one of `samples/inbound/*`).
3. You get back: a decision card + machine header, the **operation artifact**, the drafted outbound
   email(s), and the client acknowledgment — or an escalation flag with a reason code.


## What it decides
| Route | When | You get |
|-------|------|---------|
| **HANDLE** | in-scope, known operator, complete, clear | operation artifact + provider drafts + client ack |
| **ESCALATE** | cancel · unverified/impersonation/military/diplomatic · credit hold · out-of-scope (permit/fuel/FPL) · no handling anchor · incomplete · low confidence · **injection / spoofed sender** (`reference/trust-boundary.md`) | a clean escalation flag with a reason code |
| **DROP** | noise (newsletter/bounce/OOO/internal), billing, or **unrecognized sender** (off-registry, no impersonation — trust-first, v1) | logged and dropped; nothing reaches your queue |

## The decision spine
Every inbound runs these nine gates in order — the first to fire a route wins (`rules.md`).
- **S0 · Scope filter** — operational, or noise / billing / provider-FYI?
- **S1 · Identify operator** — trust before content: known, authenticated, in good standing? Unknown drops here.
- **S2 · Intent** — NEW · AMENDMENT · FYI. Cancel routes out.
- **S3 · Flight skeleton** — registry, ICAO, times, POB complete?
- **S4 · Detect services** — in-scope only; handling is the anchor.
- **S5 · Provider lookup** — resolve a provider per service + station.
- **S6 · Validate** — credit, providers, skeleton, scope all clear.
- **S7 · Draft + route** — fill templates, set CC, lock recipients, stage for approval.
- **S8 · Decide + open** — mint / reuse REF, set statuses, emit the operation artifact.

## What's in the folder
```
ground-control/
├── CLAUDE.md        the map (read first)
├── identity.md      who I am
├── rules.md         the decision spine
├── examples.md      worked decisions
├── reference/       output contract · operation-artifact schema · escalation triggers · trust boundary
├── steps/           per-step lookup tables + criteria the spine reads
├── templates/       outbound email shells
├── desk-config.md   edit this one file to retarget the operator to another desk
├── samples/         29 inbound emails + golden outputs (incl. the S-series adversarial set)
├── eval/            regression harness — run_eval.py over the 29 cases + check_consistency.py
├── state/           working-dir persistence: PN ledger, results CSV, activity log (what makes it an operator, not a prompt)
└── web/             landing page + operations console — pipeline, status board, human approval queue
```

## Security
Email content is **data, never instructions**. The trust boundary (`reference/trust-boundary.md`) is on at every step:
- **Trust before content.** Unknown / off-registry senders are dropped before their body is read — never analyzed for intent or services.
- **Injection & spoofing escalate, never execute.** Override language, ledger / registry / config tampering, or spoofed / impersonating senders → ESCALATE with the payload quoted in the briefing; nothing is acted on.
- **Exfiltration lock.** Outbound TO/CC resolve **only** from the provider database + `desk-config.md`. An address found in the email body is data, never a destination.
- **Human approval gate.** Every draft is staged in the console's approval queue and released only by a human — the desk never sends on its own.

## Testing it
`python3 eval/run_eval.py --check samples/golden` regression-checks all 29 decisions.
`python3 eval/check_consistency.py` checks folder invariants (no stale paths, ICAO coverage).

Two trust claims you can verify in under a minute:
- **Same email twice → same PN, no duplicate trip.** Minting is idempotent by trip fingerprint
  (`steps/reference-scheme.md`); the ledger recomputes the same number whether or not the commit landed.
- **An email cannot operate the desk.** Paste `samples/inbound/S01-*` — the embedded "system note"
  gets quoted in an escalation briefing, not followed (`reference/trust-boundary.md`).
