// Dream conversations: once per work per session (and on request), my head and
// the composer face each other in a drifting engraved haze while an imagined
// exchange rises between them in hatched thought-bubbles. Each dream is
// assembled at random from the work's material in dreams.json: an opening,
// 2–3 question/answer pairs (never repeated within a session) and a closing.
// The music carries on underneath.
import * as THREE from "three";

const INK = new THREE.Color("#e8e1d4");
const START_AT = 70;          // seconds into the first track played from a work
const SEEN_KEY = "cl:dreamt";
const USED_KEY = "cl:dream-pairs";   // "workId:question:answer" already heard this session

const hatchFn = /* glsl */ `
  float hatch(float coord, float w) {
    float d = abs(fract(coord) - 0.5);
    float aa = fwidth(coord) * 0.75;
    return 1.0 - smoothstep(w - aa, w + aa, d);
  }
`;

// The composer, engraved the same way as my head: tone from the portrait,
// lines leaning the other way (we face each other), a gentle relief.
const portraitVertex = /* glsl */ `
  uniform sampler2D uMap;
  uniform float uTime;
  varying vec2 vUv;
  void main() {
    vUv = uv;
    float lum = dot(texture2D(uMap, uv).rgb, vec3(0.299, 0.587, 0.114));
    vec3 p = position;
    p.z += lum * 0.07 + 0.012 * sin(uTime * 0.6 + uv.y * 6.0);
    gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0);
  }
`;
const portraitFragment = /* glsl */ `
  uniform sampler2D uMap;
  uniform vec3 uInk;
  uniform float uMix;
  varying vec2 vUv;
  ${hatchFn}
  void main() {
    float lum = dot(texture2D(uMap, vUv).rgb, vec3(0.299, 0.587, 0.114));
    float tone = smoothstep(0.08, 0.88, lum);
    vec2 c = vUv - vec2(0.5, 0.56);
    float bow = 0.5 * c.x * c.x - 0.25 * c.y * c.y;
    float k = 95.0;
    float c1 = (dot(c, normalize(vec2(-0.88, 0.47))) - bow) * k;
    float c2 = (dot(c, normalize(vec2(0.42, 0.91))) + 0.7 * bow) * k * 1.15;
    float ink = hatch(c1, mix(0.03, 0.3, tone));
    ink = max(ink, hatch(c2, 0.11) * smoothstep(0.6, 0.9, tone));
    // Dissolve into the haze toward the edges of the frame.
    float r = length(c / vec2(0.46, 0.52));
    float a = ink * (1.0 - smoothstep(0.7, 1.0, r)) * uMix;
    gl_FragColor = vec4(uInk * a, a);
  }
`;

// The hazy, shifting space: horizontal engraved strokes whose weight follows
// slowly drifting noise.
const hazeFragment = /* glsl */ `
  uniform vec3 uInk;
  uniform float uMix;
  uniform float uTime;
  varying vec2 vUv;
  ${hatchFn}
  float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
  float noise(vec2 p) {
    vec2 i = floor(p), f = fract(p);
    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(mix(hash(i), hash(i + vec2(1, 0)), u.x), mix(hash(i + vec2(0, 1)), hash(i + vec2(1, 1)), u.x), u.y);
  }
  float fbm(vec2 p) { float v = 0.0, a = 0.5; for (int i = 0; i < 4; i++) { v += a * noise(p); p *= 2.03; a *= 0.5; } return v; }
  void main() {
    vec2 p = vUv * vec2(4.0, 2.4);
    float fog = fbm(p + vec2(uTime * 0.035, -uTime * 0.02));
    fog = smoothstep(0.3, 0.75, fog);
    float line = hatch(vUv.y * 160.0 + fog * 2.5 + 0.4 * sin(vUv.x * 9.0 + uTime * 0.2), 0.05 + 0.12 * fog);
    float a = line * fog * 0.5 * uMix;
    gl_FragColor = vec4(uInk * a, a);
  }
`;
const quadVertex = /* glsl */ `
  varying vec2 vUv;
  void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }
`;

// ---- Bubble shapes: soft irregular blobs, hatched at the edge ----
const SVG = "http://www.w3.org/2000/svg";

