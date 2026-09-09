# FFXIV Soundtracks

**Live: https://chancsy.github.io/ffxiv_soundtracks/**

A filterable table of every track on the FINAL FANTASY XIV soundtrack albums that are on
Spotify, annotated with the duty, area, or moment each track scores. Filter by content-type
chip (Trial, Raid, Alliance raid, Field raid, Ultimate, …) to browse endgame music specifically
— there's no separate "playlist" view; see [Design notes](#design-notes-read-before-changing-behavior) for why one isn't needed.

This is the reference doc for working on the project — schema, conventions, research method,
and current status. Read it before adding or editing an album.

## Structure

```
├── build.py                 # generator: reads data/*.json → writes index.html
├── data/
│   ├── NN_album.py          # source: a list of tuples → writes the matching .json
│   └── NN_album.json        # generated (or hand-maintained — see note below)
├── index.html                # generated page; never hand-edit, regenerate with build.py
└── HANDOVER.md               # open TODOs and current blockers only — this file has everything else
```

Every `.py`/`.json` pair *should* round-trip byte-for-byte (`python3 data/NN_album.py`
regenerates the `.json` identically) — verify this before trusting a `.py` file you haven't
touched recently. `11_growing_light.json` has no `.py` source; it's hand-maintained directly —
edit the JSON in place, and if you ever do write a generator for it, base it on the current
JSON first, not the other way around.

### Rebuilding after an edit

```bash
python3 data/NN_album.py   # regenerate the one JSON you changed
python3 build.py           # regenerate index.html from all data/*.json
```

### Repository

Public repo: https://github.com/chancsy/ffxiv_soundtracks (`main` branch, GitHub Pages serves
`index.html` from it at the live link above). Pushing needs a fine-grained GitHub Personal
Access Token (Contents: read/write, scoped to just this repo) — none is stored between
sessions, so it has to be supplied fresh each time a push is needed.

## Roadmap

Album `order` numbers are fixed — leave gaps as shown (order 9→11 skips a reserved-but-unused
10; don't renumber to close it).

| order | album | covers | status |
|---|---|---|---|
| 1 | Before Meteor | 1.0 – 1.23 | done |
| 2 | A Realm Reborn | 2.0 – 2.1 | done |
| 3 | Before the Fall | 2.2 – 2.55 | done |
| 4 | Heavensward | 3.0 – 3.1 | done |
| 5 | The Far Edge of Fate | 3.2 – 3.56 | done |
| 6 | Stormblood | 4.0 – 4.3 | done |
| 7 | Shadowbringers | 4.4 – 4.5 **and** 5.0 (one album) | done |
| 8 | Death Unto Dawn | 5.1 – 5.5 | done |
| 9 | Endwalker | 6.0 | done |
| 11 | Growing Light | 6.1 – 6.58 | done |
| 12 | Dawntrail | 7.0 | done |
| 13 | Trail to the Heavens | 7.1 – 7.5 | **blocked — not released yet**, see HANDOVER.md |

Each expansion's own album absorbs most of its patch cycle before the *next* expansion's album
picks up the tail end of the previous one (e.g. Shadowbringers, order 7, includes 4.4–4.5
content) — don't assume patch ranges split cleanly at expansion boundaries; verify each album's
actual range against Square Enix's own catalogue rather than following the pattern blindly.

The `ROADMAP` list near the bottom of `build.py` drives the progress strip in the page header —
update it if the album list changes (it matches albums by name, not by the `order` number).

## Data schema

One JSON file per album:

```json
{
 "order": 5,
 "album": "The Far Edge of Fate",
 "full": "THE FAR EDGE OF FATE: FINAL FANTASY XIV Original Soundtrack",
 "year": 2017,
 "covers": "Patches 3.2 – 3.56",
 "spotify": "<22-char Spotify album id, optional>",
 "tracks": [
  {"n": 1, "title": "...", "type": "...", "where": "...", "origin": "...", "patch": "3.2"},
  {"n": 98, "title": "...", "type": "...", "where": "...", "origin": "...", "patch": "3.x",
   "extra_types": ["Trial"]},
  {"n": 99, "title": "...", "type": "...", "where": "...", "origin": "...", "patch": "3.x",
   "bluray_only": true}
 ]
}
```

In the `data/NN_album.py` source (a list of tuples → JSON, not hand-written JSON),
`bluray_only` and `extra_types` are both encoded as extra trailing string elements on the
tuple, parsed via `*rest`: append the literal `"bluray_only"` for that flag, and
`"extra:TypeName"` per extra type (one tuple can have several `"extra:X"` entries — they all
collect into the `extra_types` list). E.g.
`(116,"The Corpse Hall","Field battle","...","Soken","2.1","extra:Trial")`. Not every existing
album file's dict comprehension supports this yet — check the tail of a file (the
`"tracks": [...] for (n, t, c, w, o, p, *rest) in T` line) before assuming a new one does, and
copy that pattern in if it's still the plain `for n, t, c, w, o, p in T` form.

