# Service Catalog

> ⚠️ Demo data — all providers, operators and contacts are fictional. ICAO codes are real public reference data.

The services this dataset covers, and how the operator should treat each one. These are the
categories to **pluck** from an inbound email (step "detect services"). Only the **in-scope**
categories get a provider lookup and a drafted outbound email. The **out-of-scope** ones are
detected so they can be flagged, never auto-handled.

## In scope (Subprocess A — Handling, and Subprocess B — Ground/Hotel/Catering)

| service_category | trigger words in email | provider lookup | template |
|---|---|---|---|
| `handling` | handling, ramp, arrival/departure handling, ground handling, PPR | `provider-database.csv` by `icao` + `handling` | `templates/handling-request.md` |
| `ground_transport` | transport, chauffeur, car, pickup, crew transport, limo | `provider-database.csv` by `icao` + `ground_transport` | `templates/ground-transport-request.md` |
| `hotel` | hotel, accommodation, rooms, crew rest | **No ICAO provider lookup** — see rule below | `templates/hotel-request.md` |
| `catering` | catering, meals, crew meals, VIP catering | `provider-database.csv` by `icao` + `catering` | `templates/catering-request.md` |

### Handling is the anchor
Every operational trip touches handling. Ground transport, hotel and catering are normally
**attached to a handling request** — they are not offered on their own unless the operator is a
known full-service account (registry `default_services` includes the asked service). If an inbound
asks only for hotel/transport/catering with **no handling and no live handling thread**, escalate
`NO_ANCHOR_SERVICE` (ops_desk) — there is no trip to attach the service to, and opening a serviceless
operation invents one. Worked case: `samples/inbound/E10-solaris-hotel-only.md`.

### "PPR" is two different words (the tiebreak)
PPR appears as a trigger in **both** lists below, on purpose — the desk meaning depends on who grants
it. **PPR arranged via the station handler** (slot/stand at the FBO, part of normal arrival
coordination) is part of `handling` — in scope. A **standalone PPR / clearance from an authority**
(civil-aviation authority, airport authority approval, anything the handler can't grant) is `permit`
— out of scope, escalate. If the email doesn't make clear which one it is, it's the permit kind:
escalate rather than guess.

### Hotel has no provider database
Hotels are **client-specified** or **suggested by the desk**. There is intentionally no hotel row in
`provider-database.csv`.
- If the operator named a specific hotel → the hotel template books that hotel directly.
- If the operator did not name a hotel → the hotel template requests **3 options** near the field
  (4–5 star, close to the airport) and waits for the operator to choose.

### Inbound-only providers
Some providers (e.g. `Drivex Chauffeur` for ground transport at KMIA / KTEB) are marked
`inbound_only=yes`. Their booking confirmations arrive automatically; the operator **reads** them
to populate the trip, and must **never generate a new request** to them. If ground transport at
such a station is needed, that is a human action, not an outbound draft.

## Out of scope (detect → ESCALATE, never auto-handle)

| service_category | trigger words | why it's out of scope |
|---|---|---|
| `permit` | permit, overflight, OVF, landing permit, slot, APIS, PPR clearance | Provider depends on Part × permit-type × country and on legal eligibility |
| `fuel` | fuel, uplift, fuel release, into-plane, JET A1 quote | Uses a multi-broker comparative-quote process, not a single provider |
| `flight_plan` | flight plan, FPL, OFP, nav plan, flight watch, weather package | Generated in specialist software, not a provider email |

When an inbound's **primary** ask is one of these, escalate it. When it's a **secondary** line on
an otherwise handle-able email (e.g. handling + "also need overflight permit"), handle nothing and
escalate the whole email so the human keeps the trip together.
