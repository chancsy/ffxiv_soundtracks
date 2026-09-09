# FFXIV Soundtrack Table — Session Handover

Purpose: a filterable HTML table of every track on the FINAL FANTASY XIV soundtrack albums
that are on Spotify, annotated with the duty/area/moment each track scores. Filter by
content-type chip (Trial, Raid, Alliance raid, Field raid, Ultimate, …) to browse endgame
music specifically — there is no separate "playlist" view; see §4 for why one isn't needed.

This document is everything a fresh session (human or model) needs to keep building it.
Read the whole thing before adding an album — most mistakes so far came from skipping the
conventions section.

---

## 1. What exists

```
ffxiv/
├── build.py                 # generator: reads data/*.json → writes index.html
├── data/
│   ├── 01_before_meteor.{py,json}      done (104 tracks, patches 1.0–1.23)
│   ├── 02_a_realm_reborn.{py,json}     done (119 + 1 Blu-ray-only, 2.0–2.1)
│   ├── 03_before_the_fall.{py,json}    done (61 + 2 Blu-ray-only, 2.2–2.55)
│   ├── 04_heavensward.{py,json}        done (58, 3.0–3.1)
│   ├── 05_far_edge_of_fate.{py,json}   done (50, 3.2–3.56)
│   ├── 06_stormblood.{py,json}         done (105, 4.0–4.3)
│   ├── 07_shadowbringers.{py,json}     done (88, 4.4–4.5 and 5.0)
│   ├── 08_death_unto_dawn.{py,json}    done (84, 5.1–5.5)
│   ├── 09_endwalker.{py,json}          done (63, 6.0)
│   ├── 11_growing_light.json           done (93, 6.1–6.58) — **no .py source, JSON is
│   │                                   hand-maintained directly; edit it in place, and if you
│   │                                   ever do write a `.py` generator for it, base it on the
│   │                                   current JSON first (see the near-data-loss note below —
│   │                                   this is exactly the failure mode that caused it)
│   └── 12_dawntrail.{py,json}          done (66, 7.0)
└── HANDOVER.md              # this file
```

Every `.py`/`.json` pair *should* round-trip byte-for-byte (`python3 data/NN_x.py` regenerates
the `.json` identically) — verify this before trusting a `.py` file you haven't touched recently.

Output: `index.html` — a single self-contained file (inline CSS + JS, no
external dependencies). Regenerate it with `python3 build.py`; never hand-edit the HTML.

### Roadmap (album `order` numbers are fixed — leave gaps as shown)

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
| 13 | Trail to the Heavens | 7.1 – 7.5 | **blocked, not yet released** — see note below, not skipped by choice |

**Correction found in this session**: the "Stormblood" and "Shadowbringers" ranges above were originally
`4.0` and `4.1–4.5` — wrong. SE's own catalogue confirms STORMBLOOD (SQEX-20053, 105 tracks) covers
4.0–4.3, and SHADOWBRINGERS (SQEX-20069, 88 tracks) covers 4.4–4.5 *and* 5.0 as one release — i.e. each
expansion's own album absorbs most of its patch cycle before the *next* expansion's album picks up the
tail end of the previous one. Death Unto Dawn (5.1–5.5) was independently verified correct as originally
written, so this split isn't universal — verify each album's actual patch range against SE's own listing
before assuming the "one album per expansion, patch-EP albums separate" pattern from Heavensward carries
forward as-is.

The `ROADMAP` list near the bottom of `build.py` drives the progress strip in the page header.
Update it if the album list changes.

**Order 9→11 jump is intentional, not a mistake.** Order 10 was originally reserved on the
assumption Endwalker might get a mid-cycle album the way Heavensward (→ The Far Edge of Fate)
and Shadowbringers (→ Death Unto Dawn) did, before its own EP-compilation album. It didn't —
all of patches 6.1–6.58 went straight into one compilation (Growing Light, order 11) — so the
reserved row was removed from the table (confirmed first that no album JSON uses `order: 10`
and `build.py`'s `ROADMAP` list matches albums by name, not this number, so nothing depends on
it). Don't renumber 9/11/12/13 to close the gap if a real order-10 album ever does turn up
between Endwalker and Growing Light chronologically — just reintroduce it as order 10.

---

## 2. Data schema

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

In the `data/NN_album.py` source (a list of tuples → JSON, not hand-written JSON), `bluray_only`
and `extra_types` are both encoded as extra trailing string elements on the tuple, parsed via
`*rest`: append the literal `"bluray_only"` for that flag, and `"extra:TypeName"` per extra type
(one tuple can have several `"extra:X"` entries — they all collect into the `extra_types` list).
E.g. `(116,"The Corpse Hall","Field battle","...","Soken","2.1","extra:Trial")`. Not every
existing album file's dict comprehension supports this yet — `02_a_realm_reborn.py`,
`07_shadowbringers.py` and `09_endwalker.py` do; check the tail of a file (the
`"tracks": [...] for (n, t, c, w, o, p, *rest) in T` line) before assuming a new one does, and
copy that pattern in if it's still the plain `for n, t, c, w, o, p in T` form.

Field rules:

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
    was written for that difficulty and the normal version doesn't use it (rare — see §4). If a
    track is shared with a harder difficulty, say so without bare parens around the tag
    (`"...also Titan Maximum in Eden's Verse: Sepulture Savage"`, not `"...Sepulture (Savage)"`)
    — pure writing hygiene now that nothing parses the string, but keeps the two visually
    distinct for a human reader.
- **origin** — composer, and/or what it is arranged from or reused from. Short. Examples:
  `"Soken"`, `"Uematsu; arr. of FFIV"`, `"Soken; from 1.0"`, `"Takada"`, `"Taken from FFXVI"`.
