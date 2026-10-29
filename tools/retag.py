"""Retag staged Musopen MP3s and move them into the library.

Usage: python -I retag.py <staging_dir> <library_dir> [--apply]
Without --apply it only prints the plan. Works missing from staging are skipped.
"""
import os, shutil, sys

from mutagen.id3 import ID3, TALB, TCOM, TCON, TCOP, TIT2, TPE1, TPE2, TRCK, WCOP, WOAS, COMM
from mutagen.mp3 import MP3

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalogue import ITEM_URL, LICENCE, LICENCE_URL, album
from library import plan

staging, library = sys.argv[1], sys.argv[2]
apply = "--apply" in sys.argv

staged = [os.path.relpath(os.path.join(d, f), staging)
          for d, _, fs in os.walk(staging) for f in fs]
tracks, missing = plan(staged)
for t in tracks:
    print(f"{t['n']:>2}/{t['total']:<2} {t['title']}\n      {os.path.basename(t['src'])}")
print(f"\n{len(tracks)} files planned")
if missing:
    print("Not in staging (skipped):", *missing, sep="\n  ")
if not apply:
    sys.exit(0)

for t in tracks:
    w, src, dest = t["w"], os.path.join(staging, t["src"]), os.path.join(library, t["dest"])
    tags = ID3()
    tags.add(TCOM(encoding=3, text=w["composer"]))
    tags.add(TPE1(encoding=3, text=w["perf"]))
    tags.add(TPE2(encoding=3, text=w["perf"]))
    tags.add(TALB(encoding=3, text=album(w)))
    tags.add(TIT2(encoding=3, text=t["title"]))
    tags.add(TRCK(encoding=3, text=f"{t['n']}/{t['total']}"))
    tags.add(TCON(encoding=3, text="Classical"))
    tags.add(TCOP(encoding=3, text=f"{LICENCE} - Musopen"))
    tags.add(WCOP(url=LICENCE_URL))
    tags.add(WOAS(url=ITEM_URL))
    tags.add(COMM(encoding=3, lang="eng", desc="", text=f"Musopen Kickstarter recording, {ITEM_URL}"))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.move(src, dest)
    MP3(dest).delete()  # drop all old frames, then write the fresh set
    tags.save(dest, v2_version=3)
print("APPLIED")
