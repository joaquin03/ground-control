"""Assert an output's human-card body conforms to the 3-zone action-board contract.

Source of truth: `reference/decision-card.md` §2 (the three zones) and §4 (per-route shape).
This closes the gap where `run_eval.py` only parsed the 5-line machine header and was blind to
the card body — which had let the retired 8-section format pass green while the contract had
moved to the 3-zone board. Markers below are derived from the contract, never from any golden,
so the check can never silently agree with a stale corpus.

It also enforces the card-sola rule: the audit appends (`RESULTS +=`, `LOG +=`) are machine state
and live in `state/results.csv` + `state/activity-log.md` per `reference/logging.md` — they must
NOT be embedded in the human card. Only `LEDGER +=` (the trip's identity commit) stays in the card.

`check_card_body(header, text)` returns a list of problem strings (empty list = conforms).
"""
import re

# Markers that must never appear in a card body, on any route:
#  - the retired 8-section card (decision-card.md §2: skeleton/provider-lookup/routing tables removed)
#  - the audit appends, which belong in state/ not the card (logging.md). NB: 'LEDGER +=' is allowed.
_FORBIDDEN_ALL = [
    "Provider lookup",
    "Routing summary",
    "Flight skeleton",
    "Services detected",
    "8-section",
    "RESULTS +=",
    "LOG +=",
]
# Old numbered card sections: "**1 — Decision**", "**5 — Drafted outbound**", etc.
_OLD_SECTION_RE = re.compile(r"^\*\*\d+ — ", re.MULTILINE)

# The action-board banner that opens every route: "━━ <DECISION> · <INTENT> · <OP-STATUS> · <REF> ━━".
_BANNER_RE = re.compile(r"^━━ .*━━\s*$", re.MULTILINE)

# Stable marker from templates/escalation-flag.md — proves the flag is actually present on ESCALATE.
_ESCALATION_MARK = "ESCALATION — HUMAN ACTION REQUIRED"


def _route(header):
    """Collapse (decision, intent) into the shape key used by decision-card.md §4."""
    decision = (header.get("decision") or "").upper()
    intent = (header.get("intent") or "").upper()
    if decision == "HANDLE" and intent == "FYI":
        return "FYI"
    return decision  # HANDLE | ESCALATE | DROP


def check_card_body(header, text):
    problems = []
    route = _route(header)

    # 1 · Forbidden everywhere: retired 8-section format + audit appends in the card.
    for marker in _FORBIDDEN_ALL:
        if marker in text:
            problems.append(f"forbidden in card body: {marker!r} (8-section or audit-append belongs in state/)")
    if _OLD_SECTION_RE.search(text):
        problems.append("retired numbered card section present (e.g. '**1 — ...**')")

    # 2 · Every route opens with the action-board banner.
    if not _BANNER_RE.search(text):
        problems.append("missing action-board banner line ('━━ … ━━')")

    # 3 · Per-route zones (decision-card.md §4).
    if route == "HANDLE":
        for need in ("DOING →", "▸ DRAFTS", "▸ TRIP RECORD", "⛑ FLAGS"):
            if need not in text:
                problems.append(f"HANDLE missing zone marker: {need!r}")
    elif route == "FYI":
        for need in ("▸ TRIP RECORD", "⛑ FLAGS"):
            if need not in text:
                problems.append(f"FYI missing zone marker: {need!r}")
        for forb in ("DOING →", "▸ DRAFTS"):
            if forb in text:
                problems.append(f"FYI stages no work — found {forb!r}")
    elif route == "ESCALATE":
        if _ESCALATION_MARK not in text:
            problems.append(f"ESCALATE missing escalation flag ({_ESCALATION_MARK!r})")
        for forb in ("DOING →", "▸ DRAFTS"):
            if forb in text:
                problems.append(f"ESCALATE drafts nothing — found {forb!r}")
    elif route == "DROP":
        for forb in ("DOING →", "▸ DRAFTS", _ESCALATION_MARK):
            if forb in text:
                problems.append(f"DROP is minimal — found {forb!r}")

    return problems