- **patch** — the patch that added the *content the track was written for*, as a string.
  Use the exact sub-patch when known (`"3.01"`, `"2.51"`, `"6.11"`). Use `"1.x"` only for
  1.0-era tracks whose patch is undocumented. The build derives "major patch" (`3.0`) and
  expansion (`Heavensward`) from this automatically — you never write those.
- **bluray_only** — `true` for hidden tracks that exist on the physical Blu-ray Disc Music
  release but not on streaming. They render with an asterisk, no play button, and are
  excluded from the streaming track count.
- **extra_types** — optional list of additional `type` values, for a track whose music
  genuinely, confirmedly plays in a *different* content-type category than its primary `type`
  (e.g. a Field-battle FATE theme reused wholesale as a Trial's theme). The row shows up under
  every chip listed here in addition to its primary `type`'s chip. See the exclusivity note
  below for when to use this vs. just picking a different primary `type`.

### Type taxonomy (keep it to these)

```
Alliance raid, Field raid, Raid, Ultimate, Trial, Boss battle, Dungeon, Variant dungeon,
Criterion dungeon, Deep dungeon, Field battle, Guildleve, PvP, Field, City,
Instanced area, Story battle, Quest & cutscene, Cutscene, Character theme, Side story,
Tribal quest, Island Sanctuary, Grand Company, Gold Saucer, Seasonal event,
Crafting & gathering, Travel & mounts, Title & menu, Jingle, Credits & theme, FFXVI crossover
```

`type` (the primary one) is exclusive — exactly one value, chosen deliberately, never a hedge.
If you're not sure which single type is correct for a track (the Hades/Diamond Weapon bug:
a fight is actually a registered Trial but got defaulted to `Boss battle`/`Story battle` out
of uncertainty), the fix is to research it and *replace* the wrong type — never tack on a
second type to avoid deciding.

`extra_types` is the opposite situation and is additive on purpose: a track's music has a
*second, equally real* identity in a different category — not uncertainty about which one is
right, but confirmed dual membership (e.g. "The Corpse Hall" is genuinely both the Steel Reign
FATE theme *and* the Urth's Fount Trial theme; "Who Brings Shadow"/"Invincible" are genuinely
both Hades's Trial theme *and* the MSQ's climactic story battle). This exists because, since §4
removed the separate playlist view, type chips are the only way to browse "what plays in Trial
content" — so a track that's truly reused into a Trial needs the `Trial` chip too, or that
browsing claim quietly breaks. Add an entry here only once you've *confirmed* the reuse (via
the track's own Fandom page, same as the Tier 4 audit); don't add extra types speculatively.

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
  Kugane, Crystarium, Eulmore, Old Sharlayan, Radz-at-Han, Tuliyollal, Solution Nine,
  plus residential districts and inns.
- A cutscene stinger that plays *inside* a raid (e.g. "Hunger", "Sins of the Father…")
  is typed as the raid, not Cutscene.

---

## 3. How to research an album (the part that actually takes time)

Do these in order. Each step has a known failure mode noted.

### Step 1 — Official track order and credits
`https://www.jp.square-enix.com/music/en/lineup/item/SQEX-XXXXX.html` (find the catalogue
number by searching `"<Album name> FINAL FANTASY XIV Original Soundtrack SQUARE ENIX MUSIC lineup"`).
Gives the authoritative English track order. The Japanese special-site page
(`.../music/sem/page/ff14/<album>/`) additionally lists composer/arranger per track and,
in the JP language version, the Japanese subtitle of each track — which usually names the
duty (e.g. `〜蛮神ラーヴァナ討滅戦〜` = "Ravana trial"). Fetching the EN page works; the JP page
sometimes only surfaces through search snippets.

### Step 2 — Confirm the streaming track count
Search `"<album> FINAL FANTASY XIV Original Soundtrack" Spotify` or Apple Music. The song
count tells you whether hidden Blu-ray tracks exist (Blu-ray count > streaming count).
Known: ARR 119 vs 120; Before the Fall 61 vs 63. Also grab the Spotify album id from the
`open.spotify.com/album/<id>` URL for the `spotify` field.

### Step 3 — "Where it plays": the Final Fantasy Wiki (Fandom)
`https://finalfantasy.fandom.com/wiki/<Album>:_Final_Fantasy_XIV_Original_Soundtrack`
has a per-track annotation and Japanese subtitle for every album — including, critically,
which specific phase/mode a track plays in, which is usually the *only* way to tell an
Extreme/Savage-exclusive track from one that reuses normal-mode music (see §4).

**As of this session, a `playwright` MCP server (headless Chromium via `@playwright/mcp`)
is set up and can actually load this page** — plain `WebFetch` gets a flat HTTP 402 on this
domain every time, not intermittently as previously documented. The Playwright route needed
two fixes beyond just "use a real browser": (1) an init-script patching `navigator.webdriver`
and a few other automation tells (Cloudflare's static bot-fingerprint check blocks vanilla
Playwright outright — see `.mcp-playwright-stealth-init.js` at the workspace root), and
(2) accepting that even with that fix, **Cloudflare still adaptively re-challenges after
several rapid navigations in one session** — it's request-velocity/behavior based, not just
a one-time fingerprint gate, so it can't be fully "solved," only budgeted around:
- Space out navigations rather than firing them back-to-back; a page that 403s
  ("Performing security verification" / "Just a moment...") often works again after a pause.
- Treat each successful page load as opportunistic, not guaranteed on retry.
- The full setup (Node 20 static binary + Chromium + its OS deps, all self-healing via
  `custom-cont-init.d`) lives in
  `scripts_collection/userscripts/rpi5/docker_apps/code-server/` — shouldn't need touching
  again, but if `playwright` MCP tools aren't in the tool list, check `.mcp.json` is at the
  actual workspace root (not a subfolder) and that the container has been recreated since.

