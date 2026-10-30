"""Download every planned track: from the Musopen Kickstarter zip on archive.org, or from a
work's own files (catalogue.py).

Usage: python -I download.py <staging_dir> [library_dir]
Tracks already staged, or already in the library, are skipped. Stops if free disk space would drop below 1 GB.
"""
import os, shutil, sys, time, urllib.error, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from library import listing, plan

MIN_FREE = 1_000_000_000

staging = sys.argv[1]
library = sys.argv[2] if len(sys.argv) > 2 else None
os.makedirs(staging, exist_ok=True)
sizes = listing()
tracks, problems = plan(sizes)
if problems:
    sys.exit("PROBLEMS:\n  " + "\n  ".join(problems))

# Files outside the zip have no listed size: one already staged counts as done.
todo = [t for t in tracks if not (os.path.exists(p := os.path.join(staging, t["src"]))
                                  and sizes[t["src"]] in (None, os.path.getsize(p)))
        and not (library and os.path.exists(os.path.join(library, t["dest"])))]
print(f"{len(tracks)} tracks planned, {len(todo)} to download "
      f"({sum(sizes[t['src']] or 0 for t in todo)/1e9:.2f} GB listed)")
for t in todo:
    rel, size = t["src"], sizes[t["src"]]
    dest = os.path.join(staging, rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    tmp = dest + ".part"
    req = urllib.request.Request(t["get"], headers={"User-Agent": "classical-library/1.0 (personal use)"})
    for wait in (0, 30, 60, 120, None):   # Wikimedia answers 429 to quick runs: back off and retry
        try:
            r = urllib.request.urlopen(req, timeout=120)
            break
        except urllib.error.HTTPError as e:
            if e.code != 429 or wait is None:
                raise
            print(f"rate-limited, waiting {wait or 15} s", flush=True)
            time.sleep(wait or 15)
    with r, open(tmp, "wb") as f:
        size = size or int(r.headers.get("Content-Length") or 0)
        if shutil.disk_usage(staging).free - size < MIN_FREE:
            sys.exit(f"STOP: free space would drop below 1 GB before {rel}")
        shutil.copyfileobj(r, f, 1 << 20)
    if size and os.path.getsize(tmp) != size:
        sys.exit(f"SIZE MISMATCH {rel}: {os.path.getsize(tmp)} != {size}")
    os.replace(tmp, dest)
    print("ok", rel, flush=True)
    time.sleep(3)
print("DONE")
