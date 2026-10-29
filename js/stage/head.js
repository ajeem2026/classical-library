// The head as a steel engraving drawn in light: bone-white hatch lines on the
// dark ground, additive and see-through so later layers show inside it.
import * as THREE from "three";

const INK = new THREE.Color("#e8e1d4");

// The face UVs are a frontal planar projection of the photo (fitted from the
// mesh, error < 0.005): u = 0.707x + 0.492, v = 0.546 - 0.566y. Using the same
// projection on the cranium brings the photographed hair and forehead onto it.
// Landmarks below are in the model's own units, read off the photo through it.
const shared = /* glsl */ `
  uniform sampler2D uMap;
  uniform vec3 uInk;
  uniform float uLevel;     // ~1.35 playing, 0.5 paused
  uniform float uDensity;   // lines per head-unit
  varying vec3 vLocal;
  varying vec3 vNormalL;
  varying vec3 vNormalV;
  varying vec3 vViewDir;

  vec2 photoUv(vec3 p) { return vec2(0.70705 * p.x + 0.49174, 0.54641 - 0.56563 * p.y); }

  // Antialiased line of half-width w (0..0.5) in a repeating coordinate.
  float hatch(float coord, float w) {
    float d = abs(fract(coord) - 0.5);
    float aa = fwidth(coord) * 0.75;
    return 1.0 - smoothstep(w - aa, w + aa, d);
  }

  float lumAt(vec2 uv) { return dot(texture2D(uMap, uv).rgb, vec3(0.299, 0.587, 0.114)); }

  // Region masks for extra local contrast: eyes behind the glasses, mouth and beard.
  float ellipse(vec2 p, vec2 c, vec2 r) { return 1.0 - smoothstep(0.7, 1.0, length((p - c) / r)); }
  float eyeMask(vec3 p) {
    return max(ellipse(p.xy, vec2(-0.226, 0.248), vec2(0.13, 0.07)),
               ellipse(p.xy, vec2(0.259, 0.248), vec2(0.13, 0.07)));
  }
  float lowerMask(vec3 p) {
    return ellipse(p.xy, vec2(0.0, -0.33), vec2(0.36, 0.3));
  }

  // Tone 0..1 for skin: the photo with masked local contrast, shaped by a key light.
  float skinTone(vec3 p, vec3 nView) {
    vec2 uv = photoUv(p);
    float lum = lumAt(uv);
    float r = 0.022, mean = 0.0;
    for (int i = 0; i < 8; i++) {
      float a = float(i) * 0.785398;
      mean += lumAt(uv + r * vec2(cos(a), sin(a) * 0.8));
    }
    mean /= 8.0;
    float eyes = eyeMask(p), lower = lowerMask(p);
    float gain = 1.0 + 1.6 * eyes + 0.9 * lower;
    lum = mean + (lum - mean) * gain - 0.06 * eyes;
    lum = smoothstep(0.06, 0.72, lum);
    float key = clamp(dot(nView, normalize(vec3(-0.45, 0.5, 0.75))), 0.0, 1.0);
    return clamp(pow(lum, 0.9) * (0.5 + 0.75 * key), 0.0, 1.0);
  }

  // Burin lines that wrap a smooth head-shaped surface, so they bend over the
  // cheeks and jaw without clumping at the nose.
  float skinLines(vec3 p, float tone) {
    // A bow whose slope never exceeds the diagonal's (|grad| <= 0.6), so lines never close into rings.
    float bow = 0.6 * p.x * p.x - 0.3 * (p.y - 0.05) * (p.y - 0.05);
    float c1 = (dot(p.xy, normalize(vec2(0.88, 0.47))) - bow) * uDensity;   // no depth term: on steep sides it made rings
    float c2 = (dot(p.xy, normalize(vec2(-0.42, 0.91))) + 0.7 * bow) * uDensity * 1.15;
    float ink = hatch(c1, mix(0.03, 0.29, tone));
    ink = max(ink, hatch(c2, 0.12) * smoothstep(0.55, 0.85, tone));            // cross-hatch the lights
    ink = max(ink, 0.35 * (1.0 - smoothstep(0.0, 0.18, tone)) * hatch(c1 * 0.5, 0.06)); // keep darks legible
    return ink;
  }

  // How much of a point the face mask covers; the cranium takes the complement.
  float faceCover(vec3 p) {
    float r = length(vec2(p.x / 0.47, (p.y - 0.02) / 0.57));
    return 1.0 - smoothstep(0.78, 1.0, r);
  }
`;