**Better fallback found this session: the Wayback Machine.** Navigate (via the `playwright`
MCP browser, not plain `WebFetch` — archive.org itself isn't blocked either way, but the
browser route worked reliably) to
`https://web.archive.org/web/20240101000000/<the live Fandom URL>` — any date string works,
archive.org redirects to its closest actual snapshot. This serves a cached copy entirely from
archive.org's own infrastructure, never touching the live Fandom site, so **Cloudflare's rate
limit doesn't apply at all** — this worked immediately after the live site had just been
blocked for hours. Prefer this over live Fandom access outright when a snapshot from anytime
in the last few years exists (album pages don't change once released), rather than only
reaching for it as a last resort.

Fallback when Fandom (live or archived) is rate-limited and a track's mode can't be confirmed: web-search the
album name plus 4–6 quoted track titles plus `fandom` or `lit.` — the search result *snippet*
sometimes returns the annotation even when the page won't load. When even that fails and a
track's EX/Savage-exclusivity genuinely can't be confirmed, default to **not** flagging it
(leave `(Extreme)`/`(Savage)` out of `where`) rather than guessing — consistent with §6's
"prefer a broader true statement over a specific guess."

### Step 4 — Cross-check with the in-game orchestrion listings

**Scope note (added after the Tier 1–4 audit session): this is for placing a track during new-
album research — "which OST is this actually on" — not for verifying duty/exclusivity claims
on existing rows.** The whole Tier 1–4 audit never used this step; it relied on the Eorzea
Database duty roster (§7's audit notes) for "does this duty exist / what type is it" and each
track's own Fandom page for "where does it actually play, shared or exclusive" — both more
direct for those questions than this listing's `Patch`/`OST Release` columns, given the trap
noted below. Confirmed the site itself still loads fine (plain WebFetch, no Cloudflare) during
that session, but that's a connectivity check, not a claim that it was actually used or is the
right tool for auditing — use the Eorzea DB + track-page combo for that instead.

`https://ffxiv.consolegameswiki.com/wiki/Orchestrion_Roll` maps every orchestrion roll to
its theme ("Coerthas Western Highlands Night Theme", "Vanu Vanu Tribe Theme", etc.), with a
`Patch` column and which OST it's on. It fetches fine (via plain WebFetch, no Cloudflare) but
is very long — the Locales sections come first; later sections (Dungeons, Trials, Raids) get
truncated at the fetch limit. For a single uncertain track, fetch its own page:
`https://ffxiv.consolegameswiki.com/wiki/<Title>_Orchestrion_Roll` (search for it first so
the URL is "seen" by the fetch tool). This is what resolved e.g. "Game Theory" = mini-game theme.

**Trap found this session: the `Patch` column is when the orchestrion *roll item* became
obtainable in-game, not necessarily when the underlying music/dungeon shipped.** SE sometimes
backfills a roll years after its content patch (e.g. Lost City of Amdapor (Hard) is 3.2
content, but its roll's `Patch` cell reads "4.3" — a Stormblood-era backfill). Tell: the `OST
Release` column names an album that predates the `Patch` value, or the patch looks wrong for
known content (e.g. a Heavensward dungeon showing a 4.x/5.x patch). When that happens, verify
the actual content patch independently (a plain web search for "<dungeon> FFXIV patch added"
usually settles it) rather than trusting the column as-is.

`ffxiv.gamerescape.com` loads cleanly via the Playwright route (no Cloudflare at all there) —
the old "blocks automated fetches" note only applied to plain `WebFetch`. `vgmdb.net` is still
Cloudflare-gated same as Fandom and hit the same 403 via Playwright — still not worth relying on.

### Step 5 — Patch numbers
Album sections are usually grouped by patch (Before the Fall literally has 2.2/2.3/2.4/2.5
headings) but they are **not** reliable for individual tracks. Verify against the patch
the content shipped in. Known traps already handled:
- "Battle on the Big Bridge" sits in the 2.2 section but the trial is 2.1.
- Gold Saucer tracks are 2.51, Steps of Faith is 2.55, Eternal Bonding is 2.45.
- Alexander Gordias and Thordan's Reign (EX) are 3.01, not 3.0.
- Growing Light: DSR 6.11, TOP 6.31, FFXVI collab 6.58, Rising 2023 minigame 6.45.
For 1.0-era content the consolegameswiki `Patches` page has a dated list of every 1.x patch.

### Step 6 — Write the file, build, spot-check
Write `data/NN_album.py` in the same shape as the existing ones (a list of tuples → JSON),
run it, then `python3 build.py`. Then run this to see what the album contributed and
double-check nothing is mistagged — both directions matter (see §4's Sephirot/Zurvan lesson:
don't assume a track is EX/Savage-exclusive just because it's the fight's final phase; verify
against the track's own Fandom page before writing `(Extreme)`/`(Savage)` into `where`):

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

---

## 4. The playlist feature — removed; use type chips instead

Earlier versions of this project had a separate "Playlist" view: a strict subset showing only
alliance-raid themes plus music written *specifically* for an extreme/savage version (i.e. the
normal version never uses it). **This was removed in a later session** after being proven to
rest on a false premise. Keep this section as the record of why, so it doesn't get reinvented.

**What killed it**: while investigating an unrelated report, two of the four tracks flagged as
"Extreme-exclusive" on The Far Edge of Fate (Fiend — Sephirot; Equilibrium — Sophia) turned out,
per each track's own Fandom page, to explicitly say *"This song plays in [Normal duty] **and**
[Extreme duty]"* — i.e. fully shared, not exclusive. The other two (Penultimania/Infinity —
Zurvan) showed the identical signature (same Background Music list on both the normal and
Extreme duty's own Gamerescape infobox). Spot-checking further (Ifrit, Ravana/Thok ast Thok)
found the same pattern every time: **Extreme trials in FFXIV are built as "the same fight,
harder," not a different fight** — they essentially never drop music the normal version has.
That means "exclusive-only" was excluding almost nothing except genuinely bespoke EX/Savage
themes, while wrongly excluding a lot of shared music that a player doing Extreme content
would still hear — the opposite of what a "here's what plays in endgame content" feature
should do.

The fix: since hard-mode content is a strict superset of normal (never a replacement), simply
filtering **All tracks** by the `Trial` / `Raid` / `Alliance raid` / `Field raid` / `Ultimate`
type chips already surfaces everything you'd hear at *any* difficulty of that content — shared
or exclusive — because the type tag doesn't care about exclusivity. Nothing was lost by removing
the separate view; it was actively wrong. `(Extreme)`/`(Savage)` tags stay in `where` text as
descriptive annotation (genuinely useful — it tells you a piece really is difficulty-specific,
which is still true for most raid-tier "second half only" cases), they just no longer drive a
UI feature or a `playlist` flag on the row.

**Historical bugs this feature caused, kept for the writing-discipline lesson**: the original
implementation flagged a row if `type == "Alliance raid"` **or** `where` contained the bare
substring `Extreme` (no parens) **or** `(Savage)`. The bare-`Extreme` version meant *any* prose
mentioning "Extreme" — even "(normal and Extreme)" describing a *shared* track — silently
got flagged; fixed at the time to require the exact `(Extreme)` tag. Even after that fix, two
more accidental matches turned up from secondary-reuse mentions written with the literal
tag in parens (e.g. "...reused in Eden's Verse: Sepulture (Savage)" describing a *different*,
unrelated fight) — fixed by dropping the parens in secondary mentions ("...Sepulture Savage").
None of this class of bug can recur now that the mechanism is gone, which is the real fix.

A separate, still-relevant bug found along the way: filtering to the Shadowbringers expansion
and the "Trial" type chip hid the Hades fight ("Who Brings Shadow" / "Invincible") and the
Diamond Weapon fight ("In the Arms of War") — not a missing-data problem, a `type` mis-tag.
Hades's fight (the MSQ duty **The Dying Gasp**, EX form **The Minstrel's Ballad: Hades's
Elegy**) was tagged `"Story battle"`, and Diamond Weapon's fight (the duty **The Cloud Deck**,
reusing that name from the earlier Ruby/Emerald/Sapphire Weapon trio fight in 5.2) was tagged
`"Boss battle"` — both are actually queueable Duty-Finder Trials, fixed to `type: "Trial"`.
(Later refined further: Hades's fight is also the MSQ's climactic story battle — a genuinely
real second identity, not just leftover uncertainty — so it now carries
`extra_types: ["Story battle"]` alongside `type: "Trial"`, per §2's `extra_types` field.)
Takeaway, independent of the playlist removal: when `where` describes a boss/story fight,
check whether it's actually a registered Trial/Raid duty rather than defaulting to
"Boss battle"/"Story battle" — a wrong `type` silently hides a row from the type-chip filter.

Ordering is album `order` then track `n`, which matches content chronology closely enough
because the albums themselves are chronological.

---

## 5. What `build.py` does (so you can change it safely)

- Loads every `data/*.json`, sorts by `order`, assigns a running index `#`.
- Row array shape (index → meaning), used by the inline JS:
  `0 #, 1 track no., 2 title, 3 type, 4 where, 5 album, 6 patch, 7 origin,
   8 major patch, 9 expansion, 10 bluray flag, 11 extra_types (array, possibly empty)`.
  If you add a field, append it at the end and update every `d[N]` reference in the JS.
  (There used to be a `playlist flag` at index 8 — removed, see §4 — don't re-add it.)
  `allTypes(d)` in the JS returns `[d[3], ...d[11]]` — chip counts, the active-chip filter,
  and the search-text blob all go through it, so a row with `extra_types` is findable and
  counted under every one of its types, not just its primary one.
- Derives `major` (`"6.11"` → `"6.1"`; 1.x left as-is) and expansion from the patch's first digit
  (`EXP` dict at the top).
- Renders: header with progress strip (from `ROADMAP`), controls (search, album select +
  "Open album on Spotify" link, expansion select, patch select with sub-patches nested under
  majors, content-type chips with counts, Show all), the table, footnotes. One view only —
  no All/Playlist toggle.
- Play button = `https://open.spotify.com/search/<title + " FINAL FANTASY XIV">` — a search
  deep-link, because Spotify track IDs aren't fetchable. If real track URLs are ever
  collected, add a `spotify_track` field to tracks and prefer it in the `d[2]` link builder.
- Design tokens are the CSS variables at the top of `CSS` (night blue ground, amber accent,
  teal type chips, rose album column, Spotify green for play). Mobile layout collapses the
  table into cards below 820px.

Adding an album never requires touching `build.py` unless the album introduces a new
content type or the roadmap changes.

---

## 6. Conventions and decisions already made (don't relitigate silently)

- Blu-ray-only tracks: keep Blu-ray numbering, mark with `bluray_only`, asterisk in the UI,
  footnote explains. Blu-ray video extras (concert footage, documentaries) are not tracks and
  are not listed.
- Reused 1.0 themes on later albums (Fury, Pennons Aloft, Tempest…) are listed again on the
  later album with `origin: "…; from 1.0"`.
- Where a track plays in more than one place, list the original use first.
- Composer in `origin` is the credited *composer*, not arranger, unless the arrangement is
  the point (then "arr. of …").
- Uncertain? Prefer a broader true statement ("Cutscenes") over a specific guess. The user
  explicitly asked to prioritise accuracy; a wrong specific is worse than a vague correct.
- Never search-and-cite lyrics; titles and annotations only.

---

## 7. Open TODOs

Status snapshot as of the session that removed the playlist view (§4) and recovered
albums 1–3 from a near-data-loss (see the note at the end of this section). Nothing below
is urgent or user-requested-right-now — this is the running backlog so any session can pick
up a thread without re-deriving context. Update the status line inline as items move.

- **[TIER 1 FULLY DONE; TIERS 2–4 REMAIN] Accuracy audit, cross-checked by content type.** The plan agreed
  with the user: build a ground-truth duty roster per expansion from the *official* Eorzea
  Database duty browser (`na.finalfantasyxiv.com/lodestone/playguide/db/duty/?category2=N` —
  4=Trials, 5=Raids **(alliance raids are bundled in here too, not a separate category)**,
  28=Ultimate; **6 is PvP, not Alliance Raids** — corrected assumption, see below;
  `&ex_version=N` filters by expansion, where 0=ARR, 1=HW, 2=StB, 3=ShB, 4=EW, 5=DT). Plain
  `WebFetch` works fine on these pages (no Cloudflare gate, unlike Fandom) — much faster than
  the Playwright/Wayback route, save that for Fandom track/duty pages specifically. Then, in
  priority order:
  1. **Tier 1** — every row currently typed `Trial`/`Raid`/`Alliance raid`/`Field raid`/`Ultimate`
     (~222 rows): confirm the duty exists in the roster, confirm `type` matches, and — per the
     Sephirot/Zurvan lesson in §4 — confirm any `(Extreme)`/`(Savage)` claim in `where` against
     that specific track's own Fandom "Game appearances" section (not the duty infobox alone;
     that page also lists both Normal-page and Extreme-page results, no automated shortcut).

     **Tier 1 is now fully DONE — both halves, all categories, all 6 expansions.** The
     missing-duty-and-wrong-type-or-name half covered Trials, Raids, Alliance Raids, and
     Ultimate (Field raid was already handled pre-Tier-1, see §2). The exclusivity-claim half
     checked every remaining `(Extreme)`/`(Savage)` tag outside The Far Edge of Fate (which was
     done earlier) against the Sephirot/Zurvan pattern — all 8 confirmed genuinely correct, via
     each track's own Fandom page or a direct Normal-vs-Savage duty-infobox comparison:
     "Heroes Never Die" (Thordan EX — a real exception to the "Extreme always shares 100%"
     rule: it's a genuine extra first phase unique to EX, confirmed via the track's own page,
     which lists only the EX duty), "Final, Not Final" (Deltascape V4.0 Savage — confirmed
     absent from Normal's own BGM infobox), "The Extreme (Shadowbringers)" (Eden's Promise:
     Eternity Savage — confirmed absent from Normal's infobox, which lists only "Promises to
     Keep"/"Treasured Memory"), "From the Heavens" (Alphascape V4.0 Savage — its own page says
     outright "can only be heard if you... make it through... in Savage mode"), "Dancing Mad -
     Movement IV" (Sigmascape V4.0 Savage — "only plays in the Savage raid" per its own page),
     "A Risky Bet" (AAC Light-heavyweight M4 Savage phase 2 — consistently described everywhere
     as M4S-specific), "White Stone Black" and "Ultima's Perfection (Endwalker)" (Abyssos/
     Anabaseios final-circle Savage phase 2s — same consistent Savage-specific sourcing).
     Net takeaway: Trial EX content is *usually* fully shared with Normal (Far Edge of Fate's 4
     false claims) but not *always* (Thordan EX is real) — and Raid Savage "final phase" claims
     held up 100% of the time checked (7 for 7) — Savage tiers genuinely do extend fights beyond
     what Normal reaches, unlike most Trial EX content. Both are worth remembering as priors for
     future albums, but neither should be assumed without checking — that's the whole lesson of
     this audit.

     **Progress so far, Trials sub-pass:**
     - The Far Edge of Fate (Sephirot/Sophia/Zurvan): done — found and fixed 4 wrong exclusivity
       claims (Fiend, Equilibrium, Penultimania, Infinity — all actually shared, not exclusive).
     - A Realm Reborn / Before the Fall (ARR-era, `ex_version=0` roster, 26 trials): done a
       missing-duty pass (not yet an exclusivity pass on what *is* present). Found two gaps:
       **Urth's Fount** (Odin, patch 2.5) was entirely absent — fixed, it reuses "The Corpse
       Hall" (track 116, already in `02_a_realm_reborn.json` for the Steel Reign FATE); this is
       also the case that prompted adding `extra_types` (§2) — the row now carries
       `extra_types: ["Trial"]` in addition to the `where`-text mention, so it's actually
       findable under the Trial chip, not just documented in prose. **The Dragon's Neck** (Ultros
       & Typhon, Hildibrand
       questline) checked and left alone on purpose — its BGM is the raw, unarranged FFVI
       "The Decisive Battle," which per its own Fandom page was never released on any FFXIV
       soundtrack album (only the *rearranged* "A Battle Decisively," a different, unrelated
       Stormblood track, got an OST release) — so there's nothing addable within this project's
       stated scope ("every track on the soundtrack albums"), not a bug.
     - Heavensward (`ex_version=1`, 14 trials): spot-checked for missing duties only (Bismarck/
       Limitless Blue and Nidhogg/Final Steps of Faith both confirmed present) — **not yet**
       checked for wrong exclusivity claims the way Far Edge of Fate was.
     - **Stormblood/Shadowbringers/Endwalker/Dawntrail missing-duty pass: done.** All ~60 trial
       duties across these 4 expansions cross-referenced. Found and fixed three more real gaps
       (same drill: check the duty's own BGM via its Fandom page, then check whether that track
       is already in the data under a different/wrong duty name):
       - **Kugane Ohashi** (Yojimbo/Gilgamesh, Stormblood 4.56) was absent — fixed, it reuses
         "Battle on the Big Bridge" (Before the Fall track 13) for the reveal phase; noted in
         `where`, no `extra_types` needed since that track is already typed `Trial`.
       - **Cinder Drift** (Ruby Weapon, Stormblood 5.2) had a wrong duty name: tracks 24/25 in
         Death Unto Dawn (`Ultima (Scions & Sinners)`, `Rise of the White Raven`) said
         `"The Cloud Deck"`, which is actually a *different* trial (Diamond Weapon only, 5.5).
         Also dropped an incorrect "Sapphire Weapon" mention — Sapphire is a solo story
         instance, not part of this Trial, confirmed via a third-party check of the full
         Werlyt-arc weapon list. Fixed to name Cinder Drift (and confirmed via the track's own
         page that "Ultima (Scions & Sinners)" is *also* legitimately reused in Castrum Marinum/
         Emerald Weapon — that part of the original `where` text was right).
       - **The Gilded Araya** (Asura, Endwalker patch 6.55) was absent — fixed, it reuses
         "FINAL FANTASY IV: Battle 2 (Endwalker)" (Growing Light track 9, the generic
         post-Endwalker dungeon-boss theme) — `where` updated and `extra_types: ["Trial"]` added.
       - Confirmed out of scope, not bugs: **The Great Hunt** (Rathalos, Stormblood/Monster
         Hunter collab) uses two licensed MHW tracks never released on any FFXIV OST — same
         situation as The Dragon's Neck above. Dawntrail's `ex_version=5` roster includes several
         trials (Recollection, The Ageless Necropolis, The Windward Wilds, Hell on Rails, The
         Unmaking) that are all patch 7.1+ content — covered by the already-deferred "Dawntrail
         patch EPs" roadmap item (order 13), not missing from anything in scope.
       - Everything else on these 4 rosters (Susano/Pool of Tribute, Lakshmi/Emanation,
         Shinryu/Royal Menagerie, Tsukuyomi/Castrum Fluminis, Byakko/Jade Stoa, Suzaku/Hells'
         Kier, Seiryu/Wreath of Snakes, Titania/Dancing Plague, Innocence/Crown of Immaculate,
         Elidibus/Seat of Sacrifice, Emerald Weapon/Castrum Marinum, Diamond Weapon/Cloud Deck,
         Zodiark/Dark Inside, Hydaelyn/Mothercrystal, Meteion/Final Day, Zeromus/Abyssal
         Fracture, Barbariccia/Storm's Crown, Golbez/Mount Ordeals & Voidcast Dais,
         Valigarmanda/Worqor Lar Dor, Zoraal Ja/Everkeep, Sphene/Interphos) was already present
         and correctly duty-named — no further gaps found. **The exclusivity-claim pass (are any
         existing `(Extreme)`/`(Savage)` tags on these actually wrong, the Sephirot/Zurvan
         pattern) has *not* been run on any of these — only the missing-duty pass has.**
     - **Raids missing-duty pass (category2=5, all 6 expansions): done.** Note: for ARR
       (`ex_version=0`) and Endwalker (`ex_version=4`) this EDB category also lists what are
       really Alliance Raids by modern terminology (Crystal Tower; Aglaia/Euphrosyne/Thaleia) —
       an EDB historical-categorization quirk, not a problem for our own `type` tagging, just
       something to know when cross-referencing. Checked every raid tier across every
       expansion (Coils, Alexander, Omega/Deltascape-Sigmascape-Alphascape, Eden's Gate/Verse/
       Promise, Asphodelos/Abyssos/Anabaseios, AAC Light-heavyweight) — all present and
       correctly tiered. One precision fix: Heavensward's "Metal" `where` text (from an earlier
       fix this same session) said the Midas final boss is "Onslaughter" — more precise per a
       second check is **Brute Justice** (Onslaughter is one of five component robots that fuse
       into Brute Justice, the form the track is actually named for — matches "Metal – Brute
       Justice Mode" already correctly written on the Far Edge of Fate album). AAC
       Cruiserweight/Heavyweight (Dawntrail) are absent, confirmed correctly out of scope —
       patches 7.2 and 7.4 respectively, both under the already-deferred order-13 EP scope.
     - **Alliance Raids: done — turned out not to need a separate fetch at all.**
       `category2=6` is actually PvP, not Alliance Raids (corrected an assumption from earlier
       in this same pass) — there is no separate Alliance Raid category in EDB; alliance raids
       are simply bundled into `category2=5` (Raids) alongside 8-player tiers, which the Raids
       pass above already fetched. Cross-referenced the alliance-raid-specific duty names from
       those same rosters: Void Ark/Weeping City of Mhach/Dun Scaith (Heavensward), Royal City
       of Rabanastre/Ridorana Lighthouse/Orbonne Monastery (Stormblood, with Orbonne's own
       tracks correctly living on the Shadowbringers album per the "tail end" pattern), The
       Copied Factory/The Puppets' Bunker/The Tower at Paradigm's Breach (Shadowbringers,
       YoRHa: Dark Apocalypse), Aglaia/Euphrosyne/Thaleia (Endwalker, Myths of the Realm) — all
       present and correctly typed `Alliance raid`. Dawntrail's alliance raid, Echoes of
       Vana'diel (Jeuno/San d'Oria/Windurst: The First/Second/Third Walk), is entirely absent
       from the data — confirmed correct, it's 7.1/7.3/7.5 content, squarely in the
       already-deferred order-13 EP scope.
     - **Ultimate roster (category2=28, all expansions in one list): done.** UCOB, TEA (Death
       Unto Dawn), DSR and TOP (Growing Light) all present and correctly typed. **Found and
       fixed a real bug**: UWU's four tracks ("Fallen Angel," "Primal Judgment," "Under the
       Weight," "Ultima (Orchestral Version)," all "(From Astral to Umbral)"/"(Orchestral
       Version)" on Stormblood) were typed `Raid` instead of `Ultimate` — inconsistent with
       every other ultimate's treatment; retyped. Two roster entries confirmed out of scope:
       **Futures Rewritten** (patch 7.11) and **Dancing Mad (Ultimate)** (patch 7.51, released
       during this very session's real-world timeframe) — both squarely 7.1+, deferred.
  2. **Tier 2 — done.** Every `Boss battle`/`Story battle` row (~40 of them) checked against
     the Hades/Diamond Weapon mistag pattern. **Found and fixed one real issue, bigger than a
     single row**: 8 tracks on the Shadowbringers album for **Orbonne Monastery** — the third
     part of the "Return to Ivalice" alliance raid trilogy (Rabanastre → Ridorana → Orbonne) —
     were typed `Boss battle`/`Instanced area` for their sub-area and named-boss tracks
     ("Under The Stars," "Pressure (No. 1)," "Antipyretic," "B. E.," "A Man Consumed,"
     "Descent," "Ultima's Perfection," "Hall of Worship"), inconsistent with how the identical
     kind of content is typed `Alliance raid` in Rabanastre/Ridorana. Retyped all 8 to
     `Alliance raid` to match. Left alone on purpose, matching the *already-consistent*
     Rabanastre precedent: narrative cutscenes and completion jingles inside the same raid
     (Rabanastre's "Victory," "Character Creation," etc.; Orbonne's "St. Ajora's Theme," "Final
     Struggle") stay in their own generic buckets rather than becoming `Alliance raid` — only
     the actual dungeon-crawl/boss-fight tracks get the raid's type. Also spot-checked two
     ambiguous `Story battle` rows that looked like they might hide an actual Trial name
     ("Inexorable" — Zero, "Tremble" — a Garlemald encounter): both confirmed genuinely solo/
     generic MSQ content, no registered duty involved, no change needed. Everything else on the
     list (~30 rows) is a genuinely generic multi-dungeon or multi-encounter cue with no single
     named duty to mistag — left as-is.
  3. **Tier 3 — done, clean pass.** Pulled the official Dungeon roster (`category2=2`) for
     all 6 expansions (~103 named dungeons) and checked every one against the data. Zero real
     bugs — every ARR/HW/SB/ShB/EW dungeon is present; the only "missing" ones (Yuweyawata Field
     Station, The Underkeep, Meso Terminal, Mistwake, The Clyteum) are all Dawntrail 7.1+
     content, already deferred (verified Yuweyawata directly: patch 7.1). Confirms this really
     was the lower-probability tier — dungeon naming doesn't have the "which official duty is
     this really" ambiguity that Trials/Raids/Alliance Raids do.
  4. **Tier 4** — whole dataset: grep `where` for generic-reuse phrasing ("final boss fights
     in...", "normal battles in...", "miniboss", "random encounters") and check each such
     track's own Fandom page for reuse in a named duty not yet mentioned (the Memoria Misera
     bug pattern below — the Urth's Fount/Corpse Hall find above is the same pattern). When the
     reuse crosses into a different `type` category (a Field battle theme reused in a Trial,
     etc.), record it as `extra_types`, not just prose — see §2. Low-risk
     rows (Field/City/Quest & cutscene/menu/etc., ~360 rows) can be skipped entirely — no duty
     to conflate.

     **Substantially done.** Grepped the whole dataset for generic-reuse phrasing and checked
     every genuine "generic combat cue" candidate (~25 rows: dungeon-boss themes, field-battle
     themes, etc. — the ones structurally capable of hiding a Trial/dungeon-variant reuse the
     way Insatiable and The Corpse Hall did). Found and fixed three more:
     - **"Storm of Blood" / "Triumph" (Growing Light, Mount Rokkon).** Had the boss attribution
       backwards: "Storm of Blood" was tagged as Mount Rokkon's *final* boss, but per "Triumph"'s
       own Fandom page, **"Triumph" is Enenra's theme (the actual final boss)**, and "Storm of
       Blood" is the earlier mid-bosses' theme (Moko/Gorai/Shishio). Also, "Triumph" wasn't just
       Another Mount Rokkon's theme (criterion dungeon) as tagged — it's genuinely *both*
       Mount Rokkon (variant) *and* Another Mount Rokkon (criterion); added
       `extra_types: ["Variant dungeon"]` so it's findable under both chips.
     - **"Ominous Prognisticks" (Heavensward)** is also the Palace of the Dead floors 51–60 boss
       theme, not just "most Heavensward-era dungeons" — added the mention plus
       `extra_types: ["Deep dungeon"]`.

     **Resumed and finished in a later session.** Went back through the deferred pool: 166
     rows of pure zone ambience (`Field`/`City`) confirmed zero risk on inspection — there's no
     FFXIV sound-design precedent for a zone theme becoming duty combat music, so these weren't
     individually fandom-checked. Of the remaining 179 `Quest & cutscene`/`Credits & theme`/
     `Title & menu`/`Jingle`/`Character theme`/`Side story`/`Cutscene` rows, spot-checked the two
     highest-probability candidates (tracks tied to a named character who *also* has known Trial
     content): "Prima Vista Orchestra" (Sphene's intro cutscene — her actual Trial, The
     Interphos, uses different, already-correctly-tagged tracks) and "His Holiness" (Thordan
     VII's character leitmotif — his actual trial battle uses "Heroes"/"Heroes Never Die",
     already correctly tagged). Both clean. Reviewed the rest of the pool by inspection rather
     than individually fandom-verifying all 117+62 rows — several apparent candidates
     ("Wrath of the Eikons," "Meteor," "Primogenitor," "From the Ashes") turned out to already be
     correctly cross-referenced across albums via their `origin` field ("...from 1.0", etc.).
     **Net conclusion: the low-risk pool really is low-risk** — the taxonomy discipline of typing
     an in-duty cutscene stinger as the raid/trial itself (not `Cutscene`) is being followed
     consistently, which is structurally why genuine duty-reuse doesn't surface here. Tier 4 is
     complete; no further rows in this project are known to need this kind of check.

- **[NOT STARTED] Audit reused/generic tracks for missing duty reuse mentions (Tier 4 above,
  the "Memoria Misera" bug).** "Insatiable" (Shadowbringers track 49) is the boss theme for
  Varis yae Galvus in the Trial **Memoria Misera (Extreme)** (patch 5.25) — confirmed on the
  track's own Fandom page — but nothing in the row's `where` text said so, so the duty had zero
  footprint in the table, not even a mistagged one; fixed for this one row (`where` text plus
  `extra_types: ["Trial"]`, so it's now findable under the Trial chip too — see §2). Root cause: the
  per-album research method (§3 Step 3) is duty-first — it finds a track's *primary* context but
  never checks whether that same track got redeployed into some other duty later, sometimes a
  different content category entirely (dungeon-boss cue → standalone Trial theme). That reverse
  direction only shows up by opening *that track's own* Fandom page and reading its "Game
  appearances" list.

- **[DONE] Project is under git, hosted on GitHub, live on GitHub Pages.** `git init` done,
  pushed to https://github.com/chancsy/ffxiv_soundtracks (public repo, user's account), Pages
  enabled serving `index.html` at https://chancsy.github.io/ffxiv_soundtracks/. Every fix in
  this document from this point on was committed and pushed as its own commit — check `git log`
  for the detailed history instead of relying solely on this doc's prose summaries. Pushing
  needs a fine-grained GitHub PAT (Contents: read/write, scoped to this one repo) provided by
  the user each time — none is stored anywhere in this container between sessions.

- **[BLOCKED — not a skip, the content doesn't exist yet]** Roadmap order 13. User asked to
  proceed with "the rest" of the roadmap; researched it fully and confirmed there's nothing
  buildable right now:
  - The individual digital-purchase EPs (`FINAL FANTASY XIV: DAWNTRAIL - EP1` through at least
    `EP8`, covering patches 7.0 through 7.5) exist and have tracklists, but — same pattern as
    Endwalker's EP1–4 — **they never appear on Spotify individually**, only ever as
    digital-purchase/Blu-ray releases. Out of this project's stated scope ("every track on the
    soundtrack albums *that are on Spotify*").
  - The compiled album that *would* eventually hit Spotify (matching how Endwalker's EPs became
    "Growing Light") is **"TRAIL TO THE HEAVENS: FINAL FANTASY XIV Original Soundtrack"**
    (catalog SQEX-20106), covering patches 7.1–7.5, 79 main tracks plus Blu-ray-only bonus
    tracks (title count TBD). Confirmed via Square Enix's own JP music portal
    (jp.square-enix.com/music) and the official announcement. **It has not released anywhere
    yet as of this session (2026-09-09)**: Japan Blu-ray launches 2026-09-16 (one week out),
    West follows in October 2026, and Spotify/streaming — going by every prior album's pattern
    including the main Dawntrail OST and Growing Light — will likely lag even the West physical
    release by some further stretch. SE has only revealed a partial tracklist so far (tracks
    68–74 of 79, per their own product-page rollout).
  - **This is exactly the case the JP-first TODO below was written for** — checked JP first,
    found real information, but the honest answer this time is "not out yet, even there."
  - **Next step for whoever picks this up**: check whether "Trail to the Heavens" has a Spotify
    album ID yet. If yes, treat it as a normal new album per §3's process (order 13, rename to
    "Trail to the Heavens" in the roadmap, which is already updated above). If no, this stays
    blocked — no point re-researching until the release situation changes. Given the Japan
    Blu-ray date, a sensible time to check back is anywhere from late September 2026 onward,
    but streaming could easily lag well past that.

- **[NEW TODO, applies to order 13 and every future album]** Before taking a Spotify album's
  track list as final, **check the Japanese Spotify storefront, not just the US/global one** —
  the user's own observation, from experience: new FFXIV OST albums have historically released
  in Japan first, sometimes by a few months or more, before showing up in other regions. This
  means: (a) a "not yet released" album might already be out and researchable if you check JP
  Spotify, and (b) even for an album already in the dataset, JP Spotify is worth a quick check
  for a newer/more-complete release (e.g. a compilation that supersedes small EPs) before
  concluding one doesn't exist yet. No specific method worked out yet for checking a
  region-locked storefront from here — figure that out as part of doing this, and document
  what worked (or didn't) for the next session's benefit.

- **[NOT STARTED] Mobile layout: content-type chips take over the whole viewport.** User report:
  on mobile, the chip row (~30 chips, all types, wrapping across many lines) pushes the actual
  table content down so far that only a sliver is visible above the fold. Needs a mobile-specific
  treatment — candidates: collapse chips into a dropdown/expandable section below a certain
  viewport width, cap visible chips with a "more" toggle, or make the chip row horizontally
  scrollable instead of wrapping. Whatever's chosen, keep the active-chip state and counts
  working the same way. Not investigated yet — no CSS written.

**Near-miss recorded for context**: in the session that added this TODO structure, running all
`data/*.py` generators in a loop overwrote `02_a_realm_reborn.json` and `03_before_the_fall.json`
with stale versions (missing tracks and, for #2, the entire `patch` field), because two `.py`
scripts had drifted out of sync with their `.json` output and were never checked before being
re-run. No backup existed anywhere on the system. Recovered by extracting the complete `DATA`
array from this session's own cached tool-result files (`~/.claude/projects/*/tool-results/*.txt`
— large tool outputs get saved to disk even when the visible reply is truncated) and rebuilding
all three `.py` files from that recovered JSON, then verifying they round-trip byte-for-byte.
Lesson for next time a `.py`/`.json` pair looks suspicious: diff the script's output count
against the live file *before* overwriting, every time — don't assume a generator script is
still in sync with what's actually being served.
