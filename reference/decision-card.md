# reference/decision-card.md — The Output Contract

> ⚠️ Demo. The single source of truth for **what every Ground Control output looks like**. The spine
> (`rules.md`) fills this; the harness (`eval/run_eval.py`) parses the machine header from it.

## 1. The machine header (always first; 5 lines; machine-parsed)

```
CASE: <id>
DECISION: <HANDLE|ESCALATE|DROP>   INTENT: <NEW|AMENDMENT|FYI|->   OP-STATUS: <OPEN|AMENDED|ESCALATED|DROPPED>   CONFIDENCE: <HIGH|MED|LOW>   REF: <PN###### | {{ASSIGN:PN####-NNN}} | ->
SERVICES: <name=STATUS ...>   (or "-")
ROUTING: <name=queue ...>     (or "-")
REASON: <- | CODE[,CODE ...]>
```

- `CASE:` — the sample/case id (only present in test captures + goldens; omit in live use).
- `SERVICES:` — space-separated `service=STATUS`; STATUS ∈ `status-vocabulary.md` service statuses.
- `ROUTING:` — only services that carry a CC; queue ∈ `procurement` | `accounting` | `accounting-TBC`.
- `REASON:` — `-` for HANDLE; one or more escalation reason codes for ESCALATE; `-` or a route note for DROP.
- `REF:` — per `steps/reference-scheme.md`: a supplied/reused `PN######`, or `{{ASSIGN:PN####-NNN}}`, or `-` (DROP/noise).
- `CONFIDENCE:` — deterministic, tied to the `⛑ FLAGS` block:
  - `HIGH` — every gate read an explicit field or a registry/DB row; nothing was inferred.
  - `MED` — at least one **safe inference** was made (each one named in `⛑ FLAGS`); still HANDLEs.
  - `LOW` — operator / skeleton / services can't be safely resolved → `LOW_CONFIDENCE`, ESCALATE.
  Invariant: `MED` ⇔ FLAGS contains an inference line; `LOW` never reaches a draft.

## 2. The human card — action-board, 3 zones (the machine header above stays unchanged)

Below the 5-line machine header, the output is three zones, not eight sections.

**Zone 1 — Glance** (answers "what is it doing?" in ~8 lines)
- A banner line: `━━ <DECISION> · <INTENT> · <OP-STATUS> · <REF> ━━`
- One trip line: `<operator> · <registry> (<type>) · <stop/leg summary> · POB <pax>/<crew>`
- A `DOING →` list: one numbered line per staged provider email
  (`<ICAO> · <service> → <provider>   <cc note>   (<to-email>)`), then a `→ ack` line for the
  client reply. Omit the `DOING` block entirely on ESCALATE/DROP (nothing is staged) and the `ack`
  line on FYI.
- A `⛑ FLAGS` block (TBC items, standby items, "do not split the trip", etc.; `none` if empty).

**Zone 2 — Drafts** (`▸ DRAFTS — the part a human sends`)
- One draft per in-scope service + the client acknowledgment (Variant A new / B amendment), in one
  of two sanctioned forms:
  - **Full shell** — the filled `templates/` body. Required when a template *decision* is in play:
    multi-service first contact, a template variant choice (hotel A/B, ack A/B), or any draft
    carrying a TBC/FLAGGED detail the human must resolve before release.
  - **Compressed ops-shorthand** — `Subject:` line + a one/two-line body in desk telegraphese.
    Sanctioned for routine requests where **every** template field resolves from a lookup
    (registry/provider DB/airports) and the full shell adds no information; the human expands the
    shell on release (TO/CC and `REF` are already pinned in the `DOING` line and the subject).
  The golden corpus uses the full shell for 02/E02 and shorthand for routine single-anchor cases.

**Zone 3 — Trip record** (`▸ TRIP RECORD`)
- The `reference/operation-artifact.md` block, including the `LEDGER +=` line when a PN was minted.
- The audit trail is **not** in the card. Ground Control emits the `RESULTS +=` rows and the `LOG +=`
  step-trail (Step 8, `reference/logging.md`); the runtime applies them to `state/results.csv` and
  `state/activity-log.md`. Keeping CSV/log out of the card is what makes "each fact appears once" hold —
  provider/to/cc would otherwise be restated a third time here.

The old skeleton table, services-per-leg list, provider-lookup table, and routing-summary table are
**removed** — each fact now appears once: provider/to/cc in the `DOING` list, and
operator/aircraft/itinerary/services in the trip record.

## 3. The operation artifact

Always emitted (full for HANDLE; minimal for ESCALATE/DROP). Schema: `reference/operation-artifact.md`.

## 4. Per-route shape

| route | header REASON | zones present | artifact |
|---|---|---|---|
| HANDLE | `-` | banner + trip line + DOING + FLAGS + DRAFTS + TRIP RECORD | full; `LEDGER +=` if minted |
| FYI | `-` | banner + trip line + FLAGS + TRIP RECORD (service → CONFIRMED) | full; no DOING, no ack, REF reused (no `LEDGER +=`) |
| ESCALATE | reason code(s) | banner + one-line why + the escalation flag (`templates/escalation-flag.md`) | minimal: status ESCALATED, services NOT-CONTACTED |
| DROP | `-` or route note | banner + one-line why | minimal: status DROPPED, services `-` |
