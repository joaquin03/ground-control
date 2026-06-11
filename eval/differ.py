"""Diff a parsed header against an expected case. Returns a list of (field, expected, actual) fails."""
from refmatch import ref_ok

def diff_case(case, h):
    fails = []
    def check(field, expected, actual):
        if expected != actual:
            fails.append((field, expected, actual))
    check("decision", case["decision"], h.get("decision"))
    check("intent", case["intent"], h.get("intent"))
    check("op_status", case["op_status"], h.get("op_status"))
    check("services", case.get("services") or {}, h.get("services") or {})
    check("routing", case.get("routing") or {}, h.get("routing") or {})
    expected_reason = sorted(case.get("reason") or [])
    check("reason", expected_reason, sorted(h.get("reason") or []))
    if not ref_ok(case["ref_expect"], h.get("ref")):
        fails.append(("ref", case["ref_expect"], h.get("ref")))
    return fails
