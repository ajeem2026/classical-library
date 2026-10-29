# Classical Library

A personal classical music library built from [Musopen](https://musopen.org)'s public-domain (CC0)
recordings on the Internet Archive, plus a web player for it.

- `tools/` – Python scripts that download, retag (mutagen) and file the recordings
- `web/` – the player: plain HTML/CSS/JS, no build step
- [LIBRARY.md](LIBRARY.md) – every work, its performers, licence and source

## How it fits together

```
tools/catalogue.py  ──►  make download  ──►  staging/  ──►  make tag  ──►  ~/Music/Classical
   (verified works)                                                          │
        │                                                                    ▼
        └──────────────────────────►  make docs  ──►  LIBRARY.md + web/library.json
                                                                 │
                                       make serve (local files) ◄┤
                                       make publish ─► gh-pages branch ─► GitHub Pages (streams from archive.org)
```

`tools/catalogue.py` is the single source of truth: work titles, keys, catalogue numbers,
performers and movement headings. Everything else is generated from it.

## Common tasks

```sh
make setup      # once: create .venv with mutagen
make serve      # player at http://localhost:8000, playing ~/Music/Classical
make publish    # regenerate data, commit, push, redeploy web/ to the gh-pages branch
```

**Add a work** from the Musopen DVD: add an entry to `WORKS` in `tools/catalogue.py`
(check the key, catalogue number and movements against Wikipedia or IMSLP), then:

```sh
make download && make plan   # fetch it and check the titles
make tag docs                # retag, file it, refresh LIBRARY.md and the player
make publish
```

## Personalising the player

- `web/config.js` – site title, tagline, audio source, continuous play, seek step
- `web/style.css` – colours and fonts are the variables at the top (light and dark)
- `web/app.js` – behaviour; `web/index.html` – layout

Favourites, the last track and position, volume and the composer filter are remembered per browser.

## Audio sources

The live site streams from archive.org, which unpacks each track from Musopen's zip on the fly.
Playback works, but seeking far ahead may wait for the track to download. `make serve` plays your
local copies with full seeking.

## Licence

Recordings: [CC0 1.0](http://creativecommons.org/publicdomain/zero/1.0/), Musopen Kickstarter project 2012,
via [archive.org/details/MusopenKickstarterRecordings](https://archive.org/details/MusopenKickstarterRecordings).
