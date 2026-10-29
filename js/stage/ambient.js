// Ambient engraving: sparse fragments of score that surface at the edges of the
// stage and fade away. A few bars of staff in the movement's real key, its
// tempo marking in italic, the performance's dynamic (read from the live
// level), a slur drawn in one stroke, now and then a fermata. More of them in
// loud passages, one at a time in quiet ones; never over the caption, the title,
// the head or a dream. Not created at all for reduced motion.

const SVG = "http://www.w3.org/2000/svg";
const MAX = 6;
const SP = 6.5;                       // staff space, px

const SHARPS = [8, 5, 9, 6, 3, 7, 4];  // treble-clef positions (steps above the bottom line)
const FLATS = [4, 7, 3, 6, 2, 5, 1];
const MAJOR = { C: 0, G: 1, D: 2, A: 3, E: 4, B: 5, "F-sharp": 6, F: -1, "B-flat": -2, "E-flat": -3, "A-flat": -4, "D-flat": -5 };
const MINOR = { A: 0, E: 1, B: 2, "F-sharp": 3, "C-sharp": 4, D: -1, G: -2, C: -3, F: -4, "B-flat": -5 };

// "E-flat major" -> -3 (three flats); "" -> null (no key signature shown).
function accidentals(key) {
  const m = /^(.+) (major|minor)$/.exec(key || "");
  if (!m) return null;
  const n = (m[2] === "major" ? MAJOR : MINOR)[m[1]];
  return n === undefined ? null : n;
}

function dynamic(level) {
  return level < 0.18 ? "pp" : level < 0.32 ? "p" : level < 0.46 ? "mp" : level < 0.6 ? "mf" : level < 0.76 ? "f" : "ff";
}

const rnd = (a, b) => a + Math.random() * (b - a);
const el = (tag, attrs, text) => {
  const n = document.createElementNS(SVG, tag);
  for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
  if (text) n.textContent = text;
  return n;
};

