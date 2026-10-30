// Measure the library's sound effects against their ceiling: 24 dB under the music.
// Usage: node tools/sfx_check.js [wav_dir]   (with a directory, also writes each sound as a WAV)
const fs = require("fs"), path = require("path");
const { SOUNDS, make, loudest, MUSIC_DB } = require("../web/sfx.js");

const SR = 48000, CEILING = MUSIC_DB - 24;
const dir = process.argv[2];
let ok = true;
for (const name of SOUNDS) {
  for (const seed of [1, 2, 3].map((s) => s * 7919 + name.length)) {
    const buf = make(name, SR, seed);
    const db = loudest(buf, SR);
    const peak = 20 * Math.log10(buf.reduce((m, x) => Math.max(m, Math.abs(x)), 0));
    const pass = db <= CEILING;
    ok = ok && pass;
    console.log(`${name.padEnd(7)} seed ${String(seed).padStart(5)}  ${(buf.length / SR).toFixed(2)} s  ` +
      `loudest 50 ms ${db.toFixed(1)} dBFS (${(db - MUSIC_DB).toFixed(1)} dB vs music)  peak ${peak.toFixed(1)} dBFS  ${pass ? "ok" : "TOO LOUD"}`);
    if (dir && seed === 7919 + name.length) {
      // 16-bit WAV, raised 40 dB so it can be heard on its own.
      const pcm = Buffer.alloc(44 + buf.length * 2);
      pcm.write("RIFF", 0); pcm.writeUInt32LE(36 + buf.length * 2, 4); pcm.write("WAVEfmt ", 8);
      pcm.writeUInt32LE(16, 16); pcm.writeUInt16LE(1, 20); pcm.writeUInt16LE(1, 22);
      pcm.writeUInt32LE(SR, 24); pcm.writeUInt32LE(SR * 2, 28); pcm.writeUInt16LE(2, 32); pcm.writeUInt16LE(16, 34);
      pcm.write("data", 36); pcm.writeUInt32LE(buf.length * 2, 40);
      buf.forEach((x, i) => pcm.writeInt16LE(Math.max(-32767, Math.min(32767, Math.round(x * 100 * 32767))), 44 + i * 2));
      fs.writeFileSync(path.join(dir, name + ".wav"), pcm);
    }
  }
}
console.log(ok ? `all under ${CEILING.toFixed(1)} dBFS` : "some sounds are too loud");
process.exit(ok ? 0 : 1);
