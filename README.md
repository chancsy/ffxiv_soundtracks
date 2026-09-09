# FFXIV Soundtracks

**Live: https://chancsy.github.io/ffxiv_soundtracks/**

A filterable table of every track on the FINAL FANTASY XIV soundtrack albums that are on
Spotify, annotated with the duty, area, or moment each track scores. Filter by content-type
chip (Trial, Raid, Alliance raid, Field raid, Ultimate, …) to browse endgame music specifically.

## Structure

- `index.html` — the generated page. Never hand-edit; regenerate with `python3 build.py`.
- `build.py` — reads every `data/*.json` and writes `index.html`.
- `data/NN_album.py` — one script per album, a plain list of tuples that writes the matching
  `data/NN_album.json`. Run `python3 data/NN_album.py` after editing one.
- `HANDOVER.md` — the full project handover doc: data schema, research method, conventions,
  and the open TODO list. Read this before making changes.

## Rebuilding after an edit

```bash
python3 data/NN_album.py   # regenerate the one JSON you changed
python3 build.py           # regenerate index.html from all data/*.json
```
