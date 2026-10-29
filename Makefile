PY      ?= .venv/bin/python
LIBRARY ?= $(HOME)/Music/Classical
STAGING ?= staging
PORT    ?= 8000

.PHONY: setup plan download tag docs timings loudness add serve publish

setup:            ## create the venv with mutagen
	python3 -m venv .venv
	.venv/bin/pip install -q mutagen

plan:             ## dry run: show how staged files would be titled
	$(PY) -I tools/retag.py $(STAGING) $(LIBRARY)

download:         ## fetch every catalogue track not yet staged
	$(PY) -I tools/download.py $(STAGING)

tag:              ## retag staged files and move them into the library
	$(PY) -I tools/retag.py $(STAGING) $(LIBRARY) --apply

docs:             ## regenerate LIBRARY.md and the player's library.json
	$(PY) -I tools/library_md.py $(LIBRARY) > /dev/null
	$(PY) -I tools/library_md.py . > /dev/null
	$(PY) -I tools/site_data.py $(LIBRARY)
	$(PY) -I tools/notes_review.py

timings:          ## re-place the history notes' cues from your local recordings
	$(PY) -I tools/note_timing.py $(LIBRARY)

loudness:         ## measure each recording's loudness, for the listening page (new tracks only)
	$(PY) -I tools/loudness.py $(LIBRARY)

add: download tag loudness docs   ## after editing tools/catalogue.py

serve:            ## run the player locally against your own files
	$(PY) -I tools/serve.py web $(LIBRARY) $(PORT)

publish: docs     ## commit, push, and redeploy the site (web/ -> gh-pages branch)
	git add -A
	git commit -m "Update library" || true
	git push
	git push origin `git subtree split --prefix web HEAD`:refs/heads/gh-pages --force
