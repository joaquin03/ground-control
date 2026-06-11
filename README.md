# Ground Control — an AI Operator for an Executive-Aviation Trip Desk

> Drop this folder into a Claude Project. Claude becomes **Ground Control**: it reads one inbound ops
> email, **decides** HANDLE / ESCALATE / DROP, and for HANDLE hands you back the **operation opened**
> (services scheduled with per-line status), **every provider draft written**, and **the client reply
> ready to send** — or a clean escalation brief. You come back to work done or correctly flagged, never
> to a question.

**▶ Watch it work — the 90-second walkthrough:** https://www.loom.com/share/58958951bb9b43ef8551d3f29c720b8a

Built with the Clift **Interpretable Context Methodology** (folders as architecture, each file one job).
Fictional "Apex Trip Support" demo data — every operator, provider, and contact is invented; ICAO codes
are real public reference data.

**Why I built this.** I ran an operational discovery for a charter flight-support company — the desk
that arranges everything a private flight needs on the ground (handling, fuel, catering, transport,
crew hotels), one inbound email at a time, across every airport it touches. Ground Control encodes
*that desk's real workflow*: every decision rule, escalation trigger, and edge case here is one the
operation actually runs. The data is anonymized — the logic is real.

## Quick start
1. Create a Claude Project and add this `ground-control/` folder. It's self-contained.
2. Paste an inbound ops email (or one of `samples/inbound/*`).
3. You get back: a decision card + machine header, the **operation artifact**, the drafted outbound
   email(s), and the client acknowledgment — or an escalation flag with a reason code.

It never asks you *"what should I do with this?"* — deciding that **is** its job. It drafts; **a human
sends**. It never cancels confirmed work or contacts an unknown/held/military/diplomatic operator — it
escalates those with a briefing.

## What it decides
| Route | When | You get |
|-------|------|---------|
| **HANDLE** | in-scope, known operator, complete, clear | operation artifact + provider drafts + client ack |
| **ESCALATE** | cancel · unverified/impersonation/military/diplomatic · credit hold · out-of-scope (permit/fuel/FPL) · no handling anchor · incomplete · low confidence · **injection / spoofed sender** (`reference/trust-boundary.md`) | a clean escalation flag with a reason code |
| **DROP** | noise (newsletter/bounce/OOO/internal), billing, or **unrecognized sender** (off-registry, no impersonation — trust-first, v1) | logged and dropped; nothing reaches your queue |

## What's in the folder
| Path | Job |
|------|-----|
| `CLAUDE.md` | the map (read first) |
| `identity.md` · `rules.md` · `examples.md` | who I am · the decision spine · worked decisions |
| `reference/` | the output contract, the operation-artifact schema, the escalation triggers, the trust boundary |
| `steps/` | the per-step lookup tables + criteria the spine reads |
| `templates/` | the outbound email shells |
| `desk-config.md` | edit this one file to retarget the operator to another desk |
| `samples/` | 29 inbound emails + their golden outputs (incl. the S-series adversarial set) |
| `eval/` | the regression harness — `run_eval.py` over the 29 cases + `check_consistency.py` |
| `state/` | the working-directory persistence: PN ledger, results CSV, activity log (what makes it an *operator*, not a prompt) |
| `web/` | the landing page + operations console — pipeline view, status board, and the human approval queue, all driven by the real corpus |

## Testing it
`python3 eval/run_eval.py --check samples/golden` regression-checks all 29 decisions.
`python3 eval/check_consistency.py` checks folder invariants (no stale paths, ICAO coverage).

Two trust claims you can verify in under a minute:
- **Same email twice → same PN, no duplicate trip.** Minting is idempotent by trip fingerprint
  (`steps/reference-scheme.md`); the ledger recomputes the same number whether or not the commit landed.
- **An email cannot operate the desk.** Paste `samples/inbound/S01-*` — the embedded "system note"
  gets quoted in an escalation briefing, not followed (`reference/trust-boundary.md`).

## Why it's built this way (the 60/30/10)
The AI only does the ~10%: reading one email and writing the prose. Every decision input is a lookup —
registry, provider DB, airports, CC matrix, templates, desk config (~60% deterministic assets) — and
every route is a rule: the 9-gate spine, the escalation triggers, the required-fields gate (~30%
rule-based logic). That ratio is the point: the operator is trustworthy because the smallest possible
part of it is improvising.

## The one rule
**When uncertain, escalate — never guess in the client's name.**
