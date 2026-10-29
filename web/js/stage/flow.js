// The music inside the head: five-line staves that enter at the ears, curl
// through the cranium and leave at the crown, with engraved note-heads riding
// on them. Loud passages bring in more staves until the head is full of them;
// a quiet movement is one faint stave drifting. Coordinates are the model's own.
import * as THREE from "three";

const INK = new THREE.Color("#e8e1d4");
const AMBER = new THREE.Color("#d9a441");
const C = new THREE.Vector3(0, 0.15, -0.55);   // cranium centre and half-extents
const R = new THREE.Vector3(0.5, 0.746, 0.625);
const SEGMENTS = 220, LINES = 5, SPACING = 0.016;

function rng(seed) {
  return () => ((seed = (seed * 16807) % 2147483647) - 1) / 2147483646;
}

function staffPath(i, rand) {
  const side = i % 2 ? 1 : -1;
  // Interior points stay behind the face plane and climb, so each stave winds up into the cranium.
  const inside = (y) => new THREE.Vector3(
    (rand() * 2 - 1) * R.x * 0.55, y, -0.62 + (rand() * 2 - 1) * 0.2);
  return new THREE.CatmullRomCurve3([
    new THREE.Vector3(side * (0.7 + rand() * 0.2), -0.75 - rand() * 0.2, -0.95),  // from behind and below
    new THREE.Vector3(side * 0.62, -0.28, -0.72),
    new THREE.Vector3(side * 0.53, 0.02 + rand() * 0.06, -0.5),          // in at the ear
    inside(0.2 + rand() * 0.1), inside(0.38 + rand() * 0.1), inside(0.56 + rand() * 0.1),
    new THREE.Vector3((rand() - 0.5) * 0.25, 0.86, -0.55 + (rand() - 0.5) * 0.3), // out through the crown
    new THREE.Vector3((rand() - 0.5) * 0.6, 1.2, -0.6 + (rand() - 0.5) * 0.4),
    new THREE.Vector3(-side * (0.25 + rand() * 0.35), 1.5, -0.8),        // fades out below the frame's top
  ], false, "centripetal");
}

const staffVertex = /* glsl */ `
  attribute vec3 aBin;
  attribute float aSide;
  attribute float aT;
  uniform float uWidth;
  varying float vSide;
  varying float vT;
  varying float vBehindFace;
  void main() {
    vSide = aSide; vT = aT;
    // Inside the face's footprint the music glows behind the engraving, not over it.
    float r = length(vec2(position.x / 0.44, (position.y - 0.12) / 0.62));
    vBehindFace = 1.0 - 0.82 * (1.0 - smoothstep(0.7, 1.05, r));
    vec3 p = position + aBin * aSide * uWidth;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0);
  }
`;
const staffFragment = /* glsl */ `
  uniform vec3 uColor;
  uniform float uAlpha;
  uniform float uPhase;
  varying float vSide;
  varying float vT;
  varying float vBehindFace;
  void main() {
    float edge = 1.0 - smoothstep(0.35, 1.0, abs(vSide));
    float ends = smoothstep(0.0, 0.07, vT) * (1.0 - smoothstep(0.72, 1.0, vT));
    // Light travels along the staff in phrases.
    float pulse = pow(0.5 + 0.5 * sin((vT * 9.0 - uPhase) * 6.2832), 4.0);
    float a = (0.34 + 0.9 * pulse) * edge * ends * uAlpha * vBehindFace;
    gl_FragColor = vec4(uColor * a, a);
  }
`;

