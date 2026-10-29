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

function renderWorks() {
  const works = visibleWorks();
  $("status").textContent = works.length ? ""
    : state.favouritesOnly && !state.favourites.size ? "No favourites yet. Mark a work with ☆."
    : "No works match.";
  const searching = state.query.length > 1;

  // Group by composer, ordered by surname.
  const groups = new Map();
  for (const w of [...works].sort((a, b) => a.surname.localeCompare(b.surname))) {
    if (!groups.has(w.composer)) groups.set(w.composer, []);
    groups.get(w.composer).push(w);
  }

  $("works").replaceChildren(...[...groups].map(([composer, list]) =>
    el("section", { class: "composer-group" },
      el("h3", { class: "composer-name" }, composer),
      ...list.map((w) => renderWork(w, searching)))));
}

function renderWork(w, searching) {
  const playingWork = state.current && state.current.work === w;
  const open = state.open === w.id || (searching && matches(w, state.query.toLowerCase()));
  const fav = state.favourites.has(w.id);
  const listId = "tracks-" + w.id;
  return el("article", { class: "work" + (open ? " open" : "") + (playingWork ? " playing" : "") },
    el("div", { class: "work-row" },
      el("button", {
        class: "work-toggle", "aria-expanded": String(open), "aria-controls": listId,
        onclick: () => { state.open = state.open === w.id ? null : w.id; renderWorks(); },
      },
        el("span", { class: "work-title" }, w.album),
        el("span", { class: "work-perf" }, `${w.performers} · `,
          el("span", { class: "nowrap" }, w.tracks.length === 1 ? "1 movement" : w.tracks.length + " movements"))),
      el("button", {
        class: "fav", "aria-pressed": String(fav), "aria-label": `Favourite ${w.album}`, title: "Favourite",
        onclick: () => toggleFavourite(w.id),
      }, fav ? "★" : "☆")),
    el("ol", { class: "tracks", id: listId },
      ...w.tracks.map((t, i) => {
        const playing = playingWork && state.current.index === i;
        return el("li", {}, el("button", {
          class: "track" + (playing ? " playing" : ""), onclick: () => play(w, i),
          "aria-current": playing ? "true" : "false",
        },
          el("span", { class: "n" }, String(t.n)),
          el("span", {}, t.label),
          el("span", { class: "dur" }, t.duration ? fmt(t.duration) : "")));
      }),
      ...(w.note ? [el("li", { class: "note" }, w.note)] : []),
      el("li", { class: "work-links" },
        el("a", { href: w.licence_url, target: "_blank", rel: "noopener" }, w.licence), " · ",
        el("a", { href: w.reference, target: "_blank", rel: "noopener" }, "About this work"))));
}

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
  if (e.target.matches("input[type=search]")) return;
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
