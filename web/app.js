const config = Object.assign(
  { title: "Inside Jeem’s head", tagline: "", source: "auto", continuous: true, seekStep: 10 },
  window.PLAYER_CONFIG || {}
);

const $ = (id) => document.getElementById(id);
const audio = $("audio");
// The stage analyses the audio with Web Audio, which needs CORS (archive.org sends it).
audio.crossOrigin = "anonymous";
let corsRetried = false;
const state = {
  works: [],
  favouritesOnly: false,
  query: "",
  open: null,         // id of the expanded work in the list
  current: null,      // { work, index }
  useLocal: false,
  favourites: new Set(load("favourites", [])),
};

// ---- Storage (per-browser conveniences only) ----
function load(key, fallback) {
  try { const v = localStorage.getItem("cl:" + key); return v === null ? fallback : JSON.parse(v); }
  catch { return fallback; }
}
function save(key, value) {
  try { localStorage.setItem("cl:" + key, JSON.stringify(value)); } catch {}
}

// ---- Helpers ----
function fmt(sec) {
  if (!isFinite(sec)) return "0:00";
  sec = Math.round(sec);
  const h = Math.floor(sec / 3600), m = Math.floor((sec % 3600) / 60), s = sec % 60;
  return (h ? h + ":" + String(m).padStart(2, "0") : m) + ":" + String(s).padStart(2, "0");
}
function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") node.className = v;
    else if (k.startsWith("on")) node.addEventListener(k.slice(2), v);
    else node.setAttribute(k, v);
  }
  node.append(...children);
  return node;
}
let toastTimer;
function toast(msg) {
  const t = $("toast");
  t.textContent = msg; t.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => (t.hidden = true), 4000);
}
const trackUrl = (t) => (state.useLocal ? encodeURI(t.local) : t.url);

// The stage (3D head, notes, dreams) listens to these; the player never depends on it.
function emit(type, detail) {
  if (type === "track") window.__playerTrack = detail;   // for listeners that load later (the stage)
  window.dispatchEvent(new CustomEvent("player:" + type, { detail }));
}

// ---- Filtering and rendering ----
function matches(w, q) {
  return [w.composer, w.album, w.performers, ...w.tracks.map((t) => t.label)]
    .some((s) => s.toLowerCase().includes(q));
}
function visibleWorks() {
  const q = state.query.toLowerCase();
  return state.works.filter((w) =>
    (!state.favouritesOnly || state.favourites.has(w.id)) && (!q || matches(w, q)));
}

// ---- The bookcase ----
// Composers share shelves between bookends (bookcase.js packs them); each wears its binding.
const ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"];
const totalSecs = (w) => w.tracks.reduce((s, t) => s + (t.duration || 0), 0);
const phone = matchMedia("(max-width: 760px)");
const calm = matchMedia("(prefers-reduced-motion: reduce)");
const CASE_SIDES = 2 * 14 + 2 * 6;   // the uprights and the shelf's inner margin, as in style.css

function renderWorks() {
  const works = visibleWorks();
  const n = works.length;
  $("status").textContent = n ? ""
    : state.favouritesOnly && !state.favourites.size ? "No favourites yet. Open a book and mark it with a ribbon."
    : "No works match.";
  $("drawer-count").textContent = n === state.works.length ? `${n} books` : `${n} of ${state.works.length} books`;

  // While searching, the first matching book opens if none of the matches is open.
  const searching = state.query.length > 1;
  const open = works.find((w) => w.id === state.open) || (searching ? works[0] : null);
  const longest = Math.max(...state.works.map(totalSecs));

  // Ordered by surname. Thicker for more movements, taller for longer works.
  const groups = [];
  for (const w of [...works].sort((a, b) => a.surname.localeCompare(b.surname))) {
    if (groups.at(-1)?.composer !== w.composer) groups.push({ composer: w.composer, surname: w.surname, books: [] });
    groups.at(-1).books.push({
      w, thick: 32 + 3.5 * Math.min(w.tracks.length, 8),
      tall: Math.round(148 + 56 * Math.sqrt(totalSecs(w) / longest)),
    });
  }
  const shelves = !groups.length ? [{ groups: [], clear: 120 }]
    : phone.matches ? groups.map((g) => ({ groups: [{ ...g, pile: true, books: g.books.map((b) => ({ ...b, flat: true })) }] }))
    : Bookcase.pack(groups, $("works").clientWidth - CASE_SIDES);

  const nodes = [el("div", { class: "case-top", "aria-hidden": "true" })];
  for (const s of shelves) {
    nodes.push(el("div", { class: "shelf", ...(s.clear ? { style: `--clear:${s.clear}px` } : {}) },
      el("div", { class: "shelf-books" }, ...s.groups.map((g) => renderGroup(g, open))),
      el("div", { class: "shelf-edge", "aria-hidden": "true" })));
    if (s.groups.some((g) => g.books.some((b) => b.w === open))) nodes.push(renderBook(open));
  }
  nodes.push(el("div", { class: "case-base", "aria-hidden": "true" }));
  $("works").replaceChildren(...nodes);
  rovingSpines();
  settle();
}

