"""Build web/library.json for the player from the catalogue.

Usage: python -I site_data.py [library_dir]
If library_dir is given, track durations are read from the local files.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalogue import ITEM_URL, LICENCE, LICENCE_URL, album
from library import ROOT, listing, plan, source_url

library = sys.argv[1] if len(sys.argv) > 1 else None
if library:
    from mutagen.mp3 import MP3

tracks, problems = plan(listing())
if problems:
    sys.exit("PROBLEMS:\n  " + "\n  ".join(problems))

works = {}
for t in tracks:
    w = t["w"]
    key = album(w) + "|" + w["composer"]
    if key not in works:
        works[key] = dict(
            id=f"w{len(works)+1}", composer=w["composer"], surname=w["surname"],
            album=album(w), catalogue=w["cat"], key=w["key"], performers=w["perf"],
            licence=LICENCE, licence_url=LICENCE_URL, reference=w["ref"],
            note=w.get("note", ""), tracks=[])
    entry = dict(n=t["n"], title=t["title"], label=t["label"] or album(w),
                 url=source_url(t["src"]), local="media/" + t["dest"].replace(os.sep, "/"))
    path = os.path.join(library, t["dest"]) if library else None
    if path and os.path.exists(path):
        entry["duration"] = round(MP3(path).info.length)
    works[key]["tracks"].append(entry)

out = dict(source=ITEM_URL, works=list(works.values()))
dest = os.path.join(ROOT, "web", "library.json")
json.dump(out, open(dest, "w"), ensure_ascii=False, indent=1)
print(f"wrote {dest}: {len(out['works'])} works, {len(tracks)} tracks")
