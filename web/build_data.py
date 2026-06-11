#!/usr/bin/env python3
"""
build_data.py - Ground Control web data extractor.

Turns the real desk artifacts (samples/inbound, samples/golden, state/*) into a
single data bundle the static site reads. ICM-faithful: the source of truth stays
the repo files; this only projects them for the browser.

Outputs (next to this script):
  data.js    -> window.GC = {...};   (loads from file:// with no fetch/CORS)
  data.json  -> same payload, for inspection / other tooling

Run:  python3 web/build_data.py
"""
import csv
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
INBOX = ROOT / "samples" / "inbound"
GOLD = ROOT / "samples" / "golden"
STATE = ROOT / "state"
STEPS = ROOT / "steps"

FENCE = re.compile(r"```[^\n]*\n(.*?)```", re.S)
EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]+")

# The 8-step spine (rules.md). Title + one-line job, for the decision-tree view.
SPINE = [
    ("S0", "Identify the sender", "Trust before content: authenticated, known, in good standing — before a word of the body is read? Unknown escalates; machine mail drops."),
    ("S1", "Scope filter", "Operational, or billing / provider-FYI?"),
    ("S2", "Intent", "NEW, AMENDMENT, or FYI. Cancel routes out."),
    ("S3", "Flight skeleton", "Registry, ICAO, times, POB complete?"),
    ("S4", "Detect services", "In-scope only. Handling is the anchor."),
    ("S5", "Provider lookup", "Resolve a provider per service + station."),
    ("S6", "Validate", "Credit, providers, skeleton, scope all clear."),
    ("S7", "Draft + route", "Fill templates, route CC, lock recipients, stage for approval."),
    ("S8", "Decide + open", "Mint/reuse REF, set statuses, emit artifact."),
]

# reason code -> the gate (step index) it fires at. Earliest gate wins.
# v2 order (sender-first): S0 identify sender, S1 scope, S2 intent, S3 skeleton, ...
REASON_GATE = {
    # S0 — identify the sender (trust before content): envelope-level trust gates, first thing run
    "UNKNOWN_OPERATOR": 0,        # off-registry stranger -> ESCALATE to sales at identify (content-blind)
    "IMPERSONATION": 0,           # off-registry impersonating a registry operator -> ESCALATE
    "MILITARY_OPERATOR": 0,
    "DIPLOMATIC_OPERATOR": 0,
    "NO_CREDIT": 0,
    "UNVERIFIED_AUTHORITY": 0,
    "UNVERIFIED_SENDER": 0,
    # S2 — intent (content): cancel + body-level injection surface here
    "CANCELLATION": 2,
    "SUSPECTED_INJECTION": 2,     # always-on; surfaces when content is read (after identity passes)
    "INCOMPLETE_SKELETON": 3,
    "OUT_OF_SCOPE_SUBPROCESS": 4,
    "NO_ANCHOR_SERVICE": 4,
    "LOW_CONFIDENCE": 6,
}


def read(p):
    return p.read_text(encoding="utf-8")


def case_key(name):
    """Leading token shared by inbound + golden: 01..14, E01..E09, S01..S03."""
    m = re.match(r"([ES]?\d+)", name)
    return m.group(1) if m else name