function renderGroup(g, open) {
  return el("div", { class: "group" + (g.pile ? " pile" : ""), role: "group", "aria-label": g.composer, style: `--bookend:${g.bookend || 0}px` },
    el("span", { class: "bookend", "aria-hidden": "true" }),
    ...g.books.map((b) => renderSpine(b, b.w === open)),
    el("span", { class: "bookend", "aria-hidden": "true" }),
    el("span", { class: "plate", "aria-hidden": "true" }, g.surname));
}

function renderSpine(b, open) {
  const w = b.w;
  const playing = state.current && state.current.work === w;
  const fav = state.favourites.has(w.id);
  const face = (cls) => el("span", { class: "face " + cls });
  return el("button", {
    class: `spine ${Bookcase.binding(w.surname)}` + (b.flat ? " flat" : "") + (b.lean ? " lean" : "")
      + (open ? " out" : "") + (playing ? " playing" : "") + (fav ? " fav" : ""),
    style: `--thick:${b.thick}px; --tall:${b.tall}px` + (b.lean ? `; --lean:${b.lean}px` : ""),
    "aria-expanded": String(open), "aria-controls": "book-" + w.id, "data-id": w.id,
    "aria-label": `${w.album}, ${w.composer}${fav ? ", favourite" : ""}${playing ? ", playing" : ""}`,
    onclick: () => toggleBook(w),
  },
    el("span", { class: "book3d" },
      el("span", { class: "face front" },
        el("span", { class: "band h1" }), el("span", { class: "band h2" }),
        el("span", { class: "label" }, el("span", { class: "gilt", "aria-hidden": "true" })),
        el("span", { class: "band t1" }), el("span", { class: "band t2" })),
      face("side l"), face("side r"), face("top")),
    ...(playing ? [el("span", { class: "marker", "aria-hidden": "true" })] : []),
    ...(fav ? [el("span", { class: "spine-ribbon", "aria-hidden": "true" })] : []));
}

function renderBook(w) {
  const playingWork = state.current && state.current.work === w;
  const fav = state.favourites.has(w.id);
  return el("article", {
    class: `book ${Bookcase.binding(w.surname)}`, id: "book-" + w.id, "aria-label": `${w.album}: contents`,
    onkeydown: (e) => { if (e.key === "Escape") { e.stopPropagation(); closeBook(w.id); } },
  },
    el("div", { class: "page", style: `clip-path: ${Bookcase.deckle(7919 * parseInt(w.id.slice(1), 10))}` },
      el("header", { class: "book-head" },
        el("p", { class: "book-composer" }, w.composer),
        el("h4", { class: "book-title" }, w.album.replace(/–/g, "–\u2060")),   // never break "1–3"
        el("p", { class: "book-perf" }, w.performers)),
      el("p", { class: "book-contents" }, "Contents"),
      el("ol", { class: "tracks" },
        ...w.tracks.map((t, i) => {
          const playing = playingWork && state.current.index === i;
          // Roman for numbered movements, Arabic for sets of pieces, nothing for a single piece.
          const n = w.tracks.length === 1 ? "" : /^[IVX]+\.\s/.test(t.label) ? ROMAN[i] : String(t.n);
          // The label without its numeral, which the contents page sets on its own.
          const title = t.label.replace(/^[IVX]+\.\s+/, "");
          return el("li", {}, el("button", {
            class: "track" + (playing ? " playing" : ""), onclick: () => { SFX.play("tock"); play(w, i); },
            "aria-current": playing ? "true" : "false",
          },
            el("span", { class: "n" }, n),
            el("span", { class: "t" }, title, ...(t.performer ? [el("small", { class: "tp" }, t.performer)] : [])),
            el("span", { class: "leader", "aria-hidden": "true" }),
            el("span", { class: "dur" }, t.duration ? fmt(t.duration) : "")));
        })),
      ...(w.note ? [el("p", { class: "note" }, w.note)] : []),
      // Recordings from outside the Musopen set carry their own credit (CC BY needs it).
      ...(w.credit ? [el("p", { class: "book-credit" }, w.credit, " ",
        el("a", { href: w.source, target: "_blank", rel: "noopener" }, "Source"), ".")] : []),
      el("footer", { class: "book-foot" },
        el("button", {
          class: "ribbon", "aria-pressed": String(fav), onclick: () => toggleFavourite(w.id),
        }, fav ? "Remove ribbon" : "Mark with a ribbon"),
        el("span", { class: "work-links" },
          el("a", { href: w.licence_url, target: "_blank", rel: "noopener" }, w.licence), " · ",
          el("a", { href: w.reference, target: "_blank", rel: "noopener" }, "About this work")),
        el("button", { class: "book-close", onclick: () => closeBook(w.id) }, "Close"))),
    ...(playingWork ? [el("span", { class: "page-mark", "aria-hidden": "true" })] : []),
    el("div", { class: "flyleaf", "aria-hidden": "true" }));
}

