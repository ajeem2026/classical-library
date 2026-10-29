import * as THREE from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { MeshoptDecoder } from "three/addons/libs/meshopt_decoder.module.js";
import { engrave } from "./head.js";
import { createFlow } from "./flow.js";
import { createAnalysis } from "./analysis.js";
import { createDream } from "./dream.js";

const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
const phone = matchMedia("(max-width: 760px)");

// Head turn limits stay well inside the ±40° the single-photo mask can show.
const MAX_YAW = THREE.MathUtils.degToRad(14);
const MAX_PITCH = THREE.MathUtils.degToRad(7);

export async function createStage(host) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: "high-performance" });
  renderer.setClearColor(0x000000, 0);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(28, 1, 0.1, 50);

  const loader = new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
  const gltf = await loader.loadAsync("assets/head.glb");
  const model = gltf.scene;

  // Centre the head on its own bounds; turning happens around the neck-ish pivot.
  const box = new THREE.Box3().setFromObject(model);
  const size = box.getSize(new THREE.Vector3());
  const centre = box.getCenter(new THREE.Vector3());
  model.position.sub(centre);
  const head = new THREE.Group();
  head.add(model);
  scene.add(head);
  head.updateMatrixWorld(true);

  const uniforms = engrave(model);
  // Fewer staves and note-heads on phones.
  const flow = createFlow(model, phone.matches ? { staves: 4, notes: 60 } : { staves: 8, notes: 160 });
  let pixelScale = 300;
  let baseOffset = null;   // the head's framing outside dreams

  const fit = () => {
    const w = host.clientWidth, h = host.clientHeight;
    const pr = Math.min(window.devicePixelRatio || 1, phone.matches ? 1.25 : 1.75);
    renderer.setPixelRatio(pr);
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    // Fit the head's height to ~72% of the stage (86% on phones), never wider than allowed.
    const fillH = phone.matches ? 0.78 : 0.64, fillW = phone.matches ? 0.6 : 0.45;
    const target = size.y / fillH;
    const fov = THREE.MathUtils.degToRad(camera.fov);
    let dist = target / 2 / Math.tan(fov / 2);
    const widthDist = (size.x / fillW) / 2 / Math.tan(fov / 2) / camera.aspect;
    dist = Math.max(dist, widthDist) + size.z / 2;
    pixelScale = (h * pr) / (2 * Math.tan(fov / 2));
    camera.position.set(0, 0, dist);
    camera.lookAt(0, 0, 0);
    // On wide stages, frame the head right of centre and a little low, leaving
    // room above for the crown stream; the caption sits in the lower left.
    if (!phone.matches && w > h) {
      // Centre the head at least half its width clear of the caption's right edge.
      const cap = document.querySelector(".caption")?.getBoundingClientRect();
      const box = host.getBoundingClientRect();
      const headW = h * fillH * (size.x / size.y) * 1.15;            // incl. ears and rim
      const minX = cap ? cap.right - box.left + headW / 2 + 24 : 0;
      const cx = Math.max(w * 0.59, minX);
      baseOffset = { x: -(cx - w / 2), y: -h * 0.07, w, h };
      camera.setViewOffset(w, h, baseOffset.x, baseOffset.y, w, h);
    } else { baseOffset = null; camera.clearViewOffset(); }
    camera.updateProjectionMatrix();
  };
  fit();
  new ResizeObserver(fit).observe(host);
  host.replaceChildren(renderer.domElement);

  // ---- Gaze: the head turns slowly toward the cursor ----
  const aim = { yaw: 0, pitch: 0 };
  // ?yaw=-14 pins the pose in degrees, for comparing screenshots.
  const pinned = new URLSearchParams(location.search).get("yaw");
  if (pinned !== null) aim.yaw = THREE.MathUtils.degToRad(Number(pinned) || 0);
  else window.addEventListener("pointermove", (e) => {
    const r = host.getBoundingClientRect();
    const x = ((e.clientX - (r.left + r.width / 2)) / (window.innerWidth / 2));
    const y = ((e.clientY - (r.top + r.height / 2)) / (window.innerHeight / 2));
    aim.yaw = THREE.MathUtils.clamp(x, -1, 1) * MAX_YAW;
    aim.pitch = THREE.MathUtils.clamp(y, -1, 1) * MAX_PITCH;
  }, { passive: true });
  if (pinned === null) document.addEventListener("pointerleave", () => { aim.yaw = 0; aim.pitch = 0; });

  // ---- Playing / paused ----
  let playing = false;
  window.addEventListener("player:play", () => (playing = true));
  window.addEventListener("player:pause", () => (playing = false));
  const audio = document.getElementById("audio");
  playing = !audio.paused;
  const bands = createAnalysis(audio);
  const dream = createDream({ scene, audio, still: reducedMotion.matches });
  if (window.__playerTrack) window.dispatchEvent(new CustomEvent("player:track", { detail: window.__playerTrack }));

  // ---- Loop ----
  const clock = new THREE.Clock();
  let visible = true;
  new IntersectionObserver(([e]) => (visible = e.isIntersecting)).observe(host);

  renderer.setAnimationLoop(() => {
    if (!visible || document.hidden) return;
    const dt = Math.min(clock.getDelta(), 0.1);
    const t = clock.elapsedTime;
    const still = reducedMotion.matches;
    bands.update(dt);
    dream.update(dt, t);
    const m = dream.mix;     // 0 awake .. 1 dreaming
    // ~1.2 s ease toward the cursor; a slow breath of movement while playing.
    const k = 1 - Math.exp(-dt / 0.4);
    const sway = still || !playing ? 0 : 1;
    const yaw = still ? 0 : aim.yaw + sway * Math.sin(t * 0.21) * 0.03;
    const pitch = still ? 0 : aim.pitch + sway * Math.sin(t * 0.17) * 0.015;
    head.rotation.y += (THREE.MathUtils.lerp(yaw, 0.6, m) - head.rotation.y) * k;
    head.rotation.x += (THREE.MathUtils.lerp(pitch, 0, m) - head.rotation.x) * k;
    flow.update(dt, bands, playing, still, pixelScale, 1 - 0.55 * m);
    // In a dream the head moves left and turns toward the composer (34°, inside the ±40° limit),
    // and the framing recentres on the two of them.
    head.position.x = -0.5 * m;
    if (baseOffset) camera.setViewOffset(baseOffset.w, baseOffset.h, baseOffset.x * (1 - m), baseOffset.y, baseOffset.w, baseOffset.h);
    // Bass gives the head a faint pulse; loud passages lift its light.
    head.scale.setScalar(1 + (still ? 0 : bands.bass * 0.012));
    const level = playing ? 1.2 + 0.3 * bands.level : 0.5;
    uniforms.uLevel.value += (level - uniforms.uLevel.value) * (1 - Math.exp(-dt / 0.6));
    dream.level = uniforms.uLevel.value;
    head.updateMatrixWorld(true);
    uniforms.uHead.value.copy(model.matrixWorld);
    uniforms.uHeadInverse.value.copy(model.matrixWorld).invert();
    renderer.render(scene, camera);
  });

  return { renderer, scene, camera, head, uniforms, bands, dream };
}
