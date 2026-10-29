// The listening ledger: everything is computed here, from the log the player keeps in
// localStorage ("cl:listening") and the catalogue in library.json. Nothing leaves the browser.

const LOG_KEY = "cl:listening";
const $ = (id) => document.getElementById(id);
const SVG = "http://www.w3.org/2000/svg";
const LATE = (h) => h >= 23 || h < 4;          // late night: 11 pm to 4 am

function readLog() {
  try {
    const v = JSON.parse(localStorage.getItem(LOG_KEY) || "[]");
    return Array.isArray(v) ? v.filter((e) => e && e.t && e.s > 0) : [];
  } catch { return []; }
}

// ---- Dates ----
const dayStart = (ms) => { const d = new Date(ms); d.setHours(0, 0, 0, 0); return d.getTime(); };
const addDays = (ms, n) => { const d = new Date(ms); d.setDate(d.getDate() + n); return d.getTime(); };
const weekStart = (ms) => { const d = new Date(dayStart(ms)); d.setDate(d.getDate() - ((d.getDay() + 6) % 7)); return d.getTime(); };
const shortDate = (ms) => new Date(ms).toLocaleDateString("en-GB", { day: "numeric", month: "short" });
const hourName = (h) => (h === 0 ? "midnight" : h === 12 ? "noon" : h < 12 ? `${h} am` : `${h - 12} pm`);
const isoDay = (ms) => { const d = new Date(ms); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`; };
const minutes = (s) => Math.round(s / 60);
const pct = (x) => `${Math.round(x * 100)}%`;

// ---- What the music was doing during one stretch, in seconds ----
let LIB = null;            // library.json
let tracks = new Map();   // "album|n" -> { work, track }
function features(e) {
  const hit = tracks.get(`${e.k}|${e.n}`);
  const f = { minor: 0, major: 0, slow: 0, moderate: 0, fast: 0, quiet: 0, middle: 0, loud: 0 };
  if (!hit) return f;
  const t = hit.track, dur = t.duration || 0;
  const mode = /minor$/.test(t.key) ? "minor" : /major$/.test(t.key) ? "major" : null;
  for (let x = e.a; x < e.a + e.s; x += 10) {
    const w = Math.min(10, e.a + e.s - x), mid = x + w / 2;
    if (mode) f[mode] += w;
    // Compound markings are spread evenly across the movement, as on the stage.
    if (t.pace?.length && dur) {
      const p = t.pace[Math.min(t.pace.length - 1, Math.floor((mid / dur) * t.pace.length))];
      if (p !== null && p !== undefined) f[p <= 2 ? "slow" : p >= 4 ? "fast" : "moderate"] += w;
    }
    const mark = t.loud?.[Math.floor(mid / 10)];
    if (mark) f[{ q: "quiet", m: "middle", l: "loud" }[mark]] += w;
  }
  return f;
}

// Shares for a set of stretches; null where nothing in them carries that information.
function summarise(entries) {
  const sum = { total: 0, late: 0, minor: 0, major: 0, slow: 0, moderate: 0, fast: 0, quiet: 0, middle: 0, loud: 0 };
  for (const e of entries) {
    sum.total += e.s;
    if (LATE(new Date(e.t).getHours())) sum.late += e.s;
    const f = features(e);
    for (const k in f) sum[k] += f[k];
  }
  const share = (a, ...rest) => { const d = a + rest.reduce((x, y) => x + y, 0); return d > 0 ? a / d : null; };
  return {
    ...sum,
    minorShare: share(sum.minor, sum.major),
    slowShare: share(sum.slow, sum.moderate, sum.fast),
    fastShare: share(sum.fast, sum.moderate, sum.slow),
    quietShare: share(sum.quiet, sum.middle, sum.loud),
    loudShare: share(sum.loud, sum.middle, sum.quiet),
    lateShare: sum.total ? sum.late / sum.total : null,
  };
}

// ---- Reflection: one or two sentences from rules, always with the numbers ----
function reflect(cur, prev) {
  const m = minutes(cur.total);
  if (m < 10) return [`Only ${m} minute${m === 1 ? "" : "s"} so far this week, not enough to read much from the music yet.`];
  const leans = [], numbers = [];
  if (cur.minorShare !== null && cur.minorShare >= 0.5) { leans.push("minor"); numbers.push(`${pct(cur.minorShare)} of the time in minor keys`); }
  else if (cur.minorShare !== null && cur.minorShare <= 0.3) { leans.push("major"); numbers.push(`${pct(1 - cur.minorShare)} in major keys`); }
  if (cur.slowShare !== null && cur.slowShare >= 0.5) { leans.push("slow"); numbers.push(`${pct(cur.slowShare)} at Andante or slower`); }
  else if (cur.fastShare !== null && cur.fastShare >= 0.5) { leans.push("fast"); numbers.push(`${pct(cur.fastShare)} at Allegro or quicker`); }
  if (cur.quietShare !== null && cur.quietShare >= 0.45) { leans.push("quiet"); numbers.push(`${pct(cur.quietShare)} in the library’s quietest passages`); }
  else if (cur.loudShare !== null && cur.loudShare >= 0.45) { leans.push("loud"); numbers.push(`${pct(cur.loudShare)} in its loudest`); }
  const list = (xs) => (xs.length < 2 ? xs.join("") : xs.slice(0, -1).join(", ") + " and " + xs[xs.length - 1]);
  const out = [];
  if (leans.length) out.push(`This week leaned ${list(leans)}: ${list(numbers)}.`);
  else out.push(`This week was evenly mixed: ${pct(cur.minorShare ?? 0)} minor, ${pct(cur.slowShare ?? 0)} slow, ${pct(cur.fastShare ?? 0)} fast.`);

  // Then the hour, or the biggest change since last week.
  let second = "";
  if (cur.lateShare >= 0.5) second = `Most of it came after 11 pm (${pct(cur.lateShare)} of ${m} minutes)`;
  else if (cur.lateShare >= 0.3) second = `Much of it came after 11 pm (${pct(cur.lateShare)} of ${m} minutes)`;
  if (prev && prev.total >= 15 * 60) {
    const changes = [["minorShare", "minor"], ["slowShare", "slow"], ["quietShare", "quiet"], ["lateShare", "late at night"]]
      .filter(([k]) => cur[k] !== null && prev[k] !== null)
      .map(([k, word]) => ({ word, a: cur[k], b: prev[k], d: cur[k] - prev[k] }))
      .filter((c) => Math.abs(c.d) >= 0.15)
      .sort((x, y) => Math.abs(y.d) - Math.abs(x.d));
    if (changes[0]) {
      const c = changes[0];
      const phrase = `${c.d > 0 ? "more" : "less"} ${c.word} than last week (${pct(c.a)} against ${pct(c.b)})`;
      second = second ? `${second}, and ${phrase}` : phrase.charAt(0).toUpperCase() + phrase.slice(1);
    }
  }
  if (second) out.push(second + ".");
  return out;
}

// ---- Drawing ----
const el = (tag, attrs = {}, text) => {
  const n = document.createElementNS(SVG, tag);
  for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
  if (text !== undefined) n.textContent = text;
  return n;
};
const svg = (w, h) => el("svg", { viewBox: `0 0 ${w} ${h}`, width: w, height: h, role: "img" });

function drawDays(entries, today) {
  const fig = $("days"), W = Math.max(300, fig.clientWidth), H = 220, pad = 28;
  const days = Array.from({ length: 14 }, (_, i) => addDays(today, i - 13));
  const totals = days.map((d) => entries.filter((e) => e.t >= d && e.t < addDays(d, 1)).reduce((s, e) => s + e.s, 0));
  const max = Math.max(60 * 30, ...totals);
  const s = svg(W, H);
  s.setAttribute("aria-label", "Minutes per day: " + days.map((d, i) => `${shortDate(d)} ${minutes(totals[i])}`).join(", "));
  const step = (W - 8) / 14, bw = Math.min(34, step * 0.62), base = H - pad;
  for (const f of [0.5, 1]) s.append(el("line", { x1: 0, x2: W, y1: base - (base - 24) * f, y2: base - (base - 24) * f, class: "rule" }));
  s.append(el("line", { x1: 0, x2: W, y1: base, y2: base, class: "axis" }));
  days.forEach((d, i) => {
    const x = 4 + i * step + (step - bw) / 2, h = ((base - 24) * totals[i]) / max, now = i === 13;
    if (totals[i] > 0) {
      s.append(el("rect", { x, y: base - h, width: bw, height: h, fill: `url(#${now ? "hatch-amber" : "hatch"})`, class: "bar" + (now ? " now" : "") }));
      s.append(el("text", { x: x + bw / 2, y: base - h - 6, "text-anchor": "middle", class: "val" }, minutes(totals[i])));
    }
    const label = W < 520 && i % 2 ? "" : new Date(d).toLocaleDateString("en-GB", { weekday: "short", day: "numeric" });
    s.append(el("text", { x: x + bw / 2, y: base + 17, "text-anchor": "middle" }, label));
  });
  if (!totals.some(Boolean)) s.append(el("text", { x: W / 2, y: base / 2 + 10, "text-anchor": "middle", class: "note" }, "No entries in the last fourteen days."));
  fig.replaceChildren(s);
}