// After layout: each spine's vanishing point at the middle of the case, titles fitted to
// their panels, and the open book laid in front of the shelves below its own.
function settle() {
  const box = $("works");
  const mid = box.getBoundingClientRect().left + box.clientWidth / 2;
  for (const s of box.querySelectorAll(".spine")) {
    s.style.setProperty("--pox", Math.round(mid - s.getBoundingClientRect().left) + "px");
    Bookcase.fit(s.querySelector(".gilt"), state.works.find((w) => w.id === s.dataset.id), s.classList.contains("flat"));
  }
  // Plates under narrow groups would touch; nudge each clear of the one before, inside the case.
  for (const row of box.querySelectorAll(".shelf-books")) {
    let edge = row.getBoundingClientRect().left;
    for (const p of row.querySelectorAll(".plate")) {
      const r = p.getBoundingClientRect();
      if (r.left < edge + 4) p.style.marginLeft = Math.ceil(edge + 4 - r.left) + "px";
      edge = p.getBoundingClientRect().right;
    }
  }
  const book = box.querySelector(".book");
  box.style.marginBottom = "";
  if (!book) return;
  const shelf = book.previousElementSibling;
  book.style.top = shelf.offsetTop + shelf.offsetHeight + 2 + "px";
  const over = book.offsetTop + book.offsetHeight + 16 - box.offsetHeight;
  if (over > 0) box.style.marginBottom = over + "px";
  const row = book.querySelector(".track.playing"), mark = book.querySelector(".page-mark");
  // offsets, not client rects: the book may still be swinging open
  if (row && mark) mark.style.height = row.offsetParent.offsetTop + row.offsetTop + row.offsetHeight + "px";
}

// Pull a book out (a wooden scrape), then open it (a page turn); put it back with a thud.
let turning = 0;
const spineOf = (id) => document.querySelector(`.spine[data-id="${id}"]`);
function toggleBook(w) {
  if (state.open === w.id && $("book-" + w.id)) return closeBook(w.id);
  clearTimeout(turning);
  $("works").querySelector(".book")?.remove();
  document.querySelectorAll(".spine.out").forEach((s) => s.classList.remove("out"));
  spineOf(w.id)?.classList.add("out");
  SFX.play("slide");
  turning = setTimeout(() => {
    state.open = w.id;
    renderWorks();
    focusSpine(w.id);
    SFX.play("page", calm.matches ? 0 : 150);
  }, calm.matches ? 0 : 400);
}
function closeBook(id) {
  clearTimeout(turning);
  $("book-" + id)?.remove();
  spineOf(id)?.classList.remove("out");
  state.open = null;
  SFX.play("thud", calm.matches ? 0 : 180);
  turning = setTimeout(() => { renderWorks(); focusSpine(id); }, calm.matches ? 0 : 450);
}
let lastWidth = 0;
new ResizeObserver(() => {
  const w = $("works").clientWidth;
  if (w !== lastWidth && state.works.length) { lastWidth = w; renderWorks(); }
}).observe($("works"));