// One fragment as an SVG group, drawn at the origin; returns it with its size.
function fragment({ tempo, key, level, rising, bass }) {
  const g = el("g", {});
  const kind = Math.random();
  const marking = tempo && (kind < 0.25 || kind > 0.85);
  let w = 0, h = 0;

  if (kind < 0.25 && tempo) {
    // A tempo marking on its own, with the dynamic under it.
    g.append(el("text", { x: 0, y: 18, class: "amb-tempo" }, tempo));
    g.append(el("text", { x: 6, y: 42, class: "amb-dyn" }, dynamic(level)));
    return { g, w: tempo.length * 8.6 + 8, h: 50 };
  }
  if (kind < 0.42) {
    // A gesture: two or three note-heads under a slur, a fermata over the last.
    const n = 2 + (Math.random() < 0.5 ? 1 : 0);
    const ys = [], xs = [];
    let p = rnd(18, 34);
    for (let i = 0; i < n; i++) { xs.push(10 + i * 26); ys.push(p); p += rnd(-9, 9); }
    xs.forEach((x, i) => g.append(head(x, ys[i], Math.random() < 0.3)));
    const top = Math.min(...ys) - 14;
    g.append(slur(xs[0], top + 6, xs[n - 1], top + 6, -12));
    if (Math.random() < 0.6) g.append(el("text", { x: xs[n - 1], y: top - 8, class: "amb-glyph amb-fermata", "text-anchor": "middle" }, "\u{1D110}"));
    return { g, w: xs[n - 1] + 20, h: 60 };
  }

  // A few bars of staff: clef, key signature, a short phrase, sometimes a bar line.
  const top = marking ? 30 : 12, bottom = top + 4 * SP;
  const yOf = (pos) => bottom - (pos * SP) / 2;
  const notes = 3 + Math.floor(Math.random() * 4);
  const count = accidentals(key);
  const ks = count === null ? 0 : Math.abs(count);
  const clefW = bass ? 24 : 22, ksW = ks * 7.2 + (ks ? 6 : 0);
  w = clefW + ksW + notes * 20 + 18;
  for (let i = 0; i < 5; i++) g.append(el("line", { x1: 0, x2: w, y1: top + i * SP, y2: top + i * SP, class: "amb-line" }));
  g.append(el("text", { x: 2, y: yOf(bass ? 6 : 2), class: `amb-glyph ${bass ? "amb-bass" : "amb-clef"}` }, bass ? "\u{1D122}" : "\u{1D11E}"));
  for (let i = 0; i < ks; i++) {
    const pos = (count > 0 ? SHARPS : FLATS)[i] - (bass ? 2 : 0);
    g.append(el("text", { x: clefW + 3 + i * 7.2, y: yOf(pos), class: `amb-glyph amb-acc ${count > 0 ? "sharp" : "flat"}` }, count > 0 ? "♯" : "♭"));
  }
  // A melody that mostly moves by step, within the staff.
  let pos = Math.floor(rnd(1, 7));
  const xs = [], ps = [];
  for (let i = 0; i < notes; i++) {
    xs.push(clefW + ksW + 10 + i * 20);
    ps.push(pos);
    pos = Math.max(-1, Math.min(9, pos + Math.round(rnd(-2.4, 2.4))));
  }
  const open = Math.random() < 0.3;
  xs.forEach((x, i) => {
    const y = yOf(ps[i]);
    g.append(head(x, y, open));
    const up = ps[i] < 4;
    g.append(el("line", { x1: x + (up ? 4.6 : -4.6), x2: x + (up ? 4.6 : -4.6), y1: y, y2: y + (up ? -3.4 : 3.4) * SP, class: "amb-stem" }));
  });
  if (Math.random() < 0.75) {
    const hi = Math.max(...ps);
    const y = yOf(Math.min(10, hi + 3));
    g.append(slur(xs[0], y, xs[notes - 1], y, -9));
  }
  if (Math.random() < 0.5) g.append(el("line", { x1: w - 1, x2: w - 1, y1: top, y2: bottom, class: "amb-line" }));
  if (Math.random() < 0.25) g.append(el("text", { x: xs[notes - 1], y: top - 8, class: "amb-glyph amb-fermata", "text-anchor": "middle" }, "\u{1D110}"));
  if (marking) g.append(el("text", { x: 0, y: 14, class: "amb-tempo" }, tempo));
  // The dynamic as played, with a hairpin when the music is swelling.
  const dy = bottom + 3.4 * SP + 14;
  g.append(el("text", { x: clefW + ksW + 4, y: dy, class: "amb-dyn" }, dynamic(level)));
  if (rising) {
    const x0 = clefW + ksW + 30, x1 = x0 + 56;
    g.append(el("path", { d: `M${x1},${dy - 9} L${x0},${dy - 5} L${x1},${dy - 1}`, class: "amb-stem amb-hairpin" }));
  }
  h = dy + 6;
  return { g, w: Math.max(w, marking ? tempo.length * 8.6 : 0), h };
}

function head(x, y, open) {
  return el("ellipse", { cx: x, cy: y, rx: 4.4, ry: 3.1, transform: `rotate(-22 ${x} ${y})`, class: open ? "amb-head open" : "amb-head" });
}

// One stroke, drawn on as it appears.
function slur(x0, y0, x1, y1, bow) {
  const mx = (x0 + x1) / 2;
  return el("path", { d: `M${x0},${y0} Q${mx},${y0 + bow * 2} ${x1},${y1}`, class: "amb-slur", pathLength: 1 });
}

