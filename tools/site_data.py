"""Build web/library.json for the player from the catalogue.

Usage: python -I site_data.py [library_dir]
If library_dir is given, track durations are read from the local files.
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalogue import DREAMS, ITEM_URL, LICENCE, LICENCE_URL, NOTES, album
from library import ROOT, listing, plan, source_url

library = sys.argv[1] if len(sys.argv) > 1 else None
if library:
    from mutagen.mp3 import MP3

tracks, problems = plan(listing())

# Candidate times from tools/note_timing.py; missing ones fall back to the cue's fraction.
timings_path = os.path.join(ROOT, "data", "note_timings.json")
timings = json.load(open(timings_path)) if os.path.exists(timings_path) else {}
FALLBACK = {"climax": 0.6, "surge": 0.4, "hush": 0.5, "end": 0.9}


def curly(text):
    """Typographic quotes: an apostrophe after a letter closes, otherwise opens."""
    return re.sub(r"(?<=[\w.,!?])'", "\u2019", text).replace("'", "\u2018")


def track_notes(w, t, duration):
    """The notes to show during one track, as [{at, text, check}] in time order."""
    spec = NOTES.get(album(w))
    if not spec:
        return []
    out = []
    if t["n"] == 1:
        out.append(dict(at=4, text=curly(spec["work"]["text"]), kind="work"))
    for i, x in enumerate(spec["movements"].get(t["n"], [])):
        at, check = x["at"], True
        if at == "start":
            at, check = (40 if out else 6), False
        elif at.startswith("after:"):
            at, check = int(at[6:]), False
        else:
            found = timings.get(album(w), {}).get(str(t["n"]), {}).get(str(i))
            if found is not None:
                at = found
            elif duration:
                at = int(duration * (float(at[5:]) if at.startswith("frac:") else FALLBACK[at]))
            else:
                continue
        out.append(dict(at=at, text=curly(x["text"]), kind="movement", **({"check": True} if check else {})))
    return sorted(out, key=lambda n: n["at"])


if problems:
    sys.exit("PROBLEMS:\n  " + "\n  ".join(problems))

# Composer portraits for the dream scenes (public domain, from Wikimedia Commons).
PORTRAITS = json.load(open(os.path.join(ROOT, "web", "assets", "portraits", "credits.json")))
PORTRAIT_KEY = {"Dvořák": "dvorak"}


def dream(w):
    lines = DREAMS.get(album(w))
    if not lines:
        return None
    key = PORTRAIT_KEY.get(w["surname"], w["surname"].lower())
    c = PORTRAITS[key]
    return dict(
        portrait=f"assets/portraits/{key}.jpg",
        credit=f"Portrait: {c['artist']}{', ' + c['date'] if c['date'] else ''}. Public domain, via Wikimedia Commons.",
        lines=[dict(who=l["who"], text=curly(l["text"])) for l in lines])

works = {}
for t in tracks:
    w = t["w"]
    key = album(w) + "|" + w["composer"]
    if key not in works:
        works[key] = dict(
            id=f"w{len(works)+1}", composer=w["composer"], surname=w["surname"],
            album=album(w), catalogue=w["cat"], key=w["key"], performers=w["perf"],
            licence=LICENCE, licence_url=LICENCE_URL, reference=w["ref"],
            note=w.get("note", ""), dream=dream(w), tracks=[])
    entry = dict(n=t["n"], title=t["title"], label=t["label"] or album(w),
                 url=source_url(t["src"]), local="media/" + t["dest"].replace(os.sep, "/"))
    path = os.path.join(library, t["dest"]) if library else None
    if path and os.path.exists(path):
        entry["duration"] = round(MP3(path).info.length)
    entry["notes"] = track_notes(w, t, entry.get("duration"))
    works[key]["tracks"].append(entry)

out = dict(source=ITEM_URL, works=list(works.values()))
dest = os.path.join(ROOT, "web", "library.json")
json.dump(out, open(dest, "w"), ensure_ascii=False, indent=1)
print(f"wrote {dest}: {len(out['works'])} works, {len(tracks)} tracks")