// Spines are one tab stop; arrow keys move along the shelves.
function rovingSpines() {
  const spines = [...document.querySelectorAll(".spine")];
  const current = spines.find((s) => s.classList.contains("out"))
    || spines.find((s) => s.classList.contains("playing")) || spines[0];
  spines.forEach((s) => (s.tabIndex = s === current ? 0 : -1));
}
function focusSpine(id) {
  const s = document.querySelector(`.spine[data-id="${id}"]`);
  if (s) { document.querySelectorAll(".spine").forEach((x) => (x.tabIndex = -1)); s.tabIndex = 0; s.focus(); }
}
$("works").addEventListener("keydown", (e) => {
  if (!e.target.classList.contains("spine")) return;
  const spines = [...document.querySelectorAll(".spine")];
  const i = spines.indexOf(e.target);
  const to = { ArrowRight: i + 1, ArrowDown: i + 1, ArrowLeft: i - 1, ArrowUp: i - 1, Home: 0, End: spines.length - 1 }[e.key];
  if (to === undefined) return;
  e.preventDefault();
  const s = spines[Math.max(0, Math.min(spines.length - 1, to))];
  spines.forEach((x) => (x.tabIndex = -1));
  s.tabIndex = 0; s.focus();
});

function toggleFavourite(id) {
  state.favourites.has(id) ? state.favourites.delete(id) : state.favourites.add(id);
  save("favourites", [...state.favourites]);
  renderWorks();
}

// ---- Caption: what is playing (history notes join it in phase d) ----
function showNowPlaying(work, t) {
  $("now-title").textContent = t.label;
  const perf = t.performer || work.performers;
  $("now-sub").textContent = `${work.composer} — ${work.album} · ${perf}`;
  $("caption-composer").textContent = work.composer;
  $("caption-work").textContent = work.album.replace(/–/g, "–\u2060");
  $("caption-move").textContent = work.tracks.length > 1 ? `${t.label} · ${perf}` : perf;
  shownNote = undefined;
  setNote(null);
}

// ---- History notes: each appears at its moment and gives way to the next ----
const NOTE_SECS = 28;
let shownNote;
let noteTimer;
function setNote(note) {
  if (note === shownNote) return;
  shownNote = note;
  const el = $("caption-note");
  el.classList.add("fading");
  clearTimeout(noteTimer);
  noteTimer = setTimeout(() => {
    el.textContent = note ? note.text : "";
    el.classList.remove("fading");
  }, el.textContent ? 600 : 0);
}
function noteAt(track, time) {
  const notes = track.notes || [];
  for (let i = notes.length - 1; i >= 0; i--) {
    const n = notes[i];
    if (time >= n.at) return time < n.at + NOTE_SECS ? n : null;
  }
  return null;
}

// ---- Listening log: seconds actually heard, kept only in this browser ----
// One entry per stretch of uninterrupted playback: { t: start (ms), k: album, n: movement,
// a: start position (s), s: seconds heard }. Seeks, skips and pauses close the stretch, and
// only small forward steps of the playhead count, so jumping around adds nothing.
const LOG_KEY = "cl:listening";
let stretch = null, lastPos = null;
function closeStretch() {
  if (stretch && stretch.s >= 1) {
    stretch.s = Math.round(stretch.s * 10) / 10;
    try {
      const log = JSON.parse(localStorage.getItem(LOG_KEY) || "[]");
      log.push(stretch);
      localStorage.setItem(LOG_KEY, JSON.stringify(log));
    } catch {}
  }
  stretch = null;
}
function heard() {
  const pos = audio.currentTime;
  const step = lastPos === null ? 0 : pos - lastPos;
  lastPos = pos;
  if (!state.current || audio.paused || step <= 0 || step > 1.5) return;
  const { work, index } = state.current;
  if (!stretch) stretch = { t: Date.now(), k: work.album, n: work.tracks[index].n, a: Math.round(pos - step), s: 0 };
  stretch.s += step;
  if (stretch.s >= 60) closeStretch();   // flush each minute, so a closed tab loses little
}
audio.addEventListener("seeking", () => { closeStretch(); lastPos = null; });
audio.addEventListener("pause", closeStretch);
audio.addEventListener("emptied", () => { closeStretch(); lastPos = null; });
window.addEventListener("pagehide", closeStretch);

