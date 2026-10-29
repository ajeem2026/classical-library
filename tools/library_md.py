"""Write LIBRARY.md for the Musopen starter set. Usage: python -I library_md.py <output_dir>"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalogue import ITEM, ITEM_URL, LICENCE, LICENCE_URL, WORKS, album
from library import ZIP_BASE

out = [
    "# Classical Library",
    "",
    "Starter set built from Musopen's public-domain Kickstarter recordings on the Internet Archive.",
    "",
    f"- **Source item:** [{ITEM}]({ITEM_URL}) (uploaded by Musopen, `aaron@musopen.org`, 2012)",
    f"- **Licence:** [{LICENCE} Public Domain Dedication]({LICENCE_URL}) on the item's `licenseurl`."
    " No attribution is legally required; it is given here as a courtesy.",
    "- **Recordings:** Musopen / Aaron Dunn, Musopen Kickstarter project 2012.",
    "- **Metadata:** keys, catalogue numbers and movement headings checked against Wikipedia or IMSLP (reference column).",
    "",
    "| Composer | Work | Catalogue | Performers | Movements | Licence | Source | Reference |",
    "|---|---|---|---|---|---|---|---|",
]
for w in WORKS:
    work = w["work"] + (f" in {w['key']}" if w["key"] else "")
    note = f" ({w['note']})" if w.get("note") else ""
    out.append(f"| {w['composer']} | {work}{note} | {w['cat'] or '—'} | {w['perf']} | "
               f"{len(w['mov'])} | [{LICENCE}]({LICENCE_URL}) | [item]({ITEM_URL}) · "
               f"[zip listing]({ZIP_BASE}), folder `{w['src'].strip()}` | [ref]({w['ref']}) |")

out += [
    "",
    f"**{len(WORKS)} works, {sum(len(w['mov']) for w in WORKS)} tracks.** All files are 320 kbps MP3.",
    "",
    "## Notes on the source",
    "",
    "- The source files' names and tags contain errors that were corrected here: Brahms 1 is in C *minor*;"
    " Schubert D. 959 is in A *major*; the D. 850 rondo is movement IV, not V; the Mendelssohn Op. 80 finale is"
    " *Finale: Allegro molto*, not \"Fuga\"; Haydn \"Op. 645, H 363\" is Op. 64 No. 5, Hob. III:63; the four"
    " unlabelled K. 465 files were identified as Mozart's String Quartet No. 19.",
    "- The Borodin quartets are tagged \"Czech National Symphony Orchestra\" at the source. Wikipedia credits these"
    " recordings to the Musopen String Quartet, which is used here.",
    "- The Brahms 2 third movement exists in two takes at the source. Take 1 is used.",
    "- Goldberg Variations: the 32 tracks (Aria, 30 variations, Aria da capo) use Bach's own headings instead of"
    " Roman-numeral movements.",
    "",
    "## Skipped",
    "",
    "| What | Why |",
    "|---|---|",
    "| Single-work uploads in the `netfocusuniversal` collection (e.g. `SymphonyNo.3InFMajorOp.90`, `SymphonyNo.4InEMinorOp.98`, `StringQuartetInDOp.645H363Lark`) | No `licenseurl` or rights metadata. They duplicate the recordings above anyway. |",
    "| `musopen-*-compressed` session items (2–48 GB each) | No `licenseurl` on the item. They are raw session archives, not finished tracks. |",
    "| `musopen-chopin` (Complete Chopin Collection, CC0) | Licence qualifies, but 102 of 104 files have no performer credit, so the Artist tag can't be filled accurately. |",
    "| `Musopen-Libre` and other search hits | CC BY-SA, BY-NC, BY-ND or NC-ND licences, which are outside CC0/PDM/CC BY. Most are not Musopen recordings. |",
    "| `SymphonyNo.5`, `SymphonyNo.5InCMinorOp.67I.AllegroConBrio` (Public Domain Mark) | Licence qualifies, but these are single files from third-party uploaders with no performer credit, and not a complete work. |",
    "| Rest of the DVD (CC0): overtures, Mendelssohn Symphonies 3 & 4, Mozart Symphony 40, Grieg, Smetana, Borodin *Steppes* | Outside the starter scope. They can be added later from the same item. |",
    "",
    "**Not available from Musopen on archive.org:** Dvořák symphonies, anything by Sibelius, and Beethoven symphonies other than No. 3.",
    "",
]
open(os.path.join(sys.argv[1], "LIBRARY.md"), "w").write("\n".join(out))
print("\n".join(out))
