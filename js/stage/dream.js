// Dream conversations: once per work per session (and on request), my head and
// the composer face each other in a drifting engraved haze while an imagined
// exchange plays as subtitles. The music carries on underneath.
import * as THREE from "three";

const INK = new THREE.Color("#e8e1d4");
const START_AT = 70;          // seconds into the first track played from a work
const SEEN_KEY = "cl:dreamt";

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

export function createDream({ scene, audio, still }) {
  const works = new Map();      // work id -> work (with .dream)
  const loader = new THREE.TextureLoader();
  let seen;
  try { seen = new Set(JSON.parse(sessionStorage.getItem(SEEN_KEY) || "[]")); } catch { seen = new Set(); }
  const remember = (id) => { seen.add(id); try { sessionStorage.setItem(SEEN_KEY, JSON.stringify([...seen])); } catch {} };

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

  // ---- Subtitles (DOM, so they stay sharp and readable) ----
  const stageEl = document.querySelector(".stage");
  const box = document.createElement("div");
  box.className = "dream";
  box.hidden = true;
  box.setAttribute("role", "region");
  box.setAttribute("aria-label", "Imagined conversation");
  box.innerHTML = `
    <p class="dream-label">Imagined conversation</p>
    <p class="dream-line" aria-live="polite"><span class="dream-who"></span><span class="dream-text"></span></p>
    <div class="dream-foot"><span class="dream-credit"></span><button type="button" class="dream-skip">Skip</button></div>`;
  stageEl.append(box);
  const whoEl = box.querySelector(".dream-who"), textEl = box.querySelector(".dream-text");
  box.querySelector(".dream-skip").addEventListener("click", () => end());

  const replay = document.getElementById("dream-replay");
  replay.addEventListener("click", () => current && begin(current));

  // ---- State ----
  let current = null;           // the playing work
  let pending = null;           // work whose dream waits for START_AT
  let active = null;            // { work, lines, i, until }
  let target = 0;               // 1 while dreaming
  const state = { mix: 0, level: 1.2 };   // level: the head's brightness, set by the scene

  window.addEventListener("player:track", (e) => {
    current = e.detail.work;
    replay.hidden = !current.dream;
    pending = current.dream && !seen.has(current.id) && !active ? current : null;
  });
  window.addEventListener("keydown", (e) => { if (e.key === "Escape" && active) end(); });

  function begin(work) {
    pending = null;
    remember(work.id);
    loader.load(work.dream.portrait, (tex) => {
      tex.colorSpace = THREE.SRGBColorSpace;
      portraitUniforms.uMap.value?.dispose();
      portraitUniforms.uMap.value = tex;
      portrait.visible = haze.visible = true;
      box.querySelector(".dream-credit").textContent = work.dream.credit;
      active = { work, i: -1, until: performance.now() + 2200 };   // let the haze gather first
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
    textEl.textContent = whoEl.textContent = "";
    document.querySelector(".app").classList.remove("dreaming");
  }

  function showLine(i) {
    const line = active.work.dream.lines[i];
    whoEl.textContent = line.who === "me" ? "Jeem" : active.work.surname;
    textEl.textContent = line.text;
    box.dataset.who = line.who;
    const secs = Math.max(4.5, line.text.split(/\s+/).length * 0.42);
    active.until = performance.now() + secs * 1000;
  }

  function update(dt, t) {
    if (pending && audio.currentTime >= START_AT && !audio.paused) begin(pending);
    if (active && performance.now() > active.until) {
      active.i += 1;
      if (active.i < active.work.dream.lines.length) showLine(active.i);
      else end();
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
  return state;
}
