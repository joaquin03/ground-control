"""Match an output REF against a case's ref expectation (sequence wildcarded)."""
import re

_RENDERED = re.compile(r"^PN\d{7}$")
_PLACEHOLDER = re.compile(r"^\{\{ASSIGN:PN\d{4}-NNN\}\}$|^\{\{ASSIGN:PN\d{4}-\d{3}\}\}$")

def ref_ok(expect, actual):
    actual = (actual or "").strip()
    if expect == "assign":
        return bool(_RENDERED.match(actual) or _PLACEHOLDER.match(actual))
    if expect == "none":
        return actual == "-"
    if expect.startswith("fixed:"):
        return actual == expect.split(":", 1)[1]
    raise ValueError(f"unknown ref_expect: {expect}")
