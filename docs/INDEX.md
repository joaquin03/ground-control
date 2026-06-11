> 📦 **Archived design note.** This described the original `Dataset/` layout. The operator now lives one
> level up: data → `../steps/`, templates → `../templates/`, samples → `../samples/`. See `../CLAUDE.md`.
> Last updated: 10 JUN 2026 — corpus counts refreshed (27 cases: 14 core + E01–E10 + S01–S03).

# Dataset Index — Apex Trip Support (demo)

> ⚠️ **Demo data.** Fictional executive-aviation trip-support desk. Every operator, provider,
> contact, registration, and reference number is invented. ICAO airport codes are real public
> reference data. Nothing here is a live mailbox.

This folder is the **dataset** an email-operator agent reads from. It does **not** contain the
agent's brain (identity / rules / examples / how-to) — that gets built on top of this. This is the
data, the templates, the example emails, the example responses, and the design notes.

## What the operator does (so the data makes sense)

Reads an inbound ops email → decides **HANDLE / ESCALATE / DROP** → for HANDLE, drafts the outbound
provider request(s) + a reply to the sender, with the right CC line. Scope is **Handling** plus
**Ground transport / Hotel / Catering**. Permits, fuel and flight planning are detected and
escalated, never attempted. Full reasoning in [`brainstorm.md`](brainstorm.md).

## Contents

```
ground-control/
├── docs/INDEX.md                 ← you are here (data dictionary + map)
├── docs/brainstorm.md            ← what the naive 5-step flow misses (the 9-step design)
├── docs/Objetive.md              ← the competition brief this demo answers
├── docs/edge-cases-notes.md      ← the "adding auto-handles, cancelling escalates" rule
│
├── steps/                        ← the lookup tables the operator searches
│   ├── airports.csv              ← ICAO reference (real codes)
│   ├── provider-database.csv     ← the "Excel": ICAO × service → provider + email + payment
│   ├── operator-registry.csv     ← who the senders are: tier, permits, credit, flight type
│   ├── service-catalog.md        ← which services are in/out of scope + how each behaves
│   └── email-categories.md       ← classification: noise vs operational; new vs amendment
│
├── templates/                    ← outbound email shells ({{TOKENS}} to fill)
│   ├── handling-request.md
│   ├── ground-transport-request.md
│   ├── hotel-request.md          ← two variants (named hotel vs propose 3)
│   ├── catering-request.md
│   ├── client-acknowledgment.md  ← two variants (new vs amendment)
│   └── escalation-flag.md        ← internal hand-off when NOT auto-handling
│
├── samples/inbound/              ← 27 fictional incoming emails (14 core + 10 edge + 3 adversarial)
│   ├── 01-falconcrest-arrival-handling.md      (HANDLE — handling + transport)
│   ├── 02-adriaticwings-departure-full.md      (HANDLE — 4 services)
│   ├── 03-eta-amendment.md                      (HANDLE — amendment, live thread)
│   ├── 04-northern-air-command-military.md      (ESCALATE — military + permit)
│   ├── 05-fuel-only-request.md                  (ESCALATE — out-of-scope subprocess)
│   ├── 06-newsletter-noise.md                   (DROP — noise)
│   ├── 07-solaris-multileg-handling.md          (HANDLE — 2 airports, 1 reference)
│   ├── 08-meridian-kteb-inbound-only.md         (HANDLE handling; FLAG inbound-only transport)
│   ├── 09-adriatic-scel-full.md                 (HANDLE — 3 services at SCEL)
│   ├── 10-falconcrest-sbgr-handling.md          (HANDLE — terse subject-only parse)
│   ├── 11-meridian-lfpb-handling-catering.md    (HANDLE — handling + catering)
│   ├── 12-solaris-eggw-no-catering-provider.md  (HANDLE handling; FLAG missing catering provider)
│   ├── 13-libertyjet-kmia-aircard.md            (HANDLE — US station + Aircard payer → CC accounting)
│   ├── 14-cascadeair-kteb-unknown.md            (HANDLE — payment profile UNKNOWN → accounting CC TBC)
│   ├── E01..E10-*.md             E01 cancel · E02 add service · E03 remove service ·
│   │                             E04 billing (not ops) · E05 unknown operator · E06 provider FYI ·
│   │                             E07 credit hold · E08 diplomatic · E09 broker on-behalf ·
│   │                             E10 hotel-only, no handling anchor
│   └── S01..S03-*.md             adversarial (trust boundary): S01 hidden instruction ·
│                                 S02 recipient swap · S03 spoofed sender
│
└── samples/golden/               ← golden output for each inbound (01..14 + E01..E10 + S01..S03 -OUTPUT.md)
```

## Data dictionary

### `steps/airports.csv`
`icao` (real code) · `airport_name` · `city` · `country` · `timezone_utc_offset` · `notes`

### `steps/provider-database.csv` — the lookup the operator searches by ICAO + service
| column | meaning |
|---|---|
| `icao` | airport (joins to `airports.csv`) |
| `service_category` | `handling` / `ground_transport` / `catering` (no `hotel` — see note) |
| `provider_name`, `provider_email` | who to contact (fictional `.example` address) |
| `payment_type` | `CREDIT` or `CREDIT_CARD` (card → CC `procurement@`) or `PREPAID` |
| `inbound_only` | `yes` → never send a request; read their confirmations only |
| `is_designated` | `yes` → the desk's default handler at that station |
| `notes` | routing/payment caveats |

> **No `hotel` rows by design.** Hotels are operator-named or the desk proposes 3 options. See
> `steps/service-catalog.md`.

### `steps/operator-registry.csv` — who the sender is
| column | meaning |
|---|---|
| `operator_name`, `operator_code` | the charter/airline |
| `sender_domain` | match the inbound `From:` to identify the operator |
| `type_of_flight` | Part 135 / Part 91 / Military / Diplomatic — drives eligibility |
| `tier` | T1–T4 confidence/automation tier |
| `manages_permits` | `no` for Military/Diplomatic → permit work is blocked |
| `credit_status` | `OK` / `HOLD` (`HOLD` → escalate to Finance) |
| `default_services` | services this operator usually needs |
| `notes` | handling caveats, e.g. "DO NOT auto-handle" |

## How an agent should use this dataset

1. Match inbound `From:` domain → `operator-registry.csv` (identify operator, tier, credit, flight type).
2. Classify with `email-categories.md` (drop noise; decide new/amendment/FYI).
3. Extract the flight skeleton; detect services against `service-catalog.md`.
4. For each in-scope service, look up `provider-database.csv` by `icao` + `service_category`.
5. Fill the matching `templates/` shell; apply the CC rules (card → procurement@; US Aircard → accounting@).
6. Produce the fixed output card and route to **HANDLE / ESCALATE / DROP**.

The `sample-inbound/` + `sample-responses/` pairs are the acceptance tests: feed an inbound, expect
the matching output. Cases 04–06 prove the operator escalates and drops instead of forcing a draft.

## Self-consistency

Every ICAO used in a sample email exists in `airports.csv` and (for in-scope asks) has a matching
row in `provider-database.csv`. Every service requested maps to a category in `service-catalog.md`.
Out-of-scope asks (permit, fuel) are recognized categories that route to escalation, not unknowns.
