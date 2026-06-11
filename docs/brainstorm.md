# Brainstorm — what the naive flow is missing

> ⚠️ Demo doc. Fictional "Apex Trip Support" executive-aviation desk. All operators, providers and
> contacts are invented; ICAO codes are real public reference data.

This dataset backs an **operator** (in the "AI operator, not chatbot" sense): it reads an inbound
ops email, **decides**, and produces finished work or a clean flag. This file captures the design
thinking — specifically, the steps that the obvious version of the workflow skips.

## The naive flow

The first sketch of the workflow was five steps:

1. Read the email
2. Classify it
3. Pluck the services required
4. Look up the correct provider for the ICAO (from a spreadsheet)
5. Draft the provider emails + a reply to the sender

That is the happy path for one kind of email: a brand-new, complete, in-scope request from a known
operator. Most inbound is not that. The gaps below are where a chatbot would stall and ask the user
what to do — and where an operator has to decide on its own.

## The missing steps (each one is a decision)

**Gap A — "Is this even an operational email?"** (before step 2)
A large share of the inbox is noise: newsletters, delivery-failure bounces, out-of-office, internal
admin. The first decision is **in-scope vs DROP**. Without it, the operator tries to "handle" a
marketing email. → encoded in `steps/email-categories.md` (Question 1).

**Gap B — "New request, amendment, or just an FYI?"** (inside step 2)
Most operational emails are `Re:` replies on a live thread, not new bookings. The operator must
decide **open new trip / update existing trip / acknowledge only**. Getting this wrong creates
duplicate trips or silently drops a change. → `steps/email-categories.md` (Question 2); worked in
`sample-responses/03-eta-amendment-OUTPUT.md`.

**Gap C — "Who is the operator, and what rules apply to them?"** (new step, before extracting)
Identify the operator and look up their profile: tier, whether the desk handles their permits,
credit status, type of flight. This **gates everything downstream**. A military/state operator is
blocked; a credit-on-hold operator is blocked. → `steps/operator-registry.csv`; worked in
`sample-responses/04` (military).

**Gap D — "Extract the structured flight skeleton"** (the real content of step 3)
Registry, aircraft type, ICAO(s), times in UTC, flight number, pax/crew, arrival-vs-departure.
Nothing downstream can be filled without it, and this is where parsing actually fails. If critical
fields are missing and can't be safely inferred → escalate as incomplete.

**Gap E — provider lookup is not always "1 ICAO → 1 provider"** (step 4 is more than it looks)
- Handling / ground / catering: ICAO + category → one provider. ✅ the simple case.
- **Hotel** has *no* provider database — it's operator-named or the desk proposes 3 options.
- Some providers are **inbound-only** (e.g. Drivex Chauffeur): the desk reads their confirmations
  and must never generate a request to them.
- The genuinely hard ones (permits = Part × type × country; fuel = multi-broker comparative) are
  **deliberately out of scope** here and escalate. → `steps/service-catalog.md`.

**Gap F — "Validate before drafting"** (new step, before step 5)
Credit OK? Provider actually exists for this ICAO+service? For out-of-scope scope: is the ask a
primary service or a secondary line on an otherwise-handle-able email? (If any out-of-scope service
is present, escalate the whole email so the trip stays together.) → `sample-responses/05` (fuel).

**Gap G — routing & CC rules** (inside step 5, easy to get wrong)
Which mailbox sends (`info@` for handling/ground/hotel/catering), and who is copied:
`procurement@` when the provider is paid by corporate card; `accounting@` for US Aircard stations.
A wrong CC is a process failure even when the draft is perfect. → encoded in templates + `steps/`.

**Gap H — the escalation decision** (the heart of "operator, not chatbot")
After everything, the operator routes to exactly one of **HANDLE / ESCALATE / DROP**. Explicit
triggers to escalate rather than guess: military/diplomatic operator, out-of-scope subprocess,
credit on hold, unknown operator, incomplete skeleton, low confidence. This is what makes it decide
and act instead of handing the question back.

## The flow, corrected

The five steps become roughly nine:

```
0. Scope filter ............... operational? else DROP            (Gap A)
1. Intent ..................... new / amendment / FYI             (Gap B)
2. Identify operator .......... tier, permits, credit, flight type (Gap C)
3. Extract flight skeleton .... reg, type, ICAO, UTC times, pax    (Gap D)
4. Detect services ............ in-scope vs out-of-scope tags      (Gap E)
5. Provider lookup ............ per service, incl. special cases   (Gap E)
6. Validate ................... credit, provider exists, scope     (Gap F)
7. Draft + route .............. fill templates, apply CC rules     (Gap G)
8. Decide ..................... HANDLE / ESCALATE / DROP           (Gap H)
```

Steps 0, 1, 2, 6 and 8 are pure decision logic — that is the operator's brain, and it lives in the
rules the agent author writes on top of this dataset. This folder supplies everything those rules
read against: the lookup data, the service definitions, the templates, and worked examples of each
outcome.

## Deliberately out of scope (so the demo stays tight)

Permits, fuel, and flight planning are detected and escalated, never attempted. Military/diplomatic
operators, no-credit operators, and unknown operators are escalated. Auto-**sending** is out — the
operator drafts and a human sends. These choices keep the operator narrow enough to trust, which is
the bar that matters.