### Field rules

- **n** — track number on the album (Blu-ray numbering; streaming is identical except that
  hidden bonus tracks are missing).
- **title** — exactly as printed on the Square Enix tracklist. Curly apostrophes and en-dashes
  appear in some titles; copy them as-is.
- **type** — one value from the fixed taxonomy below. Do not invent new ones without also
  adding them to `TYPE_ORDER` in `build.py`, otherwise the chip won't render.
- **where** — the duty, zone or moment. Format conventions:
  - Duty name first, then a dash and the specific phase/boss: `"The Whorleater — Leviathan, phase 2"`.
  - For zones, name and time of day: `"The Sea of Clouds, night"`.
  - Reused tracks: say what they were reused for: `"Zenith in the Churning Mists; later Nidhogg's Eyes in DSR"`.
  - Put the literal text `(Extreme)` or `(Savage)` in `where` when — and only when — the track
    was written for that difficulty and the normal version doesn't use it (rare — see
    [Design notes](#design-notes-read-before-changing-behavior)). If a track is shared with a
    harder difficulty, say so without bare parens around the tag
    (`"...also Titan Maximum in Eden's Verse: Sepulture Savage"`, not
    `"...Sepulture (Savage)"`) — keeps the two visually distinct for a human reader.
- **origin** — composer, and/or what it is arranged from or reused from. Short. Examples:
  `"Soken"`, `"Uematsu; arr. of FFIV"`, `"Soken; from 1.0"`, `"Takada"`, `"Taken from FFXVI"`.
- **patch** — the patch that added the *content the track was written for*, as a string. Use
  the exact sub-patch when known (`"3.01"`, `"2.51"`, `"6.11"`). Use `"1.x"` only for 1.0-era
  tracks whose patch is undocumented. The build derives "major patch" (`3.0`) and expansion
  (`Heavensward`) from this automatically — you never write those.
- **bluray_only** — `true` for hidden tracks that exist on the physical Blu-ray Disc Music
  release but not on streaming. They render with an asterisk, no play button, and are
  excluded from the streaming track count.
- **extra_types** — optional list of additional `type` values, for a track whose music
  genuinely, confirmedly plays in a *different* content-type category than its primary `type`
  (e.g. a Field-battle FATE theme reused wholesale as a Trial's theme). The row shows up under
  every chip listed here in addition to its primary `type`'s chip.

  `type` (the primary one) is exclusive — exactly one value, chosen deliberately, never a
  hedge. If you're not sure which single type is correct for a track, research it and
  *replace* the wrong type — never tack on a second type to avoid deciding. `extra_types` is
  the opposite situation and is additive on purpose: confirmed dual membership, not
  uncertainty (e.g. "The Corpse Hall" is genuinely both the Steel Reign FATE theme *and* the
  Urth's Fount Trial theme). Since there's no separate playlist view, type chips are the only
  way to browse "what plays in Trial content" — so a track truly reused into a Trial needs the
  `Trial` chip too, or that browsing claim quietly breaks. Add an entry here only once you've
  *confirmed* the reuse (via the track's own Fandom "Game appearances" section); don't add
  extra types speculatively.

### Type taxonomy (keep it to these)

```
Alliance raid, Field raid, Raid, Ultimate, Trial, Boss battle, Dungeon, Variant dungeon,
Criterion dungeon, Deep dungeon, Field battle, Guildleve, PvP, Field, City,
Instanced area, Story battle, Quest & cutscene, Cutscene, Character theme, Side story,
Tribal quest, Island Sanctuary, Grand Company, Gold Saucer, Seasonal event,
Crafting & gathering, Travel & mounts, Title & menu, Jingle, Credits & theme, FFXVI crossover
```

Guidance on the fuzzy ones:
- **Trial** = primal/boss trials (normal or extreme). **Boss battle** = generic dungeon-boss
  or instanced-fight themes not tied to one trial. **Story battle** = solo instanced MSQ/job fights.
- **Raid** = 8-player raid tiers (Coils, Alexander, Omega, Eden, Pandæmonium, Arcadion).
  **Alliance raid** = 24-player, Duty Finder-queued (Crystal Tower, Mhach, Ivalice, YoRHa,
  Myths of the Realm, Echoes of Vana'diel). **Field raid** = large-scale (24–48 player) raid
  content accessed through a field mechanic rather than Duty Finder — currently just Delubrum
  Reginae (Bozjan Southern Front) and The Dalriada (Zadnor). **Ultimate** = ultimate-only reuse
  tracks (e.g. DSR, TOP).
- **Field** = open-world zones and settlements. **City** = the three city-states, Ishgard,
  Kugane, Crystarium, Eulmore, Old Sharlayan, Radz-at-Han, Tuliyollal, Solution Nine, plus
  residential districts and inns.
- A cutscene stinger that plays *inside* a raid (e.g. "Hunger", "Sins of the Father…") is
  typed as the raid, not Cutscene.

## Conventions (don't relitigate silently)

- Blu-ray-only tracks: keep Blu-ray numbering, mark with `bluray_only`, asterisk in the UI,
  footnote explains. Blu-ray video extras (concert footage, documentaries) are not tracks and
  are not listed.
- Reused 1.0 themes on later albums (Fury, Pennons Aloft, Tempest…) are listed again on the
  later album with `origin: "…; from 1.0"`.
- Where a track plays in more than one place, list the original use first.
- Composer in `origin` is the credited *composer*, not arranger, unless the arrangement is the
  point (then "arr. of …").
- Uncertain? Prefer a broader true statement ("Cutscenes") over a specific guess — a wrong
  specific is worse than a vague correct.
- Never search-and-cite lyrics; titles and annotations only.
- Before trusting a `.py` generator you haven't touched recently, diff its output track count
  against the live `.json` first — a script that's drifted out of sync will silently overwrite
  good data with stale data if you just run it.
- Before taking a Spotify album's track list as final, check the **Japanese Spotify
  storefront**, not just the US/global one — new FFXIV OST albums have historically released
  in Japan first, sometimes by months.

## Design notes (read before changing behavior)

**Why there's no separate "playlist" view.** An earlier version had one — a strict subset
showing only alliance-raid themes and music written *specifically* for an extreme/savage
version. It was removed after turning out to rest on a false premise: extreme trials in FFXIV
are built as "the same fight, harder," not a different fight, so they essentially never drop
music the normal version has — the exclusive-only filter was hiding shared music a player
doing extreme content would still hear. Since hard-mode content is a strict superset of normal
(never a replacement), filtering **All tracks** by the `Trial`/`Raid`/`Alliance raid`/
`Field raid`/`Ultimate` type chips already surfaces everything you'd hear at *any* difficulty —
shared or exclusive. `(Extreme)`/`(Savage)` tags stay in `where` as descriptive annotation
(still genuinely useful — most raid-tier "second half only" claims *are* real), they just don't
drive a UI feature.

That said: **Trial EX content is usually fully shared with Normal, but not always** (one
genuine counter-example found: an EX trial with a real extra phase unique to Extreme), and
**Raid Savage "final phase" exclusivity claims have held up every time checked** — Savage tiers
genuinely do extend fights beyond what Normal reaches, unlike most Trial EX content. Both are
reasonable priors, neither should be assumed without checking a track's own Fandom page.

**Row array shape** (index → meaning), used by `build.py`'s inline JS:
`0 #, 1 track no., 2 title, 3 type, 4 where, 5 album, 6 patch, 7 origin, 8 major patch,
9 expansion, 10 bluray flag, 11 extra_types (array, possibly empty), 12 spotify_track (id
string, empty if unknown)`. If you add a field, append it at the end and update every `d[N]`
reference in the JS. `allTypes(d)` returns `[d[3], ...d[11]]` — chip counts, the active-chip
filter, and the search-text blob all go through it, so a row with `extra_types` is findable and
counted under every one of its types.

**Play button plays the actual track inline** when a Spotify track ID is known for that row
(row index 12, `spotify_track` — full track for a Premium account signed into Spotify in that
browser, a 30-second preview otherwise; `<button class="play-btn" data-id="...">` fires
`playTrack()`, which points a fixed-position iframe at
`open.spotify.com/embed/track/<id>` — Spotify's own embed shows the title/artist/art, no extra
markup needed). Falls back to the old `open.spotify.com/search/<title>` deep-link when no ID is
known for a row (e.g. a newly-added album before its IDs have been fetched).

**Where the IDs come from**: `data/spotify_ids/NN_album.json`, one optional sidecar file per
album, `{"<track n>": {"id": "<spotify track id>", "name": "..."}}`. Deliberately kept *out* of
the main `data/NN_album.json` files — it's fetched wholesale from the Spotify Web API rather
than hand-researched per track, and keeping it separate means it can be regenerated anytime
without touching the tuple-based album sources (`build.py` merges it in at build time via
`spotify_ids_for()`, matching on track `n`; a missing sidecar or a missing entry both fall back
to the search-link cleanly).

To (re)fetch a sidecar file: get a Spotify Client ID + Secret from a **Developer app**
(developer.spotify.com/dashboard — free, app-only "Client Credentials" auth, no user login,
scoped to reading public catalog data only), exchange them for a bearer token at
`accounts.spotify.com/api/token`, then call
`GET api.spotify.com/v1/albums/{id}/tracks?limit=50&offset=N` (paginate via the response's
`next` field) for the album's own Spotify ID. This is far more reliable than trying to scrape
`open.spotify.com/album/<id>` directly — that page's tracklist is virtualized and can silently
render an incomplete list depending on how it's scrolled, with no error to signal the gap; the
real API returns the complete, exact, ordered tracklist every time. Verify a freshly-fetched
sidecar's track count against the main album JSON's non-Blu-ray-only track count before
trusting it, and spot-check titles — Spotify's own title metadata occasionally differs
cosmetically from Square Enix's official tracklist (e.g. expanding an abbreviation, dropping a
diacritic), which is a difference worth knowing about but not something to "fix" by overwriting
the correct title.

Adding an album never requires touching `build.py` unless it introduces a new content type or
the roadmap changes.

## Researching a new album

Each step below has a known failure mode.

1. **Official track order and credits.** Find the catalogue number
   (`"<Album name> FINAL FANTASY XIV Original Soundtrack SQUARE ENIX MUSIC lineup"`), then
   `https://www.jp.square-enix.com/music/en/lineup/item/SQEX-XXXXX.html` for the authoritative
   English track order. The Japanese special-site page (`.../music/sem/page/ff14/<album>/`)
   additionally lists composer/arranger per track and, in the JP language version, each
   track's Japanese subtitle — which usually names the duty (e.g. `〜蛮神ラーヴァナ討滅戦〜` =
   "Ravana trial").

2. **Confirm the streaming track count.** Search `"<album> FINAL FANTASY XIV Original
   Soundtrack" Spotify` (check the JP storefront too, not just US/global — see Conventions).
   The song count tells you whether hidden Blu-ray tracks exist (Blu-ray count > streaming
   count; known cases: ARR 119 vs 120, Before the Fall 61 vs 63). Grab the Spotify album id
   from the `open.spotify.com/album/<id>` URL for the `spotify` field.

3. **"Where it plays": the Final Fantasy Wiki (Fandom).**
   `https://finalfantasy.fandom.com/wiki/<Album>:_Final_Fantasy_XIV_Original_Soundtrack` has a
   per-track annotation for every album — including which specific phase/mode a track plays
   in, usually the *only* way to tell an Extreme/Savage-exclusive track from one that reuses
   normal-mode music. This domain (and `ffxiv.gamerescape.com`) sits behind Cloudflare and can
   flatly refuse a plain HTTP fetch; if that happens, a browser-based fetch usually gets
   through, but expect it to adaptively rate-limit after several rapid requests — space
   requests out rather than firing them back-to-back, and treat a successful load as
   opportunistic, not guaranteed on retry.

   **The Wayback Machine is the reliable fallback**, and often worth trying first: navigate to
   `https://web.archive.org/web/20240101000000/<the live Fandom URL>` (any date string works;
   archive.org redirects to its closest actual snapshot). This serves a cached copy entirely
   from archive.org's own infrastructure, never touching the live site, so Cloudflare's rate
   limit doesn't apply — prefer it outright over live access when a snapshot from anytime in
   the last few years exists (album pages don't change once released).

   If both are rate-limited and a track's mode can't be confirmed: web-search the album name
   plus 4–6 quoted track titles plus `fandom` — the search result *snippet* sometimes returns
   the annotation even when the page won't load. If that also fails, default to **not**
   flagging `(Extreme)`/`(Savage)` rather than guessing.

4. **Cross-check with the in-game orchestrion listings** (for placing a track — "which OST is
   this actually on" — not for verifying duty/exclusivity claims on an existing row; use each
   track's own Fandom page for that).
   `https://ffxiv.consolegameswiki.com/wiki/Orchestrion_Roll` maps every orchestrion roll to
   its theme, with a `Patch` column and which OST it's on (fetches fine, not Cloudflare-gated).
   It's long — for a single uncertain track, fetch its own page instead:
   `https://ffxiv.consolegameswiki.com/wiki/<Title>_Orchestrion_Roll`. **Trap**: the `Patch`
   column is when the orchestrion *roll item* became obtainable, not necessarily when the
   underlying music/dungeon shipped — SE sometimes backfills a roll years later. Tell: the
   `OST Release` column names an album that predates the `Patch` value, or the patch looks
   wrong for known content. Verify the actual content patch independently when that happens
   (a plain web search for "<dungeon> FFXIV patch added" usually settles it).

5. **Patch numbers.** Album sections are usually grouped by patch but aren't reliable for
   individual tracks — verify against the patch the content actually shipped in. Known traps:
   "Battle on the Big Bridge" sits in a 2.2 tracklist section but the trial is 2.1; Alexander
   Gordias and Thordan's Reign (EX) are 3.01, not 3.0. For 1.0-era content, the
   consolegameswiki `Patches` page has a dated list of every 1.x patch.

6. **Write the file, build, spot-check.** Write `data/NN_album.py` in the same shape as the
   existing ones, run it, then `python3 build.py`. Then check what the album contributed and
   whether anything's mistagged — both directions matter (don't assume a track is
   EX/Savage-exclusive just because it's the fight's final phase; verify against the track's
   own Fandom page before writing `(Extreme)`/`(Savage)` into `where`):

   ```bash
   node -e "
   const h=require('fs').readFileSync('index.html','utf8');
   const d=JSON.parse(h.match(/const DATA = (\[.*?\]);\nconst ALBUMS/s)[1]);
   const rows = d.filter(r=>r[5]==='<Album>');
   console.log('total:', rows.length);
   console.log('Trial/Raid/Alliance raid/Field raid/Ultimate rows:');
   console.log(rows.filter(r=>['Trial','Raid','Alliance raid','Field raid','Ultimate'].includes(r[3]))
     .map(r=>r[1]+' '+r[2]+' ['+r[3]+'] — '+r[4]).join('\n'));"
   ```
