const config = Object.assign(
  { title: "Classical Library", tagline: "", source: "auto", continuous: true, seekStep: 10 },
  window.PLAYER_CONFIG || {}
);

const $ = (id) => document.getElementById(id);
const audio = $("audio");
const state = {
  works: [],
  filter: "all",      // "all", "favourites" or a composer name
  query: "",
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

// ---- Filtering and rendering ----
function visibleWorks() {
  const q = state.query.toLowerCase();
  return state.works.filter((w) => {
    if (state.filter === "favourites" && !state.favourites.has(w.id)) return false;
    if (state.filter !== "all" && state.filter !== "favourites" && w.composer !== state.filter) return false;
    if (!q) return true;
    return [w.composer, w.album, w.performers, ...w.tracks.map((t) => t.label)]
      .some((s) => s.toLowerCase().includes(q));
  });
}

function renderComposers() {
  const counts = {};
  for (const w of state.works) counts[w.composer] = (counts[w.composer] || 0) + 1;
  const surname = (name) => state.works.find((w) => w.composer === name).surname;
  const names = Object.keys(counts).sort((a, b) => surname(a).localeCompare(surname(b)));
  const item = (value, label, count) =>
    el("li", {}, el("button", {
      "aria-pressed": String(state.filter === value),
      onclick: () => { state.filter = value; save("filter", value); render(); },
    }, el("span", {}, label), el("span", { class: "count" }, String(count))));
  $("composer-list").replaceChildren(
    item("all", "All works", state.works.length),
    item("favourites", "★ Favourites", state.favourites.size),
    el("li", { class: "sep" }),
    ...names.map((n) => item(n, n, counts[n]))
  );
}

function renderWorks() {
  const works = visibleWorks();
  $("status").textContent = works.length ? "" : "No works match.";
  $("works").replaceChildren(...works.map((w) => {
    const fav = state.favourites.has(w.id);
    return el("article", { class: "work" },
      el("header", {},
        el("div", {},
          el("div", { class: "composer" }, w.composer),
          el("h2", {}, w.album)),
        el("button", {
          class: "fav", "aria-pressed": String(fav), "aria-label": "Favourite", title: "Favourite",
          onclick: () => toggleFavourite(w.id),
        }, fav ? "★" : "☆")),
      el("p", { class: "perf" }, w.performers),
      ...(w.note ? [el("p", { class: "note" }, w.note)] : []),
      el("ul", { class: "tracks" }, ...w.tracks.map((t, i) => {
        const playing = state.current && state.current.work === w && state.current.index === i;
        return el("li", {}, el("button", {
          class: "track" + (playing ? " playing" : ""), onclick: () => play(w, i),
        },
          el("span", { class: "n" }, String(t.n)),
          el("span", {}, t.label),
          el("span", { class: "dur" }, t.duration ? fmt(t.duration) : "")));
      })),
      el("div", { class: "links" },
        el("a", { href: w.licence_url, target: "_blank", rel: "noopener" }, w.licence), " · ",
        el("a", { href: w.reference, target: "_blank", rel: "noopener" }, "About this work")));
  }));
}

function render() { renderComposers(); renderWorks(); }

function toggleFavourite(id) {
  state.favourites.has(id) ? state.favourites.delete(id) : state.favourites.add(id);
  save("favourites", [...state.favourites]);
  render();
}

// ---- Playback ----
function play(work, index, startAt = 0) {
  const t = work.tracks[index];
  state.current = { work, index };
  audio.src = trackUrl(t);
  if (startAt) audio.addEventListener("loadedmetadata", () => (audio.currentTime = startAt), { once: true });
  audio.play().catch(() => {});
  $("now-title").textContent = t.label;
  $("now-sub").textContent = `${work.composer} — ${work.album} · ${work.performers}`;
  document.title = `${t.label} · ${config.title}`;
  save("last", { work: work.id, index });
  if ("mediaSession" in navigator) {
    navigator.mediaSession.metadata = new MediaMetadata({
      title: t.title, artist: work.performers, album: work.album,
    });
  }
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

audio.addEventListener("play", () => { $("play").textContent = "⏸"; $("play").setAttribute("aria-label", "Pause"); });
audio.addEventListener("pause", () => { $("play").textContent = "▶"; $("play").setAttribute("aria-label", "Play"); });
audio.addEventListener("ended", () => step(1));
audio.addEventListener("error", () => {
  if (!audio.src) return;
  toast(state.useLocal ? "Couldn't open the local file." : "archive.org didn't respond — try again in a moment.");
});
let lastSaved = 0;
audio.addEventListener("timeupdate", () => {
  const dur = audio.duration;
  $("time-cur").textContent = fmt(audio.currentTime);
  $("time-dur").textContent = fmt(isFinite(dur) ? dur : state.current?.work.tracks[state.current.index].duration);
  if (!seeking && isFinite(dur)) $("seek").value = String((audio.currentTime / dur) * 1000);
  if (Date.now() - lastSaved > 5000) { lastSaved = Date.now(); save("position", audio.currentTime); }
});

let seeking = false;
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

document.addEventListener("keydown", (e) => {
  if (e.target.matches("input[type=search]")) return;
  if (e.code === "Space") { e.preventDefault(); togglePlay(); }
  else if (e.code === "ArrowRight") audio.currentTime += config.seekStep;
  else if (e.code === "ArrowLeft") audio.currentTime -= config.seekStep;
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
  $("site-tagline").textContent = config.tagline;
  document.title = config.title;
  try {
    const data = await (await fetch("library.json")).json();
    state.works = data.works;
  } catch {
    $("status").textContent = "Couldn't load library.json.";
    return;
  }
  state.useLocal = await chooseSource(state.works[0].tracks[0]);
  $("source-badge").textContent = state.useLocal ? "Playing local files" : "Streaming from archive.org";
  const filter = load("filter", "all");
  state.filter = filter === "all" || filter === "favourites" || state.works.some((w) => w.composer === filter) ? filter : "all";
  render();

  // Restore the last track, paused, at the saved position.
  const last = load("last", null);
  const work = last && state.works.find((w) => w.id === last.work);
  if (work && work.tracks[last.index]) {
    const t = work.tracks[last.index];
    state.current = { work, index: last.index };
    audio.src = trackUrl(t);
    const pos = load("position", 0);
    audio.addEventListener("loadedmetadata", () => (audio.currentTime = pos), { once: true });
    $("now-title").textContent = t.label;
    $("now-sub").textContent = `${work.composer} — ${work.album} · ${work.performers}`;
    renderWorks();
  }
}
init();
