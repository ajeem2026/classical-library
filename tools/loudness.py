"""Loudness profiles of every recording, for the listening page's quiet/loud trends.

Usage: python -I loudness.py <library_dir>
Writes data/loudness.json: per work and track, the mean loudness in dB of each
10-second stretch. site_data.py turns these into quiet / middle / loud marks.
"""
import json, math, os, subprocess, sys

RATE = 4000  # Hz; plenty for loudness


def loudness(path):
    """Loudness in dB per second of audio."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(RATE), "-f", "s16le", "-"],
        check=True, capture_output=True).stdout
    n = len(raw) // 2
    samples = memoryview(raw).cast("h")
    out = []
    for s in range(0, n - RATE + 1, RATE):
        acc = 0
        for i in range(s, s + RATE, 4):  # every 4th sample is enough for RMS
            v = samples[i]
            acc += v * v
        rms = math.sqrt(acc / (RATE / 4)) / 32768
        out.append(20 * math.log10(rms + 1e-6))
    return out



STEP = 10  # seconds per stretch


def profile(curve):
    """Mean dB of each STEP-second stretch, rounded."""
    return [round(sum(curve[i:i + STEP]) / len(curve[i:i + STEP]), 1) for i in range(0, len(curve), STEP)]


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from catalogue import album
    from library import ROOT, listing, plan

    library = sys.argv[1]
    tracks, problems = plan(listing())
    dest = os.path.join(ROOT, "data", "loudness.json")
    out = json.load(open(dest)) if os.path.exists(dest) else {}
    for t in tracks:
        key, n = album(t["w"]), str(t["n"])
        if n in out.get(key, {}):
            continue
        path = os.path.join(library, t["dest"])
        if not os.path.exists(path):
            print("missing", path)
            continue
        out.setdefault(key, {})[n] = profile(loudness(path))
        json.dump(out, open(dest, "w"), ensure_ascii=False)   # keep progress if interrupted
        print(f"{key} / {n}: {len(out[key][n])} stretches")
    print("wrote", dest)