// ---- Playback ----
function play(work, index, startAt = 0) {
  const t = work.tracks[index];
  state.current = { work, index };
  state.open = work.id;
  audio.src = trackUrl(t);
  if (startAt) audio.addEventListener("loadedmetadata", () => (audio.currentTime = startAt), { once: true });
  audio.play().catch(() => {});
  showNowPlaying(work, t);
  document.title = `${t.label} · ${config.title}`;
  save("last", { work: work.id, index });
  if ("mediaSession" in navigator) {
    navigator.mediaSession.metadata = new MediaMetadata({
      title: t.title, artist: t.performer || work.performers, album: work.album,
    });
  }
  emit("track", { work, track: t, index });
  renderWorks();
}

function step(delta) {
  if (!state.current) {
    const first = visibleWorks()[0];
    if (first) play(first, 0);
    return;
  }
  const { work, index } = state.current;
  const i = index + delta;
  if (i >= 0 && i < work.tracks.length) return play(work, i);
  if (delta > 0 && !config.continuous) return;
  const list = visibleWorks().length ? visibleWorks() : state.works;
  const w = list[(list.indexOf(work) + (delta > 0 ? 1 : -1) + list.length) % list.length];
  play(w, delta > 0 ? 0 : w.tracks.length - 1);
}

function togglePlay() {
  if (!state.current) return step(1);
  audio.paused ? audio.play().catch(() => {}) : audio.pause();
}

audio.addEventListener("play", () => { $("play").textContent = "⏸"; $("play").setAttribute("aria-label", "Pause"); emit("play"); });
audio.addEventListener("pause", () => { $("play").textContent = "▶"; $("play").setAttribute("aria-label", "Play"); emit("pause"); });
audio.addEventListener("ended", () => step(1));
audio.addEventListener("error", () => {
  if (!audio.src) return;
  // If a stream ever refuses CORS, play it without analysis rather than not at all.
  // (Not possible once Web Audio owns the element: it would play silence.)
  if (audio.crossOrigin && !window.__audioGraph && !corsRetried && !state.useLocal) {
    corsRetried = true;
    const src = audio.src, at = audio.currentTime;
    audio.removeAttribute("crossorigin");
    audio.src = src;
    audio.addEventListener("loadedmetadata", () => (audio.currentTime = at), { once: true });
    audio.play().catch(() => {});
    return;
  }
  toast(state.useLocal ? "Couldn't open the local file." : "archive.org didn't respond — try again in a moment.");
});
let lastSaved = 0;
let seeking = false;
audio.addEventListener("timeupdate", () => {
  const dur = audio.duration;
  $("time-cur").textContent = fmt(audio.currentTime);
  $("time-dur").textContent = fmt(isFinite(dur) ? dur : state.current?.work.tracks[state.current.index].duration);
  if (!seeking && isFinite(dur)) $("seek").value = String((audio.currentTime / dur) * 1000);
  if (Date.now() - lastSaved > 5000) { lastSaved = Date.now(); save("position", audio.currentTime); }
  if (state.current) setNote(noteAt(state.current.work.tracks[state.current.index], audio.currentTime));
  heard();
});