const vertex = /* glsl */ `
  uniform mat4 uHeadInverse;
  uniform mat4 uHead;
  varying vec3 vLocal;
  varying vec3 vNormalL;
  varying vec3 vNormalV;
  varying vec3 vViewDir;
  void main() {
    vec4 world = modelMatrix * vec4(position, 1.0);
    vLocal = (uHeadInverse * world).xyz;
    #ifdef CRANIUM
      // Narrow the shell toward the jaw so the silhouette reads as a head, not an egg.
      vLocal.x *= mix(1.0, 0.6, smoothstep(0.2, -0.55, vLocal.y));
      // A hint of ears: a soft bulge on each side at eye-to-nose height, just behind the face.
      float ear = exp(-pow((vLocal.y - 0.06) / 0.13, 2.0) - pow((vLocal.z + 0.42) / 0.11, 2.0));
      vLocal.x += sign(vLocal.x) * 0.065 * ear;
      world = uHead * vec4(vLocal, 1.0);
    #endif
    vNormalL = normalize(mat3(uHeadInverse) * mat3(modelMatrix) * normal);
    vec4 mv = viewMatrix * world;
    vNormalV = normalize(normalMatrix * normal);
    vViewDir = normalize(-mv.xyz);
    gl_Position = projectionMatrix * mv;
  }
`;

const faceFragment = /* glsl */ `
  ${shared}
  void main() {
    vec3 n = normalize(vNormalV);
    float tone = skinTone(vLocal, n);
    float ink = skinLines(vLocal, tone);
    float edge = faceCover(vLocal) * smoothstep(-0.05, 0.25, dot(n, vViewDir));
    float a = ink * edge * uLevel;
    gl_FragColor = vec4(uInk * a, a);
  }
`;

const craniumFragment = /* glsl */ `
  ${shared}
  const vec3 C = vec3(0.0, 0.15085, -0.55205);   // cranium centre and half-extents
  const vec3 R = vec3(0.5, 0.74574, 0.62502);
  void main() {
    vec3 p = vLocal;
    vec3 q = (p - C) / R;                        // on the unit sphere
    vec3 n = normalize(vNormalV);
    float facing = abs(dot(n, vViewDir));
    float key = clamp(dot(n, normalize(vec3(-0.45, 0.5, 0.75))), 0.0, 1.0);

    // Where the photo can be trusted: the front of the skull, above the cheeks.
    float front = smoothstep(-0.25, 0.25, q.z);
    vec2 uv = photoUv(p);
    // Smoothed tone for hair, so single photo pixels don't drive the strands.
    float lum = lumAt(uv) * 0.2;
    for (int i = 0; i < 8; i++) {
      float a = float(i) * 0.785398;
      vec2 d = vec2(cos(a), sin(a));
      lum += 0.05 * lumAt(uv + 0.015 * d) + 0.05 * lumAt(uv + 0.032 * d);
    }

    // Hair: dark in the photo at the front; everything above the nape at the back.
    float hairPhoto = smoothstep(0.5, 0.26, lum) * smoothstep(0.1, 0.3, p.y);
    float hairBack = smoothstep(-0.55, -0.3, q.y);
    float hair = mix(hairBack, hairPhoto, front);

    // Strands sweep up from the hairline and back over the crown, with a slight wave.
    // Front: strands rise from the hairline, leaning right and fanning out over the dome.
    float rise = p.y - 0.55;
    float sweepFront = (p.x * (1.0 - 0.45 * rise) - 0.22 * rise + 0.05 * sin(p.y * 9.0)) * 95.0;
    // Back: the same sweep continues over the crown and down to the nape.
    float az = atan(q.x, q.z);
    float sweepBack = az * 62.0 + q.y * 5.0 + 0.6 * sin(q.y * 7.0 + az * 3.0);
    float hairLight = 0.4 + 0.6 * key;
    float wFront = hatch(sweepFront, mix(0.08, 0.2, hairLight));
    float wBack = hatch(sweepBack, mix(0.08, 0.2, hairLight));
    float breaks = 0.65 + 0.35 * sin(p.y * 31.0 + p.x * 13.0);   // smooth, no per-strand jumps
    // The front hatch is a flat projection: where the skull turns sideways it folds and the
    // lines ring, so the sides take the surface-following meridians instead.
    float side = smoothstep(0.45, 0.8, abs(normalize(vNormalL).x));
    float hairInk = mix(wBack, wFront, front * (1.0 - side))
                  * (0.45 + 0.4 * hairLight) * breaks
                  * (1.0 - 0.75 * smoothstep(0.55, 0.95, q.y));   // the crown falls into shadow

    // Forehead skin between the mask and the hairline, hatched like the face.
    float skinZone = front * (1.0 - hair) * smoothstep(0.38, 0.5, p.y) * (1.0 - smoothstep(0.42, 0.5, abs(p.x)));
    float skinInk = skinLines(p, skinTone(p, n)) * skinZone;

    // The vessel itself: contour hatching and a crisp silhouette line.
    float contour = hatch(q.y * uDensity * 0.4, mix(0.04, 0.12, key)) * 0.2;
    float rimLine = smoothstep(0.16, 0.03, facing) * 0.75;

    float body = max(max(hairInk * hair, skinInk), contour * (1.0 - hair) * (1.0 - skinZone));
    float a = max(body * (1.0 - faceCover(p)), rimLine) * uLevel;
    gl_FragColor = vec4(uInk * a, a);
  }
`;


