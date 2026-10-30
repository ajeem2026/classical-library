"""Retag staged MP3s and move them into the library (other formats are converted first).

Usage: python -I retag.py <staging_dir> <library_dir> [--apply]
Without --apply it only prints the plan. Works missing from staging are skipped.
"""
import os, shutil, subprocess, sys

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
    licence, licence_url = w.get("licence", LICENCE), w.get("licence_url", LICENCE_URL)
    source = t["page"] or w.get("source", ITEM_URL)
    comment = w.get("credit") or f"Musopen Kickstarter recording, {ITEM_URL}"
    tags = ID3()
    tags.add(TCOM(encoding=3, text=w["composer"]))
    tags.add(TPE1(encoding=3, text=t["perf"]))
    tags.add(TPE2(encoding=3, text=w["perf"]))
    tags.add(TALB(encoding=3, text=album(w)))
    tags.add(TIT2(encoding=3, text=t["title"]))
    tags.add(TRCK(encoding=3, text=f"{t['n']}/{t['total']}"))
    tags.add(TCON(encoding=3, text="Classical"))
    tags.add(TCOP(encoding=3, text=f"{licence} - {t['perf'] if 'credit' in w else 'Musopen'}"))
    tags.add(WCOP(url=licence_url))
    tags.add(WOAS(url=source))
    tags.add(COMM(encoding=3, lang="eng", desc="", text=comment))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if src.endswith(".mp3"):
        shutil.move(src, dest)
    else:   # e.g. Ogg Vorbis from Commons: VBR ~245 kbps MP3, then drop the staged original
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-map", "0:a", "-c:a", "libmp3lame",
                        "-q:a", "0", dest], check=True)
        os.remove(src)
    MP3(dest).delete()  # drop all old frames, then write the fresh set
    tags.save(dest, v2_version=3)
print("APPLIED")
