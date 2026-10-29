"""Download every planned track from the Musopen Kickstarter zip on archive.org.

Usage: python -I download.py <staging_dir>
Already-downloaded files are skipped. Stops if free disk space would drop below 1 GB.
"""
import os, shutil, sys, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from library import listing, plan, source_url

MIN_FREE = 1_000_000_000

staging = sys.argv[1]
os.makedirs(staging, exist_ok=True)
sizes = listing()
tracks, problems = plan(sizes)
if problems:
    sys.exit("PROBLEMS:\n  " + "\n  ".join(problems))

todo = [t for t in tracks if not (os.path.exists(p := os.path.join(staging, t["src"]))
                                  and os.path.getsize(p) == sizes[t["src"]])]
print(f"{len(tracks)} tracks planned, {len(todo)} to download "
      f"({sum(sizes[t['src']] for t in todo)/1e9:.2f} GB)")
for t in todo:
    rel, size = t["src"], sizes[t["src"]]
    dest = os.path.join(staging, rel)
    if shutil.disk_usage(staging).free - size < MIN_FREE:
        sys.exit(f"STOP: free space would drop below 1 GB before {rel}")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    tmp = dest + ".part"
    with urllib.request.urlopen(source_url(rel), timeout=120) as r, open(tmp, "wb") as f:
        shutil.copyfileobj(r, f, 1 << 20)
    if os.path.getsize(tmp) != size:
        sys.exit(f"SIZE MISMATCH {rel}: {os.path.getsize(tmp)} != {size}")
    os.replace(tmp, dest)
    print("ok", rel, flush=True)
print("DONE")