function drawRanks(id, rows) {
  const list = $(id);
  if (!rows.length) { list.replaceChildren(Object.assign(document.createElement("li"), { className: "none", textContent: "Nothing yet." })); return; }
  const max = rows[0].s;
  list.replaceChildren(...rows.map((r) => {
    const li = document.createElement("li");
    const name = document.createElement("span");
    name.className = "name";
    name.textContent = r.name;
    if (r.sub) { const sm = document.createElement("small"); sm.textContent = r.sub; name.append(sm); }
    const m = document.createElement("span");
    m.className = "mins";
    m.textContent = `${minutes(r.s)} min`;
    const bar = el("svg", { viewBox: "0 0 100 8", preserveAspectRatio: "none", "aria-hidden": "true" });
    bar.append(el("rect", { x: 0, y: 0.5, width: Math.max(1, (100 * r.s) / max), height: 7, fill: "url(#hatch)", stroke: "#e8e1d4", "stroke-width": 0.4, "vector-effect": "non-scaling-stroke" }));
    li.append(name, m, bar);
    return li;
  }));
}

// A 24-hour dial, midnight at the top; each hour a hatched wedge as long as its minutes.
function drawClock(entries) {
  const fig = $("clock"), S = 400, c = S / 2, r0 = 62, R = 158;
  const byHour = Array(24).fill(0);
  for (const e of entries) byHour[new Date(e.t).getHours()] += e.s;
  const max = Math.max(...byHour, 1);
  const s = svg(S, S);
  const at = (h, r) => { const a = (h / 24) * Math.PI * 2 - Math.PI / 2; return [c + r * Math.cos(a), c + r * Math.sin(a)]; };
  s.append(el("circle", { cx: c, cy: c, r: r0, fill: "none", class: "axis" }));
  s.append(el("circle", { cx: c, cy: c, r: R, fill: "none", class: "rule", "stroke-dasharray": "2 4" }));
  // Late night, 11 pm to 4 am, marked in amber outside the dial.
  const [lx0, ly0] = at(23, R + 12), [lx1, ly1] = at(28, R + 12);
  s.append(el("path", { d: `M${lx0},${ly0} A${R + 12},${R + 12} 0 0 1 ${lx1},${ly1}`, fill: "none", stroke: "#d9a441", "stroke-width": 1.4 }));
  const [tx, ty] = at(1.5, R + 28);
  s.append(el("text", { x: tx, y: ty, "text-anchor": "start", fill: "#d9a441" }, "late night"));
  byHour.forEach((v, h) => {
    if (!v) return;
    const r = r0 + ((R - r0) * v) / max;
    const [a1, b1] = at(h + 0.06, r0), [a2, b2] = at(h + 0.06, r), [a3, b3] = at(h + 0.94, r), [a4, b4] = at(h + 0.94, r0);
    s.append(el("path", { d: `M${a1},${b1} L${a2},${b2} A${r},${r} 0 0 1 ${a3},${b3} L${a4},${b4} A${r0},${r0} 0 0 0 ${a1},${b1}Z`,
      fill: `url(#${LATE(h) ? "hatch-amber" : "hatch"})`, class: "bar" + (LATE(h) ? " now" : "") }));
  });
  for (const h of [0, 6, 12, 18]) {
    const [x, y] = at(h, R + 14 + (h === 0 ? 4 : 0));
    const anchor = h === 6 ? "start" : h === 18 ? "end" : "middle";
    s.append(el("text", { x, y: y + (h === 12 ? 12 : h === 0 ? -2 : 4), "text-anchor": anchor }, hourName(h)));
  }
  for (let h = 0; h < 24; h++) { const [x1, y1] = at(h, r0 - 6), [x2, y2] = at(h, r0); s.append(el("line", { x1, y1, x2, y2, class: "axis" })); }
  const peak = byHour.indexOf(Math.max(...byHour));
  if (byHour[peak]) {
    s.append(el("text", { x: c, y: c - 4, "text-anchor": "middle", class: "peak" }, "most often"));
    s.append(el("text", { x: c, y: c + 16, "text-anchor": "middle", class: "peak" }, `${hourName(peak)}–${hourName((peak + 1) % 24)}`));
  } else s.append(el("text", { x: c, y: c + 5, "text-anchor": "middle", class: "note" }, "no hours yet"));
  s.setAttribute("aria-label", "Minutes by hour of day: " + byHour.map((v, h) => `${hourName(h)} ${minutes(v)}`).filter((x) => !x.endsWith(" 0")).join(", "));
  fig.replaceChildren(s);
}

