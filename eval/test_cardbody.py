#!/usr/bin/env python3
"""Unit tests for cardbody.check_card_body — the 3-zone action-board body check."""
from cardbody import check_card_body

# A minimal but conforming body for each route (markers per decision-card.md §2/§4).
HANDLE_OK = """
━━ HANDLE · NEW · OPEN · PN2606031 ━━
Adriatic Wings · 9H-ADW (G650) · DEP LEMD → LFPB · POB 6/4
DOING →
  1. LEMD · handling → Iberus Ramp Partners   (handling@iberusramp.example)
  → ack to operator
⛑ FLAGS: none

▸ DRAFTS — the part a human sends
ATTN: Iberus Ramp Partners ...

▸ TRIP RECORD
OPERATION  PN2606031   status: OPEN
LEDGER += sequences."2606"=31 · trips."ADW|9H-ADW|14JUN26|LEMD"="PN2606031"
"""

FYI_OK = """
━━ HANDLE · FYI · OPEN · PN2606014 ━━
Falcon Crest · T7-FCX · ARR SUMU · POB 4/3
⛑ FLAGS: none

▸ TRIP RECORD
OPERATION  PN2606014   status: OPEN
services: handling · CONFIRMED
"""

ESCALATE_OK = """
━━ ESCALATE · NEW · ESCALATED · - ━━
Why: Military operator + permit subprocess — a human owns this.

ESCALATION — HUMAN ACTION REQUIRED
==================================
Reason code: MILITARY_OPERATOR, OUT_OF_SCOPE_SUBPROCESS
"""

DROP_OK = """
━━ DROP · - · DROPPED · - ━━
Why: Marketing newsletter — not operational.
"""

# The retired 8-section format that the contract removed.
OLD_8SECTION = """
## Operation artifact
**1 — Decision** · HANDLE.
**4 — Provider lookup** (LEMD): handling=Iberus.
**7 — Routing summary** — all From info@.
"""


def _hdr(decision, intent):
    return {"decision": decision, "intent": intent}


def test_conforming_bodies_pass():
    assert check_card_body(_hdr("HANDLE", "NEW"), HANDLE_OK) == []
    assert check_card_body(_hdr("HANDLE", "FYI"), FYI_OK) == []
    assert check_card_body(_hdr("ESCALATE", "NEW"), ESCALATE_OK) == []
    assert check_card_body(_hdr("DROP", "-"), DROP_OK) == []


def test_old_8section_fails_every_route():
    for decision, intent in [("HANDLE", "NEW"), ("ESCALATE", "NEW"), ("DROP", "-")]:
        problems = check_card_body(_hdr(decision, intent), OLD_8SECTION)
        assert problems, f"old 8-section unexpectedly passed as {decision}/{intent}"


def test_audit_appends_forbidden_in_card_but_ledger_allowed():
    # LEDGER += is the trip's identity commit — it STAYS in the card.
    assert check_card_body(_hdr("HANDLE", "NEW"), HANDLE_OK) == []
    # RESULTS += / LOG += are machine state — they must NOT be in the card body.
    with_results = HANDLE_OK + "\nRESULTS += 09JUN2026,PN2606031,x,subj,LEMD,handling,Iberus,a@b,-,REQUESTED,HANDLE,-\n"
    assert any("RESULTS +=" in p for p in check_card_body(_hdr("HANDLE", "NEW"), with_results))
    with_log = HANDLE_OK + "\nLOG +=\n## 09JUN2026 · PN · reg · op\n"
    assert any("LOG +=" in p for p in check_card_body(_hdr("HANDLE", "NEW"), with_log))


def test_handle_requires_all_zones():
    missing_drafts = HANDLE_OK.replace("▸ DRAFTS — the part a human sends", "")
    assert any("▸ DRAFTS" in p for p in check_card_body(_hdr("HANDLE", "NEW"), missing_drafts))


def test_fyi_must_not_stage_work():
    staged = FYI_OK + "\nDOING →\n  1. LEMD · handling → X\n"
    assert any("FYI stages no work" in p for p in check_card_body(_hdr("HANDLE", "FYI"), staged))


def test_escalate_requires_flag_and_no_drafts():
    no_flag = ESCALATE_OK.replace("ESCALATION — HUMAN ACTION REQUIRED", "")
    assert any("escalation flag" in p for p in check_card_body(_hdr("ESCALATE", "NEW"), no_flag))
    with_draft = ESCALATE_OK + "\n▸ DRAFTS — the part a human sends\n"
    assert any("drafts nothing" in p for p in check_card_body(_hdr("ESCALATE", "NEW"), with_draft))


def test_missing_banner_fails():
    no_banner = HANDLE_OK.replace("━━ HANDLE · NEW · OPEN · PN2606031 ━━", "HANDLE NEW OPEN")
    assert any("banner" in p for p in check_card_body(_hdr("HANDLE", "NEW"), no_banner))


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"  ok  {fn.__name__}")
    print(f"\nALL PASS — {len(fns)} tests")
