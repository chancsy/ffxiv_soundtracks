# Handover — open items only

Everything about how this project works — data schema, conventions, research method, roadmap,
design rationale — now lives in **README.md**. Read that first. This file is just the current
backlog: what's actually open right now, kept short on purpose. Detailed history of past fixes
lives in `git log`, not here — each fix was committed individually with a descriptive message.

## Open

- **Roadmap order 13, "Trail to the Heavens," is blocked — not skipped by choice, the content
  doesn't exist yet.** The compiled album that will eventually cover patches 7.1–7.5 on Spotify
  (catalog SQEX-20106, 79 tracks + Blu-ray-only bonus tracks) hasn't released anywhere as of
  this writing: Japan Blu-ray launches 2026-09-16, West follows in October 2026, and streaming
  will likely lag further still (same pattern as the main Dawntrail OST and Growing Light, both
  digital/physical before streaming). The individual digital-purchase EPs that already exist
  (`DAWNTRAIL - EP1` through at least `EP8`) never appear on Spotify individually — same
  pattern as Endwalker's EPs before *Growing Light* compiled them — so they're out of this
  project's scope regardless of release date.

  **Next step**: check whether "Trail to the Heavens" has a Spotify album ID yet (check the
  Japanese storefront first — see README's Conventions). If yes, research and build it like any
  other album. If no, leave this blocked rather than re-researching on a schedule.

## Recently completed (for context, not action)

- Full accuracy audit across every Trial/Raid/Alliance Raid/Ultimate/Dungeon and reused-track
  row in the dataset, cross-checked against the official Eorzea Database duty rosters and each
  track's own Fandom page. Found and fixed a couple dozen real mistags, wrong duty names, and
  missing duty-reuse mentions along the way. See `git log` for the specific fixes — search for
  commits mentioning "Tier 1" through "Tier 4" for the full trail.
- Project moved under git, pushed to GitHub, live on GitHub Pages (see README's Repository
  section).
- Mobile layout fix for the content-type chip row (was consuming the whole viewport on small
  screens; now scrolls horizontally).