// A closed, wobbly outline around a w×h box (Catmull-Rom through jittered points).
function blob(w, h, rand, wobble = 0.09) {
  const n = 13, cx = w / 2, cy = h / 2, pts = [];
  for (let i = 0; i < n; i++) {
    const a = (i / n) * Math.PI * 2 + rand() * 0.2;
    // A squarish ellipse, so text near the corners stays inside.
    const c = Math.cos(a), s = Math.sin(a);
    const r = 1 + (rand() * 2 - 1) * wobble;
    pts.push([cx + Math.sign(c) * Math.abs(c) ** 0.7 * cx * r, cy + Math.sign(s) * Math.abs(s) ** 0.7 * cy * r]);
  }
  let d = `M${pts[0][0].toFixed(1)},${pts[0][1].toFixed(1)}`;
  for (let i = 0; i < n; i++) {
    const p0 = pts[(i - 1 + n) % n], p1 = pts[i], p2 = pts[(i + 1) % n], p3 = pts[(i + 2) % n];
    const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
    const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
    d += `C${c1[0].toFixed(1)},${c1[1].toFixed(1)} ${c2[0].toFixed(1)},${c2[1].toFixed(1)} ${p2[0].toFixed(1)},${p2[1].toFixed(1)}`;
  }
  return d + "Z";
}

function bubbleSvg(w, h, edge) {
  const pad = edge + 6;
  const svg = document.createElementNS(SVG, "svg");
  svg.setAttribute("width", w + pad * 2);
  svg.setAttribute("height", h + pad * 2);
  svg.setAttribute("aria-hidden", "true");
  const d = blob(w, h, Math.random, 0.13);
  svg.innerHTML = `<g transform="translate(${pad} ${pad})">
    <path d="${d}" class="bub-fill" filter="url(#bub-soft)"/>
    <path d="${d}" class="bub-edge" stroke-width="${edge}" filter="url(#bub-rough)"/>
    <path d="${blob(w, h, Math.random, 0.05)}" class="bub-edge bub-edge-2" stroke-width="${edge * 0.45}" filter="url(#bub-rough)"/>
  </g>`;
  return { svg, pad };
}

// Shared pattern and filters, defined once in the page.
function defineBubbleDefs() {
  if (document.getElementById("bub-defs")) return;
  const defs = document.createElementNS(SVG, "svg");
  defs.id = "bub-defs";
  defs.setAttribute("width", "0"); defs.setAttribute("height", "0");
  defs.setAttribute("aria-hidden", "true");
  defs.style.position = "absolute";
  defs.innerHTML = `<defs>
    <pattern id="bub-hatch" width="3.4" height="3.4" patternUnits="userSpaceOnUse" patternTransform="rotate(-38)">
      <line x1="0" y1="0" x2="0" y2="3.4" stroke="#e8e1d4" stroke-width="0.9"/>
    </pattern>
    <pattern id="bub-hatch-2" width="4.2" height="4.2" patternUnits="userSpaceOnUse" patternTransform="rotate(28)">
      <line x1="0" y1="0" x2="0" y2="4.2" stroke="#e8e1d4" stroke-width="0.7"/>
    </pattern>
    <filter id="bub-soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5"/></filter>
    <filter id="bub-rough" x="-20%" y="-20%" width="140%" height="140%">
      <feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="2" seed="3" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="7"/>
      <feGaussianBlur stdDeviation="0.7"/>
    </filter>
  </defs>`;
  document.body.append(defs);
}

