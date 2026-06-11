/* landing.js - binds real corpus data into the hero artifact, stat band and
   spine flow, and runs scroll reveals. No scroll listeners (IntersectionObserver
   + CSS). Honors prefers-reduced-motion. */
(function () {
  "use strict";
  var GC = window.GC || {};
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c];
    });
  }

  /* ---- stat band (sync from data so it tracks the corpus) ---- */
  if (GC.stats) {
    var s = GC.stats, r = s.by_route || {};
    var map = {
      total: s.total,
      handle: r.HANDLE,
      escalate: r.ESCALATE,
      drop: r.DROP,
      drafts: s.drafts,
      ops: s.operations_open,
      reasons: Object.keys(s.by_reason || {}).length,
      adversarial: (GC.cases || []).filter(function (c) { return /^S/.test(c.id); }).length,
    };
    document.querySelectorAll("[data-stat]").forEach(function (n) {
      var v = map[n.getAttribute("data-stat")];
      if (v != null) n.textContent = v;
    });
  }

  /* ---- hero artifact: render a real HANDLE decision card (case 07) ---- */
  (function heroCard() {
    var host = document.getElementById("hero-artifact");
    if (!host || !GC.cases) return;
    var c = GC.cases.find(function (x) { return x.id === "07"; }) ||
            GC.cases.find(function (x) { return x.decision === "HANDLE" && x.doing.length >= 3; });
    if (!c) return;

    var hdr = '<span><b>DECISION</b> ' + esc(c.decision) + '</span>' +
              '<span><b>INTENT</b> ' + esc(c.intent) + '</span>' +
              '<span><b>REF</b> ' + esc(c.ref) + '</span>';

    var doing = c.doing.map(function (d) {
      // doing line looks like: "LFPB · handling -> Provider   cc ...   (email)"
      var m = d.match(/^([A-Z0-9]+)\s*·\s*([a-z_]+)\s*→\s*([^(]+?)\s*(?:cc[^(]*)?(?:\(([^)]+)\))?$/i);
      var leg = m ? m[1] : "";
      var who = m ? m[3].trim() : d;
      var em = m && m[4] ? m[4] : "";
      if (/ack/i.test(d)) { leg = "ack"; }
      return '<div class="row"><span class="leg">' + esc(leg) + '</span>' +
             '<span class="who">' + esc(who) + '</span>' +
             '<span class="em">' + esc(em) + '</span></div>';
    }).join("");

    host.innerHTML =
      '<div class="artifact">' +
        '<div class="top"><span class="lights"><i></i><i></i><i></i></span>' +
          '<span class="ttl">decision-card · ' + esc(c.case_id) + '</span></div>' +
        '<div class="body">' +
          '<div class="hdr">' + hdr + '</div>' +
          '<div class="sum">' + esc(c.summary) + '</div>' +
          '<div class="doing">' + doing + '</div>' +
        '</div>' +
      '</div>';
  })();

  /* ---- spine flow ---- */
  (function spineFlow() {
    var host = document.getElementById("spine-flow");
    if (!host || !GC.spine_def) return;
    var branch = {
      S0: "→ <b>DROP</b> noise / billing &nbsp;·&nbsp; FYI",
      S1: "→ <b>ESCALATE</b> unknown / spoofed sender / military / diplomatic / credit hold",
      S2: "→ <b>ESCALATE</b> cancel booked work",
      S3: "→ <b>ESCALATE</b> incomplete skeleton",
      S4: "→ <b>ESCALATE</b> permit / fuel / flight-plan / no anchor",
      S5: "search the provider DB by station → provider, or FLAGGED for a human",
      S6: "→ <b>ESCALATE</b> low confidence",
      S7: "CC by matrix · recipients locked · staged for approval",
      S8: "→ <b>HANDLE</b> operation opened",
    };
    GC.spine_def.forEach(function (st) {
      var node = el("div", "spine-step");
      node.innerHTML =
        '<div class="sid"><span class="num">' + esc(st.id) + '</span></div>' +
        '<div><div class="ttl">' + esc(st.title) + '</div>' +
        '<div class="job">' + esc(st.job) + '</div></div>' +
        '<div class="branch">' + (branch[st.id] || "") + '</div>';
      host.appendChild(node);
    });
  })();

  /* ---- eval: compact live regression-harness readout (de-emphasized) ---- */
  (function evalBlock() {
    var e = GC.eval;
    if (!e) return;
    var mini = document.getElementById("eval-mini");
    if (!mini) return;
    mini.innerHTML =
      '<div class="cmd"><span class="pr0">$</span> ' + esc(e.command) + '</div>' +
      '<div class="res"><span class="ok">' + (e.ok ? "ALL PASS" : "see output") +
      '</span> <b>' + esc(e.passed) + ' / ' + esc(e.total) + '</b> golden cases green</div>';
  })();

  /* ---- scroll reveals (IntersectionObserver, no scroll handlers) ---- */
  if (reduce || !("IntersectionObserver" in window)) {
    document.querySelectorAll(".reveal, .spine-flow, .routes-bento").forEach(function (n) { n.classList.add("in"); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
    });
  }, { threshold: 0.16 });
  document.querySelectorAll(".reveal:not(.in), .spine-flow, .routes-bento").forEach(function (n) { io.observe(n); });

  // staggered draw-in for spine steps once the flow is visible
  var flow = document.getElementById("spine-flow");
  if (flow) {
    var sio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        flow.querySelectorAll(".spine-step").forEach(function (step, i) {
          step.style.transitionDelay = (i * 0.06) + "s";
        });
        flow.classList.add("in");
        sio.unobserve(flow);
      });
    }, { threshold: 0.12 });
    sio.observe(flow);
  }
})();