export function createAmbient({ stage, bands, headRect }) {
  const layer = document.createElementNS(SVG, "svg");
  layer.classList.add("ambient");
  layer.setAttribute("aria-hidden", "true");
  stage.prepend(layer);

  let track = null, work = null, sinceSpawn = 0, sinceTrack = 0, lastLevel = 0;
  const live = [];   // { node, rect, dies }
  window.addEventListener("player:track", (e) => { track = e.detail.track; work = e.detail.work; sinceTrack = 0; });
  if (window.__playerTrack) ({ track, work } = window.__playerTrack);

  // The tempo marking in force: compound headings are split evenly across the movement.
  function tempoNow() {
    const list = track?.tempo || [];
    if (!list.length) return "";
    const audio = document.getElementById("audio");
    const frac = isFinite(audio.duration) && audio.duration ? audio.currentTime / audio.duration : 0;
    return list[Math.min(list.length - 1, Math.floor(frac * list.length))];
  }

  const hit = (a, b, m) => a.x < b.right + m && a.x + a.w > b.left - m && a.y < b.bottom + m && a.y + a.h > b.top - m;

  function place(w, h) {
    const W = stage.clientWidth, H = stage.clientHeight, s = stage.getBoundingClientRect();
    const avoid = [".wordmark", ".caption", ".dream", ".bubble"]
      .flatMap((q) => [...stage.querySelectorAll(q)])
      .map((n) => n.getBoundingClientRect())
      .filter((r) => r.width)
      .map((r) => ({ left: r.left - s.left - 24, right: r.right - s.left + 24, top: r.top - s.top - 12, bottom: r.bottom - s.top + 12 }));
    const hr = headRect();
    if (hr) avoid.push({ left: hr.left, right: hr.left + hr.width, top: hr.top, bottom: hr.top + hr.height });
    for (const l of live) avoid.push(l.rect);
    // Edge bands only: along the top, the left and the right of the stage.
    const m = 16, bands_ = [
      () => ({ x: rnd(m, W - w - m), y: rnd(m, Math.max(m, H * 0.2 - h)) }),
      () => ({ x: rnd(m, Math.max(m, W * 0.16)), y: rnd(m, H - h - m) }),
      () => ({ x: rnd(Math.min(W - w - m, W * 0.8 - w / 2), W - w - m), y: rnd(m, H - h - m) }),
    ];
    for (let i = 0; i < 16; i++) {
      const p = bands_[i % 3]();
      const r = { x: p.x, y: p.y, w, h };
      if (p.x < m || p.y < m || p.x + w > W - m || p.y + h > H - m) continue;
      if (!avoid.some((a) => hit(r, a, 18))) return r;
    }
    return null;
  }

  function spawn(level) {
    const f = fragment({
      tempo: sinceTrack < 20 || Math.random() < 0.6 ? tempoNow() : "",
      key: track?.key, level, rising: bands.level - lastLevel > 0.05,
      bass: Math.random() < 0.2,
    });
    const r = place(f.w, f.h);
    if (!r) return;
    f.g.setAttribute("transform", `translate(${r.x.toFixed(1)} ${r.y.toFixed(1)})`);
    f.g.classList.add("amb");
    layer.append(f.g);
    requestAnimationFrame(() => f.g.classList.add("shown"));
    live.push({ node: f.g, rect: { left: r.x, right: r.x + r.w, top: r.y, bottom: r.y + r.h }, dies: rnd(6, 9.5) });
  }

  return {
    update(dt, playing, dreaming) {
      sinceSpawn += dt; sinceTrack += dt;
      for (let i = live.length - 1; i >= 0; i--) {
        const l = live[i];
        l.dies -= dt;
        if (l.dies <= 0 && !l.gone) { l.gone = true; l.node.classList.remove("shown"); }
        if (l.dies < -2.6) { l.node.remove(); live.splice(i, 1); }
      }
      const level = bands.level;
      const want = playing && !dreaming ? Math.min(MAX, Math.max(1, Math.round(0.5 + level * 6))) : 0;
      const showing = live.filter((l) => !l.gone).length;
      if (showing < want && sinceSpawn > 1.6 + Math.random() * 2) { spawn(level); sinceSpawn = 0; }
      if (dreaming) for (const l of live) if (!l.gone) l.dies = Math.min(l.dies, 0);
      lastLevel += (level - lastLevel) * Math.min(1, dt / 1.5);
    },
  };
}
