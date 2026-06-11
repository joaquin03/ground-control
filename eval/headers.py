"""Parse Ground Control's machine header from an output/golden file."""
import re

_LABELS = {
    "case": r"^CASE:\s*(\S+)",
    "decision": r"DECISION:\s*(\S+)",
    "intent": r"INTENT:\s*(\S+)",
    "op_status": r"OP-STATUS:\s*(\S+)",
    "confidence": r"CONFIDENCE:\s*(\S+)",
    "ref": r"REF:\s*(\{\{ASSIGN:[^}]+\}\}|\S+)",
}

def _pairs(line_value):
    """'a=1 b=2' -> {'a':'1','b':'2'}; '-' -> {}."""
    out = {}
    for tok in line_value.split():
        if "=" in tok:
            k, v = tok.split("=", 1)
            out[k] = v
    return out

def parse_header(text):
    h = {k: None for k in _LABELS}
    for key, pat in _LABELS.items():
        m = re.search(pat, text, re.MULTILINE)
        h[key] = m.group(1) if m else None
    sm = re.search(r"^SERVICES:\s*(.*)$", text, re.MULTILINE)
    rm = re.search(r"^ROUTING:\s*(.*)$", text, re.MULTILINE)
    nm = re.search(r"^REASON:\s*(.*)$", text, re.MULTILINE)
    h["services"] = _pairs(sm.group(1).strip()) if sm else {}
    h["routing"] = _pairs(rm.group(1).strip()) if rm else {}
    reason_raw = nm.group(1).strip() if nm else "-"
    h["reason"] = [] if reason_raw in ("-", "") else [c.strip() for c in reason_raw.split(",")]
    return h
