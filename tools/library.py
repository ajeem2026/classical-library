"""Shared track plan: maps source files to verified titles and library paths.

Every source path is relative to the "Musopen DVD/" folder inside the zip, e.g.
"Brahms - Symphony No 3/Symphony No. 3 in F Major, Op. 90 - II. Andante.mp3".
Works with their own "files" (catalogue.py) are staged under extra/ instead.
"""
import json, os, re, urllib.parse

from catalogue import ITEM, WORKS, album

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LISTING = os.path.join(ROOT, "data", "dvd_files.json")
ZIP_BASE = f"https://archive.org/download/{ITEM}/{urllib.parse.quote('Musopen DVD.zip')}/"
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
SKIP = ["(take 2)"]  # Brahms 2/III exists in two takes; keep take 1


def listing():
    """Source paths and sizes from the archive.org zip listing snapshot, plus the staging
    paths of works that name their own files (sizes unknown until fetched)."""
    out = {}
    for name, size in json.load(open(LISTING)):
        if name.startswith("Musopen DVD/"):
            out[name[len("Musopen DVD/"):]] = size
    for w in WORKS:
        for n, f in enumerate(w.get("files", []), 1):
            out[extra_src(w, n, f)] = None
    return out


def extra_src(w, n, f):
    """Where a work's own file is staged: extra/<album>/<nn>.<original extension>."""
    ext = os.path.splitext(urllib.parse.unquote(f["get"]))[1]
    return f"extra/{safe(album(w))}/{n:02d}{ext}"


def source_url(rel):
    return ZIP_BASE + urllib.parse.quote("Musopen DVD/" + rel, safe="")


def safe(s):
    s = re.sub(r":(?=\d)", "-", s)  # Hob. III:63 -> Hob. III-63
    return s.replace(":", " -").replace("/", "-")


def order_key(w, name):
    if w["work"] == "Goldberg Variations":
        if name.endswith("- Aria.mp3"):
            return 0
        if "Aria Da Capo" in name:
            return 99
        return int(re.search(r"Variation (\d+)", name).group(1))
    m = re.match(r"(Adagio Allegro 1st|2nd|3rd|4th) Mov", name)
    if m:
        return {"Adagio Allegro 1st": 1, "2nd": 2, "3rd": 3, "4th": 4}[m.group(1)]
    if len(w["mov"]) == 1:
        return 1
    return ROMAN.index(re.search(r" - (I{1,3}|IV|V)\. ", name).group(1))


def plan(sources):
    """Return (tracks, problems) for an iterable of source paths."""
    sources = [s for s in sources if (s.endswith(".mp3") or s.startswith("extra/"))
               and not os.path.basename(s).startswith("._") and not any(k in s for k in SKIP)]
    tracks, problems = [], []
    for w in WORKS:
        if "files" in w:
            files = [s for n, f in enumerate(w["files"], 1) if (s := extra_src(w, n, f)) in sources]
        else:
            files = [s for s in sources if os.path.dirname(s) == w["src"]]
            if "match" in w:
                files = [s for s in files if w["match"] in os.path.basename(s)]
            files.sort(key=lambda s: order_key(w, os.path.basename(s)))
        if len(files) != len(w["mov"]):
            problems.append(f"{album(w)}: {len(files)} files for {len(w['mov'])} movements")
            continue
        alb = album(w)
        for n, (src, mov) in enumerate(zip(files, w["mov"]), 1):
            if mov is None:
                label, fname = None, f"{n:02d} {safe(w['work'])}.mp3"
            elif w.get("numbered", True):
                label, fname = f"{ROMAN[n-1]}. {mov}", f"{n:02d} {safe(mov)}.mp3"
            else:
                label, fname = mov, f"{n:02d} {safe(mov)}.mp3"
            own = w["files"][n - 1] if "files" in w else {}
            tracks.append(dict(w=w, n=n, total=len(w["mov"]), src=src, label=label,
                               title=f"{alb}: {label}" if label else alb,
                               dest=os.path.join(w["surname"], safe(alb), fname),
                               url=own.get("url") or source_url(src), get=own.get("get") or source_url(src),
                               perf=own.get("perf", w["perf"]), page=own.get("page")))
    return tracks, problems
