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

// Spine tones, one per composer, mixed from the palette (ground, step, ink, amber).
const SPINES = ["spine-a", "spine-b", "spine-c", "spine-d", "spine-e", "spine-f"];
const ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"];
const totalSecs = (w) => w.tracks.reduce((s, t) => s + (t.duration || 0), 0);

function renderWorks() {
  const works = visibleWorks();
  const n = works.length;
  $("status").textContent = n ? ""
    : state.favouritesOnly && !state.favourites.size ? "No favourites yet. Open a book and mark it with a ribbon."
    : "No works match.";
  $("drawer-count").textContent = n === state.works.length ? `${n} books` : `${n} of ${state.works.length} books`;

  // One shelf per composer, ordered by surname; the colour stays with the composer.
  const composers = [...new Set([...state.works].sort((a, b) => a.surname.localeCompare(b.surname)).map((w) => w.composer))];
  const groups = new Map();
  for (const w of [...works].sort((a, b) => a.surname.localeCompare(b.surname))) {
    if (!groups.has(w.composer)) groups.set(w.composer, []);
    groups.get(w.composer).push(w);
  }
  // While searching, the first matching book opens if none of the matches is open.
  const searching = state.query.length > 1;
  const open = works.find((w) => w.id === state.open) || (searching ? works[0] : null);
  const longest = Math.max(...state.works.map(totalSecs));

  $("works").replaceChildren(...[...groups].map(([composer, list]) => {
    const tone = SPINES[composers.indexOf(composer) % SPINES.length];
    const openHere = list.includes(open) ? open : null;
    return el("section", { class: "shelf", "aria-label": composer },
      el("h3", { class: "shelf-label" }, composer),
      el("div", { class: "shelf-row", role: "group", "aria-label": `${composer}: works` },
        ...list.map((w) => renderSpine(w, tone, w === openHere, longest))),
      ...(openHere ? [renderBook(openHere, tone)] : []));
  }));
  rovingSpines();
}

// Two short lines on the spine: "String Quartet / No. 6", "Meditation / St. Wenceslas".
function spineTitle(work) {
  const quoted = /^(\S+).*'(.+)'$/.exec(work);
  if (quoted) return `${quoted[1]}\n${quoted[2]}`;
  if (/ No\. \d+$/.test(work)) return work.replace(/ (No\. \d+)$/, "\n$1");
  return work.includes(" ") && work.length > 12 ? work.replace(" ", "\n") : work;
}

function renderSpine(w, tone, open, longest) {
  const playing = state.current && state.current.work === w;
  const fav = state.favourites.has(w.id);
  // Thicker for more movements, taller for longer works.
  const thick = 32 + 3.5 * Math.min(w.tracks.length, 8);
  const tall = Math.round(148 + 56 * Math.sqrt(totalSecs(w) / longest));
  return el("button", {
    class: `spine ${tone}` + (open ? " out" : "") + (playing ? " playing" : "") + (fav ? " fav" : ""),
    style: `--thick:${thick}px; --tall:${tall}px`,
    "aria-expanded": String(open), "aria-controls": "book-" + w.id, "data-id": w.id,
    "aria-label": `${w.album}, ${w.composer}${fav ? ", favourite" : ""}${playing ? ", playing" : ""}`,
    onclick: () => { state.open = state.open === w.id ? null : w.id; renderWorks(); focusSpine(w.id); },
  },
    el("span", { class: "spine-title" }, spineTitle(w.work)),
    el("span", { class: "spine-cat" }, (w.catalogue || w.key).split(",")[0]),
    ...(fav ? [el("span", { class: "spine-ribbon", "aria-hidden": "true" })] : []));
}

function renderBook(w, tone) {
  const playingWork = state.current && state.current.work === w;
  const fav = state.favourites.has(w.id);
  const close = () => { state.open = null; renderWorks(); focusSpine(w.id); };
  return el("article", {
    class: `book ${tone}`, id: "book-" + w.id, "aria-label": `${w.album}: contents`,
    onkeydown: (e) => { if (e.key === "Escape") { e.stopPropagation(); close(); } },
  },
    el("header", { class: "book-head" },
      el("p", { class: "book-composer" }, w.composer),
      el("h4", { class: "book-title" }, w.album),
      el("p", { class: "book-perf" }, w.performers)),
    el("p", { class: "book-contents" }, "Contents"),
    el("ol", { class: "tracks" },
      ...w.tracks.map((t, i) => {
        const playing = playingWork && state.current.index === i;
        const n = w.tracks.length > 8 ? String(t.n) : ROMAN[i] || String(t.n);
        // The label without its numeral, which the contents page sets on its own.
        const title = t.label.replace(/^[IVX]+\.\s+/, "");
        return el("li", {}, el("button", {
          class: "track" + (playing ? " playing" : ""), onclick: () => play(w, i),
          "aria-current": playing ? "true" : "false",
        },
          el("span", { class: "n" }, n),
          el("span", { class: "t" }, title),
          el("span", { class: "leader", "aria-hidden": "true" }),
          el("span", { class: "dur" }, t.duration ? fmt(t.duration) : "")));
      })),
    ...(w.note ? [el("p", { class: "note" }, w.note)] : []),
    el("footer", { class: "book-foot" },
      el("button", {
        class: "ribbon", "aria-pressed": String(fav), onclick: () => toggleFavourite(w.id),
      }, fav ? "Remove ribbon" : "Mark with a ribbon"),
      el("span", { class: "work-links" },
        el("a", { href: w.licence_url, target: "_blank", rel: "noopener" }, w.licence), " · ",
        el("a", { href: w.reference, target: "_blank", rel: "noopener" }, "About this work")),
      el("button", { class: "book-close", onclick: close }, "Close")));
}

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
  $("now-sub").textContent = `${work.composer} — ${work.album} · ${work.performers}`;
  $("caption-composer").textContent = work.composer;
  $("caption-work").textContent = work.album;
  $("caption-move").textContent = work.tracks.length > 1 ? `${t.label} · ${work.performers}` : work.performers;
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
      title: t.title, artist: work.performers, album: work.album,
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
});

$("seek").addEventListener("input", () => (seeking = true));
$("seek").addEventListener("change", () => {
  seeking = false;
  if (isFinite(audio.duration)) audio.currentTime = ($("seek").value / 1000) * audio.duration;
});
$("volume").value = load("volume", 1);
audio.volume = Number($("volume").value);
$("volume").addEventListener("input", () => { audio.volume = Number($("volume").value); save("volume", audio.volume); });
$("play").addEventListener("click", togglePlay);
$("prev").addEventListener("click", () => (audio.currentTime > 3 ? (audio.currentTime = 0) : step(-1)));
$("next").addEventListener("click", () => step(1));
$("search").addEventListener("input", (e) => { state.query = e.target.value; renderWorks(); });
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
