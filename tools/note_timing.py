"""Find candidate times for the history notes from the recordings themselves.

Usage: python -I note_timing.py <library_dir>
Decodes each track with ffmpeg into a one-second loudness curve, resolves each
note's cue (see NOTES in catalogue.py) and writes data/note_timings.json. Every
time resolved from a cue or fraction is a candidate, marked "check by ear".
"""
import json, math, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalogue import NOTES, WORKS, album
from library import ROOT, listing, plan

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


def window(curve, size):
    """Mean over a centred window of `size` seconds."""
    h, out = size // 2, []
    for i in range(len(curve)):
        part = curve[max(0, i - h):i + h + 1]
        out.append(sum(part) / len(part))
    return out


def resolve(cue, curve):
    d = len(curve)
    lo, hi = int(d * 0.1), int(d * 0.9)
    if cue == "climax":
        w = window(curve, 10)
        return max(range(lo, hi), key=lambda i: w[i]) - 5
    if cue == "hush":
        w = window(curve, 10)
        return min(range(int(d * 0.15), int(d * 0.85)), key=lambda i: w[i]) - 5
    if cue == "surge":
        def rise(i):
            before = curve[max(0, i - 8):i]
            after = curve[i:i + 4]
            return (sum(after) / len(after)) - (sum(before) / len(before)) if before and after else -99
        return max(range(max(8, int(d * 0.05)), hi), key=rise) - 2
    if cue == "end":
        return max(0, d - 60) if d > 150 else int(d * 0.8)
    if cue.startswith("frac:"):
        return int(d * float(cue[5:]))
    raise ValueError(cue)


library = sys.argv[1]
tracks, problems = plan(listing())
by_work = {}
for t in tracks:
    by_work.setdefault(album(t["w"]), {})[t["n"]] = t

out = {}
for key, spec in NOTES.items():
    for n, notes in spec["movements"].items():
        cues = [x["at"] for x in notes if x["at"] not in ("start",) and not x["at"].startswith("after:")]
        if not cues:
            continue
        path = os.path.join(library, by_work[key][n]["dest"])
        if not os.path.exists(path):
            print("missing", path)
            continue
        curve = loudness(path)
        times = {}
        for i, x in enumerate(notes):
            if x["at"] in cues:
                times[str(i)] = max(0, resolve(x["at"], curve))
        out.setdefault(key, {})[str(n)] = times
        print(f"{key} / {n}: " + ", ".join(f"{notes[int(i)]['at']}→{s // 60}:{s % 60:02d}" for i, s in times.items()))

dest = os.path.join(ROOT, "data", "note_timings.json")
json.dump(out, open(dest, "w"), ensure_ascii=False, indent=1)
print("wrote", dest)
