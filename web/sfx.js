// Library sound effects, synthesised here with Web Audio: no recordings, so no licences.
// Each sound is computed sample by sample (filtered noise and decaying sines), then set so
// its loudest 50 ms sits 26 dB under the library's median loudness (−28.1 dBFS RMS, from
// data/loudness.json), i.e. at −54.1 dBFS, and scaled by the player's volume like the music.
// tools/sfx_check.js measures every sound against that ceiling.
(function () {
  const MUSIC_DB = -28.1;
  const TARGET_DB = MUSIC_DB - 26;

  function rng(seed) {             // mulberry32: small, seedable
    return () => {
      seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
      let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // RBJ biquad; set() may be called while running, for sweeps.
  function biquad(type, sr) {
    let b0, b1, b2, a1, a2, x1 = 0, x2 = 0, y1 = 0, y2 = 0;
    const f = {
      set(freq, q) {
        const w = 2 * Math.PI * Math.min(freq, sr * 0.45) / sr, c = Math.cos(w), al = Math.sin(w) / (2 * q);
        let n0, n1, n2;
        if (type === "lp") { n0 = (1 - c) / 2; n1 = 1 - c; n2 = n0; }
        else if (type === "hp") { n0 = (1 + c) / 2; n1 = -(1 + c); n2 = n0; }
        else { n0 = al; n1 = 0; n2 = -al; }                 // band-pass, 0 dB peak
        const d0 = 1 + al;
        b0 = n0 / d0; b1 = n1 / d0; b2 = n2 / d0; a1 = -2 * c / d0; a2 = (1 - al) / d0;
        return f;
      },
      run(x) {
        const y = b0 * x + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2;
        x2 = x1; x1 = x; y2 = y1; y1 = y;
        return y;
      },
    };
    return f;
  }

  const ramp = (t, a, b) => Math.min(1, Math.max(0, (t - a) / (b - a)));
  const decay = (t, at, tau) => (t < at ? 0 : Math.exp(-(t - at) / tau));

  // Stick-slip friction: a train of tiny catches at a wandering rate, the grain of wood on wood.
  function friction(n, sr, r, rate, jitter) {
    const out = new Float32Array(n);
    let next = 0;
    while (next < n) {
      const amp = 0.45 + 0.55 * r(), tau = sr * (0.004 + 0.004 * r());
      for (let i = next; i < Math.min(n, next + tau * 5); i++) out[i] += amp * Math.exp(-(i - next) / tau);
      next += Math.round(sr / (rate * (1 + jitter * (r() - 0.5))));
    }
    return out;
  }

  const SOUNDS = {
    // Book slid out: a soft wooden scrape that slows as it comes, under a cloth whisper.
    slide(sr, r) {
      const len = 0.46, n = Math.round(sr * len), out = new Float32Array(n);
      const grit = friction(n, sr, r, 70, 0.6);
      const bp = biquad("bp", sr), hp = biquad("hp", sr).set(3600, 0.7), lp = biquad("lp", sr).set(8000, 0.7);
      for (let i = 0; i < n; i++) {
        const t = i / sr;
        if (i % 64 === 0) bp.set(1500 - 600 * (t / len), 1.1);
        const body = ramp(t, 0, 0.05) * (1 - ramp(t, 0.3, len));
        const scrape = bp.run(r() * 2 - 1) * (0.35 + grit[i]) * body;
        const whisper = lp.run(hp.run(r() * 2 - 1)) * ramp(t, 0, 0.12) * (1 - ramp(t, 0.22, len)) * 0.32;
        out[i] = scrape + whisper;
      }
      return out;
    },
    // Book opened: a page turned over, a flutter of paper and a soft fall.
    page(sr, r) {
      const len = 0.62, n = Math.round(sr * len), out = new Float32Array(n);
      const bp = biquad("bp", sr), lp = biquad("lp", sr).set(1100, 0.7), hp = biquad("hp", sr).set(2200, 0.7);
      const flap = biquad("lp", sr).set(900, 0.8);
      for (let i = 0; i < n; i++) {
        const t = i / sr;
        if (i % 64 === 0) bp.set(2400 + 3200 * Math.sin(Math.PI * Math.min(1, t / 0.45)), 0.8);
        const lift = ramp(t, 0, 0.08) * (1 - ramp(t, 0.36, 0.46));
        const flutter = 0.55 + 0.45 * Math.sin(2 * Math.PI * (34 - 30 * t) * t);
        const crackle = r() < 0.004 * lift ? (r() * 2 - 1) * 3 : 0;
        const paper = bp.run(r() * 2 - 1) * lift * flutter + hp.run(crackle) * 0.5;
        const air = lp.run(r() * 2 - 1) * Math.sin(Math.PI * Math.min(1, t / 0.46)) * 0.5;
        const fall = flap.run(r() * 2 - 1) * decay(t, 0.44, 0.03) * 1.3;
        out[i] = paper + air + fall;
      }
      return out;
    },
    // Movement chosen: a felt hammer's tock, soft at the front, low and short.
    tock(sr, r) {
      const len = 0.24, n = Math.round(sr * len), out = new Float32Array(n);
      const lp = biquad("lp", sr).set(1800, 0.7);
      let p1 = 0, p2 = 0;
      for (let i = 0; i < n; i++) {
        const t = i / sr, felt = ramp(t, 0, 0.004);
        p1 += 2 * Math.PI * (176 - 22 * Math.min(1, t / 0.05)) / sr;
        p2 += 2 * Math.PI * 524 / sr;
        out[i] = felt * (Math.sin(p1) * decay(t, 0, 0.055) + 0.35 * Math.sin(p2) * decay(t, 0, 0.022)
          + 0.6 * lp.run(r() * 2 - 1) * decay(t, 0, 0.006));
      }
      return out;
    },
    // Book returned: a short slide home and a gentle thud against the back of the shelf.
    thud(sr, r) {
      const len = 0.4, n = Math.round(sr * len), out = new Float32Array(n), at = 0.1;
      const grit = friction(n, sr, r, 80, 0.5);
      const bp = biquad("bp", sr).set(1100, 1.2), lp = biquad("lp", sr).set(380, 0.7), knock = biquad("bp", sr).set(720, 4);
      let p = 0;
      for (let i = 0; i < n; i++) {
        const t = i / sr;
        p += 2 * Math.PI * (60 + 38 * Math.exp(-Math.max(0, t - at) / 0.03)) / sr;
        const slide = bp.run(r() * 2 - 1) * (0.3 + grit[i]) * ramp(t, 0, 0.03) * (1 - ramp(t, 0.07, at)) * 0.35;
        const body = t < at ? 0 : Math.sin(p) * decay(t, at, 0.08) * ramp(t, at, at + 0.003);
        const dull = lp.run(r() * 2 - 1) * decay(t, at, 0.04) * 0.8;
        out[i] = slide + body + dull + knock.run(r() * 2 - 1) * decay(t, at, 0.02) * 0.5;
      }
      return out;
    },
    // Search: a card-catalogue drawer run out on its wooden runners, and the stop.
    drawer(sr, r) {
      const len = 0.8, n = Math.round(sr * len), out = new Float32Array(n), stop = 0.62;
      const grit = friction(n, sr, r, 46, 0.7);
      const bp = biquad("bp", sr), rum = biquad("lp", sr).set(240, 0.7), cards = biquad("hp", sr).set(4000, 0.7);
      const thump = biquad("lp", sr).set(500, 0.7);
      let p = 0;
      for (let i = 0; i < n; i++) {
        const t = i / sr, run = ramp(t, 0, 0.08) * (1 - ramp(t, stop - 0.06, stop));
        if (i % 64 === 0) bp.set(520 + 260 * Math.sin(Math.PI * Math.min(1, t / stop)), 1.3);
        p += 2 * Math.PI * 140 / sr;
        const wood = bp.run(r() * 2 - 1) * (0.3 + grit[i]) * run;
        const rumble = rum.run(r() * 2 - 1) * run * 0.9;
        const rustle = cards.run(r() * 2 - 1) * decay(t, stop, 0.07) * 0.25;
        const hit = (Math.sin(p) * 0.8 + thump.run(r() * 2 - 1)) * decay(t, stop, 0.035) * ramp(t, stop, stop + 0.002);
        out[i] = wood + rumble + rustle + hit;
      }
      return out;
    },
  };

  // Loudest 50 ms, in dBFS RMS.
  function loudest(buf, sr) {
    const w = Math.round(sr * 0.05);
    let best = 0;
    for (let s = 0; s + w <= buf.length; s += Math.round(w / 4)) {
      let acc = 0;
      for (let i = s; i < s + w; i++) acc += buf[i] * buf[i];
      best = Math.max(best, acc / w);
    }
    return 10 * Math.log10(best + 1e-20);
  }
  function make(name, sr, seed) {
    const buf = SOUNDS[name](sr, rng(seed));
    const g = Math.pow(10, (TARGET_DB - loudest(buf, sr)) / 20);
    for (let i = 0; i < buf.length; i++) buf[i] *= g;
    const fade = Math.round(sr * 0.01);           // no clicks at the ends
    for (let i = 0; i < fade; i++) { buf[i] *= i / fade; buf[buf.length - 1 - i] *= i / fade; }
    return buf;
  }

  if (typeof window === "undefined") {
    module.exports = { SOUNDS: Object.keys(SOUNDS), make, loudest, TARGET_DB, MUSIC_DB };
    return;
  }

  // ---- In the page ----
  let ctx = null;
  const cache = {};
  let enabled = true;
  try { enabled = localStorage.getItem("cl:sfx") !== "off"; } catch {}

  window.SFX = {
    volume: () => 1,       // the player's volume; app.js replaces this
    onPlay: null,          // app.js ducks the music for the length of each sound
    get enabled() { return enabled; },
    set enabled(on) {
      enabled = on;
      try { localStorage.setItem("cl:sfx", on ? "on" : "off"); } catch {}
    },
    play(name, delay = 0) {
      if (!enabled || !SOUNDS[name]) return;
      try {
        if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
        if (ctx.state !== "running") ctx.resume();
        const variants = cache[name] || (cache[name] = [1, 2, 3].map((seed) => {
          const data = make(name, ctx.sampleRate, seed * 7919 + name.length);
          const b = ctx.createBuffer(1, data.length, ctx.sampleRate);
          b.copyToChannel(data, 0);
          return b;
        }));
        const src = ctx.createBufferSource(), gain = ctx.createGain();
        src.buffer = variants[Math.floor(Math.random() * variants.length)];
        gain.gain.value = this.volume();
        src.connect(gain).connect(ctx.destination);
        src.start(ctx.currentTime + delay / 1000);
        if (this.onPlay) this.onPlay(delay, src.buffer.duration * 1000);
      } catch (err) {
        console.warn("[sfx]", err);
      }
    },
  };
})();