export function createDream({ scene, camera, host, audio, still, headRect }) {
  const loader = new THREE.TextureLoader();
  const store = (key, fallback) => { try { return JSON.parse(sessionStorage.getItem(key) || fallback); } catch { return JSON.parse(fallback); } };
  const keep = (key, value) => { try { sessionStorage.setItem(key, JSON.stringify(value)); } catch {} };
  const seen = new Set(store(SEEN_KEY, "[]"));
  const used = new Set(store(USED_KEY, "[]"));
  const remember = (id) => { seen.add(id); keep(SEEN_KEY, [...seen]); };
  let material = null;          // dreams.json, fetched when the first dream begins
  const loadMaterial = () => material ??= fetch("dreams.json").then((r) => r.json()).catch(() => ({}));

  // ---- Scene pieces ----
  const portraitUniforms = { uMap: { value: null }, uInk: { value: INK }, uMix: { value: 0 }, uTime: { value: 0 } };
  const portrait = new THREE.Mesh(
    new THREE.PlaneGeometry(1.12, 1.4, 64, 80),
    new THREE.ShaderMaterial({
      uniforms: portraitUniforms, vertexShader: portraitVertex, fragmentShader: portraitFragment,
      transparent: true, depthWrite: false, depthTest: false, blending: THREE.AdditiveBlending,
    }));
  portrait.position.set(0.66, 0.02, -0.15);
  portrait.rotation.y = -0.38;
  portrait.renderOrder = 5;
  portrait.visible = false;
  scene.add(portrait);

  const hazeUniforms = { uInk: { value: INK }, uMix: { value: 0 }, uTime: { value: 0 } };
  const haze = new THREE.Mesh(
    new THREE.PlaneGeometry(9, 5),
    new THREE.ShaderMaterial({
      uniforms: hazeUniforms, vertexShader: quadVertex, fragmentShader: hazeFragment,
      transparent: true, depthWrite: false, depthTest: false, blending: THREE.AdditiveBlending,
    }));
  haze.position.set(0, 0, -1.6);
  haze.renderOrder = -1;
  haze.visible = false;
  scene.add(haze);

  // ---- The label strip and the bubbles (DOM, so the text stays sharp) ----
  defineBubbleDefs();
  const stageEl = document.querySelector(".stage");
  const layer = document.createElement("div");
  layer.className = "bubbles";
  layer.setAttribute("aria-hidden", "true");
  stageEl.append(layer);
  const box = document.createElement("div");
  box.className = "dream";
  box.hidden = true;
  box.setAttribute("role", "region");
  box.setAttribute("aria-label", "An imagined conversation");
  box.innerHTML = `
    <p class="dream-label">An imagined conversation</p>
    <span class="dream-credit"></span>
    <button type="button" class="dream-skip">Skip</button>
    <p class="sr-only" aria-live="polite"></p>`;
  stageEl.append(box);
  const spoken = box.querySelector(".sr-only");
  box.querySelector(".dream-skip").addEventListener("click", () => end());

  const replay = document.getElementById("dream-replay");
  replay.addEventListener("click", () => current && begin(current));

  // ---- State ----
  let current = null;           // the playing work
  let pending = null;           // work whose dream waits for START_AT
  let active = null;            // { work, lines, i, until }
  let target = 0;               // 1 while dreaming
  let bubble = null;            // the bubble now speaking
  const state = { mix: 0, level: 1.2 };   // level: the head's brightness, set by the scene

  window.addEventListener("player:track", (e) => {
    current = e.detail.work;
    replay.hidden = !current.dream;
    pending = current.dream && !seen.has(current.id) && !active ? current : null;
  });
  window.addEventListener("keydown", (e) => { if (e.key === "Escape" && active) end(); });

  const pick = (list) => list[Math.floor(Math.random() * list.length)];
  const shuffle = (list) => list.map((x) => [Math.random(), x]).sort((a, b) => a[0] - b[0]).map((x) => x[1]);

  // Opening, 2–3 fresh question/answer pairs, closing. A work's pairs start over
  // only once every one has been heard this session.
  function assemble(work, m) {
    if (!m) return null;
    const fresh = () => shuffle(m.qa.map((q, qi) => [q, qi]))
      .map(([q, qi]) => [q, qi, shuffle(q.answers.map((_, ai) => ai)).find((ai) => !used.has(`${work.id}:${qi}:${ai}`))])
      .filter((x) => x[2] !== undefined);
    let pairs = fresh();
    if (pairs.length < 2) {
      for (const k of [...used]) if (k.startsWith(work.id + ":")) used.delete(k);
      pairs = fresh();
    }
    pairs = pairs.slice(0, Math.random() < 0.5 ? 2 : 3);
    for (const [, qi, ai] of pairs) used.add(`${work.id}:${qi}:${ai}`);
    keep(USED_KEY, [...used]);
    return [pick(m.open), ...pairs.flatMap(([q, , ai]) => [{ who: "me", text: q.ask }, q.answers[ai]]), pick(m.close)];
  }

  async function begin(work) {
    pending = null;
    remember(work.id);
    if (active) end();
    const lines = assemble(work, (await loadMaterial())[work.id]);
    if (!lines) return;
    loader.load(work.dream.portrait, (tex) => {
      tex.colorSpace = THREE.SRGBColorSpace;
      portraitUniforms.uMap.value?.dispose();
      portraitUniforms.uMap.value = tex;
      portrait.visible = haze.visible = true;
      box.querySelector(".dream-credit").textContent = work.dream.credit;
      active = { work, lines, i: -1, until: performance.now() + 2600 };   // let the haze gather first
      target = 1;
      box.hidden = false;
      document.querySelector(".app").classList.add("dreaming");
    });
  }

  function end() {
    if (!active) return;
    active = null;
    target = 0;
    box.hidden = true;
    spoken.textContent = "";
    dissolve(bubble);
    bubble = null;
    document.querySelector(".app").classList.remove("dreaming");
  }

  // ---- Bubbles ----
  const tmp = new THREE.Vector3();
  const toStage = (v) => {
    tmp.copy(v).project(camera);
    return { x: (tmp.x + 1) / 2 * host.clientWidth, y: (1 - tmp.y) / 2 * host.clientHeight };
  };
  // Where each speaker's thoughts leave: my crown, and the top of the composer's portrait.
  function anchors() {
    const h = headRect();
    portrait.updateMatrixWorld();
    const top = toStage(tmp.set(-0.22, 0.6, 0).applyMatrix4(portrait.matrixWorld));
    const side = toStage(tmp.set(-0.5, 0.15, 0).applyMatrix4(portrait.matrixWorld));
    return {
      me: h && { x: h.left + h.width * 0.72, y: h.top + h.height * 0.16, head: h },
      them: { x: top.x, y: top.y + (side.y - top.y) * 0.2, head: { left: side.x, top: top.y } },
    };
  }

  function speak(line) {
    dissolve(bubble);
    const who = line.who === "me" ? "me" : "them";
    const el = document.createElement("div");
    el.className = "bubble";
    el.dataset.who = who;
    const text = document.createElement("p");
    text.className = "bubble-text";
    text.textContent = line.text;
    el.append(text);
    layer.append(el);

    // Size the shape to the set text, then place it above the speaker, toward the middle.
    const tw = text.offsetWidth, th = text.offsetHeight;
    const edge = 18, { svg, pad } = bubbleSvg(tw + 64, th + 48, edge);
    el.prepend(svg);
    text.style.left = `${pad + 32}px`; text.style.top = `${pad + 24}px`;
    const bw = tw + 64 + pad * 2, bh = th + 48 + pad * 2;
    const W = layer.clientWidth, H = layer.clientHeight;
    const a = anchors()[who] || { x: W / 2, y: H * 0.3 };
    const gap = Math.min(56, H * 0.06);
    let x = who === "me" ? a.x - bw * 0.18 : a.x - bw * 0.82;
    let y = a.y - bh - gap;
    const title = document.querySelector(".wordmark").getBoundingClientRect();
    const stage = layer.getBoundingClientRect();
    const minY = 12, titleBottom = title.bottom - stage.top + 10;
    x = Math.max(12, Math.min(W - bw - 12, x));
    if (x < title.right - stage.left + 10) y = Math.max(y, titleBottom);
    y = Math.max(minY, y);
    el.style.left = `${x}px`; el.style.top = `${y}px`;

    // Trailing bubbles, smallest at the speaker, rising to the thought.
    const tip = { x: x + (who === "me" ? bw * 0.22 : bw * 0.78), y: y + bh - pad * 0.8 };
    const trail = [];
    [9, 15, 23].forEach((size, i) => {
      const f = (i + 1) / 4;
      const t = document.createElement("div");
      t.className = "bubble bubble-trail";
      const { svg: s, pad: p } = bubbleSvg(size, size * 0.86, 4.5);
      t.append(s);
      t.style.left = `${a.x + (tip.x - a.x) * f - size / 2 - p}px`;
      t.style.top = `${a.y + (tip.y - a.y) * f - size / 2 - p}px`;
      t.style.setProperty("--delay", `${i * 110}ms`);
      layer.append(t);
      trail.push(t);
    });
    el.style.setProperty("--delay", "300ms");
    el.style.setProperty("--life", `${lineSeconds(line) + 2}s`);
    requestAnimationFrame(() => [...trail, el].forEach((n) => n.classList.add("shown")));
    spoken.textContent = `${who === "me" ? "Jeem" : active.work.surname}: ${line.text}`;
    return { el, trail };
  }

  function dissolve(b) {
    if (!b) return;
    for (const n of [b.el, ...b.trail]) {
      n.classList.add("gone");
      setTimeout(() => n.remove(), still ? 400 : 1800);
    }
  }

  const lineSeconds = (line) => Math.max(4.5, line.text.split(/\s+/).length * 0.42) + 1.4;   // incl. the resolve

  function update(dt, t) {
    if (pending && audio.currentTime >= START_AT && !audio.paused) begin(pending);
    if (active && performance.now() > active.until) {
      active.i += 1;
      if (active.i < active.lines.length) {
        const line = active.lines[active.i];
        bubble = speak(line);
        active.until = performance.now() + lineSeconds(line) * 1000;
      } else end();
    }
    const k = still ? 1 : 1 - Math.exp(-dt / 0.9);
    state.mix += (target - state.mix) * k;
    if (state.mix < 0.002 && target === 0) { state.mix = 0; portrait.visible = haze.visible = false; }
    // The composer shares my head's light: dim when paused, brighter when the music swells.
    hazeUniforms.uMix.value = state.mix;
    portraitUniforms.uMix.value = state.mix * Math.min(1.25, state.level / 1.2);
    portraitUniforms.uTime.value = hazeUniforms.uTime.value = still ? 0 : t;
    if (!still) portrait.position.y = 0.02 + 0.015 * Math.sin(t * 0.4);
  }

  state.update = update;
  state.begin = begin;
  Object.defineProperty(state, "dreaming", { get: () => !!active });
  return state;
}