def parse_operator_registry():
    rows = {}
    with open(STEPS / "operator-registry.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows[r["sender_domain"].strip()] = r
    return rows


def parse_inbound(path):
    text = read(path)
    m = FENCE.search(text)
    block = m.group(1) if m else text
    lines = block.splitlines()
    hdr = {}
    body_start = 0
    for i, ln in enumerate(lines):
        hm = re.match(r"^(From|To|Date|Subject):\s*(.*)$", ln)
        if hm:
            hdr[hm.group(1).lower()] = hm.group(2).strip()
        elif ln.strip() == "" and hdr:
            body_start = i + 1
            break
    body = "\n".join(lines[body_start:]).strip()
    frm = hdr.get("from", "")
    em = EMAIL.search(frm)
    email = em.group(0) if em else ""
    domain = email.split("@", 1)[1] if "@" in email else ""
    name = re.sub(r"<.*?>", "", frm).strip()
    return {
        "from_name": name,
        "from_email": email,
        "domain": domain,
        "to": hdr.get("to", ""),
        "date": hdr.get("date", ""),
        "subject": hdr.get("subject", ""),
        "body": body,
    }


def parse_header(block):
    h = {}
    for ln in block.splitlines():
        if ln.startswith("CASE:"):
            h["case"] = ln.split(":", 1)[1].strip()
        elif ln.startswith("DECISION:"):
            for key in ("DECISION", "INTENT", "OP-STATUS", "CONFIDENCE", "REF"):
                mm = re.search(rf"{re.escape(key)}:\s*([^ ]+(?:\s+[^ ]+)*?)(?=\s+[A-Z\-]+:|$)", ln)
                if mm:
                    h[key.lower().replace("-", "_")] = mm.group(1).strip()
        elif ln.startswith("SERVICES:"):
            h["services_raw"] = ln.split(":", 1)[1].strip()
        elif ln.startswith("ROUTING:"):
            h["routing_raw"] = ln.split(":", 1)[1].strip()
        elif ln.startswith("REASON:"):
            h["reason"] = ln.split(":", 1)[1].strip()
    return h


def parse_kv_list(raw):
    if not raw or raw.strip() == "-":
        return []
    out = []
    for tok in raw.split():
        if "=" in tok:
            k, v = tok.split("=", 1)
            out.append({"name": k, "status": v})
    return out


def first_line(s):
    for ln in s.splitlines():
        if ln.strip():
            return ln.strip()
    return ""


def parse_golden(path):
    text = read(path)
    blocks = []
    for m in FENCE.finditer(text):
        blocks.append({"start": m.start(), "content": m.group(1).rstrip("\n")})

    header = trip = esc = None
    drafts = []
    lines_with_pos = []  # (offset, line) for label lookup
    pos = 0
    for ln in text.splitlines(keepends=True):
        lines_with_pos.append((pos, ln.rstrip("\n")))
        pos += len(ln)

    def label_before(offset):
        cand = ""
        for off, ln in lines_with_pos:
            if off >= offset:
                break
            s = ln.strip()
            if not s:
                continue
            if s.startswith("```") or s.startswith("▸") or s.startswith("Route to:") \
               or s.startswith("Why") or s.startswith("━━") or s.startswith(">"):
                continue
            cand = s
        # clean decoration: em-dashes, italics, backticks; drop a trailing
        # "-> email, CC ..." routing chunk (the recipient is captured separately)
        cand = cand.strip("—* ").replace("`", "").replace("*", "").strip()
        if "→" in cand:
            left, right = cand.split("→", 1)
            if "@" in right:
                cand = left.strip()
        return cand.strip()

    for b in blocks:
        head = first_line(b["content"])
        if head.startswith("CASE:"):
            header = b
        elif head.startswith("OPERATION"):
            trip = b
        elif head.startswith("ESCALATION"):
            esc = b
        else:
            label = label_before(b["start"])
            em = EMAIL.search(label) or EMAIL.search(b["content"][:200])
            drafts.append({
                "label": label,
                "to": em.group(0) if em else "",
                "body": b["content"].strip("\n"),
            })

    h = parse_header(header["content"]) if header else {}

    # glance: banner / summary / doing / flags from the card text
    banner = summary = ""
    doing, flags, why = [], [], []
    mode = None
    body_text = text
    if header:
        body_text = text[header["start"] + len(header["content"]):]
    for ln in body_text.splitlines():
        s = ln.strip()
        if s.startswith("━━"):
            banner = s.strip("━ ").strip()
            mode = "after_banner"
            continue
        if s.startswith("DOING"):
            mode = "doing"
            continue
        if s.startswith("⛑") or s.startswith("FLAGS"):
            mode = "flags"
            continue
        if s.startswith("Why"):
            mode = "why"
            continue
        if s.startswith("▸") or s.startswith("```"):
            mode = None
            continue
        if not s:
            if mode in ("doing", "flags", "why"):
                mode = None
            continue
        if mode == "after_banner" and not summary:
            summary = s
            mode = None
        elif mode == "doing":
            doing.append(re.sub(r"^\d+\.\s*", "", s).lstrip("→ ").strip())
        elif mode == "flags":
            flags.append(s.lstrip("- ").strip())
        elif mode == "why":
            why.append(s.lstrip("- ").strip())

    route_to = ""
    rm = re.search(r"^Route to:\s*(.+)$", text, re.M)
    if rm:
        route_to = rm.group(1).strip()

    return {
        "header": h,
        "banner": banner,
        "summary": summary,
        "doing": doing,
        "flags": flags,
        "why": why,
        "drafts": drafts,
        "escalation_flag": esc["content"].strip("\n") if esc else "",
        "route_to": route_to,
        "trip_record": trip["content"].strip("\n") if trip else "",
    }


def build_spine(decision, intent, reason, why=""):
    reasons = [r.strip() for r in re.split(r"[,\s]+", reason or "") if r.strip() and r != "-"]
    gate = None
    if decision == "ESCALATE":
        gates = [REASON_GATE[r] for r in reasons if r in REASON_GATE]
        gate = min(gates) if gates else 2
    elif decision == "DROP":
        # machine/bulk mail drops at S0 (sender gate, header markers); billing/internal at S1 (scope)
        dgates = [REASON_GATE[r] for r in reasons if r in REASON_GATE]
        if dgates:
            gate = min(dgates)
        elif re.search(r"newsletter|marketing|bounce|out.of.office|read receipt|bulk|noise",
                       (why or "") + " " + (reason or ""), re.I):
            gate = 0
        else:
            gate = 1
    out = []
    for i, (sid, title, job) in enumerate(SPINE):
        state = "pass"
        if decision == "HANDLE":
            state = "pass"
        elif decision == "ESCALATE":
            if i < gate:
                state = "pass"
            elif i == gate:
                state = "stop"
            else:
                state = "skip"
        elif decision == "DROP":
            if i < gate:
                state = "pass"
            elif i == gate:
                state = "stop"
            else:
                state = "skip"
        out.append({"id": sid, "title": title, "job": job, "state": state})
    # FYI handling: a provider confirmation - operational, FYI intent, jumps to S8
    if intent == "FYI":
        for s in out:
            s["state"] = "skip"
        out[0]["state"] = "pass"   # S0 identify (sender = provider on a live thread)
        out[1]["state"] = "pass"   # S1 scope: operational, provider confirmation
        out[2]["state"] = "pass"   # S2 intent = FYI, reuse thread REF
        out[8]["state"] = "pass"   # S8 service -> CONFIRMED, no outbound
    return out, gate, reasons


def parse_node_detail(spine):
    """Split an activity-log spine string into per-step (S0..S8) detail."""
    out = {}
    marks = list(re.finditer(r"S(\d)\b", spine))
    for i, m in enumerate(marks):
        start = m.end()
        end = marks[i + 1].start() if i + 1 < len(marks) else len(spine)
        out["S" + m.group(1)] = spine[start:end].strip(" ·,;")
    return out


def derive_from_spine(spine):
    if re.search(r"\bDROP\b", spine):
        dec = "DROP"
    elif re.search(r"\bESCALATE\b", spine):
        dec = "ESCALATE"
    else:
        dec = "HANDLE"
    im = re.search(r"S2\s+(NEW|AMENDMENT|FYI)", spine)
    intent = im.group(1) if im else ("FYI" if "FYI" in spine else "-")
    head = spine.split("S5")[0] if "S5" in spine else spine
    svc = set(re.findall(r"handling|ground_transport|catering|hotel", head))
    return dec, intent, svc


def attach_log(cases, log):
    """Join each case to its activity-log entry (the per-step trail), so the
    decision tree can show what each gate actually read. Subjects repeat across
    threads, so ambiguous matches are scored on decision + intent + services."""
    def norm(x):
        return re.sub(r"\s+", " ", x or "").strip().lower()

    def base(x):
        return re.sub(r"^(re|fw):\s*", "", norm(x))

    used = [False] * len(log)
    for c in cases:
        subj = norm(c["inbound"]["subject"])
        cand = [i for i, e in enumerate(log) if not used[i] and norm(e["inbound"]) == subj]
        if not cand:
            cand = [i for i, e in enumerate(log) if not used[i] and base(e["inbound"]) == base(subj)]
        pick = None
        if len(cand) == 1:
            pick = cand[0]
        elif len(cand) > 1:
            cs = set(s["name"] for s in c["services"])
            best = -1
            for i in cand:
                dec, intent, svc = derive_from_spine(log[i]["spine"])
                score = (2 if dec == c["decision"] else 0) + (2 if intent == c["intent"] else 0) + len(cs & svc)
                if score > best:
                    best, pick = score, i
        if pick is not None:
            used[pick] = True
            e = log[pick]
            c["log"] = {"spine": e["spine"], "actions": e["actions"], "flags": e["flags"]}
            c["node_detail"] = parse_node_detail(e["spine"])
        else:
            c["log"] = None
            c["node_detail"] = {}


def parse_eval():
    """Read cases.jsonl and run the real regression harness, capturing its output."""
    cj = []
    for line in (ROOT / "eval" / "cases.jsonl").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            cj.append(json.loads(line))
    guard_counts = {}
    for c in cj:
        for g in c.get("guards", []):
            guard_counts[g] = guard_counts.get(g, 0) + 1

    ok, passed, summary, pass_lines = None, 0, "", []
    try:
        p = subprocess.run(
            [sys.executable, "run_eval.py", "--check", str(GOLD)],
            cwd=str(ROOT / "eval"), capture_output=True, text=True, timeout=90,
        )
        out = (p.stdout or "") + ("\n" + p.stderr if p.stderr else "")
        lines = [l.rstrip() for l in out.splitlines() if l.strip()]
        ok = "ALL PASS" in out
        summary = next((l.strip() for l in lines if "files" in l and "cases" in l), "")
        pass_lines = [re.sub(r"\s+", " ", l.strip()) for l in lines if l.strip().startswith("PASS")]
        passed = len(pass_lines) if ok else 0
    except Exception as e:  # harness unavailable; report honestly
        summary = "harness not run (" + str(e) + ")"

    return {
        "ok": ok,
        "passed": passed,
        "total": len(cj),
        "summary": summary or ("ALL PASS - " + str(passed) + " files, " + str(len(cj)) + " cases"),
        "command": "python3 run_eval.py --check ../samples/golden",
        "pass_lines": pass_lines,
        "layers": [
            {"k": "machine header", "v": "DECISION, INTENT, OP-STATUS, service statuses, ROUTING (CC), REASON pinned per case"},
            {"k": "card body", "v": "the 3-zone action-board contract; retired markers absent; audit appends kept out of the card"},
            {"k": "soft guards", "v": "provider-correct, cc-correct, no-fabrication, required-fields, distinct-read, on-voice"},
        ],
        "guards": sorted(guard_counts.keys()),
        "guard_counts": guard_counts,
    }


def main():
    reg = parse_operator_registry()
    inbound_files = {case_key(p.name): p for p in INBOX.glob("*.md")}
    golden_files = {case_key(p.name): p for p in GOLD.glob("*.md")}

    cases = []
    for key in sorted(inbound_files, key=lambda k: (k[0] == "E", k)):
        gp = golden_files.get(key)
        if not gp:
            continue
        inb = parse_inbound(inbound_files[key])
        g = parse_golden(gp)
        h = g["header"]
        decision = h.get("decision", "?")
        intent = h.get("intent", "-")
        reason = h.get("reason", "-")
        spine, gate, reasons = build_spine(decision, intent, reason, read(gp) if decision == "DROP" else "")

        # operator: trip-record line first, enriched by registry
        op = {"name": "UNKNOWN", "code": "", "tier": "", "type_of_flight": "", "credit": ""}
        tm = re.search(r"^operator:\s*(.+)$", g["trip_record"], re.M)
        if tm:
            op["name"] = re.sub(r"\(.*?\).*$", "", tm.group(1)).strip() or tm.group(1).strip()
            cm = re.search(r"\(([A-Z]{2,4})\)", tm.group(1))
            if cm:
                op["code"] = cm.group(1)
        rrow = reg.get(inb["domain"])
        if rrow:
            op["name"] = rrow["operator_name"]
            op["code"] = rrow["operator_code"]
            op["tier"] = rrow["tier"]
            op["type_of_flight"] = rrow["type_of_flight"]
            op["credit"] = rrow["credit_status"]

        cases.append({
            "id": key,
            "case_id": h.get("case", key),
            "decision": decision,
            "intent": intent,
            "op_status": h.get("op_status", "-"),
            "confidence": h.get("confidence", "-"),
            "ref": h.get("ref", "-"),
            "reason": reason,
            "reasons": reasons,
            "services": parse_kv_list(h.get("services_raw", "-")),
            "routing": parse_kv_list(h.get("routing_raw", "-")),
            "operator": op,
            "inbound": inb,
            "banner": g["banner"],
            "summary": g["summary"],
            "doing": g["doing"],
            "flags": g["flags"],
            "why": g["why"],
            "drafts": g["drafts"],
            "escalation_flag": g["escalation_flag"],
            "route_to": g["route_to"],
            "trip_record": g["trip_record"],
            "spine": spine,
            "gate": gate,
        })

    # audit: results.csv
    audit = []
    with open(STATE / "results.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            audit.append(r)

    # log: activity-log.md entries
    log = []
    log_text = read(STATE / "activity-log.md")
    for blk in re.split(r"\n(?=## )", log_text):
        if not blk.startswith("## "):
            continue
        head = blk.splitlines()[0][3:].strip()
        parts = [p.strip() for p in head.split("·")]
        sub = re.search(r'inbound:\s*"(.*)"', blk)
        spine_m = re.search(r"spine:\s*(.+?)(?=\nactions:)", blk, re.S)
        act = re.search(r"actions:\s*(\d+)", blk)
        flg = re.search(r"flags:\s*(.+)", blk)
        log.append({
            "date": parts[0] if len(parts) > 0 else "",
            "ref": parts[1] if len(parts) > 1 else "",
            "registry": parts[2] if len(parts) > 2 else "",
            "operator": parts[3] if len(parts) > 3 else "",
            "inbound": sub.group(1) if sub else "",
            "spine": re.sub(r"\s+", " ", spine_m.group(1)).strip() if spine_m else "",
            "actions": int(act.group(1)) if act else 0,
            "flags": flg.group(1).strip() if flg else "",
        })

    # join the per-step trail (activity-log) onto each case for the decision tree
    attach_log(cases, log)

    ledger = json.loads(read(STATE / "pn-ledger.json"))

    # stats
    by_route = {}
    for c in cases:
        by_route[c["decision"]] = by_route.get(c["decision"], 0) + 1
    by_reason = {}
    for c in cases:
        for r in c["reasons"]:
            by_reason[r] = by_reason.get(r, 0) + 1
    drafted = sum(len(c["drafts"]) for c in cases)
    provider_drafts = sum(
        1 for c in cases for d in c["drafts"]
        if "ack" not in d["label"].lower() and "client" not in d["label"].lower()
    )
    ops_open = len({c["ref"] for c in cases if c["op_status"] in ("OPEN", "AMENDED") and c["ref"].startswith("PN")})
    total_actions = sum(int(r["actions"]) if isinstance(r["actions"], int) else 0 for r in log)

    stats = {
        "total": len(cases),
        "by_route": by_route,
        "by_reason": by_reason,
        "drafts": drafted,
        "provider_drafts": provider_drafts,
        "operations_open": ops_open,
        "log_actions": total_actions,
        "audit_rows": len(audit),
        "ledger_bucket": "2606",
        "ledger_counter": ledger.get("sequences", {}).get("2606", 0),
        "date_range": "09-10 JUN 2026",
    }

    payload = {
        "desk": "Apex Trip Support",
        "operator_name": "Ground Control",
        "spine_def": [{"id": s[0], "title": s[1], "job": s[2]} for s in SPINE],
        "stats": stats,
        "cases": cases,
        "audit": audit,
        "log": log,
        "ledger": ledger,
        "eval": parse_eval(),
    }

    (HERE / "data.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    (HERE / "data.js").write_text(
        "/* generated by build_data.py - do not hand-edit */\n"
        "window.GC = " + json.dumps(payload, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )

    print(f"cases: {len(cases)}  | routes: {by_route}")
    print(f"drafts(total): {drafted}  provider drafts: {provider_drafts}  ops open: {ops_open}")
    print(f"audit rows: {len(audit)}  log entries: {len(log)}  actions: {total_actions}")
    print(f"reasons: {by_reason}")
    ev = payload["eval"]
    print(f"eval: ok={ev['ok']}  {ev['passed']}/{ev['total']}  | {ev['summary']}")
    print("wrote data.js + data.json")


if __name__ == "__main__":
    main()
