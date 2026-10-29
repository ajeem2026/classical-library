"""Build web/library.json for the player from the catalogue.

Usage: python -I site_data.py [library_dir]
If library_dir is given, track durations are read from the local files.
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalogue import ITEM_URL, LICENCE, LICENCE_URL, MKEYS, NOTES, album
from dreams import DREAMS
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
    """Portrait and credit for the work's dream scenes; the dialogue goes to web/dreams.json."""
    if album(w) not in DREAMS:
        return None
    key = PORTRAIT_KEY.get(w["surname"], w["surname"].lower())
    c = PORTRAITS[key]
    return dict(
        portrait=f"assets/portraits/{key}.jpg",
        credit=f"Portrait: {c['artist']}{', ' + c['date'] if c['date'] else ''}. Public domain, via Wikimedia Commons.")


def dream_material(a):
    """The work's dream material (tools/dreams.py), for the player to assemble from."""
    line = lambda l: dict(who=l["who"], text=curly(l["text"]))
    d = DREAMS[a]
    return dict(open=[line(l) for l in d["open"]], close=[line(l) for l in d["close"]],
                qa=[dict(ask=curly(q["ask"]), answers=[line(x) for x in q["answers"]]) for q in d["qa"]])


TEMPO_WORDS = ("Allegro Allegretto Adagio Andante Andantino Lento Largo Moderato Presto Prestissimo "
               "Vivace Un Poco Più Meno Con Al Alla Molto Tempo").split()


def tempi(heading):
    """Tempo markings in a movement heading, in order: 'Scherzo: Allegro – Trio: Più lento' -> both."""
    out = []
    for seg in (heading or "").split(" – "):
        seg = seg.split(": ")[-1].split(". ")[-1].strip()
        if seg.split(" ")[0] in TEMPO_WORDS:
            out.append(seg)
    return out


# Tempo buckets for the listening page, slowest first. Each marking's leading word decides.
PACE = ["Largo", "Adagio", "Andante", "Moderato", "Allegro", "Presto"]
PACE_WORDS = {"Largo": 0, "Lento": 0, "Adagio": 1, "Sostenuto": 1, "Andante": 2, "Andantino": 2,
              "Moto": 2, "Moderato": 3, "Allegretto": 3, "Allegro": 4, "Vivace": 4, "Giga": 4,
              "Presto": 5, "Prestissimo": 5}


def pace(marking):
    """'Un poco sostenuto' -> 1 (Adagio); 'Allegro con brio' -> 4; unknown -> None."""
    for word in marking.replace(",", " ").split():
        if word.capitalize() in PACE_WORDS:
            return PACE_WORDS[word.capitalize()]
    return None


# Loudness: each 10-second stretch marked q(uiet), m(iddle) or l(oud) against the whole
# library's thirds, from data/loudness.json (tools/loudness.py).
loud_path = os.path.join(ROOT, "data", "loudness.json")
LOUD = json.load(open(loud_path)) if os.path.exists(loud_path) else {}
levels = sorted(x for w in LOUD.values() for t in w.values() for x in t)
QUIET_DB, LOUD_DB = (levels[len(levels) // 3], levels[2 * len(levels) // 3]) if levels else (0, 0)


def marks(profile):
    return "".join("q" if x < QUIET_DB else "l" if x >= LOUD_DB else "m" for x in profile)


def movement_key(w, n, count):
    """The movement's key, when known: listed in MKEYS, or the home key for outer movements and variation sets."""
    known = MKEYS.get(album(w), {})
    if n in known:
        return known[n]
    if w["key"] and (n in (1, count) or count > 6):
        return w["key"]
    return ""


works = {}
for t in tracks:
    w = t["w"]
    key = album(w) + "|" + w["composer"]
    if key not in works:
        works[key] = dict(
            id=f"w{len(works)+1}", composer=w["composer"], surname=w["surname"],
            album=album(w), work=w["work"], catalogue=w["cat"], key=w["key"], performers=w["perf"],
            licence=LICENCE, licence_url=LICENCE_URL, reference=w["ref"],
            note=w.get("note", ""), dream=dream(w), tracks=[])
    entry = dict(n=t["n"], title=t["title"], label=t["label"] or album(w),
                 url=source_url(t["src"]), local="media/" + t["dest"].replace(os.sep, "/"))
    path = os.path.join(library, t["dest"]) if library else None
    if path and os.path.exists(path):
        entry["duration"] = round(MP3(path).info.length)
    entry["notes"] = track_notes(w, t, entry.get("duration"))
    count = len(w["mov"])
    entry["tempo"] = tempi(t["title"].split(": ", 1)[1] if ": " in t["title"] else "")
    entry["key"] = movement_key(w, t["n"], count)
    entry["pace"] = [pace(x) for x in entry["tempo"]]
    profile = LOUD.get(album(w), {}).get(str(t["n"]))
    if profile:
        entry["loud"] = marks(profile)
    works[key]["tracks"].append(entry)

out = dict(source=ITEM_URL, pace=PACE, loud_step=10,
           loud_db=dict(quiet_below=QUIET_DB, loud_from=LOUD_DB), works=list(works.values()))
dest = os.path.join(ROOT, "web", "library.json")
json.dump(out, open(dest, "w"), ensure_ascii=False, indent=1)
print(f"wrote {dest}: {len(out['works'])} works, {len(tracks)} tracks")

# Dream dialogue, loaded only when a dream begins.
material = {w["id"]: dream_material(w["album"]) for w in out["works"] if w["dream"]}
dest = os.path.join(ROOT, "web", "dreams.json")
json.dump(material, open(dest, "w"), ensure_ascii=False, indent=1)
print(f"wrote {dest}: dream material for {len(material)} works")
