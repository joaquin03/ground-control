# Required Fields per Service

> ⚠️ Demo data. Fictional "Apex Trip Support" desk. This is the precise definition behind
> `INCOMPLETE_SKELETON` (brainstorm.md, Gap D). A request can only be drafted when its
> **hard-required** fields are present or safely inferable. Otherwise the operator does not guess.

## Operation-level minimum (before any service)

All of these must be present, or the email escalates as `INCOMPLETE_SKELETON`:
- **Operator** identifiable (sender domain matches `operator-registry.csv`, or clearly named)
- **Airport** — a valid ICAO that exists in `airports.csv`
- **Date** of the movement
- **At least one service** requested

## Per-service fields

Legend: **H** = hard-required (missing ⇒ escalate/ask) · **S** = soft (proceed; mark `TBC` or infer).

### `handling`
| field | H/S | note |
|---|---|---|
| operator | H | |
| registry | H | tail number |
| aircraft_type | H | |
| movement | H | ARRIVAL or DEPARTURE |
| ICAO | H | |
| date | H | |
| time (UTC) | H | ETA/ETD in Z; if only local given, convert via `airports.csv` offset |
| POB (pax/crew) | H | |
| from/to ICAO | S | the other end of the leg — nice to have |

### `ground_transport`
| field | H/S | note |
|---|---|---|
| ICAO | H | |
| date | H | |
| time | H | pickup time; "on arrival" is acceptable and follows the handling time |
| route (pickup → drop-off) | H | e.g. FBO → hotel |
| pax | H | |
| vehicle type | S | inferable from pax count |

### `hotel`
| field | H/S | note |
|---|---|---|
| city / ICAO | H | |
| guests | H | |
| rooms | H | |
| check-in date | H | |
| check-out date | H | |
| hotel name | S | if absent → Variant B (propose 3 options) instead of escalating |

### `catering`
| field | H/S | note |
|---|---|---|
| ICAO | H | |
| date | H | |
| delivery time | H | local time to aircraft/handler |
| pax | H | |
| dietary requirements | S | if unstated, proceed and note "none advised" |

## How to apply

1. Check operation-level minimum first. Fail → `INCOMPLETE_SKELETON`, escalate (or reply asking for
   the missing field).
2. For each requested service, check its hard-required fields. If a hard field is missing and cannot
   be safely inferred → do not draft that service; escalate or ask for it. **Exception:** a service
   that will be FLAGGED anyway (no provider on file, Step 5) defers its hard-field check — the missing
   field rides on the FLAGGED line for the human who sources the provider (e.g. Sample 12: catering
   with no EGGW provider and no delivery time → FLAGGED, not `INCOMPLETE_SKELETON`).
3. Missing **soft** fields never block a draft — infer, or set the line to `TBC`
   (see `steps/status-vocabulary.md`).

> Example: a "need handling for our jet next week, details to follow" email fails the
> operation-level minimum (no registry, no ICAO, no time, no POB) → `INCOMPLETE_SKELETON`.
