/* console.js - the operations console. Renders the inbox, the per-email
   pipeline (inbound -> decision tree -> operation), the generated emails, and
   the whole-desk status board. All from window.GC (real corpus data). */
(function () {
  "use strict";
  var GC = window.GC || {};
  var cases = GC.cases || [];
  var stats = GC.stats || {};
  var filter = "ALL";
  var selected = null;

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c];
    });
  }

  /* ---------- human approval gate (trust boundary: exfiltration lock) ----------
     Drafts are staged, never sent: every HANDLE case with drafts sits in the
     approval queue until a human releases or holds it. Demo state persists in
     localStorage; in a wired desk this would be the runtime's send gate. */
  var APPR_KEY = "gc-approvals";
  function apprState() {
    try { return JSON.parse(localStorage.getItem(APPR_KEY) || "{}"); } catch (e) { return {}; }
  }
  function setAppr(id, v) {
    var s = apprState();
    if (v) s[id] = v; else delete s[id];
    try { localStorage.setItem(APPR_KEY, JSON.stringify(s)); } catch (e) {}
  }
  function needsApproval(c) { return c.decision === "HANDLE" && c.drafts && c.drafts.length > 0; }
  function apprOf(c) {
    // clamp to the three known states — localStorage is untrusted input for innerHTML
    var v = apprState()[c.id];
    return v === "approved" || v === "rejected" ? v : "pending";
  }
  function apprCounts() {
    var n = { pending: 0, approved: 0, rejected: 0 };
    cases.forEach(function (c) { if (needsApproval(c)) n[apprOf(c)]++; });
    return n;
  }
  function $(id) { return document.getElementById(id); }
  function tail(c) {
    var t = (c.inbound.subject || "").split("|")[0].trim();
    return /[0-9-]/.test(t) && t.length <= 9 ? t : (c.operator.code || "-");
  }
  // a DOING line reads "<ICAO> · <service> -> <provider> [cc ...] [(email)]".
  // split on the arrow so "hotel (named)" and trailing notes don't break it.
  function parseDoing(line) {
    var ack = /(^|\s)ack\b|client ack/i.test(line);
    var em = (line.match(/\(([^)]*@[^)]+)\)/) || [])[1] ||
             (line.match(/[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]+/) || [])[0] || "";
    var cc = /cc\s*procurement/i.test(line) ? "procurement"
           : /cc\s*accounting/i.test(line) ? "accounting" : "";
    var leg = "", svc = "", who = line;
    var parts = line.split("→");
    if (parts.length > 1) {
      var lhs = parts[0].trim();
      var rhs = parts.slice(1).join("→").trim();
      var lm = lhs.match(/^([A-Z0-9]+)\s*·\s*(.+)$/);
      if (lm) { leg = lm[1]; svc = lm[2].replace(/\s*\(.*$/, "").trim(); }
      who = rhs.replace(/\s*cc\b.*/i, "").replace(/⛑.*$/, "").replace(/\s*\([^)]*\)\s*$/, "").trim();
    }
    if (ack) { leg = "ack"; }
    return { leg: leg, svc: svc, who: who, cc: cc, email: em, ack: ack };
  }

  // a service line that produces no email: flagged (no provider) or inbound-only.
  var NO_EMAIL = /FLAGGED|INBOUND|no draft/i;

  /* ---------- ribbon ---------- */
  function renderRibbon() {
    var r = stats.by_route || {};
    var ap = apprCounts();
    $("ribbon").innerHTML =
      '<div class="m"><b>' + (stats.total || 0) + '</b> inbound</div>' +
      '<div class="m go"><b>' + (r.HANDLE || 0) + '</b> handle</div>' +
      '<div class="m at"><b>' + (r.ESCALATE || 0) + '</b> escalate</div>' +
      '<div class="m"><b>' + (r.DROP || 0) + '</b> drop</div>' +
      '<div class="m"><b>' + (stats.drafts || 0) + '</b> drafts</div>' +
      '<div class="m at"><b>' + ap.pending + '</b> awaiting approval</div>' +
      '<div class="m">ledger <b>' + esc(stats.ledger_bucket) + ' · ' + (stats.ledger_counter || 0) + '</b></div>';
  }
  renderRibbon();

  /* ---------- inbox ---------- */
  function renderInbox() {
    var list = cases.filter(function (c) { return filter === "ALL" || c.decision === filter; });
    $("inbox-count").textContent = list.length + " / " + cases.length;
    $("inbox-list").innerHTML = list.map(function (c) {
      var ap = needsApproval(c)
        ? '<span class="apch ' + apprOf(c) + '" title="human approval: ' + apprOf(c) + '"></span>'
        : "";
      return '<div class="mailrow' + (selected === c.id ? " sel" : "") + '" data-id="' + c.id + '">' +
        '<span class="op">' + esc(c.operator.name) + '</span>' +
        '<span class="rdot ' + c.decision + '" title="' + c.decision + '"></span>' + ap +
        '<span class="reg">' + esc(tail(c)) + '</span>' +
        '<span class="subj">' + esc(c.inbound.subject) + '</span>' +
        '</div>';
    }).join("");
    $("inbox-list").querySelectorAll(".mailrow").forEach(function (row) {
      row.addEventListener("click", function () { select(row.getAttribute("data-id")); });
    });
  }

  /* ---------- decision tree ---------- */
  function decisionTree(c) {
    var nd = c.node_detail || {};
    var nodes = c.spine.map(function (s) {
      var det = nd[s.id] || "";
      var out = det ? '<div class="out"><span class="lbl">Output</span>' + esc(det) + '</div>' : "";
      var reason = "";
      if (s.state === "stop" && c.decision === "ESCALATE") {
        reason = '<div class="reason">routes to ' + esc(c.route_to || "a human queue") +
                 (c.reasons.length ? '  ·  ' + esc(c.reasons.join(" + ")) : "") + '</div>';
      }
      return '<div class="dnode ' + s.state + '">' +
        '<div class="rail"><span class="mk">' + esc(s.id) + '</span><span class="ln"></span></div>' +
        '<div class="c"><div class="st">' + esc(s.title) + '</div>' +
        '<div class="jb">' + esc(s.job) + '</div>' + out + reason + '</div></div>';
    }).join("");
    var acts = (c.log && c.log.actions != null) ? '  ·  ' + c.log.actions + ' action' + (c.log.actions === 1 ? '' : 's') : "";

    var badge = '<span class="badge ' + c.decision.toLowerCase() + '"><span class="dot"></span>' + c.decision + '</span>';
    var desc = c.decision === "HANDLE"
      ? (c.intent === "FYI"
          ? "Provider confirmation on a live thread. Recorded as FYI, no outbound, reference reused."
          : "Cleared every gate. Operation " + c.ref + " opened, drafts written, client reply ready.")
      : c.decision === "ESCALATE"
        ? "Stopped at the firing gate. Nothing drafted, briefing routed to " + (c.route_to || "a human queue") + "."
        : esc(c.summary || "Filtered at the scope gate.");
    var outcome = '<div class="outcome"><div class="oh">' + badge +
      '<span class="mono" style="font-size:12px;color:var(--faint)">' + esc(c.intent) + ' · ' + esc(c.op_status) + acts + '</span></div>' +
      '<div class="od">' + desc + '</div></div>';

    return '<div class="dtree">' + nodes + '</div>' + outcome;
  }

  /* ---------- center pane ---------- */
  function renderCenter(c) {
    var inb = c.inbound;
    var head =
      '<div class="block"><div class="bh">Inbound</div>' +
      '<div class="mailhead">' +
        '<div>from <b>' + esc(inb.from_name) + '</b> &lt;' + esc(inb.from_email) + '&gt;</div>' +
        '<div>' + esc(inb.date) + '</div>' +
        '<div>subject <b>' + esc(inb.subject) + '</b></div>' +
      '</div>' +
      '<div class="mailbody">' + esc(inb.body) + '</div></div>';

    var tree =
      '<div class="block"><div class="bh">Decision tree</div>' +
      decisionTree(c) + '</div>';

    // the Operation block lives in the Outbox for approvable cases, so the
    // human reads what they're approving right above the Approve button;
    // op-fallback keeps it visible here when the outbox pane is collapsed
    var op = needsApproval(c) ? opBlock(c, "op-fallback") : opBlock(c);

    var flags = "";
    if (c.flags && c.flags.length) {
      flags = '<div class="block"><div class="bh">Flags for a human</div><div class="tflags">' +
        c.flags.map(function (f) {
          return '<div class="f"><span class="b">!</span><span>' + esc(f) + '</span></div>';
        }).join("") + '</div></div>';
    }

    $("center").innerHTML = head + tree + op + flags;
    $("center").scrollTop = 0;
  }

  /* ---------- operation block (shared: center pane / outbox) ---------- */
  function opBlock(c, extraClass) {
    if (!c.trip_record) return "";
    var chips = (c.services || []).map(function (s) {
      return '<span class="chip ' + s.status + '">' + esc(s.name) + ' <b>' + esc(s.status) + '</b></span>';
    }).join("");
    return '<div class="block' + (extraClass ? " " + extraClass : "") + '"><div class="bh">Operation</div>' +
      '<div class="trip">' + esc(c.trip_record) + '</div>' +
      (chips ? '<div class="svc-chips">' + chips + '</div>' : "") + '</div>';
  }

  /* ---------- outbox pane ---------- */
  function renderOutbox(c) {
    var out = $("outbox");
    if (c.decision === "ESCALATE") {
      out.innerHTML =
        '<div class="pane-h"><span class="t">Outbox</span><span class="ct">briefing</span></div>' +
        '<div class="escflag">' + esc(c.escalation_flag) + '</div>' +
        (c.route_to ? '<div class="routeto">Routed to <b>' + esc(c.route_to) + '</b>. No provider or client was contacted.</div>' : "");
      return;
    }
    if (c.decision === "DROP") {
      out.innerHTML =
        '<div class="pane-h"><span class="t">Outbox</span><span class="ct">none</span></div>' +
        '<div class="empty">Dropped at the scope filter. Nothing drafted, nothing queued.</div>';
      return;
    }
    // HANDLE
    if (!c.drafts.length) {
      out.innerHTML =
        '<div class="pane-h"><span class="t">Outbox</span><span class="ct">no outbound</span></div>' +
        '<div class="empty" style="color:var(--go)">Inbound provider confirmation. Recorded against ' + esc(c.ref) + ', service set to CONFIRMED. No email generated.</div>';
      return;
    }
    // ONE ordered list of the emails the pipeline wrote: recipient, address, cc,
    // service status, and the body. Service lines that get NO email (flagged or
    // inbound-only) are listed under it, so the count difference is explained.
    var sendable = (c.doing || []).filter(function (d) { return !NO_EMAIL.test(d); });
    var staged = c.drafts.map(function (d, i) {
      var isAck = /\back\b|client/i.test(d.label);
      var p = i < sendable.length ? parseDoing(sendable[i]) : {};
      var who = isAck ? (c.operator.name + " (client)") : (p.who || d.label);
      var leg = isAck ? "reply" : (p.leg || "");
      var svc = isAck ? "acknowledgment" : (p.svc || "");
      var to = p.email || d.to || "";
      var svcStatus = (c.services.find(function (s) { return s.name === svc; }) || {}).status;
      var status = isAck ? "DRAFTED" : (svcStatus || "REQUESTED");
      return '<details class="semail"' + (i === 0 ? " open" : "") + '>' +
        '<summary>' +
          '<span class="n">' + (i + 1).toString().padStart(2, "0") + '</span>' +
          '<span class="meta">' +
            '<span class="r1"><b>' + esc(who) + '</b><span class="stat ' + status + '">' + status + '</span></span>' +
            '<span class="r2">' + (leg ? esc(leg) + ' · ' : "") + esc(svc) +
              ' · to ' + (to ? esc(to) : '<i>TBC</i>') + (p.cc ? ' · cc ' + esc(p.cc) : "") + '</span>' +
          '</span>' +
          '<span class="car" aria-hidden="true">&#9656;</span>' +
        '</summary>' +
        '<div class="dbody">' + esc(d.body) + '</div></details>';
    }).join("");

    var heldLines = (c.doing || []).filter(function (d) { return NO_EMAIL.test(d); });
    var held = heldLines.length
      ? '<div class="notemail"><span class="nh">No email sent</span>' +
        heldLines.map(function (d) {
          var p = parseDoing(d);
          var why = /INBOUND/i.test(d) ? "inbound-only provider, booked on their own channel"
                                       : "no provider on file, a human sources it";
          return '<div class="nm">' + esc((p.leg ? p.leg + " · " : "") + (p.svc || "")) + ' · ' + why + '</div>';
        }).join("") + '</div>'
      : "";

    var st = apprOf(c);
    var approval =
      '<div class="approval ' + st + '">' +
        '<div class="ah"><span class="al">Human approval gate</span>' +
          '<span class="as">' + (st === "pending" ? "PENDING APPROVAL"
                               : st === "approved" ? "APPROVED · RELEASED" : "REJECTED · HELD") + '</span></div>' +
        '<div class="ad">' + (st === "pending"
            ? "Drafts are staged, never sent (trust boundary: approval gate). Review the " +
              c.drafts.length + " draft" + (c.drafts.length === 1 ? "" : "s") +
              " below. Nothing leaves the desk until a human releases it."
            : st === "approved"
              ? "Released by a human. The " + c.drafts.length + " draft" + (c.drafts.length === 1 ? "" : "s") + " count as sent."
              : "Held by a human. Nothing was sent; the case stays on the desk.") + '</div>' +
        '<div class="ab">' +
          (st !== "approved" ? '<button class="appr-btn ok" data-a="approved">Approve &amp; release</button>' : "") +
          (st !== "rejected" ? '<button class="appr-btn no" data-a="rejected">Reject &amp; hold</button>' : "") +
          (st !== "pending" ? '<button class="appr-btn rs" data-a="">Reset to pending</button>' : "") +
        '</div></div>';

    // top-down read: what the operation is -> the approve decision -> the staged emails
    out.innerHTML =
      '<div class="pane-h"><span class="t">Outbox</span><span class="ct">' + c.drafts.length + ' email' + (c.drafts.length === 1 ? '' : 's') + ' staged</span></div>' +
      opBlock(c) + approval +
      '<div class="staged-h">Staged emails<span>written and queued. They go out only after you approve.</span></div>' +
      staged + held;

    out.querySelectorAll(".appr-btn").forEach(function (b) {
      b.addEventListener("click", function () {
        setAppr(c.id, b.getAttribute("data-a") || null);
        renderOutbox(c);
        renderRibbon();
        renderInbox();
        renderBoard();
      });
    });
  }

  function select(id) {
    var c = cases.find(function (x) { return x.id === id; });
    if (!c) return;
    selected = id;
    renderInbox();
    renderCenter(c);
    renderOutbox(c);
  }

  /* ---------- status board ---------- */
  function renderBoard() {
    var r = stats.by_route || {};
    var rows = cases.map(function (c) {
      return '<tr><td class="mono" style="color:var(--faint);font-size:11px">' + esc(c.inbound.date.split(",").pop().trim().slice(0, 9) || "") + '</td>' +
        '<td class="ref">' + esc(c.ref) + '</td>' +
        '<td class="op"><b>' + esc(c.operator.name) + '</b><div class="mono" style="font-size:10.5px;color:var(--faint)">' + esc(tail(c)) + '</div></td>' +
        '<td><span class="badge ' + c.decision.toLowerCase() + '"><span class="dot"></span>' + c.decision + '</span></td>' +
        '<td class="mono" style="font-size:11.5px;color:var(--muted)">' + esc(c.op_status) + '</td>' +
        '<td class="mono" style="font-size:11px;color:var(--faint)">' + esc(c.reasons.join(", ") || "-") + '</td></tr>';
    }).join("");

    var maxReason = Math.max.apply(null, Object.values(stats.by_reason || { x: 1 }));
    var bars = Object.keys(stats.by_reason || {}).sort(function (a, b) {
      return stats.by_reason[b] - stats.by_reason[a];
    }).map(function (k) {
      var v = stats.by_reason[k];
      return '<div class="rb"><span class="nm">' + esc(k) + '</span><span class="ct">' + v + '</span>' +
        '<span class="bar"><i style="width:' + Math.round((v / maxReason) * 100) + '%"></i></span></div>';
    }).join("");

    $("view-status").innerHTML =
      '<div class="board-grid">' +
        '<div class="left">' +
          '<h3>Every inbound, processed</h3>' +
          '<table class="optable"><thead><tr><th>Date</th><th>Ref</th><th>Operator</th><th>Route</th><th>Status</th><th>Reason</th></tr></thead>' +
          '<tbody>' + rows + '</tbody></table>' +
        '</div>' +
        '<div class="right">' +
          '<div class="miniband">' +
            '<div class="m go"><div class="n">' + (r.HANDLE || 0) + '</div><div class="l">Handled</div></div>' +
            '<div class="m at"><div class="n">' + (r.ESCALATE || 0) + '</div><div class="l">Escalated</div></div>' +
            '<div class="m"><div class="n">' + (r.DROP || 0) + '</div><div class="l">Dropped</div></div>' +
            '<div class="m"><div class="n">' + (stats.drafts || 0) + '</div><div class="l">Drafted</div></div>' +
          '</div>' +
          '<div class="sub">Escalations by reason</div>' +
          '<div class="reasonbars">' + bars + '</div>' +
          '<div class="sub">PN ledger</div>' +
          '<div class="trip" style="font-size:12px">bucket ' + esc(stats.ledger_bucket) + '  ·  counter ' + (stats.ledger_counter || 0) +
            '  ·  next ' + esc("PN" + stats.ledger_bucket + String((stats.ledger_counter || 0) + 1).padStart(3, "0")) + '</div>' +
          '<div class="sub">Approval queue (human gate)</div>' +
          '<div class="trip" style="font-size:12px">' + (function () {
            var ap = apprCounts();
            return ap.pending + ' pending  ·  ' + ap.approved + ' released  ·  ' + ap.rejected +
              ' held  ·  drafts are staged, never sent (reference/trust-boundary.md)';
          })() + '</div>' +
          '<div class="sub">Audit trail</div>' +
          '<div class="trip" style="font-size:12px">' + (stats.audit_rows || 0) + ' action rows in results.csv  ·  ' +
            (GC.log ? GC.log.length : 0) + ' step-trail entries in activity-log.md</div>' +
        '</div>' +
      '</div>';
  }

  /* ---------- view tabs ---------- */
  function setView(v) {
    var pipe = $("view-pipeline"), board = $("view-status");
    var tp = $("tab-pipeline"), ts = $("tab-status");
    if (v === "status") {
      pipe.style.display = "none"; board.hidden = false;
      ts.classList.add("on"); tp.classList.remove("on");
      if (location.hash !== "#status") history.replaceState(null, "", "#status");
    } else {
      pipe.style.display = ""; board.hidden = true;
      tp.classList.add("on"); ts.classList.remove("on");
      if (location.hash === "#status") history.replaceState(null, "", "#pipeline");
    }
  }
  $("tab-pipeline").addEventListener("click", function () { setView("pipeline"); });
  $("tab-status").addEventListener("click", function () { setView("status"); });

  $("filters").querySelectorAll("button").forEach(function (b) {
    b.addEventListener("click", function () {
      filter = b.getAttribute("data-f");
      $("filters").querySelectorAll("button").forEach(function (x) { x.classList.remove("on"); });
      b.classList.add("on");
      renderInbox();
    });
  });

  /* ---------- boot ---------- */
  renderInbox();
  renderBoard();
  if (cases.length) select(cases[0].id);
  if (location.hash === "#status") setView("status");
})();
