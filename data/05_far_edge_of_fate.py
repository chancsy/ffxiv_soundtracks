import json, pathlib

# (album track no., title, content type, where it plays, origin, patch)
T = [
(1,"Fiend","Trial","Containment Bay S1T7 — Sephirot, final phase (normal and Extreme)","Soken; lyrics Fox; vocals Dan Inoue","3.2"),
(2,"Down the Up Staircase","Dungeon","The Antitower","Soken","3.2"),
(3,"Dancing Calcabrina","Boss battle","The Antitower — final boss (Calcabrina)","Uematsu","3.2"),
(4,"Revenge Twofold","Boss battle","Second final boss theme in Heavensward-era dungeons as of patch 3.4","Soken","3.4"),
(5,"Piece of Mind","Tribal quest","Vath beast tribe theme","Takada","3.5"),
(6,"No Sound, No Scutter","Tribal quest","Vath beast tribe quests","Takada","3.5"),
(7,"The Kiss","Seasonal event","Valentione's Day (2017)","Takada","3.5"),
(8,"Starved","PvP","The Feast","Soken","3.2"),
(9,"The Ancient City","Dungeon","The Lost City of Amdapor (Hard)","Soken","3.2"),
(10,"Metal – Brute Justice Mode","Raid","Alexander: The Burden of the Son — once Brute Justice appears","Soken; vocals Fox","3.2"),
(11,"Holy Consult","Dungeon","Hullbreaker Isle (Hard)","Uematsu","3.2"),
(12,"Apologies","Dungeon","Sohr Khai","Soken","3.3"),
(13,"Faith in Her Fury","Trial","The Steps of Faith","Soken","2.55"),
(14,"Primogenitor","Boss battle","Midgardsormr's theme; final boss of Keeper of the Lake","Soken","3.0"),
(15,"Freefall","Trial","The Final Steps of Faith — Nidhogg, second part","Soken","3.3"),
(16,"Revenge of the Horde","Trial","The Final Steps of Faith — Nidhogg, third part","Soken; lyrics Fox","3.3"),
(17,"Only the Dead","Quest & cutscene","Dragonsong War MSQ finale, Litany of Peace cutscene; remix of \"Night in the Brume\"","Soken","3.3"),
(18,"Freedom","Instanced area","Old 1.0 theme of La Noscea; reused in The Parrock during the Shadow of Mhach quest series","Uematsu; from 1.0","3.3"),
(19,"Teardrops in the Rain","Alliance raid","The Weeping City of Mhach — ambient","Soken","3.3"),
(20,"Torrent","Alliance raid","The Weeping City of Mhach — battles","Soken","3.3"),
(21,"A Thousand Faces","Alliance raid","The Weeping City of Mhach — Ozma, Black Hole phase","Soken","3.3"),
(22,"Blackbosom","Deep dungeon","Palace of the Dead, floor 50 boss (Edda Blackbosom)","Soken","3.3"),
(23,"The Merry Wanderer Waltz","Deep dungeon","Palace of the Dead — main ambient theme","Soken","3.3"),
(24,"Emerald Labyrinth","Deep dungeon","Old 1.0 theme of the Black Shroud; reused as Palace of the Dead ambient","Uematsu; from 1.0","3.3"),
(25,"Enraptured","Deep dungeon","Old 1.0 theme reused as Palace of the Dead ambient","Uematsu; from 1.0","3.3"),
(26,"Tears for Mor Dhona","Deep dungeon","Old 1.0 theme of Mor Dhona; reused as Palace of the Dead ambient","Uematsu; from 1.0","3.3"),
(27,"Fog of Phantom","Deep dungeon","Palace of the Dead, floors 97–100 ambient","Iwata","3.3"),
(28,"Notice of Death","Deep dungeon","Palace of the Dead — Nybeth Obdilord cutscenes","Sakimoto","3.3"),
(29,"Blasphemous Experiment","Deep dungeon","Palace of the Dead, floor 100 boss (Nybeth Obdilord)","Iwata","3.3"),
(30,"The Gauntlet","PvP","Wolves' Den — The Dueling Circle 1v1 duels","Soken","3.2"),
(31,"Hyper Rainbow Z","Tribal quest","Final cutscene of an Allied Society (beast tribe) quest chain","Takada","3.4"),
(32,"Up at Dawn","Seasonal event","Haunted Manor during All Saints' Wake (2016)","Takada","3.4"),
(33,"Grounded","Dungeon","Xelphatol","Uematsu","3.4"),
(34,"Bibliophobia","Dungeon","The Great Gubal Library (Hard)","Soken","3.4"),
(35,"Exponential Entropy","Raid","Alexander: The Heart of the Creator — boss battle","Soken; lyrics Fox; vocals Fox","3.4"),
(36,"Out of Time","Raid","Alexander: The Soul of the Creator — muted remix of \"Exponential Entropy\", heard only inside Alexander Prime's portals","Soken","3.4"),
(37,"Moebius","Raid","Alexander: The Soul of the Creator — main battle theme until Judgement","Soken","3.4"),
(38,"Stasis Loop","Raid","Alexander: The Soul of the Creator — during Temporal Stasis","Soken","3.4"),
(39,"Rise","Raid","Alexander: The Soul of the Creator — third phase","Soken; lyrics Fox; vocals Fox","3.4"),
(40,"Fragments of Forever","Quest & cutscene","Old 1.0 theme; plays during heartwarming story moments","Uematsu; from 1.0","3.0"),
(41,"He Who Continues the Attack","Quest & cutscene","Warring Triad trial quest series — Regula van Hydrus cutscenes","Soken","3.2"),
(42,"Battle to the Death – Heavensward","Trial","Warring Triad — first phase of Sephirot, Sophia and Zurvan (normal)","Uematsu","3.2"),
(43,"Equilibrium","Trial","Containment Bay P1T6 — Sophia, final phase (normal and Extreme)","Soken; lyrics Fox; vocals Ayumi Murata","3.4"),
(44,"Promises","Alliance raid","Dun Scaith — first boss","Soken","3.5"),
(45,"Shadow of the Body","Alliance raid","Dun Scaith — ambient","Soken","3.5"),
(46,"Quicksand","Dungeon","Sohm Al (Hard)","Uematsu","3.5"),
(47,"Penultimania","Trial","Containment Bay Z1T9 — Zurvan, second phase (normal and Extreme)","Soken","3.5"),
(48,"Infinity","Trial","Containment Bay Z1T9 — Zurvan, third phase (normal and Extreme)","Soken","3.5"),
(49,"Another Brick","Dungeon","Baelsar's Wall","Soken","3.5"),
(50,"Scale and Steel","Quest & cutscene","Omega vs. Shinryu in \"Fly Free, My Pretty\"; reprised in The Royal Menagerie","Soken","3.5","extra:Trial"),
]

album = {
 "order": 5,
 "album": "The Far Edge of Fate",
 "full": "THE FAR EDGE OF FATE: FINAL FANTASY XIV Original Soundtrack",
 "year": 2017,
 "covers": "Patches 3.2 – 3.56",
 "spotify": "73mih5aIcuQ4OaQLI7O0X9",
 "tracks": [
   {"n": n, "title": t, "type": c, "where": w, "origin": o, "patch": p,
    **({"extra_types": [r.split(":",1)[1] for r in rest if r.startswith("extra:")]} if any(r.startswith("extra:") for r in rest) else {})}
   for (n, t, c, w, o, p, *rest) in T
 ],
}
ROOT = pathlib.Path(__file__).resolve().parent
(ROOT / "05_far_edge_of_fate.json").write_text(json.dumps(album, indent=1))
print(len(T), "tracks written")