$("seek").addEventListener("input", () => (seeking = true));
$("seek").addEventListener("change", () => {
  seeking = false;
  if (isFinite(audio.duration)) audio.currentTime = ($("seek").value / 1000) * audio.duration;
});
// The volume the listener set; sound effects briefly duck the music under it by 6 dB.
let userVolume = Number(load("volume", 1)), duck = 1, duckFrame = 0, lastFrame = 0;
const ducks = [];
$("volume").value = userVolume;
audio.volume = userVolume;
$("volume").addEventListener("input", () => {
  userVolume = Number($("volume").value);
  audio.volume = userVolume * duck;
  save("volume", userVolume);
});
function ducking(now) {
  const dt = lastFrame ? now - lastFrame : 16;
  lastFrame = now;
  while (ducks.length && ducks[0].end < now) ducks.shift();
  const target = ducks.some((d) => now >= d.start) ? 0.5 : 1;
  duck += (target - duck) * (1 - Math.exp(-dt / (target < duck ? 40 : 300)));
  if (!ducks.length && duck > 0.995) duck = 1;
  audio.volume = userVolume * duck;
  duckFrame = duck < 1 || ducks.length ? requestAnimationFrame(ducking) : 0;
  if (!duckFrame) lastFrame = 0;
}
SFX.volume = () => userVolume;
SFX.onPlay = (delay, ms) => {
  if (audio.paused) return;
  const start = performance.now() + delay - 40;
  ducks.push({ start, end: start + ms + 160 });
  ducks.sort((a, b) => a.end - b.end);
  if (!duckFrame) duckFrame = requestAnimationFrame(ducking);
};
$("sfx-toggle").setAttribute("aria-pressed", String(SFX.enabled));
$("sfx-toggle").addEventListener("click", () => {
  SFX.enabled = !SFX.enabled;
  $("sfx-toggle").setAttribute("aria-pressed", String(SFX.enabled));
});
$("play").addEventListener("click", togglePlay);
$("prev").addEventListener("click", () => (audio.currentTime > 3 ? (audio.currentTime = 0) : step(-1)));
$("next").addEventListener("click", () => step(1));
// The drawer runs out when a search begins, not on every key.
let lastSearch = 0;
$("search").addEventListener("input", (e) => {
  if (performance.now() - lastSearch > 1500) SFX.play("drawer");
  lastSearch = performance.now();
  state.query = e.target.value;
  renderWorks();
});
$("fav-filter").addEventListener("click", () => {
  state.favouritesOnly = !state.favouritesOnly;
  $("fav-filter").setAttribute("aria-pressed", String(state.favouritesOnly));
  save("favouritesOnly", state.favouritesOnly);
  renderWorks();
});

document.addEventListener("keydown", (e) => {
  if (e.target.matches("input[type=search]") || e.target.closest(".shelves")) return;
  if (e.code === "Space" && !e.target.matches("button, a")) { e.preventDefault(); togglePlay(); }
  else if (e.code === "ArrowRight" && !e.target.matches("input[type=range]")) audio.currentTime += config.seekStep;
  else if (e.code === "ArrowLeft" && !e.target.matches("input[type=range]")) audio.currentTime -= config.seekStep;
  else if (e.key === "/") { e.preventDefault(); $("search").focus(); }
});

if ("mediaSession" in navigator) {
  navigator.mediaSession.setActionHandler("play", () => audio.play());
  navigator.mediaSession.setActionHandler("pause", () => audio.pause());
  navigator.mediaSession.setActionHandler("previoustrack", () => step(-1));
  navigator.mediaSession.setActionHandler("nexttrack", () => step(1));
}

// ---- Start-up ----
async function chooseSource(sample) {
  if (config.source === "local") return true;
  if (config.source === "archive") return false;
  try {
    const r = await fetch(encodeURI(sample.local), { method: "HEAD" });
    return r.ok;
  } catch { return false; }
}

async function init() {
  $("site-title").textContent = config.title;
  document.title = config.title;
  try {
    const data = await (await fetch("library.json")).json();
    state.works = data.works;
  } catch {
    $("status").textContent = "Couldn't load library.json.";
    return;
  }
  // Spine titles are measured in Newsreader, so wait for it (but not forever).
  await Promise.race([document.fonts.load("500 14px Newsreader"), new Promise((r) => setTimeout(r, 2500))]).catch(() => {});
  state.useLocal = await chooseSource(state.works[0].tracks[0]);
  $("source-badge").textContent = state.useLocal ? "Local files" : "Streaming from archive.org";
  state.favouritesOnly = !!load("favouritesOnly", false);
  $("fav-filter").setAttribute("aria-pressed", String(state.favouritesOnly));

  // Restore the last track, paused, at the saved position.
  const last = load("last", null);
  const work = last && state.works.find((w) => w.id === last.work);
  if (work && work.tracks[last.index]) {
    const t = work.tracks[last.index];
    state.current = { work, index: last.index };
    state.open = work.id;
    audio.src = trackUrl(t);
    const pos = load("position", 0);
    audio.addEventListener("loadedmetadata", () => (audio.currentTime = pos), { once: true });
    showNowPlaying(work, t);
    emit("track", { work, track: t, index: last.index });
  }
  renderWorks();
}
init();
