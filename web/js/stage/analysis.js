// Live bands from the playing audio: bass (pulse), mids (flow speed), highs
// (sparkle) and overall level. Web Audio is connected only inside a user
// gesture, because a suspended AudioContext would silence the element.
// Without CORS or Web Audio, a gentle synthetic pulse stands in.

export function createAnalysis(audio) {
  const bands = { bass: 0, mid: 0, high: 0, level: 0, live: false };
  let ctx = null, analyser = null, freq = null, wave = null, binHz = 0;

  function connect() {
    if (ctx || audio.crossOrigin !== "anonymous") return;
    try {
      ctx = new (window.AudioContext || window.webkitAudioContext)();
      const source = ctx.createMediaElementSource(audio);
      analyser = ctx.createAnalyser();
      analyser.fftSize = 2048;
      analyser.smoothingTimeConstant = 0.55;
      analyser.minDecibels = -90;
      analyser.maxDecibels = -20;
      source.connect(analyser);
      analyser.connect(ctx.destination);
      freq = new Uint8Array(analyser.frequencyBinCount);
      wave = new Float32Array(analyser.fftSize);
      binHz = ctx.sampleRate / analyser.fftSize;
      window.__audioGraph = true; // app.js must not drop CORS once the graph exists
      bands.live = true;
    } catch (err) {
      console.warn("[stage] no Web Audio analysis:", err);
      ctx = null;
    }
  }
  const wake = () => { connect(); if (ctx && ctx.state !== "running") ctx.resume(); };
  for (const type of ["pointerdown", "keydown"]) window.addEventListener(type, wake, { capture: true });

  const avg = (lo, hi) => {
    const a = Math.max(1, Math.floor(lo / binHz)), b = Math.min(freq.length - 1, Math.ceil(hi / binHz));
    let s = 0;
    for (let i = a; i <= b; i++) s += freq[i];
    return s / (b - a + 1) / 255;
  };
  const ease = (cur, target, dt, attack, release) =>
    cur + (target - cur) * (1 - Math.exp(-dt / (target > cur ? attack : release)));

  let t = 0;
  bands.update = (dt) => {
    t += dt;
    let bass, mid, high, level;
    if (analyser && ctx.state === "running" && !audio.paused) {
      analyser.getByteFrequencyData(freq);
      analyser.getFloatTimeDomainData(wave);
      let sum = 0;
      for (let i = 0; i < wave.length; i++) sum += wave[i] * wave[i];
      const db = 20 * Math.log10(Math.sqrt(sum / wave.length) + 1e-6);
      level = Math.min(1, Math.max(0, (db + 48) / 36));     // -48 dBFS quiet .. -12 dBFS loud
      bass = Math.min(1, Math.max(0, (avg(30, 160) - 0.3) / 0.5));
      mid = Math.min(1, Math.max(0, (avg(250, 2000) - 0.25) / 0.5));
      high = Math.min(1, Math.max(0, (avg(3000, 10000) - 0.04) / 0.3));
    } else if (!audio.paused) {
      // Synthetic stand-in: a slow breath, enough to show the music is moving.
      level = 0.35 + 0.1 * Math.sin(t * 0.7);
      bass = 0.3 + 0.2 * Math.max(0, Math.sin(t * 2.1));
      mid = 0.35; high = 0.15 + 0.1 * Math.sin(t * 5.3);
    } else {
      level = bass = mid = high = 0;
    }
    bands.bass = ease(bands.bass, bass, dt, 0.05, 0.35);
    bands.mid = ease(bands.mid, mid, dt, 0.3, 0.8);
    bands.high = ease(bands.high, high, dt, 0.03, 0.2);
    bands.level = ease(bands.level, level, dt, 0.25, 1.6);
  };
  return bands;
}