function staffGeometry(curve) {
  const frames = curve.computeFrenetFrames(SEGMENTS, false);
  const pos = [], bin = [], side = [], t = [], index = [];
  for (let l = 0; l < LINES; l++) {
    const off = (l - (LINES - 1) / 2) * SPACING;
    for (let j = 0; j <= SEGMENTS; j++) {
      const u = j / SEGMENTS;
      const p = curve.getPointAt(u).addScaledVector(frames.normals[j], off);
      for (const s of [-1, 1]) {
        pos.push(p.x, p.y, p.z);
        const b = frames.binormals[j];
        bin.push(b.x, b.y, b.z);
        side.push(s);
        t.push(u);
      }
      if (j < SEGMENTS) {
        const a = (l * (SEGMENTS + 1) + j) * 2;
        index.push(a, a + 1, a + 2, a + 1, a + 3, a + 2);
      }
    }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute("aBin", new THREE.Float32BufferAttribute(bin, 3));
  g.setAttribute("aSide", new THREE.Float32BufferAttribute(side, 1));
  g.setAttribute("aT", new THREE.Float32BufferAttribute(t, 1));
  g.setIndex(index);
  return { geometry: g, frames };
}

const noteVertex = /* glsl */ `
  attribute float aSize;
  attribute float aBright;
  attribute float aAmber;
  uniform float uScale;
  varying float vBright;
  varying float vAmber;
  void main() {
    float r = length(vec2(position.x / 0.44, (position.y - 0.12) / 0.62));
    vBright = aBright * (1.0 - 0.82 * (1.0 - smoothstep(0.7, 1.05, r))); vAmber = aAmber;
    vec4 mv = modelViewMatrix * vec4(position, 1.0);
    gl_PointSize = aSize * uScale / -mv.z;
    gl_Position = projectionMatrix * mv;
  }
`;
const noteFragment = /* glsl */ `
  uniform vec3 uInk;
  uniform vec3 uAmber;
  varying float vBright;
  varying float vAmber;
  void main() {
    // An engraved note-head: a filled ellipse tilted about 20 degrees.
    vec2 p = gl_PointCoord * 2.0 - 1.0;
    p = mat2(0.94, -0.34, 0.34, 0.94) * p;
    float d = length(p / vec2(1.0, 0.68));
    float a = (1.0 - smoothstep(0.78, 0.95, d)) * vBright;
    if (a < 0.01) discard;
    gl_FragColor = vec4(mix(uInk, uAmber, vAmber) * a, a);
  }
`;

export function createFlow(parent, { staves = 8, notes = 160 } = {}) {
  const rand = rng(1868);
  const group = new THREE.Group();
  parent.add(group);

  const list = [];
  for (let i = 0; i < staves; i++) {
    const curve = staffPath(i, rand);
    const { geometry, frames } = staffGeometry(curve);
    const material = new THREE.ShaderMaterial({
      uniforms: {
        uColor: { value: INK }, uAlpha: { value: 0 }, uPhase: { value: rand() * 10 }, uWidth: { value: 0.0022 },
      },
      vertexShader: staffVertex, fragmentShader: staffFragment,
      transparent: true, depthWrite: false, depthTest: false, blending: THREE.AdditiveBlending,
      side: THREE.DoubleSide,
    });
    const mesh = new THREE.Mesh(geometry, material);
    mesh.renderOrder = 3;
    group.add(mesh);
    // A lookup table of centre points for the note-heads.
    const table = [];
    for (let j = 0; j <= SEGMENTS; j++) table.push(curve.getPointAt(j / SEGMENTS));
    list.push({ material, table, normals: frames.normals, intensity: 0 });
  }

  // Note-heads sit on a line or a space of their staff and travel with it.
  const nPos = new Float32Array(notes * 3), nSize = new Float32Array(notes),
        nBright = new Float32Array(notes), nAmber = new Float32Array(notes);
  const meta = [];
  for (let k = 0; k < notes; k++) {
    meta.push({ staff: k % staves, t: rand(), slot: Math.floor(rand() * 9) - 4, speed: 0.8 + rand() * 0.4, seed: rand() * 100 });
    nAmber[k] = k % staves === 0 && rand() < 0.35 ? 1 : 0;   // the leading staff carries a little gaslight
  }
  const ng = new THREE.BufferGeometry();
  ng.setAttribute("position", new THREE.BufferAttribute(nPos, 3));
  ng.setAttribute("aSize", new THREE.BufferAttribute(nSize, 1));
  ng.setAttribute("aBright", new THREE.BufferAttribute(nBright, 1));
  ng.setAttribute("aAmber", new THREE.BufferAttribute(nAmber, 1));
  const noteMaterial = new THREE.ShaderMaterial({
    uniforms: { uInk: { value: INK }, uAmber: { value: AMBER }, uScale: { value: 300 } },
    vertexShader: noteVertex, fragmentShader: noteFragment,
    transparent: true, depthWrite: false, depthTest: false, blending: THREE.AdditiveBlending,
  });
  const points = new THREE.Points(ng, noteMaterial);
  points.frustumCulled = false;
  points.renderOrder = 4;
  group.add(points);

  const tmp = new THREE.Vector3();
  let clock = 0;

  // bands: {bass, mid, high, level}; playing: bool; still: reduced motion.
  function update(dt, bands, playing, still, pixelScale, dim = 1) {
    clock += dt;
    noteMaterial.uniforms.uScale.value = pixelScale;
    const presence = (playing ? 1 : 0.3) * dim;
    const active = 1 + Math.pow(bands.level, 0.8) * staves * 1.15;   // loud passages flood the head
    const speed = playing && !still ? 0.025 + bands.mid * 0.14 : 0;
    const width = 0.0022 * (1 + bands.bass * 1.6);

    list.forEach((s, i) => {
      const target = i === 0 ? 0.3 + 0.7 * bands.level
        : Math.min(1, Math.max(0, active - i)) * (0.35 + 0.65 * bands.level);
      s.intensity += (target - s.intensity) * (1 - Math.exp(-dt / 1.2));
      const u = s.material.uniforms;
      u.uAlpha.value = s.intensity * presence;
      u.uWidth.value = width;
      u.uPhase.value += speed * 9 * dt;
    });

    for (let k = 0; k < notes; k++) {
      const m = meta[k], s = list[m.staff];
      m.t = (m.t + speed * m.speed * dt) % 1;
      const f = m.t * SEGMENTS, j = Math.floor(f), w = f - j;
      tmp.lerpVectors(s.table[j], s.table[Math.min(j + 1, SEGMENTS)], w)
        .addScaledVector(s.normals[j], m.slot * SPACING * 0.5);
      nPos.set([tmp.x, tmp.y, tmp.z], k * 3);
      const ends = Math.min(1, m.t / 0.08) * Math.min(1, (1 - m.t) / 0.28);
      const sparkle = still ? 0 : bands.high * Math.max(0, Math.sin(clock * 11 + m.seed * 7)) ** 6;
      nBright[k] = s.intensity * presence * ends * (0.55 + 0.45 * bands.level + 0.9 * sparkle);
      nSize[k] = 0.017 * (1 + bands.bass * 0.8 + sparkle * 0.6);
    }
    ng.attributes.position.needsUpdate = true;
    ng.attributes.aBright.needsUpdate = true;
    ng.attributes.aSize.needsUpdate = true;
  }

  return { group, update };
}