const MEASURES = [
  ["minorShare", "Minor keys", "of keyed music"],
  ["slowShare", "Slow tempi", "Andante or slower"],
  ["fastShare", "Fast tempi", "Allegro or quicker"],
  ["quietShare", "Quiet passages", "library’s softest third"],
  ["loudShare", "Loud passages", "library’s loudest third"],
  ["lateShare", "Late night", "11 pm to 4 am"],
];

function drawMeasures(cur) {
  $("measures").replaceChildren(...MEASURES.map(([k, label]) => {
    const row = document.createElement("div");
    const dt = document.createElement("dt"); dt.textContent = label;
    const dd = document.createElement("dd");
    const bar = el("svg", { viewBox: "0 0 100 14", preserveAspectRatio: "none", "aria-hidden": "true" });
    bar.append(el("rect", { x: 0, y: 0.5, width: 100, height: 13, fill: "url(#hatch-light)", opacity: 0.35 }));
    if (cur[k] !== null) bar.append(el("rect", { x: 0, y: 0.5, width: 100 * cur[k], height: 13, fill: "url(#hatch)", stroke: "#e8e1d4", "stroke-width": 0.6, "vector-effect": "non-scaling-stroke" }));
    dd.append(bar);
    const p = document.createElement("span"); p.className = "pct"; p.textContent = cur[k] === null ? "–" : pct(cur[k]);
    row.append(dt, dd, p);
    return row;
  }));
}