const neckFragment = /* glsl */ `
  uniform vec3 uInk;
  uniform float uLevel;
  uniform float uDensity;
  varying vec3 vLocal;
  varying vec3 vNormalV;
  varying vec3 vViewDir;
  float hatch(float coord, float w) {
    float d = abs(fract(coord) - 0.5);
    float aa = fwidth(coord) * 0.75;
    return 1.0 - smoothstep(w - aa, w + aa, d);
  }
  void main() {
    vec3 n = normalize(vNormalV);
    float facing = abs(dot(n, vViewDir));
    float key = clamp(dot(n, normalize(vec3(-0.45, 0.5, 0.75))), 0.0, 1.0);
    float contour = hatch(vLocal.y * uDensity * 0.4, mix(0.04, 0.12, key)) * 0.2;
    float rimLine = smoothstep(0.16, 0.03, facing) * 0.75;
    // Starts under the jaw and dissolves toward the collar.
    float fade = smoothstep(-0.5, -0.62, vLocal.y) * smoothstep(-1.15, -0.85, vLocal.y);
    float a = max(contour, rimLine) * fade * uLevel;
    gl_FragColor = vec4(uInk * a, a);
  }
`;

function neckMesh(uniforms) {
  // Profile from just under the jaw to the collar: narrow, then a slight flare.
  const profile = [[0.27, -0.42], [0.25, -0.6], [0.235, -0.8], [0.25, -0.98], [0.3, -1.15]]
    .map(([r, y]) => new THREE.Vector2(r, y));
  const geometry = new THREE.LatheGeometry(profile, 48);
  geometry.translate(0, 0, -0.42);
  const material = new THREE.ShaderMaterial({
    uniforms, vertexShader: vertex, fragmentShader: neckFragment,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  });
  const mesh = new THREE.Mesh(geometry, material);
  mesh.renderOrder = 0;
  return mesh;
}

export function engrave(head, { density = 72 } = {}) {
  let map = null;
  head.traverse((o) => { if (o.isMesh && o.material.map) map = o.material.map; });
  const uniforms = {
    uHeadInverse: { value: new THREE.Matrix4() },
    uHead: { value: new THREE.Matrix4() },
    uMap: { value: map },
    uInk: { value: INK },
    uLevel: { value: 0.5 },
    uDensity: { value: density },
  };
  head.traverse((o) => {
    if (!o.isMesh) return;
    const isFace = !!o.material.map;
    const material = new THREE.ShaderMaterial({
      uniforms,
      vertexShader: vertex,
      fragmentShader: isFace ? faceFragment : craniumFragment,
      defines: isFace ? {} : { CRANIUM: 1 },
      transparent: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
    });
    o.material.dispose();
    o.material = material;
    o.renderOrder = isFace ? 2 : 1;
  });
  head.add(neckMesh(uniforms));
  return uniforms;
}