// Small multiples: the last eight weeks, one hatched column each, this week in amber.
function drawTrends(weeks) {
  const host = $("trends");
  const W = Math.max(280, host.clientWidth - (host.clientWidth > 760 ? 176 : 0)), H = 150, base = H - 24;
  host.replaceChildren(...MEASURES.map(([k, label, sub]) => {
    const row = document.createElement("div"); row.className = "trend";
    const h3 = document.createElement("h3"); h3.textContent = label;
    const sm = document.createElement("small"); sm.textContent = sub; h3.append(sm);
    const s = svg(W, H);
    s.setAttribute("aria-label", `${label} by week: ` + weeks.map((w) => `${shortDate(w.start)} ${w.sum[k] === null ? "no data" : pct(w.sum[k])}`).join(", "));
    const step = W / weeks.length, bw = Math.min(40, step * 0.5);
    s.append(el("line", { x1: 0, x2: W, y1: base, y2: base, class: "axis" }));
    weeks.forEach((w, i) => {
      const v = w.sum[k], x = i * step + (step - bw) / 2, now = i === weeks.length - 1;
      if (v === null) s.append(el("text", { x: x + bw / 2, y: base - 6, "text-anchor": "middle" }, "–"));
      else {
        const h = Math.max(1, (base - 26) * v);
        s.append(el("rect", { x, y: base - h, width: bw, height: h, fill: `url(#${now ? "hatch-amber" : "hatch"})`, class: "bar" + (now ? " now" : "") }));
        s.append(el("text", { x: x + bw / 2, y: base - h - 7, "text-anchor": "middle", class: "val" }, pct(v)));
      }
      // Narrow screens label every other week.
      const narrow = step < 64, label = now ? (narrow ? "now" : "this week") : narrow && (weeks.length - 1 - i) % 2 ? "" : shortDate(w.start);
      s.append(el("text", { x: x + bw / 2, y: H - 5, "text-anchor": "middle", class: now ? "now-label" : "" }, label));
    });
    row.append(h3, s);
    return row;
  }));
}

// ---- The page ----
function weeksOf(log, now, count) {
  const first = weekStart(now);
  return Array.from({ length: count }, (_, i) => {
    const start = addDays(first, 7 * (i - count + 1)), end = addDays(start, 7);
    return { start, sum: summarise(log.filter((e) => e.t >= start && e.t < end)) };
  });
}

function streaks(log, today) {
  const per = new Map();
  for (const e of log) per.set(dayStart(e.t), (per.get(dayStart(e.t)) || 0) + e.s);
  const days = new Set([...per].filter(([, s]) => s >= 60).map(([d]) => d));
  let d = days.has(today) ? today : addDays(today, -1), current = 0;
  while (days.has(d)) { current++; d = addDays(d, -1); }
  let longest = 0, run = 0, prev = null;
  for (const x of [...days].sort((a, b) => a - b)) {
    run = prev !== null && addDays(prev, 1) === x ? run + 1 : 1;
    longest = Math.max(longest, run);
    prev = x;
  }
  return { current, longest };
}

function render() {
  const log = readLog(), now = Date.now(), today = dayStart(now), week = weekStart(now);
  $("empty").hidden = log.length > 0;
  const total = (xs) => xs.reduce((s, e) => s + e.s, 0);
  $("t-today").textContent = minutes(total(log.filter((e) => e.t >= today)));
  $("t-week").textContent = minutes(total(log.filter((e) => e.t >= week)));
  $("t-all").textContent = minutes(total(log));
  const st = streaks(log, today);
  $("t-streak").textContent = st.current;
  $("t-longest").textContent = st.longest;

  drawDays(log, today);
  const by = (key) => {
    const m = new Map();
    for (const e of log) {
      const hit = tracks.get(`${e.k}|${e.n}`);
      if (!hit) continue;
      const k = key(hit.work);
      m.set(k, (m.get(k) || 0) + e.s);
    }
    return [...m].sort((a, b) => b[1] - a[1]).slice(0, 6);
  };
  drawRanks("composers", by((w) => w.composer).map(([name, s]) => ({ name, s })));
  const works = new Map(LIB.works.map((w) => [w.album, w]));
  drawRanks("works", by((w) => w.album).map(([album, s]) => ({ name: album, sub: works.get(album)?.composer, s })));
  drawClock(log);

  const weeks = weeksOf(log, now, 8);
  const cur = weeks[7].sum, prev = weeks[6].sum;
  $("reflection").replaceChildren(...reflect(cur, prev).map((t) => Object.assign(document.createElement("p"), { textContent: t })));
  drawMeasures(cur);
  drawTrends(weeks);
}

// ---- Export and clear ----
$("export").addEventListener("click", () => {
  const log = readLog();
  const first = log.length ? weekStart(Math.min(...log.map((e) => e.t))) : weekStart(Date.now());
  const count = Math.max(1, Math.round((weekStart(Date.now()) - first) / (7 * 86400000)) + 1);
  const r = (x) => (x === null ? null : Math.round(x * 1000) / 1000);
  const weeks = weeksOf(log, Date.now(), count).map((w) => ({
    week_starting: isoDay(w.start), minutes: minutes(w.sum.total),
    minor_share: r(w.sum.minorShare), slow_share: r(w.sum.slowShare), fast_share: r(w.sum.fastShare),
    quiet_share: r(w.sum.quietShare), loud_share: r(w.sum.loudShare), late_night_share: r(w.sum.lateShare),
  }));
  const data = {
    exported: new Date().toISOString(),
    about: "Listening log from Inside Jeem’s head. Each entry: t = start (ms since 1970), k = work, n = movement, a = start position (s), s = seconds heard.",
    method: "Minor/major from catalogue keys; slow = Andante or slower, fast = Allegro or quicker; quiet/loud = library's softest/loudest thirds in 10 s stretches; late night = 23:00–04:00 local time.",
    log, weekly: weeks,
  };
  const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 1)], { type: "application/json" }));
  const a = Object.assign(document.createElement("a"), { href: url, download: `listening-${isoDay(Date.now())}.json` });
  document.body.append(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});

// Clearing asks first, in the page itself.
$("clear").addEventListener("click", () => { $("clear-confirm").hidden = false; $("clear").hidden = true; $("clear-no").focus(); });
$("clear-no").addEventListener("click", () => { $("clear-confirm").hidden = true; $("clear").hidden = false; $("clear").focus(); });
$("clear-yes").addEventListener("click", () => {
  try { localStorage.removeItem(LOG_KEY); } catch {}
  $("clear-confirm").hidden = true; $("clear").hidden = false;
  render();
});

let resizeTimer;
window.addEventListener("resize", () => { clearTimeout(resizeTimer); resizeTimer = setTimeout(() => LIB && render(), 150); });
window.addEventListener("storage", (e) => { if (e.key === LOG_KEY && LIB) render(); });   // the player in another tab

fetch("library.json").then((r) => r.json()).then((lib) => {
  LIB = lib;
  tracks = new Map(lib.works.flatMap((w) => w.tracks.map((t) => [`${w.album}|${t.n}`, { work: w, track: t }])));
  render();
}).catch(() => { $("empty").hidden = false; $("empty").textContent = "Couldn’t load the catalogue (library.json)."; });
